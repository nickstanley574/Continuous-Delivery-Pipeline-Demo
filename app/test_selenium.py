import unittest
from selenium import webdriver
import docker
import time
import socket
from contextlib import closing


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


class SeleniumTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docker = docker.from_env()
        cls.container_name_pattern = "cicd-demo-webapp-selenium-local-"
        cls.image = "cicd-demo-webapp:local"

    @classmethod
    def tearDownClass(cls):
        # Code that runs once after all test methods have been called
        # Get a list of all containers
        for container in cls.docker.containers.list():
            # Check if the container name contains the specified pattern
            if cls.container_name_pattern in container.name:
                container.stop()
                container.remove()
                print(f"\nOrphan Container found {container.name} removed.")

    def setUp(self):
        port = find_free_port()
        container_name = f"{self.container_name_pattern}{port}"
        self.container = self.docker.containers.run(
            self.image, detach=True, name=container_name, ports={5000: port}
        )

        time.sleep(2)

        self.options = webdriver.ChromeOptions()
        # self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(f"http://127.0.0.1:{port}")
        self.driver.set_window_size(1024, 768)

    def tearDown(self):
        # logs = self.container.logs().decode('utf-8')
        self.container.stop()
        self.container.remove()
        self.driver.quit()

    def test_add_task(self):
        input_element = self.driver.find_element("name", "title")
        submit_button = self.driver.find_element("xpath", "//form/button")
        input_element.send_keys("Selenium Test Task")
        submit_button.click()

        # Verify that the task is added to the list
        tasks = self.driver.find_elements("xpath", "//ul/li/span")
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].text, "Selenium Test Task")

    def test_task_order(self):
        r = range(1, 3)

        for i in r:
            input_element = self.driver.find_element("name", "title")
            submit_button = self.driver.find_element("xpath", "//form/button")
            input_element.send_keys(f"Selenium Test Task {i}")
            submit_button.click()

        tasks = self.driver.find_elements("xpath", "//ul/li/span")

        for i in r:
            self.assertEqual(tasks[i - 1].text, f"Selenium Test Task {i}")

    def test_delete_task(self):
        # Add a task for deletion
        input_element = self.driver.find_element("name", "title")
        submit_button = self.driver.find_element("xpath", "//form/button")
        input_element.send_keys("Task to Delete")
        submit_button.click()

        # Find the delete link and click it
        delete_link = self.driver.find_element("xpath", "//ul/li/a")
        delete_link.click()

        # Verify that the task is deleted from the list
        tasks = self.driver.find_elements("xpath", "//ul/li")
        self.assertEqual(len(tasks), 0)


if __name__ == "__main__":
    unittest.main()
