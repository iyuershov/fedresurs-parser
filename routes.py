import redis

from rq import Queue
from rq.registry import FinishedJobRegistry, StartedJobRegistry
from rq.job import Job
from flask import Flask, request, abort, jsonify
from app.main.service import get_messages

app = Flask(__name__)

connection = redis.Redis(host='redis', port=6379)
queue = Queue(connection=connection)


@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'keyword' in request.json:
        abort(400)

    keyword = request.json['keyword']

    code = None
    name = None

    if keyword.isdigit():
        code = keyword
    else:
        name = keyword

    if (code is not None) or (name is not None):
        organization = dict(code=code, name=name)

        with app.app_context():
            task = queue.enqueue(get_messages, organization)

        return jsonify({'task': task.id}), 201

    return abort(400)


@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    if Job.exists(task_id, connection=connection):
        job = Job.fetch(task_id, connection=connection)
        if job.get_status() == "finished":
            return job.result
        else:
            return job.get_status()
    else:
        return "No such task."


@app.route('/tasks', methods=['GET'])
def get_task_list():
    tasks = []
    registry = StartedJobRegistry('default', connection=connection)
    job_ids = registry.get_job_ids()
    for job_id in job_ids:
        j = Job.fetch(job_id, connection=connection)
        job_info = dict(guid=j.id, status=j.get_status())
        tasks.append(job_info)

    finished = []
    finished_registry = FinishedJobRegistry('default', connection=connection)
    finished_job_ids = finished_registry.get_job_ids()
    for finished_job_id in finished_job_ids:
        j = Job.fetch(finished_job_id, connection=connection)
        finished_info = {"guid": j.id}
        finished.append(finished_info)

    return jsonify({
        "tasks": tasks,
        "finished": finished
    }), 201


if __name__ == '__main__':
    app.run()
