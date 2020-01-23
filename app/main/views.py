from flask import render_template, request, Blueprint
from app.models import Post

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.posted_date.desc()).paginate(page=page, per_page=7)
    # categories = Post.query.filter_by(category=post.category).all()
    myposts = Post.query.order_by(Post.posted_date.desc())
    return render_template('index.html', posts=posts, myposts=myposts)


@main.route("/about")
def about():
    myposts = Post.query.order_by(Post.posted_date.desc())
    return render_template('about.html', title='About', myposts=myposts)


@main.route("/subscribe")
def subscribe():
    return render_template('subscribe.html', title='Subscription')