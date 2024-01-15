from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson import ObjectId  # Import ObjectId for proper conversion

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://mongo:27017/notedb'
mongo = PyMongo(app)

@app.route('/')
def index():
    notes = mongo.db.notes.find()
    return render_template('main.html', notes=notes)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        mongo.db.notes.insert_one({'title': title, 'content': content})
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/delete/<note_id>', methods=['GET'])
def delete(note_id):
    mongo.db.notes.delete_one({'_id': ObjectId(note_id)})
    return redirect(url_for('index'))

@app.route('/read/<note_id>', methods=['GET'])
def read(note_id):
    note = mongo.db.notes.find_one({'_id': ObjectId(note_id)})
    return render_template('read.html', note=note)

@app.route('/update/<note_id>', methods=['GET', 'POST'])
def update(note_id):
    note = mongo.db.notes.find_one({'_id': ObjectId(note_id)})

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        mongo.db.notes.update_one({'_id': ObjectId(note_id)}, {'$set': {'title': title, 'content': content}})
        return redirect(url_for('index'))

    return render_template('update.html', note=note)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

