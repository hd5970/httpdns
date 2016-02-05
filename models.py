from app import db


class Domain(db.Model):
    __tablename__ = 'domain'
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(128), index=True)
    first_class = db.Column(db.String(128), index=True)
    description = db.Column(db.TEXT)
    ips = db.relationship('IP', backref='domain', lazy='dynamic')


class IP(db.Model):
    __tablename__ = 'ip'
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(128), db.ForeignKey('domain.domain'))
    priority = db.Column(db.Integer, index=True)
