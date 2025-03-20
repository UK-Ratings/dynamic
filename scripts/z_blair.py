#!/usr/bin/env python3

from assn_mgr.models import *
from users.models import User

from integrations.models import *
from tourneys.models import *

from scripts.x_helper_functions import *
from scripts.x_helper_assn_specific import *

from scripts.x_apply_ratings import *

from django.db.models.functions import Length
from django.db.models import ForeignKey

from django.utils import timezone
from django.db.models import F
import os
import inspect
import re
from django.db import connection

from dotenv import load_dotenv
from django.conf import settings

import matplotlib.pyplot as plt
import time

from math import radians, sin, cos, sqrt, atan2

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")

def trial_distance(f):
        a_tourneys = tournaments.objects.filter(tourney_name__icontains = 'Championships')
        a_tourneys_dict = [model_to_dict(tt) for tt in a_tourneys]
        local_tourneys_dict = delete_distant_tourneys(a_tourneys_dict, ['500 km'])

        all_tourneys = list(local_tourneys_dict)
        all_tourneys.sort(key=lambda x: (x['tourney_start_date'], x['tourney_name']))



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
#        Test_Currrent_Rating(f)
#        trial_distance(f)

#                    Sam Blair U 162047 in prod
#                    Sam Blair B 55652 in dev

#                        322043	20785	"55652"	"R"	"S"	"S R"
#                        301480	222	"120579"	"Samuel"	"BLAIR"	"BLAIR Samuel"

        asn = get_association(f, "British Fencing", DEBUG_WRITE)
        assn_recs = association_members.objects.filter(assn = asn).values_list('assn_member_full_name', flat=True)
        Duplicate_Final_Results_Ratings_For_Performance(f, asn, True, DEBUG_WRITE)
        if(1==1):
                f.write("DEBUG_WRITE: " + str(DEBUG_WRITE) + "\n")
                f.write("asn:  " + str(asn.assn_name) + "\n")

        if(1==0):
                ls_date = Make_String_Timezone_Aware("06/01/2022")
                le_date = Make_String_Timezone_Aware("06/07/2022")
                record_log_data(app_name, "UK_Apply_NIFs", "Starting")
                UK_Apply_NIFs(f, ls_date, le_date, True)
                record_log_data(app_name, "UK_Apply_NIFs", "Completed")



        if(1==0):
                g_abbr = 'M'
                weapon = 'Foil'
                members = association_members.objects.filter(assn = asn, 
                    assn_member_gender = g_abbr, 
                    assn_member_valid=True,assn_member_suspended=False)

                uc_ef = association_member_extra_fields.objects.filter(
                        assn_member_field_name="Current Rating",
                        assn_member_field5_value__iexact=weapon.lower(),
                        assn_member__in = members).order_by('assn_member__assn_member_full_name')
                for qq in uc_ef:
                        if(qq.assn_member_field3_value in ('A')):
#                        if(qq.assn_member.assn_member_identifier in ('136150', '136151')):
                                print(qq.assn_member.assn_member_identifier, 
                                      qq.assn_member.assn_member_full_name, qq.assn_member_field3_value)


#        get_assn_member_record(f, asn, assn_recs, None, "BLAIR Sam", "", "", True)
#        for x in association_members.objects.annotate(name_length=Length('assn_member_full_name')).filter(assn=asn, name_length__lte=4):
#                f.write("assn_member_full_name: " + str(x.assn_member_full_name) + "\n")


#        for x in s80_load_membership_records.objects.annotate(name_length=Length('last_name')).filter(name_length__lte=1):
#                f.write("last_name: " + str(x.last_name) + " " + str(x.first_name)+ "\n")

#        s_date = timezone.now() - relativedelta(years=2)
#        e_date = timezone.now() + relativedelta(years=+1)
#        BF_clear_assn_member_history_recalc_current_rating(f, s_date, e_date, True)



#        weapon = 'Foil'
#        gender_abbr = 'M'
#        cnt = 0
#        the_list = [0, 0, 0, 0, 0, 0]#

#        if(gender_abbr == 'M'):
#            g_abbr = 'M'
#            title_text = "Men Total: " + str(cnt)
#        else:
#            g_abbr = 'F'
#            title_text = "Women Total: " + str(cnt)

#        asn = get_association(None, "British Fencing", False)
#        members = association_members.objects.filter(assn = asn, assn_member_gender = g_abbr, assn_member_valid=True,assn_member_suspended=False)

#        s_date = timezone.now()
#        for x in members:
#            if(x.assn_member_identifier in ('136150', '136151')):
#                amr = get_assn_member_record_by_assn_member_number(f, asn, x.assn_member_number, True)
#                print(weapon, x.assn_member_identifier, x.assn_member_number, x, amr, timezone.now())
##            if(1==1):
#                cur_rating, event = BF_get_rating_at_specific_date(f, amr, 
#                        'Foil', s_date, True)

##                cur_rating, event = BF_get_rating_at_specific_date(f, x, weapon, timezone.now(), True)
#                print(cur_rating, event)
#                pos = ord(cur_rating) - ord('A')
#                if(pos>4):
#                    pos = 5
#                the_list[pos] = the_list[pos] + 1
#                cnt = cnt + 1

#        BF_daily_validate_current_rating(f, DEBUG_WRITE)

        if(1==0):  #to check history
                amr = get_assn_member_record_by_assn_assn_member_identifier(f, asn, '136151', True)
                print(amr, amr.assn_member_full_name)
                last_events, participating_disciplines = BF_athlete_get_last_events(amr, 99)
                for x in last_events:
                        print(x[1], x[12], x[2], x[3], x[5], x[6]) 
                        f.write(str(x[1]) + " " + str(x[12]) + " " + str(x[2]) + " " + str(x[3]) + " " 
                                + str(x[5]) + " prev: " + str(x[6]) + " earned: " + str(x[7]) 
                                + " on: " + str(x[8])+ "\n")
                
                ex_field_name = "Rating History"

                uc_ef = association_member_extra_fields.objects.filter(
                        assn_member=amr,
                        assn_member_field_name=ex_field_name,
                        assn_member_field5_value__iexact='foil').order_by('-id')
                print("uc_ef: ", uc_ef) 
                f.write("\n\n\n")
                for x in uc_ef:
                        ev = events.objects.get(ev_number = x.assn_member_field4_value)
#                        print(ev.ev_tourney.tourney_name, ev.ev_number, ev.ev_name)
                        print(ev.ev_tourney.tourney_name, ev.ev_number, ev.ev_name, x.assn_member,
#                                        x.assn_member_field_sequence,
#                                        x.assn_member_field_active,
#                                        x.assn_member_field_group,
#                                        x.assn_member_field_name,
#                                        x.assn_member_field1_type,
#                                        x.assn_member_field1_value,
#                                        x.assn_member_field2_type,
#                                        x.assn_member_field2_value,
#                                        x.assn_member_field3_type,
                                        x.assn_member_field3_value,
#                                        x.assn_member_field4_type,
#                                        x.assn_member_field4_value,
#                                        x.assn_member_field5_type ,
#                                        x.assn_member_field5_value  ,
#                                        x.assn_member_field_date_updated
                                        )
                        f.write(str(ev.ev_tourney.tourney_name) + " " + str(ev.ev_number) + " " 
                                + str(ev.ev_name) + " " + str(x.assn_member) + " " 
                                + str(x.assn_member_field3_value) + "\n")


#                am_current_rating = get_assn_member_extra_field(f, amr, "Current Rating", "Foil", "", "", "", "", DEBUG_WRITE)
#                print("Assn Member Current Rating: ", am_current_rating, am_current_rating.assn_member_field3_value)
 #               am_rating_history = get_assn_member_extra_field(f, amr, "Rating History", "Foil", "", "", "", "", DEBUG_WRITE)
 #               print("Assn Member Rating History: ", am_rating_history)
        
#                q_rating, q_award_date, q_award_date_end, q_event = BF_get_rating_at_specific_date_from_assn_member_extra_field(f, amr, 'Foil', timezone.now(), DEBUG_WRITE)
#                print(q_rating, q_event)

#                rat, award_date, award_date_end, eve = BF_get_rating_at_specific_date_from_assn_member_extra_field(f, amr, 'Foil', timezone.now(), DEBUG_WRITE)
#                print(rat, eve)

        if(1==0):
                last_events, participating_disciplines = BF_athlete_get_last_events(amr, 99)
                for x in last_events:
#                        print(x, x[12])
                        eve = events.objects.get(ev_number = x[12])
                        new_rating = x[7]
                        rating_date = eve.ev_start_date
                        print(x, x[12], eve, eve.ev_name, new_rating, rating_date)
#                        BF_update_or_create_rating_history(f, amr, eve, 'Foil', new_rating, rating_date, DEBUG_WRITE)

#                rat, award_date, award_date_end, eve = BF_get_rating_at_specific_date_from_assn_member_extra_field(f, amr, 'Foil', timezone.now(), DEBUG_WRITE)
#                print(rat, eve)


        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()
        record_log_data(app_name, funct_name, "Completed")



# python manage.py runscript z_blair

