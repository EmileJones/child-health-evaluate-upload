import abc

from entity.InspectInfo import InspectInfo
from entity.UploadStatus import UploadStatus


class AbstractServerAccess(abc.ABC):
    @abc.abstractmethod
    def login(self, username: str, password: str) -> str:
        pass

    @abc.abstractmethod
    def get_need_upload_inspect_infos(self, limit: int, upload_status: list[UploadStatus], token: str) -> list[InspectInfo]:
        pass