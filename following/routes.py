import sqlite3

from flask import Blueprint, redirect, url_for
from flask_login import current_user, login_required

from init_db import db
from model.Models import Following
from search.routes import current_company

following = Blueprint('following', __name__)


@following.route('/follow', methods=['GET', 'POST'])
@login_required
def follow():
    if len(current_company) == 0:
        return redirect(url_for('dashboard'))
    else:
        new_follow = Following(company_no=current_company[0], user_id=current_user.id)
        db.session.add(new_follow)
        db.session.commit()
        current_company.clear()
        return redirect(url_for('dashboard'))


@following.route('/unfollow', methods=['GET', 'POST'])
@login_required
def unfollow():
    if len(current_company) == 0:
        return redirect(url_for('dashboard'))
    else:
        con = sqlite3.connect("instance/database.db")
        cur = con.cursor()
        print(f"current user id: {current_user.id} company id to delete: {current_company[0]}")
        cur.execute("DELETE FROM Following WHERE company_no=? AND user_id=?", (current_company[0], current_user.id))
        con.commit()
        print("??")
        current_company.clear()
        return redirect(url_for('dashboard'))
