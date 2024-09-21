# import pytest
from todo_project import app, db, bcrypt
# from todo_project.models import User, Task

# @pytest.fixture(scope='module')
# def test_client():
#     # Cria o app de teste
#     flask_app = app
#     flask_app.config['TESTING'] = True
#     flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/laisdumont/Github/Task-Manager-using-Flask/todo_project/todo_project/tests/site.db'
#     flask_app.config['WTF_CSRF_ENABLED'] = False

#     with flask_app.test_client() as testing_client:
#         with flask_app.app_context():
#             # db.create_all()
#             yield testing_client  # os testes são executados aqui
#             db.session.remove()
#             db.drop_all()


# @pytest.fixture(scope='module')
# def init_database():
#     # Inicializa o banco de dados com um usuário
#     hashed_password = bcrypt.generate_password_hash('testpassword').decode('utf-8')
#     user = User(username='testuser', password=hashed_password)
#     db.session.add(user)
#     db.session.commit()
#     yield
#     db.session.remove()
#     db.drop_all()


# def test_about_route(test_client):
#     response = test_client.get('/about')
#     assert response.status_code == 200
#     assert b'About' in response.data


# def test_login_route(test_client, init_database):
#     # Teste de GET na rota de login
#     response = test_client.get('/login')
#     assert response.status_code == 200

#     # Teste de POST com login correto
#     response = test_client.post('/login', data=dict(
#         username='testuser',
#         password='testpassword'
#     ), follow_redirects=True)
#     assert response.status_code == 200
#     assert b'Login Successfull' in response.data


# def test_register_route(test_client):
#     response = test_client.get('/register')
#     assert response.status_code == 200

#     response = test_client.post('/register', data=dict(
#         username='newuser',
#         password='newpassword',
#         confirm='newpassword'
#     ), follow_redirects=True)
#     assert response.status_code == 200
#     assert b'Account Created For newuser' in response.data


# def test_add_task_route(test_client, init_database):
#     # Primeiro, faça o login
#     test_client.post('/login', data=dict(
#         username='testuser',
#         password='testpassword'
#     ))

#     # Em seguida, adicione uma tarefa
#     response = test_client.post('/add_task', data=dict(
#         task_name='Test Task'
#     ), follow_redirects=True)
#     assert response.status_code == 200
#     assert b'Task Created' in response.data


# def test_update_task_route(test_client, init_database):
#     # Login e adicione uma tarefa
#     test_client.post('/login', data=dict(
#         username='testuser',
#         password='testpassword'
#     ))

#     task = Task(content='Old Task', author=User.query.first())
#     db.session.add(task)
#     db.session.commit()

#     # Atualize a tarefa
#     response = test_client.post(f'/all_tasks/{task.id}/update_task', data=dict(
#         task_name='Updated Task'
#     ), follow_redirects=True)
#     assert response.status_code == 200
#     assert b'Task Updated' in response.data


# def test_delete_task_route(test_client, init_database):
#     # Login e adicione uma tarefa
#     test_client.post('/login', data=dict(
#         username='testuser',
#         password='testpassword'
#     ))

#     task = Task(content='Test Task', author=User.query.first())
#     db.session.add(task)
#     db.session.commit()

#     # Delete a tarefa
#     response = test_client.get(f'/all_tasks/{task.id}/delete_task', follow_redirects=True)
#     assert response.status_code == 200
#     assert b'Task Deleted' in response.data

import pytest
from todo_project import app as create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI":'sqlite:////home/laisdumont/Github/Task-Manager-using-Flask/todo_project/todo_project/tests/site.db'
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200