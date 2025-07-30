import datetime
import traceback
from typing import Any
import importlib.metadata
from typing import Union, Type
import pandas as pd
from sqlalchemy import create_engine, MetaData, Column, inspect, Table, String, text, insert, delete, update, select, \
    func, asc, desc, BOOLEAN
from sqlalchemy.dialects.mysql import INTEGER, DOUBLE, BIGINT, VARCHAR, CHAR, TEXT, DATETIME, DATE
from sqlalchemy.engine import Engine, Row
from sqlalchemy.exc import PendingRollbackError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import Select

from yangke.common.config import logger


def get_sqlalchemy_version() -> str:
    """
    获取 SQLAlchemy 的版本号。
    """
    try:
        # Python 3.8+ 推荐使用 importlib.metadata
        version = importlib.metadata.version("sqlalchemy")
    except ImportError:
        # 兼容旧版本 Python
        import pkg_resources
        version = pkg_resources.get_distribution("sqlalchemy").version
    return version


def import_by_version(module_path: str, class_name: str) -> Union[Type, None]:
    """
    根据模块路径和类名动态导入类。
    """
    module = __import__(module_path, fromlist=[class_name])
    return getattr(module, class_name)


def import_sqlalchemy_components() -> dict:
    """
    根据 SQLAlchemy 版本动态导入所需的组件。
    """
    version = get_sqlalchemy_version()
    major_version = int(version.split(".")[0])  # 获取主版本号

    components1 = {}

    if major_version >= 2:
        # SQLAlchemy 2.0+ 的导入路径
        components1["Engine"] = import_by_version("sqlalchemy", "Engine")
        components1["QueuePool"] = import_by_version("sqlalchemy", "QueuePool")
        components1["Row"] = import_by_version("sqlalchemy.engine", "Row")
        components1["Double"] = import_by_version("sqlalchemy", "Double")
    elif major_version == 1:
        # SQLAlchemy 1.4.x 的导入路径
        components1["Engine"] = import_by_version("sqlalchemy.engine", "Engine")
        components1["QueuePool"] = import_by_version("sqlalchemy.pool", "QueuePool")
        components1["Row"] = import_by_version("sqlalchemy.engine.result", "Row")
        components1["Double"] = import_by_version("sqlalchemy", "Float")  # 1.4.x 中使用 Float 替代 Double
    else:
        raise ImportError(f"Unsupported SQLAlchemy version: {version}")

    return components1


# 动态导入 SQLAlchemy 组件
components = import_sqlalchemy_components()
# Engine = components["Engine"]
QueuePool = components["QueuePool"]
# Row = components["Row"]
Double = components["Double"]

# # 创建基类, 使用ORM方式操作数据库是继承该类
Base = declarative_base()
# noinspection all
修改时间记录表 = 'modify_time'


class ModifyTime(Base):
    """
    用来记录数据库表格最后更新时间的表格，因为目前MySql和Sqlite数据库均无法查询表格的最后更新时间，因此使用数据库表格记录所有表格的最后更新
    时间
    """
    __tablename__ = 修改时间记录表
    table = Column(String(50, collation='utf8mb4_bin'), nullable=False, primary_key=True)  # 设置collation为区分大小写
    datetime = Column(DATETIME, nullable=False)

    def __init__(self, table, date_time):
        super(ModifyTime, self).__init__()
        self.table = table  # 表名
        self.datetime = date_time  # 表的最后修改时间

    def __repr__(self):
        return f"ModifyTime(table={self.table}, 修改时间={self.datetime})"


class YkTable(Table):
    def __init__(self, name, metadata, columns=None):
        if columns is None:
            columns = []
        super().__init__(name, metadata, *columns)


class YkColumn(Column):
    inherit_cache = True

    def __init__(self, name, dtype, primary_key=False, nullable=False):
        """
        Sqlite数据库不支持foreignKey关键字，YkColumn的内容默认区分大小写
        :param name: 列名
        :param dtype: 数据类型
        :nullable: 是否可以为空
        """
        if (isinstance(dtype, String) or isinstance(dtype, VARCHAR) or
                isinstance(dtype, CHAR) or isinstance(dtype, TEXT)):
            dtype.collation = 'utf8mb4_bin'
        super().__init__(name, dtype, primary_key=primary_key, nullable=nullable)


class SqlOperator:
    def __init__(self, engine: Engine = None):
        """
        SQL数据库操作类，同时支持MySql和Sqlite数据库，使用示例：
        engine = create_engine("mysql+mysqlconnector://root:password@localhost:3306", pool_recycle=7200)
        engine = create_engine('sqlite:///stocks.db', echo=True)
        create_engine(f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}',
                      poolclass=QueuePool,
                      pool_size=5,
                      pool_timeout=30,  # 连接池中没有可用连接时的等待时间，超过该时间还没有可用连接，则报错
                      pool_recycle=3600,  # 连接池中的连接1小时后会回收
                      pool_pre_ping=True,  # 每次连接请求时，先测试返回的连接是否还存活，不存活则从连接池中取下一个连接
                      )  # 使用连接池
        so = SqlOperator(engine=engine)
        然后可以调用so的增删改查等方法，所有方法均同时支持MySql和Sqlite数据库

        可能遇到的问题：
        1.sqlalchemy.exc.InterfaceError: (mysql.connector.errors.InterfaceError) 2003: Can't connect to MySQL server on
        'disk.yangke.site:3306' (10060 由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。)
        解决方法： 不使用mysqlconnector连接，pip install mysql后使用：create_engine("mysql://root:password@localhost:3306")
        """
        # 创建数据库引擎，ps:这里并没有连接具体数据库
        # engine = create_engine("mysql+mysqlconnector://root:password@localhost:3306/db?charset=utf8", pool_recycle=7200)

        # 连接时，如果报Character set 'utf8' unsupported错误，且数据库文件中没有非ascii字符，可以尝试切换charset的值。
        # 已知charset可取值包括(ascii, utf8, utf8mb4, gbk, cp1250)，可以执行show collation语句查看mysql数据库支持的字符集。

        self.engine = engine
        # self.insp = inspect(self.engine)  # 在需要时inspect，而不是开始就inspect
        self.meta_data = MetaData()  # 兼容sqlalchemy 2.0版本的写法，bind参数写在reflect()方法中
        self.meta_data.reflect(bind=engine)  # 需要的时候在reflect，否则当数据库中表多的话，耗时很长
        self.SessionMaker = sessionmaker(bind=engine)  # 使用sessionmaker保持数据库会话连接
        self.base = Base
        # self.connect = self.engine.connect() // Connection随用随关，不能长时间保持连接
        self.create_all_base_table()  # 创建修改时间记录表

    def create_table(self, table_name, columns):
        """
        创建数据库表，如果同名表存在，会报错，SqlAlchemy 2.0.36已测试
        示例1：
        self.create_table(table_name=f"daily{symbol}",
                          columns=[
                              YkColumn('trade_date', DATE(), primary_key=True),
                              YkColumn('open', Float()),
                              YkColumn('high', Float()),
                              YkColumn('low', Float()),
                              YkColumn('close', Float()),
                              YkColumn('vol', Float()),
                              YkColumn('amount', Float()),
                          ])
        """
        table = Table(table_name, self.meta_data, *columns)
        logger.debug(f"创建表格{table_name}")
        with self.engine.connect() as connection:
            table.create(bind=connection)  # bind=self.engine时，部分情况下会卡住

    def create_all_base_table(self):
        """
        创建所有继承自Base类的Python类的映射数据库表。也就是说，只要定义了继承自本模块中Base类的类，则该类会被映射成一个数据库表，
        本方法会自动创建所有映射的数据库表。本方法主要用于创建修改时间记录表，如果创建用户的专有表，建议使用self.create_table()方法
        """
        self.base.metadata.create_all(self.engine)

    def get_type_of_column(self, table_name=None, column_name=None):
        """
        获取mysql表中字段的类型，如果不设置column_name则返回所有的字段类型
        :param table_name:
        :param column_name: 为空则依次返回所有列的类型，封装为一个列表
        :return:
        """
        cols = inspect(self.engine).get_columns(table_name)
        res = None
        if column_name is None:
            res = {}
            for col in cols:
                res.update({col["name"]: col["type"]})
        else:
            for col in cols:
                if col["name"] == column_name:
                    res = col["type"]
                    break
        return res

    def get_column_names(self, table_name):
        """
        获取表格中的列名，返回列名列表
        """
        cols = inspect(self.engine).get_columns(table_name)
        res = [col["name"] for col in cols]
        return res

    def get_update_time_of_table(self, table_name):
        """
        获取表的最后更新时间
        """
        session = self.SessionMaker()
        try:
            if self.has_table(table_name):
                # 查询modifyTime表，modifyTime表中记录了所有表格的最后更新时间
                if self.has_table(修改时间记录表):
                    table1: Table = self.get_table(修改时间记录表)
                    select1: Select = table1.select().where(table1.c.table == table_name)  # 构建一个选择语句
                    res = session.execute(select1)  # 执行选择语句并获取结果
                    res = res.fetchone()
                    # res = session.query(table1).filter(table1.table == table_name).first()

                    if res is None:
                        return None
                    return res.datetime  # 该写法兼容sqlalchemy1.4和2.0
                    # return res["datetime"]  # 该写法不兼容sqlalchemy2.0
                else:
                    return None
            else:
                return None
        except PendingRollbackError:
            try:
                session.rollback()
            except Exception:
                logger.warning("回滚失败")
        finally:
            session.close()

    def update_update_time_of_table(self, table_name):
        """
        更新表的最后更新时间
        """
        session = self.SessionMaker()
        try:
            if not self.has_table(修改时间记录表):
                self.create_all_base_table()

            now = datetime.datetime.now()
            if self.exists_in_table(table_name=修改时间记录表, col_name='table', value=table_name):
                self.update_item(table_name=修改时间记录表, conditions={"table": table_name}, values={"datetime": now})
            else:
                self.insert_item(table_name=修改时间记录表, values=[table_name, now], col_names=['table', 'datetime'])
                # session.add(ModifyTime(table_name, now))
            session.commit()
        except PendingRollbackError:
            try:
                session.rollback()  # 尝试回滚，但可能已经有一个回滚在进行中
            except Exception as rollback_exc:
                # 记录回滚失败的信息
                print(f"回滚失败: {rollback_exc}")
        except Exception as e:
            # 处理其他数据库异常
            session.rollback()
            print(f"发生数据库错误: {e}")
        finally:
            session.close()

    def exists_in_table(self, table_name: str = None, col_name: str = None, value: str = None,
                        condition_dict: dict = None,
                        return_result: bool = False):

        """
        表tableName中是否存在列col_name的值位value的行

        :param table_name: 表名
        :param col_name: 列名
        :param value: 列的值
        :param condition_dict: 查询的键值对字典值，优先于col_name和value传入的值，即会覆盖col_name和value传入的值
        :param return_result: 是否需要返回查找到的数据行，如果为真，则返回所有符合查找条件的数据行
        :return:
        """
        if return_result:
            first_or_all = 'all'
        else:
            first_or_all = 'first'

        condition_dict = condition_dict or {}
        if col_name is not None and value is not None:
            condition_dict.update({col_name: value})

        res = self.select_item(table_name, condition_dict, first_or_all=first_or_all)
        if res is not None:
            return True
        else:
            return False

    def select_in_table(self, table_name=None, condition_dict: dict = None, result_col: list | str = None, limit=10,
                        offset=0,
                        fuzzy=False, first_or_all="first", result_type=None, cls=None, **kwargs) -> Row | list | Any:
        """
        查

        精确查询，设置fuzzy为True，且condition_dict中的value为字符串值
        模糊查询，设置fuzzy为False，日期列不能使用模糊查询，只能使用范围查询
        范围查询，设置fuzzy为True，且condition_dict中的value为长度为2的列表，列表第一、二项分别为范围下、上限，且包含上下限

        当result_type=="json"时，返回的是一个list(dict)的json对象，即[{col1: value1, col2: value2,...}, ...}的json对象
        列表的每一项对应一条匹配的查询结果
        每一项的字典分别是{列名：值}

        kwargs={"date_format": "%Y-%m-%d %H:%M:%S"} 如果mysql中存在日期列，需要将日期转换为字符串，该参数定义日期字符串格式

        示例1：
        fetch = self.sql.select_in_table(cls=Holiday, condition_dict={"calendarDate": day_datetime},
                                         result_col=['isOpen'])

        :param table_name: 当使用传统查询方式时，需要传入数据库表名
        :param cls: 当使用ORM模型时，只需要传入数据库表在python中对应的映射类名，如果通过该方法查询，则查询到的数据会被自动转换为cls对象
        :param condition_dict:
        :param result_col: 不传入或传入空列表，则返回数据库中所有列
        :param limit:
        :param offset:
        :param fuzzy: 是否模糊查询
        :param first_or_all: 返回满足条件的第一个还是所有，支持"first", "all",
        :param result_type: 返回类型，如果为json，则返回为json格式的字符串
        :return: None或查询的列值列表或数据条的列表或sqlalchemy.engine.Row对象，出错时返回None，如列明不存在等；否则返回一个tuple类型的数据，长度为0表示未查询到满足条件的数据
        """
        # ---------------------- 如果使用table_name查询，则构建Table对象 ------------------------
        # Table对象可以当cls一样使用
        if cls is None:
            if self.has_table(table_name):
                table: Table = self.get_table(table_name)
                if table is None:
                    return None
                cls = table
        # ---------------------- 如果使用table_name查询，则构建Table对象 ------------------------
        session = self.SessionMaker()
        try:
            # ----------------------- 根据条件字典，构建查询条件 --------------------------------
            if condition_dict is None:  # 查询表格中某列的所有值
                if result_col is None:
                    result_col = self.get_column_names(table_name)
                if isinstance(result_col, str):
                    res = session.execute(select(cls.c.get(result_col))).fetchall()
                    res = [i._data[0] for i in res]
                else:  # list
                    n = len(result_col)
                    _1 = []
                    for i in range(n):
                        _1.append(f"cls.c.get(result_col[{i}])")
                    _2 = ",".join(_1)

                    _3 = f"select({_2})"
                    try:
                        _4 = eval(_3)
                        res = session.execute(_4).fetchall()
                        res = [i._data for i in res]
                    except:
                        traceback.print_exc()
                        logger.error(f"检查返回列的名称是否正确：{result_col=}")
                        res = None
                if result_type == "json":
                    res = [dict(zip([str(column.name) for column in table.c], list(item))) for item in res]
                return res

            _1 = []
            vals = []
            i = 0
            for k, v in condition_dict.items():
                vals.append(v)  # 为了兼容v为datetime或date类型的参数
                _1.append(f"cls.c.{k}==vals[{i}]")
                i += 1
            _2 = ",".join(_1)

            _3 = f"select(cls).where({_2})"
            items = session.execute(eval(_3)).fetchall()
            if len(items) == 0 or items is None:
                return None
            if first_or_all == "first":
                item = items[0]
            else:
                item = items

            # ------------------------ 如果指定了返回的数据列，则取出数据列并返回 -----------------------
            if isinstance(item, str):
                item = [item]
            if item is None or len(item) == 0:
                return item
            else:
                try:
                    if isinstance(item, Row):  # item是个sqlalchemy.engine.row.Row对象，如读取Holiday表时会出现该情况
                        if result_col is None:
                            if result_type == 'json':
                                return dict(zip([str(column.name) for column in table.c], list(item)))
                            else:
                                return item
                        elif isinstance(result_col, str):
                            # sqlalchemy2.0中，item.__getattr__(result_col)语法是正确的
                            # sqlalchemy1.4中，item.__getitem__(result_col)语法是正确的
                            res = eval(f"item.{result_col}")  # 该写法兼容sqlalchemy2.0
                            return res
                        elif isinstance(result_col, list):
                            if len(result_col) == 1:
                                res = eval(f"item.{result_col[0]}")  # 该写法兼容sqlalchemy2.0
                                return res
                            else:
                                return [getattr(item, col) for col in result_col]

                    logger.debug(f"{item=}, {type(item)=}")
                    # noinspection all
                    _ = [getattr(item, col) for col in item]  # table_name和cls两种方法都适用
                    if len(_) == 1:
                        _ = _[0]
                    return _
                except AttributeError:
                    logger.error(item)
            # ------------------------ 如果指定了返回的数据列，则取出数据列并返回 -----------------------
        except PendingRollbackError:
            try:
                session.rollback()  # 尝试回滚，但可能已经有一个回滚在进行中
            except Exception as rollback_exc:
                # 记录回滚失败的信息
                print(f"回滚失败: {rollback_exc}")
        finally:
            session.close()

    def select_item(self, table_name=None, condition_dict: dict = None, result_col: list | str = None, limit=10,
                    offset=0, first_or_all="first",
                    fuzzy=False, result_type=None):
        """
        查

        精确查询，设置fuzzy为True，且condition_dict中的value为字符串值
        模糊查询，设置fuzzy为False，日期列不能使用模糊查询，只能使用范围查询
        范围查询，设置fuzzy为True，且condition_dict中的value为长度为2的列表，列表第一、二项分别为范围下、上限，且包含上下限

        当result_type=="json"时，返回的是一个list(dict)的json对象，即[{col1: value1, col2: value2,...}, ...}的json对象
        列表的每一项对应一条匹配的查询结果
        每一项的字典分别是{列名：值}

        kwargs={"date_format": "%Y-%m-%d %H:%M:%S"} 如果mysql中存在日期列，需要将日期转换为字符串，该参数定义日期字符串格式

        示例1：
        fetch = self.sql.select_in_table(cls=Holiday, condition_dict={"calendarDate": day_datetime},
                                         result_col=['isOpen'])

        :param table_name: 当使用传统查询方式时，需要传入数据库表名
        :param condition_dict:
        :param result_col: 不传入或传入空列表，则返回数据库中所有列
        :param limit:
        :param offset:
        :param fuzzy: 是否模糊查询
        :param first_or_all: 返回满足条件的第一个还是所有，支持"first", "all",
        :param result_type: 返回类型，如果为json，则返回为json格式的字符串
        :return: None或查询的列值列表或数据条的列表或sqlalchemy.engine.Row对象，出错时返回None，如列明不存在等；否则返回一个tuple类型的数据，长度为0表示未查询到满足条件的数据
        """
        return self.select_in_table(table_name=table_name, condition_dict=condition_dict, result_col=result_col,
                                    limit=limit, offset=offset,
                                    fuzzy=fuzzy, first_or_all=first_or_all, result_type=result_type)

    def update_item(self, table_name, conditions: dict, values):
        """
        self.update_item('user', {"id": 1}, values={"name": "Tom"})

        兼容sqlalchemy 1.4及2.0以上版本。
        query.filter()或query.filter_by()的写法无法同时兼容sqlalchemy 1.4和2.0版本

        Parameters
        ----------
        table_name
        conditions: 数据表的索引列的值，必须唯一确定某一个记录
        values: 数据表中其他列的值，可以只设置部分列的值

        Returns
        -------

        """
        table: Table = self.get_table(table_name)
        update_obj = update(table)
        for col_title, col_value in conditions.items():
            update_obj = update_obj.where(table.c.get(col_title) == col_value)  # 兼容写法

        dict_str = "{"
        objs = []
        i = 0
        for title, value in values.items():
            # if isinstance(value, datetime):
            #     dict_str = f"{dict_str}table.c.{title}: value,"
            objs.append(value)
            dict_str = f"{dict_str} table.c.{title}: objs[{i}],"  # 这样的写法是为了解决value是datetime或date类型时的兼容写法
            i += 1
        dict_str += "}"
        values = eval(dict_str)
        update_obj = update_obj.values(values)
        session = self.SessionMaker()
        try:
            session.execute(update_obj)
            session.commit()
        except PendingRollbackError:
            try:
                session.rollback()  # 尝试回滚，但可能已经有一个回滚在进行中
            except Exception as rollback_exc:
                # 记录回滚失败的信息
                print(f"回滚失败: {rollback_exc}")
        finally:
            session.close()

    def get_primary_col(self, table_name):
        """
        获取表的主键

        Parameters
        ----------
        table_name

        Returns
        -------

        """
        table = self.get_table(table_name)
        if isinstance(table, Table):
            # noinspection all
            for col in table.columns:
                if col.primary_key:
                    return col
        return None

    def insert_dataframe(self, table_name, df: pd.DataFrame, if_exists="append", index=False, dtype=None):
        """
        将DataFrame对象写入数据库中。兼容mysql和sqlite。df对象可以包含数据库中不存在的列，该方法会忽略这些列。同时该方法会记录表的最后更新时间

        pandas的to_sql方法存在以下问题：1.表格存在时，如果使用replace，则新创建的表的主键会丢失；2.append时会报重复键错误；

        批量插入数据时，
        简单说明：同样添加10W行数据，插入时间比
        1，Session.add(obj)   使用时间：6.89754080772秒
        2，Session.add(obj)注意：手动添加了主键id   使用时间：4.09481811523秒
        3，bulk_save_objects([obj1, obj2])   使用时间：1.65821218491秒
        4，bulk_insert_mappings(DBmodel, [dict1, dict2])  使用时间： 0.466513156781秒
        5，SQLAlchemy_core(DBmodel.__table__insert(), [dict1, dict2]) 使用时间：0.21024107933秒
        6，直接执行execute(str_sql_insert)  直接执行sql插入语句 使用时间：0.137335062027秒
        ————————————————
        版权声明：本文为CSDN博主「DHogan」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
        原文链接：https://blog.csdn.net/dongyouyuan/article/details/79236673

        Parameters
        ----------
        table_name
        df
        if_exists: 参数参加pandas.DataFrame().to_sql()方法，可取值append, replace, fail
        index
        dtype : 指定df中各列的数值类型

        Returns
        -------

        """

        def slice_str(long_string):
            if len(long_string) > 200:
                short_string_with_ellipsis = long_string[:200] + "..."
            else:
                short_string_with_ellipsis = long_string
            return short_string_with_ellipsis

        session = self.SessionMaker()
        try:
            if self.has_table(table_name):  # 逐条插入，只要表存在，则不要使用pandas的to_sql方法，因为to_sql方法会覆盖原表，导致丢失主键
                primary_col = self.get_primary_col(table_name)
                primary_key = primary_col.name
                items_exist = self.select_item(table_name, result_col=primary_key)  # 获取数据库中表现有的数据记录的唯一标记
                primary_type = self.get_type_of_column(table_name, primary_key)
                if isinstance(items_exist, list):
                    table: Table = self.get_table(table_name)
                    # ---------------------- 判断需要插入的和需要更新的数据 ---------------------------
                    df = df.fillna(0)  # 有些股票的交易量为nan，例如600607的1993-12-23日的交易量为nan

                    cols_table = self.get_column_names(table_name)
                    for col in cols_table:  # 补齐数据库中有的列但是df中没有的列
                        if col not in df.columns:
                            df[col] = None

                    if isinstance(primary_type, DATE):
                        df['new'] = df.apply(
                            func=lambda r: False if pd.to_datetime(r[primary_key]).date() in items_exist else True,
                            axis=1)
                    elif isinstance(primary_type, DATETIME):
                        df['new'] = df.apply(
                            func=lambda r: False if pd.to_datetime(r[primary_key]) in items_exist else True,
                            axis=1)
                    else:
                        df['new'] = df.apply(func=lambda r: False if r[primary_key] in items_exist else True, axis=1)
                    # 2.0版本需要将Timestamp转换为str类型，pandas中的字符串在插入数据库时，会由str强制转换成DATE类型
                    if len(df) > 0:
                        row1: pd.Series = df.iloc[0]  # df中的第一个记录
                        for title, value in row1.items():
                            if isinstance(value, pd.Timestamp):
                                df[title] = df[title].astype(str)

                    df_new = df[df['new']]
                    df_old = df[df['new'] == 0]  # 已存在的数据，视情况忽略或更新，0==False，写False会报PEP == False的警告
                    # ---------------------- 判断需要插入的和需要更新的数据 ---------------------------

                    # ---------------------- 判断是否需要执行插入操作 ---------------------------------
                    if if_exists == "append":  # 存在的数据不操作，只添加不存在的数据
                        if len(df_new) == 0:  # 如果只是追加不存在的数据，且插入的数据全部存在，则无须执行插入操作
                            # 此时将数据更新时间更新一下，因为也是验证过后了
                            self.update_update_time_of_table(table_name)  # 最后更新数据库中数据的最后更新日期
                            return
                    # ---------------------- 判断是否需要执行插入操作 ---------------------------------

                    # 按数据库表的列顺序排列dataframe列，无论if_exists取replace还是append，都要插入新值
                    values_new = [dict(zip(cols_table, item)) for _, item in df_new[cols_table].iterrows()]
                    try:
                        session.execute(table.insert(), values_new)  # 该方法速度仅次于直接执行sql语句，尽量使用该方法

                        if if_exists == "replace":  # 如果存在的数据需要替换
                            values_old = [dict(zip(cols_table, item)) for _, item in df_old[cols_table].iterrows()]
                            session.execute(table.update(), values_old)
                    except:
                        traceback.print_exc()
                        logger.debug(f"{table=}, values_new={slice_str(values_new)}")
                else:
                    logger.warning("未处理的数据插入")
            else:
                # 插入大数据量是特别慢，尤其是数据库已有重复记录时
                logger.warning(f"df.to_sql方法创建的表{table_name}没有主键，建议先创建表后，再插入数据")
                df.to_sql(table_name, self.engine, if_exists=if_exists, index=index)  # 该方法设置的数据库表没有主键
            self.update_update_time_of_table(table_name)  # 最后更新数据库中数据的最后更新日期
        except PendingRollbackError:
            try:
                session.rollback()  # 尝试回滚，但可能已经有一个回滚在进行中
            except Exception as rollback_exc:
                # 记录回滚失败的信息
                print(f"回滚失败: {rollback_exc}")
        finally:
            session.commit()
            session.close()

    def get_count_of_table(self, table_name: str):
        """
        获取表中数据的行数
        """
        session = self.SessionMaker()
        # 获取表中的记录数量
        table: Table = self.get_table(table_name)
        count = session.query(func.count(table.columns[0])).scalar()
        session.close()
        return count

    def get_last_record(self, table_name: str, refer_column: str, ascend=True):
        """
        获取表中最后一条数据
        :param table_name 表名
        :param refer_column 排序的列名
        :param ascend 是否升序排列，默认为真
        """
        table = self.get_table(table_name)
        session = self.SessionMaker()

        if ascend:  # table.id可以写成table.c.get('id')
            res = session.query(table).order_by(desc(table.c.get(refer_column))).first()  # 因为是first()，所有相当于排序取反
        else:
            res = session.query(table).order_by(asc(table.c.get(refer_column))).first()
        session.close()
        return res

    def insert_item(self, table_name: str = None, values: list = None,
                    col_names: list = None, ignore=False,
                    replace=False, filter_warning=None):
        """
        向数据库中插入数据，这里传入的列名不要用反引号括起来，增

        values中的数据类型需要与表中每列的数据类型一致，数据库和python中数据类型对应如下：
        SqlAlchemy          python
        DATETIME            datetime.datetime/datetime.date
        VARCHAR             str

        cols_names和values两个列表一一对应。

        :param table_name: 表名
        :param values:
        :param col_names: 列名，如果是插入带有auto_increment属性的表数据，则必须指定列名，否则就需要指定auto_increment属性的字段的值
        :param ignore: 当插入数据重复时，是否忽略
        :param replace: 当插入数据重复时，是否替换，ignore和replace不能同时为True
        :param filter_warning: 过滤警告信息，[1062, 1265, 1366]，分别对应["Duplicate", "Data truncated", "Incorrect integer value"]
        """
        _: Table = self.get_table(table_name)
        session = self.SessionMaker()
        # ------------------ 该段语句在sqlite服务器上测试成功，但mysql5.6服务器上测试数据不更新 -------------------
        # if col_names is None:
        #     col_names = self.get_column_names(table_name)
        # paras = []
        # for col, val in zip(col_names, values):
        #     if isinstance(val, datetime.datetime) or isinstance(val, datetime.date):
        #         val = val.__repr__()
        #         paras.append(f"{col}={val}")
        #     else:
        #         paras.append(f"{col}='{val}'")
        # paras = ",".join(paras)
        # state = f"_.insert().values({paras})"
        # eval(state)
        # self.session.commit()
        # ------------------ 该段语句在sqlite服务器上测试成功，但mysql5.6服务器上测试数据不更新 -------------------

        # ------------------ mysql5.6以下语句测试成功 -------------------------------
        if replace:
            columns = ""
            self.insert_item()
        else:
            values = dict(zip(col_names, values))
            try:
                ins = _.insert(values=values)  # 低版本sqlalchemy语法1.4.39
                session.execute(ins)  # self.conn.execute()
                session.commit()
            except PendingRollbackError:
                try:
                    session.rollback()  # 尝试回滚，但可能已经有一个回滚在进行中
                except Exception as rollback_exc:
                    # 记录回滚失败的信息
                    print(f"回滚失败: {rollback_exc}")
                finally:
                    session.close()
                    return
            except TypeError:  # TypeError: TableClause.insert() got an unexpected keyword argument 'values'
                # ins = _.insert().values(values)  # 高版本sqlalchemy语法2.0.36
                stmt = (
                    insert(_).
                    values(values)
                )
                try:
                    # with self.engine.connect() as conn:
                    #     conn.execute(stmt)
                    #     conn.commit()
                    session.execute(stmt)
                    session.commit()
                except PendingRollbackError:
                    try:
                        session.rollback()  # 尝试回滚，但可能已经有一个回滚在进行中
                    except Exception as rollback_exc:
                        # 记录回滚失败的信息
                        print(f"回滚失败: {rollback_exc}")
                finally:
                    session.close()

    def has_table(self, table_name):
        """
        判断数据库中是否存在某个表
        """
        # return self.engine.has_table(table_name) # 该写法不兼容sqlalchemy 2.0版本
        return inspect(self.engine).has_table(table_name)  # 2.0已测试，该方法不需要连接池中的连接资源，如果可以的话优先使用
        # with self.engine.connect() as conn:
        #     res = self.engine.dialect.has_table(conn, table_name)
        # return res  # 该写法兼容sqlalchemy1.4和2.0版本

    def exist_table(self, table_name):
        """
        同has_table()
        """
        return self.has_table(table_name)

    def get_table(self, table_name=None) -> Table | None:
        """
        获取表名为table_name的表对象，返回的是 Table()对象。
        如果不传入table_name，则返回数据库中的所有表，返回的是Table()对象的列表。
        """
        tables = [i for i in self.meta_data.tables.values()]
        if table_name is not None:
            for table in tables:
                if table.name == table_name:
                    return table
            return None
        return [i for i in self.meta_data.tables.values()]

    def get_pool_info(self):
        """
        获取连接池信息
        """
        return self.engine.pool.status()


if __name__ == '__main__':
    sql = SqlOperator(create_engine('mysql+pymysql://sges:sges@sges.yangke.site:3306/sges',
                                    poolclass=QueuePool,
                                    pool_size=5,
                                    max_overflow=10,
                                    pool_timeout=30,  # 连接池中没有可用连接时的等待时间，超过该时间还没有可用连接，则报错
                                    pool_recycle=3600,  # 连接池中的连接1小时后会回收
                                    pool_pre_ping=True,  # 每次连接请求时，先测试返回的连接是否还存活，不存活则从连接池中取下一个连接
                                    ))
    # _ = sql.exist_table('user')
    # sql.insert_item('user', ['杨可', 'yangkexn@tpri.com.cn', 'test'], col_names=['user_name', 'email', 'password'])
    _ = sql.exists_in_table('user', condition_dict={'username': '杨可', 'password': 'test'})
    print(sql.get_pool_info())
    print(_)
