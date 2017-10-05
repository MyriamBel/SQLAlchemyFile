#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlalchemy.orm

engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=True)  # Создаем подключение к БД

metadata = sqlalchemy.MetaData()  # Задаем метаданные таблицы

users_table = sqlalchemy.Table('users', metadata,  # Создаем таблицу юзерс_тэбл с метаданными и заданными столбцами
                                   sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                                   sqlalchemy.Column('name', sqlalchemy.String),
                                   sqlalchemy.Column('fullname', sqlalchemy.String),
                                   sqlalchemy.Column('password', sqlalchemy.String)
                                   )

metadata.create_all(engine)

class User(object):  # Создаем пользователя с атрибутами, как в таблице
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<User ('%s','%s','%s')>" % (self.name, self.fullname, self.password)

print(sqlalchemy.orm.mapper(User, users_table))

def createSession():
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker()
    Session.configure(bind = engine)
    session = Session()
    return session

def exit():
    quit()

def pass_treb(passw):  # функция проверки соответствия пароля требованиям
    if len(passw) > 8:
        import string
        upper = 0
        lower = 0
        punct = 0
        digit = 0
        for i in passw:
            if i in string.ascii_lowercase:
                lower += 1
            if i in string.ascii_uppercase:
                upper += 1
            if i in string.punctuation:
                punct += 1
            if i in string.digits:
                digit += 1
        if upper > 0 and lower > 0 and punct > 0 and digit > 0:
            return 0
        else:
            return 1  # Пароль не соотв. требованиям - не хватает определенных символов
    else:
        return 2  # Пароль не соотв. требованиям - слишком короткий

def add(name, fullname, passw):
    sess = createSession()
    anyUser = User(name, fullname, passw)
    sess.add(anyUser)
    sess.commit()
    return 0

def inf_user(name, passw):
    sess = createSession()
    res = sess.query(User).filter_by(name=name).first()
    if res == None:
        return 2  # Пользователь не найден
    elif passw == res.password:
        return res.name + res.fullname
    elif passw != res.password:
        return 1  # Пароли не совпали

def remove(name, passw):
    sess = createSession()
    res = sess.query(User).filter_by(name=name).first()
    if res == None:
        return 2  # Пользователь не найден
    elif passw == res.password:
        sess.delete(res)
        sess.commit()
        return 0
    elif passw != res.password:
        return 1  # Пароли не совпали

def change(name, passw, newpassw):
    sess = createSession()
    res = sess.query(User).filter_by(name=name).first()
    if res == None:
        return 2  # Пользователь не найден
    elif res.password == passw:
        res.password = newpassw
        sess.commit()
        return 0
    elif res.password != passw:
        return 1  # Пароли не совпали

while True:
    print('Будем работать с БД?')
    j = input()
    if j == 'y' or j == 'Y':

        while True:
            i = input('Добавить нового пользователя?')
            if i == 'Y' or i == 'y':
                c = ''
                a = input('Введите имя')
                b = input('Введите полное имя')
                while pass_treb(c) != 0:
                    c = input(
                        'Введите пароль, длина более 8 символов, латинские буквы, 1 прописная, 1 строчная, 1 знак препинания, 1 цифра')
                add(a, b, c)
            else:
                break

        while True:
            i = input('Вывести информацию о пользователе?')
            if i == 'y' or i == 'Y':
                a = input('Введите имя')
                b = input('Введите пароль')
                if inf_user(a, b) == 1:
                    print('Неверный пароль')
                elif inf_user(a, b) == 2:
                    print('Пользователь не найден')
                else:
                    print(inf_user(a, b))
            else:
                break

        while True:
            i = input('Будем менять пароли?')
            if i == 'y' or i == 'Y':
                a = input('Введите имя')
                b = input('Введите старый пароль')
                c = ''
                d = ' '
                while c != d:
                    while pass_treb(c) != 0:
                        c = input(
                            'Введите пароль, длина более 8 символов, латинские буквы, 1 прописная, 1 строчная, 1 цифра')
                    d = input('Повторите новый пароль')
                if change(a, b, c) == 1:
                    print('Вы ввели неверный старый пароль')
                elif change(a, b, c) == 2:
                    print('Пользователь не найден')
                else:
                    change(a, b, c)
                    print('Пароль изменен')
            else:
                break

        while True:
            i = input('Будем удалять пользователей?')
            if i == 'y' or i == 'Y':
                a = input('Введите имя')
                b = input('Введите пароль')
                if remove(a, b) == 1:
                    print('Неверный пароль')
                elif remove(a, b) == 2:
                    print('Пользователь не найден')
                else:
                    remove(a, b)
                    print('Пользователь %s удален' % (a))
            else:
                break

        print('Желаете завершить работу?')
        i = input()
        if i == 'y' or i == 'Y':
            exit()

    else:
        exit()