# encoding=utf8
"""
制作*.whl的安装文件
"""
__version__ = "2.0.0"

import traceback

extras_require = {  # 额外依赖项，安装方法“pip install yangke[Database]”
    "Database": [
        'pymysql>=0.9.3',
        'DBUtils>=1.3',  # 用于创建数据库连接池
        'cryptography>=3.1.1',  # 用于mysql8以上版本的连接加密，必须安装，否则无法解析密码
        'python-docx',
        'mysql-connector-python>=8.0.24',
        'sqlalchemy<=1.4.39',  # 2.0版本的sqlalchemy存在很多兼容性问题，还需要进一步解决
    ],
    "windows": [
        'pypiwin32',
    ],
    "web": [
        'flask>=1.1.2',
        'Flask-Cors>=3.0.8',
        'waitress',
    ],
    "Stock": [
        # 'torch>=1.4.0', # pytorch需要单独安装，pypi里版本太老
        'tushare>=1.2.48',
        'scrapy>=2.0.0',
        # 'sxtwl>=1.0.7',  # 该库是用于农历节假日计算的，从2022年开始已经停止更新了，因此新版python不适用
        'pymysql>=0.9.3',
        'DBUtils>=1.3',
        'selenium>=3.141.0',
        'mysql-connector-python>=8.0.24',
        'selenium>=3.141.0',
        'sqlalchemy>=1.3.23',
    ],
    "ImageRecognition": [
        'opencv-python>=4.2.0',
        'cmake>=3.18.2',
        'boost',
        # 'dlib>=19.17.0',  # dlib需要单独安装，涉及到cmake和boost
        'pillow>=7.0.0',
        'requests>=2.22.0',
        # 'tensorflow>=2.8.0',
        # 'torch>=1.11.0',
        'optuna',
        'plotly',
        'paddlepaddle',

    ],

    "GameServer": [
        'twisted>=20.3.0',
        'flask>=1.1.2',
        'flask_cors>=3.0.8',
        'requests>=2.22.0',
        'gevent>=20.5.0',
        'gevent-websocket',
        'waitress>=1.4.4',
        'lxml',
    ],
    "Performance": [
        'iapws>=1.5.2',
        'pygame',
        # 'PyQt5',
        # 安装PyQt5时如果出现ERROR: Could not install packages due to an OSError: [Errno 13] Permission denied:
        # ‘C:\Users\zhangbin\AppData\Roaming\Python\Python39\site-packages\PyQt5\Qt5\bin\d3dcompiler_47.dll’，
        # 说明d3dcompiler_47.dll文件占用，禁止无关应用开机启动，重启安装尝试。
        # 'PyQtWebEngine',  # 用于显示pyecharts图形
        'PyQt6',
        "PyQt6-WebEngine",
        'PyQt6-QScintilla'
        'PyQt6-WebEngine',
        # 'PySide6'
    ],

}

module_name_list = list(extras_require.keys())


def info():
    from yangke.common.config import printInColor
    printInColor(" module 'yangke' installed successfully ",
                 color_fg='white', color_bg='cyan', mode=1)
    printInColor(" version is {} ".format(__version__),
                 color_fg="white", color_bg="yellow", mode=1)
    print("The optional submodules are: ", end="")

    for mod in module_name_list[:-1]:
        printInColor('[{}]'.format(mod), mode=1, color_bg='', end='')
        print(", ", end='')
    printInColor('[{}]'.format(module_name_list[-1]), color_bg='', mode=1)

    print("Use command ", end="")  # end设置不换行输出
    printInColor("pip install yangke", color_fg='red',
                 color_bg='yellow', end='', mode=1)
    printInColor("[Database]", color_bg='yellow', end="", mode=1)
    print("/", end='')
    printInColor("pip install *.whl", color_fg='red',
                 color_bg='yellow', end='', mode=1)
    printInColor("[Database]", color_bg='yellow', end="", mode=1)
    print(" to install the selected submodule.")

    print("Use command ", end="")
    printInColor(
        "pip install *.whl[All]", color_fg='red', color_bg='yellow', end='', mode=1)
    printInColor("[Database]", color_bg='yellow', end="", mode=1)
    print(" to install all the submodule.")


def yangke_test():
    info()


def version():
    info()


def test():
    info()


def stock():
    """
    http://y.mairui.club/hslt/list/8B92E04E-302A-4BB0-9468-54FBB51F7401
    8B92E04E-302A-4BB0-9468-54FBB51F7401
    """
    license = '8B92E04E-302A-4BB0-9468-54FBB51F7401'
    url = f'http://y.mairui.club/hslt/list/{license}'


def login(args):
    """
    查询登录用户信息是否正确，返回注册结果
    """
    import sqlalchemy
    from yangke.dataset.YKSqlalchemy import SqlOperator
    import datetime
    username = args['username']
    encrypt_pass = args['password']
    sql: SqlOperator = args['sql']
    try:
        res = sql.select_in_table(table_name='user', condition_dict={'username': username, 'password': encrypt_pass},
                                  result_type='json')

        if res:  # 成功登录后，余额减1
            today = datetime.date.today()
            last_login_time: datetime.datetime = res.get("last_login")
            if last_login_time is None:
                last_login_time = datetime.datetime.now()

            last_login_date = last_login_time.date()
            if last_login_date != today:  # 如果最后登录日期不是今天，则余额减1
                money = res.get("money") - 1
            else:
                money = res.get("money")

            sql.update_item(table_name='user', conditions={'username': username, 'password': encrypt_pass},
                            values={"money": money, "last_login": datetime.datetime.now()})
            return {
                "success": True,
                "login_res_type": 0,
                "login_info": res,
            }
        else:
            return {
                "success": True,
                "login_res_type": 1,
                "login_info": res
            }
    except sqlalchemy.exc.PendingRollbackError:
        traceback.print_exc()
        return {
            "success": False,
            "login_res_type": 2,
            "login_info": traceback.format_exc()
        }
    except:
        traceback.print_exc()
        return {
            "success": False,
            "login_res_type": 3,
            "login_info": traceback.format_exc()
        }


def register(args):
    """
    注册用户，向mysql数据库表中添加用户
    """
    from yangke.dataset.YKSqlalchemy import SqlOperator
    import datetime
    sql: SqlOperator = args['sql']
    username = args['username']
    encrypt_pass = args['password']
    email = args['email']
    money = 0
    vip = 0
    last_login = datetime.datetime.now()

    if sql.exists_in_table('user', condition_dict={'username': username}):
        return {
            "success": True,
            "register_res_type": 1,
            "register_info": "duplicated username"
        }
    elif sql.exists_in_table("user", condition_dict={'email': email}):
        return {
            "success": True,
            "register_res_type": 2,
            "register_info": "duplicated email"
        }
    else:
        sql.insert_item('user', values=[username, email, encrypt_pass, money, vip, last_login],
                        col_names=['username', 'email', 'password', "money", "vip", "last_login"])
        return {"success": True,
                "register_res_type": 0,
                "register_info": "success", }


def charge(args):
    """
    向指定账号充值
    """
    from yangke.dataset.YKSqlalchemy import SqlOperator
    from yangke.common.config import logger
    logger.debug(args)
    name = args.get('name')
    username = name.split('-')[0]
    money = args.get('money')  # 单位元
    money = int(float(money)) * 10  # 将单位转换成角
    pid = args.get('pid')
    no = args.get('out_trade_no')
    site_name = args.get('sitename')
    trade_status = args.get('trade_status')
    sql: SqlOperator = args.get('sql')
    logger.debug(f"{username}, {pid}, {no}, {site_name}, {trade_status}")

    # https://z-pay.cn/submit.php?money=1&name=undefined-SGES-1%E5%85%83out_trade_no=1733882848665&pid=2024120914335319
    try:
        exist_no = sql.select_item('trade', {"no": no})
        logger.debug(f"{exist_no=}, {trade_status=}")
        if trade_status == "TRADE_SUCCESS" and not exist_no:
            now_money = int(sql.select_item(
                'user', {"username": username}, result_col='money'))
            logger.debug(f"{now_money=}")
            conditions = {"username": username}
            values = {"money": now_money + money}
            logger.debug(f"{conditions=}, {values=}")
            sql.update_item('user', conditions, values)
            sql.insert_item('trade', values=[no, username, money, name, pid, trade_status],
                            col_names=['no', 'username', 'amount', 'name', 'pid', 'status'])
            logger.debug(f"充值成功")
            return "success"
        else:
            return "success"  # 告诉支付官方通知收到，不要再次发送了
    except:
        logger.debug(traceback.format_exc())
        return "error"  # 告诉官方再次尝试发送充值信息


def testrest(args):
    return {
        "success": True,
        "info": '服务正在运行中...',
        "args": str(args)
    }


def GetPoolInfo(args):
    from yangke.dataset.YKSqlalchemy import SqlOperator
    sql: SqlOperator = args['sql']
    return {
        "success": True,
        "info": sql.get_pool_info()
    }


def systemTick(args):
    from yangke.dataset.YKSqlalchemy import SqlOperator
    import datetime
    sql: SqlOperator = args.get('sql')
    username = args.get('username')
    try:
        last_login, money = sql.select_item(
            'user', {"username": username}, result_col=['last_login', 'money'])
        if last_login.date() == datetime.date.today():
            now_money = int(money)  # 当天已经登录，则不进行操作
        else:
            # 当前未登录，则扣费后将最后登录时间更改为今天
            now_money = int(money) - 1
            sql.update_item('user', {"username": username},
                            values={'money': now_money, 'last_login': datetime.datetime.now()})
        if now_money < -10:
            return {
                "username": username,
                "isLogin": True,
                "money": now_money,
                "status": "arrear"
            }
        else:
            return {
                "username": username,
                "isLogin": True,
                "money": now_money,
                "status": "success"
            }
    except Exception as e:
        traceback.print_exc()
        return {
            "username": username,
            "isLogin": False,
            "status": "Server Error"
        }


def autoUpdateStockData():
    """
    自动更新股票数据
    """
    ...


def start_restful_mysql(mysql_user, mysql_password, mysql_host='localhost', mysql_port=3306, mysql_db='sges',
                        rest_port=5000, ssl=True, cors=True, single_thread=False):
    from yangke.dataset.YKSqlalchemy import SqlOperator
    from sqlalchemy import create_engine
    from sqlalchemy.pool import QueuePool
    from yangke.web.flaskserver import start_server_app
    sql = SqlOperator(
        create_engine(f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}',
                      poolclass=QueuePool,
                      pool_size=5,
                      max_overflow=10,
                      pool_timeout=30,  # 连接池中没有可用连接时的等待时间，超过该时间还没有可用连接，则报错
                      pool_recycle=3600,  # 连接池中的连接1小时后会回收
                      pool_pre_ping=True,  # 每次连接请求时，先测试返回的连接是否还存活，不存活则从连接池中取下一个连接
                      ))

    def deal(args):
        try:
            # 因为下方use_action=True，所以这里的action必然有值，避免eval函数出错
            action = args.get('action')
            args['sql'] = sql
            result = eval(f"{action}(args)")
            return result
        except:
            return {"success": False,
                    "info": "执行deal时错误"}

    start_server_app(deal=deal, use_action=True,
                     allow_action=['login', 'register', 'testrest', 'GetPoolInfo', 'charge',
                                   'systemTick'],
                     host='0.0.0.0',
                     port=rest_port,
                     example_url=[
                         f'http://localhost:{rest_port}/?Action=login&username=杨可&password=test'],
                     single_thread=single_thread, ssl=ssl, cors=cors)


def start_update_stocks_data(kind, ip, port, user, passwd, db):
    """
    每天定时更新服务器端的股票数据，并提供Restful API服务，默认服务端口5002，
    支持['downloadHolidays', 'downloadStocksDailyAll', 'downloadStocksDailySingle', 'downloadStocksTotalInfo', 'downloadLastDay']等方法。
    
    
    :param kind: 数据库类型，目前支持mysql
    :param ip: 数据库IP地址
    :param port: 数据库端口号
    """
    from yangke.stock.dataset.服务器更新股票数据 import UpdateDataBase

    udb = UpdateDataBase(kind=kind, ip=ip, port=port,
                         user=user, passwd=passwd, db=db)
    udb.update()
    udb.start(True)

# 该文件无法调试，提示空套件错误
# if __name__ == '__main__':
#     start_restful_mysql('root', 'YangKe.08', '101.37.118.81')
