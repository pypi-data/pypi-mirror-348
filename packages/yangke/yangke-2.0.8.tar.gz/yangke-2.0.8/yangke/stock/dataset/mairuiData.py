import time
import toml
from pathlib import Path
import pandas as pd
import requests
from yangke.base import timeout
from yangke.common.config import logger


class StockData:
    def __init__(self, lincense=None):
        """
        获取股票数据的类，该类只负责数据获取，数据的存储在storage.py中
        """
        super().__init__()
        # 从settings.toml加载license（当入参为None时）
        if lincense is None:
            settings_path = Path.cwd() / "settings.toml"
            try:
                with open(settings_path, "r", encoding="utf-8") as f:
                    settings = toml.load(f)
                self.license = settings.get("license")
                if not self.license:
                    logger.info("settings.toml中未找到有效的license字段，正在添加...")
                    settings["license"] = "请在这里填入您的【麦蕊智数】许可证密钥"
                    with open(settings_path, "w", encoding="utf-8") as f:
                        toml.dump(settings, f)
                    logger.info(f"已在settings.toml文件中添加license字段，请进行填写。")
                    raise ValueError("请在settings.toml文件中填入有效的license字段")
            except FileNotFoundError:
                logger.info("未找到settings.toml文件，正在生成新文件...")
                default_settings = {
                    "license": "请在这里填入您的【麦蕊智数】许可证密钥"
                }
                try:
                    with open(settings_path, "w", encoding="utf-8") as f:
                        toml.dump(default_settings, f)
                    logger.info(f"已生成新的settings.toml文件，路径: {settings_path}")
                    raise ValueError("请在settings.toml文件中填入有效的license字段")
                except Exception as e:
                    logger.error(f"生成settings.toml文件时出错: {str(e)}")
                    raise
            except toml.TomlDecodeError:
                raise ValueError("settings.toml文件格式错误")
            except ValueError as e:
                logger.error(f"请填写settings.toml文件中的license字段！")
                exit(0)
                
        else:
            self.license = lincense
        self.pre_url = 'https://y.mairui.club'

    def get_market(self, symbol):
        """
        获取股票所属的板块
        """
        symbol = str(symbol)
        if symbol.startswith('60'):
            return '主板'
        elif symbol.startswith('00'):
            return "主板"
        elif symbol.startswith('30'):
            return '创业板'
        elif symbol.startswith('68'):
            return '科创板'
        elif symbol.startswith('82'):
            return '优先股'
        elif symbol.startswith('83'):
            return '普通股'
        elif symbol.startswith('87'):
            return '普通股'
        elif symbol.startswith('4'):
            return '北交所'

    def get_all_stock_basic_info(self) -> pd.DataFrame | None:
        """
        获得上海和深圳证券交易所目前上市的所有股票代码
        """
        url = f'{self.pre_url}/hslt/list/{self.license}'
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # 主动触发HTTP错误异常
            if response.status_code == 200:
                df = pd.DataFrame(response.json())
                df.rename(columns={"dm": "symbol", "mc": "name", "jys": "exchange"}, inplace=True)
                # 统一股票代码格式为6位数字
                df['symbol'] = df['symbol'].apply(lambda x: x[:6] if '.' in x else x)
                # 将exchange列统一改为小写
                df['exchange'] = df['exchange'].str.lower()
                # 移除lambda函数，直接使用函数引用
                df['market'] = df['symbol'].apply(self.get_market)
                df = df.sort_values(by='symbol', ascending=True)
                df = df.reset_index().drop(columns='index')
                return df
            else:
                logger.debug(f"获取数据失败，检查网络或证书，尝试连接{url}")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"获取股票基本信息失败: {str(e)}")
            logger.debug(f"请求URL: {url}")
            logger.debug(f"响应状态码: {getattr(response, 'status_code', '无响应')}")
            return None

    @timeout(240)
    def get_daily(self, symbol):
        """
        获取指定股票的日线数据
        """
        # "https://y.mairui.club/zs/hfsjy/000001/dn/lincense"
        # 根据《股票列表》得到的股票代码和分时级别获取历史交易数据，交易时间从远到近排序。目前 分时级别 支持5分钟、15分钟、30分钟、60分钟、日
        # 周月年级别（包括前后复权），对应的值分别是 5m（5分钟）、15m（15分钟）、30m（30分钟）、60m（60分钟）、dn(日线未复权)、dq（日线前复权）
        # 、dh（日线后复权）、wn(周线未复权)、wq（周线前复权）、wh（周线后复权）、mn(月线未复权)、mq（月线前复权）、mh（月线后复权）、
        # yn(年线未复权)、yq（年线前复权）、yh（年线后复权）
        url = f'{self.pre_url}/zs/hfsjy/{symbol}/dn/{self.license}'
        try:
            response = requests.get(url, timeout=60)
            if response.status_code == 404:
                logger.error(f"股票{symbol}日线数据未找到, URL: {url}")
                if symbol == "000508":
                    logger.debug("该股已退市")
                return None
            elif response.status_code == 200:
                res = pd.DataFrame(response.json())
                res.rename(columns={"d": "trade_date",
                                    "o": "open", "h": "high",
                                    "l": "low", "c": "close",
                                    "v": "vol", "e": "amount",
                                    "hs": "换手率",
                                    "sz": "市值",  # 总市值
                                    "lt": "流通市值",
                                    "pe": "市盈率",
                                    "sjl": "市净率"
                                    },
                           inplace=True)
                return res
        except requests.exceptions.SSLError:
            logger.debug("请求数据发生SSLError，间隔1分钟后重新尝试")
            time.sleep(60)  # 间隔60s后重试
            return self.get_daily(symbol)

    def get_daily_sh_index(self):
        """
        获取上证指数的日线
        """
        symbol = 'sh000001'
        return self.get_daily(symbol)

    def get_daily_sz_index(self):
        """
        获取深证指数的日线
        """
        symbol = ''
        return self.get_daily(symbol)

    @timeout(10)
    def get_single_day_data(self, symbol):
        """
        获取指定股票的日线数据
        http://api1.mairui.club/hsrl/ssjy/股票代码(如000001)/您的licence
        """
        url = f'{self.pre_url}/hsrl/ssjy/{symbol}/{self.license}'
        # 添加超时参数，避免程序无限期挂起
        response = requests.get(url, timeout=10)
        res = pd.DataFrame([response.json()])
        res.rename(columns={"t": "trade_date",
                            "o": "open", "h": "high",
                            "l": "low", "p": "close",
                            "v": "vol", "cje": "amount",
                            "hs": "换手率",
                            "sz": "市值",  # 总市值
                            "lt": "流通市值",
                            "pe": "市盈率",
                            "sjl": "市净率"
                            },
                   inplace=True)
        return res

    def get_daily_all(self, try_times=1, need_json=False):
        """
        获取所有股票当天的交易数据
        https://y.mairui.club/hsrl/ssjy/all/lincense
        http://a.mairui.club/hsrl/ssjy/all/lincense  该地址已测试
        """
        url = f'http://a.mairui.club/hsrl/ssjy/all/{self.license}'
        try:
            response = requests.get(url, timeout=40)
            response.raise_for_status()  # 主动触发HTTP错误异常，会被requests.exceptions.RequestException捕获
            
            try:
                json_res = response.json()
                res = pd.DataFrame(json_res)
                res.rename(columns={
                    "t": "trade_date",
                    "o": "open", "h": "high",
                    "l": "low", "p": "close",
                    "v": "vol", "cje": "amount",
                    "hs": "换手率",
                    "sz": "市值",
                    "lt": "流通市值",
                    "pe": "市盈率",
                    "sjl": "市净率",
                    "dm": "symbol"
                }, inplace=True)
                
                if need_json:
                    return json_res, res
                return res
                
            except requests.exceptions.JSONDecodeError:
                logger.error(f"JSON解析失败: {response.text}")
                if try_times < 3:
                    time.sleep(70)
                    return self.get_daily_all(try_times + 1, need_json=need_json)
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"请求失败: {str(e)}")
            if try_times < 3:
                time.sleep(70)
                return self.get_daily_all(try_times + 1, need_json=need_json)
            return None


if __name__ == '__main__':
    sd = StockData()
    sd.get_all_stock_basic_info()
