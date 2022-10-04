import os, json
import click
from cleancsv import *
from definitions import ROOT_DIR, JSON_DIR, CONFIG_FILE

from db import *
# Paths

# Utility Functions
def connect_db(user, password, host, port, database=None):
    if database:
        return psycopg2.connect(user=user, password=password, \
                                      database=database, host=host, port=port)
    else:
        return psycopg2.connect(user=user, password=password, host=host, port=port)

def create_db(connection, database:str) -> None:
    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    curs = connection.cursor()
    with curs:
        curs.execute(f"CREATE DATABASE {database};")
        create_appeal_table(curs)
        create_appln_table(curs)
        create_atty_table(curs)
        create_bond_table(curs)
        create_case_table(curs)
        create_caseid_table(curs)
        create_caseprioritytable(curs)
        create_charges_tabe(curs)
        create_custody_tale(curs)
        create_fedcourtstable(curs)
        create_juveniletable(curs)
        create_motion_able(curs)
        create_probono_table(curs)
        create_proceeding_table(curs)
        create_reps_table(curs)
        create_rider_table(curs)
        create_schedule_table(curs)
        create_threembr_table(curs)

def load_config() -> dict:
    return json.load(open(CONFIG_FILE))

def configure(ctx:dict):
    _config = {
            'host': click.prompt("Enter host name", default='localhost'),
            'port': click.prompt('PostgreSQL database port', default=5432),
            'database': click.prompt('PostgreSQL database name', default='eoir_foia')
            }
    database = _config.pop('database')
    try:
        connection = connect_db(user=ctx['user'], password=ctx['password'], **_config)
        create_db(connection, database)
        _config['database'] = database
        with open(CONFIG_FILE, 'w') as f:
            json.dump(_config, f, ensure_ascii=False, indent=4)
        click.echo("Configuration complete.")
    except psycopg2.Error as e:
        click.echo("Unable to connect to the database. Check that you've entered the proper credentials.")
        click.echo(e)

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


