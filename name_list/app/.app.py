from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# 名前を保存するリスト
names = []

# HTML テンプレートを文字列として定義
HTML_TEMPLATE = """
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

# HTML テンプレートを文字列として定義
HTML_TEMPLATE2 = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>running</title>
    <style>
        /* CSS部分 */
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            text-align: center;
        }

        progress {
            width: 80%;
            height: 20%;
            appearance: none;
            border: 1px solid #ccc;
            border-radius: 5px;
            background-color: #f3f3f3;
        }

        progress::-webkit-progress-bar {
            background-color: #f3f3f3;
        }

        progress::-webkit-progress-value {
            background-color: #4caf50;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>ダウンロード中...</h1>
    <progress id="downloadProgress" value="0" max="100"></progress>
    <script>
        // JavaScript部分
        document.addEventListener('DOMContentLoaded', () => {
            const progressBar = document.getElementById('downloadProgress');
            let downloadValue = 0;

            // ダウンロードのシミュレーション
            const downloadInterval = setInterval(() => {
                if (downloadValue < 100) {
                    downloadValue += 1; // 進行状況を更新
                    progressBar.value = downloadValue;
                } else {
                    clearInterval(downloadInterval); // ダウンロード完了
                    alert('ダウンロード完了');
                }
            }, 100); // 100msごとに進行状況を1%増加
        });
    </script>
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


@app.route("/running", methods=["GET", "POST"])
def running():
    return render_template_string(HTML_TEMPLATE2)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
