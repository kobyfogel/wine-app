from flask import abort, flash, jsonify, make_response, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import and_
from wine import app, bcrypt, db
from wine.forms import (CommentForm, FavoriteForm, LoginForm, 
    RegistrationForm, ResetPasswordForm, SearchFrom, WineForm)
from wine.models import FavoriteWine, User, Wine, WineComment


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = SearchFrom()
    if form.validate_on_submit():
        del form['submit']
        # form = {key: value.capitalize() for key, value 
        #     in form.data.items() if value != ""}
        # results = Wine.query.filter_by(**form).all()
        title = form.title.data.split(" ")
        form = {key: value.capitalize() for key, value 
            in form.data.items() if value != "" and key != "title"}
        results = Wine.query.filter_by(**form).all()
        title_results = title_results = Wine.query.filter(and_(Wine.title.contains(word.capitalize()) for word in title)).all()  
        final_results = []
        for result in results:
            for title in title_results:
                if result._id == title._id:
                    final_results.append(result)
        return render_template('results.j2', results=final_results, 
            title='Search Results')
    return render_template('home.j2', form=form, title='home')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, 
            password=hashed_password, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account was created for {form.username.data}!', 'seccess')
        return redirect(url_for('login'))
    return render_template('register.j2', form=form, title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessfull! please check credentials', 'danger')
    return render_template('login.j2', form=form, title='Login')


@app.route('/account/', methods=['GET', 'POST'])
@login_required
def account():
    favorites_id = FavoriteWine.query.filter_by(favored_by=current_user).all()
    favorites = [Wine.query.filter_by(
        _id=wine.wine_id).first() for wine in favorites_id]
    favorites = {wine: WineComment.query.filter_by(
        wine_id=wine._id).all() for wine in favorites}
    return render_template('account.j2', title="Account", favorites=favorites)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.email == form.email.data:
            login_user(user)
            current_user.password = bcrypt.generate_password_hash(
                form.new_password.data).decode('utf-8')
            db.session.commit()
            logout_user()
            flash('Password updated successfully!', 'seccess')
            return redirect(url_for('login'))
        flash('Password update failed! please check credentials', 'danger')
    return render_template('reset.j2', form=form, title="Reset Password")


@app.route('/results', methods=['GET', 'POST'])
def results(results):
    return render_template('results.h2', 
        results=results, title="Search Results")


@app.route('/wine/<int:wine_id>', methods=['GET', 'POST'])
def wine(wine_id):
    wine = Wine.query.get_or_404(wine_id)
    form = CommentForm()
    if form.validate_on_submit() and form.submit.data:
        new_comment = WineComment(comment=form.content.data, 
            commented_by=current_user, commented_on=wine)
        db.session.add(new_comment)
        db.session.commit()
        form.content.data = None
    wine_comments = WineComment.query.filter_by(wine_id=wine._id)
    favorite_form = FavoriteForm()
    if current_user.is_authenticated:
        is_favored = FavoriteWine.query.filter_by(wine_id=wine._id, 
            user_id=current_user._id).first()
    else:
        is_favored = False
    if favorite_form.clicked.data:
        if is_favored:
            db.session.delete(is_favored)
            is_favored = False
        else:
            favorite = FavoriteWine(
                favored_by=current_user, favored_wine=wine)
            db.session.add(favorite)
            is_favored = True
        db.session.commit()
    return render_template('wine.j2', wine=wine,
        form=form, title=wine.title, comments=wine_comments, 
        is_favored=is_favored, favorite_form=favorite_form)


@app.route('/edit-comment', methods=['POST'])
def edit_comment():
    req = request.get_json()
    comment = WineComment.query.get_or_404(req['comment_id'])
    comment.comment = req['comment_content']
    db.session.commit()
    return make_response(jsonify({"message": "comment updated"}), 200)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_wine():
    form = WineForm()
    if form.validate_on_submit():
        del form['submit']
        data = {key: value.capitalize() 
            for key, value in form.data.items() if value != "" and type(value) is str}
        wine = Wine(points=form.points.data, added_by=current_user, **data)
        db.session.add(wine)
        db.session.commit()
        flash('You successfully added a wine!', 'success')
        return redirect(url_for('home'))
    return render_template('new_wine.j2', title='New Wine',
                           form=form, legend='Add new wine')


@app.route("/wine/<int:wine_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_wine(wine_id):
    wine = Wine.query.get_or_404(wine_id)
    if wine.added_by != current_user:
        abort(403)
    form = WineForm()
    if form.validate_on_submit():
        wine.title = form.title.data.capitalize()
        wine.country = form.country.data.capitalize()
        wine.description = form.description.data.capitalize()
        wine.points = form.points.data
        wine.province = form.province.data.capitalize()
        wine.variety = form.variety.data.capitalize()
        wine.winery = form.winery.data.capitalize()
        db.session.commit()
        flash('You successfully editted the wine!', 'success')
        return redirect(url_for('wine', wine_id=wine._id))
    if request.method == 'GET':
        form.title.data = wine.title
        form.country.data = wine.country
        form.description.data = wine.description
        form.points.data = wine.points
        form.province.data = wine.province
        form.variety.data = wine.variety
        form.winery.data = wine.winery
    return render_template('new_wine.j2', title='Edit Wine',
                           form=form, legend='Edit wine')


@app.route("/wine/<int:wine_id>/delete", methods=['POST'])
@login_required
def delete_wine(wine_id):
    wine = Wine.query.get_or_404(wine_id)
    if wine.added_by != current_user:
        abort(403)
    db.session.delete(wine)
    db.session.commit()
    flash('Your wine has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/comment/<int:comment_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = WineComment.query.get_or_404(comment_id)
    wine = Wine.query.get_or_404(comment.wine_id) 
    if comment.commented_by != current_user:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted!', 'success')
    return redirect(url_for('wine', wine_id=wine._id))
