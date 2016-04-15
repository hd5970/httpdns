# coding=utf-8
from app import db



class Domain(db.Model):
    __tablename__ = 'domain'
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(128), index=True)
    first_class = db.Column(db.String(128), index=True)
    description = db.Column(db.TEXT)
    ips = db.relationship('IP', backref='domain', lazy='dynamic')
    # 是否按照优先级
    priority = db.Column(db.Boolean, default=False)


class IP(db.Model):
    __tablename__ = 'ip'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(64), index=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domain.id'))
    priority = db.Column(db.Integer, index=True)
    province_name = db.Column(db.String, db.ForeignKey('province.name'))


class Province(db.Model):
    __tablename__ = 'province'
    name = db.Column(db.String(64), primary_key=True)
    ips = db.relationship('IP', backref='province', lazy='dynamic')

    @staticmethod
    def insert_provinces():
        all_provinces = [u'湖北', u'湖南', u'河南', u'河北', u'山东', u'山西',
                         u'江西', u'江苏', u'浙江', u'黑龙江', u'新疆', u'云南',
                         u'贵州', u'福建', u'吉林', u'安徽', u'四川', u'西藏',
                         u'宁夏', u'辽宁', u'青海', u'甘肃', u'陕西', u'内蒙',
                         u'台湾', u'北京', u'上海', u'海南', u'天津', u'重庆']
        for p in all_provinces:
            province = Province(
                name=p
            )
            db.session.add(province)
            db.session.commit()

    def __repr__(self):
        return '<Province %r>' % self.name


def get_all_provinces(choices=False, default=False):
    p_list = []
    if choices:
        if not default:
            p_list.append(('', u' '))
        for pro in Province.query.all():
            if pro.name == default:
                pro_tuple = (pro.name, pro.name)
                if p_list:
                    temp = p_list[0]
                    p_list[0] = pro_tuple
                else:
                    temp = pro_tuple
                p_list.append(temp)
            else:
                pro_tuple = (pro.name, pro.name)
                p_list.append(pro_tuple)
        return p_list
    else:
        for pro in Province.query.all():
            p_list.append(pro.name)
        return p_list
