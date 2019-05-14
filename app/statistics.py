import matplotlib.pyplot as plt
import mpld3
import numpy as np
from sqlalchemy import func
from app.models import User, Post, PostToTag
from app import db


def get_posts_per_user_statistic():
    """
    This function return the posts per user as a html/js diagram.
    """

    posts_per_user = get_posts_per_user()

    x = np.arange(len(posts_per_user))
    posts = posts_per_user.values()

    font = {'weight': 'bold',
            'size': 20}

    plt.rc('font', **font)  # set font size

    fig, ax = plt.subplots()
    fig.set_size_inches(9, 7)  # set plot size
    plt.bar(x, posts)  # plot bars with number of posts
    plt.xticks(x, posts_per_user.keys())  # user names as label

    return mpld3.fig_to_html(fig)


def get_tag_frequency_statistics():
    """
    This function return appearances of tags as a html/js diagram.
    """

    tag_frequency = get_tag_frequency()

    x = np.arange(len(tag_frequency))
    tag_appearances = tag_frequency.values()

    font = {'weight': 'bold',
            'size': 10}

    plt.rc('font', **font)  # set font size

    fig, ax = plt.subplots()
    fig.set_size_inches(9, 7)  # set plot size
    plt.bar(x, tag_appearances)  # plot bars with number of tag appearance
    plt.xticks(x, tag_frequency.keys())  # tag names as label

    return mpld3.fig_to_html(fig)


def get_posts_per_user():
    """
    This function return the posts per user as a dictionary with the username and number of posts.
    """

    posts_per_user = {}
    posts_per_user_id = db.session.query(func.count('Post.id'), Post.user_id).group_by(Post.user_id).all()  # database call
    posts_per_user_id = dict([(t[1], t[0]) for t in posts_per_user_id])  # swap tuple values and make dict from list of tuples
    for user, posts in posts_per_user_id.items():  # map username to id
        posts_per_user[User.query.get(user).name] = posts
    return posts_per_user


def get_tag_frequency():
    """
    This function return how often tags appear as a dictionary with the tag name and number of appearances.
    """

    tag_frequency = db.session.query(func.count('PostToTag.name'), PostToTag.name).group_by(PostToTag.name).all()  # database call
    tag_frequency = dict([(t[1], t[0]) for t in tag_frequency])  # swap tuple values and make dict from list of tuples
    return tag_frequency
