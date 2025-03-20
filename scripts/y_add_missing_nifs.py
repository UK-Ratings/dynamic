#!/usr/bin/env python3

from django.utils import timezone
import os
from dotenv import load_dotenv
from django.conf import settings

from assn_mgr.models import *    
from club_mgr.models import *
from base.models import *
from tourneys.models import *
from scripts.x_helper_functions import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")

def Fix_BF_NIF_British_Fencing_Championships_2022(f, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("Fix_BF_NIF_British_Fencing_Championships_2022: " + str(timezone.now()) + "\n")

        tourney = tournaments.objects.get(tourney_name__icontains = "British Fencing Championships 2022")
        eve = events.objects.get(ev_tourney = tourney, ev_name__iexact = "Men's Epee")
        update_or_create_event_extra_field(f, eve, 'NIF', 539, False)
        eve = events.objects.get(ev_tourney = tourney, ev_name__iexact = "Men's Epee - B Championships")
        update_or_create_event_extra_field(f, eve, 'NIF', 63, False)

        eve = events.objects.get(ev_tourney = tourney, ev_name__iexact = "Men's Foil")
        update_or_create_event_extra_field(f, eve, 'NIF', 443, False)
        eve = events.objects.get(ev_tourney = tourney, ev_name__iexact = "Men's Foil - B Championships")
        update_or_create_event_extra_field(f, eve, 'NIF', 50, False)

        eve = events.objects.get(ev_tourney = tourney, ev_name__iexact = "Men's Sabre")
        update_or_create_event_extra_field(f, eve, 'NIF', 324, False)
        eve = events.objects.get(ev_tourney = tourney, ev_name__iexact = "Men's Sabre - B Championships")
        update_or_create_event_extra_field(f, eve, 'NIF', 34, False)

##                    Men's Epee	Epee	Men	Senior	121	539
##                    Men's Epee - B Championships	Epee	Men	Senior	35	63
#                    Men's Foil	Foil	Men	Senior	102	443
#                    Men's Foil - B Championships	Foil	Men	Senior	28	50
#                    Men's Sabre	Sabre	Men	Senior	64	324
#                    Men's Sabre - B Championships	Sabre	Men	Senior	19	34

        eve = events.objects.get(ev_tourney = tourney, ev_name__iexact = "Women's Epee")
        update_or_create_event_extra_field(f, eve, 'NIF', 323, False)
        eve = events.objects.get(ev_tourney = tourney, ev_name__iexact = "Women's Epee - B Championships")
        update_or_create_event_extra_field(f, eve, 'NIF', 36, False)

        eve = events.objects.get(ev_tourney = tourney, ev_name__iexact = "Women's Foil")
        update_or_create_event_extra_field(f, eve, 'NIF', 325, False)
        eve = events.objects.get(ev_tourney = tourney, ev_name__iexact = "Women's Foil - B Championships")
        update_or_create_event_extra_field(f, eve, 'NIF', 34, False)

        eve = events.objects.get(ev_tourney = tourney, ev_name__iexact = "Women's Sabre")
        update_or_create_event_extra_field(f, eve, 'NIF', 163, False)
        eve = events.objects.get(ev_tourney = tourney, ev_name__iexact = "Women's Sabre - B Championships")
        update_or_create_event_extra_field(f, eve, 'NIF', 12, False)

#                    Women's Epee	Epee	Women	Senior	68	323
#                    Women's Epee - B Championships	Epee	Women	Senior	20	36
#                    Women's Foil	Foil	Women	Senior	66	325
#                    Women's Foil - B Championships	Foil	Women	Senior	19	34
#                    Women's Sabre	Sabre	Women	Senior	27	163
#                    Women's Sabre - B Championships	Sabre	Women	Senior	7	12



def run(*args):

        db_host_name = str(settings.DATABASES['default']['HOST'])
        db_name = str(settings.DATABASES['default']['NAME'])
        path_logs = os.path.join(settings.BASE_DIR, "logs/")
        path_input = os.path.join(settings.BASE_DIR, "scripts/")

        logs_filename = path_logs+db_name+"_"+os.path.splitext(os.path.basename(__file__))[0] + ".txt"
        f = open(logs_filename, "w", encoding='utf-8')
        f.write("Starting " + logs_filename + str(timezone.now()) + "\n")
        f.write("database_host_name: " + db_host_name + "\n")
        f.write("database_name: " + db_name + "\n")

        DEBUG_WRITE = True
        record_log_data("y_add_missing_nifs.py", "Fix_BF_NIF_British_Fencing_Championships_2022", "Starting")
        Fix_BF_NIF_British_Fencing_Championships_2022(f, DEBUG_WRITE)
        record_log_data("y_add_missing_nifs.py", "Fix_BF_NIF_British_Fencing_Championships_2022", "Completed")

        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()
 
        #Email log file
#        send_attachment(fname)
#        os.remove(fname)


# python manage.py runscript y_add_missing_nifs

