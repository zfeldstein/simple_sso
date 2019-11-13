import os
from app import app, auth, db
from flask import abort, request, jsonify, g, url_for
from app.models import Admins, Users



@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = Admins.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = Admins.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/api/admin/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    ssh_key = request.json.get('ssh_key')
    expiration = request.json.get('expiration')
    email_addr = request.json.get('email_addr')
    if username is None or password is None:
        abort(400)# missing arguments
    if Admins.query.filter_by(username=username).first() is not None:
        abort(400) # existing user
    user = Admins(username=username)
    user.hash_password(password)
    user.expiration
    user.ssh_key
    user.email_addr
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})


@app.route('/api/admin/<int:id>')
def get_user(id):
    user = Admins.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})


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
    if not os.path.exists('d3.sqlite'):
        db.create_all()
    app.run(debug=True)
