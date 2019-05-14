import flask, app
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, RegistrationForm, PostForm
from app.models import User, Post, PostToTag
from app.utils import paginate, add_author
from app import app, db
import app.statistics as stats
from app import app

'''
Route für die Index Seite
'''
@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)        # URL Argument page wird geholt, default zu 1
    posts = add_author(Post.query.all())                # Alle Posts werden aus der DB geholt, ihnen wird je ein Autor-Objekt gematcht
    posts = paginate(posts, page, 5)                    # und in 5er Listen "paginated"  
    next_url = url_for('index', page=posts.next_num()) if posts.has_next() else None
    prev_url = url_for('index', page=posts.prev_num()) if posts.has_prev() else None
    return render_template('list_posts.html', posts=posts.items, title='DHBW Microblog', var=None, type=None, next_url=next_url, prev_url=prev_url)


'''
Route zum zeigen von Posts von einem User
'''
@login_required
@app.route('/user/<username>/')
def profile(username):
    page = request.args.get('page', 1, type=int)        # URL Argument page wird geholt, default zu 1
    if not username:
        user = current_user
    else:
        user = User.query.filter_by(name=username).first()      # das passende User Objekt zur URL wird aus der DB geladen
    if not user:
        flash('User does not exist.')                           # Falls der User nicht mit diesem Namen existiert wird eine Fehlernachricht angezeigt
        return redirect(url_for('index'))                       # Und auf den Index weitergeleitet
    posts = add_author(user.posts)                      # Alle Posts des Users werden aus der DB geholt, ihnen wird je ein Autor-Objekt gematcht
    posts = paginate(posts, page, 5)                    # und in 5er Listen "paginated"  
    next_url = f'/user/{username}/?page={posts.next_num()}' if posts.has_next() else None
    prev_url = f'/user/{username}/?page={posts.prev_num()}' if posts.has_prev() else None
    return render_template('list_posts.html', title=f'{user.name} - Profile', posts=posts.items, var=user.name, type='Profile', next_url=next_url, prev_url=prev_url)


'''
Route zum Zeigen von Posts mit einem bestimmten Tag
'''
@login_required
@app.route('/tag/<tag>/')
def tag(tag):
    page = request.args.get('page', 1, type=int)        # URL Argument page wird geholt, default zu 1
    posts = []
    posts_with_tag = PostToTag.query.filter_by(name=tag).all()  # Es werden alle PostToTag Objekte aus der DB geholt
    if not posts_with_tag:
        flash('Tag does not exist.')                            # Falls der tag nicht existiert
        return redirect(url_for('index'))                       # Wird ein Fehler angezeigt und auf den Index weitergeleitet
    for post in posts_with_tag:                         # Anhand der PostToTag Objekte werden nun Post Objekte anhand der PostID aus der DB geladen
        post = Post.query.get(int(post.post_id))
        posts.append(post)
    posts = add_author(posts)                           # Diesen Posts wird nun ein Autor Objekt gematcht
    posts = paginate(posts, page, 5)                    # und sie werde in 5er Listen "paginated"
    next_url = f'/tag/{tag}/?page={posts.next_num()}' if posts.has_next() else None
    prev_url = f'/tag/{tag}/?page={posts.next_num()}' if posts.has_prev() else None
    return render_template('list_posts.html', title=f'{tag} - Tag', posts=posts.items, var=tag, type='Posts with Tag', next_url=next_url, prev_url=prev_url)

'''
Login Route
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:                   # Login Seite ist nicht erreichtbar als eingeloggter Nutzer
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():                       # Falls ein POST/PATCH/DELETE durchgeführt wird
        user = User.query.filter_by(name=form.username.data).first()        # Wird das User Objekt mit dem Namen aus der DB geladen 
        if not user or not user.check_password(form.password.data):         # Benutzername und Passwort werden auf Fehler überprüft
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.keep_logged_in.data)                 # Der Benutzer wird eingeloggt
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)        # Bei einem GET wird nur die Form geladen

@app.route('/logout')
def logout():
    logout_user()                                       # User wird ausgeloggt
    return redirect(url_for('index'))


'''
Register Route
'''
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:                   # Register nur verwendbar nur für anonyme Nutzer
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():                       # Falls ein POST/PATCH/DELETE durchgeführt wird
        user = User(name=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)                            # Die Daten werden überprüft und als User-Objekt dem DB commit hinzugefügt
        db.session.commit()
        flash('Congratulations, you are now registered!')
        return redirect(url_for('login'))               # Weiterleiten zum Login
    return render_template('register.html', title='Register now!', form=form)


'''
Statistics Route
'''
@login_required
@app.route('/statistics')
def statistics():
    return render_template('statistics.html', posts_per_user=stats.get_posts_per_user_statistic(), tag_frequency=stats.get_tag_frequency_statistics())


'''
Post Submission Route
'''
@login_required
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if not current_user.is_authenticated:               # Post Submission nur verwendbar nur für anonyme Nutzer
        return redirect(url_for('index'))
    form = PostForm()
    if form.validate_on_submit():                       # Falls ein POST/PATCH/DELETE durchgeführt wird
        user = current_user 
        post = Post(title=form.title.data, text=form.content.data, user_id=user.id)             # Post Objekt wird erstellt
        db.session.add(post)                            # Objekt wird dem nächsten DB commit hinzugefügt
        db.session.commit()
        tags = form.tags.data.split(',')                # Der Tag String wird am Komma getrennt
        for tag in tags:
            tag = tag.strip()
            cur_tag = PostToTag(name=tag, post_id=post.id)      # Jeder tag wird einzeln in Verbindung mit dem POST gespeichert
            db.session.add(cur_tag)                     # Tag Objekt wird dem nächsten DB Commit hinzugefügt
        db.session.commit()
        return redirect(f'/user/{user.name}')
    return render_template('submit.html', form=form)
