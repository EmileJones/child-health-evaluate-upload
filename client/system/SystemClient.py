from client.system.access.AbstractServerAccess import AbstractServerAccess
from entity.InspectInfo import InspectInfo
from entity.UploadStatus import UploadStatus
from exception.AuthenticationException import AuthenticationException
from logger import logger


class SystemClient:

    def __init__(self, access: AbstractServerAccess):
        self.__token: str | None = None
        self.__access: AbstractServerAccess = access

    def get_need_upload_inspect_infos(self, limit: int, upload_status: list[UploadStatus]) -> list[InspectInfo]:
        if self.__token is None:
            raise AuthenticationException('Token required')
        return self.__access.get_need_upload_inspect_infos(limit, upload_status, self.__token)

    def login_system(self) -> None:
        test_time = 0
        while test_time < 3:
            try:
                username = input("请输入账号:\n")
                password = input("请输入密码:\n")
                self.__token = self.__access.login(username, password)
                logger.debug("用户成功登录系统")
                return
            except AuthenticationException as e:
                test_time = test_time + 1
                print(e.args[0])
        logger.warn("用户登录系统失败")
        raise AuthenticationException("登录失败")
