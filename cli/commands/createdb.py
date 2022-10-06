import os, json
import click
from definitions import ROOT_DIR, JSON_DIR, CONFIG_FILE

@click.command
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
