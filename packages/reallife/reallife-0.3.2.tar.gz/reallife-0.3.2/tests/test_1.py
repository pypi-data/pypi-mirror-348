# from reallife.utils import Date

from datetime import datetime

class Date:
    """日期, 来控制系统时间

    Returns:
        object: 单例模式
    """
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self,date:str = None,time:str = None):
        # 只有第一次初始化时设置值，后续的初始化调用不会更改实例的值
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.date = date or datetime.today().strftime("%Y-%m-%d")
            self.time = time or datetime.today().strftime("%H:%M:%S")

    def set_date(self,date):
        self.date = date

    def set_time(self,time):
        self.time = time

date_c = Date()

print(f"{date_c.date} {date_c.time}")