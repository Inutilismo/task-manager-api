from flask import request
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
    @api.param("page", "Page number", required=False, default=1)
    @api.param("page_size", "Number of tasks per page", required=False, default=10)
    def get(self):
        """List all tasks with pagination"""
        from app.database import Task
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 10))
        tasks_query = Task.query
        tasks = tasks_query.offset((page - 1) * page_size).limit(page_size).all()
        return [t.as_dict() for t in tasks]

    @api.expect(task_model, validate=True)
    def post(self):
        """Create a new task"""
        from app.database import db_session, Task
        data = request.json
        if not data.get("name"):
            api.abort(400, "The 'name' field is required.")
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
        from app.database import Task
        task = Task.query.get(task_id)
        if not task:
            api.abort(404, "Task not found")
        return task.as_dict()

    @api.doc("update_task")
    @api.expect(task_model)
    @api.marshal_with(task_model)
    def put(self, task_id):
        """Update a task"""
        from app.database import Task, db_session
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
        from app.database import Task, db_session
        task = Task.query.get(task_id)
        if not task:
            api.abort(404, "Task not found")
        db_session.delete(task)
        db_session.commit()
        return {"message": "Task deleted"}, 200
