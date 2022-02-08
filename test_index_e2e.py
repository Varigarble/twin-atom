import unittest
from selenium import webdriver
import requests


'''Flask must be launched from app.py before running tests!'''

class E2ETests(unittest.TestCase):
    API_URL = "http://localhost:5000"

    def setUp(self):
        self.driver = webdriver.Chrome(r"C:\Program Files (x86)\chromedriver.exe")
        self.driver.get(E2ETests.API_URL)

    def test_1_http_response(self):
        r = requests.get(E2ETests.API_URL)
        self.assertEqual(r.status_code, 200)

    def test_2_browser_title_contains_app_name(self):
        self.assertIn('The World Needs Another Task Manager!', self.driver.title)

    def test_3_tasks_entry(self):
        r = requests.get(E2ETests.API_URL + "/tasks_entry.html")
        self.assertEqual(r.status_code, 200)

    def test_4_tasks_view(self):
        r = requests.get(E2ETests.API_URL + "/tasks_view.html")
        self.assertEqual(r.status_code, 200)

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
