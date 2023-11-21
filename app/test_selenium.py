import unittest
from selenium import webdriver

# from selenium.webdriver.common.keys import Keys
import time


class SeleniumTestCase(unittest.TestCase):
    def setUp(self):
        self.options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=self.options)

        self.driver.get("http://127.0.0.1:5000/")
        time.sleep(5)

    def tearDown(self):
        self.driver.quit()

    def test_add_task(self):
        # Find the input field and submit button
        input_element = self.driver.find_element_by_name("title")
        submit_button = self.driver.find_element_by_xpath("//form/button")
        time.sleep(3)

        # Type a task into the input field and submit
        input_element.send_keys("Selenium Test Task")
        submit_button.click()
        time.sleep(3)

        # Verify that the task is added to the list
        tasks = self.driver.find_elements_by_xpath("//ul/li")
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].text, "Selenium Test Task")

    # def test_delete_task(self):
    #     # Add a task for deletion
    #     input_element = self.driver.find_element_by_name('title')
    #     submit_button = self.driver.find_element_by_xpath('//form/button')
    #     input_element.send_keys('Task to Delete')
    #     submit_button.click()

    #     # Find the delete link and click it
    #     delete_link = self.driver.find_element_by_xpath('//ul/li/a')
    #     delete_link.click()

    #     # Verify that the task is deleted from the list
    #     tasks = self.driver.find_elements_by_xpath('//ul/li')
    #     self.assertEqual(len(tasks), 0)


if __name__ == "__main__":
    unittest.main()
