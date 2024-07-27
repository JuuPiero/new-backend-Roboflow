import json
import os
from sqlalchemy.orm import Session
from flask import Flask, request, jsonify
from flask_cors import CORS


from DB import *
from entities.User import User
from entities.Image import Image
from entities.Project import Project
from entities.Version import Version 

from helper.ultils import *

Base.metadata.create_all(bind=engine)
db = SessionLocal()

app = Flask(__name__)
CORS(app)

# user = User(email='test1@test.com', first_name='test', last_name='test', password='123456')
# print(to_dict(Project.DeleteById(db, 1)))
DBController().show_tables()
# created_user = User.Create(db, user)
# project = Project(user_id=1, project_name='tét2 project', project_type='object dê', classes='[]')
# Project.Create(db, project)
# project = Project.GetById(db, 1)
# images = []
# for image in project.images:
#     images.append(to_dict(image))
# print(images)
# user = User.GetById(db ,1)
# image = Image(project_id=1, type="png", image_name="image.png", image_path="ssss/ss/image.png")
# Image.Create(db, image)

# for p in user.projects:
#     print(to_dict(p))
# print(to_dict(User.Update(db, 1, {
#     'password' : 'lam123',
#     'first_name': 'Lâm'
#     # 'email': 'lam@gmail.com'
# })))

@app.route('/', methods=['POST'])
def check_health():
    return jsonify({'status': 'OK'})

@app.route('/api/login', methods=['POST'])
def onUserLogin():
    credentials = request.json
    user = User.GetByEmail(db, credentials['email'])
    emailValid = False
    passwordValid = False
    if user:
        emailValid = user.email == credentials['email']
        passwordValid = user.password == credentials['password']
    if not emailValid:
        return jsonify({'error': 'Invalid email', 'type': 'email'})
    elif not passwordValid:
        return jsonify({'error': 'Invalid password', 'type': 'password'})
    else:
        user = to_dict(user)
        user['_id'] = user['id']
        return jsonify(user)
    
@app.route('/api/register', methods=['POST'])
def onUserRegister():
    data = request.json
    user = User(email=data['email'], first_name=data['first_name'], last_name=data['last_name'], password=data['password'])
    try:
        User.Create(db, user)
        return jsonify({'status': 'OK'})
    except:
        return jsonify({'error': 'Email already exists!'})

@app.route('/api/get_all_projects', methods=['POST'])
def getAllProjects():
    user_id = request.json['user_id']
    user = User.GetById(db, user_id)
    projects = []
    for p in user.projects:
        project = to_dict(p)
        project['_id'] = project['id']
        projects.append(project)
    return jsonify({'projects': projects})

@app.route('/api/get_project', methods=['POST'])
def onGetProject():
    project_id = request.json['project_id']
    project = to_dict(Project.GetById(db, project_id))
    project['classes'] = json.loads(project['classes'])
    project['_id'] = project['id']
    return jsonify({'project': project})

@app.route('/api/create_project', methods=['POST'])
def onCreateProject():
    data = request.json
    print(data)
    project = Project.Create(db, Project(user_id=data['user_id'], project_name=data['project_name'], project_type=data['project_type'], classes='[]'))
    return jsonify({'project_id': project.id})

@app.route('/api/delete_project', methods=['POST'])
def onDeleteProject():
    project_id = request.json['project_id']
    Project.DeleteById(db, project_id)
    return jsonify({'project_id': project_id})

@app.route('/api/add_project_classes', methods=['POST'])
def addProjectClasses():
    data = request.json
    project_id = data['project_id']
    project = Project.GetById(db, project_id)
    updateClasses = json.loads(project.classes) + data['classes_list']
    Project.Update(db, project_id, {
        'classes': json.dumps(updateClasses)
    })
    return jsonify({'project_id': project_id})


# Image item endpoints
@app.route('/api/get_image_items/project_version', methods=['POST'])
def getImagesByProjectVersion():
    project_id = request.json['project_id']
    project = Project.GetById(db, project_id)
    images = []
    for image in project.images:
        images.append(to_dict(image))
    return jsonify(images)



@app.route('/api/upload_data', methods=['POST'])
def onUploadImages():
    files = request.files.getlist('files_obj[]')
    data = request.form.to_dict()
    
    for file in files:
        filename = generate_name(os.path.splitext(os.path.basename(file.filename))[0])
        exist = Image.GetByName(db, filename)
        if not exist:
            img_paths = save_image(file, filename)
            Image.Create(db, Image(project_id=data['project_id'], type=file.mimetype, image_name= filename, image_path=img_paths['local'], label_path="", version_ids="[]")) 
    return jsonify({'project_id': str(data['project_id'])})


# if __name__ == '__main__':
#     app.run(port=8080, debug=True, host='0.0.0.0', threaded=True)