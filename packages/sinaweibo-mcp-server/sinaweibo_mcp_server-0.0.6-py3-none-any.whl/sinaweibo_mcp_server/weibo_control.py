import json
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 微博自动发布器
class WeiboPoster:
    def __init__(self,path=os.path.dirname(os.path.abspath(__file__))):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        # 获取当前执行文件所在目录
        current_dir = path
        self.cookies_file = os.path.join(current_dir, "weibo_cookies.json")
        self._load_cookies()


    def _load_cookies(self):
        """从文件加载cookies"""
        if os.path.exists(self.cookies_file):
            try:
                with open(self.cookies_file, 'r') as f:
                    cookies = json.load(f)
                    self.driver.get("https://weibo.com/")
                    for cookie in cookies:
                        self.driver.add_cookie(cookie)
            except:
                pass

    def _save_cookies(self):
        """保存cookies到文件"""
        cookies = self.driver.get_cookies()
        with open(self.cookies_file, 'w') as f:
            json.dump(cookies, f)


    def login(self, phone, country_code="+86"):
        """登录微博"""
        login_url = 'https://passport.weibo.com/sso/signin'
        # 尝试加载cookies进行登录
        self.driver.get(login_url)
        self._load_cookies()
        self.driver.refresh()
        time.sleep(3)
        print(self.driver.current_url)

        if self.driver.current_url != login_url:
            print("使用cookies登录成功")
            self._save_cookies()
            time.sleep(2)
            return
        else:
            # 清理无效的cookies
            self.driver.delete_all_cookies()
            print("无效的cookies，已清理")

        # 定位手机号输入框
        phone_input = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='手机号']")))
        phone_input.clear()
        phone_input.send_keys(phone)

        send_code_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.text-sm.text-alink.cursor-pointer")))
        send_code_btn.click()

        # 输入验证码
        verification_code = input("请输入验证码: ")
        code_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='验证码']")))
        code_input.clear()
        code_input.send_keys(verification_code)

        # 点击登录按钮
        login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div[2]/div[2]/button/span')))
        login_button.click()

        # 等待登录成功,获取token
        time.sleep(3)

        # 保存cookies
        self._save_cookies()

    def login_to_publish(self, content, images=None):
        self._load_cookies()
        self.driver.refresh()
        self.driver.get("https://weibo.com/")
        time.sleep(3)
        if self.driver.current_url != "https://weibo.com/":
            return False, "登录失败"

        # 输入内容
        print(content)
        content_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="homeWrap"]/div[1]/div/div[1]/div/textarea')))
        content_input.clear()
        content_input.send_keys(content)
        time.sleep(2)

        # 上传图片
        if images:
            print("upload images")
            upload_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
            upload_input.send_keys('\n'.join(images))

        time.sleep(2)
        # 等待发布按钮可用尝试进行发布
        try:
            submit_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="homeWrap"]/div[1]/div/div[4]/div/div[5]/button/span/span')))
            self.driver.execute_script("arguments[0].click();", submit_btn)
            print("Submit post")
            time.sleep(2)
            return True, "发布成功 "+content + "" + '\n'.join(images)
        except Exception as e:
            print("Submit post fail {}".format(e))
            return False, "发布失败"


    def close(self):
        """关闭浏览器"""
        self.driver.quit()

