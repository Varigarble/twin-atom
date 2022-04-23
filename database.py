from dataclasses import asdict
import pymongo
import db_tasks
import db_data


DEFAULT_DB_NAME = "task_mgr"


def connect_db(db_name=None):
    client = pymongo.MongoClient()
    if db_name:
        db = client[db_name]
    else:
        db = client[DEFAULT_DB_NAME]
    return db


def view_all_tasks() -> list():
    db = connect_db()
    query = db.tasks.find()
    tasks = []
    for each in query:
        tasks.append(each)
    return tasks


def get_all_creators() -> list():
    db = connect_db()
    query = db.tasks.distinct("creators")
    creators = [""]
    for each in query:
        creators.append(each)
    return creators


def view_all_tasks_by_creators(creator_name: str) -> list():
    db = connect_db()
    query = db.tasks.find({"creators" : creator_name})
    stuff = []
    for each in query:
        stuff.append(each)
    return stuff


task_list = list()


def create_task():
    # Collect user input & create Task class instance
    class_fields = list(db_tasks.Tasks.__annotations__.keys())
    task_create = dict()
    for field in class_fields:
        task_create[field] = input(fr"{field}: ")  # TODO: input from Flask
    task_create['creators'] = [task_create['creators']]
    task_classed = db_tasks.Tasks(**task_create)
    task_list.append(task_classed)
    return task_classed


def add_task_to_db(task_list_items):
    db = connect_db()
    for item in task_list_items:
        db.tasks.insert_one(asdict(item))


def delete_task(unwanted_task):
    # users w/out deletion privilege update task w/ delete request
    db = connect_db()
    db.tasks.update_one(unwanted_task, {'$set': {'marker': 'delete'}})


def update_task():
    pass


def view_all_data():
    db = connect_db()
    query = db.data.find()
    data = []
    for each in query:
        data.append(each)
    return data


def view_one_data(criteria):
    db = connect_db()
    query = db.data.find_one(criteria)
    return query


def createdata():
    # # Collect admin input & create Task class instance - restricted access
    with db_data.mongoengine.connect(db="task_mgr"):
        # db = client["task_mgr"]
        data = db_data.Data(client = "test_data_1")
        data.product = ["GC"]
        data.subs_start_date = "1/1/2020"
        data.subs_end_date = "1/1/2021"
        data.save()
        # db.tasks.insertOne({data_1})


def deletedata(to_delete):
    # admin/restricted access, warning message
    # users w/out delete privilege should update task w/ delete request
    pass


def updatedata():
    pass


if __name__ == "__main__":
    pass
