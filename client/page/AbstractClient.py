import abc

from entity.InspectInfo import InspectInfo


class AbstractClient(abc.ABC):
    SIGN_IN_PAGE_URL = 'https://ws71.shousuan.com/www/index.php'
    HOME_PAGE_URL = 'https://ws71.shousuan.com/www/data.php'
    THREE_YEARS_OLD_UPLOAD_URL = 'https://ws71.shousuan.com/www/children3.php'
    FOUR_TO_SIX_CHILD_UPLOAD_URL = 'https://ws71.shousuan.com/www/children4_6.php'
    CREATE_NEW_PERSONAL_ARCHIVE = "https://ws71.shousuan.com/www/personal.php?url=1"

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