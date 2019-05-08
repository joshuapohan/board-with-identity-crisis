from model.models import TasksContainer, Task, User
from config import Config

def populateDB():
	"""
		For testing and debugging purposes
	"""
	Config.load_config()
	task1 = Task(None,1, "Make full maps", "Map variables and create relations table with foreign keys", None)
	task1.save()
	task2 = Task(None,1, "Make coffee", "make coffee and drink it", None)
	task2.save()
	task3 = Task(None,1, "Buy present", "buy present for april", None)
	task3.save()
	container1 = TasksContainer(None, 1, "todo")
	container1.add_task(task2, task3)
	container1.save()
	container2 = TasksContainer(None, 1, "testing")
	container2.add_task(task1)
	container2.save()
	container3 = TasksContainer.get_by_id(container1._id)
	container3.print_container()
	task3.detail = "Updated details"
	task3.save()
	container3._name = "Updated name"
	container3.save()
	user = User(None, 'admin','admin','admin@test.com',True)
	user.save()
    
populateDB()
