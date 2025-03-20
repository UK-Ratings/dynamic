#!/usr/bin/env python3

from assn_mgr.models import *

from integrations.models import *
from tourneys.models import *

from scripts.x_helper_functions import *
from scripts.x_helper_assn_specific import *

from django.utils import timezone
import os
import inspect

from dotenv import load_dotenv
from django.conf import settings

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")

def Process_Addresses(f, all_addresses, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("Process_Addresses: " + str(all_addresses) + str(timezone.now()) + "\n")
    
    tot_addr = address.objects.count()
    if all_addresses:
        addr = address.objects.all().order_by('id')#[:50]
    else:
        addr = address.objects.all().exclude(address_validated=True).order_by('id')#[:50]

    if DEBUG_WRITE:
        print("all addresses: ", str(all_addresses) + "\n")
        print("To be processed: ", str(addr.count()) + " of " + str(tot_addr))
    if(1==1):
        f.write("To be processed: " + str(addr.count()) + " " + str(timezone.now()) + " of " + str(tot_addr) + "\n")

    ctr = 0
    batch_size = 500 #50
    updates = []

    for x in addr:
        lat, long, real_latlong = GetLatLong(f, x.address_postcode, False)
        if DEBUG_WRITE:
            f.write("Get Lat Long Results: " + str(lat) + " " + str(long) + " real:" +str(real_latlong) + " " + str(timezone.now()) + " of " + str(tot_addr) + "\n")
#        print(x.address_postcode, lat, long, real_latlong)

        if real_latlong:
            x.address_lat = lat
            x.address_long = long
            x.address_validated = True
            updates.append(x)
        
        ctr += 1
        if ctr % batch_size == 0:
            if DEBUG_WRITE:
#                print("Processed: ", str(ctr))
                f.write("Processed: " + str(ctr) + " " + str(timezone.now()) + "\n")
            # Bulk update
            with transaction.atomic():
                address.objects.bulk_update(updates, ['address_lat', 'address_long', 'address_validated'])
            updates = []

    # Final bulk update for remaining records
    if updates:
        with transaction.atomic():
            address.objects.bulk_update(updates, ['address_lat', 'address_long', 'address_validated'])

    if DEBUG_WRITE:
        f.write(" COMPLETE: Process_Addresses: " + str(timezone.now()) + "\n")
        f.write(" Total Addresses: " + str(tot_addr) + " and address_validated=false: " + str(address.objects.all().exclude(address_validated=True).count()) + "\n")
        f.write("COMPLETE: Process_Addresses: " + str(timezone.now()) + "\n")


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
        if 'reset' in args:
                force_overwrite = True
        else:
                force_overwrite = False

        if(1==1):
                f.write("DEBUG_WRITE: " + str(DEBUG_WRITE) + "\n")
                f.write("asn:  " + str(asn.assn_name) + "\n")
                f.write("force_overwrite:  " + str(force_overwrite) + "\n")

        record_log_data(app_name, "process_lat_long", "Starting")
        Process_Addresses(f, force_overwrite, DEBUG_WRITE)
        record_log_data(app_name, "process_lat_long", "Completed")

        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()
        record_log_data(app_name, funct_name, "Completed")





# python manage.py runscript x_process_addresses
# python manage.py runscript x_process_addresses --script-args reset



