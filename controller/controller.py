from flask import Flask
from dto.repository import DB

app = Flask(__name__)
db = DB()

@app.route("/login")
def login(phone: str, password: str):
    user = db.find_user(phone)
    if user.password == password:
        pass


@app.route("/edit")
def edit_record(rec_id, time, comment):  # phone, full_name, ...
    # check admin session
    pass


@app.route("/delete")
def delete_record(id: int):
    pass


@app.route("/search")
def search_record(phone_number: str):
    pass


@app.route("/add")
def add_record():  # phone, full_name, ...
    pass


@app.route("/")
def get_all_dates():
    pass
