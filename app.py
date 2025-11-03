import bcrypt
from flask import Flask, request, jsonify
from models.user import User
from config.database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required


app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/flaskcrud'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view='login'

#view login

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({'message':'Login Successful'}), 200
        else:
            return jsonify({'message':'Invalid Credentials'}), 401
    return jsonify({'message':'Username and Password required'}), 400


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message':'Logout Successful'}), 200


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    hashdpassword = bcrypt.hashpw(str.encode(password), bcrypt.gensalt());

    if username and password:
        if User.query.filter_by(username=username).first():
            return jsonify({'message':'Username already exists'}), 409
        new_user = User(username=username, password=hashdpassword)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message':'User created successfully'}), 201
    return jsonify({'message':'Username and Password required'}), 400

@app.route('/user/<int:id_user>', methods=['GET'])
@login_required
def get_user(id_user):
    user = User.query.get(id_user)
    if user:
        return jsonify({'id': user.id, 'username': user.username}), 200
    return jsonify({'message':'User not found'}), 404

@app.route('/user/<int:id_user>', methods=['PUT'])
@login_required
def update_user(id_user):
    data= request.get_json()
    user = User.query.get(id_user)
    if user:
        username = data.get('username')
        password = data.get('password')


        if user.id != current_user().id and current_user.role == 'user':
            return jsonify({'message':'Unauthorized to update this user'}), 403

        if username and user.id != current_user().id:
            user.username = username
        if password:
            hashdpassword = bcrypt.hashpw(str.encode(password), bcrypt.gensalt());
            user.password = hashdpassword
        db.session.commit()
        return jsonify({'message':'User updated successfully'}), 200
    return jsonify({'message':'User not found'}), 404

@login_required
@app.route('/user', methods=['GET'])
def show_user():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify(user_list), 200


@app.route('/user/<int:id_user>', methods=['DELETE'])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)

    if id_user==current_user.id:
        return jsonify({'message':'You cannot delete your own account'}), 403

    if current_user.role == 'user':
        return jsonify({'message':'Unauthorized to delete this user'}), 403


    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message':'User deleted successfully'}), 200
    return jsonify({'message':'User not found'}), 404

@app.route('/hello-world', methods=['GET'])
def hello_world():
    return 'Hello, World!', 200

if __name__ == '__main__':
    app.run(debug=True)
