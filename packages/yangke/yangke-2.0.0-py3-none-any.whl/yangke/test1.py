# from yangke import start_update_stocks_data
# from yangke.base import yield_all_file
# from yangke.objDetect.ocr import ocr
#
# start_update_stocks_data('mysql', '101.37.118.81', '3306', 'root', 'YangKe.08', 'stocks')

import threading
import time
from functools import wraps


def timeout(seconds=5, callback=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 定义一个线程局部变量来存储函数结果
            result = None
            exception = None

            def target():
                nonlocal result, exception
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    exception = e

            # 创建并启动线程
            thread = threading.Thread(target=target)
            thread.start()

            # 等待线程完成，最多等待 seconds 秒
            thread.join(seconds)

            # 如果线程仍然存活，说明函数执行超时
            if thread.is_alive():
                if callback is not None:
                    callback()  # 调用回调函数
                raise TimeoutError(f"Function {func.__name__} timed out after {seconds} seconds")

            # 如果函数抛出了异常，重新抛出
            if exception is not None:
                raise exception

            return result

        return wrapper

    return decorator


# 使用示例
def timeout_callback():
    print("Timeout occurred! Executing callback...")


@timeout(seconds=5)
def long_running_function():
    time.sleep(3)
    return "Function completed"


try:
    result = long_running_function()
    print(result)
except TimeoutError as e:
    print(e)
