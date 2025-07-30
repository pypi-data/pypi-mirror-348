""" The command line interface for nbconvertjkl """

import click
import sys
import nbformat

from nbconvertjkl.log import configure_logger
from nbconvertjkl.config import get_config
from nbconvertjkl.converter import Converter

#TODO maybe add click.progressbar() for some things

@click.command()
@click.option('--yes', is_flag=True, help="Run without confirmation prompts.")
def run(yes):
    """ Simple program that helps you build Jekyll compatable html files from ipython notebooks """

    logger = configure_logger()
    config_dict = get_config()

    click.echo("Initializing converter and gathering notebooks...")
    converter = Converter(config_dict)

    if not converter.new_nbs:
        click.secho("No notebooks found.\nMake sure the "
                    "read/write config paths are set properly "
                    "and try again.\nExiting", fg='red')
        sys.exit(1)
    
    else:

        if not yes and not click.confirm("Found {} notebooks to convert.\nDo you want to continue?".format(len(converter.new_nbs)), default=True):
            sys.exit(1)
        
        else:

            for nbtitle in converter.new_nbs.keys():

                if not yes and not click.confirm(click.style("{} -- Add nb to site? ('n' will skip it)".format(nbtitle), fg='bright_white'), default=True):
                    converter.new_nbs[nbtitle]['skip_build'] = True
                    click.secho("Skipped.", fg='red')
                else:
                    fm_confirmed = False
                    fm_valid = True
                    while not fm_confirmed or not fm_valid:

                        fm = converter.new_nbs[nbtitle]["front_matter"]
                        click.secho(fm, fg='yellow')

                        if not fm_valid:
                            click.secho("The front matter displayed is invalid. Please edit it.", fg='red')
                            #TODO add specific validation error so user knows whats wrong
                        
                        if not yes and not click.confirm("Confirm front matter ('n' will open an editor for you to modify it).", default=True):
                            fm = click.edit(fm)
                            fm_valid = converter.validate_front_matter(fm)
                        else:
                            fm_confirmed = converter.validate_front_matter(fm)

            if config_dict['nb_nav_top'] or config_dict['nb_nav_bottom']:
                converter.add_nb_nav()
            else:
                logger.debug('No nb nav added - see configs to change')

            click.secho("*****CONVERTER SUMMARY START*****".format(nbtitle), fg='bright_white')
            click.secho(converter.get_summary(), fg='yellow')
            click.secho("*****CONVERTER SUMMARY END*****".format(nbtitle), fg='bright_white')
            
            if not yes and not click.confirm(click.style("Write files and finish?", fg='green'), default=True):
                sys.exit(1)
            else:
                click.echo("Preparing to write files to {}".format(config_dict['nb_write_path']))
                if config_dict.get('overwrite_existing', True):
                    click.secho("Found existing files in write directory!", fg='red')
                    click.secho("Continuing will replace all existing files with the same name!", fg='red')
                    if not yes and not click.confirm("Are you sure you want to continue?", default=True):
                        sys.exit(1)
                else:
                    logger.debug("Overwrite disabled. Existing files will be preserved and only new ones added.")

                click.echo("Writing notebooks...")
                converter.write_nbs()

                click.echo("Collecting and moving notebook assets to {}".format(config_dict['asset_write_path']))
                converter.copy_and_move_assets()
            
        click.secho("Site build complete.", fg='bright_white')

if __name__ == "__main__":
    run()