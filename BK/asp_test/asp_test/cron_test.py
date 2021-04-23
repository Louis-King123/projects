# -*- coding: utf-8 -*-

import datetime


def ct():
    with open('text.txt', 'rw') as f:

        f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
