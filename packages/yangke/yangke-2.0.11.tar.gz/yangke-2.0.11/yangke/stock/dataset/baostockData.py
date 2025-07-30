# 使用baostock库获取股票数据
from datetime import datetime, date

import baostock as bs
import pandas as pd

from yangke.common.config import logger


def get_holiday(day_datetime: datetime.date = date.today(), start_date: date | None = None,
                end_date: date | None = None) -> pd.DataFrame:
    """
    获取股票交易日历
    :param day_datetime:
    :param start_date: 开始日期最早不能早于1990-12-19日，因为A股首次开盘的日期是1990-12-19日
    :param end_date: 结束日期和开始日期之间最多不能超过10000天，建议不要超过20年
    """
    year = day_datetime.year
    bs.login()
    if start_date is not None and end_date is not None:
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')
        holiday_data: pd.DataFrame = bs.query_trade_dates(start_date=start_str,
                                                          end_date=end_str).get_data()
    else:
        holiday_data: pd.DataFrame = bs.query_trade_dates(start_date=f'{year}-01-01',
                                                          end_date=f'{year}-12-31').get_data()
    bs.logout()
    if len(holiday_data) == 0:
        logger.error('获取假日数据出错，检查baostock版本')
    holiday_data.rename(columns={"calendar_date": "date", "is_trading_day": "open"}, inplace=True)
    # 日期必须转换为datetime才能与数据库中的DATE列匹配
    holiday_data["date"] = pd.to_datetime(holiday_data["date"])
    holiday_data["open"] = holiday_data["open"].apply(lambda x: True if int(x) == 1 else False)
    return holiday_data
