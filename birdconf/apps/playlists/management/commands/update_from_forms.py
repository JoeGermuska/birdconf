"""
"""
from django.core.management.base import BaseCommand, CommandError, handle_default_options
from optparse import make_option

from playlists import scraper,models
    
class Command(BaseCommand):
    args=''
    help=''
    option_list= BaseCommand.option_list + ()

    def get_version(self):
        return "0.1"

    def handle(self, *args, **options):
        x = scraper.update_json_from_forms()
        scraper.dump_json_playlists(x)
        
        show = x[-1]
        models.show_from_json(*show)
        scraper.print_show(show[1])
        
        