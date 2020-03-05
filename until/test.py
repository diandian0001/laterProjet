# coding: utf-8
from redis import Redis
import time

red = Redis()

# red.set('1', 111, ex=10)
# print(red.get('1'))
# time.sleep(3)
# print(red.get('1'))
# time.sleep(7)
# print(red.get('1'))
# time.sleep(1)
# print(red.get('1'))