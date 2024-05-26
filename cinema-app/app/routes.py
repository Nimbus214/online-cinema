import os
from flask import Flask, render_template, flash, redirect, url_for
import grpc

from cinema_library_pb2 import FilmGenre, Film, RecommendationRequest, FilmId
from cinema_library_pb2_grpc import RecommendationsStub

from users_pb2 import Status, UserRequest
from users_pb2_grpc import UsersStub

from app import app
from app.forms import PastebinEntry, LoginForm

recommendations_host = os.getenv("RECOMMENDATIONS_HOST", "localhost")
recommendations_channel = grpc.insecure_channel(f"{recommendations_host}:50051")
recommendations_client = RecommendationsStub(recommendations_channel)

users_host = os.getenv("USERS_HOST", "localhost")
users_channel = grpc.insecure_channel(f"{users_host}:50052")
users_client = UsersStub(users_channel)
current_user = None


@app.route("/", methods=['GET'])
@app.route("/index", methods=['GET'])
def index():
    global recommendations_client
    recommendations_request = RecommendationRequest(category=FilmGenre.ALL)
    recommendations_response = recommendations_client.Recommend(recommendations_request)
    return render_template(
        "homepage.html",
        recommendations=recommendations_response.recommendations
    )

@app.route('/film/<id>', methods=['GET', 'POST'])
def render_film(id):
    global recommendations_client
    film_request = FilmId(id=int(id))
    film = recommendations_client.GetFilm(film_request)
    form = PastebinEntry()
    if form.marks.data is not None:
        flash('Оценка поставлена!')
    return render_template(
        "film.html",
        film=film,
        form=form,
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if not form.validate_on_submit():
        return render_template('login.html', title='Sign In', form=form)
        
    user_request = UserRequest(username=str(form.username.data), password=str(form.password.data))
    status = users_client.UserExist(user_request)
    if status.status == Status.EXIST:
        global current_user
        current_user = form.username.data, form.password.data
        flash(
            'Login requested for user {}, remember_me={}'.format(
                form.username.data, form.remember_me.data
            )
        )
        return redirect(url_for('index'))
    else:
        flash("Все хуйня давай по новой")
    return render_template('login.html', title='Sign In', form=form)

@app.route('/user', methods=['GET'])
def user():
    if current_user is None:
        return redirect(url_for('index'))
    return render_template('user.html', user=current_user)
