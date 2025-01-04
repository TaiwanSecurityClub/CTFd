import os

from flask import render_template
from flask_babel import lazy_gettext as _l
from wtforms import StringField

from CTFd.constants import JinjaEnum, RawEnum
from CTFd.forms import BaseForm, Forms
from CTFd.forms.fields import SubmitField
from CTFd.models import db
from CTFd.utils import config
from CTFd.utils.config.visibility import scores_visible
from CTFd.utils.decorators.visibility import (
    check_account_visibility,
    check_score_visibility,
)
from CTFd.utils.helpers import get_infos
from CTFd.utils.scores import get_standings
from CTFd.utils.user import is_admin


def load(app):
    @app.route("/")
    def index():
        return render_template(
            "index.html"
        )
