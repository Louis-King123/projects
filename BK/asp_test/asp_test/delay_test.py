import requests

import time
import requests

url_login = 'http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex03/'

session = requests.Session()

test = session.get('http://www.baidu.com', timeout=15)
print(test.content)
print(round(test.elapsed.microseconds/1000))
