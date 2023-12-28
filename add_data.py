# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db, Data  # 导入 Data 模型

app = Flask(__name__)
current_directory = os.getcwd()

# 设置数据库URI，使用相对路径
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(current_directory, "instance", "site.db")}'
db = SQLAlchemy(app)

if __name__ == '__main__':
    with app.app_context():
        action = input("请选择操作 (add/edit): ")

        if action == "add":
            # 提示用户输入数据
            id = input("请输入牌号: ")
            owner = input("请输入所有者: ")
            phone_number = input("请输入电话号码: ")

            # 创建一个新的 Data 对象并添加到数据库
            new_data = Data(id=id, owner=owner, phone_number=phone_number)
            db.session.add(new_data)
            db.session.commit()

            print("数据已成功添加到数据库。")
        elif action == "edit":
            id = input("请输入要编辑的数据ID: ")
            data = Data.query.get(id)

            if not data:
                print(f"未找到 ID 为 {id} 的数据。")
            else:
                new_owner = input(f"新的所有者 (当前所有者为 {data.owner}): ")
                new_phone_number = input(
                    f"新的电话号码 (当前电话号码为 {data.phone_number}): ")

                # 更新数据
                data.owner = new_owner
                data.phone_number = new_phone_number
                db.session.commit()

                print(f"数据 ID {id} 已成功更新。")
        else:
            print("无效的操作。请选择 'add' 或 'edit'。")
