import os, json
import click
from cleancsv import *
from definitions import ROOT_DIR, JSON_DIR, CONFIG_FILE

# Paths

# Utility Functions
def connect_db(user, password, host, port, database=None):
    if database:
        return psycopg2.connect(user=user, password=password, \
                                      database=database, host=host, port=port)
    else:
        return psycopg2.connect(user=user, password=password, host=host, port=port)

def load_config() -> dict:
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def create_db(connection, database:str) -> None:
    curs = connection.cursor()
    curs.execute(f"CREATE DATABASE {database};")
    connection.commit()

# Cli Commands
@click.group(chain=True)
@click.option('--user', default=f"{os.environ.get('USER')}", help='PostgreSQL database user',
              prompt='Please enter the PostgreSQL database user')
@click.option('--password', default='password', help='PostgreSQL database password',
              hide_input=True, prompt='Please enter the PostgreSQL database password')
@click.pass_context
def cli(ctx, user, password):
    try:
        ctx.obj = {'username': user, 'password': password}
        # import IPython; IPython.embed()
        ctx.obj.update(load_config()) #add config variables to context
        connection = connect_db(**ctx.obj)
    except (json.JSONDecodeError, psycopg2.Error) as e:
        click.echo("""It appears the database connection hasn't been configured""")
        if click.confirm("Run cleancsv setup?"):
            setup()
        click.echo(e)
        sys.exit(1)


@cli.command
@click.option('--host', default='localhost', help='PostgreSQL database host',
             prompt='Please enter the PostgreSQL database host')
@click.option('--port', default=5432, help='PostgreSQL database port',
              prompt='Please enter the PostgreSQL database port')
@click.option('--database', default='eoir_foia', help='PostgreSQL database name',
              prompt='Please name the database to create.')
def setup(ctx, host, port, database):
    connection = ctx.obj['connection']
    create_db(connection, database)
    config = {
            'host': host,
            'port':port,
            'database':database
            }

    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

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


