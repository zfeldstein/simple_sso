import click



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
def main(ctx, user, passwd, ssh_key,  expiration, email):
    ctx.obj = {
        "user": user,
        "passwd": passwd,
        "ssh_key": ssh_key,
        "expiration": expiration,
        "email": email
    }

@main.command()
@click.pass_context
def add(ctx):
    click.echo("Adding user %s" % ctx.obj['user'])

@main.command()
@click.pass_context
def delete():
    pass

@main.command()
@click.pass_context
def list():
    pass

@main.command()
@click.pass_context
def info():
    pass

@main.command()
@click.pass_context
def update():
    pass

if __name__ == '__main__':
    main()