from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydb'
mongo = PyMongo(app)

# Create a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    task = request.json['task']
    is_completed = request.json['is_completed']
    end_date = request.json['end_date']
    task_id = mongo.db.tasks.insert({'task': task, 'is_completed': is_completed, 'end_date': end_date})
    new_task = mongo.db.tasks.find_one({'_id': task_id})
    result = {'task': new_task['task'], 'is_completed': new_task['is_completed'], 'end_date': new_task['end_date']}
    return jsonify({'result': result})

# List all tasks with pagination
@app.route('/tasks', methods=['GET'])
def list_tasks():
    page = int(request.args.get('page', 1))
    page_size = 10
    tasks = []
    for task in mongo.db.tasks.find().skip((page-1)*page_size).limit(page_size):
        tasks.append({'task': task['task'], 'is_completed': task['is_completed'], 'end_date': task['end_date']})
    return jsonify({'tasks': tasks})

# Retrieve a single task by ID
@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    task = mongo.db.tasks.find_one({'_id': ObjectId(id)})
    if task:
        result = {'task': task['task'], 'is_completed': task['is_completed'], 'end_date': task['end_date']}
    else:
        result = 'No task found'
    return jsonify({'result': result})

# Update a task by ID
@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    task = request.json['task']
    is_completed = request.json['is_completed']
    end_date = request.json['end_date']
    mongo.db.tasks.update_one({'_id': ObjectId(id)}, {'$set': {'task': task, 'is_completed': is_completed, 'end_date': end_date}})
    task = mongo.db.tasks.find_one({'_id': ObjectId(id)})
    result = {'task': task['task'], 'is_completed': task['is_completed'], 'end_date': task['end_date']}
    return jsonify({'result': result})

# Delete a task by ID
@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    mongo.db.tasks.delete_one({'_id': ObjectId(id)})
    result = 'Task deleted'
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
