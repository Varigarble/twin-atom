'''Flask must be launched from app.py before running tests!'''
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import requests

class E2ETests(unittest.TestCase):
    API_URL = "http://localhost:5000"
    TASKS_ENTRY = f"{API_URL}/tasks_entry.html"
    TASKS_VIEW = f"{API_URL}/tasks_view.html"

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(r"C:\Program Files (x86)\chromedriver.exe",
            options=chrome_options)

        # driver = webdriver.Chrome(options=chrome_options)

    def test_http_response_layout(self):
        self.driver.get(E2ETests.API_URL)
        r = requests.get(E2ETests.API_URL)
        self.assertEqual(r.status_code, 200)

    def test_http_response_tasks_entry(self):
        self.driver.get(E2ETests.TASKS_ENTRY)
        r = requests.get(E2ETests.TASKS_ENTRY)
        self.assertEqual(r.status_code, 200)
        self.assertEqual("http://localhost:5000/tasks_entry.html", 
            self.driver.current_url)

    def test_http_response_tasks_view(self):
        self.driver.get(E2ETests.TASKS_VIEW)
        r = requests.get(E2ETests.TASKS_VIEW)
        self.assertEqual(r.status_code, 200)
        self.assertEqual("http://localhost:5000/tasks_view.html", 
            self.driver.current_url)

    def test_browser_title_contains_app_name(self):
        self.driver.get(E2ETests.API_URL)
        self.assertIn('The World Needs Another Task Manager!', 
            self.driver.title)

    def test_flask_selenium_find_in_layout(self):
        self.driver.get(E2ETests.API_URL)
        r = requests.get(E2ETests.API_URL)
        self.assertIn("Twin Atom", 
            self.driver.find_element_by_class_name("header__center").text) 

    def test_flask_selenium_find_in_tasks_view(self):
        self.driver.get(E2ETests.TASKS_VIEW)
        r = requests.get(E2ETests.TASKS_VIEW)
        self.assertIn("Tasks View", 
            self.driver.find_element_by_class_name("main").text)

    def test_creator_selection(self):
        self.driver.get(E2ETests.TASKS_VIEW)
        r = requests.get(E2ETests.TASKS_VIEW)
        # test initial dropdown menu selection 'None' matches displayed selection:
        self.assertIn(self.driver.find_element_by_class_name("selected_creator").text, 
            self.driver.find_element_by_class_name("creators_tasks").text)
        # change dropdown to 'Varigarble', submit, match to displayed selection:
        dropdown = self.driver.find_element_by_name("creators")
        selector = Select(dropdown)
        selector.select_by_value("Varigarble")
        submit = self.driver.find_element_by_name("Submit")
        submit.submit()
        self.assertIn("Varigarble", 
            self.driver.find_element_by_class_name("creators_tasks").text)


    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
