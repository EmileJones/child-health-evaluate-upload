import math
import signal
import time
import traceback
from datetime import datetime

from client.page.AbstractClient import AbstractClient
from client.page.ChromeClient import ChromeClient
from client.system.SystemClient import SystemClient
from client.system.access.RequestServerAccess import RequestServerAccess
from entity.InspectInfo import InspectInfo
from entity.UploadStatus import UploadStatus
from exception.upload.ChildInfoIsNotExist import ChildInfoIsNotExist
from exception.upload.InspectInfoIsAlreadyUploaded import InspectInfoIsAlreadyUploaded
from exception.upload.UploadDatumException import UploadDatumException
from logger import logger


def calculate_age(start: datetime, end: datetime) -> int:
    day_delta: int = end.day - start.day
    month_delta: int = end.month - start.month
    year_delta: int = end.year - start.year
    age: int = 0
    age += year_delta * 12
    age += month_delta
    age += 0 if day_delta >= 0 else -1
    return age


def upload_child(info: InspectInfo, page_client: AbstractClient) -> UploadStatus:
    try:
        page_client.upload_child(info)
        return UploadStatus.succeed(info.info_id)
    except InspectInfoIsAlreadyUploaded as e:
        # 检查出生日月是否在体检日期和8月31日之间
        birthday: datetime = datetime.strptime(info.identity[6:14], "%Y%m%d")
        if birthday.month <= info.inspect_time.month or birthday.month > 8 or birthday.day <= info.inspect_time.day:
            # 如果出生日月不在体检日期和8月31日之间，则不上传到下一年
            logger.info(str(e))
            return UploadStatus.was_uploaded(info.info_id)
        else:
            # 如果出生日月在体检日期和8月31日之间，则上传到下一年
            info.age = info.age + 1
            logger.info("尝试提升一岁")
            try:
                # 下一个年龄段上传成功
                page_client.upload_child(info, True)
                return UploadStatus.succeed(info.info_id, "成功上传到下一个年龄段")
            except InspectInfoIsAlreadyUploaded as ee:
                # 下一个年龄段上传失败
                logger.info(str(e))
                return UploadStatus.was_uploaded(info.info_id)
            except UploadDatumException as ee:
                # 数据不足
                logger.info(str(ee))
                return UploadStatus.failure(info.info_id, str(ee))
            except Exception as ee:
                # 发生了其他错误
                traceback.print_exc()
                if len(e.args) != 0:
                    return UploadStatus.failure(info.info_id, str(e))
                else:
                    return UploadStatus.failure(info.info_id, "未知的错误")
    except ChildInfoIsNotExist as e:
        logger.info(str(e))
        return UploadStatus.have_no_archive(info.info_id)
    except UploadDatumException as e:
        logger.info(str(e))
        return UploadStatus.failure(info.info_id, str(e))
    except Exception as e:
        traceback.print_exc()
        if len(e.args) != 0:
            return UploadStatus.failure(info.info_id, str(e))
        else:
            return UploadStatus.failure(info.info_id, "未知的错误")


if __name__ == '__main__':
    running = True
    start_time = time.time()
    run_time: float = float(input("请输入期望运行时间(分)：")) * 60

    system_client: SystemClient = SystemClient(RequestServerAccess())
    page_client: AbstractClient | None = None

    LIMIT = 1
    total_num = 0
    success_num = 0
    exception_num = 0
    no_archive_num = 0
    try:
        system_client.login_system()
        page_client = ChromeClient()
        page_client.switch_sign_page()
        page_client.wait_user_login()
        inspect_infos: list[InspectInfo] = system_client.get_need_upload_inspect_infos(LIMIT, [])
        while len(inspect_infos) != 0 and running:
            upload_status: list[UploadStatus] = []
            for info in inspect_infos:
                upload_result = upload_child(info, page_client)
                upload_status.append(upload_result)
                # 计数
                total_num = total_num + 1
                if upload_result.status == 1:
                    # 异常
                    exception_num = exception_num + 1
                elif upload_result.status == 4:
                    # 未建档
                    no_archive_num = no_archive_num + 1
                elif upload_result.status == 2:
                    # 成功
                    success_num = success_num + 1

            # 获取下一个需要上传的儿童数据
            inspect_infos = system_client.get_need_upload_inspect_infos(LIMIT, upload_status)
            # 计算是否达到用户规定的时间
            now_time = time.time()
            if now_time - start_time > run_time:
                running = False
    except Exception as error:
        traceback.print_exc()
    finally:
        page_client.close()
        logger.info("程序结束")
        logger.info("录入数据总人数：" + str(total_num))
        logger.info("成功人数：" + str(success_num))
        logger.info("发生异常人数：" + str(exception_num))
        logger.info("没有建档人数：" + str(no_archive_num))
        time.sleep(1000)
