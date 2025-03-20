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


def Fix_BF_Corrects_Discipline(f, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("Fix_BF_Corrects_Discipline: " + str(timezone.now()) + "\n")

        asn = get_association(None, "British Fencing", False)
        for x in admin_corrects_disciplines.objects.all():
                disp = get_assn_discipline_from_text(f, asn, x.event_assn_discipline, None, None, DEBUG_WRITE)
                if(disp is not None):
                        eve = None
                        tourney = None
                        f.write("Looking for: " + str(x.tourney_name) + " " + str(x.event_name) + "\n")
                        tourney = tournaments.objects.filter(tourney_name__iexact = x.tourney_name)
                        if(tourney is None or len(tourney) == 0):
                                f.write("     ERROR: cannot find tourney: " + str(x.tourney_name) + "\n")
                        else:
                                for y in tourney:
                                        f.write("  found tourney: " + str(y.tourney_name) + "\n")
                                        eve = events.objects.filter(ev_tourney = y, ev_name__iexact = x.event_name)
                                        if(eve is None or len(eve) == 0):
                                                f.write("     ERROR: cannot find event: " + str(x.event_name) + "\n")
                                        else:
                                                for z in eve:
                                                        f.write("  found event: " + str(z.ev_name) + " Discipline: "+ str(disp.discipline_name) + "\n")
                                                        ue = update_or_create_event(None, False, y, z, z.ev_name,
                                                                        z.ev_status.status, z.ev_assn_type, disp, z.ev_assn_gender, z.ev_assn_ages, z.ev_start_date)
                                                        f.write("  updated event: " + str(ue) + " " + str(z.ev_name) + " Discipline: "+ str(disp.discipline_name) + "\n")
                else:
                        f.write("     ERROR: cannot find discipline: " + str(x.event_assn_discipline) + "\n")
        if(DEBUG_WRITE):
                f.write(" Complete Fix_BF_Corrects_Discipline: " + str(timezone.now()) + "\n")

def Fix_BF_Corrects_Gender(f, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("Fix_BF_Corrects_Gender: " + str(timezone.now()) + "\n")

        asn = get_association(None, "British Fencing", False)
        for x in admin_corrects_genders.objects.all():
                gen = get_assn_gender_from_text(f, asn, x.event_assn_gender, None, None, DEBUG_WRITE)
                if(gen is not None):
                        eve = None
                        tourney = None
                        f.write("Looking for: " + str(x.tourney_name) + " " + str(x.event_name) + "\n")
                        tourney = tournaments.objects.filter(tourney_name__iexact = x.tourney_name)
                        if(tourney is None or len(tourney) == 0):
                                f.write("     ERROR: cannot find tourney: " + str(x.tourney_name) + "\n")
                        else:
                                for y in tourney:
                                        f.write("  found tourney: " + str(y.tourney_name) + "\n")
                                        eve = events.objects.filter(ev_tourney = y, ev_name__iexact = x.event_name)
                                        if(eve is None or len(eve) == 0):
                                                f.write("     ERROR: cannot find event: " + str(x.event_name) + "\n")
                                        else:
                                                for z in eve:
                                                        f.write("  found event: " + str(z.ev_name) + " Discipline: "+ str(gen.gender_name) + "\n")
                                                        ue = update_or_create_event(None, False, y, z, z.ev_name,
                                                                        z.ev_status.status, z.ev_assn_type, z.ev_assn_discipline, gen, z.ev_assn_ages, z.ev_start_date)
                                                        f.write("  updated event: " + str(ue) + " " + str(z.ev_name) + " Discipline: "+ str(gen.gender_name) + "\n")
                else:
                        f.write("     ERROR: cannot find gender: " + str(x.event_assn_gender) + "\n")
        if(DEBUG_WRITE):
                f.write(" Complete Fix_BF_Corrects_Gender: " + str(timezone.now()) + "\n")


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
        record_log_data("y_add_missing_disciplines_genders.py", "Fix_BF_Corrects_Discipline", "Starting")
        Fix_BF_Corrects_Discipline(f, DEBUG_WRITE)
        record_log_data("y_add_missing_disciplines_genders.py", "Fix_BF_Corrects_Discipline", "Completed")

        record_log_data("y_add_missing_disciplines_genders.py", "Fix_BF_Corrects_Gender", "Starting")
        Fix_BF_Corrects_Gender(f, DEBUG_WRITE)
        record_log_data("y_add_missing_disciplines_genders.py", "Fix_BF_Corrects_Gender", "Completed")

        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()
 
        #Email log file
#        send_attachment(fname)
#        os.remove(fname)


# python manage.py runscript y_add_missing_disciplines_genders

