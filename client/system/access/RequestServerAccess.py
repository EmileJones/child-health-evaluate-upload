import json
from datetime import datetime

import requests

from client.system.access.AbstractServerAccess import AbstractServerAccess
from entity.InspectInfo import InspectInfo
from entity.UploadStatus import UploadStatus
from exception.AuthenticationException import AuthenticationException
from exception.UnknownException import UnknownException


class RequestServerAccess(AbstractServerAccess):
    baseurl: str = "https://emilejones.top:20001/api/"
    # baseurl: str = "http://192.168.0.3:20001"

    def get_need_upload_inspect_infos(self, limit: int, upload_status: list[UploadStatus], token: str) -> list[
        InspectInfo]:
        headers = {
            'token': token
        }
        dict_list: list[dict] = []
        for r in upload_status:
            dict_list.append(self.__convert_upload_status_to_dict(r))
        res = requests.post(self.baseurl + "/upload", headers=headers, json={'uploadStatus': dict_list, 'limit': limit})
        if res.status_code != 200:
            raise UnknownException(res.text)
        json_res = json.loads(res.text)

        result: list[InspectInfo] = []
        for info in json_res["result"]:
            i = self.__covert_json_to_inspect_info(info)
            result.append(i)
        return result

    def login(self, username: str, password: str) -> str:
        r"""
            如果登陆成功则返回token，如果失败则抛出异常
            :param username: 用户名
            :param password: 密码
            :return token字符串
            :exception UnknownException: 如果返回的HTTP报文状态码不是200，则抛出此异常
            :exception AuthenticationException: 如果是用户的输入错误，则抛出此异常
        """

        my_params = {"userName": username, "password": password}
        res = requests.post(self.baseurl + "/login", my_params)
        if res.status_code != 200:
            raise UnknownException(res.text)
        json_res = json.loads(res.text)
        if json_res["code"] != 200:
            raise AuthenticationException(json_res["msg"])
        return json_res["result"]["token"]

    @staticmethod
    def __covert_json_to_inspect_info(json_object: dict) -> InspectInfo:
        i = InspectInfo()
        i.name = json_object.get("name")
        i.identity = json_object.get("identity")

        inspect_info = json_object.get("inspectInfos")[0]
        i.info_id = inspect_info.get("id")
        i.age = inspect_info.get("ageMonth")
        i.height = inspect_info.get("height")
        i.weight = inspect_info.get("weight")
        i.hb = inspect_info.get("hb")
        i.tooth_num = inspect_info.get("toothNum")
        i.decayed_tooth_num = inspect_info.get("decayedToothNum")
        i.eye_sight_l = inspect_info.get("nakedEyeVisionL")
        i.eye_sight_r = inspect_info.get("nakedEyeVisionR")
        i.sph_l = inspect_info.get("sphL")
        i.sph_r = inspect_info.get("sphR")
        i.cyl_l = inspect_info.get("cylL")
        i.cyl_r = inspect_info.get("cylR")
        i.axis_l = inspect_info.get("axisL")
        i.axis_r = inspect_info.get("axisR")
        i.inspect_time = datetime.strptime(inspect_info.get("inspectTime"), "%Y-%m-%d") if inspect_info.get(
            "inspectTime") is not None else None
        i.other = inspect_info.get("other")
        i.eye_ills = inspect_info.get("eyeSightIlls")
        i.oral_ills = inspect_info.get("oralIlls")
        i.spirit = inspect_info.get("spirit")

        assess_result = inspect_info.get("assessResult")
        i.height_assess = assess_result.get("ageHeight")
        i.weight_assess = assess_result.get("ageWeight")
        i.bmi_assess = assess_result.get("heightWeight")
        i.hb_assess = assess_result.get("hb")
        i.eye_sight_assess = assess_result.get("eyesight")
        return i

    @staticmethod
    def __convert_upload_status_to_dict(upload_status: UploadStatus) -> dict:
        d: dict = {"status": upload_status.status, "inspectId": upload_status.inspectId,
                   "needUpload": upload_status.needUpload, "message": upload_status.message}
        return d