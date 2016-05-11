# -*- coding: utf-8 -*-
import os
import random

from ipip import IP

dat_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ip.dat')
IP.load(dat_path)


def get_ip_locality(ip):
    # fake province name for localhost
    if ip == '127.0.0.1':
        all_provinces = [u'湖北', u'湖南', u'河南', u'河北', u'山东', u'山西',
                         u'江西', u'江苏', u'浙江', u'黑龙江', u'新疆', u'云南',
                         u'贵州', u'福建', u'吉林', u'安徽', u'四川', u'西藏',
                         u'宁夏', u'辽宁', u'青海', u'甘肃', u'陕西', u'内蒙',
                         u'台湾', u'北京', u'上海', u'海南', u'天津', u'重庆']
        return random.choice(all_provinces)
    raw = IP.find(ip)
    return raw[3:5]
