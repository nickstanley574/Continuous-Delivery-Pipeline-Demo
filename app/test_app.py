import unittest
from app import app, db, Task


class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index_route(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_add_task(self):
        response = self.app.post("/add", data={"title": "Test Task"})
        self.assertEqual(response.status_code, 302)  # 302 indicates a redirect
        with app.app_context():
            tasks = Task.query.all()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Test Task")

    def test_delete_task(self):
        task = Task(title="Test Task")
        with app.app_context():
            db.session.add(task)
            db.session.commit()

        response = self.app.get("/delete/1")
        self.assertEqual(response.status_code, 302)  # 302 indicates a redirect
        with app.app_context():
            tasks = Task.query.all()
        self.assertEqual(len(tasks), 0)


if __name__ == "__main__":
    unittest.main()
