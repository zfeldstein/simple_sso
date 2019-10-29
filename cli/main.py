import click
import os.path
import configparser
from pathlib import Path

def config_reader(conf):
    config = configparser.ConfigParser()
    config.read(conf)
    auth_info = {
        "user_name" : config['DEFAULT']['user_name'],
        "passwd" : config['DEFAULT']['passwd'],
        "server_url" : config['DEFAULT']['url']
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
def main(ctx, user, passwd, ssh_key,  expiration, email, config="/.ssso"):
    conf_dir= str(Path.home()) + config
    conf_file = conf_dir + "/config"
    auth_info = config_reader(conf_file)
    ctx.obj = {
        "user": user,
        "passwd": passwd,
        "ssh_key": ssh_key,
        "expiration": expiration,
        "email": email,
        "config": conf_dir,
        "auth_info": auth_info
    }

@main.command()
@click.pass_context
def add(ctx):
    # click.echo("Adding user %s" % ctx.obj['user'])
    click.echo(ctx.obj['auth_info']['user_name'])

@main.command()
@click.pass_context
def delete(ctx):
    pass

@main.command()
@click.pass_context
def list(ctx):
    pass

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
def config(ctx):
    config_path = ctx.obj["config"] + "/config"
    if not os.path.exists(config_path):
        #Create .ssso dir
        if not os.path.exists(ctx.obj["config"]):
            os.mkdir(ctx.obj["config"])
        config = configparser.ConfigParser()
        config['DEFAULT'] = {
            "user_name" : click.prompt("Enter ssso Username"),
            "passwd" : click.prompt("Enter ssso password"),
            "url" : click.prompt("Enter ssso URL")
        }
        with open(config_path, 'w') as configfile:
            config.write(configfile)

if __name__ == '__main__':
    main()