import unittest
from selenium import webdriver
import docker
import time
import socket
from contextlib import closing
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    filename="selenium.log",
    format="[%(levelname)s] %(asctime)s - %(message)s",
)


def find_free_port():
    """Find and return a free port on the local machine."""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = s.getsockname()[1]
        print(f"\n\n{port}\n\n")
        return port


class SeleniumTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docker = docker.from_env()
        cls.container_name_pattern = "cicd-demo-webapp-selenium-local-"
        cls.image = f"cicd-demo-webapp:cicd-demo-local-jenkins-9"

        selenium_name = "selenium-standalone-chrome"

        logging.info(f"Starting selenium container: {selenium_name}")
        cls.selenium_container = cls.docker.containers.run(
            name=selenium_name,
            image="selenium/standalone-chrome",
            detach=True,
            environment={
                "SE_NODE_MAX_SESSIONS": "3",
                "SE_NODE_OVERRIDE_MAX_SESSIONS": "true",
                "SE_NODE_SESSION_TIMEOUT": "60",
            },
            ports={"4444": "4444", "7900": "7900"},
        )

    @classmethod
    def tearDownClass(cls):
        # Get a list of all containers
        for container in cls.docker.containers.list():
            # Check if the container name contains the specified pattern
            if cls.container_name_pattern in container.name:
                logging.warning(f"Orphan Container found {container.name} removing.")
                container.stop()
                container.remove()

        logging.info(f"Stopping selenium container: {cls.selenium_container.name}")
        cls.selenium_container.stop()
        cls.selenium_container.remove()

    def setUp(self):
        port = find_free_port()
        container_name = f"{self.container_name_pattern}{port}"
        logging.info(f"Starting app container: {container_name}")
        self.container = self.docker.containers.run(
            self.image, name=container_name, detach=True, ports={5000: port}
        )
        time.sleep(3)
        self.options = webdriver.ChromeOptions()
        self.driver = webdriver.Remote(
            command_executor="http://localhost:4444", options=self.options
        )
        self.driver.set_window_size(1024, 768)
        self.driver.get(f"http://192.168.5.207:{port}")

    def tearDown(self):
        # logs = self.container.logs().decode('utf-8')
        self.driver.quit()
        logging.info(f"Deleting app container {self.container.name}")
        self.container.stop()
        self.container.remove()

    ##############
    # Unit Tests #
    ##############

    def test_add_task(self):
        """Test ensures that adding a task through the UI works as expected."""

        # Input task name and submit
        input_element = self.driver.find_element("name", "title")
        input_element.send_keys("Selenium Test Task")

        submit_button = self.driver.find_element("xpath", "//form/button")
        submit_button.click()

        # Check if task is added successfully
        tasks = self.driver.find_elements("xpath", "//ul/li/span")
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].text, "Selenium Test Task")

    def test_task_order(self):
        """Test ensures that tasks are added in the correct order."""

        task_indices = range(1, 3)

        # Iterate over the range to add tasks with different indices
        for i in task_indices:
            input_element = self.driver.find_element("name", "title")
            input_element.send_keys(f"Selenium Test Task {i}")

            submit_button = self.driver.find_element("xpath", "//form/button")
            submit_button.click()

        # Find all task
        tasks = self.driver.find_elements("xpath", "//ul/li/span")

        # Iterate over the range to assert the task text matches the expected values
        for i in task_indices:
            self.assertEqual(tasks[i - 1].text, f"Selenium Test Task {i}")

    def test_delete_task(self):
        """This test ensures that the deletion functionality works as expected."""

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
    print("\n\n")
    unittest.main()
    print("More log details: selenium.log")
    print("\nDone.")
