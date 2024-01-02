from flask import Blueprint, Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from os import environ, path

app = Flask(__name__)

# I know this is not great.
# In a real setup there would be 1 database all containers connect to.
# This purpose of this project is the CI/CD process itself not the
# application or database. For simplify and demo this setups aligns
# with the goals of this project.
is_prod_like = environ.get("PROD_LIKE", "").lower() == "true"

# When running gunicorn their code be many works for 1 container
# when this is the case all the workers need to connect to the same
# database.
# TODO: Fine a better solution for this.
if is_prod_like:
    db = "sqlite:///" + path.join("/opt/simple-task-app/database/", "database.db")
else:
    db = "sqlite:///:memory:"


app.config["SQLALCHEMY_DATABASE_URI"] = db

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)


with app.app_context():
    db.create_all()

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("/")
def index():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)


@tasks_bp.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_task = Task(title=title)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("tasks.index"))


@tasks_bp.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Task.query.get(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for("tasks.index"))


app.register_blueprint(tasks_bp, url_prefix="/")


if __name__ == "__main__":
    debug = environ.get("FLASK_DEBUG", False)
    host = environ.get("FLASK_HOST", "127.0.0.1")
    port = environ.get("FLASK_PORT", 5000)
    app.run(debug=debug, host=host, port=port)
else:
    gunicorn_app = app
