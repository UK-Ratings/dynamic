#!/usr/bin/env python3

from assn_mgr.models import *

from integrations.models import *
from tourneys.models import *

from scripts.x_helper_functions import *
from scripts.x_helper_assn_specific import *
from scripts import x_process_addresses

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

        if os.environ.get("DURHAM_TOURNAMENT_PROCESS_DAY_TO_LOAD") is not None:
                process_days_back = int(os.environ.get("DURHAM_TOURNAMENT_PROCESS_DAY_TO_LOAD"))
        else:
                process_days_back = None
        if os.environ.get("S80_UPCOMING_DAYS_OUT") is not None:
                process_days_out = int(os.environ.get("S80_UPCOMING_DAYS_OUT"))
        else:
                process_days_out = None

        if(process_days_back is not None and process_days_out is not None):
                ls_date = None
                le_date = None
                force_overwrite = False
                reset_string = ""
                no_load_data = False

                asn = get_association(f, "British Fencing", DEBUG_WRITE)
                if(DEBUG_WRITE):
                        f.write("DEBUG_WRITE: " + str(DEBUG_WRITE) + "\n")
                        f.write("asn:  " + str(asn.assn_name) + "\n")
                        f.write("process_days_back:  " + str(process_days_back) + "\n")
                        f.write("process_days_back:  " + str(process_days_out) + "\n")
                ls_date, le_date, le_date_future, reset_string, no_load_data, ls_date_str, \
                                le_date_str, le_date_future_str = process_workflow_args(f, args, process_days_back, process_days_out, DEBUG_WRITE)

        if(process_days_back is not None  and process_days_out is not None):

                record_log_data(app_name, "x_process_addresses", "Starting")
                x_process_addresses.run(reset_string)
                record_log_data(app_name, "x_process_addresses", "Completed")

        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()
        record_log_data(app_name, funct_name, "Completed")





# python manage.py runscript workflow_daily_40_addresses
# python manage.py runscript workflow_daily_40_addresses --script-args reset
# python manage.py runscript workflow_daily_40_addresses --script-args 06/01/2024 11/12/2024
# python manage.py runscript workflow_daily_40_addresses --script-args reset 01/01/2022 03/31/2022

# python manage.py runscript workflow_daily_40_addresses --script-args reset 01/06/2022 01/31/2031 noload

# nohup python manage.py runscript workflow_daily_40_addresses --script-args reset 01/01/2022 01/31/2029 &
# nohup python manage.py runscript workflow_daily_40_addresses --script-args reset &

# nohup python manage.py runscript workflow_daily_40_addresses --script-args 06/01/2024 01/31/2029 noload &

# nohup python manage.py runscript workflow_daily_40_addresses --script-args 06/01/2024 01/31/2029 noload &

# python manage.py runscript workflow_daily_40_addresses --script-args 06/01/2024 01/31/2029 noload
