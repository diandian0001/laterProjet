# coding: utf-8
import random
import string

import requests


class YunPian(object):
    # 发送短信的工具类
    def __init__(self, api_key="40d6180426417bfc57d0744a362dc108"):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    @staticmethod
    def __get_code():
        # 生成验证码
        code = random.sample(string.digits, 6)
        # print("".join(code))
        return "".join(code)

    def send_msg(self, mobile='17680274515'):
        code = self.__get_code()
        params = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【毛信宇test】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }
        response = requests.post(self.single_send_url, data=params)
        # print(response)
        print(code)
        return code


if __name__ == '__main__':
    y = YunPian()
    y.send_msg('17680274515')