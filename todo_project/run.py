from todo_project import app
import os

if __name__ == '__main__':
    app.run(host=os.getenv('HOST'), debug=True)
