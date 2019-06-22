from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flaskblog import db
from flaskblog.posts.forms import PostForm
from flaskblog.models import Post, PostLike, Cat
from flaskblog.posts.utils import save_picture
from flask_login import current_user, login_required
from sqlalchemy import func, desc
import bleach

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        attrs = {
            'img': ['src', 'alt', 'title', 'style'],
            'p': ['style'],
            'h1': ['style']
        }
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            clean_content = bleach.clean(request.form.get('content'),
                                         tags=bleach.sanitizer.ALLOWED_TAGS + ['h1', 'br', 'p', 'img', 'blockquote'],
                                         attributes=attrs,
                                         protocols=bleach.sanitizer.ALLOWED_PROTOCOLS + ['data'],
                                         styles=bleach.sanitizer.ALLOWED_STYLES + ['color', 'width', 'text-align'])
            post = Post(title=form.title.data, content=clean_content,
                        author=current_user,
                        cat_id=form.category.data.id, image_file=picture_file)
        else:
            post = Post(title=form.title.data,
                        content=bleach.clean(form.content.data,
                                             tags=bleach.sanitizer.ALLOWED_TAGS + ['h1', 'br', 'p', 'img', 'blockquote'],
                                             attributes=attrs,
                                             protocols=bleach.sanitizer.ALLOWED_PROTOCOLS + ['data'],
                                             styles=bleach.sanitizer.ALLOWED_STYLES + ['color', 'width', 'text-align']),
                        author=current_user,
                        cat_id=form.category.data.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.cat_id = form.category.data.id
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        # form.category.default = post.categ.title
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    return redirect(url_for('main.home'))


@posts.route('/post/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)


@posts.route('/categories')
def categories():
    cat = Cat.query.order_by(Cat.title)
    return render_template('categories.html', cat=cat)


@posts.route('/categories/<string:category_title>/<int:category_id>')
def selected_category(category_title, category_id):
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(cat_id=category_id).order_by(Post.date_posted.desc()).paginate(page=page, per_page=20)
    if posts.has_next:
        next_page = page + 1
    else:
        next_page = None
    if posts.has_prev:
        prev_page = page - 1
    else:
        prev_page = None
    cat = Cat.query.order_by(Cat.title).limit(10)
    featured_id = db.session.query(PostLike.post_id,
                                   func.count(PostLike.id).label('qty')
                                   ).group_by(PostLike.post_id
                                              ).order_by(desc('qty')).limit(3)
    featured_posts = db.session.query(Post).filter(Post.id.in_(x for x, _ in featured_id)).all()
    projects = Post.query.filter_by(user_id=1).filter_by(cat_id=1).order_by(Post.date_posted.desc()).limit(2)
    return render_template('blogs_category.html', posts=posts, category_title=category_title, category_id=category_id,
                           featured=featured_posts, cat=cat, projects=projects,
                           next_page=next_page, prev_page=prev_page)


