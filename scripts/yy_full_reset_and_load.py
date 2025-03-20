#!/usr/bin/env python3

from base.models import *
from django.utils import timezone
from decouple import config

#from club_mgr.models import *
#from assn_mgr.models import *
#from integrations.models import *
#from tourneys.models import *
#from scripts.x_helper_functions import *

from scripts import y_reset_system
from scripts import y_load_test_data
from scripts import workflow_daily_10_licenses
from scripts import workflow_daily_20_loads
from scripts import workflow_daily_30_process
from scripts import workflow_daily_40_addresses
import os
import inspect
from dotenv import load_dotenv
from scripts.x_helper_functions import record_log_data#, record_message, get_association
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")

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

        load_dotenv()  #must have to access .env file values

        app_name = os.path.splitext(os.path.basename(__file__))[0]+".py"
        funct_name = inspect.getframeinfo(inspect.currentframe()).function

        record_log_data("yy_full_reset_and_load.py", "yy_full_reset_and_load", "Resetting system with full reload")

        record_log_data(app_name, "y_reset_system.run()", "Starting")
        y_reset_system.run()
        record_log_data(app_name, "y_reset_system.run()", "Completed")

        record_log_data(app_name, "y_load_test_data.run()", "Starting")
        y_load_test_data.run()
        record_log_data(app_name, "y_load_test_data.run()", "Completed")

        record_log_data(app_name, "workflow_daily_10_licenses.run()", "Starting")
        workflow_daily_10_licenses.run('reset')
        record_log_data(app_name, "workflow_daily_10_licenses.run()", "Completed")

        record_log_data(app_name, "workflow_daily_20_loads.run()", "Starting")
        workflow_daily_20_loads.run('reset')
        record_log_data(app_name, "workflow_daily_20_loads.run()", "Completed")

        record_log_data(app_name, "workflow_daily_30_process.run()", "Starting")
        workflow_daily_30_process.run('reset')
        record_log_data(app_name, "workflow_daily_30_process.run()", "Completed")

        record_log_data(app_name, "workflow_daily_40_addresses.run()", "Starting")
        workflow_daily_40_addresses.run('reset')
        record_log_data(app_name, "workflow_daily_40_addresses.run()", "Completed")

        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()
 
        #Email log file
#        send_attachment(fname)
#        os.remove(fname)


# python manage.py runscript yy_full_reset_and_load

# nohup python manage.py runscript yy_full_reset_and_load &

#All require fresh restart
#    0. Check env if doing from desktop!!!
#    1. Ensure github has latest files in zbackupfiles
#    2. Connect to Azure Portal and start ssh
#    3. Run 'nohup python manage.py runscript yy_full_reset_and_load &'
