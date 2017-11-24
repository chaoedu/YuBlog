from flask import render_template, redirect, url_for, request, current_app

from .. import db
from . import main
from .forms import *
from ..models import *


@main.route('/')
@main.route('/index')
def index():
    page = request.args.get('page', 1, type=int)

    pagination = Post.query.order_by(Post.id.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    posts = [post for post in pagination.items if post.draft == False]

    return render_template('index.html',
                           title='首页',
                           posts=posts,
                           pagination=pagination)

@main.route('/<int:time>/<article_name>/')
def post(time, article_name):
    timestamp = str(time)[0:4] + '-' + str(time)[4:6] + '-' + str(time)[6:8]
    print(timestamp)

    post = Post.query.filter_by(timestamp=timestamp, url_name=article_name).first()
    if post:
        post.view_num += 1
        db.session.add(post)
        tags = [tag for tag in post.tags.split(',')]
        return render_template('post.html', post=post, tags=tags)
    return None

@main.route('/<page_url>/')
def page(page_url):
    page = Page.query.filter_by(url_name=page_url).first()

    return render_template('page.html', page=page)

@main.route('/tag/<tag_name>/')
def tag(tag_name):
    tag = Tag.query.filter_by(tag=tag_name).first()
    post_ids = PostTag.query.filter_by(tag_id=tag.id).all()
    # all_posts = Post.order_by().all()
    # posts = [post for post in all_posts if post.tag_in_post(tag.tag)]
    posts = []
    for id in post_ids:
        post = Post.query.filter_by(id=id).first()
        posts.append(post)
    return render_template('tag.html', tag=tag, posts=posts)

@main.route('/category/<category_name>/')
def category(category_name):
    category = Category.query.filter_by(category=category_name).first()
    posts = Post.query.filter_by(category=category).all()
    return render_template('category.html',
                           category=category,
                           posts=posts,
                           title='分类：' + category.category)

@main.route('/archives/')
def archives():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    posts = [post for post in pagination.items if post.draft == False]
    return render_template('archives.html',
                           title='归档',
                           posts=posts,
                           pagination=pagination)

@main.route('/search/')
# url_for('main.search', {keywords: xxx})
def search():
    search = request.args.get('keywords')
    pass

