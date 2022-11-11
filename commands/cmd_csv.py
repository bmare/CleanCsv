import click
import os
from cleancsv import CleanCsv

@click.command()
@click.argument('foia_files')
def cli(foia_files):
    files_to_clean=[file for file in os.scandir(foia_files) \
                   if os.path.basename(file).endswith('.csv') \
                   and click.confirm(f'Clean file {os.path.basename(file)}?')]
    for file in files_to_clean:
        _csv = CleanCsv(os.path.abspath(file))
        _csv.replace_nul()
        click.echo(f"Cleaning {os.path.abspath(file)}")
        _csv.write_to_csv()
        _csv.del_no_nul()
        click.echo(f"Cleaned {_csv.row_count}")
