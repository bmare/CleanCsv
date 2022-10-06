import os

import click, psycopg2
from .commands import configure, createdb
from definitions import CONFIG_FILE

@click.group(chain=True)
@click.option('--user', default=f"{os.environ.get('USER')}", help='PostgreSQL database user',
              prompt='Please enter the PostgreSQL database user')
@click.option('--password', default='password', help='PostgreSQL database password',
              hide_input=True, prompt='Please enter the PostgreSQL database password')
@click.pass_context
def cli(ctx, user, password):
    try:
        ctx.obj = {'user': user, 'password': password}
        ctx.obj.update(json.load(open(CONFIG_FILE))) #add config variables to context
        connection = connect_db(**ctx.obj)
    except (json.JSONDecodeError, psycopg2.Error) as e:
        click.echo("""It appears the database connection hasn't been configured. Try Running cleancsv cli configure""")
        sys.exit(1)


cli.add_command(configure)
cli.add_command(createdb)



