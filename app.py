from flask import Flask, render_template
from flask_login import LoginManager, login_required, current_user
from dotenv import load_dotenv
from init_db import db
from model.Models import User
from init_bycrypt import bcrypt
from authentication.routes import authentication
from following.routes import following
from search.routes import search
import sqlite3
import os
import requests


load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
db.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(authentication)
app.register_blueprint(following)
app.register_blueprint(search)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    con = sqlite3.connect("instance/database.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT company_no FROM Following WHERE user_id={current_user.id}")
    followed_companies = res.fetchall()
    res.close()
    followed_companies_dict = {}
    for f in followed_companies:
        data = requests.get(f"https://api.company-information.service.gov.uk/company/{f[0]}", auth=(os.getenv("API_KEY"),
                                                                                                 ""), params={
            "company_number": f[0]
        })
        followed_companies_dict[f[0]] = data.json()['company_name']

    print(followed_companies_dict)
    return render_template('dashboard.html', user=current_user, followers=followed_companies_dict)


if __name__ == '__main__':
    app.run()

