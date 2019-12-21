import click
import os.path
import configparser
import requests
import json
from tabulate import tabulate

from requests.auth import HTTPBasicAuth
from os.path import expanduser

# Don't allow user to change config files
home_dir = expanduser("~")
# This is ~/.ssso
config_path = '{}/.ssso'.format(home_dir)
# This is ~/.ssso/config
config_file = '{}/config'.format(config_path)

#
# Validate response code from API
#
def check_response(response):
    if response.status_code == 401:
        click.echo("Unauthorized Access")
        exit()
    if not response.status_code >= 200 < 300:
        click.echo(
            "An error occured, http return code {}".format(
                response.status_code
            )
        )
        exit()
    return response
#
# Requests wrapper
#
def api_call(ctx, url, method='get', user_hash={}):
    methods = ['get', 'post', 'put', 'delete', 'head']
    if method.lower() not in methods:
        click.echo("{} is not a valid REST method".format(method))
        exit(1)
    auth = HTTPBasicAuth(
            ctx.obj['username'],
            ctx.obj['passwd']
        )
    # GET requests
    if method.lower() == 'get':
        response = requests.get(url, auth=auth )
    # POST requests (user add)
    if method.lower() == 'post':
        response = requests.post(url, auth=auth, json=user_hash)
    if method.lower() == 'delete':
        response = requests.delete(url, auth=auth)
    if method.lower() == 'put':
        response = requests.put(url, auth=auth, json=user_hash)

    return (check_response(response))
#
# Read Config File set auth hash
#
def config_reader(conf):
    config = configparser.ConfigParser()
    config.read(conf)
    auth_info = {
        "username" : config['DEFAULT']['username'],
        "passwd" : config['DEFAULT']['passwd'],
        "server_url" : config['DEFAULT']['server_url'],
        "ssh_key" : config['DEFAULT']['ssh_key'],
        "expiration" : config['DEFAULT']['expiration'],
        "email_addr": config['DEFAULT']['email']
    }
    return auth_info

@click.group()
@click.pass_context
@click.option(
    '--user',
    '-u',
    help='Name of user to create'
)
@click.option(
    '--passwd',
    '-p',
    default=None,
    help='Password for user, leave blank for random'
)
@click.option(
    '--ssh_key',
    '-s',
    default=None,
    help='Public ssh_key to upload'
)
@click.option(
    '--expiration',
    '-e',
    default=None,
    help='Password for user, leave blank for random'
)
@click.option(
    '--email',
    '-m',
    default=None,
    help='Email address for user'
)
@click.option(
    '--admin',
    '-a',
    is_flag=True,
    help='Use -a to create an admin user'
)
# Use config values by default override with CLI
def main(ctx, user, passwd, ssh_key,  expiration, email, admin):
    if not os.path.exists(config_file):
        ctx.invoke(new_config)
    # username/password info for API calls
    # is in auth_info. Params to method are
    # CLI flags (aka users to be created )
    auth_info = config_reader(config_file)
    server_url = "{}/api".format(auth_info['server_url'])
    user_hash = {
        "username": user,
        "passwd": passwd,
        "ssh_key": ssh_key,
        "expiration": expiration,
        "email_addr": email,
        "is_admin": admin
    }
    # TODO
    # Removed keys w/ undefined values
    # Find a better way to do this
    user_hash = {k: v for k, v in user_hash.items() if v is not None}
    ctx.obj = {
        "username": auth_info['username'],
        "passwd": auth_info['passwd'],
        "ssh_key": auth_info['ssh_key'],
        "expiration": auth_info['expiration'],
        "email_addr": auth_info['email_addr'],
        "server_url" : server_url,
        "user_hash": user_hash
    }

#
# Delete Users
#
@main.command()
@click.pass_context
def delete(ctx):
    username = ctx.obj['user_hash']['username']
    url = "{}/users/{}".format(
        ctx.obj['server_url'],
        username
    )
    click.echo("Deleting User {}".format(username))
    response = api_call(ctx, url, method='delete')
    click.echo(response.text)

#
# Add users
#
@main.command()
@click.pass_context
def add(ctx):
    url = "{}/users".format(ctx.obj['server_url'])
    click.echo("Adding user ")
    click.echo(ctx.obj['user_hash'])
    user_hash = ctx.obj['user_hash']
    response = api_call(ctx, url, method='post',user_hash=user_hash)
    print(response.text)
#
# Update User
#
@main.command()
@click.pass_context
def update(ctx):
    username = ctx.obj['user_hash']['username']
    url = "{}/users/{}".format(
        ctx.obj['server_url'],
        username
    )
    click.echo("Updating User {}".format(username))
    user_hash = ctx.obj['user_hash']
    response = api_call(ctx, url, method='put', user_hash=user_hash)
    print(response.text)

#
# List users
#
@main.command()
@click.pass_context
def list(ctx):
    url = "{}/users".format(ctx.obj['server_url'])
    click.echo("Listing Users")
    response = api_call(ctx, url)
    response = response.json()
    resp_table = []
    for user in response:
        resp_table.append(
            [
                user['id'] or "None", # Probably a better way to do this lol
                user['username'] or "None",
                user['email_addr'] or "None",
                user['expiration'] or "None",
                user['is_admin'] or "False",
                user['ssh_key'] or "None"
            ]
        )
    click.echo(tabulate(resp_table, headers=[
        "user_id",
        "username",
        "email",
        "key expiration",
        "is_admin",
        "ssh_key"
    ]))

@main.command()
@click.pass_context
def info(ctx):
    pass

# Create a ~/.ssso/config and use for auth with server
@main.command()
@click.pass_context
def new_config(ctx):
    if not os.path.exists(config_file):
        #Create .ssso dir
        if not os.path.exists(config_path):
            os.mkdir(config_path)
        config = configparser.ConfigParser()
        config['DEFAULT'] = {
            "username" : click.prompt("Enter ssso Username"),
            "passwd" : click.prompt("Enter ssso password"),
            "server_url" : click.prompt("Enter ssso server URL"),
            "ssh_key": click.prompt("Enter path to public ssh_key"),
            "expiration": click.prompt("Enter time key expires in days"),
            "email" : click.prompt("Enter your email address")
        }
        with open(config_file, 'w') as configfile:
            config.write(configfile)

if __name__ == '__main__':
    main()