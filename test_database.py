from unittest.mock import patch
from dataclasses import asdict
from datetime import datetime
import unittest
import pymongo
import database
import db_tasks

@patch('database.DEFAULT_DB_NAME', 'test_task_mgr')
class test_db_connect(unittest.TestCase):

    def setUp(self):
        test_tasks = db_tasks.Tasks(
            name = "test task name",
            creators = ["Varigarble"],
            description = "Test Task Description",
            start_date = datetime(2021, 11, 11),
            completion_date = datetime(2022, 2, 9),
            due_date = datetime(2022, 2, 9),
            assigned_to = "RDRR",
        )

        client = pymongo.MongoClient()
        db = client['test_task_mgr']
        db.tasks.insert_one(asdict(test_tasks))


    def tearDown(self) -> None:
        client = pymongo.MongoClient()
        db = client['test_task_mgr']
        db.tasks.delete_many({'name': 'test task name'})
        db.tasks.delete_many({'assigned_to': 'QQQ'})  # clean up test_add_task_to_db()


    def test_connect_db(self):
        expected = 'test_task_mgr'
        self.assertEqual(expected, database.connect_db().name)


    def test_add_task_to_db(self):
        test_task_list = list()
        task = db_tasks.Tasks(
            name = "test create task",
            creators = ["VG"],
            description = "Test Create Task Description",
            start_date = datetime(2021, 11, 11),
            completion_date = datetime(2022, 2, 9),
            due_date = datetime(2022, 2, 9),
            assigned_to = "QQQ",
        )
        test_task_list.append(task)
        database.add_task_to_db(test_task_list)

        client = pymongo.MongoClient()
        db = client['test_task_mgr']
        self.assertEqual('QQQ', db.tasks.find({'name': 'test create task'})[0]['assigned_to'])


    def test_view_all_tasks(self):
        self.assertTrue(len(database.view_all_tasks()) >= 1)
        # clear database and assert empty
        client = pymongo.MongoClient()
        db = client['test_task_mgr']
        db.tasks.delete_many({'name': 'test task name'})
        self.assertTrue(len(database.view_all_tasks()) == 0)


    def test_get_all_creators(self):
        self.assertTrue(len(database.get_all_creators()) >= 1)
        self.assertEqual(["Varigarble"], database.get_all_creators())
        # clear database and assert empty
        client = pymongo.MongoClient()
        db = client['test_task_mgr']
        db.tasks.delete_many({'name': 'test task name'})
        self.assertTrue(len(database.get_all_creators()) == 0)


    def test_view_all_tasks_by_creators(self):
        self.assertEqual("RDRR", database.view_all_tasks_by_creators("Varigarble")[0]['assigned_to'])


    def test_create_task(self):
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ('test name', 'test creators', '', '', '', '', '', '', '', '')
            test_object = database.create_task()
            self.assertEqual(['test creators'], test_object.creators)


if __name__ == '__main__':
    unittest.main()
