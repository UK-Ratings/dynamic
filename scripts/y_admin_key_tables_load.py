#!/usr/bin/env python3

import os
import csv
import shutil
import pytz

import csv
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")
import django
django.setup()

from django.utils import timezone
from dotenv import load_dotenv

from scripts.x_helper_functions import *



def special_load_a4_minimums_from_file(f, file_path, app_name, table_name, file_format, DEBUG_WRITE):
        f.write("special_load_A4: "
            + " File Path: " + file_path
            + " App_Name: " + app_name
            + " Table_name: " + table_name
            + " File Format: " + file_format
            + " " + str(timezone.now()) + "\n")

        admin_a4_minimums.objects.all().delete()
        timezonee = pytz.timezone('UTC')  # Change 'UTC' to your desired timezone, e.g., 'America/New_York'

        if file_format == 'csv':
                with open(file_path, 'r', newline='') as csvfile:
                        reader = csv.reader(csvfile)
                        next(reader)
                        for row in reader:
                                try:
                                        asn = associations.objects.get(assn_name=row[0])
                                except:
                                        asn = None

                                if asn:
                                        a_event_assn_type = association_types.objects.get(assn = asn, type_category=row[1])
                                        a_event_assn_discipline = association_discipline.objects.get(assn = asn, discipline_name=row[2])
                                        a_event_assn_gender = association_genders.objects.get(assn = asn, gender_name=row[3])
                                        a_event_assn_age_category = association_ages.objects.get(assn = asn, age_category=row[4])
                                        a_nif = row[5]
                                        a_total_fencers = row[6]
                                        a_end_date = datetime.strptime(row[7], '%Y-%m-%d').replace(tzinfo=timezonee)
                                        rec, created = admin_a4_minimums.objects.update_or_create(
                                                a4_assn = asn,
                                                a4_event_assn_type = a_event_assn_type,
                                                a4_event_assn_discipline = a_event_assn_discipline,
                                                a4_event_assn_gender = a_event_assn_gender,
                                                a4_event_assn_age_category = a_event_assn_age_category, 
                                                defaults={'a4_nif': a_nif, 'a4_total_fencers': a_total_fencers, 'a4_end_date': a_end_date})
        else:
                f.write(f"Unsupported file format: {file_format}\n")
                return
        f.write(f"Table {table_name} loaded from {file_path} successfully.\n")

def special_load_a4_minimums_from_permanent(f, DEBUG_WRITE):
        record_log_data("y_load_dump_tables.py", "special_load_a4_minimums_from_permanent", "special_load_a4_minimums_from_permanent starting")
        f.write(f"Loading special_load_a4_minimums_from_permanent.\n")

        admin_a4_minimums.objects.all().delete()
        for x in permanent_admin_a4_minimums.objects.all():

                try:
                        asn = associations.objects.get(assn_name=x.a4_assn_name)
                except:
                        asn = None
                if asn:
                        a_event_assn_type = association_types.objects.get(assn = asn, type_category=x.a4_event_assn_type_name)
                        a_event_assn_discipline = association_discipline.objects.get(assn = asn, discipline_name=x.a4_event_assn_discipline_name)
                        a_event_assn_gender = association_genders.objects.get(assn = asn, gender_name=x.a4_event_assn_gender_name)
                        a_event_assn_age_category = association_ages.objects.get(assn = asn, age_category=x.a4_event_assn_age_category_name)
                        a_nif = x.a4_nif
                        a_total_fencers = x.a4_total_fencers
                        a_end_date = x.a4_end_date
                        rec, created = admin_a4_minimums.objects.update_or_create(
                                a4_assn = asn,
                                a4_event_assn_type = a_event_assn_type,
                                a4_event_assn_discipline = a_event_assn_discipline,
                                a4_event_assn_gender = a_event_assn_gender,
                                a4_event_assn_age_category = a_event_assn_age_category, 
                                defaults={'a4_nif': a_nif, 'a4_total_fencers': a_total_fencers, 'a4_end_date': a_end_date})

def zzzspecial_load_manual_event_final_results_from_permanent(f, DEBUG_WRITE):
        record_log_data("y_load_dump_tables.py", "special_load_manual_event_final_results_from_permanent", "special_load_manual_event_final_results_from_permanent starting")
        f.write(f"Loading special_load_manual_event_final_results_from_permanent.\n")

        def get_tourney(f, asn, DEBUG_WRITE, x):
                cur_tourney = get_tournament(f, DEBUG_WRITE, None, x.pmefr_tourney_name, asn, x.pmefr_tourney_start_date, None, x.pmefr_tourney_inbound)
                if(DEBUG_WRITE):
                        f.write("      Tourney: " + x.pmefr_tourney_name + "\n")
                        if(cur_tourney):
                                f.write("      Found Tourney: " + str(cur_tourney.tourney_name) + " " + str(cur_tourney.tourney_number) + "\n")
                        else:
                                f.write("      Tourney not found: " + x.pmefr_tourney_name + "\n")
                if(cur_tourney):
                        tournaments.objects.filter(tourney_number=cur_tourney.tourney_number).delete()
                cur_tourney = update_or_create_tournament(f, DEBUG_WRITE, None, asn, x.pmefr_tourney_name, 
                                "Completed", x.pmefr_tourney_start_date, x.pmefr_tourney_end_date, 
                                x.pmefr_tourney_end_date, "", "",
                                "", False, "", 
                                "", "Durham", False, sys_user)
                return cur_tourney
        def get_evt(f, asn, DEBUG_WRITE, x, t):
                cur_event = get_event(f, DEBUG_WRITE, cur_tourney, x.pmefr_event_name, None)
                if(DEBUG_WRITE):
                        f.write("         Event: " + x.pmefr_event_name + "\n")
                        if(cur_event):
                                f.write("         Found Event: " + str(cur_event.ev_name) + " " + str(cur_event.ev_number) + "\n")
                        else:
                                f.write("         Event not found: " + x.pmefr_event_name + "\n")
                if(cur_event):
                        events.objects.filter(ev_number=cur_event.ev_number).delete()
                event_assn_type = association_types.objects.get(assn = asn, type_category=x.pmefr_event_assn_type)
                event_assn_discipline = association_discipline.objects.get(assn = asn, discipline_name=x.pmefr_event_assn_discipline)
                event_assn_gender = association_genders.objects.get(assn = asn, gender_name=x.pmefr_event_assn_gender)
                event_assn_age_category = association_ages.objects.get(assn = asn, age_category=x.pmefr_event_assn_ages)

                cur_event = update_or_create_event(f, DEBUG_WRITE, t, None, x.pmefr_event_name, 
                        "Completed", event_assn_type, event_assn_discipline, 
                        event_assn_gender, event_assn_age_category, x.pmefr_event_start_datetime)
                return cur_event

        sys_user = User.objects.get(email='Ftmanageruser@gmail.com')
        asn = None
        cur_tourney = None
        cur_event = None
        for x in permament_manual_event_final_results.objects.all():
                if asn == None or asn.assn_name != x.pmefr_tourney_assn_name:
                        try:
                                asn = associations.objects.get(assn_name=x.pmefr_tourney_assn_name)
                        except:
                                asn = None
                        if(DEBUG_WRITE):
                                f.write("   Association: " + str(asn.assn_name) + "\n")
                if(asn):
                        if(cur_tourney is None or cur_tourney.tourney_name != x.pmefr_tourney_name):
                                cur_tourney = get_tourney(f, asn, DEBUG_WRITE, x)
                        if(cur_tourney):
                                if(cur_event is None or cur_event.ev_name != x.pmefr_event_name):
                                        cur_event = get_evt(f, asn, DEBUG_WRITE, x, cur_tourney)
                                if(cur_event):
                                        update_or_create_event_final_result(f, DEBUG_WRITE, cur_event, None, 
                                                x.pmefr_efr_final_position, x.pmefr_efr_given_name, 
                                                x.pmefr_efr_given_club, x.pmefr_efr_given_member_identifier, 
                                                x.pmefr_assn_member_number)
#        print("loaded from special_load_manual_event_final_results_from_permanent")
        record_log_data("y_load_dump_tables.py", "special_load_manual_event_final_results_from_permanent", "special_load_manual_event_final_results_from_permanent complete")

def special_load_manual_event_final_results_from_file(f, file_path, app_name, table_name, file_format, DEBUG_WRITE):
        record_log_data("y_load_dump_tables.py", "special_load_manual_event_final_results_from_file", "special_load_manual_event_final_results_from_file starting")
        f.write(f"Loading special_load_manual_event_final_results_from_file.\n")

        def get_tourney_file(f, asn, DEBUG_WRITE, x):
                timezonee = pytz.timezone('UTC')  # Change 'UTC' to your desired timezone, e.g., 'America/New_York'
                a_start_date = datetime.fromisoformat(x[3])
                a_end_date = datetime.fromisoformat(x[4])

                cur_tourney = get_tournament(f, DEBUG_WRITE, None, x[1], asn, a_start_date, None, x[2])
                if(DEBUG_WRITE):
                        f.write("      Tourney: " + x[1] + "\n")
                        if(cur_tourney):
                                f.write("      Found Tourney: " + str(cur_tourney.tourney_name) + " " + str(cur_tourney.tourney_number) + "\n")
                        else:
                                f.write("      Tourney not found: " + x[1] + "\n")
                if(cur_tourney):
                        tournaments.objects.filter(tourney_number=cur_tourney.tourney_number).delete()
                cur_tourney = update_or_create_tournament(f, DEBUG_WRITE, None, asn, x[1], 
                                "Completed", a_start_date, a_end_date, 
                                a_end_date, "", "",
                                "", False, "", 
                                "", "Durham", False, sys_user)
                return cur_tourney

        def get_evt_file(f, asn, DEBUG_WRITE, x, t):
                timezonee = pytz.timezone('UTC')  # Change 'UTC' to your desired timezone, e.g., 'America/New_York'
                a_start_date = datetime.fromisoformat(x[6])

                cur_event = get_event(f, DEBUG_WRITE, cur_tourney, x[5], None)
                if(DEBUG_WRITE):
                        f.write("         Event: " + x[5] + "\n")
                        if(cur_event):
                                f.write("         Found Event: " + str(cur_event.ev_name) + " " + str(cur_event.ev_number) + "\n")
                        else:
                                f.write("         Event not found: " + x[5] + "\n")
                if(cur_event):
                        events.objects.filter(ev_number=cur_event.ev_number).delete()
                event_assn_type = association_types.objects.get(assn = asn, type_category=x[8])
                event_assn_discipline = association_discipline.objects.get(assn = asn, discipline_name=x[9])
                event_assn_gender = association_genders.objects.get(assn = asn, gender_name=x[10])
                event_assn_age_category = association_ages.objects.get(assn = asn, age_category=x[11])

                cur_event = update_or_create_event(f, DEBUG_WRITE, t, None, x[5], 
                        "Completed", event_assn_type, event_assn_discipline, 
                        event_assn_gender, event_assn_age_category, a_start_date)
                return cur_event

        sys_user = User.objects.get(email='Ftmanageruser@gmail.com')
        asn = None
        cur_tourney = None
        cur_event = None

        permament_manual_event_final_results.objects.all().delete()

        if file_format == 'csv':
                if os.path.exists(file_path):
                        with open(file_path, 'r', newline='') as csvfile:
                                reader = csv.reader(csvfile)
                                next(reader)
                                last_asn = None
                                for row in reader:
                                        asn = get_association(f, row[0], DEBUG_WRITE)
                                        if(DEBUG_WRITE):
                                                f.write("   Association: " + str(asn.assn_name) + "\n")
                                        if(last_asn != asn):
                                                assn_recs = association_members.objects.filter(assn = asn).values_list('assn_member_full_name', flat=True)
                                        last_asn = asn
                                        if(asn is not None):
                                                if(cur_tourney is None or cur_tourney.tourney_name != row[1]):
                                                        cur_tourney = get_tourney_file(f, asn, DEBUG_WRITE, row)
                                                if(cur_tourney):
                                                        if(cur_event is None or cur_event.ev_name != row[5]):
                                                                cur_event = get_evt_file(f, asn, DEBUG_WRITE, row, cur_tourney)
                                                        if(cur_event):
                                                                amr = get_assn_member_record(f, asn, assn_recs, row[14], row[15], "", "", False)
                                                                if amr is not None:
                                                                        assn_mbr_num = amr.assn_member_number
                                                                else:
                                                                        assn_mbr_num = 0
                                                                update_or_create_event_final_result(f, DEBUG_WRITE, cur_event, None, 
                                                                        row[13], row[15], 
                                                                        row[16], row[14], assn_mbr_num)   

                                                                rec, created = permament_manual_event_final_results.objects.update_or_create(
                                                                        pmefr_tourney_assn_name = row[0],
                                                                        pmefr_tourney_name = row[1],
                                                                        pmefr_tourney_inbound = row[2],
                                                                        pmefr_tourney_start_date = row[3],
                                                                        pmefr_tourney_end_date = row[4],
                                                                        pmefr_event_name = row[5],
                                                                        pmefr_event_start_datetime = row[6],
                                                                        pmefr_event_status = row[7],
                                                                        pmefr_event_assn_type = row[8],
                                                                        pmefr_event_assn_discipline = row[9],
                                                                        pmefr_event_assn_gender = row[10],
                                                                        pmefr_event_assn_ages = row[11],
                                                                        pmefr_assn_member_number = assn_mbr_num,
                                                                        pmefr_efr_final_position = row[13],
                                                                        pmefr_efr_given_member_identifier = row[14],
                                                                        pmefr_efr_given_name = row[15],
                                                                        pmefr_efr_given_club = row[16]
                                                                        )
                                                                ev_fencers = event_final_results.objects.filter(efr_event = cur_event).count()
                                                                if ev_fencers > 0:
                                                                        update_or_create_event_extra_field(f, cur_event, 'Fencers', ev_fencers, False)
                else:
                        f.write(f"File {file_path} does not exist.")
        else:
                f.write(f"Unsupported file format: {file_format}\n")
        f.write(f"Completed loading special_load_manual_event_final_results_from_file.\n")
        record_log_data("y_load_dump_tables.py", "special_load_manual_event_final_results_from_file", "special_load_manual_event_final_results_from_file starting")

def special_load_permanent_admin_hide_event_from_file(f, file_path, app_name, table_name, file_format, DEBUG_WRITE):
        f.write("special_load_permanent_admin_hide_event_from_file: "
            + " File Path: " + file_path
            + " App_Name: " + app_name
            + " Table_name: " + table_name
            + " File Format: " + file_format
            + " " + str(timezone.now()) + "\n")

        admin_hide_event.objects.all().delete()

        if file_format == 'csv':
                with open(file_path, 'r', newline='') as csvfile:
                        reader = csv.reader(csvfile)
                        next(reader)
                        for row in reader:
                                try:
                                        asn = associations.objects.get(assn_name=row[0])
                                except:
                                        asn = None
                                try:
                                        eve = events.objects.get(ev_tourney__tourney_assn=asn, ev_tourney__tourney_name__iexact=row[1], ev_name__iexact=row[5])
                                except:
                                        eve = None
                                if asn and eve:
                                        rec, created = admin_hide_event.objects.update_or_create(
                                                hide_event = eve,
                                                defaults={
                                                        'hide_from_listings': row[6],
                                                        'hide_from_ratings_calc': eval(row[7]),
#                                                        'hide_user': eval(row[8]),
                                                        'hide_update_date': timezone.now()
                                                })
                                else:
                                        f.write(f"Association or Event not found: {row[0]} {row[1]} {row[5]}\n")

        else:
                f.write(f"Unsupported file format: {file_format}\n")
                return
        f.write(f"Table {table_name} loaded from {file_path} successfully.\n")

def special_load_permanent_admin_hide_event_from_permanent(f, DEBUG_WRITE):
        f.write("special_load_permanent_admin_hide_event_from_permanent: "
            + " " + str(timezone.now()) + "\n")

        admin_hide_event.objects.all().delete()

        for x in permanent_admin_hide_event.objects.all():
                try:
                        asn = associations.objects.get(assn_name=x.hide_tourney_assn_name)
                except:
                        asn = None
                try:
                        eve = events.objects.get(ev_tourney__tourney_assn=asn, ev_tourney__tourney_name__iexact=x.hide_tourney_name, ev_name__iexact=x.hide_event_name)
                except:
                        eve = None
                if asn and eve:
                        rec, created = admin_hide_event.objects.update_or_create(
                                hide_event = eve,
                                defaults={
                                        'hide_from_listings': x.hide_from_listings,
                                        'hide_from_ratings_calc': x.hide_from_ratings_calc,
                                        'hide_user': x.hide_user,
                                        'hide_update_date': timezone.now()
                                })
                else:
                        f.write(f"Association or Event not found: {x.hide_tourney_assn_name} {x.hide_tourney_name} {x.hide_event_name}\n")

def load_userdata_from_files(f, user_file_path, profile_file_path, DEBUG_WRITE):
        f.write("load_table_from_file: " + " File Path: " + user_file_path
            + " File Path: " + profile_file_path + " " + str(timezone.now()) + "\n")

        ProdUser.objects.all().delete()
        ProdProfile.objects.all().delete()

        asn = get_association(f, 'British Fencing', DEBUG_WRITE)

        weird_id = False
        if os.environ.get("AZURE_DB") is not None:
                if(os.environ.get("AZURE_DB") == 'local'):
                        weird_id = True


        if asn is not None:
                profile_data = []
                if os.path.exists(profile_file_path):
                        with open(profile_file_path, 'r', newline='') as profilecsvfile:
                                reader = csv.DictReader(profilecsvfile)
                                for row in reader:
#                                        print(row)
                                        profile_data.append(row)
                else:
                        f.write(f"File {user_file_path} does not exist.")

                if os.path.exists(user_file_path):
                        with open(user_file_path, 'r', newline='') as usercsvfile:
                                reader = csv.DictReader(usercsvfile)
                                for row in reader:
#                                        print(row)
                                        user, created = User.objects.get_or_create(email=row['email'], 
                                                                        defaults={'first_name': row['first_name'], 'last_name': row['last_name'], 
                                                                                'is_staff': False, 'is_superuser': False})
                                        if created:
                                                user.set_password(row['password'])
                                                user.save()
        #                                print(user, created)
                                        for qq in profile_data:
                                                if(weird_id):
                                                        if(qq['ï»¿id'] == row['ï»¿id']):
                                                                if(len(qq['bf_license_given']) > 0):
        #                                                                print('found',qq['bf_license_given'])
                                                                        amr = None
                                                                        if asn is not None:
                                                                                amr = get_assn_member_record_by_assn_assn_member_identifier(f, asn, qq['bf_license_given'], DEBUG_WRITE)
                                                                        if amr is not None and user is not None:
                                                                                upp, created = custom_user_assn_memberships.objects.update_or_create(
                                                                                        cuser=user, cuser_assn_member=amr)
        #                                                                        print(upp, created)
                                                else:
                                                        if(qq["\ufeffid"] == row["\ufeffid"]):
                                                                if(len(qq['bf_license_given']) > 0):
        #                                                                print('found',qq['bf_license_given'])
                                                                        amr = None
                                                                        if asn is not None:
                                                                                amr = get_assn_member_record_by_assn_assn_member_identifier(f, asn, qq['bf_license_given'], DEBUG_WRITE)
                                                                        if amr is not None and user is not None:
                                                                                upp, created = custom_user_assn_memberships.objects.update_or_create(
                                                                                        cuser=user, cuser_assn_member=amr)
        #                                                                        print(upp, created)

                else:
                        f.write(f"File {user_file_path} does not exist.")

        f.write("Complete: load_table_from_file: " + " File Path: " + user_file_path
            + " File Path: " + profile_file_path + " " + str(timezone.now()) + "\n")

def load_table_from_file(f, file_path, app_name, table_name, file_format, DEBUG_WRITE):
    f.write("load_table_from_file: "
            + " File Path: " + file_path
            + " App_Name: " + app_name
            + " Table_name: " + table_name
            + " File Format: " + file_format
            + " " + str(timezone.now()) + "\n")
    try:
        model = apps.get_model(app_name, table_name)
    except LookupError:
        f.write(f"Table {table_name} does not exist.\n")
        return
    model.objects.all().delete()
    if file_format == 'csv':
        # Read from CSV file
        if os.path.exists(file_path):
            with open(file_path, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    print(row)
                    model.objects.create(**row)
        else:
            f.write(f"File {file_path} does not exist.")
    else:
        f.write(f"Unsupported file format: {file_format}\n")
        return
    f.write(f"Table {table_name} loaded from {file_path} successfully.\n")
def load_permanent_to_models(f, copy_table, DEBUG_WRITE):
        record_log_data("y_load_dump_tables.py", "load_permanent_to_models", "permanent_to_models starting")
        f.write(f"load_permanent_to_models Table {copy_table}.\n")

        if(copy_table == 'admin_modified_event_final_results'):
                admin_modified_event_final_results.objects.all().delete()
                for x in permanent_admin_modified_event_final_results.objects.all():
                        admin_modified_event_final_results.objects.create(
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
        if(copy_table == 'admin_deleted_tournaments'):
                admin_deleted_tournaments.objects.all().delete()
                for x in permanent_admin_deleted_tournaments.objects.all():
                        admin_deleted_tournaments.objects.create(
                                adt_tourney_assn_name = x.adt_tourney_assn_name,
                                adt_tourney_name = x.adt_tourney_name,
                                adt_tourney_inbound = x.adt_tourney_inbound,
                                adt_tourney_start_date = x.adt_tourney_start_date,
                                adt_tourney_end_date = x.adt_tourney_end_date,
                                adt_date_deleted = x.adt_date_deleted
                        )

        if(copy_table == 'admin_deleted_events'):
                admin_deleted_events.objects.all().delete()
                for x in permanent_admin_deleted_events.objects.all():
                        admin_deleted_events.objects.create(               
                                ade_tourney_assn_name = x.ade_tourney_assn_name,
                                ade_tourney_name = x.ade_tourney_name,
                                ade_tourney_inbound = x.ade_tourney_inbound,
                                ade_tourney_start_date = x.ade_tourney_start_date,
                                ade_tourney_end_date = x.ade_tourney_end_date,
                                ade_event_name = x.ade_event_name,
                                ade_delete_date = x.ade_delete_date
                        )

        record_log_data("y_load_dump_tables.py", "load_permanent_to_models", "models_to_permanent completed")
def tables_to_load(f, dump_dir, DEBUG_WRITE):

        l_tables = []
        l_tables.append([dump_dir + "admin_deleted_tournaments" + "_dump.csv",'tourneys','admin_deleted_tournaments', 'csv'])
        l_tables.append([dump_dir + "admin_deleted_events" + "_dump.csv", 'tourneys','admin_deleted_events', 'csv'])
        l_tables.append([dump_dir + "admin_modified_event_final_results" + "_dump.csv", 'tourneys','admin_modified_event_final_results', 'csv'])
        l_tables.append([dump_dir + "admin_corrects_disciplines" + "_dump.csv", 'tourneys','admin_corrects_disciplines', 'csv'])
        l_tables.append([dump_dir + "admin_corrects_genders" + "_dump.csv", 'tourneys','admin_corrects_genders', 'csv'])

        load_userdata_from_files(f, dump_dir + "prod_users" + "_dump.csv", dump_dir + "prod_profile" + "_dump.csv", DEBUG_WRITE)

        for x in l_tables:
                perm_recs_exist = True
                try:
                        model = apps.get_model('base', 'permanent_'+x[2])
                except LookupError:
                        perm_recs_exist = False
                else:
                       if(model.objects.all().count() == 0):
                              perm_recs_exist = False
#                print(x[1], x[2], perm_recs_exist)
                if(perm_recs_exist):
                        load_permanent_to_models(f, x[2], DEBUG_WRITE)
                else:
                        print('load_table_from_file', x[0], x[1], x[2], x[3], DEBUG_WRITE)
                        load_table_from_file(f, x[0], x[1],x[2], x[3], DEBUG_WRITE)
        if(1==1):
                try:
                        permanent_admin_a4_minimums.objects.all()
                except:
                        f.write("ERROR - Permanent table does not exist: permanent_admin_a4_minimums\n")
                else:
                        special_load_a4_minimums_from_permanent(f, DEBUG_WRITE)
                        if(permanent_admin_a4_minimums.objects.all().count() == 0):
                                special_load_a4_minimums_from_file(f, dump_dir + "admin_a4_minimums" + "_dump.csv",'assn_mgr','admin_a4_minimums', 'csv', DEBUG_WRITE)
                try:
                        permament_manual_event_final_results.objects.all()
                except:
                        f.write("ERROR - Permanent table does not exist: permament_manual_event_final_results\n")
                else:
                        cnt = permament_manual_event_final_results.objects.all().count()
                        special_load_manual_event_final_results_from_file(f, dump_dir + "permament_manual_event_final_results" + "_dump.csv",'assn_mgr','admin_a4_minimums', 'csv', DEBUG_WRITE)
                        f.write("Loaded from special_load_manual_event_final_results_from_file\n")
                try:
                        permanent_admin_hide_event.objects.all()
                except:
                        f.write("ERROR - Permanent table does not exist: permanent_admin_hide_event\n")
                else:
                        cnt = permanent_admin_hide_event.objects.all().count()
                        special_load_permanent_admin_hide_event_from_file(f, dump_dir + "permanent_admin_hide_event" + "_dump.csv",'assn_mgr','admin_a4_minimums', 'csv', DEBUG_WRITE)
                        f.write("Loaded from special_load_permanent_admin_hide_event_from_file\n")


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

        record_log_data("y_admin_key_tables_load.py", "tables_to_load", "Starting")
        tables_to_load(f, dump_dir, DEBUG_WRITE)
        record_log_data("y_admin_key_tables_load.py", "tables_to_load", "Completed")

        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()


#python manage.py runscript y_admin_key_tables_load

