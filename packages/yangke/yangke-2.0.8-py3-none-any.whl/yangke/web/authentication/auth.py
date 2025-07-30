import os

from flask import Flask
from sqlalchemy import create_engine
from yangke.web.flaskserver import start_server_app, run
from yangke.dataset.YKSqlalchemy import SqlOperator


def deal(args):
    action = args.get('Action')  # 因为下方use_action=True，所以这里的action必然有值，避免eval函数出错
    result = eval("{}(args)".format(action))
    return result


# app = start_server_app(deal=None, run_immediate=False)
sql = SqlOperator(create_engine('mysql+pymysql://sges:sges@sges.yangke.site:3306/sges'))


def login(args):
    username = args['username']
    password = args['password']
    res = sql.exists_in_table('user', condition_dict={'user_name': username, 'password': password})
    return {
        "success": True,
        "login_info": res
    }


def register(args):
    username = args['username']
    password = args['password']
    email = args['email']
    sql.insert_item('user', values=[username, email, password], col_names=['user_name', 'email', 'password'])
    return {"success": True}


app = start_server_app(deal=deal, allow_action=['login', 'register'], host='0.0.0.0', port=5000,
                       example_url=['http://localhost:5000/?Action=login&username=杨可&password=test'])
