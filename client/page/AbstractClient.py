import abc

from config import (
    CREATE_NEW_PERSONAL_ARCHIVE_URL,
    FOUR_TO_SIX_CHILD_UPLOAD_URL,
    HOME_PAGE_URL,
    SIGN_IN_PAGE_URL,
    THREE_YEARS_OLD_UPLOAD_URL,
)
from entity.InspectInfo import InspectInfo


class AbstractClient(abc.ABC):
    SIGN_IN_PAGE_URL = SIGN_IN_PAGE_URL
    HOME_PAGE_URL = HOME_PAGE_URL
    THREE_YEARS_OLD_UPLOAD_URL = THREE_YEARS_OLD_UPLOAD_URL
    FOUR_TO_SIX_CHILD_UPLOAD_URL = FOUR_TO_SIX_CHILD_UPLOAD_URL
    CREATE_NEW_PERSONAL_ARCHIVE = CREATE_NEW_PERSONAL_ARCHIVE_URL

    @abc.abstractmethod
    def switch_sign_page(self) -> None:
        pass

    @abc.abstractmethod
    def upload_child(self, info: InspectInfo, is_reupload: bool = False) -> None:
        pass

    @abc.abstractmethod
    def wait_user_login(self) -> None:
        pass

    @abc.abstractmethod
    def close(self) -> None:
        pass
