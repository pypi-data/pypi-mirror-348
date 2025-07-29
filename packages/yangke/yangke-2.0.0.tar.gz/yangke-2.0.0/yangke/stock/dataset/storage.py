# 量化分析中使用的数据库对应的类
import datetime
import os
import time
import traceback
import pandas as pd
import sys
from yangke.common.config import logger
from yangke.dataset.YKSqlalchemy import (
    SqlOperator, YkColumn, Engine, Double, QueuePool, String,
    BOOLEAN, DATE, create_engine, VARCHAR
)
from yangke.base import timeout


class Storage:
    def __init__(self, kind: str, sql_user=None, sql_passwd=None, sql_ip=None, sql_port=3306,
                 sql_db='stocks', sqlite_db='stocks.db'):
        """
        初始化股票数据存储工具，该工具需要用户已经在数据库服务器上创建了相应的db或schema，注意mysql存储内容默认不区分大小写，需要将collation
        修改为utf8mb4_bin以支持区分大小写。

        该类只负责数据的存储，股票数据的获取在marruiData.py或tushareData.py中

        :param kind: mysql,sqlite 分别表示使用mysql数据库或sqlite数据库存储
        :param sql_user: mysql数据库的用户名，kind=mysql时必须传入
        :param sql_passwd: mysql数据库的密码，kind=mysql时必须传入
        :param sql_ip: mysql数据库的ip，kind=mysql时必须传入
        :param sql_port: mysql数据库的端口，kind=mysql时必须传入
        :param sql_db: mysql数据库的db，kind=mysql时必须传入
        :param sqlite_db: sqlite数据库文件，kind=sqlite时必须传入
        """
        self.kind: str = kind.lower()  # 可取值mysql、sqlite、字符串路径
        self.table_all_stocks_info = 'all_stocks_info'
        self.table_holiday = 'holiday'
        self.table_modify_time = 'modify_time'
        if self.kind.lower() == 'sqlite':
            self.encoding = 'utf8'
            # sqlite数据库默认utf8编码，不需要指定，且连接字符串也不支持指定编码
            self.engine: Engine = create_engine(
                f'sqlite:///{sqlite_db}', echo=False)
        elif self.kind.lower() == 'mysql':
            self.encoding = 'utf8mb4'  # mysql数据库的utf8mb4编码兼容性更强
            self.engine: Engine = create_engine(
                f"mysql+pymysql://{sql_user}:{sql_passwd}@{sql_ip}:{sql_port}/{sql_db}?charset={self.encoding}",
                echo=False,
                poolclass=QueuePool,
                pool_size=5,
                max_overflow=10,
                pool_timeout=30,  # 连接池中没有可用连接时的等待时间，超过该时间还没有可用连接，则报错
                pool_recycle=3600,  # 连接池中的连接1小时后会回收
                pool_pre_ping=True,  # 每次连接请求时，先测试返回的连接是否还存活，不存活则从连接池中取下一个连接)
            )
        else:
            logger.error("暂不支持除了'mysql'和'sqlite'之外的其他存储方式！")
            self.engine = None

        self.sql: SqlOperator = SqlOperator(self.engine)
        self.daily_all_data: str | None = None  # 所有股票最后一天的日线数据
        self.init()

    def init(self):
        if not self.sql.has_table(self.table_holiday):
            self.sql.create_table(self.table_holiday,
                                  columns=[
                                      YkColumn(
                                          'date', DATE, nullable=False, primary_key=True),  # 日期
                                      YkColumn('open', BOOLEAN,
                                               nullable=False)  # 是否开盘
                                  ])
        if not self.sql.has_table(self.table_all_stocks_info):
            self.sql.create_table(table_name=self.table_all_stocks_info,
                                  columns=[  # mysql默认不区分大小写，这里设置collation为区分大小写
                                      YkColumn('symbol', VARCHAR(
                                          10), nullable=False, primary_key=True),  # 000001
                                      YkColumn('name', String(20)),  # 平安银行
                                      YkColumn('exchange', String(10)),  # SZ
                                      YkColumn('market', String(10)),  # SZ
                                  ])
        if not self.sql.has_table(self.table_modify_time):
            self.sql.create_all_base_table()

    @timeout(10)
    def create_stock_table_day(self, code):
        """
        为代码为code的股票创建日线表
        :param code: 股票代码，如"600001"，对应的数据库表名为"daily600001"
        """
        table_name = f"daily{code}"
        if not self.sql.has_table(table_name):
            self.sql.create_table(table_name=table_name,
                                  columns=[
                                      YkColumn('trade_date', DATE(),
                                               primary_key=True),
                                      # 在Ubuntu系统测试，Mysql的Float类型只有6位有效数字
                                      YkColumn('open', Double()),
                                      YkColumn('high', Double()),
                                      YkColumn('low', Double()),
                                      YkColumn('close', Double()),
                                      YkColumn('vol', Double()),
                                      YkColumn('amount', Double()),
                                      YkColumn('换手率', Double()),
                                      YkColumn('市值', Double(), nullable=True),
                                      YkColumn('流通市值', Double(),
                                               nullable=True),
                                      YkColumn('市盈率', Double(), nullable=True),
                                      YkColumn('市净率', Double(), nullable=True),
                                  ])

    def update_all_stocks_table(self, df: pd.DataFrame | None):
        self.sql.insert_dataframe(self.table_all_stocks_info, df)

    def get_all_stock_basic_info(self) -> pd.DataFrame:
        all_stocks = self.sql.select_item(
            table_name=self.table_all_stocks_info, result_type='json')
        return pd.DataFrame(all_stocks)

    def need_update_all_stocks_table(self):
        """
        检查所有股票信息表是否需要更新。

        :return: 如果需要更新返回True，否则返回False
        """
        last_time = self.sql.get_update_time_of_table(
            self.table_all_stocks_info)
        return self.need_update(last_time)

    def get_modify_time_all(self):
        """
        获取所有表格的最后更新时间
        """
        items = self.sql.select_item(table_name=self.table_modify_time)
        return items

    def get_need_single_day_update_stocks(self):
        """
        获取只需要补充最新一天数据的股票列表
        """
        ...

    def need_update_holiday_table(self, date: datetime.date = None):
        """
        是否需要更新假期表，如果能查询到指定日期的数据项，则不需要更新，否则需要更新
        """
        if date is None:
            date = datetime.date.today()  # 不能使用datetime.datetime.today()否则时分秒对不上
        item = self.sql.select_item(self.table_holiday, {"date": date})
        if item is None:
            return True
        else:
            return False

    @timeout(10)
    def need_update_daily(self, symbol: str):
        """
        检查指定股票的日线数据是否需要更新。

        :param symbol: 股票代码，如"600001"
        :return: 如果需要更新返回True，否则返回False
        """
        table_name = f"daily{symbol}"
        last_time = self.sql.get_update_time_of_table(table_name)
        return self.need_update(last_time)

    @timeout(10)
    def get_last_date_of_daily_table(self, symbol: str):
        """
        获取日线数据表中的最后一条数据的日期
        """
        table_name = f"daily{symbol}"
        res = self.sql.get_last_record(table_name, 'trade_date', True)
        return res if res is None else res.trade_date

    @timeout(20)
    def update_daily(self, symbol: str, daily_data: pd.DataFrame):
        """
        更新指定股票的日线数据
        """
        table_name = f"daily{symbol}"
        if not self.sql.has_table(table_name):
            self.create_stock_table_day(symbol)
        self.sql.insert_dataframe(table_name, daily_data)

    def update_daily_all(self, daily_all_data: str):
        """
        更新所有股票的日线数据
        """
        self.daily_all_data = daily_all_data

    def update_holiday_table(self, holiday: pd.DataFrame):
        """
        更新假期表的数据。

        :param holiday: 包含假期信息的DataFrame对象
        """
        self.sql.insert_dataframe(self.table_holiday, holiday)

    @timeout(20)
    def is_holiday(self, day_datetime: datetime.date = datetime.date.today()):
        """
        判断今天是不是休市，只适用于国内股市，不包括港股

        :param day_datetime: 给定日期的datetime类型
        :return: True 或 False
        """
        day_str = day_datetime.strftime("%Y%m%d")
        if (day_datetime.weekday() == 5) or (day_datetime.weekday() == 6):  # 周六和周日肯定是休市的，这里的5、6分别代表周六和周日
            return True
        date_str = day_str
        is_open = self.sql.select_in_table(table_name=self.table_holiday, condition_dict={"date": day_datetime},
                                           result_col=['open'])
        is_open = bool(is_open)  # 1：True，0：False
        if is_open is None:  # 未查找到相关记录
            year = day_datetime.year
            # try:
            #     holiday_data: pd.DataFrame = self.api.query('trade_cal', start_date=f'{year}0101',
            #                                                 end_date=f'{year}1231')  # tushare该接口现在收费了，不让使用
            #     holiday_data.rename(
            #         columns={"cal_date": "calendarDate", "is_open": "isOpen"}, inplace=True)
            # except:
            #     traceback.print_exc()
            #     logger.debug('似乎没有tushare的数据获取权限，尝试使用baostock获取数据')
            #     import baostock as bs
            #     bs.login()
            #     holiday_data: pd.DataFrame = bs.query_trade_dates(start_date=f'{year}-01-01',
            #                                                       end_date=f'{year}-12-31').get_data()
            #     bs.logout()
            #     holiday_data.rename(columns={
            #                         "calendar_date": "calendarDate", "is_trading_day": "isOpen"}, inplace=True)
            # 日期必须转换为datetime才能与数据库中的DATE列匹配
            # holiday_data["calendarDate"] = pd.to_datetime(
            #     holiday_data["calendarDate"])
            # holiday_data["isOpen"] = holiday_data["isOpen"].apply(
            #     lambda x: True if int(x) == 1 else False)

            # # to_sql()语句存储时，使用dtype参数指定dataframe到数据库的对应类型
            # # holiday_data[["calendarDate", "isOpen"]].to_sql(self.假期表, con=self.engine, if_exists='append',
            # #                                                 index=False,
            # #                                                 dtype={"calendarDate": DATE, "isOpen": BOOLEAN})
            # self.sql.insert_dataframe(self.table_holiday, holiday_data, if_exists='append', index=False,
            #                           dtype={"calendarDate": DATE, "isOpen": BOOLEAN})

            # if holiday_data[holiday_data['calendarDate'] == date_str]['isOpen'].item():
            #     return False
            # else:
            #     return True
        else:
            return not is_open  # python会自动将0转换成False，1转换成True

    def need_update(self, data_file: str or datetime.datetime):
        """
        检查数据文件是否需要更新；如果传入的是时间，则检查该时间之后是否有股票数据更新。
        当上一个工作日4点以后更新过，且今天时间不到下午4点，则无需更新

        :param data_file:
        :return:
        """
        if isinstance(data_file, datetime.datetime):
            last_change_time = data_file
            last_change_date_str = last_change_time.strftime("%Y-%m-%d")
        elif data_file is None:  # 如果文件为空
            return True
        elif os.path.exists(data_file):  # 如果文件存在，判断文件是否需要更新
            last_change_time = os.stat(data_file).st_mtime
            last_change_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_change_time))
            last_change_time = datetime.datetime.strptime(last_change_time_str, "%Y-%m-%d %H:%M:%S")
            last_change_date_str = last_change_time.strftime("%Y-%m-%d")
        else:  # 文件不存在，则需要更新
            return True

        now_time = datetime.datetime.now()  # 当前时间
        now_time_date_str = now_time.strftime("%Y-%m-%d")  # 用来和最后修改日期作比较

        if last_change_date_str == now_time_date_str:  # 如果是今天修改的
            if last_change_time.hour > 15:  # 最后修改日期是当天15点以后，则不用更新数据
                logger.debug(f"数据文件{data_file}已经最新，无需更新！")
                return False  # 无需更新数据
            else:
                if now_time.hour < 16:  # 如果今天修改过且今天还没到16:00，也无须更新
                    return False
                # 如果今天时holiday
                if self.is_holiday(datetime.date.today()):  # 如果今天时休息日，今天更新过也不用更新
                    logger.debug(f"数据文件{data_file}已经最新，无需更新！")
                    return False
                else:
                    return True
        else:
            last_working_day_str = str(self.get_previous_working_day(include_time=True)) + ' 16:00:00'
            last_working_datetime = datetime.datetime.strptime(last_working_day_str, '%Y-%m-%d %H:%M:%S')
            if last_change_time > last_working_datetime:
                # 如果最后修改日期在上一个工作日15点之后
                if isinstance(data_file, str):
                    logger.debug(f"数据文件{data_file}已经最新，无需更新！{last_working_datetime=}")
                else:
                    logger.debug(f"数据更新于{data_file}，无需更新！{last_working_datetime=}")
                return False  # 无需更新数据
            else:
                return True

    def get_previous_working_day(self, last_date=None, include_time=False) -> datetime.date:
        """
        获得指定日期的上一个交易日，如果不传入参数，则获得最近的一个交易日，包含今天。

        :param last_date: 指定的日期
        :param include_time: 是否判断时间，如果includeTime=True，则会进一步判断今天的时间，如果时间在下午4:00之前，则不包括今天，因为当天的股票数据还没整理出来
        :return: 最近一个交易日日期
        """
        if last_date is None:  # 不能直接在定义函数时给初值，否则初值将在函数第一次运行时就确定，后续无论运行多少次，都不会改变
            last_date = datetime.date.today()
        if last_date > datetime.date.today():
            logger.warning("因为未来的股票数据不存在，不能获得将来日期的前一个工作日！")
        if self.is_holiday(last_date):
            one_day = datetime.timedelta(days=1)
            pre_day = last_date - one_day
            while self.is_holiday(pre_day):
                pre_day = pre_day - one_day
            return pre_day
        else:
            if include_time and last_date == datetime.date.today():  # 需要判断时间，且last_date是今天
                dt = datetime.datetime.now()
                hour = dt.hour
                if hour < 16:  # 额外对时间进行判断
                    return self.get_working_day_before_day(datetime.date.today())
                else:
                    return last_date
            return last_date

    def get_working_day_before_day(self, day_datetime: None | datetime.date,
                                   day_num: int = 1) -> datetime.date:
        """
        获得指定日期的前一个交易日或后一个交易日，需要注意的是，该函数不对指定日期是否为工作日进行判断，
        因此，获得最近一个交易日，不能使用get_working_day_before_day(date.today(),1)
        :param day_datetime: datetime类型，默认为今天
        :param day_num: 可取正整数和-1，前day_num个交易日，取-1时,表示指定日期的后一个交易日，不可以取其他负值
        :return: date_datetime】,-----返回对应交易日的datetime类型数据
        """
        if day_datetime is None:
            day_datetime = datetime.date.today()
        if day_num < -1:
            logger.error("day_num不能取-1以外的负值（{}）".format(day_num))
            sys.exit()
        if day_num == 1 or day_num == -1:
            one_day = datetime.timedelta(days=1)
            if day_num == -1:
                pre_day = day_datetime + one_day
            else:
                pre_day = day_datetime - one_day
            while self.is_holiday(pre_day):
                if day_num == -1:
                    pre_day = pre_day + one_day
                else:
                    pre_day = pre_day - one_day
            return pre_day
        else:  # day_num为大于1的整数
            day_datetime = self.get_working_day_before_day(
                day_datetime, 1)  # 计算上一个交易日
            # 返回上一个交易日的上day_num-1个交易日
            return self.get_working_day_before_day(day_datetime, day_num - 1)

    @timeout(seconds=10)
    def downloadHolidays(self, args):
        res = self.sql.select_item(self.table_holiday, result_type="json")
        # 判断数据库中是否存在当天的数据，不存在则更新

        # res = [{'date': item['date'].strftime('%Y-%m-%d'), 'open': item['open']} for item in res]
        return res

    @timeout(seconds=10)
    def downloadStocksTotalInfo(self, args):
        res = self.sql.select_item(
            self.table_all_stocks_info, result_type="json")
        return res

    @timeout(seconds=10)
    def downloadStocksDailySingle(self, args: dict):
        symbol = args.get("symbol", None)
        if symbol is None:
            return None
        res = self.sql.select_item(f"daily{symbol}", result_type="json")
        return res

    def downloadStocksDailyAll(self, args: dict):
        return {"info": "暂不支持"} | args

    @timeout(seconds=10)
    def downloadLastDay(self, args):
        """
        下载最后一天所有股票的日线数据
        """
        return self.daily_all_data

    def start_rest_service(self, rest_port=5002, single_thread=False, daemon=True):
        """
        开启restful服务，等待客户端连接
        """
        from yangke.web.flaskserver import start_server_app

        def deal(args):
            try:
                # 因为下方use_action=True，所以这里的action必然有值，避免eval函数出错
                action = args.get('action')
                result = eval(f"self.{action}(args)", {}, {
                              "self": self, "args": args})
                return result
            except TimeoutError:
                logger.warning(f"函数执行超时")
                return {"success": False,
                        "info": "执行deal时错误，函数执行超时"}
            except:
                traceback.print_exc()
                return {"success": False,
                        "info": "执行deal时错误"}

        start_server_app(deal=deal, use_action=True,
                         allow_action=['downloadHolidays', 'downloadStocksDailyAll', 'downloadStocksDailySingle',
                                       'downloadStocksTotalInfo', 'downloadLastDay'],
                         host='0.0.0.0',
                         port=rest_port,
                         example_url=[
                             f'http://localhost:{rest_port}/?Action=downloadHolidays'],
                         single_thread=single_thread)


if __name__ == '__main__':
    storage = Storage('mysql', 'stock', 'YangKe.08', 'sges.yangke.site', 3306,
                      'stocks')
