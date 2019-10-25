import click

@click.command()
@click.argument('filename')
@click.option('--user',  help='Name of user to create')
@click.option('--passwd', default=None,
              help='Password for user, leave blank for random')
@click.option('--ssh_key', default=None,
              help='Public ssh_key to upload')
@click.option('--expiration', "-e", default=90,
              help='Password for user, leave blank for random')
@click.option('--email',  default=None,
              help='Email address for user')

def hello(user, passwd, ssh_key, expiration, email):
    click.echo("Email %s" % expiration)

if __name__ == '__main__':
    hello()