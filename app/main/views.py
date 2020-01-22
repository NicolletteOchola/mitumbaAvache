from flask import render_template, request, Blueprint
from app.models import Post
from app.request import get_quote

main = Blueprint('main', __name__)