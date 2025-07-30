import time
import sys
import functools
from threading import Thread, Event, Lock
from typing import Callable, Any, Union, Tuple, Type




# ================================================== 单次定时器 ==================================================
def setTimeout(sleepTime: float, awaitResult: bool = False) -> Callable[[Callable], Callable]:
    """
    单次定时器装饰器工厂
    :param sleepTime: 延迟时间（秒）
    :param awaitResult: 是否同步等待结果
    :raises ValueError: 当延迟时间为负数时抛出
    """

    # 校验参数
    if sleepTime < 0: raise ValueError("延迟时间不能为负数")

    # 定义装饰器
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # 使用列表存储结果以实现闭包效果
            resultContainer = [None]
            exceptionContainer = [None]

            # 定义任务函数
            def task():
                try:
                    time.sleep(sleepTime)
                    resultContainer[0] = func(*args, **kwargs)  # 执行目标函数
                except Exception as e: exceptionContainer[0] = e  # 捕获异常

            # 启动任务线程
            taskThread = Thread(target=task)
            taskThread.start()

            # 等待结果（同步模式）
            if awaitResult:
                taskThread.join()
                if exceptionContainer[0]:  raise exceptionContainer[0] # 如果有异常则重新抛出
                return resultContainer[0]
            
            # 异步模式返回任务线程对象
            return taskThread.join(0)  
        return wrapper
    return decorator



# ================================================== 循环定时器 ==================================================
class IntervalController:
    # 循环定时器控制器（用于停止定时任务）
    def __init__(self):
        self._stopEvent = Event()  # 停止事件标志
        self._thread: Union[Thread, None] = None  # 工作线程引用

    # 停止定时循环
    def stop(self):
        self._stopEvent.set()  # 设置停止标志
        if self._thread and self._thread.is_alive():
            self._thread.join()  # 等待线程结束

    # 检查定时器是否在运行
    def isRunning(self) -> bool:  # 修正方法名
        return not self._stopEvent.is_set()


def setInterval(interval: float, endTime: float = 0) -> Callable[[Callable], Callable]:
    """
    循环定时器装饰器工厂
    :param interval: 执行间隔（秒）
    :param endTime: 最大持续时间（秒），0表示无限
    :raises ValueError: 时间参数为负数时抛出
    """

    # 校验参数
    if interval < 0 or endTime < 0: raise ValueError("时间参数不能为负数")

    # 定义装饰器
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> IntervalController:
            # 创建控制器对象
            controller = IntervalController()
            endTimestamp = time.time() + endTime if endTime > interval else float('inf')  # 计算结束时间戳

            
            def task():
                while not controller._stopEvent.is_set():
                    controller._stopEvent.wait(max(0, interval))  # 带停止检测的等待
                    if time.time() >= endTimestamp: break

                    # 执行目标函数
                    try: func(*args, **kwargs)
                    except Exception as e:
                        print(f"定时任务执行失败: {str(e)}")
                        break

            # 启动任务线程
            controller._thread = Thread(target=task)
            controller._thread.start()

            # 返回控制器对象
            return controller
        return wrapper
    return decorator



# ================================================== 耗时计算 ==================================================
def timeIt(showMessage: bool = True) -> Callable[[Callable], Callable]:
    """
    耗时统计装饰器工厂
    :param showMessage: 是否直接打印耗时信息
    :return: 返回原始结果或(结果, 耗时)元组
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Union[Any, Tuple[Any, float]]:
            start = time.perf_counter()  # 高精度计时开始
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start  # 计算耗时

            # 判断是否显示耗时信息
            if showMessage:
                print(f"函数 {func.__name__} 执行耗时: {elapsed:.5f}秒")
                return result
            
            # 返回结果和耗时
            return result, elapsed
        return wrapper
    return decorator



# ================================================== 异常处理 ==================================================
def catch(
    exceptionToHandle: Union[Type[Exception], Tuple[Type[Exception]]] = Exception,
    defaultValue: Any = None,
    reRaise: bool = False,
    showError: bool = True
) -> Tuple[Callable[[Callable], Callable], Any]:
    """
    异常捕获装饰器工厂
    :param exceptionToHandle: 要捕获的异常类型
    :param defaultValue: 异常发生时返回的默认值
    :param reRaise: 是否重新抛出异常
    :param showError: 是否显示错误信息
    :return: 装饰器函数和默认值
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # 捕获异常并返回默认值
            try: return func(*args, **kwargs)  # 正常执行
            except exceptionToHandle as e:
                if showError: print(f"[异常捕获 {func.__name__}], 错误信息: [{str(e)}]")
                if reRaise: raise # 重新抛出异常开关
                return (defaultValue, e)  # 返回元组

        # 包装后的函数
        return wrapper
    return decorator



# ================================================== 全局异常捕获 ==================================================
def _catchAllErrors(func: Callable, showError: bool = True, defaultValue: Any = None) -> Tuple[Callable[[Callable], Callable], Any]:
    """
    内部实现的全局异常捕获装饰器
    :param func: 需要装饰的目标函数
    :param showError: 是否显示错误信息
    :param defaultValue: 异常发生时返回的默认值
    :return: 装饰器函数和默认值
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try: return func(*args, **kwargs)
        except Exception as e:
            if showError: print(f"[异常捕获 {func.__name__}], 错误信息: [{str(e)}]")
            return (defaultValue, e)
    return wrapper


def catchAll(name: str, error: bool = True, value: Any = None) -> Tuple[Callable[[Callable], Callable], Any]:
    """
    模块级全局异常捕获
    :param name: 需要处理的模块名称
    :param error: 是否显示错误信息
    :param value: 异常发生时返回的默认值
    :return: 装饰器函数和默认值
    """
    # 获取模块对象
    targetModule = sys.modules.get(name)
    if not targetModule: raise ValueError(f"找不到模块: {name}")

    # 遍历模块所有成员
    for attrName in dir(targetModule):
        # 获取成员对象
        attr = getattr(targetModule, attrName)

        # 仅处理用户定义的函数
        if callable(attr) and not isinstance(attr, type):
            try:
                # 添加异常捕获装饰器
                wrappedFunc = _catchAllErrors(attr, error, value)
                setattr(targetModule, attrName, wrappedFunc)
            except Exception as e: 
                if error: print(f"处理函数 {attrName} 时发生错误: {str(e)}")
                return e



# ================================================== 调用限制 ==================================================
def callLimit(maxCalls: int, defaultValue: Any = None) -> Callable[[Callable], Callable]:
    """
    调用次数限制装饰器工厂（线程安全版）
    :param maxCalls: 最大允许调用次数
    :param defaultValue: 超限后返回值
    """
    def decorator(func: Callable) -> Callable:
        lock = Lock()  # 线程锁
        callCount = 0  # 调用计数器

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # 保证原子操作
            nonlocal callCount

            # 循环计数器
            with lock:  
                if callCount >= maxCalls: return defaultValue  # 超限
                callCount += 1  # 计数加1

            # 执行目标函数
            return func(*args, **kwargs)
        return wrapper
    return decorator



# ================================================== 失败重试 ==================================================
def retry(
    maxAttempts: int = 3,
    delay: float = 0,
    exceptions: Union[Type[Exception], Tuple[Type[Exception]]] = Exception,
    showError: bool = True
) -> Callable[[Callable], Callable]:
    """
    失败重试装饰器工厂
    :param maxAttempts: 最大尝试次数
    :param delay: 重试延迟时间（秒）
    :param exceptions: 要捕获的异常类型
    :param showError: 是否显示错误信息
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        @catch(showError = showError)
        def wrapper(*args, **kwargs) -> Any:
            # 尝试执行目标函数
            for attempt in range(1, maxAttempts + 1):
                # 捕获异常并重试
                try: return func(*args, **kwargs)
                except exceptions as e:
                    if showError: print(f"第 {attempt} 次尝试失败: {str(e)}")
                    if attempt == maxAttempts: raise  # 最后一次尝试失败后抛出异常
                    time.sleep(delay)  # 重试前等待

            return func(*args, **kwargs)  # 最后一次尝试
        return wrapper
    return decorator
