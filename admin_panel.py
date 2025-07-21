from flask import Flask, request, render_template_string, redirect, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
TOKEN = '7257032872:AAGrW1dPt1T-Rh3BhDX3Xvtk0_fK3OXHrNo'  # Замените на свой токен
ANNOUNCE_FILE = 'announcements.json'

HTML = '''
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Админ-панель мероприятий</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; }
    h1 { color: #333; }
    form { margin-bottom: 30px; }
    textarea { width: 100%; height: 80px; }
    button { padding: 10px 20px; background: #007bff; color: #fff; border: none; border-radius: 4px; cursor: pointer; }
    .announcements { margin-top: 30px; }
    .announcement { background: #f8f9fa; padding: 10px; margin-bottom: 10px; border-radius: 4px; }
    .date { color: #888; font-size: 0.9em; }
  </style>
</head>
<body>
  <h1>Админ-панель мероприятий</h1>
  <form method="POST" action="/add">
    <label for="announcement">Текст анонса:</label><br>
    <textarea name="announcement" id="announcement" required></textarea><br>
    <button type="submit">Добавить анонс</button>
  </form>
  <div class="announcements">
    <h2>Список анонсов</h2>
    {% if announcements %}
      {% for a in announcements %}
        <div class="announcement">
          <div>{{ a['text'] }}</div>
          <div class="date">{{ a['date'] }}</div>
        </div>
      {% endfor %}
    {% else %}
      <i>Анонсов нет</i>
    {% endif %}
  </div>
</body>
</html>
'''

def load_announcements():
    if os.path.exists(ANNOUNCE_FILE):
        with open(ANNOUNCE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_announcements(announcements):
    with open(ANNOUNCE_FILE, 'w', encoding='utf-8') as f:
        json.dump(announcements, f, ensure_ascii=False, indent=2)

@app.route('/', methods=['GET'])
def index():
    announcements = load_announcements()
    return render_template_string(HTML, announcements=announcements)

@app.route('/add', methods=['POST'])
def add_announcement():
    text = request.form.get('announcement')
    if not text:
        return 'Нет текста анонса', 400
    announcements = load_announcements()
    announcements.append({'text': text, 'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    save_announcements(announcements)
    return redirect('/')

@app.route('/api/announcements', methods=['GET'])
def get_announcements():
    token = request.args.get('token')
    if token != TOKEN:
        return jsonify({'error': 'Forbidden'}), 403
    announcements = load_announcements()
    return jsonify(announcements)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
