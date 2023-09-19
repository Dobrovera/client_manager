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
@app.get('/nsi')
def get_nsi():
    if current_user.is_authenticated:
        return render_template("NSIs/nsi_list.html")
    else:
        return redirect(url_for('home'))

@cross_origin()
@app.get('/nsi/object_type/add')
@app.get('/nsi/mis_type/add')
@app.get('/nsi/info_system/add')
@app.get('/nsi/modules/add')
@app.get('/nsi/semd_sms/add')
@app.get('/nsi/statuses/add')
def get_object_type_add():
    if current_user.is_authenticated:
        return render_template("NSIs/add.html")
    else:
        return redirect(url_for('home'))


'''Справочник "Тип объекта"'''


@cross_origin()
@app.get('/nsi/object_type')
def get_object_type_nsi():
    if current_user.is_authenticated:
        return render_template("NSIs/nsi_values_table.html",
                               name='Тип объекта',
                               nsi=ObjectType.query.all(),
                               ref='object_type',
                               )
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.post('/nsi/object_type/add')
def post_object_type_add():
    if current_user.is_authenticated:
        name = request.form.get('name')
        if name:
            if ObjectType.query.filter(ObjectType.name == name).all():
                flash('Имя уже существует', category='warning')
                return render_template('NSIs/add.html')
            else:
                new_object_type = ObjectType(name=name)
                db.session.add(new_object_type)
                db.session.commit()
                flash('Справочник успешно обновлен', category='success')
                return render_template('NSIs/nsi_values_table.html',
                                       nsi=ObjectType.query.all(),
                                       name='Тип объекта',
                                       ref='object_type',
                                       )
        else:
            flash('Введите название', category='warning')
            return redirect(url_for('post_object_type_add'))
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.route('/nsi/object_type/delete/<int:id>')
def delete_obj_type(id):
    obj_type_delete = ObjectType.query.get_or_404(id)
    try:
        db.session.delete(obj_type_delete)
        db.session.commit()
        flash('Успешно удалено', category='success')
        return redirect('/nsi/object_type')
    except:
        return redirect('/nsi/object_type')


@cross_origin()
@app.get('/nsi/object_type/update/<int:id>')
def update_object_type_get(id):
    if current_user.is_authenticated:
        nsi = ObjectType.query.filter_by(id=id).first()
        return render_template("NSIs/update.html",
                               nsi=nsi,
                               ref='object_type',
                               )
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.post('/nsi/object_type/update/<int:id>')
def update_object_type_post(id):
    if current_user.is_authenticated:
        nsi = ObjectType.query.filter_by(id=id).first()
        nsi.name = request.form['name']
        try:
            db.session.commit()
            flash("Значение успешно обновлено", category='success')
            return render_template("NSIs/nsi_values_table.html",
                                   nsi=ObjectType.query.order_by(ObjectType.id).all(),
                                   name='Тип объекта',
                                   ref='object_type',
                                   )
        except:
            flash("Что-то пошло не так", category='warning')
            return redirect(url_for('get_all_users'))


'''Справочник "Тип МИС"'''


@cross_origin()
@app.get('/nsi/mis_type')
def get_mis_type_nsi():
    if current_user.is_authenticated:
        return render_template('NSIs/nsi_values_table.html',
                               nsi=MISType.query.all(),
                               name='Тип МИС',
                               ref='mis_type',
                               )
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.post('/nsi/mis_type/add')
def post_mis_type_add():
    if current_user.is_authenticated:
        name = request.form.get('name')
        if name:
            if MISType.query.filter(MISType.name == name).all():
                flash('Имя уже существует', category='warning')
                return render_template('NSIs/add.html')
            else:
                new_object_type = MISType(name=name)
                db.session.add(new_object_type)
                db.session.commit()
                flash('Справочник успешно обновлен', category='success')
                return render_template('NSIs/nsi_values_table.html',
                                       nsi=MISType.query.all(),
                                       name='Тип МИС',
                                       ref='mis_type',
                                       )
        else:
            flash('Введите название', category='warning')
            return redirect(url_for('post_object_type_add'))
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.route('/nsi/mis_type/delete/<int:id>')
def delete_mis_type(id):
    mis_type_delete = MISType.query.get_or_404(id)
    try:
        db.session.delete(mis_type_delete)
        db.session.commit()
        flash('Успешно удалено', category='success')
        return redirect('/nsi/mis_type')
    except:
        return redirect('/nsi/mis_type')


@cross_origin()
@app.get('/nsi/mis_type/update/<int:id>')
def update_mis_type_get(id):
    if current_user.is_authenticated:
        nsi = MISType.query.filter_by(id=id).first()
        return render_template("NSIs/update.html",
                               nsi=nsi,
                               ref='mis_type',
                               )
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.post('/nsi/mis_type/update/<int:id>')
def update_mis_type_post(id):
    if current_user.is_authenticated:
        nsi = MISType.query.filter_by(id=id).first()
        nsi.name = request.form['name']
        try:
            db.session.commit()
            flash("Значение успешно обновлено", category='success')
            return render_template("NSIs/nsi_values_table.html",
                                   nsi=MISType.query.order_by(MISType.id).all(),
                                   name='Тип МИС',
                                   ref='mis_type',
                                   )
        except:
            flash("Что-то пошло не так", category='warning')
            return redirect(url_for('get_mis_type_nsi'))


'''Справочник "Информационные системы"'''


@cross_origin()
@app.get('/nsi/info_system')
def get_info_system_nsi():
    if current_user.is_authenticated:
        return render_template("NSIs/nsi_values_table.html",
                               nsi=InfoSystem.query.all(),
                               name='Информационные системы',
                               ref='info_system',
                               )
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.post('/nsi/info_system/add')
def post_info_system_add():
    if current_user.is_authenticated:
        name = request.form.get('name')
        if name:
            if InfoSystem.query.filter(InfoSystem.name == name).all():
                flash('Имя уже существует', category='warning')
                return render_template('NSIs/add.html')
            else:
                new_object_type = InfoSystem(name=name)
                db.session.add(new_object_type)
                db.session.commit()
                flash('Справочник успешно обновлен', category='success')
                return render_template('NSIs/nsi_values_table.html',
                                       nsi=InfoSystem.query.all(),
                                       name='Информационные системы',
                                       ref='info_system',
                                       )
        else:
            flash('Введите название', category='warning')
            return redirect(url_for('post_object_type_add'))
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.route('/nsi/info_system/delete/<int:id>')
def delete_info_system(id):
    info_system_delete = InfoSystem.query.get_or_404(id)
    try:
        db.session.delete(info_system_delete)
        db.session.commit()
        flash('Успешно удалено', category='success')
        return redirect('/nsi/info_system')
    except:
        return redirect('/nsi/info_system')


@cross_origin()
@app.get('/nsi/info_system/update/<int:id>')
def update_info_system_get(id):
    if current_user.is_authenticated:
        nsi = InfoSystem.query.filter_by(id=id).first()
        return render_template("NSIs/update.html",
                               nsi=nsi,
                               ref='info_system',
                               )
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.post('/nsi/info_system/update/<int:id>')
def update_info_system_post(id):
    if current_user.is_authenticated:
        nsi = InfoSystem.query.filter_by(id=id).first()
        nsi.name = request.form['name']
        try:
            db.session.commit()
            flash("Значение успешно обновлено", category='success')
            return render_template("NSIs/nsi_values_table.html",
                                   nsi=InfoSystem.query.order_by(InfoSystem.id).all(),
                                   name='Информационные системы',
                                   ref='info_system',
                                   )
        except:
            flash("Что-то пошло не так", category='warning')
            return redirect(url_for('get_info_system_nsi'))


'''Справочник "Модули"'''


@cross_origin()
@app.get('/nsi/modules')
def get_modules_nsi():
    if current_user.is_authenticated:
        return render_template("NSIs/nsi_values_table.html",
                               nsi=Modules.query.all(),
                               name='Модули',
                               ref='modules',
                               )
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.post('/nsi/modules/add')
def post_modules_add():
    if current_user.is_authenticated:
        name = request.form.get('name')
        if name:
            if Modules.query.filter(Modules.name == name).all():
                flash('Имя уже существует', category='warning')
                return render_template('NSIs/add.html')
            else:
                new_object_type = Modules(name=name)
                db.session.add(new_object_type)
                db.session.commit()
                flash('Справочник успешно обновлен', category='success')
                return render_template('NSIs/nsi_values_table.html',
                                       nsi=Modules.query.all(),
                                       name='Модули',
                                       ref='modules',
                                       )
        else:
            flash('Введите название', category='warning')
            return redirect(url_for('post_object_type_add'))
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.route('/nsi/modules/delete/<int:id>')
def delete_modules(id):
    modules_delete = Modules.query.get_or_404(id)
    try:
        db.session.delete(modules_delete)
        db.session.commit()
        flash('Успешно удалено', category='success')
        return redirect('/nsi/modules')
    except:
        return redirect('/nsi/modules')


@cross_origin()
@app.get('/nsi/modules/update/<int:id>')
def update_module_get(id):
    if current_user.is_authenticated:
        nsi = Modules.query.filter_by(id=id).first()
        return render_template("NSIs/update.html",
                               nsi=nsi,
                               ref='modules',
                               )
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.post('/nsi/modules/update/<int:id>')
def update_module_post(id):
    if current_user.is_authenticated:
        nsi = Modules.query.filter_by(id=id).first()
        nsi.name = request.form['name']
        try:
            db.session.commit()
            flash("Значение успешно обновлено", category='success')
            return render_template("NSIs/nsi_values_table.html",
                                   nsi=Modules.query.order_by(Modules.id).all(),
                                   name='Модули',
                                   ref='modules',
                                   )
        except:
            flash("Что-то пошло не так", category='warning')
            return redirect(url_for('get_modules_nsi'))


'''Справочник "СЭМД/СМС"'''


@cross_origin()
@app.get('/nsi/semd_sms')
def get_sms_nsi():
    if current_user.is_authenticated:
        return render_template("NSIs/nsi_values_table.html",
                               nsi=SMS.query.order_by(SMS.id).all(),
                               name='СЭМД/СМС',
                               ref='semd_sms',
                               )
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.post('/nsi/semd_sms/add')
def post_sms_add():
    if current_user.is_authenticated:
        name = request.form.get('name')
        if name:
            if SMS.query.filter(SMS.name == name).all():
                flash('Имя уже существует', category='warning')
                return render_template('NSIs/add.html')
            else:
                new_object_type = SMS(name=name)
                db.session.add(new_object_type)
                db.session.commit()
                flash('Справочник успешно обновлен', category='success')
                return render_template('NSIs/nsi_values_table.html',
                                       nsi=SMS.query.all(),
                                       name='СЭМД/СМС',
                                       ref='semd_sms',
                                       )
        else:
            flash('Введите название', category='warning')
            return redirect(url_for('post_object_type_add'))
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.route('/nsi/semd_sms/delete/<int:id>')
def delete_sms(id):
    sms_delete = SMS.query.get_or_404(id)
    try:
        db.session.delete(sms_delete)
        db.session.commit()
        flash('Успешно удалено', category='success')
        return redirect('/nsi/semd_sms')
    except:
        return redirect('/nsi/semd_sms')


@cross_origin()
@app.get('/nsi/semd_sms/update/<int:id>')
def update_sms_get(id):
    if current_user.is_authenticated:
        nsi = SMS.query.filter_by(id=id).first()
        return render_template("NSIs/update.html",
                               nsi=nsi,
                               ref='semd_sms',
                               )
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.post('/nsi/semd_sms/update/<int:id>')
def update_sms_post(id):
    if current_user.is_authenticated:
        sms_to_upd = SMS.query.filter_by(id=id).first()
        sms_to_upd.name = request.form['name']
        try:
            db.session.commit()
            flash("Значение успешно обновлено", category='success')
            return render_template("NSIs/nsi_values_table.html",
                                   nsi=SMS.query.order_by(SMS.id).all(),
                                   name='СЭМД/СМС',
                                   ref='semd_sms',
                                   )
        except:
            flash("Что-то пошло не так", category='warning')
            return redirect(url_for('get_sms_nsi'))


'''Справочник "Статусы"'''


@cross_origin()
@app.get('/nsi/statuses')
def get_status_nsi():
    if current_user.is_authenticated:
        return render_template("NSIs/nsi_values_table.html",
                               nsi=Status.query.order_by(Status.id).all(),
                               name='Статусы',
                               ref='statuses',
                               )
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.post('/nsi/statuses/add')
def post_status_add():
    if current_user.is_authenticated:
        name = request.form.get('name')
        if name:
            if Status.query.filter(Status.name == name).all():
                flash('Имя уже существует', category='warning')
                return render_template('NSIs/add.html')
            else:
                new_status = Status(name=name)
                db.session.add(new_status)
                db.session.commit()
                flash('Справочник успешно обновлен', category='success')
                return render_template('NSIs/nsi_values_table.html',
                                       nsi=Status.query.all(),
                                       name='Статусы',
                                       ref='statuses',
                                       )
        else:
            flash('Введите название', category='warning')
            return redirect(url_for('post_status_add'))
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.route('/nsi/statuses/delete/<int:id>')
def delete_status(id):
    status_delete = Status.query.get_or_404(id)
    try:
        db.session.delete(status_delete)
        db.session.commit()
        flash('Успешно удалено', category='success')
        return redirect('/nsi/statuses')
    except:
        return redirect('/nsi/statuses')


@cross_origin()
@app.get('/nsi/statuses/update/<int:id>')
def update_status_get(id):
    if current_user.is_authenticated:
        nsi = Status.query.filter_by(id=id).first()
        return render_template("NSIs/update.html",
                               nsi=nsi,
                               ref='statuses',
                               )
    else:
        return redirect(url_for('home'))


@cross_origin()
@app.post('/nsi/statuses/update/<int:id>')
def update_status_post(id):
    if current_user.is_authenticated:
        status_to_upd = Status.query.filter_by(id=id).first()
        status_to_upd.name = request.form['name']
        try:
            db.session.commit()
            flash("Значение успешно обновлено", category='success')
            return render_template("NSIs/nsi_values_table.html",
                                   nsi=Status.query.order_by(Status.id).all(),
                                   name='Статусы',
                                   ref='statuses',
                                   )
        except:
            flash("Что-то пошло не так", category='warning')
            return redirect(url_for('get_status_nsi'))
