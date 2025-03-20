#!/usr/bin/env python3

from assn_mgr.models import *
from users.models import User

from integrations.models import *
from tourneys.models import *

from scripts.x_helper_functions import *
from scripts.x_helper_assn_specific import *
from scripts import x_apply_member_numbers

from django.utils import timezone
from django.db.models import F
import os
import inspect
import re

from dotenv import load_dotenv
from django.conf import settings

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")


def Delete_Tournaments(f, DEBUG_WRITE):
        record_log_data("x_apply_te_delete_hide.py", "Delete_Tournaments", "started: " + str(timezone.now()))
        f.write("\n Delete_Tournaments: " + str(timezone.now()) + "\n")

        for x in admin_deleted_tournaments.objects.all():
                asn = get_association(f, x.adt_tourney_assn_name, DEBUG_WRITE)
                f.write("Searching for Admin Deleted Tourney: " + x.adt_tourney_name + " " + str(x.adt_tourney_start_date) + " " + x.adt_tourney_inbound + "\n")

                try:
                        found_tournament = tournaments.objects.get(tourney_name__iexact = x.adt_tourney_name, 
                                                tourney_assn=asn, 
                                                tourney_start_date = x.adt_tourney_start_date,
                                                tourney_inbound__iexact=x.adt_tourney_inbound)
                except tournaments.DoesNotExist:
                        found_tournament = None
                        f.write("ERROR  ---> Tournament not found: " + x.adt_tourney_name + " " + str(x.adt_tourney_start_date) + " " + x.adt_tourney_inbound + "\n")
                else:
                        f.write("         Tournament found: " + x.adt_tourney_name + " " + str(x.adt_tourney_start_date) + " " + x.adt_tourney_inbound + "\n")
                        found_tournament.delete()
        f.write(" COMPLETE: Delete_Tournaments: " + str(timezone.now()) + "\n")
        record_log_data("x_apply_te_delete_hide.py", "Delete_Tournaments", "completed: " + str(timezone.now()))

def Delete_Events(f, DEBUG_WRITE):
        record_log_data("x_apply_te_delete_hide.py", "Delete_Events", "started: " + str(timezone.now()))
        f.write("\n Delete_Events: " + str(timezone.now()) + "\n")

        for x in admin_deleted_events.objects.all():
                asn = get_association(f, x.ade_tourney_assn_name, DEBUG_WRITE)
                try:
                        found_event = events.objects.get(ev_tourney__tourney_name__iexact = x.ade_tourney_name,
                                                ev_tourney__tourney_assn=asn, 
                                                ev_name__iexact=x.ade_event_name,
#                                                tourney_start_date = x.adt_tourney_start_date,
                                                ev_tourney__tourney_inbound__iexact=x.ade_tourney_inbound)
                except events.DoesNotExist:
                        found_event = None
                        f.write("Event not found: " + x.ade_tourney_name + " " + str(x.ade_event_name) + " " + str(x.ade_tourney_start_date) + " " + x.ade_tourney_inbound + "\n")
                else:
                        f.write("Event found: " + x.ade_tourney_name + " " + str(x.ade_event_name) + " " + str(x.ade_tourney_start_date) + " " + x.ade_tourney_inbound + "\n")
                        found_event.delete()
        f.write(" COMPLETE: Delete_Events: " + str(timezone.now()) + "\n")
        record_log_data("x_apply_te_delete_hide.py", "Delete_Events", "completed: " + str(timezone.now()))

def Hide_Events(f, DEBUG_WRITE):
        record_log_data("x_apply_te_delete_hide.py", "Hide_Events", "started: " + str(timezone.now()))
        f.write("\n Hide_Events: " + str(timezone.now()) + "\n")

        events.objects.all().update(ev_hide_from_listings=False, ev_hide_from_ratings_calc=False)

        for x in admin_hide_event.objects.all():
                try:
                        event = events.objects.get(id=x.hide_event.id)
                        event.ev_hide_from_listings = x.hide_from_listings
                        event.ev_hide_from_ratings_calc = x.hide_from_ratings_calc
                        event.save()
                        f.write(f"Event found and updated: {x.hide_event.ev_tourney.tourney_name} {x.hide_event.ev_name} {x.hide_event.ev_tourney.tourney_inbound}\n")
                except events.DoesNotExist:
                        f.write(f"Event NOT found: {x.hide_event.ev_tourney.tourney_name} {x.hide_event.ev_name} {x.hide_event.ev_tourney.tourney_inbound}\n")

        f.write(" COMPLETE: Hide_Events: " + str(timezone.now()) + "\n")
        record_log_data("x_apply_te_delete_hide.py", "Hide_Events", "completed: " + str(timezone.now()))

def run(*args):
        if(1==1): #basic setup
                db_host_name = str(settings.DATABASES['default']['HOST'])
                db_name = str(settings.DATABASES['default']['NAME'])
                path_logs = os.path.join(settings.BASE_DIR, "logs/")
                path_input = os.path.join(settings.BASE_DIR, "scripts/")

                logs_filename = path_logs+db_name+"_"+os.path.splitext(os.path.basename(__file__))[0] + ".txt"
                f = open(logs_filename, "w", encoding='utf-8')
                f.write("Starting " + logs_filename + str(timezone.now()) + "\n")
                f.write("database_host_name: " + db_host_name + "\n")
                f.write("database_name: " + db_name + "\n")

                load_dotenv()  #must have to access .env file values

                app_name = os.path.splitext(os.path.basename(__file__))[0]+".py"
                funct_name = inspect.getframeinfo(inspect.currentframe()).function

        DEBUG_WRITE = True
        f.write("DEBUG_WRITE: " + str(DEBUG_WRITE) + "\n")
        f.write("args: " + str(args) + " " + str(len(args)) + "\n")

        record_log_data(app_name, "Delete_Tournaments", "Starting")
        Delete_Tournaments(f, DEBUG_WRITE)
        record_log_data(app_name, "Delete_Tournaments", "Completed")

        record_log_data(app_name, "Delete_Events", "Starting")
        Delete_Events(f, DEBUG_WRITE)
        record_log_data(app_name, "Delete_Events", "Completed")

        record_log_data(app_name, "Hide_Events", "Starting")
        Hide_Events(f, DEBUG_WRITE)
        record_log_data(app_name, "Hide_Events", "Completed")

        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()
        record_log_data(app_name, funct_name, "Completed")


#Process runs as follows:
#        admin_hide_event - hide_from_listings = True = Make sure event is not in listings
#        admin_hide_event - hide_from_ratings_calc = True = Make sure event is not in ratings calc

#        admin_deleted_tournaments - delete tournament and all events
#        admin_deleted_events - delete event

#class admin_hide_event(models.Model):
#    hide_event = models.ForeignKey(events, on_delete=models.CASCADE)
#    hide_from_listings = models.BooleanField("Hide from Listings", default=False)
#    hide_from_ratings_calc = models.BooleanField("Hide from Ratings Calc", default=False)
#    hide_user=models.CharField("Inbound Tournament", max_length=100, blank=True, null=True)
#    hide_update_date = models.DateTimeField("Update Date", blank=True, null=True)

#class admin_deleted_tournaments(models.Model):
#    adt_tourney_assn_name = models.CharField("Tournament Association Name", max_length=300)
#    adt_tourney_name = models.CharField("Tournament Name", max_length=300)
#    adt_tourney_inbound = models.CharField("Inbound Tournament", max_length=100, blank=True, null=True)
#    adt_tourney_start_date = models.DateTimeField("Tournament Start Time", blank=True, null=True)
#    adt_tourney_end_date = models.DateTimeField("Tournament End Time", blank=True, null=True)
#    adt_date_deleted = models.DateTimeField(blank=True, null=True)

#class admin_deleted_events(models.Model):
#    ade_tourney_assn_name = models.CharField("Tournament Association Name", max_length=300)
#    ade_tourney_name = models.CharField("Tournament Name", max_length=300)
#    ade_tourney_inbound = models.CharField("Inbound Tournament", max_length=100, blank=True, null=True)
#    ade_tourney_start_date = models.DateTimeField("Tournament Start Time", blank=True, null=True)
#    ade_tourney_end_date = models.DateTimeField("Tournament End Time", blank=True, null=True)
#    ade_event_name = models.CharField("Event Name", max_length = 400)
#    ade_delete_date = models.DateTimeField("Update Date", blank=True, null=True)



# python manage.py runscript x_apply_te_delete_hide


