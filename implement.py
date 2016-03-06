# coding=utf-8
from app import db, redis_store
from models import Province, Domain

try:
    import cPickle as pickle
except ImportError:
    import pickle


def reload_redis():
    redis_store.flushdb()
    # provinces = Province.query.all()
    # for province in provinces:
    #     redis_store.set(province.name, )
    domains = Domain.query.all()
    for domain in domains:
        if domain.priority:
            domain_ip_list = []
            domain_priority_list = []
            for single_ip in domain.ips:
                domain_ip_list.append(single_ip.ip)
                domain_priority_list.append(single_ip.priority)
            redis_store.set(domain.domain, pickle.dumps(domain_ip_list))
            domain_priority_list = current_choice(domain_priority_list)
            redis_store.set('%s_priority' % domain.domain, pickle.dumps(domain_priority_list))
        else:
            redis_store.set(domain.domain, 0)
            for single_ip in domain.ips:
                redis_store.set('%s_%s' % (domain.domain, single_ip.province_name), single_ip.ip)
    print redis_store.keys()


def current_choice(s):
    def gcd(a):
        a.sort()
        temp_min = a[0]
        result = 1
        for i in range(2, temp_min + 1):
            flag = True
            for j in a:
                if j % i != 0:
                    flag = False
            if flag:
                result = i
        return result

    result = []
    n = len(s)
    i = -1
    current = 0
    counter = 0
    while counter < sum(s):
        i = (i + 1) % n
        if i == 0:
            current -= gcd(s)
            if current <= 0:
                current = max(s)
        if s[i] >= current:
            result.append(i)
        counter += 1
    return result

# 迭代方式的加权轮训在协程中失败
# def current_choice(s):
#     def gcd(a):
#         a.sort()
#         temp_min = a[0]
#         result = 1
#         for i in range(2, temp_min + 1):
#             flag = True
#             for j in a:
#                 if j % i != 0:
#                     flag = False
#             if flag:
#                 result = i
#         return result
#
#     n = len(s)
#     i = -1
#     current = 0
#     while True:
#         i = (i + 1) % n
#         if i == 0:
#             current -= gcd(s)
#             if current <= 0:
#                 current = max(s)
#         if s[i] >= current:
#             yield i
#     return

#
# nice = [2, 8, 16]
# c = current_choice(nice)
#
# for i in xrange(30):
#     i += 1
#     print nice[c.next()]
