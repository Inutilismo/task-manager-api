from flask import request, jsonify
from flask_restx import Namespace, Resource, fields

api = Namespace("tasks", description="Task operations")

task_model = api.model(
    "Task",
    {
        "id": fields.Integer(readOnly=True, description="The task unique identifier"),
        "name": fields.String(required=True, description="The task name"),
        "description": fields.String(description="The task description"),
    },
)

tasks_response_model = api.model(
    "TasksResponse",
    {
        "tasks": fields.List(fields.Nested(task_model)),
    },
)

@api.route("/")
class TaskList(Resource):
    @api.doc("list_tasks")
    @api.marshal_list_with(task_model)
    def get(self):
        """List all tasks"""
        from database import Task
        tasks = Task.query.all()  
        return [t.as_dict() for t in tasks]

    @api.doc("create_task")
    @api.expect(task_model)
    @api.marshal_with(task_model, code=201)
    def post(self):
        """Create a new task"""
        from database import db_session, Task
        data = request.json
        task = Task(name=data["name"], description=data.get("description", ""))
        db_session.add(task)
        db_session.commit()
        return task.as_dict(), 201


@api.route("/<int:task_id>")
@api.param("task_id", "The task identifier")
class Task(Resource):
    @api.doc("get_task")
    @api.marshal_with(task_model)
    def get(self, task_id):
        """Fetch a task by ID"""
        from database import Task
        task = Task.query.get(task_id)
        if not task:
            api.abort(404, "Task not found")
        return task.as_dict()

    @api.doc("update_task")
    @api.expect(task_model)
    @api.marshal_with(task_model)
    def put(self, task_id):
        """Update a task"""
        from database import Task, db_session
        task = Task.query.get(task_id)
        if not task:
            api.abort(404, "Task not found")
        data = request.json
        task.name = data["name"]
        task.description = data.get("description", "")
        db_session.commit()
        return task.as_dict()

    @api.doc("delete_task")
    def delete(self, task_id):
        """Delete a task"""
        from database import Task, db_session
        task = Task.query.get(task_id)
        if not task:
            api.abort(404, "Task not found")
        db_session.delete(task)
        db_session.commit()
        return {"message": "Task deleted"}, 200
