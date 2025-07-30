from yangke.ebsilon.ebsilon import EbsApp, EbsModel, EbsProfile
from yangke.web.flaskserver import start_server_app
from yangke.common.config import logger
from typing import Optional
import pythoncom

ebs = EbsApp()


def EbsilonAvailable(args):
    _ = ebs.get_application_string()
    return _


def GenerateTCurve(args):
    model_path = args.get("modelPath")
    model = ebs.open(model_path)
    profile = model.get_profile("母体工况")
    root_profile = model.get_profile("设计")
    success, coped_profile = profile.copy(profile, False, root_profile)
    coped_profile.change_name("大气温度")
    children = [coped_profile]
    for i in range(1, 9):
        children.append(coped_profile.new_child())
        children[i].change_name(f"大气温度{i}")

    model.save_as(r"E:\new.ebs", True)


def solve(args):
    action = args.get('Action')  # 因为下方use_action=True，所以这里的action必然有值，避免eval函数出错
    result = eval("{}(args)".format(action))
    return result


if __name__ == "__main__":
    start_server_app(deal=solve, port=20011, host="0.0.0.0", single_thread=True)  # 必须以单线程模式启动，否则EbsApp难以运行
