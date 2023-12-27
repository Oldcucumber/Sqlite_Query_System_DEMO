from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import base64
from flask_cors import CORS
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from sqlalchemy import text


print(os.getcwd())

# 读取同目录的private_key.pem文件，获取私钥
with open("private_key.pem", "rb") as f:
    private_key = RSA.importKey(f.read())


app = Flask(__name__)

# 获取当前工作目录
current_directory = os.getcwd()

# 设置数据库URI，使用相对路径
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(current_directory, "instance", "site.db")}'
db = SQLAlchemy(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# 用户名、密码和密文的映射表
class User(db.Model):
    username = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# 数据查询表


class Data(db.Model):
    id = db.Column(db.String(7), primary_key=True, unique=True)
    owner = db.Column(db.String(5), nullable=False)
    phone_number = db.Column(db.String(11), nullable=False)


with app.app_context():
    db.create_all()


def decrypt_data(encrypt_msg):
    print (type(private_key))
    cipher = PKCS1_cipher.new(private_key)
    back_text = cipher.decrypt(base64.b64decode(encrypt_msg), 0)
    return back_text.decode('utf-8')

def perform_query(search_query):
    query = text("""
        SELECT id, owner, phone_number 
        FROM QueryData 
        WHERE id LIKE :search_query 
        OR owner LIKE :search_query 
        OR phone_number LIKE :search_query
    """)
    query_result = db.session.execute(query, [{"search_query": f'%{search_query}%'}]).fetchall()
    return [{'id': row['id'], 'owner': row['owner'], 'phone_number': row['phone_number']} for row in query_result]


@app.route('/api/query', methods=['POST'])
def query():
    try:
        # 获取用户名和加密后的请求数据
        username = request.json.get('username')
        password = request.json.get('password')
        encrypted_data = request.json.get('encrypted_data')

        # 查找用户名对应的用户
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': '用户不存在', 'errorCode': 'user_not_found'})

        # 验证密码
        decrypted_password = decrypt_data(password)
        if decrypted_password != user.password:
            return jsonify({'error': '密码错误', 'errorCode': 'password_error'})

        # 解密查询数据
        decrypted_data = decrypt_data(encrypted_data)
        print(decrypted_data)

        # 查询数据中是否包含关键词
        results = Data.query.filter(
            (Data.id.like(f'%{decrypted_data}%')) |
            (Data.owner.like(f'%{decrypted_data}%')) |
            (Data.phone_number.like(f'%{decrypted_data}%'))
        ).all()
        
        if results:
            # 有查询结果
            data_list = [{'id': data.id, 'owner': data.owner, 'phone_number': data.phone_number} for data in results]
            return jsonify({'results': data_list})
        else:
            # 查询成功但无结果
            return jsonify({'error': '查询成功但没有找到结果', 'errorCode': 'no_results'})
    except Exception as e:
        # 异常处理
        return jsonify({'error': str(e), 'errorCode': 'exception'})

if __name__ == '__main__':
    app.run(debug=True)