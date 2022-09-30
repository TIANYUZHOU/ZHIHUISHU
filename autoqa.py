"""
QA
"""

import time
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By

UESER_INFO_ROOT = "./userinfo.json"
QA_URL_ROOT = "./qaurl.txt"

URLS = [""]


class AutoQA:
    r"""
    Automatic question and answer
    """

    def __init__(self, urls: Optional[List[str]] = None):
        self.user_info = {}
        self.urls = []
        self.read_urls(urls)
        self.driver = webdriver.Chrome()

    def read_urls(self, urls: Optional[List[str]] = None):
        r"""
        read urls
        """
        if urls is None:
            with open(QA_URL_ROOT, 'r', encoding="utf8") as url_data:
                for line in url_data.readlines():
                    self.urls.append(line.strip())
        else:
            self.urls.extend(urls)
        return self.urls

    def get_urls(self):
        r"""
        get urls
        """
        return self.urls

    def login_qapage(self):
        r"""
        login qapage
        """
        self.driver.get(self.urls[0])
        input_username = self.driver.find_element(
            By.XPATH, '//*[@id="lUsername"]')
        input_passwordd = self.driver.find_element(
            By.XPATH, '//*[@id="lPassword"]')
        login_botton = self.driver.find_element(
            By.XPATH, '//*[@id="f_sign_up"]/div[1]/span')
        input_username.send_keys(self.user_info['username'])
        input_passwordd.send_keys(self.user_info['password'])
        login_botton.click()

    def get_qa(self):
        r"""
        get qa
        """
        question_xpath = '//*[@id="app"]/div/div[2]/div[1]\
            /div/div[2]/div[1]/div/ul/li[@class="question-item"]'
        question = self.driver.find_element(By.XPATH, question_xpath)
        question.click()
        answer_xpath = '//*[@id="app"]/div/div[3]/div[1]/div[2]\
            /ul/li[1]/div[@class="answer-content"]/p/span'
        answer = self.driver.find_element(By.XPATH, answer_xpath).text
        print(answer)


if __name__ == '__main__':
    AUTO_QA = AutoQA()
    # print(AUTO_QA.get_urls())
    AUTO_QA.login_qapage()
    time.sleep(5)
    AUTO_QA.get_qa()
