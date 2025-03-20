#!/usr/bin/env python3

from assn_mgr.models import *
from users.models import User

from integrations.models import *
from tourneys.models import *

from scripts.x_helper_functions import *
from scripts.x_helper_assn_specific import *
from scripts import x_apply_difficulty 
from scripts import x_apply_te_delete_hide
from scripts import y_add_missing_nifs
from scripts import y_add_missing_disciplines_genders


from django.utils import timezone
from django.db.models import F
import os
import inspect
import re

from dotenv import load_dotenv
from django.conf import settings

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")


def Ratings_Work_Tournaments(f, asn, s_date, e_date, DEBUG_WRITE):
        record_log_data("x_apply_ratings.py", "Ratings_Work_Tournaments", "started: " + str(timezone.now()))
        f.write("\n Ratings_Work_Tournaments: " + str(asn.assn_name) \
                + " s_date: " + str(s_date) + " e_date: " + str(e_date) + str(timezone.now()) + "\n")

        for tt in tournaments.objects.filter(tourney_assn = asn, tourney_start_date__gte = s_date, tourney_start_date__lte = e_date).order_by('tourney_start_date'):
#        for tt in tournaments.objects.filter(tourney_inbound = 'Durham', tourney_assn = asn, tourney_start_date__gte = s_date, tourney_start_date__lte = e_date).order_by('tourney_start_date'):
                if(DEBUG_WRITE):
                        print(tt.tourney_name, tt.tourney_start_date, tt.tourney_inbound)
                tfr = is_tournament_rated(f, tt, False)
                f.write("      Tournament: " + tt.tourney_name 
                        + "---tournament rated: " + str(tfr)
                        + "---tournament start date: " + str(tt.tourney_start_date) + "\n")
#                tfr = False
                if(tfr is False):
                        for x in events.objects.filter(ev_tourney = tt).order_by('ev_start_date'):
                                if(DEBUG_WRITE):
                                        print("Tournament: " + x.ev_tourney.tourney_name + "---" + x.ev_name)
# Technically correct but too confusing.
#                                er = is_event_complete(f, x, False)
                                er = True
                                if(er):
                                        if(DEBUG_WRITE):
                                                f.write("         Event Complete: Tournament: " + x.ev_tourney.tourney_name 
                                                        + "---" + x.ev_name + " " + str(timezone.now()) + "\n")
                                        BF_calc_ratings_and_write_event_extra_fields(f, x, DEBUG_WRITE)        
#technically correct to delete but too confusing to viewer
#                                else:
#                                        if(DEBUG_WRITE):
#                                                f.write("         No final results.  Deleting event: Tournament: " + x.ev_tourney.tourney_name 
#                                                        + "---" + x.ev_name + " " + str(timezone.now()) + "\n")
#                                        x.delete()
                        BF_tournament_extra_field_value_build_ratings(f, tt, DEBUG_WRITE)

        f.write(" COMPLETE: Ratings_Work_Tournaments: " + str(asn.assn_name) + " " + str(timezone.now()) + "\n")
        record_log_data("x_apply_ratings.py", "Ratings_Work_Tournaments", "completed: " + str(timezone.now()))


def Duplicate_Final_Results_Ratings_For_Performance(f, asn, force_override, DEBUG_WRITE):
        record_log_data("x_apply_ratings.py", "Duplicate_Final_Results_Ratings_For_Performance", "started: " + str(timezone.now()))
        f.write("\n Duplicate_Final_Results_Ratings_For_Performance: " + str(asn.assn_name) \
                + " force_override: " + str(force_override) + " " + str(timezone.now()) + "\n")

#        for tt in tournaments.objects.filter(tourney_assn = asn, tourney_name = 'Welsh National Championships 2025',tourney_start_date__gte = (timezone.now()-relativedelta(day=7)), tourney_inbound__icontains = "upcoming").order_by('tourney_start_date'):
#        for tt in tournaments.objects.filter(tourney_assn = asn, tourney_start_date__gte = (timezone.now()-relativedelta(day=21)), tourney_inbound__icontains = "upcoming").order_by('tourney_start_date'):
#        for tt in tournaments.objects.filter(tourney_assn = asn, tourney_inbound__icontains = "upcoming").order_by('tourney_start_date'):
        for tt in tournaments.objects.filter(tourney_assn = asn).order_by('tourney_start_date'):
                if(DEBUG_WRITE):
                        print(tt.tourney_name, tt.tourney_start_date, tt.tourney_inbound)
                for ee in events.objects.filter(ev_tourney = tt).order_by('ev_start_date'):
                        disp_name = ee.ev_assn_discipline.discipline_name
                        day_before = ee.ev_start_date - relativedelta(hours=1)
                        for efr in event_final_results.objects.filter(efr_event = ee).order_by('efr_final_position'):
                                if(force_override or efr.efr_final_rating is None):
                                        amr = get_assn_member_record_by_assn_member_number(f, asn, efr.efr_assn_member_number, DEBUG_WRITE)
                                        points = get_efr_extra_field_value(None, efr, 'efr_final_points', False)
#                                        pr = get_efr_extra_field_value(None, efr, 'efr_previous_rating', False)   #
                                        if(amr is not None):
                                                pr, pr_award_year, award_year_end, event = BF_get_rating_at_specific_date_from_assn_member_extra_field(
                                                        f, amr, ee.ev_assn_discipline.discipline_name, ee.ev_start_date-relativedelta(hour=1), DEBUG_WRITE)
                                        else:
                                                pr = "U"
                                                pr_award_year = str(ee.ev_start_date.year)[2:4]
                                        previous_rating_value = pr + str(pr_award_year)
                                        er = get_efr_extra_field_value(None, efr, 'efr_rating', False)  
                                        award_year = get_efr_extra_field_value(None, efr, 'efr_award_date', False)  
                                        if(er in ("U", "NR")):
                                                earned_rating_value = er
                                        else:
                                                earned_rating_value = er + str(award_year)
                                        efr.efr_nif = points
                                        efr.efr_previous_rating = previous_rating_value
                                        efr.efr_final_rating = earned_rating_value
                                        efr.save()
                        for era in event_registered_athletes.objects.filter(era_event=ee).order_by('era_given_name'):
                                era.era_current_rating = None
                                era.save()
                        for era in event_registered_athletes.objects.filter(era_event=ee).order_by('era_given_name'):
                                if(era.era_current_rating is None):
                                        amr = get_assn_member_record_by_assn_member_number(None, tt.tourney_assn, era.era_assn_member_number, False)
                                        pr, award_year, award_year_end, event = BF_get_rating_at_specific_date_from_assn_member_extra_field(None, amr, disp_name, day_before, False)
                                        if(pr in ("U", "NR")):
                                                current_rating_value = pr
                                        else:
                                                current_rating_value = pr + str(award_year)
#                                                print("current_rating_value: ", current_rating_value)
                                        era.era_current_rating = current_rating_value
                                        era.save()

        f.write(" COMPLETE: Duplicate_Final_Results_Ratings_For_Performance: " + str(asn.assn_name) + " " + str(timezone.now()) + "\n")
        record_log_data("x_apply_ratings.py", "Duplicate_Final_Results_Ratings_For_Performance", "completed: " + str(timezone.now()))


def yyyRemove_Empty_Events(f, asn, DEBUG_WRITE):
        record_log_data("x_apply_ratings.py", "Remove_Empty_Events", "started: " + str(timezone.now()))
        e_date = timezone.now() - relativedelta(days=2)
        ti = ('FencingTimeLive', 'S80', 'LPJS', 'Engarde', 'Durham')

        f.write("\n Remove_Empty_Events: " + str(asn.assn_name) \
                + " e_date: " + str(e_date) + str(timezone.now()) + "\n")

        for tt in tournaments.objects.filter(tourney_assn = asn, 
                        tourney_inbound__in = ('FencingTimeLive', 'S80', 'LPJS', 'Engarde', 'Durham'),
                        tourney_start_date__lte = e_date).order_by('tourney_start_date'):
#                if(DEBUG_WRITE):
#                        print(tt.tourney_name, tt.tourney_inbound, tt.tourney_start_date, tt.tourney_inbound)
                f.write("      Tournament: " + tt.tourney_name 
                        + "---tournament start date: " + str(tt.tourney_start_date) + "\n")
                for x in events.objects.filter(ev_tourney = tt).order_by('ev_start_date'):
#                        if(DEBUG_WRITE):
#                                print("Tournament: " + x.ev_tourney.tourney_name + "---" + x.ev_name)
                        er = is_event_complete(f, x, False)
                        if(er==False):
                                if(DEBUG_WRITE):
                                        f.write("         No final position records: Tournament: " + x.ev_tourney.tourney_name 
                                                + "---" + x.ev_name + " " + str(timezone.now()) + "\n")
                                x.delete()

        f.write(" COMPLETE: Remove_Empty_Events: " + str(asn.assn_name) + " " + str(timezone.now()) + "\n")
        record_log_data("x_apply_ratings.py", "Remove_Empty_Events", "completed: " + str(timezone.now()))


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

        DEBUG_WRITE = False
        specific_tourney_error = False
        force_override = False
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
                specific_tournament = None
                reset_string = ""
                asn = get_association(f, "British Fencing", DEBUG_WRITE)
                if(1==1):
                        f.write("DEBUG_WRITE: " + str(DEBUG_WRITE) + "\n")
                        f.write("asn:  " + str(asn.assn_name) + "\n")
                        f.write("process_days_back:  " + str(process_days_back) + "\n")
                        f.write("process_days_out:  " + str(process_days_out) + "\n")

                if('reset' in args):
                        force_override = True
                        reset_string = "reset"
                        if (len(args) == 3):  #reset and dates
                                ls_date = Make_String_Timezone_Aware(args[1])
                                le_date = Make_String_Timezone_Aware(args[2])
                        else:  
                                ls_date = Make_String_Timezone_Aware("01/01/2022")
                                le_date = timezone.now() + relativedelta(days=process_days_out)
                        print("BF_clear_tourney_event_and_final_result_ratings_extra_fields")
                        BF_clear_tourney_event_and_final_result_ratings_extra_fields(f, ls_date, le_date, DEBUG_WRITE)
                        print("BF_clear_assn_member_history_recalc_current_rating")
                        BF_clear_assn_member_history_recalc_current_rating(f, ls_date, le_date, DEBUG_WRITE)
                        print("done")
                else:
                        if(len(args) == 2):  #dates only
                                ls_date = Make_String_Timezone_Aware(args[0])
                                le_date = Make_String_Timezone_Aware(args[1])
                        else:  # run with defaults
                                ls_date = timezone.now() - relativedelta(days=int(process_days_back)) 
                                le_date = timezone.now() + relativedelta(days=process_days_out)

                if(1==1):
                        f.write("args: " + str(args) + " " + str(len(args)) + "\n")
                        f.write("New Start Date: " + str(ls_date) + "\n")
                        f.write("New End Date: " + str(le_date) + "\n")
                        f.write("force_override: " + str(force_override) + "\n")
#                        print("New Start Date: ", str(ls_date))
#                        print("New End Date: ", str(le_date))

        DEBUG_WRITE = False
        if(process_days_back is not None and (not specific_tourney_error)):

                record_log_data(app_name, "x_apply_te_delete_hide", "Starting")
                x_apply_te_delete_hide.run()
                record_log_data(app_name, "x_apply_te_delete_hide", "Completed")

                record_log_data(app_name, "UK_Apply_NIFs", "Starting")
                UK_Apply_NIFs(f, ls_date, le_date, DEBUG_WRITE)
                record_log_data(app_name, "UK_Apply_NIFs", "Completed")

                record_log_data(app_name, "y_add_missing_nifs", "Starting")
                y_add_missing_nifs.run()
                record_log_data(app_name, "y_add_missing_nifs", "Completed")

                record_log_data(app_name, "y_add_missing_disciplines_genders", "Starting")
                y_add_missing_disciplines_genders.run()
                record_log_data(app_name, "y_add_missing_disciplines_genders", "Completed")

                record_log_data(app_name, "UK_Apply_Fencer_Count_To_Event", "Starting")
                UK_Apply_Fencer_Count_To_Event(f, ls_date, le_date, DEBUG_WRITE)
                record_log_data(app_name, "UK_Apply_Fencer_Count_To_Event", "Completed")

                record_log_data(app_name, "Ratings_Work_Tournaments", "Starting")
                Ratings_Work_Tournaments(f, asn, ls_date, le_date, DEBUG_WRITE)
                record_log_data(app_name, "Ratings_Work_Tournaments", "Completed")

#correct but confusing to viewer since won't match original system
#                record_log_data(app_name, "Remove_Empty_Events", "Starting")
#                Remove_Empty_Events(f, asn, True)
#                record_log_data(app_name, "Remove_Empty_Events", "Completed")

                record_log_data(app_name, "BF_daily_validate_current_rating", "Starting")
                BF_daily_validate_current_rating(f, DEBUG_WRITE)
                record_log_data(app_name, "BF_daily_validate_current_rating", "Completed")

                record_log_data(app_name, "Duplicate_Final_Results_Ratings_For_Performance", "Starting")
                Duplicate_Final_Results_Ratings_For_Performance(f, asn, force_override, DEBUG_WRITE)
                record_log_data(app_name, "Duplicate_Final_Results_Ratings_For_Performance", "Completed")

                record_log_data(app_name, "x_apply_difficulty", "Starting")
                x_apply_difficulty.run(reset_string)
                record_log_data(app_name, "x_apply_difficulty", "Completed")


        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()
        record_log_data(app_name, funct_name, "Completed")


#Process runs as follows:
#       No args - Goes back 21 days and recalculates all tournaments and events.
#       Reset - Goes back to 2022 and clears all ratings and final ratings then recalculates all tournaments and events.
#       Specific Tournament - Using tourney_number goes back to day before the specific tournament and recalculates all tournaments and events.
#       DEBUG Purposes only - Specific Dates - Goes back to the specific dates and recalculates all tournaments and events.
#       DEBUG - specific tournament will only run that one tournament.  Will remove after testing.

# python manage.py runscript x_apply_ratings
# python manage.py runscript x_apply_ratings --script-args reset

#  
# python manage.py runscript x_apply_ratings --script-args reset 01/01/2022 02/28/2022

# python manage.py runscript x_apply_ratings --script-args reset 01/01/2022 02/28/2029
# nohup python manage.py runscript x_apply_ratings --script-args reset 01/01/2022 02/28/2029 &

