from flask import Flask, render_template, request
import os

app = Flask(__name__)

# トップ画面（アクセスしたときに最初に表示されるページ）
@app.route('/')
def index():
    return render_template('index.html')

# フォームが送信されたときの処理
@app.route('/greet', methods=['POST'])
def greet():
    # HTMLのinputタグの「name="username"」から値を取得
    user_name = request.form.get('username')
    
    # 名前が空っぽだった場合のデフォルト値
    if not user_name:
        user_name = "ゲスト"
        
    # 結果画面（result.html）に名前のデータを渡して表示
    return render_template('result.html', name=user_name)

if __name__ == '__main__':
    # Render環境のポート番号を取得、なければ5000番を使う
    port = int(os.environ.get('PORT', 5000))
    # host='0.0.0.0' にすることで、外部からのアクセスを受け付けます
    app.run(host='0.0.0.0', port=port)