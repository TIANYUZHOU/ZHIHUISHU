'''
1、文本改写 Web API 调用示例
2、运行前：请先填写Appid、APIKey、APISecret 相关信息
'''
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib
import base64
import hmac
from urllib.parse import urlencode
import json
import configparser
import requests

# pylint: disable=E,W,C


class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg


class Url:
    def __init__(self, host, path, schema):
        self.host = host
        self.path = path
        self.schema = schema


class wsParam(object):
    def __init__(self):
        self.APPID = ""
        self.APIKey = ""
        self.APISecret = ""
        self.url = 'https://api.xf-yun.com/v1/private/se3acbe7f'
        self.level = ""
        self.get_config()

    def parse_url(self, requset_url):
        stidx = requset_url.index("://")
        host = requset_url[stidx + 3:]
        schema = requset_url[:stidx + 3]
        edidx = host.index("/")
        if edidx <= 0:
            raise AssembleHeaderException("invalid request url:" + requset_url)
        path = host[edidx:]
        host = host[:edidx]
        u = Url(host, path, schema)
        return u

    def init_header(self):
        headers = {
            'content-type': "application/json",
            'host': 'api.xf-yun.com'
        }
        return headers

    def get_body(self, text):
        data = {
            "header": {
                "app_id": self.APPID,
                "status": 3,
            },
            "parameter": {
                "se3acbe7f": {
                    "level": self.level,
                    "result": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "json"
                    }
                }
            },
            "payload": {
                "input1": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "plain",
                    "status": 3,
                    "text": str(base64.b64encode(text.encode('utf-8')), 'utf-8')
                }
            }
        }
        body = json.dumps(data)
        return body

    def get_config(self):
        file = 'config/config.ini'
        config = configparser.ConfigParser()
        config.read(file, encoding="utf-8")
        self.APPID = config.get('API', 'APPID')
        self.APIKey = config.get('API', 'APIKey')
        self.APISecret = config.get('API', 'APISecret')
        self.level = "<L4>"  # 改写等级 <L1>  ~  <L6>  等级越高，改写程度越深


class ReWrite:
    def __init__(self) -> None:
        global wsParam
        self.wsParam = wsParam()

    def assemble_ws_auth_url(self, requset_url, method="POST", api_key="", api_secret=""):
        u = self.wsParam.parse_url(requset_url)
        host = u.host
        path = u.path
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        # print(date)
        # date = "Thu, 12 Dec 2019 01:57:27 GMT"
        signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(
            host, date, method, path)
        # print("----2", signature_origin)
        signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(
            signature_sha).decode(encoding='utf-8')
        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            api_key, "hmac-sha256", "host date request-line", signature_sha)
        # print("----1:", authorization_origin)
        authorization = base64.b64encode(
            authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # print(authorization_origin)
        values = {
            "host": host,
            "date": date,
            "authorization": authorization
        }
        return requset_url + "?" + urlencode(values)

    def rewrite(self, text: str):
        request_url = self.assemble_ws_auth_url(
            self.wsParam.url, "POST", self.wsParam.APIKey, self.wsParam.APISecret)
        # print("request_url:", request_url)
        response = requests.post(
            request_url, data=self.wsParam.get_body(text), headers=self.wsParam.init_header())
        # print("response:", response)
        str_result = response.content.decode('utf8')
        json_result = json.loads(str_result)
        # print("response-content:", json_result)
        if json_result. __contains__('header') and json_result['header']['code'] == 0:
            renew_text_list = json_result['payload']['result']['text']
            renew_text = eval(str(base64.b64decode(renew_text_list), 'utf-8'))
            # print("\n改写结果：", str(base64.b64decode(renew_text_list), 'utf-8'))
            print("=" * 50)
            print("原答案：", text)
            print("改写后：", renew_text[0][0])
        return renew_text[0][0]
