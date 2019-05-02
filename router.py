import json
from flask import make_response, request, send_from_directory
from app import app
from model.models import TasksContainer, Task, ConfigTask

def set_cors_header(response):
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS,PUT,DELETE"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"

@app.route('/')
def index():
    return "Hello World"

@app.route('/session/<session_id>', methods=['GET'])
def get_session(session_id):
    #Retrieve the objects by session
    containers = TasksContainer.get_all_by_session(session_id)
    for cur_container in containers:
        for cur_task in cur_container.my_tasks:
            cur_cfg = ConfigTask.get_by_task_id(cur_task._id)
            if cur_cfg:
                cur_task.color_id = cur_cfg.color_id
    containers_JSON = [container.to_json() for container in containers]
    session_response = make_response(json.dumps(containers_JSON))
    set_cors_header(session_response)
    return session_response

def db_update_task(task):
    if task["_id"] is not None:
        task_dict = None
        cfg_dict = None
        task_db_id = task["_id"].replace("task","")
        cur_task = Task.get_by_id(task_db_id)
        if cur_task:
            cur_task._name = task["_title"]
            cur_task.detail = task["_text"]
            cur_task.save()
            task_dict = cur_task.to_dict()
            cur_cfg = ConfigTask.get_by_task_id(task_db_id)
            if cur_cfg:
                cur_cfg.color_id = int(task["color_id"])
                cur_cfg.save()
                cfg_dict = cur_cfg.to_dict()
            if task_dict is not None and cfg_dict is not None:
                task_dict.update(cfg_dict)
                return json.dumps(task_dict)
    else:
        cur_task = Task(None, task["session_id"], "Default value", "", 0)
        cur_task.save()
        return cur_task.to_json()
    return json.dumps({})

@app.route('/task', methods=['POST'])
def update_task():
    obj_ins = json.loads(request.data)
    res_obj = db_update_task(obj_ins)
    session_response = make_response(res_obj)
    set_cors_header(session_response)
    return session_response

@app.route('/task', methods=['DELETE'])
def delete_task():
    obj_ins = json.loads(request.data)
    Task.delete_by_id(obj_ins["_id"].replace("task",""))
    session_response = make_response({"Deleted": obj_ins["id"]})
    set_cors_header(session_response)
    return session_response

def db_update_container(container):
    if container["_id"] is not None:
        cur_container = TasksContainer.get_by_id(container["_id"])
        cur_container._name = container["_title"]
        cur_container.task_ids = [x["_id"].replace("task","") for x in container["myTasks"]]
        cur_container.save()
    else:
        cur_container = TasksContainer(None, container["session_id"], "Default container")
        cur_container.save()
    if cur_container:
        return cur_container.to_json()
    else:
        return json.dumps({})

@app.route('/container', methods=['POST'])
def update_container():
    obj_ins = json.loads(request.data)
    res_obj = db_update_container(obj_ins)
    session_response = make_response(res_obj)
    set_cors_header(session_response)
    return session_response

# Custom static data
@app.route('/<path:filename>')
def custom_static(filename):
    print("static directory")
    return send_from_directory('/client/client-board/build', 'index.html')