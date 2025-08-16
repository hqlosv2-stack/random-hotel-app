import random
import json
from flask import Flask, render_template, request, redirect, url_for, flash

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)
# フラッシュメッセージを使うために、シークレットキーを設定
app.secret_key = 'your_secret_key'  # 任意の文字列に置き換えてください

# ホテルのデータをJSONファイルから読み込む
# with open(...) as f:を使うと、ファイルが自動で閉じられる
try:
    with open('data/hotels.json', 'r', encoding='utf-8') as f:
        hotels = json.load(f)
except FileNotFoundError:
    hotels = [] # ファイルが見つからない場合は空のリストにする

# ルートURL（/）にアクセスしたときの処理
@app.route('/', methods=['GET', 'POST'])
def home():
    # POSTリクエスト（フォーム送信）の場合
    if request.method == 'POST':
        try:
            location = request.form['location']
            capacity = int(request.form['capacity'])

            # 人数が0以下の場合にエラーを出す
            if capacity <= 0:
                flash('人数は1人以上で入力してください。')
                return redirect(url_for('home'))

            # 場所を小文字に変換して比較することで、大文字小文字の違いを吸収
            # 「in」演算子を使って、部分一致をチェック
            filtered_hotels = [
                hotel for hotel in hotels
                if location.lower() in hotel['location'].lower() and hotel['capacity'] >= capacity
            ]

            # 条件に合うホテルがあればランダムに1つ選ぶ
            if filtered_hotels:
                chosen_hotel = random.choice(filtered_hotels)
                return render_template('result.html', hotel=chosen_hotel)
            else:
                # ホテルが見つからない場合、エラーメッセージを格納してリダイレクト
                flash('条件に合うホテルが見つかりませんでした。')
                return redirect(url_for('home'))
        except ValueError:
            # 人数に数字以外の文字が入力された場合
            flash('人数は半角数字で入力してください。')
            return redirect(url_for('home'))

    # GETリクエストの場合、入力フォームを表示
    return render_template('index.html')

# アプリケーションを直接実行する場合
if __name__ == '__main__':
    app.run(debug=True)
