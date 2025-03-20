#!/usr/bin/env python3

from assn_mgr.models import *

from integrations.models import *
from tourneys.models import *

from scripts.x_helper_functions import *
from scripts.x_helper_assn_specific import *
from scripts import integrations_load_bf_ranking_points
from scripts import assn_mgr_s80_load_members_clubs
from scripts import assn_mgr_s80_process_members_clubs

from django.utils import timezone
import os
import inspect

from dotenv import load_dotenv
from django.conf import settings

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")



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

        asn = get_association(f, "British Fencing", DEBUG_WRITE)

        if(DEBUG_WRITE):
                f.write("DEBUG_WRITE: " + str(DEBUG_WRITE) + "\n")
                f.write("asn:  " + str(asn.assn_name) + "\n")

        record_log_data(app_name, "workflow_daily_10_licenses", "Starting")

        record_log_data(app_name, "assn_mgr_s80_load_members_clubs.run()", "Starting")
        assn_mgr_s80_load_members_clubs.run()
        record_log_data(app_name, "assn_mgr_s80_load_members_clubs.run()", "Completed")

        record_log_data(app_name, "assn_mgr_s80_process_members_clubs.run()", "Starting")
        assn_mgr_s80_process_members_clubs.run()
        record_log_data(app_name, "assn_mgr_s80_process_members_clubs.run()", "Completed")

        record_log_data(app_name, "integrations_load_bf_ranking_points.run()", "Starting")
        integrations_load_bf_ranking_points.run()                 
        record_log_data(app_name, "integrations_load_bf_ranking_points.run()", "Completed")

        record_log_data(app_name, "workflow_daily_10_licenses", "Complete")

        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()
        record_log_data(app_name, funct_name, "Completed")


# python manage.py runscript workflow_daily_10_licenses
# nohup python manage.py runscript workflow_daily_10_licenses &


