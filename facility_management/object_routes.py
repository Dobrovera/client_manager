from flask import render_template, request, redirect, \
    url_for, flash
import psycopg2
from flask_login import current_user
from flask_cors import cross_origin


from facility_management import  app
from facility_management.settings import *
from facility_management.models import *

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)


@cross_origin()
@app.get('/objects')
def get_objects_list():
    if current_user.is_authenticated:
        object_obj = Object.query.all()
        return render_template('object/objects_list.html',
                               object_obj=object_obj,
                               )
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.get('/objects/add')
def get_objects_add():
    if current_user.is_authenticated:
        object_type = ObjectType.query.all()
        mis_type = MISType.query.all()
        users = User.query.all()
        modules = Modules.query.all()
        semd_sms = SMS.query.all()
        status = Status.query.all()
        info_sys = InfoSystem.query.all()
        return render_template("object/object_add.html",
                               object_type=object_type,
                               mis_type=mis_type,
                               users=users,
                               modules=modules,
                               semd_sms=semd_sms,
                               statuses=status,
                               info_sys=info_sys,
                               )
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.post('/objects/add')
def post_objects_add():
    name = request.form.get('name')
    short_name = request.form.get('short_name')
    site_link = request.form.get('site_link')
    address = request.form.get('address')
    address_comment = request.form.get('address_comment')
    object_type_id = request.form.get('object_type_id')
    object_comment = request.form.get('object_comment')
    financial_features = request.form.get('financial_features')
    problem_description = request.form.get('problem_description')
    task_link = request.form.get('task_link')
    problem_deadline = request.form.get('problem_deadline')
    actuality = True if request.form.get('actuality') else False
    vpn_enidesk = request.form.get('vpn_enidesk')
    tadam_link = request.form.get('tadam_link')
    youtrack_link = request.form.get('youtrack_link')
    executor_id = request.form.get('executor_id')
    user_visit_id = request.form.getlist('user_visit_id')
    departure_date = request.form.get('departure_date')
    departure_specifics = request.form.get('departure_specifics')
    departure_reason = request.form.get('departure_reason')
    departure_comment = request.form.get('departure_comment')
    sms_id = request.form.get('sms_id')
    status_id = request.form.get('status_id')
    current_release = request.form.get('current_release')
    sms_launch_date = request.form.get('sms_launch_date')
    info_sys_list = request.form.getlist('IS_id')

    new_object = Object(
        name=name,
        short_name=short_name,
        site_link=site_link,
        financial_features=financial_features,
        current_release=current_release,
        vpn_enidesk=vpn_enidesk,
        tadam_link=tadam_link,
        youtrack_link=youtrack_link,
        departure_specifics=departure_specifics,
        executor=executor_id,
    )

    db.session.add(new_object)
    db.session.commit()
    object = db.session.query(Object.id).filter(Object.name == name).one()
    object_id = object.id

    new_object_problem = ObjectProblemList(
        object_id=object_id,
        description=problem_description,
        task_link=task_link,
        deadline=problem_deadline,
        actuality=actuality,
    )

    db.session.add(new_object_problem)
    db.session.commit()

    new_address = ObjectAddress(
        object_id=object_id,
        address=address,
        comment=address_comment,
    )

    new_obj_obj_type = ObjectObjType(
        object_id=object_id,
        object_type_id=object_type_id,
        comment=object_comment,
    )

    for id in info_sys_list:
        new_info_sys = ObjectInfoSysList(
            object_id=object_id,
            infosys_id=id,
        )

        db.session.add(new_info_sys)
        db.session.commit()

    db.session.add(new_address)
    db.session.add(new_obj_obj_type)

    if request.form["btn"] == "sms":
        if sms_id and status_id and sms_launch_date:
            new_semd_sms = ObjectSemdSms(
                object_id=object_id,
                sms_id=sms_id,
                status_id=status_id,
                launch_date=sms_launch_date,
            )
            db.session.add(new_semd_sms)
        elif sms_id and status_id:
            new_semd_sms = ObjectSemdSms(
                object_id=object_id,
                sms_id=sms_id,
                status_id=status_id,
            )
            db.session.add(new_semd_sms)

    elif request.form["btn"] == "departure":
        if departure_date and departure_comment and departure_reason:
            new_visit = ObjectVisitList(
                object_id=object_id,
                departure_date=departure_date,
                departure_reason=departure_reason,
                comment=departure_comment,
            )
            db.session.add(new_visit)
            db.session.commit()
            visit = db.session.query(ObjectVisitList.id).filter(ObjectVisitList.id == new_visit.id).one()
            visit_id = visit.id
            for id in user_visit_id:
                new_specialist_visit = ObjectSpecialistVisitList(
                    obj_vis_list_id=visit_id,
                    user_id=id,
                )
                db.session.add(new_specialist_visit)
                db.session.commit()
        elif not departure_date or departure_comment or departure_reason:
            flash("Введите все данные", category='success')
            return redirect(url_for('post_objects_add'))

    db.session.commit()

    return redirect(url_for('get_objects_list'))

@cross_origin()
@app.get('/objects/<int:id>')
def get_object_card(id):
    if current_user.is_authenticated:
        users = User.query.all()
        object_card = Object.query.filter_by(id=id).first()
        executor_id = object_card.executor
        executor = User.query.filter_by(id=executor_id).first()
        object_type = ObjectObjType.query.filter_by(object_id=object_card.id).first()
        installation = ObjectInstallation.query.filter_by(object_id=object_card.id).first()
        info_sys = ObjectInfoSysList.query.filter_by(object_id=object_card.id).all()
        modules_list = ObjectModulesList.query.filter_by(object_id=object_card.id).all()
        problems = ObjectProblemList.query.filter_by(object_id=object_card.id).all()
        visits = ObjectVisitList.query.filter_by(object_id=object_card.id).all()
        addresses = ObjectAddress.query.filter_by(object_id=object_card.id).all()
        semd_sms = ObjectSemdSms.query.filter_by(object_id=object_card.id).all()
        visit_specialists = ObjectSpecialistVisitList.query.all()
        instal = ObjectInstallation.query.filter_by(object_id=object_card.id).all()
        sms = SMS.query.all()
        statuses = Status.query.all()
        modules = Modules.query.all()
        mis_type = MISType.query.all()
        return render_template("object/object_card.html",
                               users=users,
                               object_card=object_card,
                               executor=executor,
                               object_type=object_type,
                               installation=installation,
                               info_sys=info_sys,
                               modules_list=modules_list,
                               problems=problems,
                               visits=visits,
                               addresses=addresses,
                               semd_sms=semd_sms,
                               visit_specialists=visit_specialists,
                               statuses=statuses,
                               sms=sms,
                               modules=modules,
                               mis_type=mis_type,
                               instal=instal
                               )
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.post('/objects/<int:id>')
def post_object_card(id):
    if current_user.is_authenticated:
        user_visit_id = request.form.getlist('user_visit_id')
        departure_date = request.form.get('departure_date')
        departure_reason = request.form.get('departure_reason')
        departure_comment = request.form.get('departure_comment')
        object = Object.query.filter_by(id=id).first()
        object_id = object.id
        sms_id = request.form.get('sms_id')
        status_id = request.form.get('status_id')
        sms_launch_date = request.form.get('sms_launch_date')
        module_id = request.form.get('module_id')
        module_launch_date = request.form.get('module_launch_date')
        module_log_link = request.form.get('module_log_link')
        module_comment = request.form.get('module_comment')
        mis_id = request.form.get('mis_id')
        mis_comment = request.form.get('mis_comment')

        if request.form["btn"] == "sms":
            if sms_id and status_id and sms_launch_date:

                new_semd_sms = ObjectSemdSms(
                    object_id=object_id,
                    sms_id=sms_id,
                    status_id=status_id,
                    launch_date=sms_launch_date,
                )

                db.session.add(new_semd_sms)
                db.session.commit()
            elif sms_id and status_id:
                new_semd_sms = ObjectSemdSms(
                    object_id=object_id,
                    sms_id=sms_id,
                    status_id=status_id,
                )
                db.session.add(new_semd_sms)
                db.session.commit()
            else:
                flash("Введите все данные", category='success')

            return redirect(url_for('get_object_card', id=object_id))

        elif request.form["btn"] == "departure":
            if departure_date and departure_comment and departure_reason:
                new_visit = ObjectVisitList(
                    object_id=object_id,
                    departure_date=departure_date,
                    departure_reason=departure_reason,
                    comment=departure_comment,
                )
                db.session.add(new_visit)
                db.session.commit()
                visit = db.session.query(ObjectVisitList.id).filter(ObjectVisitList.id == new_visit.id).one()
                visit_id = visit.id

                for id in user_visit_id:
                    new_specialist_visit = ObjectSpecialistVisitList(
                        obj_vis_list_id=visit_id,
                        user_id=id,
                    )
                    db.session.add(new_specialist_visit)
                    db.session.commit()

                return redirect(url_for('get_object_card', id=object_id))

            elif not departure_date or departure_comment or departure_reason:
                flash("Введите все данные", category='success')
                return redirect(url_for('get_object_card', id=object_id))

        elif request.form["btn"] == "module":
            if module_id and module_launch_date and module_log_link and module_comment:

                new_module = ObjectModulesList(
                    object_id=object_id,
                    module_id=module_id,
                    launch_date=module_launch_date,
                    log_link=module_log_link,
                    comment=module_comment,
                )

                db.session.add(new_module)
                db.session.commit()

                return redirect(url_for('get_object_card', id=object_id))

            else:
                flash("Введите все данные", category='success')
                return redirect(url_for('get_object_card', id=object_id))

        elif request.form["btn"] == "installation":
            if mis_id and mis_comment:
                new_installation = ObjectInstallation(
                    object_id=object_id,
                    mis_type_id=mis_id,
                    comment=mis_comment,
                )

                db.session.add(new_installation)
                db.session.commit()

                return redirect(url_for('get_object_card', id=object_id))

            else:
                flash("Введите все данные", category='success')
                return redirect(url_for('get_object_card', id=object_id))
    else:
        return redirect(url_for('home'))
