import os
import sqlite3

import requests
from flask import Blueprint, request, render_template
from flask_login import login_required, current_user
current_company = []
search = Blueprint('search', __name__)

@search.route('/')
@login_required
def index():
    if not request.args.get('q'):
        return render_template("index.html")
    data = requests.get("https://api.company-information.service.gov.uk/search/companies", auth=(os.getenv("API_KEY"),
                                                                                                 ""), params={
        "q": request.args.get("q"),
        "items_per_page": "50",
    })

    return render_template("results.html", data=data.json(), q=request.args.get("q"))
    # if not current_user:
    #     return redirect(url_for("login"))
    # else:
    #     return redirect(url_for("dashboard"))

@search.route('/company/<no>')
def get_company(no):
    data = requests.get(f"https://api.company-information.service.gov.uk/company/{no}", auth=(os.getenv("API_KEY"),
                                                                                              ""), params={
        "company_number": no
    })
    if len(current_company) == 1:
        current_company[0] = no
    else:
        current_company.append(no)
    con = sqlite3.connect("instance/database.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT company_no FROM Following WHERE user_id={current_user.id}")
    followed_companies = res.fetchall()
    res.close()
    followed_companies_dict = {}
    for f in followed_companies:
        comp_data = requests.get(f"https://api.company-information.service.gov.uk/company/{f[0]}",
                            auth=(os.getenv("API_KEY"),
                                  ""), params={
                "company_number": f[0]
            })
        followed_companies_dict[f[0]] = comp_data.json()['company_name']
    return render_template("company.html", data=data.json(), no=no, followers=followed_companies_dict)
