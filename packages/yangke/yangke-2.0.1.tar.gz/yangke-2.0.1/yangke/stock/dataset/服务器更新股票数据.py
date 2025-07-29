"""
本模块用于更新mysql服务器中的数据
"""
import datetime
import pandas as pd
from yangke.common.config import logger
from yangke.base import execute_function_every_day
from yangke.stock.dataset.mairuiData import StockData
from yangke.stock.dataset.storage import Storage
import yangke.stock.dataset.baostockData as bsd


class UpdateDataBase:
    def __init__(self, kind='dataset', ip=None, port=None, user=None, passwd=None, db=None):
        """
        更新股票数据至数据库
        :param kind: 可取值mysql，表示存储到mysql数据库，sqlite表示sqlite数据库，其他字符串表示存储到运行路径下的文件夹
        """
        self.storage = Storage(kind, user, passwd, ip, port, db)
        self.ds: StockData = StockData()
        d1, _ = self.ds.get_daily_all(need_json=True)  # 一次性获取所有股票当天的数据
        self.storage.update_daily_all(d1)

    def update_all_holidays(self):
        """
        更新服务器上的假日信息数据，手动运行，一次更新10年的假日信息最好
        """
        holiday = bsd.get_holiday(start_date=datetime.date(1990, 12, 19), end_date=datetime.date(2000, 1, 1))
        self.storage.update_holiday_table(holiday)

    def update(self):
        """
        更新一次股票数据
        每次执行时，会自动检测当天所属的年份的假日数据是否存在，不存在增更新当年的假日数据

        """
        # ----------------------------- 首先更新假期表 -----------------------------------------
        # 只有tushare和baostock有假期数据
        if self.storage.need_update_holiday_table():
            holiday = bsd.get_holiday()  # 获取今年的holiday数据
            self.storage.update_holiday_table(holiday)

        # ----------------------------- 更新全部股票列表数据 ------------------------------------
        all_stocks: pd.DataFrame | None = None
        if self.storage.need_update_all_stocks_table():  # 从网络获取
            all_stocks = self.ds.get_all_stock_basic_info()
            self.storage.update_all_stocks_table(all_stocks)
        if all_stocks is None:  # 获取失败，从自建数据库获取
            all_stocks = self.storage.get_all_stock_basic_info()  # 从数据库存储中读取所有的股票信息

        last_day_desired = self.storage.get_previous_working_day(include_time=True)
        pre_day = self.storage.get_working_day_before_day(last_day_desired)

        d1, daily_all = self.ds.get_daily_all(need_json=True)  # 一次性获取所有股票当天的数据
        self.storage.update_daily_all(d1)

        for index, row in all_stocks.iterrows():
            symbol = row['symbol']
            logger.info(f"开始更新{symbol}的日线数据，进度{index}/{all_stocks.shape[0]}")
            try:
                self.storage.create_stock_table_day(symbol)
                if self.storage.need_update_daily(symbol):  # 首先判断是否需要更新数据
                    # 其次判断表中最后一条数据的日期，如果只是缺少一条数据，只需要获取最后一天的数据即可
                    last_date = self.storage.get_last_date_of_daily_table(symbol)
                    if last_date == pre_day:
                        d = daily_all[daily_all['symbol'] == symbol]
                        if len(d) == 1 and pd.to_datetime(d["trade_date"]).iloc[0].date() == last_day_desired:
                            daily_data = d
                        else:
                            daily_data = self.ds.get_single_day_data(symbol)
                    else:
                        daily_data = self.ds.get_daily(symbol)
                    if daily_data is not None:
                        self.storage.update_daily(symbol, daily_data)
            except TimeoutError:
                logger.debug(f"获取{symbol}的日线数据失败，跳过")
        logger.debug("数据更新完成")

    def start(self, daemon=True, test_service=False):
        if not test_service:
            execute_function_every_day(self.update, hour=16, minute=0, daemon=False)
        self.storage.start_rest_service(daemon=daemon)


if __name__ == "__main__":
    udb = UpdateDataBase(kind='mysql', ip="sges.yangke.site", port=3306, user="stock", passwd="YangKe.08", db="stocks")
    udb.update()
    udb.start(test_service=True)
