import os, json, sys

import click, psycopg2
from definitions import ROOT_DIR, JSON_DIR, CONFIG_FILE
from cleancsv import CleanCsv
from utils import open_db
from tx import *

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
    except (json.JSONDecodeError, psycopg2.Error, FileNotFoundError) as e:
        click.echo("""It appears the database connection hasn't been configured. Try Running cleancsv cli configure""")
        click.echo(e) #DEBUG
        sys.exit(1)

@cli.command()
@click.pass_obj
def configure(obj):
    _config = {
            'host': click.prompt("Enter host name", default='localhost'),
            'port': click.prompt('PostgreSQL database port', default=5432),
            'database': click.prompt('PostgreSQL database name', default='eoir_foia')
            }
    obj.update(_config)
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(_config, f, ensure_ascii=False, indent=4)
        click.echo("Configuration complete.")
    except Error as e:
        click.echo(e)

@cli.command()
@click.option('--new', default=None, help="Specify database name different from that in config file.")
@click.pass_obj
def createdb(obj, new):
    if new:
        obj['database'] = new
    conn_args = {key:value for key, value in obj.items() if key != 'database'}
    conn = psycopg2.connect(**conn_args)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # Create database cannot run inside a transaction block

    with open_db(conn) as curs:
        curs.execute(f"CREATE DATABASE {obj['database']}")  

    #Update the config file
    old_config = json.load(open(CONFIG_FILE))   
    with open(CONFIG_FILE, 'w') as f:
        old_config['database'] = obj['database']
        json.dump(old_config, f, ensure_ascii=False, indent=4)

    with open_db(psycopg2.connect(**obj)) as curs:
        for tx_name, create in create_tx_functions.items():
            create(curs)
            click.echo(f"Created {tx_name} table")

@cli.command()
@click.argument('path')
@click.pass_obj
def copy_files(obj, path):
    files_to_copy=[file for file in os.scandir(path) \
                   if os.path.basename(file).endswith('.csv') \
                   and click.confirm(f'Copy file {os.path.basename(file)} to the database')]
    for file in files_to_copy:
        # import IPython; IPython.embed()
        _csv = CleanCsv(os.path.abspath(file))
        _csv.replace_nul()
        click.echo(f"Copying {os.path.abspath(file)} to {obj['database']}")
        _csv.copy_to_table(psycopg2.connect(**obj))
        _csv.del_no_nul()
        click.echo(f"Copied {_csv.row_count} rows to {obj['database']}")

cli.add_command(configure)
cli.add_command(createdb)
cli.add_command(copy_files)



