import persistentvals
p = persistentvals.PersistentVals('./test.dat')
from flask import Flask, request, render_template_string, redirect, url_for

p.app = Flask(__name__)

# 名前を保存するリスト
p.names = []

# HTML テンプレートを文字列として定義
p.HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>名前リスト</title>
</head>
<body>
    <h1>名前リスト</h1>
    <form method="post">
        <label for="name">名前を入力してください:</label>
        <input type="text" id="name" name="name" required>
        <button type="submit">追加</button>
    </form>
    <h2>リストの内容:</h2>
    <ul>
        {% for name in names %}
            <li>{{ name }}</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # フォームから名前を取得してリストに追加
        name = request.form.get("name")
        if name:
            names.append(name)
        return redirect(url_for("index"))
    return render_template_string(HTML_TEMPLATE, names=names)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
