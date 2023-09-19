from facility_management import db
from facility_management.models import *


def create_nsi():

    obj_type = [
                ObjectType(name='Амбулатория'),
                ObjectType(name='Стационар'),
                ObjectType(name='Федеральный'),
                ObjectType(name='Санаторий'),
                ObjectType(name='Другое')
    ]

    mis_type = [
                MISType(name='Виста десктоп'),
                MISType(name='Докторрум'),
                MISType(name='Виста+Докторрум'),
                MISType(name='ГНЦ'),
                MISType(name='Другое'),
    ]

    info_sys = [
                InfoSystem(name='Виста'),
                InfoSystem(name='Докторрум'),
                InfoSystem(name='Травма'),
                InfoSystem(name='Склад аптеки'),
                InfoSystem(name='Аптека (Листы назначения/исполнения/списания)'),
                InfoSystem(name='Оперблок'),
                InfoSystem(name='Личный кабинет пациента'),
                InfoSystem(name='Контроль качества'),
                InfoSystem(name='Веб регистратура'),
                InfoSystem(name='Мобильное приложение врача'),
                InfoSystem(name='Очередь'),
                InfoSystem(name='Инфомат')
    ]

    modules = [
                Modules(name='Newegisz'),
                Modules(name='ИЭМК (РЭМД+ВИМИС) региональный'),
                Modules(name='ИЭМК Федеральный'),
                Modules(name='РЭМД Федеральный'),
                Modules(name='ВИМИС Федеральный'),
                Modules(name='Телемедицина'),
                Modules(name='Очередь'),
                Modules(name='Инфомат'),
                Modules(name='ОДЛИ'),
                Modules(name='ОДИИ'),
                Modules(name='Обмен с ЛИС'),
                Modules(name='Обмен с РИС'),
                Modules(name='Запись на приём к врачу'),
    ]

    sms = [
            SMS(name='Эпикриз амбулаторный'),
            SMS(name='Эпикриз стационар'),
            SMS(name='МСЭ'),
            SMS(name='Прием (осмотр) врача-специалиста АКИНЕО'),
            SMS(name='Прием (осмотр) врача-специалиста ССЗ'),
            SMS(name='Прием (осмотр) врача-специалиста Онко'),
            SMS(name='Прием (осмотр) врача-специалиста Профилактика'),
    ]

    status = [
            Status(name='Не нужен'),
            Status(name='Не разработан'),
            Status(name='Не настроен'),
            Status(name='Выгружается'),
            Status(name='Проблема'),
    ]

    nsis = [
        NSIs(nsi_name='ObjectType', nsi_rus_name='Тип объекта'),
        NSIs(nsi_name='MISType', nsi_rus_name='Тип МИС'),
        NSIs(nsi_name='InfoSystem', nsi_rus_name='Информационные системы'),
        NSIs(nsi_name='Modules', nsi_rus_name='Модули'),
        NSIs(nsi_name='SMS', nsi_rus_name='СЭМД/СМС'),
        NSIs(nsi_name='Status', nsi_rus_name='Статусы'),
    ]


    db.session.bulk_save_objects(obj_type)
    db.session.bulk_save_objects(mis_type)
    db.session.bulk_save_objects(info_sys)
    db.session.bulk_save_objects(modules)
    db.session.bulk_save_objects(sms)
    db.session.bulk_save_objects(status)
    db.session.bulk_save_objects(nsis)

    db.session.commit()

create_nsi()
