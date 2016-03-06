import random

from flask import Flask, render_template, flash, url_for, redirect, request, jsonify, abort

from api import api
from api.errors import bad_request
from ip.main import get_ip_locality

from app import redis_store
from models import Domain, IP

try:
    import cPickle as pickle
except ImportError:
    import pickle


@api.route('/', methods=['post', 'get'])
def a():
    query = request.args.get('domain')
    if query:
        domain = query
    else:
        http_request = request.json
        result = {}
        if not request.json:
            abort(500)
        domain = http_request.get('domain')
        if not domain:
            return bad_request()
    result_domain = redis_store.get(domain)
    province = get_ip_locality(request.remote_addr)

    if result_domain:
        if result_domain == '0':
            a_record = redis_store.get('%s_%s' % (domain, province))
            matched = True
            if not a_record:
                invalid_province_domain = Domain.query.filter_by(domain=domain).first()
                a_record = IP.query.filter_by(domain_id=invalid_province_domain.id).first().ip
                matched = False
            result = {domain: a_record,
                      province: matched}
        elif result_domain:
            ip_list = pickle.loads(redis_store.get(domain))
            priority_list = pickle.loads(redis_store.get('%s_priority' % domain))
            index = random.choice(priority_list)
            result = {domain: ip_list[index],
                      'index': index}
        return jsonify(result)
    else:
        return bad_request()
