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

def BF_calc_difficulty(f, asn, eve, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      BF_calc_difficulty: " + str(eve) + " " + str(timezone.now()) + "\n")
        start_a = 0
        start_b = 0
        start_c = 0
        start_d = 0
        start_e = 0
        event_difficulty = 0.0

        if('upcoming' in eve.ev_tourney.tourney_inbound.lower()):
                fencers = event_registered_athletes.objects.filter(era_event = eve).order_by('era_given_name')
        else:
                fencers = event_final_results.objects.filter(efr_event = eve).order_by('efr_final_position')
        for q in fencers:
                if('upcoming' in eve.ev_tourney.tourney_inbound.lower()):
                        amr = get_assn_member_record_by_assn_member_number(f, asn, q.era_assn_member_number, False)
                        given_member_identifier = q.era_given_member_identifier
                        given_member_name = q.era_given_name
                        final_position = None
                else:
                        amr = get_assn_member_record_by_assn_member_number(f, asn, q.efr_assn_member_number, False)
                        given_member_identifier = q.efr_given_member_identifier
                        given_member_name = q.efr_given_name
                        final_position = q.efr_final_position
                if(amr is None):
                        current_rating = "U"
                else:
                        day_before = eve.ev_start_date - relativedelta(hours=1)
                        current_rating, q_award_date, q_award_date_end, q_event = BF_get_rating_at_specific_date_from_assn_member_extra_field(f, amr, eve.ev_assn_discipline.discipline_name, day_before, False)
                if(1==0):
                        if(amr is None):
                                f.write("            Association Member Record Not Found:  " 
                                        + "---Given Member Identifier: " + str(given_member_identifier)
                                        + "---Given Name: " + str(given_member_name)
                                        + " Final Position: " + str(final_position) + "\n")
                        else:
                                f.write("            Current Rating: " + str(current_rating)
                                        + "---Given Member Identifier: " + str(given_member_identifier)
                                        + " Mem ID: " + str(amr.assn_member_number)
                                        + "---Given Name: " + str(given_member_name)
                                        + " Final Position: " + str(final_position) + "\n")

                if(current_rating.upper() == "A"):
                        start_a = start_a + 1
                if(current_rating.upper() == "B"):
                        start_b = start_b + 1
                if(current_rating.upper() == "C"):
                        start_c = start_c + 1
                if(current_rating.upper() == "D"):
                        start_d = start_d + 1
                if(current_rating.upper() == "E"):
                        start_e = start_e + 1

        #we know how many, calculate event difficulty
        if os.environ.get("BF_DIFF_POINTS_A") is not None:
                a_points = int(os.environ.get("BF_DIFF_POINTS_A"))
        else:
                a_points = 0
        if os.environ.get("BF_DIFF_POINTS_B") is not None:
                b_points = int(os.environ.get("BF_DIFF_POINTS_B"))
        else:
                b_points = 0
        if os.environ.get("BF_DIFF_POINTS_C") is not None:
                c_points = int(os.environ.get("BF_DIFF_POINTS_C"))
        else:
                c_points = 0
        if os.environ.get("BF_DIFF_POINTS_D") is not None:
                d_points = int(os.environ.get("BF_DIFF_POINTS_D"))
        else:
                d_points = 0
        if os.environ.get("BF_DIFF_POINTS_E") is not None:
                e_points = int(os.environ.get("BF_DIFF_POINTS_E"))
        else:
                e_points = 0
        if os.environ.get("BF_MAX_DIFFICULTY") is not None:
                max_diff = int(os.environ.get("BF_MAX_DIFFICULTY"))
        else:
                max_diff = 100

        tot_fencers = fencers.count()
        ev_points = ((start_a * a_points) + (start_b * b_points) + (start_c * c_points) + (start_d * d_points) + (start_e * e_points))
        if(float(tot_fencers) > 0):
                c_pts = float(ev_points) / (float(tot_fencers) * float(a_points))
        else:
                c_pts = 0.0

        pre_event_difficulty = float(c_pts) * 100.0
        event_difficulty = (pre_event_difficulty / max_diff) * 100.0
        if(event_difficulty > 100.0):
                event_difficulty = 100.0

        ex_field_value = ("Event Difficulty Calculation:" 
                        + " ((((" + str(start_a) + "*" + str(a_points) + ")"
                        + "+(" + str(start_b) + "*" + str(b_points) + ")"
                        + "+(" + str(start_c) + "*" + str(c_points) + ")"
                        + "+(" + str(start_d) + "*" + str(d_points) + ")"
                        + "+(" + str(start_e) + "*" + str(e_points) + ")"
                        + ") / (" + str(tot_fencers) + "*" + str(a_points) + ")) * 100)")
        update_or_create_event_extra_field(f, eve, "Difficulty", event_difficulty, False)
        update_or_create_event_extra_field(f, eve, "Difficulty Calculation", ex_field_value, False)

        if(DEBUG_WRITE):
                f.write("         Calcing FINAL Rating\n")
                f.write("            Tournament Name: " + str(eve.ev_tourney.tourney_name) + " Event Name: " + str(eve.ev_name) + "\n")
                f.write("            Total Fencers: " + str(tot_fencers) + "\n")
                f.write("            Difficulty: " + str(event_difficulty) + " pre_max: " + str(pre_event_difficulty) + " " + str(ev_points) + " " + str(tot_fencers) + " " + str(c_pts) + "\n")
        if(DEBUG_WRITE):
                f.write("      BF_calc_difficulty: " + str(eve.ev_name) 
                        + "---Difficulty: " + str(event_difficulty) + " " + str(timezone.now()) + "\n")


def Difficulties_Work_Tournaments(f, asn, force_override, DEBUG_WRITE):
        record_log_data("x_apply_difficulty.py", "Difficulties_Work_Tournaments", "started: " + str(timezone.now()))
        f.write("\n Difficulties_Work_Tournaments: " + str(asn.assn_name) \
                + " force_override: " + str(force_override) + str(timezone.now()) + "\n")

#        for ee in events.objects.filter(ev_tourney__tourney_assn = asn, ev_tourney__tourney_name__icontains = 'Championships').order_by('ev_tourney__tourney_start_date', 'ev_tourney__tourney_name'):
        for ee in events.objects.filter(ev_tourney__tourney_assn = asn).order_by('ev_tourney__tourney_start_date', 'ev_tourney__tourney_name'):
                if(1==0):
                        print(ee.ev_tourney.tourney_name, ee.ev_tourney.tourney_start_date, ee.ev_tourney.tourney_inbound, ee.ev_name)
                if(force_override):
                        eef = None
                else:
                        eef = get_event_extra_field(f, ee, "Difficulty", '', '', '', False)
                if(DEBUG_WRITE):
                        f.write("   " 
                                + " eef: " + str(eef)
                                + " force_override: " + str(force_override)
                                + " tourney_name: " + str(ee.ev_tourney.tourney_name)
                                + " tourney_start_date: " + str(ee.ev_tourney.tourney_start_date)
                                + " tourney_inbound: " + str(ee.ev_tourney.tourney_inbound)
                                + " event_name: " + str(ee.ev_name)
                                + "\n")

                if(eef is None or force_override or ('upcoming' in ee.ev_tourney.tourney_inbound.lower() and ee.ev_tourney.tourney_start_date >= timezone.now())):
                        if(1==0):
                                print('Calling')
                        BF_calc_difficulty(f, asn, ee, DEBUG_WRITE)

        f.write(" COMPLETE: Difficulties_Work_Tournaments: " + str(asn.assn_name) + " " + str(timezone.now()) + "\n")
        record_log_data("x_apply_difficulty.py", "Difficulties_Work_Tournaments", "completed: " + str(timezone.now()))



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
        force_override = False

        asn = get_association(f, "British Fencing", DEBUG_WRITE)
        if(1==1):
                f.write("DEBUG_WRITE: " + str(DEBUG_WRITE) + "\n")
                f.write("asn:  " + str(asn.assn_name) + "\n")

                if('reset' in args):
                        force_override = True

                if(1==1):
                        f.write("args: " + str(args) + " " + str(len(args)) + "\n")
                        f.write("force_override: " + str(force_override) + "\n")

        DEBUG_WRITE = True

        record_log_data(app_name, "Difficulties_Work_Tournaments", "Starting")
        Difficulties_Work_Tournaments(f, asn, force_override, DEBUG_WRITE)
        record_log_data(app_name, "Difficulties_Work_Tournaments", "Completed")

        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()
        record_log_data(app_name, funct_name, "Completed")


# python manage.py runscript x_apply_difficulty
# python manage.py runscript x_apply_difficulty --script-args reset

