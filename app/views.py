import os
from app import app, auth, db
from flask import abort, request, jsonify, g, url_for, Response
from app.models import Users, UsersSchema

users_schema = UsersSchema(many=True)

#This method is called for user specific resources
def check_user_permissions(id=0, admin_required=False):
    user = Users.query.filter_by(username=g.user.username).first()
    if user.is_admin:
        return True
    if not admin_required:
        if id == g.user.id:
            return True
    abort(401)

@auth.verify_password
def verify_password(username, password):
    # try to authenticate with username/password
    user = Users.query.filter_by(username=username).first()
    if not user:
        return False
    passwd = user.verify_password(password)
    if not passwd:
        return False
    g.user = user
    return True

@app.route('/api/users/<int:id>', methods=['PUT'])
@auth.login_required
def update_user(id):
    check_user_permissions(id)
    print(request.json)
    user = Users.query.get(id)
    if not user:
        abort(404)
    return jsonify("world")


@app.route('/api/users', methods=['POST'])
@auth.login_required
def new_user():
    check_user_permissions(admin_required=True)
    username = request.json.get('username')
    password = request.json.get('password')
    ssh_key = request.json.get('ssh_key')
    expiration = request.json.get('expiration')
    email_addr = request.json.get('email_addr')
    is_admin = request.json.get('is_admin')
    if username is None or password is None:
        abort(400)# missing arguments
    if Users.query.filter_by(username=username).first() is not None:
        abort(400) # existing user
    user = Users(username=username)
    user.hash_password(password)
    user.expiration
    user.ssh_key
    user.email_addr
    user.is_admin
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201)
    #         {'Location': url_for('get_user', id=user.id, _external=True)})
    return get_user(user.id)

# List users
@app.route('/api/users', methods=['GET'])
@auth.login_required
def get_user():
    check_user_permissions()
    users = Users.query.all()
    return(jsonify(users_schema.dump(users)), 201)

# Delete User
@app.route('/api/users/<int:id>', methods=['DELETE'])
@auth.login_required
def del_user(id):
    if id == 1:
        return( jsonify( {"response": "Can't delete admin account"}), 400)
    check_user_permissions(id, admin_required=True)
    user = Users.query.filter_by(id = id).one()
    db.session.delete(user)
    db.session.commit()
    return(jsonify({"response": "User {} deleted".format(user.username)}), 201)

@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


if __name__ == '__main__':
    # if not os.path.exists('d3.sqlite'):
    #     db.create_all()
    app.run(debug=False)
