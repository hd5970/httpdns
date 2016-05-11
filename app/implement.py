# coding=utf-8
from app import redis_store
from app.models import Domain

try:
    import cPickle as pickle
except ImportError:
    import pickle


def reload_redis(single_domain=None):
    if single_domain is None:
        redis_store.flushdb()
        domains = Domain.query.all()
        for domain in domains:
            if domain.priority:
                domain_ip_list = []
                domain_priority_list = []
                for single_ip in domain.ips:
                    domain_ip_list.append(single_ip.ip)
                    domain_priority_list.append(single_ip.priority)
                redis_store.set(domain.domain, pickle.dumps(domain_ip_list))
                domain_priority_list = generate_priority_list(domain_priority_list)
                redis_store.set('%s_priority' % domain.domain, pickle.dumps(domain_priority_list))
            else:
                redis_store.set(domain.domain, 0)
                for single_ip in domain.ips:
                    redis_store.set('%s_%s' % (domain.domain, single_ip.province_name), single_ip.ip)
    else:
        domain = Domain.query.filter_by(domain=single_domain).first()
        if domain.priority:
            domain_ip_list = []
            domain_priority_list = []
            for single_ip in domain.ips:
                domain_ip_list.append(single_ip.ip)
                domain_priority_list.append(single_ip.priority)
            redis_store.set(domain.domain, pickle.dumps(domain_ip_list))
            domain_priority_list = generate_priority_list(domain_priority_list)
            redis_store.set('%s_priority' % domain.domain, pickle.dumps(domain_priority_list))
        else:
            redis_store.set(domain.domain, 0)
            for single_ip in domain.ips:
                redis_store.set('%s_%s' % (domain.domain, single_ip.province_name), single_ip.ip)


def generate_priority_list(s):
    def gcd(a):
        a.sort()
        temp_min = a[0]
        gcd_result = 1
        for temp in range(2, temp_min + 1):
            flag = True
            for j in a:
                if j % temp != 0:
                    flag = False
            if flag:
                gcd_result = temp
        return gcd_result

    result = []
    n = len(s)
    i = -1
    current = 0
    counter = 0
    gcd_s = gcd(s)
    max_s = max(s)
    while counter <= sum(s):
        i = (i + 1) % n
        if i == 0:
            current -= gcd_s
            if current <= 0:
                current = max_s
        if s[i] >= current:
            result.append(i)
        counter += 1
    print result
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
