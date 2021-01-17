# python中的时间

## 时间的形式

- 类： object
- 时间戳： timestamp
- 字符串： string

## 三个库： time、datetime 、



```python
from datetime import datetime

# 获取当前的时间
datetime.now()

# 初始化一个datetime对象
datetime(2020, 7, 28, 11, 17, 38, 972555)  # 年、月、日、时、分、秒、毫秒，极少用
datetime(2020, 7, 23, 17, 38)  # 年、月、日、时、分

# 初始化一个time对象, 时、分、秒
datetime.time(17, 38, 5)

# 初始化一个date对象：年、月、日
datetime.date(2020, 7, 28)

```

```python
import time


time.localtime()  # 返回一个time tuple用于表示当前时间的local time
time.struct_time(tm_year=2018, tm_mon=7, tm_mday=28, tm_hour=11,   tm_min=26, tm_sec=19, tm_wday=5, tm_yday=209, tm_isdst=0)


# 获取当前的时间戳
time.time()


```

## 日期时间字符串

```python
from datetime import datetime


dt = datetime.now()

# 获取ISO8601标准时间字符串
dt.isoformat()  # '2020-06-28T12:11:33.582380'

# 自定义格式的时间字符串
dt.strftime("%Y%m%d-%H:%M:%S")  # '20180728-12:11:33'

```


## 日期时间处理场景

- 获取当前时间

```python
from datetime import datetime
import time


# 最常用的获取当前日期时间的方法，其有一个tz参数用于设置时区，默认为None，所以最终获取的是一个原始naive时间
dt = datetime.now()
# 注意获取的是当地时间的时间表示，但其本身是一个原始naive时间
print(dt)
# datetime(2020, 7, 28, 12, 58, 57, 676468)

# 获取当前时间的UTC时间表示，注意这仍然是一个原始naive时间，也就是用当前的UTC时间4点59分32秒来构造一个naive时间对象，但这个对象并没有包含时区信息
utc_now = datetime.utcnow()
print(utc_now)
#  datetime.datetime(2018, 7, 28, 4, 59, 32, 258087)

# 获取当前时间的时间戳
time()

# 获取当地时间的time tuple
time.localtime()
time.struct_time(tm_year=2018, tm_mon=7, tm_mday=28, tm_hour=13, tm_min=0, tm_sec=2, tm_wday=5, tm_yday=209, tm_isdst=0)
```

- 获取特定的时间：比如获取5天钱的时间

```python
from datetime import datetime


dt = datetime.now()

#  获取两天前的时间
two_day_before = dt - datetime.timedelta(days=2)

#  获取一周前的时间
a_week_before = dt - datetime.timedelta(weeks=1)

#  获取3小时前的时间
three_hours_before = dt - datetime.timedelta(hours=3)
```

- 不同时间表示之间的转化： 比如把datetime对象转化为时间字符串

```python
import time
from datetime import datetime


#  从时间戳转化datetime类
ts = time.time()
dt = datetime.fromtimestamp(ts)

utc_dt = datetime.utcfromtimestamp(ts)


# 从datetime类转化为时间戳timestamp
def get_timestamp(datetime_obj):
    if not isinstance(datetime_obj, datetime):
        raise ValueError()
    return (datetime_obj - datetime(1970, 1, 1)).total_seconds()

get_timestamp(dt)


# datetime类转化为time字符串
dt.strftime("%Y-%m-%dT%H:%M:%S")

# 转化为ISO8601格式字符串的快捷方式
dt.isoformat()


# 时间字符串time string 转化为 datetime类

time_str = '2018-07-28T18:53:54'
dt2 = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")

time.struct_time(tm_year=2018, tm_mon=7, tm_mday=28, tm_hour=18, tm_min=53, tm_sec=54, tm_wday=5, tm_yday=209, tm_isdst=-1)
```

- 时区处理
