import os
from flask import render_template, request, Blueprint, flash, url_for, redirect
from datetime import datetime, timedelta
from sqlalchemy import func, desc
from flaskblog import db
from flaskblog.models import User, Post, PostLike, Cat
from flaskblog.users.forms import ContactForm
from flaskblog.users.utils import send_contact_email

main = Blueprint('main', __name__)

HOME_USER = os.environ.get('HOME_USER')


@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home_page():
    form = ContactForm()
    if form.validate_on_submit():
        email = form.email.data
        subject = form.subject.data
        message = form.message.data
        send_contact_email(email, subject, message)
        flash('Thank you for your interest! I will get back to you as soon as possible.', 'info')
        return redirect(url_for('main.home_page'))
    projects = Post.query.filter_by(user_id=1).filter_by(cat_id=1).order_by(Post.date_posted.desc())
    return render_template('home_page.html', form=form, projects=projects)


@main.route('/blog')
def home():
    page = request.args.get('page', 1, type=int)
    home_posts = User.query.filter_by(email=HOME_USER).first_or_404()
    home_id = home_posts.id
    # posts = Post.query.filter_by(user_id=home_id).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=20)
    if posts.has_next:
        next_page = page + 1
    else:
        next_page = None
    if posts.has_prev:
        prev_page = page - 1
    else:
        prev_page = None
    latest_posts = Post.query.order_by(Post.date_posted.desc()).limit(3)
    # projects = Post.query.filter_by(user_id=home_id).order_by(Post.date_posted.desc()).limit(3)
    featured_id = db.session.query(PostLike.post_id,
                                   func.count(PostLike.id).label('qty')
                                   ).group_by(PostLike.post_id
                                              ).order_by(desc('qty')).limit(3)
    featured_posts = db.session.query(Post).filter(Post.id.in_(x for x, _ in featured_id)).all()
    date_filter = datetime.utcnow() - timedelta(days=14)
    popular = db.session.query(Post.cat_id,
                               func.count(Post.id).label('qty')
                               ).filter(Post.date_posted > date_filter
                                        ).group_by(Post.cat_id
                                                   ).order_by(desc('qty')).limit(10)
    popular_categories = db.session.query(Cat).filter(Cat.id.in_(x for x, _ in popular)).all()
    cat = Cat.query.order_by(Cat.title).limit(10)
    projects = Post.query.filter_by(user_id=1).filter_by(cat_id=1).order_by(Post.date_posted.desc()).limit(2)
    return render_template('home.html',
                           posts=posts,
                           latest_posts=latest_posts,
                           projects=projects,
                           featured=featured_posts,
                           popular_categories=popular_categories,
                           cat=cat,
                           next_page=next_page,
                           prev_page=prev_page)


@main.route('/blog/recent')
def blogs():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('blogs.html', posts=posts)


@main.route('/about')
def about():
    featured_id = db.session.query(PostLike.post_id,
                                   func.count(PostLike.id).label('qty')
                                   ).group_by(PostLike.post_id
                                              ).order_by(desc('qty')).limit(3)
    featured_posts = db.session.query(Post).filter(Post.id.in_(x for x, _ in featured_id)).all()
    cat = Cat.query.order_by(Cat.title).limit(10)
    projects = Post.query.filter_by(user_id=1).filter_by(cat_id=1).order_by(Post.date_posted.desc()).limit(2)
    return render_template('about.html', title='About', featured=featured_posts, cat=cat, projects=projects)


@main.route('/help')
def help():
    featured_id = db.session.query(PostLike.post_id,
                                   func.count(PostLike.id).label('qty')
                                   ).group_by(PostLike.post_id
                                              ).order_by(desc('qty')).limit(3)
    featured_posts = db.session.query(Post).filter(Post.id.in_(x for x, _ in featured_id)).all()
    cat = Cat.query.order_by(Cat.title).limit(10)
    projects = Post.query.filter_by(user_id=1).filter_by(cat_id=1).order_by(Post.date_posted.desc()).limit(2)
    return render_template('help.html', title='Help', featured=featured_posts, cat=cat, projects=projects)


@main.route('/updates')
def updates():
    featured_id = db.session.query(PostLike.post_id,
                                   func.count(PostLike.id).label('qty')
                                   ).group_by(PostLike.post_id
                                              ).order_by(desc('qty')).limit(3)
    featured_posts = db.session.query(Post).filter(Post.id.in_(x for x, _ in featured_id)).all()
    cat = Cat.query.order_by(Cat.title).limit(10)
    projects = Post.query.filter_by(user_id=1).filter_by(cat_id=1).order_by(Post.date_posted.desc()).limit(2)
    return render_template('updates.html', title='Updates', featured=featured_posts, cat=cat, projects=projects)


@main.route('/privacy')
def privacy():
    featured_id = db.session.query(PostLike.post_id,
                                   func.count(PostLike.id).label('qty')
                                   ).group_by(PostLike.post_id
                                              ).order_by(desc('qty')).limit(3)
    featured_posts = db.session.query(Post).filter(Post.id.in_(x for x, _ in featured_id)).all()
    cat = Cat.query.order_by(Cat.title).limit(10)
    projects = Post.query.filter_by(user_id=1).filter_by(cat_id=1).order_by(Post.date_posted.desc()).limit(2)
    return render_template('privacy.html', title='Privacy', featured=featured_posts, cat=cat, projects=projects)


@main.route('/terms')
def terms():
    featured_id = db.session.query(PostLike.post_id,
                                   func.count(PostLike.id).label('qty')
                                   ).group_by(PostLike.post_id
                                              ).order_by(desc('qty')).limit(3)
    featured_posts = db.session.query(Post).filter(Post.id.in_(x for x, _ in featured_id)).all()
    cat = Cat.query.order_by(Cat.title).limit(10)
    projects = Post.query.filter_by(user_id=1).filter_by(cat_id=1).order_by(Post.date_posted.desc()).limit(2)
    return render_template('terms.html', title='Terms', featured=featured_posts, cat=cat, projects=projects)


# @main.route("/load")
# def load():
#     dbs = list()  # The mock database
#     items = Post.query.order_by(Post.date_posted.desc())
#     posts = Post.query.order_by(Post.date_posted.desc()).count()
#     quantity = 5  # num posts to return per request
#
#     for x in items:
#         dbs.append([x.date_posted.strftime('%Y-%m-%d'), x.categ.title, x.title, x.content, x.author.username])
#
#     time.sleep(0.2)  # Used to simulate delay
#
#     if request.args:
#         counter = int(request.args.get("c"))  # The 'counter' value sent in the QS
#
#         if counter == 0:
#             print(f"Returning posts 0 to {quantity}")
#             # Slice 0 -> quantity from the db
#             res = make_response(jsonify(dbs[0: quantity]), 200)
#
#         elif counter == posts:
#             print("No more posts")
#             res = make_response(jsonify({}), 200)
#
#         else:
#             print(f"Returning posts {counter} to {counter + quantity}")
#             # Slice counter -> quantity from the db
#             res = make_response(jsonify(dbs[counter: counter + quantity]), 200)
#
#     return res


# @main.route('/background_process')
# def background_process():
#     try:
#         lang = request.args.get('like', 0, type=int)
#         return jsonify(result=lang + 1)
#
#         # if lang.lower() == 'python':
#         #     return jsonify(result='You are wise')
#         # else:
#         #     return jsonify(result='Try again.')
#     except Exception as e:
#         return str(e)


# @main.route('/_search_results', methods=['GET', 'POST'])
# def search_results():
#     page = request.args.get('page', 1, type=int)
#     posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=8)
