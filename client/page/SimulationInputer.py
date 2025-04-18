from datetime import datetime, timedelta

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from exception.DatumMissingException import DatumMissingException
from exception.UnknownException import UnknownException
from exception.upload.ChildInfoIsNotExist import ChildInfoIsNotExist
from exception.upload.InspectInfoIsAlreadyUploaded import InspectInfoIsAlreadyUploaded
from exception.upload.UploadDatumException import UploadDatumException


class SimulationInputer:
    def __init__(self, w: WebDriver):
        self.__driver = w

    def __check_dialog_and_raise_exception(self):
        """
            如果弹出提示框，有'成功'二字或者'正在保存信息'则什么都不做
            如果弹出提示框,则抛出对应的异常,他们全部继承于UploadDatumException,规则如下
            如果内容存在 '该儿童已做过记录',则抛出InspectInfoIsAlreadyUploaded
            如果内容存在 '找不到个人信息',则抛出ChildInfoIsNotExist
            如果没有以上情况,则抛出UploadDatumException
        """
        dialog_table = self.__driver.find_element(By.XPATH, '//*[@id="dialog"]')
        if dialog_table.is_displayed():
            alert_message_td = self.__driver.find_element(By.XPATH, '//*[@id="dlg_info"]')
            if '成功' in alert_message_td.text or "正在保存信息" in alert_message_td.text:
                return
            if '该儿童已做过记录' in alert_message_td.text:
                raise InspectInfoIsAlreadyUploaded('该儿童已做过记录')
            if '找不到个人信息' in alert_message_td.text:
                raise ChildInfoIsNotExist('找不到个人信息')
            raise UploadDatumException(alert_message_td.text)

    def input_age(self, age_of_month: int):
        if age_of_month >= 72:
            six_years_old_li = self.__driver.find_element(By.XPATH, '//*[@id="age"]/li[3]')
            ActionChains(self.__driver).move_to_element(six_years_old_li).click().perform()
        elif age_of_month >= 60:
            five_years_old_li = self.__driver.find_element(By.XPATH, '//*[@id="age"]/li[2]')
            ActionChains(self.__driver).move_to_element(five_years_old_li).click().perform()
        elif age_of_month >= 48:
            four_years_old_li = self.__driver.find_element(By.XPATH, '//*[@id="age"]/li[1]')
            ActionChains(self.__driver).move_to_element(four_years_old_li).click().perform()
        else:
            raise UnknownException("未知的年龄")
        self.__check_dialog_and_raise_exception()

    def input_identity(self, identity: str):
        if identity is None:
            raise DatumMissingException("缺少身份证数据")

        title_h1 = self.__driver.find_element(By.XPATH, '//*[@id="A4"]/h1')
        id_input = self.__driver.find_element(By.ID, 'no')
        (ActionChains(self.__driver)
         .move_to_element(id_input).click().send_keys(identity)
         .move_to_element(title_h1).click()
         .perform())

        # 判断身份证是否正确
        self.__check_dialog_and_raise_exception()
        # 等待系统查出儿童数据
        WebDriverWait(self.__driver, 5).until(expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="noaftername"]')))


    def input_inspect_time(self, inspect_time: datetime):
        if inspect_time is None:
            raise DatumMissingException("缺少体检日期数据")

        inspect_time_input = self.__driver.find_element(By.ID, 'followup_date')
        title_h1 = self.__driver.find_element(By.XPATH, '//*[@id="A4"]/h1')
        (ActionChains(self.__driver)
         .move_to_element(inspect_time_input).click().send_keys(inspect_time.strftime("%Y%m%d"))
         .move_to_element(title_h1).click()
         .perform())
        # 判断日期是否正确
        self.__check_dialog_and_raise_exception()

    def input_weight(self, weight: float, weight_assess: str):
        if weight_assess is None or weight_assess is None:
            raise DatumMissingException("缺少体重数据")

        weight_input = self.__driver.find_element(By.XPATH, '//*[@id="weight"]')
        ActionChains(self.__driver).move_to_element(weight_input).click().send_keys(str(weight)).perform()
        if weight_assess == '中':
            li = self.__driver.find_element(By.XPATH, '//*[@id="weight2"]/li[3]')
            ActionChains(self.__driver).move_to_element(li).click().perform()
        elif weight_assess == '中上':
            li = self.__driver.find_element(By.XPATH, '//*[@id="weight2"]/li[2]')
            ActionChains(self.__driver).move_to_element(li).click().perform()
        elif weight_assess == '中下':
            li = self.__driver.find_element(By.XPATH, '//*[@id="weight2"]/li[4]')
            ActionChains(self.__driver).move_to_element(li).click().perform()
        elif weight_assess == '上' or weight_assess == '超上':
            li = self.__driver.find_element(By.XPATH, '//*[@id="weight2"]/li[1]')
            ActionChains(self.__driver).move_to_element(li).click().perform()
        elif weight_assess == '低体重' or weight_assess == '重度低体重':
            li = self.__driver.find_element(By.XPATH, '//*[@id="weight2"]/li[5]')
            ActionChains(self.__driver).move_to_element(li).click().perform()
        self.__check_dialog_and_raise_exception()

    def input_height(self, height: float, height_assess: str):
        if height_assess is None or height_assess is None:
            raise DatumMissingException("缺少身高数据")

        height_input = self.__driver.find_element(By.XPATH, '//*[@id="height"]')
        ActionChains(self.__driver).move_to_element(height_input).click().send_keys(str(height)).perform()
        if height_assess == '中':
            li = self.__driver.find_element(By.XPATH, '//*[@id="height2"]/li[3]')
            ActionChains(self.__driver).move_to_element(li).click().perform()
        elif height_assess == '中上':
            li = self.__driver.find_element(By.XPATH, '//*[@id="height2"]/li[2]')
            ActionChains(self.__driver).move_to_element(li).click().perform()
        elif height_assess == '中下':
            li = self.__driver.find_element(By.XPATH, '//*[@id="height2"]/li[4]')
            ActionChains(self.__driver).move_to_element(li).click().perform()
        elif height_assess == '上' or height_assess == '超上':
            li = self.__driver.find_element(By.XPATH, '//*[@id="height2"]/li[1]')
            ActionChains(self.__driver).move_to_element(li).click().perform()
        elif height_assess == '生长迟缓' or height_assess == '重度生长迟缓':
            li = self.__driver.find_element(By.XPATH, '//*[@id="height2"]/li[5]')
            ActionChains(self.__driver).move_to_element(li).click().perform()
        self.__check_dialog_and_raise_exception()

    def input_bmi(self, bmi_assess: str):
        if bmi_assess is None:
            raise DatumMissingException("缺少bmi数据")

        if bmi_assess == '中' or bmi_assess == '超重' or bmi_assess == '中下':
            hw_li = self.__driver.find_element(By.XPATH, '//*[@id="wheight2"]/li[2]')
            ActionChains(self.__driver).move_to_element(hw_li).click().perform()
        elif bmi_assess == '肥胖' or bmi_assess == '重度肥胖':
            hw_li = self.__driver.find_element(By.XPATH, '//*[@id="wheight2"]/li[1]')
            ActionChains(self.__driver).move_to_element(hw_li).click().perform()
        elif bmi_assess == '消瘦' or bmi_assess == '重度消瘦':
            hw_li = self.__driver.find_element(By.XPATH, '//*[@id="wheight2"]/li[3]')
            ActionChains(self.__driver).move_to_element(hw_li).click().perform()
        self.__check_dialog_and_raise_exception()

    def input_assess(self, bmi_assess: str, height_assess: str, weight_assess: str):
        if bmi_assess is None:
            raise DatumMissingException("缺少bmi数据")
        if height_assess is None:
            raise DatumMissingException("缺少身高数据")
        if weight_assess is None:
            raise DatumMissingException("缺少体重数据")

        abnormal: bool = False
        if bmi_assess == '超重' or bmi_assess == '肥胖' or bmi_assess == '重度肥胖':
            li = self.__driver.find_element(By.XPATH, '//*[@id="growth_evaluate"]/li[5]')
            ActionChains(self.__driver).move_to_element(li).click().perform()
            abnormal = True
        if weight_assess == '低体重' or weight_assess == '重度低体重':
            li = self.__driver.find_element(By.XPATH, '//*[@id="growth_evaluate"]/li[2]')
            ActionChains(self.__driver).move_to_element(li).click().perform()
            abnormal = True
        if bmi_assess == '消瘦' or bmi_assess == '重度消瘦':
            li = self.__driver.find_element(By.XPATH, '//*[@id="growth_evaluate"]/li[3]')
            ActionChains(self.__driver).move_to_element(li).click().perform()
            abnormal = True
        if height_assess == '生长迟缓' or height_assess == '重度生长迟缓':
            li = self.__driver.find_element(By.XPATH, '//*[@id="growth_evaluate"]/li[4]')
            ActionChains(self.__driver).move_to_element(li).click().perform()
            abnormal = True
        if not abnormal:
            li = self.__driver.find_element(By.XPATH, '//*[@id="growth_evaluate"]/li[1]')
            ActionChains(self.__driver).move_to_element(li).click().perform()
        self.__check_dialog_and_raise_exception()

    def input_eyesight(self, eye_sight_l: float, eye_sight_r: float,
                       sph_l: float, sph_r: float, cyl_l: float, cyl_r: float, axis_l: int, axis_r: int,
                       eye_sight_assess: list[str] | None):
        if eye_sight_l is None or eye_sight_r is None:
            return

        eyesight: str = str(eye_sight_r) + '/' + str(eye_sight_l)
        eyesight_input = self.__driver.find_element(By.XPATH, '//*[@id="eye2_val"]')
        ActionChains(self.__driver).move_to_element(eyesight_input).click().send_keys(eyesight).perform()

        if eye_sight_assess is None or len(eye_sight_assess) == 0 or eye_sight_assess[0] == "zc":
            # 如果没有异常
            normal_li = self.__driver.find_element(By.XPATH, '//*[@id="eye"]/li[1]')
            ActionChains(self.__driver).move_to_element(normal_li).click().perform()
        else:
            # 如果有异常
            abnormal_li = self.__driver.find_element(By.XPATH, '//*[@id="eye"]/li[2]')
            ActionChains(self.__driver).move_to_element(abnormal_li).click().perform()
            # 输入屈光信息
            abnormal_textarea = self.__driver.find_element(By.XPATH, '//*[@id="eye_other"]/textarea')
            abnormal_textarea.clear()
            output_content = None
            if sph_r is None or cyl_r is None or sph_l is None or cyl_l is None:
                # Modify
                # output_content = '数据不足'
                output_content = ''
            else:
                output_format = 'R:{:+.2f}DS/{:+.2f}DC×{:d}\nL:{:+.2f}DS/{:+.2f}DC×{:d}'
                output_content = output_format.format(sph_r, cyl_r, axis_r, sph_l, cyl_l, axis_l)
            ActionChains(self.__driver).move_to_element(abnormal_textarea).click().send_keys(output_content).perform()
        self.__check_dialog_and_raise_exception()

    def input_hearing(self):
        """
            默认正常
        """
        allow_li = self.__driver.find_element(By.XPATH, '//*[@id="ear"]/li[1]')
        ActionChains(self.__driver).move_to_element(allow_li).click().perform()
        self.__check_dialog_and_raise_exception()

    def input_tooth(self, age: int, tooth_num: int, decayed_tooth_num: int):
        if tooth_num is None or decayed_tooth_num is None:
            raise DatumMissingException("缺少牙齿数据")
        tooth_input = None
        decayed_tooth_input = None
        if age >= 48:
            tooth_input = self.__driver.find_element(
                By.XPATH,
                '//*[@id="A4"]/form/table[2]/tbody/tr[11]/td[2]/input[1]'
            )
            decayed_tooth_input = self.__driver.find_element(
                By.XPATH,
                '//*[@id="A4"]/form/table[2]/tbody/tr[11]/td[2]/input[2]'
            )
        else:
            tooth_input = self.__driver.find_element(
                By.XPATH,
                '//*[@id="A4"]/form/table[2]/tbody/tr[10]/td[2]/input[1]'
            )
            decayed_tooth_input = self.__driver.find_element(
                By.XPATH,
                '//*[@id="A4"]/form/table[2]/tbody/tr[10]/td[2]/input[2]'
            )
        (ActionChains(self.__driver)
         .move_to_element(tooth_input).click()
         .send_keys(str(tooth_num))
         .perform())
        (ActionChains(self.__driver)
         .move_to_element(decayed_tooth_input).click()
         .send_keys(str(decayed_tooth_num))
         .perform())
        self.__check_dialog_and_raise_exception()

    def input_chest(self, other: list[str] | None):
        """
            包含'心'和'支气管'和'肺'都算异常
        """
        normal_flag: bool = True
        ills: list[str] = []
        if other is not None:
            for c in other:
                if "心" in c or "支气管" in c or "肺" in c:
                    normal_flag = False
                    ills.append(c)

        if normal_flag:
            chest_li = self.__driver.find_element(By.XPATH, '//*[@id="cardiopulmonary"]/li[1]')
            ActionChains(self.__driver).move_to_element(chest_li).click().perform()
        else:
            chest_li = self.__driver.find_element(By.XPATH, '//*[@id="cardiopulmonary"]/li[2]')
            msg_input = self.__driver.find_element(By.XPATH, '//*[@id="cardiopulmonary2_val"]')
            (ActionChains(self.__driver)
             .move_to_element(chest_li).click()
             .move_to_element(msg_input).click().send_keys(",".join(ills))
             .perform())
        self.__check_dialog_and_raise_exception()

    def input_abdomen(self, other: list[str] | None):
        """
            默认正常
        """
        abdomen_li = self.__driver.find_element(By.XPATH, '//*[@id="abdomen"]/li[1]')
        ActionChains(self.__driver).move_to_element(abdomen_li).click().perform()
        self.__check_dialog_and_raise_exception()

    def input_hb(self, hb: float | None):
        """
            输入hb，如果没有就是"未查"
        """
        hb_input = self.__driver.find_element(By.XPATH, '//*[@id="hemoglobin"]')
        (ActionChains(self.__driver).move_to_element(hb_input).click()
         .send_keys("未查" if hb is None else format("%d" % hb))
         .perform())
        self.__check_dialog_and_raise_exception()

    def input_other(self, other: list[str] | None, eyesight_other: list[str] | None, oral_ills: list[str] | None):

        """
            '屈光其他', '其他'(除了'心' '肺' '支气管'), '口腔其他' 中的内容全部填进去
        """

        other_input = self.__driver.find_element(By.XPATH, '//*[@id="other"]')
        ills: list[str] = []
        if other is not None:
            for c in other:
                if "心" not in c and "支气管" not in c and "肺" not in c:
                    ills.append(c)
        if eyesight_other is not None:
            ills.extend(eyesight_other)
        if oral_ills is not None:
            ills.extend(oral_ills)

        (ActionChains(self.__driver).move_to_element(other_input).click()
         .send_keys(",".join(ills))
         .perform())
        self.__check_dialog_and_raise_exception()

    def input_patient_status(self):
        """
            默认选无
        """
        null_li = self.__driver.find_element(By.XPATH, '//*[@id="illness"]/li[1]')
        ActionChains(self.__driver).move_to_element(null_li).click().perform()
        self.__check_dialog_and_raise_exception()

    def input_switch_hospital_advice(self, other: list[str]):
        """
            只要包含'心'就转诊,原因内容填关于'心'的病,机构及科室内容填'上级专科医院'
        """
        normal_flag: bool = True
        ills: list[str] = []
        if other is not None:
            for c in other:
                if "心" in c:
                    normal_flag = False
                    ills.append(c)
        if normal_flag:
            null_li = self.__driver.find_element(By.XPATH, '//*[@id="referral"]/li[1]')
            ActionChains(self.__driver).move_to_element(null_li).click().perform()
        else:
            have_li = self.__driver.find_element(By.XPATH, '//*[@id="referral"]/li[2]')
            reason_input = self.__driver.find_element(By.XPATH, '//*[@id="referral_reason"]')
            institution_input = self.__driver.find_element(By.XPATH, '//*[@id="referral_hospital"]')
            (ActionChains(self.__driver).move_to_element(have_li).click()
             .move_to_element(reason_input).click().send_keys(",".join(ills))
             .move_to_element(institution_input).click().send_keys("上级专科医院")
             .perform())
        self.__check_dialog_and_raise_exception()

    def input_advice(self):
        """
            全部都选1-5
        """
        li1 = self.__driver.find_element(By.XPATH, '//*[@id="advising"]/li[1]')
        li2 = self.__driver.find_element(By.XPATH, '//*[@id="advising"]/li[2]')
        li3 = self.__driver.find_element(By.XPATH, '//*[@id="advising"]/li[3]')
        li4 = self.__driver.find_element(By.XPATH, '//*[@id="advising"]/li[4]')
        li5 = self.__driver.find_element(By.XPATH, '//*[@id="advising"]/li[5]')
        (ActionChains(self.__driver)
         .move_to_element(li1).click()
         .move_to_element(li2).click()
         .move_to_element(li3).click()
         .move_to_element(li4).click()
         .move_to_element(li5).click()
         .perform())
        self.__check_dialog_and_raise_exception()

    def input_next_inspect_time(self, inspect_time: datetime | None):
        """
            下次寻访时间为一年后
            :param inspect_time 这次的寻访时间
        """

        if inspect_time is None:
            raise DatumMissingException("缺少体检日期数据")
        # 到明年的时间差
        delta = None
        if inspect_time.year % 4 == 0 and inspect_time.month < 3 and inspect_time.day < 29:
            delta = timedelta(days=366)
        else:
            delta = timedelta(days=365)

        next_inspect_time_input = self.__driver.find_element(By.XPATH, '//*[@id="followup_date2"]')
        (ActionChains(self.__driver)
         .move_to_element(next_inspect_time_input).click()
         .send_keys((inspect_time + delta).strftime("%Y%m%d"))
         .perform())
        self.__check_dialog_and_raise_exception()

    def input_signature(self):
        """
            签名医生名称为 ”王琴“
        """
        signature_input = self.__driver.find_element(By.XPATH, '//*[@id="followup_doctor"]')
        (ActionChains(self.__driver)
         .move_to_element(signature_input).click()
         .send_keys('王琴')
         .perform())
        self.__check_dialog_and_raise_exception()

    def input_zdyj(self, age: int, eyesight_assess: str | None,
                   height_assess: str | None,
                   bmi_assess: str | None,
                   weight_assess: str | None,
                   is_reupload: bool = False):
        """
            选择规则：
            bmi_assess包含'消瘦' '肥胖' '低体重' 或 weight_assess 包含 '超重' 或 height_assess 包含 '生长迟缓'就选选择第一个和第二个
            视力有问题的选第七个
            所有人都选第六个
            根据年龄选对应的
        """
        if age < 48:
            select_button = self.__driver.find_element(By.XPATH, '//*[@id="A4"]/form/table[2]/tbody/tr[19]/td[1]/input')
            ActionChains(self.__driver).move_to_element(select_button).click().pause(0.05).perform()
        else:
            select_button = self.__driver.find_element(By.XPATH, '//*[@id="A4"]/form/table[2]/tbody/tr[20]/td[1]/input')
            ActionChains(self.__driver).move_to_element(select_button).click().pause(0.05).perform()

        # 切换到iframe
        select_iframe = self.__driver.find_element(By.XPATH, '//*[@id="popup"]')
        self.__driver.switch_to.frame(select_iframe)
        # 包含'消瘦' '生长迟缓' '超重' '肥胖' '低体重' 就选选择第一个和第二个
        if (height_assess is not None and "生长迟缓" in height_assess) or (
                weight_assess is not None and "低体重" in weight_assess) or (
                bmi_assess is not None and ("肥胖" in bmi_assess or "超重" in bmi_assess or "消瘦" in bmi_assess)):
            first_checkbox = self.__driver.find_element(By.XPATH, '//*[@id="zd1"]')
            second_checkbox = self.__driver.find_element(By.XPATH, '//*[@id="zd2"]')
            (ActionChains(self.__driver)
             .move_to_element(first_checkbox).click()
             .move_to_element(second_checkbox).click()
             .perform())

        # 所有人都选第六个
        sixth_checkbox = self.__driver.find_element(By.XPATH, '//*[@id="zd6"]')
        ActionChains(self.__driver).move_to_element(sixth_checkbox).click().perform()

        # 视力有问题的选第七个
        if eyesight_assess is not None and eyesight_assess != "zc":
            seventh_checkbox = self.__driver.find_element(By.XPATH, '//*[@id="zd7"]')
            ActionChains(self.__driver).move_to_element(seventh_checkbox).click().perform()

        # 根据年龄选对应的
        if is_reupload:
            age = age - 12

        if age >= 72:
            checkbox = self.__driver.find_element(By.XPATH, '//*[@id="zd19"]')
            ActionChains(self.__driver).move_to_element(checkbox).click().perform()
        elif age >= 60:
            checkbox = self.__driver.find_element(By.XPATH, '//*[@id="zd18"]')
            ActionChains(self.__driver).move_to_element(checkbox).click().perform()
        elif age >= 48:
            checkbox = self.__driver.find_element(By.XPATH, '//*[@id="zd17"]')
            ActionChains(self.__driver).move_to_element(checkbox).click().perform()
        elif age >= 36:
            checkbox = self.__driver.find_element(By.XPATH, '//*[@id="zd16"]')
            ActionChains(self.__driver).move_to_element(checkbox).click().perform()
        else:
            raise UnknownException('低于三岁')

        ActionChains(self.__driver).scroll_by_amount(0, 200).perform()

        # 确认
        ensure_button = self.__driver.find_element(By.XPATH, '//*[@id="dialog"]/tbody/tr[3]/td/button[1]')
        ActionChains(self.__driver).move_to_element(ensure_button).click().perform()
        # 退出iframe
        self.__driver.switch_to.default_content()
        self.__check_dialog_and_raise_exception()

    def input_development_assess(self, age: int, spirit: list[str] | None):
        """
            只要心理有内容就选1,其他选无
        """
        ul = None
        if age >= 72:
            ul = self.__driver.find_element(By.XPATH,
                                            '/html/body/div/div[1]/div[2]/div/div/form/table[2]/tbody/tr[16]/td[2]/span/ul[3]')
        elif age >= 60:

            ul = self.__driver.find_element(By.XPATH,
                                            '/html/body/div/div[1]/div[2]/div/div/form/table[2]/tbody/tr[16]/td[2]/span/ul[2]')
        elif age >= 48:
            ul = self.__driver.find_element(By.XPATH,
                                            '/html/body/div/div[1]/div[2]/div/div/form/table[2]/tbody/tr[16]/td[2]/span/ul[1]')
        else:
            ul = self.__driver.find_element(By.XPATH,
                                            '/html/body/div/div[1]/div[2]/div/div/form/table[2]/tbody/tr[16]/td[2]/span/ul[1]')

        if spirit is None or len(spirit) == 0:
            li = ul.find_elements(By.TAG_NAME, 'li')[0]
            ActionChains(self.__driver).move_to_element(li).click().perform()
        else:
            li = ul.find_elements(By.TAG_NAME, 'li')[1]
            ActionChains(self.__driver).move_to_element(li).click().perform()

    def input_clyj(self, age: int, other: list[str] | None, hb_assess: str | None):
        """
            处理意见选择：
            other中有涉及 '心' 的选第五个
            hb贫血则选择第二个
            每个人都选第八个
        """
        if age < 48:
            select_button = self.__driver.find_element(By.XPATH, '//*[@id="A4"]/form/table[2]/tbody/tr[20]/td[1]/input')
            ActionChains(self.__driver).move_to_element(select_button).click().pause(0.05).perform()
        else:
            select_button = self.__driver.find_element(By.XPATH, '//*[@id="A4"]/form/table[2]/tbody/tr[21]/td[1]/input')
            ActionChains(self.__driver).move_to_element(select_button).click().pause(0.05).perform()

        # 切换到iframe
        select_iframe = self.__driver.find_element(By.XPATH, '//*[@id="popup"]')
        self.__driver.switch_to.frame(select_iframe)

        # 选择第五个
        if other is not None:
            for o in other:
                if "心" in o:
                    checkbox = self.__driver.find_element(By.XPATH, '//*[@id="zd5"]')
                    ActionChains(self.__driver).move_to_element(checkbox).click().perform()
                    return
        # 选择第二个
        if hb_assess is not None and "贫血" in hb_assess:
            checkbox = self.__driver.find_element(By.XPATH, '//*[@id="zd2"]')
            ActionChains(self.__driver).move_to_element(checkbox).click().perform()

        # 选择第八个
        checkbox = self.__driver.find_element(By.XPATH, '//*[@id="zd8"]')
        ActionChains(self.__driver).move_to_element(checkbox).click().perform()

        # 确认
        ensure_button = self.__driver.find_element(By.XPATH, '//*[@id="dialog"]/tbody/tr[3]/td/button[1]')
        ActionChains(self.__driver).move_to_element(ensure_button).click().perform()

        # 退出iframe
        self.__driver.switch_to.default_content()
        self.__check_dialog_and_raise_exception()

    def input_chinese_medicine_service(self):
        first_checkbox = self.__driver.find_element(By.XPATH, '//*[@id="zyyjkgl"]/li[1]')
        second_checkbox = self.__driver.find_element(By.XPATH, '//*[@id="zyyjkgl"]/li[2]')
        third_checkbox = self.__driver.find_element(By.XPATH, '//*[@id="zyyjkgl"]/li[3]')
        (ActionChains(self.__driver)
         .move_to_element(first_checkbox).click()
         .move_to_element(second_checkbox).click()
         .move_to_element(third_checkbox).click()
         .perform())
        self.__check_dialog_and_raise_exception()

    def save(self):
        save_button = self.__driver.find_element(By.XPATH, '//*[@id="t_save"]/a')
        ActionChains(self.__driver).move_to_element(save_button).click().perform()
        self.__driver.implicitly_wait(0.5)
        self.__check_dialog_and_raise_exception()
