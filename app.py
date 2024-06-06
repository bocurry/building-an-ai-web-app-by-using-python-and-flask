from flask import Flask, redirect, url_for, request, render_template, session, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()  # take environment variables from .env.
os.environ['http_proxy'] = "http://localhost:7890"
client = OpenAI(
    # api_key =os.environ.get("OPENAI_API_KEY"),
    api_key = 'sk-1TX8AEx5RsmDF9vpoN19jYZ394drHS7ecgI1npSoWycsLjxK',
    base_url = "https://api.moonshot.cn/v1",
)

# 初始化对话历史
conversation_history = [
    {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"}
]

app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history
    data = request.get_json()
    user_message = data.get("message")
    # 更新对话历史
    conversation_history.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=conversation_history,
        max_tokens=150,
        temperature = 0.3,
    )
    result = response.choices[0].message.content
    print(result)
    conversation_history.append({"role": "assistant", "content": result})
    # 将整个响应返回给客户端
    response_dict = response.to_dict()
    return jsonify(response_dict)

if __name__ == '__main__':
    app.run(debug=True)