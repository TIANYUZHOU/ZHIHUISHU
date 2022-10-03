"""
QA
"""

# pylint: disable=E,W,C

import os
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

    def __init__(self):
        self.user_info = {}
        self.urls = []
        self.answered_num = 0
        self.driver = None
        self.answer_num = 0
        self.start_index = 0
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option(
            'excludeSwitches', ['enable-logging'])
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
        self.answer_num = int(config.get('ANSWER', 'ANSWER_NUM'))
        self.start_index = int(config.get('QUESTION', 'START')) - 1

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

    def login_qapage(self, url: str):
        r"""
        login qapage
        """
        self.answered_num = 0   # 上个课程链接回答完毕需要清零
        self.driver = webdriver.Chrome(options=self.options)
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

    def answer_question(self):
        r"""
        answer question
        """
        question_list_xpath = '//*[@id="app"]/div/div[2]/div[1]\
            /div/div[2]/div[1]/div/ul/li[@class="question-item"]'
        question_list = []
        to_answer_question_num = self.answer_num
        start_index = self.start_index
        for _ in range(start_index // 50):
            # 模拟滚动 加载更多问题
            js = 'document.querySelector("div.el-scrollbar__view").scrollIntoView(false)'
            self.driver.execute_script(js)
            time.sleep(2)
        # 如果已回答的问题数量达到设定值，退出循环
        while self.answered_num < to_answer_question_num:
            # find_elements 返回的是列表，并且如果没匹配到，返回空列表
            question_list = self.driver.find_elements(
                By.XPATH, question_list_xpath)
            question_list = question_list[start_index:]
            for question in question_list:
                time.sleep(3)
                question.find_element(By.TAG_NAME, 'span').click()
                self.get_answer()
                # 在这里判断的原因是：to_answer_questio
                # n_num 可能小于 len(question_list)
                if self.answered_num >= to_answer_question_num:
                    break
            start_index = len(question_list)
            # 模拟滚动 加载更多问题
            js = 'document.querySelector("div.el-scrollbar__view").scrollIntoView(false)'
            self.driver.execute_script(js)
        print("-" * 50)
        print(f"已完成当前课程 {self.answer_num} 个问题的回答，5s 后关闭浏览器...")
        time.sleep(5)
        self.driver.quit()

    def get_answer(self):
        r"""
        get answer
        """
        time.sleep(3)
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])

        is_answered_xpath = '//*[@id="app"]/div/div[4]/span'
        is_answered = self.driver.find_elements(By.XPATH, is_answered_xpath)
        if len(is_answered) != 0:
            answers_list_xpath = '//*[@id="app"]/div/div[3]/div[1]/div[2]/ul/li'
            # 问题下面的回答列表
            answers_list = self.driver.find_elements(
                By.XPATH, answers_list_xpath)
            # 如果长度为 0 说明这个问题还没人回答，则关掉该问题标签页，并切换到前一页
            if len(answers_list) == 0:
                self.driver.close()
                self.driver.switch_to.window(windows[0])
                print("<" * 50)
                print("此问题目前还无人回答！")
                return False
            else:
                answer_text_list = []
                for answer in answers_list:
                    answer_text = answer.find_elements(
                        By.XPATH, 'div[@class="answer-content"]/p/span')[0].text
                    answer_text_list.append(answer_text)

                final_answer_text_list = []
                min_len = 10

                while len(final_answer_text_list) == 0:
                    for answer in answer_text_list:
                        if len(answer) > min_len:
                            final_answer_text_list.append(answer)
                    min_len -= 5
                random.shuffle(final_answer_text_list)
                is_answered[0].click()
                self.input_answer(final_answer_text_list)
                return final_answer_text_list
        else:
            print("=" * 50)
            print("已经回答过此问题！")
            self.driver.close()
            self.driver.switch_to.window(windows[0])
            return False

    def input_answer(self, text_list: list):
        r"""
        input answer
        """
        time.sleep(5)
        inputbox_xpath = '//*[@id="app"]/div/div\
            [@class="questionDialog ZHIHUISHU_QZMD"]/div/div/div[2]/div[1]/div[1]/div/textarea'
        inputbox = self.driver.find_elements(By.XPATH, inputbox_xpath)
        # print("-------before rewrite------")
        input_text = self.rewrite(text_list[0])
        inputbox[0].send_keys(input_text)
        self.submmit_answer()

    def submmit_answer(self):
        r"""
        submmit answer
        """
        time.sleep(2)
        up_btn_list = self.driver.find_elements(
            By.CSS_SELECTOR, "div.dialog-bottom > div.up-btn")
        up_btn_list[0].click()
        time.sleep(2)
        self.answered_num += 1
        self.driver.close()
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])

    def run(self):
        r"""
        run
        """
        print("-" * 50)
        print("！！！！！脚本开始运行！！！！！")
        url_num = len(self.urls)
        print("-" * 50)
        print(f"共 {url_num} 条 url 需要处理，浏览器会启动 {url_num} 次！")
        print(f">>>>>！请注意需要输入 {url_num} 次验证码！<<<<<")
        for url in self.urls:
            self.login_qapage(url=url)
            print("请在 15s 内完成登录验证码的输入并等待，否则自动回答无法进行！")
            time.sleep(15)
            print("-" * 50)
            print("开始选取问题并回答...")
            try:
                self.answer_question()
                print("-" * 50)
                print(">>>>>>>>>>！！！已关闭浏览器！！！<<<<<<<<<<")
            except Exception as e:
                print(">>>>>>>>>>！！！发生错误！！！<<<<<<<<<<")
                print(e)
                print("<<<<<<<<<<！脚本已终止运行！>>>>>>>>>")
        print("-" * 50)
        print(">>>>>>>>>>！！！已完成所有课程回答！！！<<<<<<<<<<")
        print("<<<<<<<<<<！脚本已终止运行！>>>>>>>>>")


if __name__ == "__main__":
    autoqa = AutoQA()
    autoqa.run()
    os.system("pause")
