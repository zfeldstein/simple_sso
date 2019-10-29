import click
import os.path
import configparser
from pathlib import Path


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
    config= str(Path.home()) + config
    ctx.obj = {
        "user": user,
        "passwd": passwd,
        "ssh_key": ssh_key,
        "expiration": expiration,
        "email": email,
        "config": config
    }

@main.command()
@click.pass_context
def add(ctx,zack):
    click.echo("Adding user %s" % ctx.obj['user'])

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