# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from random import choice, randint
from app import db, Data  # 导入 Data 模型

app = Flask(__name__)
current_directory = os.getcwd()


app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(current_directory, "instance", "site.db")}'
db = SQLAlchemy(app)

#随机生成牌号
def generate_license_plate():
    provinces = "京津晋冀蒙辽吉黑沪苏浙皖闽赣鲁豫鄂湘粤桂琼渝川贵云藏陕甘青宁新"
    authorities = "ABCDEFGHJKLMNPQRSTUVWXY"
    characters = "ABCDEFGHJKLMNPQRSTUVWXYZ0123456789"

    return choice(provinces) + choice(authorities) + ''.join(choice(characters) for _ in range(5))

#随机生成姓名
def generate_owner_name():
    from faker import Faker
    fake = Faker("zh_CN")
    return fake.name()

#随机生成电话号码
def generate_phone_number():
    return '1' + ''.join(str(randint(0, 9)) for _ in range(10))

#循环并且写入
def generate_data():
    for index, _ in enumerate(range(9999999), 1):  # 生成n条数据，enumerate从1开始计数
        id = generate_license_plate()
        owner = generate_owner_name()
        phone_number = generate_phone_number()
        # 创建一个新的 Data 对象并添加到数据库
        new_data = Data(id=id, owner=owner, phone_number=phone_number)
        db.session.add(new_data)
        db.session.commit()
        print(f"第{index}条测试数据已生成并添加到数据库。")  # 打印当前条目数
    return "1000条测试数据已生成并添加到数据库。"


if __name__ == '__main__':
    with app.app_context():
        generate_data()
