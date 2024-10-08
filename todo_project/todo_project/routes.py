from flask import render_template, url_for, flash, redirect, request

from todo_project import app, db, bcrypt
from prometheus_client import Counter

home_counter = Counter('home_requests_total', 'Total requests to the home page')
about_counter = Counter('about_requests_total', 'Total requests to the about page')
login_counter = Counter('login_requests_total', 'Total requests to the login page')
register_counter = Counter('register_requests_total', 'Total requests to the register page')
all_tasks_counter = Counter('all_tasks_requests_total', 'Total requests to the all_tasks page')
add_task_counter = Counter('add_task_requests_total', 'Total requests to the add_task page')
update_task_counter = Counter('update_task_requests_total', 'Total requests to the update_task page')
delete_task_counter = Counter('delete_task_requests_total', 'Total requests to the delete_task page')
account_counter = Counter('account_requests_total', 'Total requests to the account page')
change_password_counter = Counter('change_password_requests_total', 'Total requests to the change_password page')


# Import the forms
from todo_project.forms import (LoginForm, RegistrationForm, UpdateUserInfoForm, 
                                UpdateUserPassword, TaskForm, UpdateTaskForm)

# Import the Models
from todo_project.models import User, Task

# Import 
from flask_login import login_required, current_user, login_user, logout_user


@app.errorhandler(404)
def error_404(error):
    return (render_template('errors/404.html'), 404)

@app.errorhandler(403)
def error_403(error):
    return (render_template('errors/403.html'), 403)

@app.errorhandler(500)
def error_500(error):
    return (render_template('errors/500.html'), 500)


@app.route("/")
@app.route("/about")
def about():
    home_counter.inc()
    about_counter.inc()
    return render_template('about.html', title='About')


@app.route("/login", methods=['POST', 'GET'])
def login():
    login_counter.inc()
    if current_user.is_authenticated:
        return redirect(url_for('all_tasks'))

    form = LoginForm()
    # After you submit the form
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # Check if the user exists and the password is valid
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            task_form = TaskForm()
            flash('Login Successfull', 'success')
            app.logger.info(f'Login bem sucedido: {form.username.data}')
            return redirect(url_for('all_tasks'))
        else:
            flash('Login Unsuccessful. Please check Username Or Password', 'danger')
            app.logger.warning(f'Falha no login: {form.username.data}')
    
    return render_template('login.html', title='Login', form=form)
    

@app.route("/logout")
def logout():
    logout_user()
    app.logger.info(f'Logout bem sucedido!')
    return redirect(url_for('login'))


@app.route("/register", methods=['POST', 'GET'])
def register():
    register_counter.inc()
    if current_user.is_authenticated:
        return redirect(url_for('all_tasks'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        app.logger.info(f'Cadastro efetuado: {form.username.data}')
        flash(f'Account Created For {form.username.data}', 'success')
        return redirect(url_for('login'))
    elif request.method == 'POST':
        app.logger.warning(f'Cadastro não efetuado: {form.username.data}')

    return render_template('register.html', title='Register', form=form)


@app.route("/all_tasks")
@login_required
def all_tasks():
    all_tasks_counter.inc()
    tasks = User.query.filter_by(username=current_user.username).first().tasks
    app.logger.info(f'Visualização de tasks.')
    return render_template('all_tasks.html', title='All Tasks', tasks=tasks)


@app.route("/add_task", methods=['POST', 'GET'])
@login_required
def add_task():
    add_task_counter.inc()
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(content=form.task_name.data, author=current_user)
        db.session.add(task)
        db.session.commit()
        app.logger.info(f'Criação de task bem sucedida! {form.task_name.data}')
        flash('Task Created', 'success')
        return redirect(url_for('add_task'))
    elif request.method == 'POST':
        app.logger.warning(f'Criação de task não efetuada: {form.task_name.data}')
    return render_template('add_task.html', form=form, title='Add Task')


@app.route("/all_tasks/<int:task_id>/update_task", methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    update_task_counter.inc()
    task = Task.query.get_or_404(task_id)
    form = UpdateTaskForm()
    if form.validate_on_submit():
        if form.task_name.data != task.content:
            task.content = form.task_name.data
            db.session.commit()
            app.logger.info(f'Atualização de task bem sucedida! {form.task_name.data}')
            flash('Task Updated', 'success')
            return redirect(url_for('all_tasks'))
        else:
            flash('No Changes Made', 'warning')
            return redirect(url_for('all_tasks'))
    elif request.method == 'POST':
        app.logger.warning(f'Atualização de task não efetuada: {form.task_name.data}')
    elif request.method == 'GET':
        form.task_name.data = task.content
    return render_template('add_task.html', title='Update Task', form=form)


@app.route("/all_tasks/<int:task_id>/delete_task")
@login_required
def delete_task(task_id):
    delete_task_counter.inc()
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    app.logger.info(f'Exclusão de task bem sucedida!')
    flash('Task Deleted', 'info')
    return redirect(url_for('all_tasks'))


@app.route("/account", methods=['POST', 'GET'])
@login_required
def account():
    account_counter.inc()
    form = UpdateUserInfoForm()
    if form.validate_on_submit():
        if form.username.data != current_user.username:  
            current_user.username = form.username.data
            db.session.commit()
            app.logger.info(f'Atualização de usuário bem sucedida! {form.username.data}')
            flash('Username Updated Successfully', 'success')
            return redirect(url_for('account'))
    elif request.method == 'POST':
        app.logger.warning(f'Atualização de usuário não efetuada: {form.username.data}')
    elif request.method == 'GET':
        form.username.data = current_user.username 

    return render_template('account.html', title='Account Settings', form=form)


@app.route("/account/change_password", methods=['POST', 'GET'])
@login_required
def change_password():
    change_password_counter.inc()
    form = UpdateUserPassword()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.old_password.data):
            current_user.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            db.session.commit()
            app.logger.info(f'Atualização de senha bem sucedida!')
            flash('Password Changed Successfully', 'success')
            redirect(url_for('account'))
        else:
            app.logger.warning(f'Atualização de senha não efetuada.')
            flash('Please Enter Correct Password', 'danger') 

    return render_template('change_password.html', title='Change Password', form=form)

