from datetime import datetime
from flask_login import UserMixin

from facility_management import db, manager


class Right(db.Model):
    __tablename__ = 'right'

    id = db.Column(db.Integer, primary_key=True)
    right_name = db.Column(db.String(100), nullable=False, unique=True)


class NSIs(db.Model):
    __tablename__ = 'nsis'

    id = db.Column(db.Integer, primary_key=True)
    nsi_name = db.Column(db.String(100), nullable=False, unique=True)
    nsi_rus_name = db.Column(db.String(100), nullable=False, unique=True)


class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    profile_name = db.Column(db.String(100), nullable=False, unique=True)
    user = db.relationship('User', backref='u')

class ProfileRight(db.Model):
    __tablename__ = 'profile_right'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    right_id = db.Column(db.Integer, db.ForeignKey("right.id"))


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    patronymic = db.Column(db.String(100))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120))
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    current = db.Column(db.Boolean, default=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    last_login = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    object_specialist_visit_list = db.relationship('ObjectSpecialistVisitList', backref='object_specialist_visit_list')


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


'''Справочники'''


class ObjectType(db.Model):
    __tablename__ = 'object_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    object_obj_type = db.relationship('ObjectObjType', backref='object_obj_type')


class MISType(db.Model):
    __tablename__ = 'MIS_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    object_installation = db.relationship('ObjectInstallation', backref='object_installation')


class InfoSystem(db.Model):
    __tablename__ = 'info_system'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    object_info_sys_list = db.relationship('ObjectInfoSysList', backref='object_info_sys_list')


class Modules(db.Model):
    __tablename__ = 'modules'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    object_modules_list = db.relationship('ObjectModulesList', backref='object_modules_list')


class SMS(db.Model):
    __tablename__ = 'semd_sms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    object_semd_sms = db.relationship('ObjectSemdSms', backref='object_semd_sms')


class Status(db.Model):
    __tablename__ = 'status'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    object_semd_sms = db.relationship('ObjectSemdSms', backref='object_sem_sms')


'''Модели для объекта'''


class Object(db.Model):
    __tablename__ = 'object'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    short_name = db.Column(db.Text, unique=True)
    site_link = db.Column(db.Text)
    financial_features = db.Column(db.Text)
    current_release = db.Column(db.Text)
    vpn_enidesk = db.Column(db.Text)
    tadam_link = db.Column(db.Text)
    youtrack_link = db.Column(db.Text)
    departure_specifics = db.Column(db.Text)
    executor = db.Column(db.Text)
    object_problem = db.relationship('ObjectProblemList', backref='object_problem')
    object_visit_list = db.relationship('ObjectVisitList', backref='object_visit_list')
    object_address = db.relationship('ObjectAddress', backref='object_address')
    object_obj_type = db.relationship('ObjectObjType', backref='obj_type')
    object_installation = db.relationship('ObjectInstallation', backref='object_install')
    object_info_sys_list = db.relationship('ObjectInfoSysList', backref='object_info_sys')
    object_modules_list = db.relationship('ObjectModulesList', backref='object_modules')
    object_semd_sms = db.relationship('ObjectSemdSms', backref='object_sms')


class ObjectProblemList(db.Model):
    __tablename__ = 'object_problem_list'

    id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey("object.id"))
    description = db.Column(db.Text)
    task_link = db.Column(db.Text)
    deadline = db.Column(db.TIMESTAMP)
    actuality = db.Column(db.Boolean)


class ObjectVisitList(db.Model):
    __tablename__ = 'object_visit_list'

    id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey("object.id"))
    departure_date = db.Column(db.TIMESTAMP)
    departure_reason = db.Column(db.Text)
    comment = db.Column(db.Text)
    obj_vis_list_id = db.relationship('ObjectSpecialistVisitList', backref='object_specialist_visit')


class ObjectSpecialistVisitList(db.Model):
    __tablename__ = 'object_specialist_visit_list'

    id = db.Column(db.Integer, primary_key=True)
    obj_vis_list_id = db.Column(db.Integer, db.ForeignKey("object_visit_list.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class ObjectAddress(db.Model):
    __tablename__ = 'object_address'

    id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey("object.id"))
    address = db.Column(db.Text)
    comment = db.Column(db.Text)


class ObjectObjType(db.Model):
    __tablename__ = 'object_obj_type'

    id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey("object.id"))
    object_type_id = db.Column(db.Integer, db.ForeignKey("object_type.id"))
    comment = db.Column(db.Text)


class ObjectInstallation(db.Model):
    __tablename__ = 'object_installation'

    id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey("object.id"))
    mis_type_id = db.Column(db.Integer, db.ForeignKey("MIS_type.id"))
    comment = db.Column(db.Text)


class ObjectInfoSysList(db.Model):
    __tablename__ = 'object_info_sys_list'

    id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey("object.id"))
    infosys_id = db.Column(db.Integer, db.ForeignKey("info_system.id"))


class ObjectModulesList(db.Model):
    __tablename__ = 'object_modules_list'

    id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey("object.id"))
    module_id = db.Column(db.Integer, db.ForeignKey("modules.id"))
    launch_date = db.Column(db.TIMESTAMP)
    log_link = db.Column(db.Text)
    comment = db.Column(db.Text)


class ObjectSemdSms(db.Model):
    __tablename__ = 'object_semd_sms'

    id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey("object.id"))
    sms_id = db.Column(db.Integer, db.ForeignKey("semd_sms.id"))
    status_id = db.Column(db.Integer, db.ForeignKey("status.id"))
    launch_date = db.Column(db.TIMESTAMP)
