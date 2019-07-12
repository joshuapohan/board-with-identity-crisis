import os
import json
from functools import wraps
from flask import make_response, request, send_from_directory, url_for, session, redirect
from app import app
from model.models import TasksContainer, Task, ConfigTask, User, TaskSession

def set_cors_header(response):
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS,PUT,DELETE"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"

def login_required(f):
    """
        Decorator for routes requiring login
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" in session:
            cur_user = User.get_by_username(session["username"])
            if cur_user:
                return f(*args, **kwargs)
            else:
                return redirect(url_for("login_page"))
        else:
            return redirect(url_for("login_page"))
    return decorated_function
        

@app.route('/')
@login_required
def index():
    #check if logged in, if not redirect to login page
    return send_from_directory(os.path.join('.', 'static'), 'index.html')

@app.route('/register', methods=['POST'])
def register():
    user_ins = json.loads(request.data)
    is_name_taken = User.get_by_username(user_ins["username"]) is not None
    if not is_name_taken:
        new_user = User(None, user_ins["username"], user_ins["password"], user_ins["email"], False)
        new_user.save()
        session["username"] = user_ins["username"]
        return new_user.to_json()
    else:
        return redirect(url_for("login_page"))

@app.route('/login', methods=['POST'])
def login():
    user_ins = json.loads(request.data)
    cur_user = User.get_by_username(user_ins["username"])
    if cur_user.is_password_valid(user_ins["password"]):
        session["username"] = user_ins["username"]
        return cur_user.to_json()
    else:
        return json.dumps({"Error Message":"Wrong username/password"})

@app.route('/newsession', methods=['POST'])
@login_required
def new_session():
    if "username" in session:
        username = session["username"]
        cur_user = User.get_by_username(username)
        if cur_user:
            session_json = json.loads(request.data)
            new_session = TaskSession(None, session_json['session_name'])
            new_session.save()
            new_session.add_user(cur_user, new_session)
            return json.dumps({"_id":new_session._id, "name":new_session.name})
        else:
            return json.dumps({"Error Message":"Invalid session, please login"})
    else:
        return json.dumps({"Error Message":"Please login first"})


@app.route('/login',  methods=['GET'])
def login_page():
    #basedir = os.path.abspath(os.path.dirname(__file__))
    #return str(os.path.join(basedir,'static'))
    return send_from_directory(os.path.join('.', 'static'), 'login.html')

@login_required
def logout():
    session.pop("username", None)
    return redirect(url_for("login_page"))

@app.route('/sessions', methods=['GET'])
@login_required
def get_sessions():
    if "username" in session:
        session_list = []
        username = session["username"]
        cur_user = User.get_by_username(username)
        session_ids = cur_user.get_my_sessions()
        for _id in session_ids:
            cur_session = TaskSession.get_by_id(_id)
            if cur_session:
                session_list.append({'_id':cur_session._id,'name':cur_session.name})
        return json.dumps({
            'sessions': session_list
        })
    else:
        return json.dumps({"Error Message":"Please login first"})

@app.route('/session/<session_id>', methods=['GET'])
@login_required
def get_session(session_id):
    """
    if "username" in session:
        is_authorized = False
        username = session["username"]
        cur_user = User.get_by_username(username)
        authorized_user = User.get_user_for_session()
        
        if cur_user:
            if authorized_user:
                if authorized_user._id == cur_user._id:
                    is_authorized = True
            else:
                cur_user.save_session(session_id)
                is_authorized = True

            if is_authorized: 
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
            else:
                return "Not authorized" 
    """
    #return redirect(url_for("login_page"))
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
        if "username" in session:
            username = session["username"]
            cur_user = User.get_by_username(username)
            if cur_user and cur_user.is_authorized_for_task(int(task["_id"].replace("task",""))):
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
@login_required
def update_task():
    obj_ins = json.loads(request.data)
    res_obj = db_update_task(obj_ins)
    session_response = make_response(res_obj)
    set_cors_header(session_response)
    return session_response

@app.route('/task', methods=['DELETE'])
@login_required
def delete_task():
    obj_ins = json.loads(request.data)
    Task.delete_by_id(obj_ins["_id"].replace("task",""))
    session_response = make_response({"Deleted": obj_ins["id"]})
    set_cors_header(session_response)
    return session_response

def db_update_container(container):
    #if "username" in session:
    #    cur_user = User.get_by_username(session["username"])
    #    session_ids = cur_user.get_my_sessions()
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
@login_required
def update_container():
    obj_ins = json.loads(request.data)
    res_obj = db_update_container(obj_ins)
    session_response = make_response(res_obj)
    set_cors_header(session_response)
    return session_response

# Custom static data
@app.route('/<path:filename>')
def custom_static(filename):
    return send_from_directory('/client/client-board/build', 'index.html')
