"""
QA
"""

# pylint: disable=E,W,C

import random
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.text_rewriting import rewrite

class AutoQA:
    r"""
    Automatic question and answer
    """

    def __init__(self):
        self.user_info = {}
        self.urls = []
        self.get_config()
        self.driver = webdriver.Chrome()

    def get_config(self):
        r"""
        get config
        """
        file = 'config/config.ini'
        config = configparser.ConfigParser()
        config.read(file, encoding="utf-8")
        self.user_info = eval(config.get('USER_INFO', 'USER_INFO'))
        self.urls = eval(config.get('URL', 'URLS'))

    def get_user_info(self):
        r"""
        get user info
        """
        return self.user_info

    def get_urls(self):
        r"""
        get urls
        """
        return self.urls

    def get_driver(self):
        r"""
        get driver
        """
        return self.driver

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
        
    def select_question(self):
        r"""
        select question
        """
        question_xpath = '//*[@id="app"]/div/div[2]/div[1]\
            /div/div[2]/div[1]/div/ul/li[@class="question-item"]'
        # find_elements 返回的是列表，并且如果没匹配到，返回空列表
        question = self.driver.find_elements(By.XPATH, question_xpath)
        question[1].click()     
        
    def get_answer(self): 
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])

        is_answered_xpath = '//*[@id="app"]/div/div[4]/span'
        is_answered = self.driver.find_elements(By.XPATH, is_answered_xpath)
        if len(is_answered) != 0:
            answers_list_xpath = '//*[@id="app"]/div/div[3]/div[1]/div[2]/ul/li'
            # 问题下面的回答列表
            answers_list = self.driver.find_elements(By.XPATH, answers_list_xpath)
            # 如果长度为 0 说明这个问题还没人回答，则关掉该问题标签页，并切换到前一页
            if len(answers_list) == 0:
                self.driver.close()
                self.driver.switch_to.window(windows[0])
                return False
            else:
                answer_text_list = []
                for answer in answers_list:
                    answer_text = answer.find_elements(By.XPATH, 'div[@class="answer-content"]/p/span')[0].text
                    answer_text_list.append(answer_text)
                
                final_answer_text_list = []
                min_len = 31
                
                while len(final_answer_text_list) == 0:
                    for answer in answer_text_list:
                        if len(answer) > min_len:
                            final_answer_text_list.append(answer)
                    min_len -= 5

                print(len(final_answer_text_list))
                # print(final_answer_text_list)
                random.shuffle(final_answer_text_list)
                # print(final_answer_text_list)
                is_answered[0].click()
                return final_answer_text_list
        else:
            print("已经回答过此问题！")
            self.driver.close()
            self.driver.switch_to.window(windows[0])
            return False

    def input_answer(self, text_list: list):
        r"""
        input answer
        """
        inputbox_xpath = '//*[@id="app"]/div/div\
            [@class="questionDialog ZHIHUISHU_QZMD"]/div/div/div[2]/div[1]/div[1]/div/textarea'
        inputbox = self.driver.find_elements(By.XPATH, inputbox_xpath)
        inputbox[0].send_keys(text_list[0])

    def submmit_answer(self):
        r"""
        submmit answer
        """
        submit_botton_xpath = '//*[@id="app"]/div/div\
            [@class="questionDialog ZHIHUISHU_QZMD"]/div/div/div[2]/div[1]/div[2]/div'

        submit_botton = self.driver.find_elements(By.XPATH, submit_botton_xpath)

        # submit_botton[0].click()


if __name__ == '__main__':
    # AUTO_QA = AutoQA()
    # print(AUTO_QA.get_urls()[0])
    # print(type(AUTO_QA.get_urls()[0]))
    # AUTO_QA.login_qapage()
    # time.sleep(5)
    # AUTO_QA.get_qa()
    # print(AUTO_QA.get_urls())
    pass
