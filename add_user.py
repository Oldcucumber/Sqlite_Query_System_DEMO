# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db, User
import os

app = Flask(__name__)
current_directory = os.getcwd()

# 设置数据库URI，使用相对路径
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(current_directory, "instance", "site.db")}'
db = SQLAlchemy(app)

if __name__ == '__main__':
    with app.app_context():
        # 提示用户输入用户名和密码
        username = input("请输入用户名: ")
        password = input("请输入密码: ")

        # 创建一个新的User对象并添加到数据库
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        print("用户已成功添加到数据库。")

