import os
import click
from cleancsv import *

@click.group(chain=True)
@click.option('--user', default=f"{os.environ.get('USER')}", help='PostgreSQL database user',
              prompt='Please enter the PostgreSQL database user')
@click.option('--password', default='password', help='PostgreSQL database password',
              prompt='Please enter the PostgreSQL database password')
@click.option('--host', default='localhost', help='PostgreSQL database host',
             prompt='Please enter the PostgreSQL database host')
@click.option('--port', default=5432, help='PostgreSQL database port',
              prompt='Please enter the PostgreSQL database port')
@click.option('--database', default=None, help='PostgreSQL database name',
              prompt='Name of preexisting database or database to create.')
@click.pass_context
def cli(ctx, database, user, password, host, port):
    try:
        connection = connect_db(**ctx.params)
        ctx.obj = {"connection": connection, **ctx.params}

    except psycopg2.Error as e:
        database = ctx.params.pop('database')
        connection = connect_db(**ctx.params) 

        click.echo(f"Could not connect to the database. Creating database {database}")
        curs = conn.cursor()
        curs.execute(f"CREATE DATABASE {database};")

        connection = connect_db(database=database, **ctx.params)
        ctx.obj = {"connection": connection, **ctx.params}
        import IPython; IPython.embed()

def connect_db(user, password, host, port, database=None):
    if database:
        return psycopg2.connect(user=user, password=password, \
                                      database=database, host=host, port=port)
    else:
        return psycopg2.connect(user=user, password=password, host=host, port=port)

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


