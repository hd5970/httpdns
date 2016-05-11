# coding=utf-8
from flask import render_template, flash, url_for, redirect

from app import db
from app.implement import reload_redis
from .forms import AddNameServer, data_to_form
from app.models import Domain, IP
from . import admin


@admin.route('/', methods=['get', 'post'])
def index():
    form = AddNameServer.set_provinces()
    if form.validate_on_submit():
        print form.data
        if not form.priority.data:
            print form.priority.data
            form.priority.data = 1
        current = Domain.query.filter_by(domain=form.domain.data).first()
        if not current:
            if not form.provinces.data:
                item = Domain(
                    domain=form.domain.data,
                    priority=True
                )
            else:
                item = Domain(
                    domain=form.domain.data,
                )
            db.session.add(item)
            db.session.commit()
            d_id = item.id
        else:
            d_id = current.id
        if form.provinces.data:
            ip = IP(
                ip=form.ip.data,
                domain_id=d_id,
                province_name=form.provinces.data
            )
        else:
            ip = IP(
                ip=form.ip.data,
                domain_id=d_id,
                priority=form.priority.data
            )
        db.session.add(ip)
        db.session.commit()
        flash(u'添加成功')
        reload_redis()
        return redirect(url_for('admin.records'))
    return render_template('admin.html', form=form)


@admin.route('/all', methods=['get', 'post'])
def records():
    all_domain = Domain.query.all()
    return render_template('all.html', list=all_domain)


@admin.route('/domain/<int:domain_id>', methods=['get', 'post'])
def domain_view(domain_id):
    current_domain = Domain.query.get_or_404(domain_id)
    if not current_domain.priority:
        form = data_to_form(current_domain)
        return render_template('domain.html', form=form)
    else:
        return redirect('admin.index')
