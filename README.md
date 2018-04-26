A Minimal To-Do List app with Flask

To use the app run below commands

git clone https://github.com/veeshalsoni/flask-todo.git
pip install --requirement requirement.txt
flask db init
flask db migrate
flask db upgrade
export FLASK_APP=todo.py
flask run