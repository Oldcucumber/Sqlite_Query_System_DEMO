from flask import Flask, send_from_directory
import webbrowser
import os

app = Flask(__name__)

# 为 main.js, style.css, 和 back.gif 创建路由


@app.route('/main.js')
def serve_js():
    return send_from_directory(os.getcwd(), 'main.js')


@app.route('/style.css')
def serve_css():
    return send_from_directory(os.getcwd(), 'style.css')


@app.route('/back.gif')
def serve_gif():
    return send_from_directory(os.getcwd(), 'back.gif')


@app.route('/')
def serve_index_page():
    return send_from_directory(os.getcwd(), 'index.html')


if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8000')
    app.run(host='0.0.0.0', port=8000)
