import os, json
import click
from definitions import ROOT_DIR, JSON_DIR, CONFIG_FILE

@click.command()
def configure(ctx:dict):
    pass
    # _config = {
    #         'host': click.prompt("Enter host name", default='localhost'),
    #         'port': click.prompt('PostgreSQL database port', default=5432),
    #         'database': click.prompt('PostgreSQL database name', default='eoir_foia')
    #         }
    # database = _config.pop('database')
    # try:
    #     connection = connect_db(user=ctx['user'], password=ctx['password'], **_config)
    #     create_db(connection, database)
    #     _config['database'] = database
    #     with open(CONFIG_FILE, 'w') as f:
    #         json.dump(_config, f, ensure_ascii=False, indent=4)
    #     click.echo("Configuration complete.")
    # except psycopg2.Error as e:
    #     click.echo("Unable to connect to the database. Check that you've entered the proper credentials.")
    #     click.echo(e)
