import datetime
import math

from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from client.page.SimulationInputer import SimulationInputer
from entity.InspectInfo import InspectInfo
from exception.upload.ChildInfoIsNotExist import ChildInfoIsNotExist
from logger import logger
from time import sleep
from selenium import webdriver

from client.page.AbstractClient import AbstractClient


class ChromeClient(AbstractClient):
    def __init__(self):
        self.__driver = webdriver.Chrome()
        self.__driver.minimize_window()
        self.__inputer: SimulationInputer = SimulationInputer(self.__driver)

    def close(self) -> None:
        self.__driver.close()

    def switch_sign_page(self) -> None:
        self.__driver.maximize_window()
        self.__driver.get(self.SIGN_IN_PAGE_URL)

    def wait_user_login(self) -> None:
        while self.__driver.current_url != self.HOME_PAGE_URL:
            sleep(1)
        logger.debug("用户已进入国家基本卫生公共管理系统")

    def upload_child(self, info: InspectInfo, is_reupload: bool = False) -> None:
        logger.debug("上传数据: " + str(vars(info)))
        print(vars(info), end="\r")
        try:
            if info.age >= 48:
                self.__upload_four_to_six_years_old_child(info, is_reupload)
            else:
                self.__upload_three_years_old_child(info, is_reupload)
        except ChildInfoIsNotExist as e:
            self.__create_child_info(info)
            self.upload_child(info)

    def __create_child_info(self, info: InspectInfo) -> None:
        raise ChildInfoIsNotExist("建档功能暂未实现")

    def __upload_three_years_old_child(self, info: InspectInfo, is_reupload: bool) -> None:
        # 跳转入页面
        self.__driver.get(self.HOME_PAGE_URL)
        try:
            WebDriverWait(self.__driver, 0.5).until(expected_conditions.alert_is_present())
            self.__driver.switch_to.alert.accept()
        except TimeoutException:
            pass
        self.__driver.get(self.THREE_YEARS_OLD_UPLOAD_URL)
        new_btn = self.__driver.find_element(By.XPATH, '//*[@id="info"]/a[1]')
        ActionChains(self.__driver).move_to_element(new_btn).click().perform()
        self.__driver.implicitly_wait(0.5)
        # 输入身份证
        self.__inputer.input_identity(info.identity)
        # 输入随访日期
        self.__inputer.input_inspect_time(info.inspect_time)
        # 输入体重
        self.__inputer.input_weight(info.weight, info.weight_assess)
        # 输入身高
        self.__inputer.input_height(info.height, info.height_assess)
        # 输入体重/身高
        self.__inputer.input_bmi(info.bmi_assess)
        # 输入体格发育评价
        self.__inputer.input_assess(info.bmi_assess, info.height_assess, info.weight_assess)
        # 输入视力
        self.__inputer.input_eyesight(info.eye_sight_l, info.eye_sight_r, info.sph_l, info.sph_r, info.cyl_l,
                                      info.cyl_r, info.axis_l, info.axis_r, info.eye_sight_assess)
        # 输入听力
        self.__inputer.input_hearing()
        # 输入牙数
        self.__inputer.input_tooth(info.age, info.tooth_num, info.decayed_tooth_num)
        # 输入胸部
        self.__inputer.input_chest(info.other)
        # 输入腹部
        self.__inputer.input_abdomen(info.other)
        # 输入血红蛋白
        self.__inputer.input_hb(info.hb)
        # 输入其他
        self.__inputer.input_other(info.other, info.eye_ills, info.oral_ills)
        # 发育评估
        self.__inputer.input_development_assess(info.age, info.spirit)
        # 输入两次随访患病情况
        self.__inputer.input_patient_status()
        # 输入转诊建议
        self.__inputer.input_switch_hospital_advice(info.other)
        # 输入指导
        self.__inputer.input_advice()
        # 输入指导意见
        self.__inputer.input_zdyj(info.age, info.eye_sight_assess,
                                  info.height_assess,
                                  info.bmi_assess,
                                  info.weight_assess,
                                  is_reupload)
        # 输入处理意见
        self.__inputer.input_clyj(info.age, info.other, info.hb_assess)
        # 输入中医药健康管理服务
        self.__inputer.input_chinese_medicine_service()
        # 输入下次随访日期
        self.__inputer.input_next_inspect_time(info.inspect_time)
        # 随访医生签名
        self.__inputer.input_signature()
        # 保存
        self.__inputer.save()

    def __upload_four_to_six_years_old_child(self, info: InspectInfo, is_reupload: bool) -> None:
        # 跳转入页面
        self.__driver.get(self.HOME_PAGE_URL)
        try:
            WebDriverWait(self.__driver, 0.5).until(expected_conditions.alert_is_present())
            self.__driver.switch_to.alert.accept()
        except TimeoutException:
            pass
        self.__driver.get(self.FOUR_TO_SIX_CHILD_UPLOAD_URL)
        new_btn = self.__driver.find_element(By.XPATH, '//*[@id="info"]/a[1]')
        ActionChains(self.__driver).move_to_element(new_btn).click().perform()
        self.__driver.implicitly_wait(0.5)
        # 输入身份证
        self.__inputer.input_identity(info.identity)
        # 输入年龄
        self.__inputer.input_age(info.age)
        # 输入随访日期
        self.__inputer.input_inspect_time(info.inspect_time)
        # 输入体重
        self.__inputer.input_weight(info.weight, info.weight_assess)
        # 输入身高
        self.__inputer.input_height(info.height, info.height_assess)
        # 输入体重/身高
        self.__inputer.input_bmi(info.bmi_assess)
        # 输入体格发育评价
        self.__inputer.input_assess(info.bmi_assess, info.height_assess, info.weight_assess)
        # 输入视力
        self.__inputer.input_eyesight(info.eye_sight_l, info.eye_sight_r, info.sph_l, info.sph_r, info.cyl_l,
                                      info.cyl_r, info.axis_l, info.axis_r, info.eye_sight_assess)
        # 输入听力
        self.__inputer.input_hearing()
        # 输入牙数
        self.__inputer.input_tooth(info.age, info.tooth_num, info.decayed_tooth_num)
        # 输入胸部
        self.__inputer.input_chest(info.other)
        # 输入腹部
        self.__inputer.input_abdomen(info.other)
        # 输入血红蛋白
        self.__inputer.input_hb(info.hb)
        # 输入其他
        self.__inputer.input_other(info.other, info.eye_ills, info.oral_ills)
        # 发育评估
        self.__inputer.input_development_assess(info.age, info.spirit)
        # 输入两次随访患病情况
        self.__inputer.input_patient_status()
        # 输入转诊建议
        self.__inputer.input_switch_hospital_advice(info.other)
        # 输入指导
        self.__inputer.input_advice()
        # 输入指导意见
        self.__inputer.input_zdyj(info.age, info.eye_sight_assess,
                                  info.height_assess,
                                  info.bmi_assess,
                                  info.weight_assess,
                                  is_reupload)
        # 输入处理意见
        self.__inputer.input_clyj(info.age, info.other, info.hb_assess)
        # 输入下次随访日期
        self.__inputer.input_next_inspect_time(info.inspect_time)
        # 随访医生签名
        self.__inputer.input_signature()
        # 保存
        self.__inputer.save()
