# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from random import choice, randint
from app import db, Data  # 导入 Data 模型
import os

app = Flask(__name__)
current_directory = os.getcwd()


app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(current_directory, "instance", "site.db")}'
db = SQLAlchemy(app)


def generate_license_plate():
    provinces = "京津晋冀蒙辽吉黑沪苏浙皖闽赣鲁豫鄂湘粤桂琼渝川贵云藏陕甘青宁新"
    authorities = "ABCDEFGHJKLMNPQRSTUVWXY"
    characters = "ABCDEFGHJKLMNPQRSTUVWXYZ0123456789"

    return choice(provinces) + choice(authorities) + ''.join(choice(characters) for _ in range(5))

def generate_owner_name():
    from faker import Faker
    fake = Faker("zh_CN")
    return fake.name()

def generate_phone_number():
    return '1' + ''.join(str(randint(0, 9)) for _ in range(10))


def generate_data():
    for _ in range(10000000):  # 生成1000条数据
            id = generate_license_plate()
            owner = generate_owner_name()
            phone_number = generate_phone_number()
            # 创建一个新的 Data 对象并添加到数据库
            new_data = Data(id=id, owner=owner, phone_number=phone_number)
            db.session.add(new_data)
            db.session.commit()
    return "1000条测试数据已生成并添加到数据库。"

if __name__ == '__main__':
    with app.app_context():
        generate_data()
