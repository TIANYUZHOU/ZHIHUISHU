"""
QA
"""

# pylint: disable=E,W,C

import time
import random
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.text_rewriting import ReWrite


class AutoQA:
    r"""
    Automatic question and answer
    """

    def __init__(self, answer_num: int):
        self.user_info = {}
        self.urls = []
        self.answered_num = 0
        self.driver = None
        self.answer_num = answer_num
        self.get_config()
        self.rewrite = ReWrite().rewrite

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

    def login_qapage(self, url:str):
        r"""
        login qapage
        """
        self.driver = webdriver.Chrome()
        self.driver.get(url)
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
        question_list_xpath = '//*[@id="app"]/div/div[2]/div[1]\
            /div/div[2]/div[1]/div/ul/li[@class="question-item"]'
        question_list = []
        to_answer_question_num = self.answer_num
        start_index = 0
        # 如果已回答的问题数量达到设定值，退出循环
        while self.answered_num < to_answer_question_num:
            # find_elements 返回的是列表，并且如果没匹配到，返回空列表
            question_list = self.driver.find_elements(By.XPATH, question_list_xpath)
            question_list = question_list[start_index:] 
            for question in question_list:
                question.click()
                self.get_answer()
                # 在这里判断的原因是：to_answer_question_num 可能小于 len(question_list)
                if self.answered_num >= to_answer_question_num:
                    break
            start_index = len(question_list)
            # 模拟滚动 加载更多问题
            js = 'document.querySelector("div.el-scrollbar__view").scrollIntoView(false)'
            self.driver.execute_script(js)
        print("=" * 50)
        print("已完成当前课程的回答，5s后关闭窗口...")
        time.sleep(5)
        self.driver.close()
        
    def get_answer(self):
        time.sleep(3) 
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
                min_len = 10
                
                while len(final_answer_text_list) == 0:
                    for answer in answer_text_list:
                        if len(answer) > min_len:
                            final_answer_text_list.append(answer)
                    min_len -= 5

                # print(len(final_answer_text_list))
                # print(final_answer_text_list)
                random.shuffle(final_answer_text_list)
                # print(final_answer_text_list)
                is_answered[0].click()
                self.input_answer(final_answer_text_list)
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
        time.sleep(2)
        inputbox_xpath = '//*[@id="app"]/div/div\
            [@class="questionDialog ZHIHUISHU_QZMD"]/div/div/div[2]/div[1]/div[1]/div/textarea'
        inputbox = self.driver.find_elements(By.XPATH, inputbox_xpath)
        input_text = self.rewrite(text_list[0])
        inputbox[0].send_keys(input_text)
        self.submmit_answer()
    
    def submmit_answer(self):
        r"""
        submmit answer
        """
        time.sleep(3)
        self.answered_num += 1
        self.driver.close()
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
        
    def run(self):
        r"""
        run
        """
        url_num = len(self.urls)
        print(f"共 {url_num} 条 url 需要处理，浏览器窗口会启动 {url_num} 次！")
        for url in self.urls:
            self.login_qapage(url=url)
            print("请在30s内完成登录验证码的输入并等待，否则自动回答无法进行！")
            time.sleep(30)
            print("-" * 50)
            print("开始选取问题，并回答...")
            print("-" * 50)
            try:
                self.select_question()
            except Exception as e:
                print(e)
            finally:
                print("！！脚本已终止！！")
        print("！！！已完成所有链接回答！！!")