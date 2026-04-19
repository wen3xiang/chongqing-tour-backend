# app.py
from flask import Flask
from flask_cors import CORS
from API import bp as api_bp
import jieba
def tokenizer_func(text):
    """分词函数 - 用于加载vectorizer.pkl"""
    return jieba.lcut(text)
app = Flask(__name__)
CORS(app)

app.register_blueprint(api_bp)

@app.route('/')
def index():
    return {'message': '景区智慧治理系统 API'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
