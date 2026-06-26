from flask import Flask, render_template, request

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
    # debug=True にすると、コードを変更したときに自動でアプリが再起動して便利です
    app.run(debug=True)