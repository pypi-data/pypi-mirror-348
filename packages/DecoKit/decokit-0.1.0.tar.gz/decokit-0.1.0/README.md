# `DecoKit` 使用文档

## 一、概述
`DecoKit` 是一个 Python 模块，提供了多个实用的装饰器，可用于实现定时器、耗时计算、异常处理、调用限制和失败重试等功能，能帮助开发者更高效地管理函数的执行。

## 二、导入模块
在使用这些装饰器之前，需要先安装 `DecoKit` 模块，示例如下：

```bash
pip install DecoKit
```

```python
from DecoKit import setTimeout, setInterval, timeIt, catch, catchAll, callLimit, retry
```

## 三、各装饰器详细使用说明

### 1. 单次定时器 (`setTimeout`)
#### 功能
该装饰器可让被装饰的函数在指定的延迟时间后执行。
#### 参数
- `sleepTime`：延迟时间，单位为秒，必须为非负数。
- `awaitResult`：布尔值，指示是否同步等待函数执行结果，默认为 `False`。
#### 示例代码
```python
# 导入单次定时器装饰器
from DecoKit import setTimeout

# 使用 setTimeout 装饰器，设置延迟 2 秒后执行函数，且同步等待结果
@setTimeout(sleepTime=2, awaitResult=True)
def my_function():
    print("此函数在延迟 2 秒后被调用。")

# 调用被装饰的函数
my_function()
```
#### 代码解释
- `@setTimeout(sleepTime=2, awaitResult=True)`：使用 `setTimeout` 装饰器，设置延迟 2 秒后执行 `my_function`，并同步等待结果。
- `my_function()`：调用被装饰的函数，函数会在 2 秒后执行。

### 2. 循环定时器 (`setInterval`)
#### 功能
该装饰器能让被装饰的函数按指定的时间间隔循环执行。
#### 参数
- `interval`：函数执行的时间间隔，单位为秒，必须为非负数。
- `endTime`：最大持续时间，单位为秒，0 表示无限循环，必须为非负数。
#### 示例代码
```python
# 导入循环定时器装饰器
from DecoKit import setInterval

# 使用 setInterval 装饰器，设置函数每隔 1 秒执行一次，持续 5 秒
@setInterval(interval=1, endTime=5)
def my_function():
    print("此函数每秒被调用一次，持续 5 秒。")

# 调用被装饰的函数，返回一个控制器对象
controller = my_function()

# 若要提前停止定时任务，可调用控制器的 stop 方法
# controller.stop()
```
#### 代码解释
- `@setInterval(interval=1, endTime=5)`：使用 `setInterval` 装饰器，设置 `my_function` 每隔 1 秒执行一次，持续 5 秒。
- `controller = my_function()`：调用被装饰的函数，返回一个 `IntervalController` 对象，可用于停止定时任务。
- `controller.stop()`：调用控制器的 `stop` 方法可提前停止定时任务。

### 3. 耗时计算 (`timeIt`)
#### 功能
该装饰器用于统计被装饰函数的执行耗时。
#### 参数
- `showMessage`：布尔值，指示是否直接打印耗时信息，默认为 `True`。
#### 示例代码
```python
# 导入耗时计算装饰器
from DecoKit import timeIt

# 使用 timeIt 装饰器，设置显示耗时信息
@timeIt(showMessage=True)
def my_function():
    sum = 0
    for i in range(1000000):
        sum += i
    return sum

# 调用被装饰的函数
result = my_function()
```
#### 代码解释
- `@timeIt(showMessage=True)`：使用 `timeIt` 装饰器，设置显示 `my_function` 的执行耗时信息。
- `result = my_function()`：调用被装饰的函数，函数执行完成后会打印耗时信息。

### 4. 异常处理 (`catch`)
#### 功能
该装饰器用于捕获被装饰函数的指定异常，并在异常发生时返回默认值。
#### 参数
- `exceptionToHandle`：要捕获的异常类型，默认为 `Exception`。
- `defaultValue`：异常发生时返回的默认值，默认为 `None`。
- `reRaise`：布尔值，指示是否重新抛出异常，默认为 `False`。
- `showError`：布尔值，指示是否显示错误信息，默认为 `True`。
#### 示例代码
```python
# 导入异常处理装饰器
from DecoKit import catch

# 使用 catch 装饰器，捕获 ZeroDivisionError 异常，异常发生时返回 None，不重新抛出异常，显示错误信息
@catch(exceptionToHandle=ZeroDivisionError, defaultValue=None, reRaise=False, showError=True)
def my_function():
    return 1 / 0

# 调用被装饰的函数
result = my_function()
```
#### 代码解释
- `@catch(exceptionToHandle=ZeroDivisionError, defaultValue=None, reRaise=False, showError=True)`：使用 `catch` 装饰器，捕获 `ZeroDivisionError` 异常，异常发生时返回 `None`，不重新抛出异常，显示错误信息。
- `result = my_function()`：调用被装饰的函数，若发生 `ZeroDivisionError` 异常，会显示错误信息并返回 `None`。

### 5. 全局异常捕获 (`catchAll`)
#### 功能
该装饰器用于为指定模块中的所有用户定义函数添加全局异常捕获。
#### 参数
- `name`：需要处理的模块名称。
- `error`：布尔值，指示是否显示错误信息，默认为 `True`。
- `value`：异常发生时返回的默认值，默认为 `None`。
#### 示例代码
```python
# 导入全局异常捕获装饰器
from DecoKit import catchAll

def my_function():
    raise ValueError("错误发生。")

def my_function2():
    return 1 / 0

# 在函数定义之后使用 catchAll 装饰器，为当前模块（__main__）中的所有用户定义函数添加全局异常捕获，显示错误信息，异常发生时返回 None
catchAll(__main__)

decorator()

decorator()
```
#### 代码解释
- `catchAll(__main__)`：使用 `catchAll` 装饰器，为当前模块（__main__）中的所有用户定义函数添加全局异常捕获，显示错误信息，异常发生时返回 `None`。

### 6. 调用限制 (`callLimit`)
#### 功能
该装饰器用于限制被装饰函数的最大调用次数。
#### 参数
- `maxCalls`：最大允许调用次数。
- `defaultValue`：调用次数超过限制后返回的值，默认为 `None`。
#### 示例代码
```python
# 导入调用限制装饰器
from DecoKit import callLimit

# 使用 callLimit 装饰器，设置函数最多调用 3 次，超限后返回 None
@callLimit(maxCalls=3, defaultValue=None)
def my_function():
    print("此函数最多只能被调用 3 次。")

# 循环调用被装饰的函数 5 次
for i in range(5):
    my_function()
```
#### 代码解释
- `@callLimit(maxCalls=3, defaultValue=None)`：使用 `callLimit` 装饰器，设置 `my_function` 最多调用 3 次，调用次数超过 3 次后返回 `None`。
- `for i in range(5): my_function()`：循环调用 `my_function` 5 次，前 3 次正常执行，后 2 次返回 `None`。

### 7. 失败重试 (`retry`)
#### 功能
该装饰器用于在被装饰函数执行失败时进行重试。
#### 参数
- `maxAttempts`：最大尝试次数，默认为 3。
- `delay`：重试延迟时间，单位为秒，默认为 0。
- `exceptions`：要捕获的异常类型，默认为 `Exception`。
- `showError`：布尔值，指示是否显示错误信息，默认为 `True`。
#### 示例代码
```python
# 导入失败重试装饰器
from DecoKit import retry
import random

# 使用 retry 装饰器，设置最大尝试次数为 3 次，重试延迟为 1 秒，捕获所有异常，显示错误信息
@retry(maxAttempts=3, delay=1, exceptions=Exception, showError=True)
def my_function():
    # 模拟随机出错
    if random.random() < 0.5:
        raise ValueError("随机错误发生。")
    return "成功"

# 调用被装饰的函数
result = my_function()
```
#### 代码解释
- `@retry(maxAttempts=3, delay=1, exceptions=Exception, showError=True)`：使用 `retry` 装饰器，设置 `my_function` 最大尝试次数为 3 次，每次重试延迟 1 秒，捕获所有异常，显示错误信息。
- `result = my_function()`：调用被装饰的函数，若函数执行失败，会进行重试，最多尝试 3 次。

### 8. 计算缓存
#### 功能
该装饰器用于缓存函数的执行结果，避免重复计算。
#### 参数
- `maxSize`：最大缓存条目数，默认为 `128`。
- `ttl`：缓存的过期时间，单位为秒，默认为 0。
#### 示例代码
```python
# 导入计算缓存装饰器
from DecoKit import memoize

# 使用 memoize 装饰器，设置缓存最大条目数为 1024，缓存过期时间为 60 秒
@memoize(maxSize=1024, ttl=60)
def my_function(n):
    print("计算 n！")
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

# 调用被装饰的函数
result1 = my_function(5)
result2 = my_function(5)
```
#### 代码解释
- `@memoize(maxSize=1024, ttl=60)`：使用 `memoize` 装饰器，设置 `my_function` 缓存最大条目数为 1024，缓存过期时间为 60 秒。
- `result1 = my_function(5)`：调用被装饰的函数，第一次执行，会计算 `n!` 并缓存结果，第二次执行，会直接返回缓存结果。


### 9. 速率限制
#### 功能
该装饰器用于限制函数的执行频率。
#### 参数
- `maxCalls`：周期内最大允许调用次数。
- `period`：周期，单位为秒，默认为 1。
- `value`：调用次数超过限制后返回的值，默认为 `None`。
#### 示例代码
```python
# 导入速率限制装饰器
from DecoKit import rateLimit

# 使用 rateLimit 装饰器，设置周期为 1 秒，周期内最多调用 3 次，超限后返回 None
@rateLimit(maxCalls=3, period=1, value=None)
def my_function():
    print("此函数每秒最多只能被调用 3 次。")

# 循环调用被装饰的函数 5 次
for i in range(5):
    my_function()
```
#### 代码解释
- `@rateLimit(maxCalls=3, period=1, value=None)`：使用 `rateLimit` 装饰器，设置 `my_function` 周期为 1 秒，周期内最多调用 3 次，超限后返回 `None`。
- `for i in range(5): my_function()`：循环调用 `my_function` 5 次，前 3 次正常执行，后 2 次返回 `None`。


## 四、总结
通过使用这些装饰器，开发者可以更方便地实现函数的定时执行、耗时统计、异常处理、调用限制和失败重试等功能，提高代码的健壮性和可维护性。