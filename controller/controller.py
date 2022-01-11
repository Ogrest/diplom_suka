from flask import Flask, app

app - Flask(__name__)


#должен быть тонким

@app.route("/login")
def login(login: str, password: str):
    pass

@app.route("/edit")
def edit_record(id: int): #phone, full_name, ...
    #check admin session
    pass

@app.route("/delete")
def delete_record(id: int):
    pass

@app.route("/search")
def search_record(phone_number: str):
    pass

@app.route("/add")
def add_record(): #phone, full_name, ...
    pass

@app.route("/")
def get_all_dates():
    pass
