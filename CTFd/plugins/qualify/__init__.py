from CTFd.models import db
from CTFd.utils.decorators import authed_only,get_current_user
from CTFd.utils import config
from CTFd.utils.config.visibility import scores_visible
from CTFd.utils.decorators.visibility import (
    check_account_visibility,
    check_score_visibility,
)
from CTFd.utils.helpers import get_infos
from CTFd.utils.scores import get_standings
from CTFd.utils.user import is_admin
from CTFd.constants import JinjaEnum, RawEnum
from CTFd.forms import Forms,BaseForm
from CTFd.forms.fields import SubmitField
from wtforms import StringField

from flask import request,render_template
from flask_babel import lazy_gettext as _l
import random
import string
import os

@JinjaEnum
class ScoreboardCache(str, RawEnum):
    Qualified_SCOREBOARD_TABLE = "qualified_scoreboard_table"

class QualifyForm(BaseForm):
    code = StringField(_l("Qualify Code"))
    submit = SubmitField(_l("Submit"))


class QualifyUsers(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(128), unique = True)
    code = db.Column(db.String(32))
    qualified = db.Column(db.Boolean, default = False)

    def __init__(self, email):
        self.email = email
        self.code = ''.join(random.choice(string.ascii_letters) for _ in range(32))

def init_code():
    if not os.path.exists('./emails.txt'):
        return
    f = open('./emails.txt','r').read()
    emails = f.split('\n')
    for email in emails:
        try:
            QualifyUsers.query.filter_by(email=email).one()
        except:
            db.session.add(QualifyUsers(email))
    db.session.commit()


def load(app):
    app.db.create_all()
    Forms.self.QualifyForm = QualifyForm
    init_code()
    
    @authed_only
    @app.route('/user/qualify',methods=['POST'])
    def qualify_user():
        code = request.json['code']
        if code == None or code == '':
            return {"success": False, "errors": ["Your qualification code is empty."]}
        user = get_current_user()
        q_user = QualifyUsers.query.filter_by(email = user.email).first()
        if q_user.qualified:
            return {"success": False, "errors": ["You have already qualified."]}
        if code == q_user.code:
            setattr(q_user, 'qualified', True)
            db.session.commit()
            return {"success": True}
        return {"success": False, "errors": ["Qualification failed."]}
    
    @check_account_visibility
    @check_score_visibility
    @app.route("/qualified_scoreboard")
    def listing():
        infos = get_infos()

        if config.is_scoreboard_frozen():
            infos.append("Scoreboard has been frozen")

        if is_admin() is True and scores_visible() is False:
            infos.append("Scores are not currently visible to users")

        standings = get_standings(qualify=True)
        return render_template("qualified_scoreboard.html", standings=standings, infos=infos)

