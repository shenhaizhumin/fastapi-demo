from datetime import datetime, timedelta


# value 为 python 中的 datetime 类型数据
def released_time(value):
    """自定义发布时间过滤器"""
    created_time = value.timestamp()  # 把发布时间转换成秒级时间戳
    now_time = datetime.now().timestamp()  # 获取当前时间戳（秒级）
    duration = now_time - created_time
    if duration < 60:  # 小于一分钟
        display_time = "刚刚"
    elif duration < 60 * 60:  # 小于一小时
        display_time = str(int(duration / 60)) + "分钟前"
    elif duration < 60 * 60 * 24:  # 小于24小时
        display_time = str(int(duration / 60 / 60)) + "小时前"
    elif duration < 60 * 60 * 24 * 30:  # 小于30天
        display_time = str(int(duration / (60 * 60 * 24))) + "天前"
    else:
        display_time = value.strftime('%Y-%m-%d')  # 大于30天
    return display_time
