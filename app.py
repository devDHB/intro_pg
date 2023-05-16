from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://sparta:test@cluster0.snrvzql.mongodb.net/?retryWrites=true&w=majority"
)
db = client.dbsparta

# import requests
# from bs4 import BeautifulSoup


@app.route("/")
def home():
    return render_template("index.html")

# 루트 추가
@app.route("/테스트")
def test():
    return render_template("test.html")


@app.route("/member", methods=["POST"])
def member_post():
    # 멤버 정보 받기
    url_receive = request.form["url_give"]
    name_receive = request.form["name_give"]
    age_receive = request.form["age_give"]
    mbti_receive = request.form["mbti_give"]
    comment_receive = request.form["comment_give"]
    intro_receive = request.form["intro_give"]

    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
    # }
    # data = requests.get(url_receive, headers=headers)
    # soup = BeautifulSoup(data.text, "html.parser")

    # ogtitle = soup.select_one("meta[property='og:title']")["content"]
    # ogimage = soup.select_one("meta[property='og:image']")["content"]
    # ogdesc = soup.select_one("meta[property='og:description']")["content"]

    doc = {
        # "title": ogtitle,
        # "desc": ogdesc,
        # "image": ogimage,
        "url" : url_receive,
        "name": name_receive,
        "age":age_receive,
        "mbti":mbti_receive,
        "comment": comment_receive,
        "intro" : intro_receive,
    }
    db.members.insert_one(doc)

    return jsonify({"msg": "저장 완료!"})


@app.route("/member", methods=["GET"])
def member_get():
    all_members = list(db.members.find({}, {"_id": False}))
    return jsonify({"result": all_members})

# 삭제 기능 추가
@app.route("/delete_member", methods=["POST"])
def delete_member():
    delete_name_receive = request.form["delete_name_give"]
    db.members.delete_one({"name": delete_name_receive})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
