#!/usr/bin/env python3

import os
import csv
import shutil
import pytz

import csv
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")
import django
django.setup()

from django.utils import timezone
from dotenv import load_dotenv


from scripts.x_helper_functions import *
from tourneys.models import *






def dump_table_admin_a4_minimums(f, dump_directory, app_name, table_name, file_format, DEBUG_WRITE):
        f.write("dump_table_admin_a4_minimums: " 
                + " Directory: " + dump_directory
                + " App_Name: " + app_name
                + " Table_name: " + table_name
                + " File Format: " + file_format
                + " " + str(timezone.now()) + "\n")
        if file_format == 'csv':
                records = []
                for x in admin_a4_minimums.objects.all():
                        records.append([
                                x.a4_assn.assn_name,
                                x.a4_event_assn_type.type_category,
                                x.a4_event_assn_discipline.discipline_name,
                                x.a4_event_assn_gender.gender_name,
                                x.a4_event_assn_age_category.age_category,
                                x.a4_nif,
                                x.a4_total_fencers,
                                x.a4_end_date.strftime('%Y-%m-%d') if x.a4_end_date else ''
                                ])        
                dump_records_to_file(f, dump_directory, app_name, table_name, file_format, records, DEBUG_WRITE)
        else:
                f.write("Unsupported file format: " + file_format + "\n")
                return
        f.write(" Completed dump_table_admin_a4_minimums: " + str(timezone.now()) + "\n")
def dump_tables(f, dump_dir, DEBUG_WRITE):
        os.makedirs(dump_dir, exist_ok=True)        
        delete_files_in_directory_by_extension(f, dump_dir, 'csv')
#        delete_all_files_in_directory(f, dump_dir)

        #This is because admin_a4_minimums requires base data relationships.  Other do not
        dump_table_admin_a4_minimums(f, dump_dir, 'assn_mgr','admin_a4_minimums', 'csv', DEBUG_WRITE)

        d_tables = []
        d_tables.append([dump_dir, 'tourneys','admin_corrects_disciplines', 'csv'])
        d_tables.append([dump_dir, 'tourneys','admin_corrects_genders', 'csv'])
        d_tables.append([dump_dir, 'tourneys','admin_deleted_tournaments', 'csv'])
        d_tables.append([dump_dir, 'tourneys','admin_deleted_events', 'csv'])
        d_tables.append([dump_dir, 'tourneys','admin_modified_event_final_results', 'csv'])
        d_tables.append([dump_dir, 'base','permanent_admin_hide_event', 'csv'])
        d_tables.append([dump_dir, 'tourneys','permament_manual_event_final_results', 'csv'])

        attachments = []
        for x in d_tables:
                dump_table_to_file(f, x[0], x[1], x[2], x[3], DEBUG_WRITE)
                attachments.append(x[0] + x[2] + "_dump." + x[3])
        attachments.append(dump_dir + "admin_a4_minimums_dump.csv")
        
        recipient_list = [os.environ.get("EMAIL_LOGS_USERNAME")]

        db_settings = settings.DATABASES['default']
        db_server = db_settings['HOST']
        db_name = db_settings['NAME']

        subjectline = db_name + " " + db_server + " --- Key Tables"
        send_email_with_attachments(f, subjectline, "This is a failsafe", recipient_list, attachments, DEBUG_WRITE)

def models_to_permanent(f, DEBUG_WRITE):
        record_log_data("y_load_dump_tables.py", "models_to_permanent", "models_to_permanent starting")

        permanent_admin_modified_event_final_results.objects.all().delete()
        for x in admin_modified_event_final_results.objects.all():
               permanent_admin_modified_event_final_results.objects.create(
                        amefr_tourney_assn_name = x.amefr_tourney_assn_name,
                        amefr_tourney_name = x.amefr_tourney_name, 
                        amefr_tourney_inbound = x.amefr_tourney_inbound, 
                        amefr_tourney_start_date = x.amefr_tourney_start_date,
                        amefr_tourney_end_date = x.amefr_tourney_end_date, 
                        amefr_event_name = x.amefr_event_name, 
                        amefr_orig_assn_member_number = x.amefr_orig_assn_member_number, 
                        amefr_new_assn_member_number = x.amefr_new_assn_member_number, 
                        amefr_efr_final_position = x.amefr_efr_final_position, 
                        amefr_orig_efr_given_member_identifier = x.amefr_orig_efr_given_member_identifier, 
                        amefr_new_efr_given_member_identifier = x.amefr_new_efr_given_member_identifier, 
                        amefr_orig_efr_given_name = x.amefr_orig_efr_given_name, 
                        amefr_new_efr_given_name = x.amefr_new_efr_given_name, 
                        amefr_orig_efr_given_club = x.amefr_orig_efr_given_club, 
                        amefr_new_efr_given_club = x.amefr_new_efr_given_club, 
                        amefr_modified_date = x.amefr_modified_date, 
                        amefr_user = x.amefr_user.name
                       )

        permanent_admin_deleted_tournaments.objects.all().delete()
        for x in admin_deleted_tournaments.objects.all():
                permanent_admin_deleted_tournaments.objects.create(
                        adt_tourney_assn_name = x.adt_tourney_assn_name,
                        adt_tourney_name = x.adt_tourney_name,
                        adt_tourney_inbound = x.adt_tourney_inbound,
                        adt_tourney_start_date = x.adt_tourney_start_date,
                        adt_tourney_end_date = x.adt_tourney_end_date,
                        adt_date_deleted = x.adt_date_deleted
                )

        permanent_admin_deleted_events.objects.all().delete()
        for x in admin_deleted_events.objects.all():
                permanent_admin_deleted_events.objects.create(               
                        ade_tourney_assn_name = x.ade_tourney_assn_name,
                        ade_tourney_name = x.ade_tourney_name,
                        ade_tourney_inbound = x.ade_tourney_inbound,
                        ade_tourney_start_date = x.ade_tourney_start_date,
                        ade_tourney_end_date = x.ade_tourney_end_date,
                        ade_event_name = x.ade_event_name,
                        ade_delete_date = x.ade_delete_date
                )

        permanent_admin_hide_event.objects.all().delete()
        for x in admin_hide_event.objects.all():
                permanent_admin_hide_event.objects.create(               
                        hide_tourney_assn_name = x.hide_event.ev_tourney.tourney_assn.assn_name,
                        hide_tourney_name = x.hide_event.ev_tourney.tourney_name,
                        hide_tourney_inbound = x.hide_event.ev_tourney.tourney_inbound,
                        hide_tourney_start_date = x.hide_event.ev_tourney.tourney_start_date,
                        hide_tourney_end_date = x.hide_event.ev_tourney.tourney_end_date,
                        hide_event_name = x.hide_event.ev_name,
                        hide_from_listings = x.hide_from_listings,
                        hide_from_ratings_calc = x.hide_from_ratings_calc,
                        hide_user = x.hide_user,
                        hide_update_date = x.hide_update_date
                )

        permanent_admin_a4_minimums.objects.all().delete()
        for x in admin_a4_minimums.objects.all():
                permanent_admin_a4_minimums.objects.create(               
                        a4_assn_name = x.a4_assn.assn_name,
                        a4_event_assn_type_name = x.a4_event_assn_type.type_category,
                        a4_event_assn_discipline_name = x.a4_event_assn_discipline.discipline_name,
                        a4_event_assn_gender_name = x.a4_event_assn_gender.gender_name,
                        a4_event_assn_age_category_name = x.a4_event_assn_age_category.age_category,
                        a4_nif = x.a4_nif,
                        a4_total_fencers = x.a4_total_fencers,
                        a4_end_date = x.a4_end_date
                )
        record_log_data("y_load_dump_tables.py", "models_to_permanent", "models_to_permanent completed")

def manual_tournaments_to_permanent(f, DEBUG_WRITE):
        record_log_data("y_load_dump_tables.py", "manual_tournaments_to_permanent", "manual_tournaments_to_permanent starting")

        permament_manual_event_final_results.objects.all().delete()

        for x in event_final_results.objects.filter(efr_event__ev_tourney__tourney_inbound__contains='Durham'):
                if(DEBUG_WRITE):
                        f.write("processing: " + x.efr_event.ev_tourney.tourney_name 
                                + " " + x.efr_event.ev_name + " " + str(x.efr_final_position) 
                                + " " + x.efr_given_name + "\n")
#                        print("processing: ", x.efr_event.ev_tourney.tourney_name, x.efr_given_name)
                permament_manual_event_final_results.objects.create(
                        pmefr_tourney_assn_name = x.efr_event.ev_tourney.tourney_assn.assn_name,
                        pmefr_tourney_name = x.efr_event.ev_tourney.tourney_name,
                        pmefr_tourney_inbound = x.efr_event.ev_tourney.tourney_inbound,
                        pmefr_tourney_start_date = x.efr_event.ev_tourney.tourney_start_date,
                        pmefr_tourney_end_date = x.efr_event.ev_tourney.tourney_end_date,
                        pmefr_event_name = x.efr_event.ev_name,
                        pmefr_event_start_datetime = x.efr_event.ev_start_date,
                        pmefr_event_status = x.efr_event.ev_status.status,
                        pmefr_event_assn_type = x.efr_event.ev_assn_type.type_category,
                        pmefr_event_assn_discipline = x.efr_event.ev_assn_discipline.discipline_name,
                        pmefr_event_assn_gender = x.efr_event.ev_assn_gender.gender_name,
                        pmefr_event_assn_ages = x.efr_event.ev_assn_ages.age_category,
                        pmefr_assn_member_number = x.efr_assn_member_number,
                        pmefr_efr_final_position = x.efr_final_position,
                        pmefr_efr_given_member_identifier = x.efr_given_member_identifier,
                        pmefr_efr_given_name = x.efr_given_name,
                        pmefr_efr_given_club = x.efr_given_club
                        )

        record_log_data("y_load_dump_tables.py", "manual_tournaments_to_permanent", "manual_tournaments_to_permanent completed")


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

        record_log_data("y_admin_key_tables_backup.py", "models_to_permanent", "Starting")
        models_to_permanent(f, DEBUG_WRITE)
        record_log_data("y_admin_key_tables_backup.py", "models_to_permanent", "Completed")

        record_log_data("y_admin_key_tables_backup.py", "manual_tournaments_to_permanent", "Starting")
        manual_tournaments_to_permanent(f, DEBUG_WRITE)
        record_log_data("y_admin_key_tables_backup.py", "manual_tournaments_to_permanent", "Completed")

        record_log_data("y_admin_key_tables_backup.py", "tables_to_dump", "Starting")
        dump_tables(f, dump_dir, DEBUG_WRITE)
        record_log_data("y_admin_key_tables_backup.py", "tables_to_dump", "Completed")

        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()


#python manage.py runscript y_admin_key_tables_backup

