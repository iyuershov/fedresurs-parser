import redis

from rq import Queue
from rq.job import Job
from flask import Flask, request
from app.service import get_messages

app = Flask(__name__)

connection = redis.Redis()
queue = Queue(connection=connection)


@app.route('/create_task', methods=['GET'])
def create_task():
    # Параметры задаются в адресной строке
    code = request.args.get('code')
    name = request.args.get('name')

    if (code is not None) or (name is not None):
        organization = dict(code=code, name=name)

        with app.app_context():
            task = queue.enqueue(get_messages, organization)

        return f"Task {task.id} created at {task.enqueued_at}"

    return "Wrong parameters"


@app.route('/get_task/<id>', methods=['GET'])
def get_task(id):
    if Job.exists(id,connection=connection):
        job = Job.fetch(id, connection=connection)
        if job.get_status() == "finished":
            return job.result
        else:
            return job.get_status()
    else:
        return "No such task."


if __name__ == '__main__':
    app.run()
