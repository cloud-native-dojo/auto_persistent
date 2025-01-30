from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# 名前を保存するリスト
names = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # フォームから名前を取得してリストに追加
        name = request.form.get("name")
        if name:
            names.append(name)
        return redirect(url_for("index"))
    return render_template("index.html", names=names)

@app.route("/running", methods=["GET", "POST"])
def running():
    return render_template("running.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

