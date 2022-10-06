import os, json
import click
from cleancsv import *

from db import *
# Paths

# Utility Functions
def connect_db(user, password, host, port, database=None):
    if database:
        return psycopg2.connect(user=user, password=password, \
                                      database=database, host=host, port=port)
    else:
        return psycopg2.connect(user=user, password=password, host=host, port=port)




# Cli Commands
@click.group(chain=True)
@click.option('--user', default=f"{os.environ.get('USER')}", help='PostgreSQL database user',
              prompt='Please enter the PostgreSQL database user')
@click.option('--password', default='password', help='PostgreSQL database password',
              hide_input=True, prompt='Please enter the PostgreSQL database password')
@click.option('--config', default=False, help='Configure database name, host, and port.')
@click.pass_context
def cli(ctx, user, password, config):
    if config:
        configure(ctx.params)
    else:
        try:
            ctx.obj = {'user': user, 'password': password}
            ctx.obj.update(load_config()) #add config variables to context
            connection = connect_db(**ctx.obj)
        except (json.JSONDecodeError, psycopg2.Error) as e:
            click.echo("""It appears the database connection hasn't been configured""")
            if click.confirm("Run cleancsv --config?"):
                configure(ctx.params)
            sys.exit(1)



@cli.command
@click.argument('target')
@click.argument('table')
@click.option('--delete-nul', default=True,
              help='Delete the csv file where nul bytes were replaced?')
@click.pass_obj
def cp(target, table, delete_nul):
    """
    Copy specified csv file to database

    :param target: File to copy to database
    :param table: Database table to connect to
    :param delete_nul: Specify whether the file with nul_bytes replaced should be deleted 
    :return: None
    """
    connection = obj['connection']
    target = CleanCsv(target)

    click.echo(f"Replacing nul bytes in {target.name}.")
    target.replace_nul()

    click.echo(f"Success! Copying {target.name} to {table}")
    target.copy_to_table(table, connection)

    click.echo(f"Success! Copied {target.name} to {table}")
    if delete_nul:
        target.del_no_nul()
        click.echo(f"Deleted where nul bytes were replaced.")


