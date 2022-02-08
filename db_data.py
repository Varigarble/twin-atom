import mongoengine
from datetime import datetime

class Data(mongoengine.Document):
    client = mongoengine.StringField(required=True)
    product = mongoengine.StringField()
    subs_start_date = mongoengine.DateTimeField(default=datetime.utcnow)
    subs_end_date = mongoengine.DateTimeField(default=datetime.utcnow)
    task_in_progress = mongoengine.BooleanField(default=False)
    task_id = mongoengine.ObjectIdField()  # ObjectId of Tasks collection document
    