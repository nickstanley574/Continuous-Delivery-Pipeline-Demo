from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import logging


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    db = SQLAlchemy(app)

    # log = logging.getLogger('werkzeug')
    # log.setLevel(logging.ERROR)

    class Task(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(50), nullable=False)

    @app.route("/")
    def index():
        tasks = Task.query.all()
        return render_template("index.html", tasks=tasks)


    @app.route("/add", methods=["POST"])
    def add():
        title = request.form.get("title")
        new_task = Task(title=title)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("index"))


    @app.route("/delete/<int:id>")
    def delete(id):
        task_to_delete = db.session.get(Task, id)
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for("index"))
    
    return app, db


if __name__ == "__main__":
    app, db = create_app()
    with app.app_context():
        db.create_all()
    # app.run(debug=True)
    app.run(debug=True, port=5000, host='0.0.0.0')
