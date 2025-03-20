#!/usr/bin/env python3

from base.models import *
from django.utils import timezone
from django.contrib import messages
from decouple import config

from club_mgr.models import *
from assn_mgr.models import *
from integrations.models import *
from tourneys.models import *
from scripts import y_admin_key_tables_load

import os
import inspect
from dotenv import load_dotenv
from scripts.x_helper_functions import copy_zbackup_files_if_exist, record_log_data, get_association
from scripts.x_helper_assn_specific import BF_Create_Assn
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")


def clear_loading_tables():
        load_lpjs_competitions_results.objects.all().delete()
        load_lpjs_competitions_results_events.objects.all().delete()
        load_lpjs_competitions_results_events_fencers.objects.all().delete()
        load_engarde_event.objects.all().delete()
        load_engarde_final_results.objects.all().delete()
        load_s80_fencing_competitions.objects.all().delete()
        load_s80_fencing_competitions_series.objects.all().delete()
        load_s80_fencing_events_category.objects.all().delete()
        load_s80_fencing_events.objects.all().delete()
        load_s80_fencing_fencing_results.objects.all().delete()
        load_s80_upcoming_tournaments.objects.all().delete()
        load_s80_upcoming_tournaments_entries.objects.all().delete()
        load_s80_upcoming_tournaments_entries_fencers.objects.all().delete()
        load_ftl_tournaments.objects.all().delete()
        load_ftl_tournament_events.objects.all().delete()
        load_ftl_event_rounds.objects.all().delete()
        load_ftl_round_seeding.objects.all().delete()
        load_ftl_pool_round_pool.objects.all().delete()
        load_ftl_round_pool_results.objects.all().delete()
        load_ftl_round_pool_scores.objects.all().delete()
        load_ftl_elimination_scores.objects.all().delete()
        load_ftl_event_final_results.objects.all().delete()
        bf_member_rank_points.objects.all().delete()
        s80_load_membership_records_clubs.objects.all().delete()
        s80_load_membership_records.objects.all().delete()
        s80_load_club_records.objects.all().delete()
        load_engarde_final_results.objects.all().delete()
        log_progress_data.objects.all().delete()
        load_s80_upcoming_tournaments_entries_fencers.objects.all().delete()

def base_clear_tables():
        if(1==1): #clear base tables
                log_progress_data.objects.all().delete()
                log_error_data.objects.all().delete()
                log_messages.objects.all().delete()
                record_log_data("x_reset_system.py", "base_clear_tables", "Clearing Tables")
                custom_user_assn_memberships.objects.all().delete()
        if(1==1):  #clear club tables
                club_members.objects.all().delete()
                club_assn_clubs.objects.all().delete()
                club_assn.objects.all().delete()
                club_admins.objects.all().delete()
                club_ages.objects.all().delete()
                club_disciplines.objects.all().delete()
                club_address.objects.all().delete()
                club_extra_fields.objects.all().delete()
                clubs.objects.all().delete()
        if(1==1):  #clear tournament tables
                event_round_pool_results.objects.all().delete()
                tournament_status.objects.all().delete()
                event_status.objects.all().delete()
                tournaments.objects.all().delete()
                tournament_address.objects.all().delete()
                tournament_notes.objects.all().delete()
                events.objects.all().delete()
                event_extra_fields.objects.all().delete()
                event_final_results.objects.all().delete()
                event_final_results_extra_fields.objects.all().delete()
                tournament_admins.objects.all().delete()
                tournament_ages.objects.all().delete()
                tournament_geography.objects.all().delete()
                tournament_types.objects.all().delete()
        if(1==1):  #clear association tables
                association_member_extra_fields.objects.all().delete()
                association_member_address.objects.all().delete()
                association_club_admins.objects.all().delete()
                association_club_ages.objects.all().delete()
                association_club_disciplines.objects.all().delete()
                association_clubs.objects.all().delete()
                association_club_extra_fields.objects.all().delete()
                association_club_address.objects.all().delete()
                association_club_members.objects.all().delete()
                association_extra_fields.objects.all().delete()
                association_ages.objects.all().delete()
                association_geographies.objects.all().delete()
                association_types.objects.all().delete()
                association_discipline.objects.all().delete()
                association_genders.objects.all().delete()
                association_countries.objects.all().delete()
                association_tournament_extra_fields.objects.all().delete()
                association_event_extra_fields.objects.all().delete()
                association_event_final_results_extra_fields.objects.all().delete()
                association_members.objects.all().delete()
                associations.objects.all().delete()
                s80_membership_records.objects.all().delete()
                s80_club_records.objects.all().delete()
                s80_membership_records_clubs.objects.all().delete()
                user_member_to_watch.objects.all().delete()
        if(1==1):  #clear rest of base data
                Profile.objects.all().delete()
                language.objects.all().delete()
                system_values.objects.all().delete()
                user_role.objects.all().delete()
                address.objects.all().delete()
                admin_modified_event_final_results.objects.all().delete()
                admin_deleted_events.objects.all().delete()
                admin_deleted_tournaments.objects.all().delete()
                log_page_data.objects.all().delete()
                User.objects.all().delete()
        if(1==1): #clear permanent tables
                permanent_admin_deleted_events.objects.all().delete()
                permanent_admin_deleted_tournaments.objects.all().delete()
                permanent_admin_hide_event.objects.all().delete()
                permanent_admin_modified_event_final_results.objects.all().delete()
                permanent_admin_a4_minimums.objects.all().delete()
                permament_manual_event_final_results.objects.all().delete()

def base_reset_system_variables():
    record_log_data("x_reset_system.py", "base_reset_system_variables", "Resetting system variables")

    if(1==1):  #load languages
        lg = language(language_name='English', language_code='en-us', language_active=True)    
        lg.save()
        lg = language(language_name='French', language_code='fr', language_active=True)    
        lg.save()
        lg = language(language_name='Spanish', language_code='es', language_active=True)    
        lg.save()
        lg_id = language.objects.get(language_code='en-us')
        sv = system_values(value_name='default_language',value_language=lg_id)
        sv.save()
    if(1==1):  #load base system values
        sv = system_values(value_name='next_tournament_id',value_int=config('BASE_STARTING_ID_TOURNAMENT'))
        sv.save()
        sv = system_values(value_name='next_event_id',value_int=config('BASE_STARTING_ID_EVENT'))
        sv.save()
        sv = system_values(value_name='next_club_id',value_int=config('BASE_STARTING_ID_CLUB'))
        sv.save()
        sv = system_values(value_name='next_user_id',value_int=config('BASE_STARTING_ID_USER'))
        sv.save()
        sv = system_values(value_name='next_assn_id',value_int=config('BASE_ASSN_STARTING_ID'))
        sv.save()
        sv = system_values(value_name='next_assn_member_id',value_int=config('BASE_ASSN_MEMBER_STARTING_ID'))
        sv.save()
        sv = system_values(value_name='next_assn_club_id',value_int=config('BASE_STARTING_ID_ASSN_CLUB'))
        sv.save()
        sv = system_values(value_name='next_upcoming_tournament_id',value_int=config('BASE_STARTING_ID_UPCOMING_TOURNAMENT'))
        sv.save()
        sv = system_values(value_name='next_upcoming_event_id',value_int=config('BASE_STARTING_ID_UPCOMING_EVENT'))
        sv.save()
        sv = system_values(value_name='next_event_round_id',value_int=config('BASE_STARTING_EVENT_ROUND_ID'))
        sv.save()
        sv = system_values(value_name='next_event_pool_id',value_int=config('BASE_STARTING_EVENT_POOL_ID'))
        sv.save()
    if(1==1):  #load categories
        lg_id = language.objects.get(language_code='en-us')

        sv = system_values(value_group = 'category', value_name='all_ages', value_string = 'All Ages', value_language=lg_id).save()
        sv = system_values(value_group = 'category', value_name='under_5', value_string = 'Under 5', value_language=lg_id).save()
        sv = system_values(value_group = 'category', value_name='under_6', value_string = 'Under 6', value_language=lg_id).save()
        sv = system_values(value_group = 'category', value_name='under_7', value_string = 'Under 7', value_language=lg_id).save()
        sv = system_values(value_group = 'category', value_name='under_8', value_string = 'Under 8', value_language=lg_id).save()
        sv = system_values(value_group = 'category', value_name='under_9', value_string = 'Under 9', value_language=lg_id).save()
        sv = system_values(value_group = 'category', value_name='under_10', value_string = 'Under 10', value_language=lg_id).save()
        sv = system_values(value_group = 'category', value_name='under_11', value_string = 'Under 11', value_language=lg_id).save()
        sv = system_values(value_group = 'category', value_name='under_12', value_string = 'Under 12', value_language=lg_id).save()
        sv = system_values(value_group = 'category', value_name='under_13', value_string = 'Under 13', value_language=lg_id).save()
        sv = system_values(value_group = 'category', value_name='under_14', value_string = 'Under 14', value_language=lg_id).save()
        sv = system_values(value_group = 'category', value_name='under_15', value_string = 'Under 15', value_language=lg_id).save()
        sv = system_values(value_group = 'category', value_name='under_16', value_string = 'Under 16', value_language=lg_id).save()
        sv = system_values(value_group = 'category', value_name='under_17', value_string = 'Under 17', value_language=lg_id).save()
        sv = system_values(value_group = 'category', value_name='under_18', value_string = 'Under 18', value_language=lg_id).save()
        sv = system_values(value_group = 'category', value_name='under_19', value_string = 'Under 19', value_language=lg_id).save()
        sv = system_values(value_group = 'category', value_name='under_20', value_string = 'Under 20', value_language=lg_id).save()
        sv = system_values(value_group = 'category', value_name='under_21', value_string = 'Under 21', value_language=lg_id).save()
        sv = system_values(value_group = 'category', value_name='under_22', value_string = 'Under 22', value_language=lg_id).save()
        sv = system_values(value_group = 'category', value_name='under_23', value_string = 'Under 23', value_language=lg_id).save()

        sv = system_values(value_group = 'category', value_name='over_16', value_string = 'Over 16', value_language=lg_id).save()

        sv = system_values(value_group = 'category', value_name='cadet', value_string = 'Cadet', value_language=lg_id).save()
        sv = system_values(value_group = 'category', value_name='junior', value_string = 'Junior', value_language=lg_id).save()
        sv = system_values(value_group = 'category', value_name='senior', value_string = 'Senior', value_language=lg_id).save()
        sv = system_values(value_group = 'category', value_name='veteran', value_string = 'Veteran', value_language=lg_id).save()
        sv = system_values(value_group = 'category', value_name='unknown', value_string = 'Unknown', value_language=lg_id).save()

    if(1==1):  #load event types
        lg_id = language.objects.get(language_code='en-us')
        sv = system_values(value_group = 'event_type', value_name='individual', value_string = 'Individual', value_language=lg_id)
        sv.save()
        sv = system_values(value_group = 'event_type', value_name='team', value_string = 'Team', value_language=lg_id)
        sv.save()
    if(1==1):   #load gender
        lg_id = language.objects.get(language_code='en-us')
        sv = system_values(value_group = 'gender', value_name='men', value_string = 'Men', value_language=lg_id)
        sv.save()
        sv = system_values(value_group = 'gender', value_name='women', value_string = 'Women', value_language=lg_id)
        sv.save()
        sv = system_values(value_group = 'gender', value_name='mixed', value_string = 'Mixed', value_language=lg_id)
        sv.save()
        sv = system_values(value_group = 'gender', value_name='unknown', value_string = 'Unknown', value_language=lg_id)
        sv.save()
    if(1==1):   #load weapon
        lg_id = language.objects.get(language_code='en-us')
        sv = system_values(value_group = 'weapon', value_name='foil', value_string = 'Foil', value_language=lg_id)
        sv.save()
        sv = system_values(value_group = 'weapon', value_name='epee', value_string = 'Epee', value_language=lg_id)
        sv.save()
        sv = system_values(value_group = 'weapon', value_name='sabre', value_string = 'Sabre', value_language=lg_id)
        sv.save()
        sv = system_values(value_group = 'weapon', value_name='unknown', value_string = 'Unknown', value_language=lg_id)
        sv.save()
    if(1==1):  #load tournament status and event status
        tournament_status(status='Upcoming').save()
        tournament_status(status='Active').save()
        tournament_status(status='Inactive').save()
        tournament_status(status='Cancelled').save()
        tournament_status(status='Postponed').save()
        tournament_status(status='Completed').save()
        event_status(status='Upcoming').save()
        event_status(status='Active').save()
        event_status(status='Inactive').save()
        event_status(status='Cancelled').save()
        event_status(status='Postponed').save()
        event_status(status='Completed').save()

def create_system_users(f, DEBUG_WRITE):
        f.write("\n\ncreate_system_users: " + str(timezone.now()) + "\n")

        if os.environ.get("DURHAM_PASSWORDS_ADMIN") is not None:
                passwd = str(os.environ.get("DURHAM_PASSWORDS_ADMIN"))
        else:
                passwd = None

        user, created = User.objects.get_or_create(email='admin@gmail.com', 
                                        defaults={'first_name': 'Admin', 'last_name': 'Admin', 
                                                'is_staff': True, 'is_superuser': True})
        user.set_password(passwd)
        user.is_superuser = True
        user.save()

        user, created = User.objects.get_or_create(email='ukrdl@gmail.com', 
                                        defaults={'first_name': 'Data Loader', 'last_name': 'UKRatings', 
                                                'is_staff': True, 'is_superuser': False})
        user.set_password(passwd)
        user.is_superuser = True
        user.save()

        user, created = User.objects.get_or_create(email='Ftmanagerinfo@gmail.com', 
                                        defaults={'first_name': 'Info', 'last_name': 'Tourney', 
                                                'is_staff': True, 'is_superuser': True})
        user.set_password(passwd)
        user.is_superuser = True
        user.save()

        user, created = User.objects.get_or_create(email='Ftmanagerlogs@gmail.com', 
                                        defaults={'first_name': 'Logs', 'last_name': 'Tourney', 
                                                'is_staff': True, 'is_superuser': True})
        user.set_password(passwd)
        user.is_superuser = True
        user.save()

        user, created = User.objects.get_or_create(email='Ftmanageruser@gmail.com', 
                                        defaults={'first_name': 'Sys User', 'last_name': 'Tourney', 
                                                'is_staff': True, 'is_superuser': True})
        user.set_password(passwd)
        user.is_superuser = True
        user.save()


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

        record_log_data("x_reset_system.py", "base_reset_system", "Resetting system")

#        record_log_data(app_name, "y_load_dump_customuser.run()", "Starting")
#        y_load_dump_user.run()               
#        record_log_data(app_name, "y_load_dump_customuser.run()", "Completed")

        record_log_data(app_name, "base_clear_tables", "Starting")
        base_clear_tables()
        record_log_data(app_name, "base_clear_tables", "Completed")

        record_log_data(app_name, "clear_loading_tables", "Starting")
        clear_loading_tables()  
        record_log_data(app_name, "clear_loading_tables", "Completed")

        record_log_data(app_name, "base_reset_system_variables", "Starting")
        base_reset_system_variables()
        record_log_data(app_name, "base_reset_system_variables", "Completed")

        record_log_data(app_name, "create_system_users", "Starting")
        create_system_users(f, True) 
        record_log_data(app_name, "create_system_users", "Complete")

        record_log_data(app_name, "BF_Create_Assn", "Starting")
        asn = BF_Create_Assn(f, True)
        record_log_data(app_name, "BF_Create_Assn", "Complete")

        record_log_data(app_name, "Copying Backup Files", "Starting")
        zbackup_dir = os.path.join(settings.BASE_DIR, "zbackupfiles/")
        dump_dir = os.path.join(settings.BASE_DIR, "dumps/")
        copy_zbackup_files_if_exist(f, zbackup_dir, dump_dir, True)
        record_log_data(app_name, "Copying Backup Files", "Complete")

        record_log_data(app_name, "y_admin_key_tables_load.run()", "Starting")
        y_admin_key_tables_load.run()
        record_log_data(app_name, "y_admin_key_tables_load.run()", "Completed")

        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()
 
        #Email log file
#        send_attachment(fname)
#        os.remove(fname)


#python manage.py runscript y_reset_system
# nohup python manage.py runscript y_reset_system &


###To check row count of tables
#SELECT
#    schemaname || '.' || relname AS table_name,
#    n_live_tup AS row_count
#FROM
#    pg_stat_user_tables
#ORDER BY
#    n_live_tup DESC;