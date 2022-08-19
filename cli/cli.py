import os
import click
from cleancsv import *

@click.group(chain=True)
@click.option('--database', default='cleancsv', help='PostgreSQL database name',
              prompt='Please enter the PostgreSQL database name')
@click.option('--user', default=f"{os.environ.get('USER')}", help='PostgreSQL database user',
              prompt='Please enter the PostgreSQL database user')
@click.option('--password', default='password', help='PostgreSQL database password',
              prompt='Please enter the PostgreSQL database password')
@click.option('--host', default='localhost', help='PostgreSQL database host',
              prompt='Please enter the PostgreSQL database host')
@click.option('--port', default=5432, help='PostgreSQL database port',
              prompt='Please enter the PostgreSQL database port')
@click.pass_context
def cli(ctx, database, user, password, host, port):
    try:
        connection = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
        ctx.obj = {
            "connection": connection,
            "database": database,
            "username": user,
            "password": password,
            "host": host,
            "port": str(port)
        }

    except psycopg2.Error as e:
        click.echo("Could not connect to the database: ")
        click.echo(e.message)
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

@cli.command
@click.argument('target')
@click.pass_obj
def json(target):
    """
    Create json file for schema

    :param target: File to copy to database
    :return: None
    """
    connection = obj['connection']
    target = CleanCsv(target)
    target.generate_table_type_file()
    click.echo(f"Wrote schema file to {target.js_name}.")


