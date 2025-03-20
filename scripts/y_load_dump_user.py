#!/usr/bin/env python3

import os
import csv
import shutil
import pytz

from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")
import django
django.setup()

from django.utils import timezone
from dotenv import load_dotenv

from scripts.x_helper_functions import *


def special_load_user_data(f, file_path, app_name, table_name, file_format, DEBUG_WRITE):
        f.write("special_load_user_data: "
            + " File Path: " + file_path
            + " App_Name: " + app_name
            + " Table_name: " + table_name
            + " File Format: " + file_format
            + " " + str(timezone.now()) + "\n")

        if file_format == 'csv':
                with open(file_path, 'r', newline='') as csvfile:
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                                email = row['email']
#                                username = row['username']
                                first_name = row['first_name']
                                last_name = row['last_name']
                                password = row['password']  # Assuming the CSV contains hashed passwords

                                user, created = User.objects.update_or_create(
                                        email=email,
                                        defaults={
#                                        'username': username,
                                        'first_name': first_name,
                                        'last_name': last_name,
                                        'password': password,  # Ensure this is a hashed password
                                        }
                                )

#                                if created:
#                                        print(f"Created new user: {username}")
#                                else:
#                                        print(f"Updated existing user: {username}")

def dump_table_to_file(f, dump_directory, app_name, table_name, file_format, DEBUG_WRITE):
        f.write("dump_table_to_file: " 
                + " Directory: " + dump_directory
                + " App_Name: " + app_name
                + " Table_name: " + table_name
                + " File Format: " + file_format
                + " " + str(timezone.now()) + "\n")

        try:
                model = apps.get_model(app_name, table_name)
        except LookupError:
                f.write("Table " + str(table_name) + " does not exist in " + str(app_name) + ".\n")
                return
        records = model.objects.all()
        output_file = dump_directory + table_name + "_dump." + file_format

        if file_format == 'csv':
                with open(output_file, 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        fields = [field.name for field in model._meta.fields if field.name != 'id']
                        writer.writerow(fields)
                        for record in records:
                                writer.writerow([getattr(record, field.name) for field in model._meta.fields if field.name != 'id'])
        else:
                f.write("Unsupported file format: " + file_format + "\n")
                return

        f.write(" Completed dump_table_to_file: " + str(timezone.now()) + "\n")
   
def tables_to_dump(f, dump_dir, DEBUG_WRITE):
        os.makedirs(dump_dir, exist_ok=True)        
#        delete_all_files_in_directory(f, dump_dir)

        dump_table_to_file(f, dump_dir, 'users','User', 'csv', DEBUG_WRITE)

        if(DEBUG_WRITE):
                rec = os.environ.get("EMAIL_LOGS_USERNAME")
                title = "Duram Dump Files"
                email_with_attachment(title, 'User_dump',[rec],
                        'dumps', 'User_dump.csv') 

def tables_to_load(f, dump_dir, DEBUG_WRITE):
        input_file = dump_dir + "User" + "_dump.csv"
        special_load_user_data(f, input_file, 'users','User', 'csv', DEBUG_WRITE)

def models_to_permanent(f, DEBUG_WRITE):
        record_log_data("y_load_dump_user.py", "models_to_permanent", "models_to_permanent starting")

#        permanent_admin_modified_event_final_results.objects.all().delete()
#        for x in admin_modified_event_final_results.objects.all():
#               permanent_admin_modified_event_final_results.objects.create(
#                        amefr_tourney_assn_name = x.amefr_tourney_assn_name,
#                        amefr_tourney_name = x.amefr_tourney_name, 
#                        amefr_tourney_inbound = x.amefr_tourney_inbound, 
#                        amefr_tourney_start_date = x.amefr_tourney_start_date,
#                        amefr_tourney_end_date = x.amefr_tourney_end_date, 
#                        amefr_event_name = x.amefr_event_name, 
#                        amefr_orig_assn_member_number = x.amefr_orig_assn_member_number, 
#                        amefr_new_assn_member_number = x.amefr_new_assn_member_number, 
#                        amefr_efr_final_position = x.amefr_efr_final_position, 
#                        amefr_orig_efr_given_member_identifier = x.amefr_orig_efr_given_member_identifier, 
#                        amefr_new_efr_given_member_identifier = x.amefr_new_efr_given_member_identifier, 
#                        amefr_orig_efr_given_name = x.amefr_orig_efr_given_name, 
#                        amefr_new_efr_given_name = x.amefr_new_efr_given_name, 
#                        amefr_orig_efr_given_club = x.amefr_orig_efr_given_club, 
#                        amefr_new_efr_given_club = x.amefr_new_efr_given_club, 
#                        amefr_modified_date = x.amefr_modified_date, 
#                        amefr_user = x.amefr_user.name
#                       )


        record_log_data("y_load_dump_user.py", "models_to_permanent", "models_to_permanent completed")


def run(*args):

        db_host_name = str(settings.DATABASES['default']['HOST'])
        db_name = str(settings.DATABASES['default']['NAME'])
        path_logs = os.path.join(settings.BASE_DIR, "logs/")
        path_input = os.path.join(settings.BASE_DIR, "scripts/")
        dump_dir = os.path.join(settings.BASE_DIR, "dumps/")

        logs_filename = path_logs+db_name+"_"+os.path.splitext(os.path.basename(__file__))[0] + ".txt"
        f = open(logs_filename, "w", encoding='utf-8')
        f.write("Starting " + logs_filename + str(timezone.now()) + "\n")
        f.write("database_host_name: " + db_host_name + "\n")
        f.write("database_name: " + db_name + "\n")


        DEBUG_WRITE = True
        if(len(args) == 1) and ((args[0] == "load" )):
                record_log_data("y_load_dump_user.py", "tables_to_load", "Starting")
                tables_to_load(f, dump_dir, DEBUG_WRITE)
                record_log_data("y_load_dump_user.py", "tables_to_load", "Completed")
        else:               
                record_log_data("y_load_dump_user.py", "tables_to_dump", "Starting")
                tables_to_dump(f, dump_dir, DEBUG_WRITE)
                record_log_data("y_load_dump_user.py", "tables_to_dump", "Completed")


#If needed - Could force password reset for all users here!

        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()


#default is dump
#python manage.py runscript y_load_dump_user
#python manage.py runscript y_load_dump_user --script-args load