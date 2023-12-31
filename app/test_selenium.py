import unittest
from selenium import webdriver
import docker
import time
import socket
from contextlib import closing
import logging
import os
import requests


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("debug.log")],
)


def wait_for_url(url, max_try=3, sleep_duration=2, timeout=5):
    for i in range(max_try):
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                logging.info(f"URL {url} returned a 200 OK.")
                return True
            else:
                logging.info(
                    f"Attempt {i + 1}: {url} returned a non-200 code: {response.status_code}. Retrying..."
                )
        except requests.RequestException as e:
            logging.info(
                f"Attempt {i + 1}: Error accessing the URL {url}: {e}. Retrying..."
            )
        time.sleep(sleep_duration)

    logging.critical(
        f"Maximum number of retries ({max_try}) reached. Unable to get a 200 status code for the URL {url}."
    )
    return False


def find_free_port():
    """Find and return a free port on the local machine."""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = s.getsockname()[1]
        return port


class DockerHelper:
    """Utility class for managing Docker containers and images."""

    def __init__(self) -> None:
        """Initializes a new instance and sets up the Docker client."""
        self.client = docker.from_env()

    def remove_container(self, container):
        """Removes the specified Docker container.

        Args:
            container (str or docker.models.containers.Container): Container ID or object.

        Raises:
            docker.errors.NotFound: If the specified container is not found.
            Exception: For other unexpected errors during container removal.
        """
        try:
            if isinstance(container, str):
                container = self.client.containers.get(container)
            container.stop()
            container.remove()
            logging.info(f"Container '{container.name} {container.short_id}' removed.")
        except docker.errors.NotFound:
            logging.warn(f"Container '{container.name}' not found.")
        except Exception as e:
            logging.fatal(f"Docker helper Fatal Exception: {e}")

    def container_exists(self, container_name):
        """Checks if a Docker container with the given name exists.

        Args:
            container_name (str): Name of the Docker container.

        Returns:
            bool: True if the container exists, False otherwise.
        """
        try:
            self.client.containers.get(container_name)
            return True
        except docker.errors.NotFound:
            return False

    def image_exists(self, image_name):
        """Checks if a Docker image with the given name exists.

        Args:
            image_name (str): Name of the Docker image.

        Returns:
            bool: True if the image exists, False otherwise.
        """
        try:
            self.client.images.get(image_name)
            return True
        except docker.errors.ImageNotFound:
            return False

    def get_internal_ip(self, container):
        """Retrieves the internal IP address of a Docker container.

        Args:
            container (docker.models.containers.Container): Docker container object.

        Returns:
            str: Internal IP address of the container.
        """
        return (
            container.exec_run("hostname -i").output.decode("utf-8").replace("\n", "")
        )


class SeleniumTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.info(f"Starting Selenium test run...")

        force_reset = os.getenv("FORCE_GRID_RESET", "").lower() == "true"
        cls.local_mode = os.getenv("LOCAL", "").lower() == "true"

        cls.image = os.environ.get("IMAGE")

        app_image = cls.image.split(":")[0].replace("/", "-")
        tag_value = cls.image.split(":")[-1]

        cls.docker_helper = DockerHelper()
        cls.docker_client = cls.docker_helper.client

        cls.container_name_pattern = f"{app_image}-selenium-"

        if tag_value is None:
            msg = "Environment variable 'TAG' is not set. Please set it before running the script. Exiting with code 2."
            logging.fatal(msg)
            raise Exception(msg)

        # Check if the image exists locally
        if not cls.docker_helper.image_exists(cls.image):
            try:
                cls.docker_client.images.pull(cls.image)
                logging.info(f"Image '{cls.image}' has been pulled successfully.")
            except:
                msg = f"Unable to locate image '{cls.image}' from local or remote."
                raise Exception(msg)

        selenium_name = f"selenium-standalone-chrome"

        logging.info(f"Starting selenium container: {selenium_name}")

        if cls.docker_helper.container_exists(selenium_name) and (
            force_reset or cls.local_mode
        ):
            cls.docker_helper.remove_container(selenium_name)

        cls.selenium_container = cls.docker_client.containers.run(
            name=selenium_name,
            image="selenium/standalone-chrome",
            detach=True,
            environment={"SE_NODE_MAX_SESSIONS": "1", "SE_NODE_SESSION_TIMEOUT": "15"},
            ports={4444: 4444, 7900: 7900},
        )

        cls.selenium_internal_ip = cls.docker_helper.get_internal_ip(
            cls.selenium_container
        )

    @classmethod
    def tearDownClass(cls):
        # Get a list of all containers
        for container in cls.docker_client.containers.list():
            # Check if the container name contains the specified pattern
            if cls.container_name_pattern in container.name:
                logging.warning(f"Orphan Container found {container.name} removing.")
                cls.docker_helper.remove_container(container)

        logging.info(f"Stopping selenium container: {cls.selenium_container.name}")
        cls.docker_helper.remove_container(cls.selenium_container)
        logging.info(f"Test run complete.")

    def setUp(self):
        port = find_free_port()
        container_name = f"{self.container_name_pattern}{port}"

        logging.info(
            f"{self._testMethodName}: Starting app container: {container_name}"
        )

        self.container = self.docker_client.containers.run(
            self.image, name=container_name, detach=True, ports={8080: port}
        )

        if self.local_mode:
            # if in local mode use local chrome.
            self.driver = webdriver.Chrome()
            app_url = f"http://localhost:{port}"

        else:
            grid_url = f"http://{self.selenium_internal_ip}:4444"
            wait_for_url(grid_url)
            options = webdriver.ChromeOptions()
            self.driver = webdriver.Remote(
                command_executor=grid_url,
                options=options,
            )
            app_internal_ip = self.docker_helper.get_internal_ip(self.container)
            app_url = f"http://{app_internal_ip}:8080"

        wait_for_url(app_url)

        self.driver.set_window_size(1024, 768)

        logging.info(
            f"{self._testMethodName}: Making request to {container_name} at {app_url}"
        )

        self.driver.get(app_url)

    def tearDown(self):
        try:
            result = self.defaultTestResult()
            status = "PASSED" if result.wasSuccessful() else "FAILED"

            logging.info(f"{self._testMethodName}: {status}")

            # logs = self.container.logs().decode('utf-8')
            self.driver.quit()
            logging.info(
                f"{self._testMethodName}: Deleting app container {self.container.name}"
            )
            self.docker_helper.remove_container(self.container)
        except Exception as e:
            logging.fatal(f"{e}")

    ####################
    ## Selenium Tests ##
    ####################

    def test_add_task(self):
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
    print("More log details: selenium.log")
    unittest.main()
    print("\nDone.")
