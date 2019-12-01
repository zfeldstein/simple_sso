import click
import os.path
import configparser
import requests
from tabulate import tabulate

from requests.auth import HTTPBasicAuth
from os.path import expanduser

# Don't allow user to change config files
home_dir = expanduser("~")
# This is ~/.ssso
config_path = '{}/.ssso'.format(home_dir)
# This is ~/.ssso/config
config_file = '{}/config'.format(config_path)

def api_auth(conn_info):
    response = requests.get(
        conn_info["server_url"],
        auth=HTTPBasicAuth(conn_info['user_name'], conn_info['passwd'])
    )


def config_reader(conf):
    config = configparser.ConfigParser()
    config.read(conf)
    auth_info = {
        "username" : config['DEFAULT']['username'],
        "passwd" : config['DEFAULT']['passwd'],
        "server_url" : config['DEFAULT']['server_url'],
        "ssh_key" : config['DEFAULT']['ssh_key'],
        "expiration" : config['DEFAULT']['expiration'],
        "email": config['DEFAULT']['email']
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
    default=90,
    help='Password for user, leave blank for random'
)
@click.option(
    '--email',
    '-a',
    default=None,
    help='Email address for user'
)
# Use config values by default override with CLI
def main(ctx, user, passwd, ssh_key,  expiration, email):
    if not os.path.exists(config_file):
        ctx.invoke(new_config)
    auth_info = config_reader(config_file)
    server_url = "{}/api".format(auth_info['server_url'])

    ctx.obj = {
        "username": auth_info['username'],
        "passwd": auth_info['passwd'],
        "ssh_key": auth_info['ssh_key'],
        "expiration": auth_info['expiration'],
        "email": auth_info['email'],
        "server_url" : server_url
    }

@main.command()
@click.pass_context
def add(ctx):
    # click.echo("Adding user %s" % ctx.obj['user'])
    # curl -i -X POST
    # -H "Content-Type: application/json"
    # -d '{"username":"migu2ell","password":"pythlon"}' http://127.0.0.1:5000/api/users
    click.echo(ctx.obj['auth_info']['user_name'])

@main.command()
@click.pass_context
def delete(ctx):
    pass

@main.command()
@click.pass_context
def list(ctx):
    url = "{}/users".format(ctx.obj['server_url'])
    click.echo("Listing Users")
    response = requests.get(
        url,
        auth=HTTPBasicAuth(
            ctx.obj['username'],
            ctx.obj['passwd']
        )
    )
    if response.status_code == 401:
        click.echo("Only admins can list users")
        exit()
    if not response.status_code == 201:
        click.echo(
            "An error occured, http return code {}".format(
                response.status_code
            )
        )
    response = response.json()
    resp_table = []
    for user in response:
        resp_table.append(
            [
                user['id'] or "None", # Probably a better way to do this lol
                user['username'] or "None",
                user['email_addr'] or "None",
                user['expiration'] or "None",
                user['is_admin'] or "None",
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

@main.command()
@click.pass_context
def update(ctx):
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