from datetime import datetime
from flask_login import UserMixin
from LogServer import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(16), unique=True, nullable=False)
    role = db.Column(db.String(5), default="USER")
    key = db.Column(db.String(6), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    salt = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(32))
    phone = db.Column(db.String(10))
    orginization_id = db.Column(db.Integer)
    orginization_role_id = db.Column(db.Integer, default=0)

    def __str__(self) -> str: return f"[{self.name:^18} @ {self.role:^12}]({self.email:32})"
    def __repr__(self) -> str: return self.name

class Orginization(db.Model):
    __tablename__ = 'orginizations'
    orginization_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(4), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    desc = db.Column(db.String(250))

    def __str__(self) -> str: return f"[{self.name}:^66]({self.orginization_id}) <{self.key}>"
    def __repr__(self) -> str: return self.orginization_id


class Project(db.Model):
    __tablename__ = 'projects'
    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_accessed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String(250))

    def __repr__(self) -> str: return f"[{self.name:^18}<{self.pid:^7}> << {self.uid:^5}] {self.date_created} -> {self.last_accessed}"

class SnapShot(db.Model):
    __tablename__ = 'snapshots'
    ssid = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey('projects.pid'), nullable=False)
    scope = db.Column(db.String(7), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str: return f"[{self.ssid:^5} << {self.pid:^7}] {self.timestamp}"

class SnapComponent(db.Model):
    __tablename__ = 'snapcomponents'
    scid = db.Column(db.Integer, primary_key=True)
    ssid = db.Column(db.Integer, db.ForeignKey('snapshots.ssid'), nullable=False)
    name = db.Column(db.String(16), nullable=False)
    type = db.Column(db.String(8), nullable=False)
    data = db.Column(db.String(250))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str: return f"({self.type.upper()})[{self.name:^18} @ {self.timestamp}]:: {self.data}"

class LogFile(db.Model):
    __tablename__ = 'logfiles'
    lfid = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey('projects.pid'), nullable=False)
    name = db.Column(db.String(12), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_accessed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str: return f"[{self.name:^14} << {self.pid:^7}] {self.date_created} -> {self.last_accessed}"


class LogStatement(db.Model):
    __tablename__ = 'logstatements'
    lsid = db.Column(db.Integer, primary_key=True)
    lfid = db.Column(db.Integer, db.ForeignKey('logfiles.lfid'), nullable=False)
    status = db.Column(db.String(6), default="STATUS")
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data = db.Column(db.String(250), default="")

    def __repr__(self) -> str: return f"({self.status.upper()})[{self.lfid:^7} @ {self.timestamp}]:: {self.data}"