from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = "你的密鑰"  # flash 功能需要設定密鑰

GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbwFDfnP9DaLJCtoCLaBiUGPeHuiQkcToFlKaZXhqIsr_qNcSvl8pyhw3uAJwkAnK83p/exec"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    # 這裡可以擴充為搜尋資料庫或其他資料來源
    return f"你搜尋了：{keyword}"

@app.route("/report", methods=["POST"])
def report():
    message = request.form.get("message")

    # 儲存到本地 logs.txt
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(message + "\n---\n")

    # 傳送到 Google Sheet
    if message:
        try:
            requests.post(GOOGLE_SHEET_URL, data={"message": message})
        except Exception as e:
            print("傳送到 Google Sheet 時出錯：", e)

    flash("問題已回報，感謝您！")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
