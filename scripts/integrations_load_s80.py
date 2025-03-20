#!/usr/bin/env python3

from scripts.x_helper_functions import *
from scripts.integrations_load_s80_upcoming import Get_Rankings_JWT

from integrations.models import *
from tourneys.models import *

import requests
import json
import io
import os
import inspect
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from decouple import config
from datetime import datetime 
from django.utils.dateparse import parse_datetime

from dotenv import load_dotenv
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")


#https://admin-bf-rankings.s80testing.co.uk/api/docs.html   --- JWT
#https://bf.s80testing.co.uk/api/doc --- access_token
#https://curlconverter.com/



###  ALL NEW HERE ###
def get_s80_fencing_competition_record(f, dict, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("         get_s80_fencing_competition_record: " + str(dict) + " " + str(timezone.now()) + "\n")
        try:
                competition = load_s80_fencing_competitions.objects.get(id_str = dict.get("id"))
        except:
                competition = None
        if(DEBUG_WRITE):
                f.write("         Completed: get_s80_fencing_competition_record: " + str(competition) + " " + str(timezone.now()) + "\n")
        return(competition)
def Get_S80_Fencing_Competitions(f, JWT_token_string, s_date, e_date, s80, DEBUG_WRITE):
        f.write("   Get_S80_Fencing_Competitions: " + str(s_date) + " " + str(e_date) + " at: "+ str(timezone.now()) + "\n")

        headers = {'accept': 'application/ld+json','Authorization': 'Bearer '+str(JWT_token_string)}
        query_params = {'endDate[strictly_after]': s_date.strftime("%m/%d/%Y"),'endDate[strictly_before]': e_date.strftime("%m/%d/%Y"),}
        if(s80):
                f.write("Sport80 DEBUG = True\n")
                endpoint = 'https://admin-bf-rankings.s80testing.co.uk/api/fencing_competitions'
        else:
                endpoint = 'https://admin-bf-rankings.sport80.com/api/fencing_competitions'

        if(DEBUG_WRITE):
                f.write("      s_date: " + str(s_date)+"\n")
                f.write("      e_date: " + str(e_date)+"\n")
                f.write("      endpoint: " + endpoint + "\n")
                f.write("      query_params: " + str(query_params) + "\n")
#                f.write("      headers: " + str(headers) + "\n")

        response = requests.get(endpoint, params=query_params, headers=headers)
        if(DEBUG_WRITE):
                f.write("      response status code: " + str(response.status_code)+"\n")

        if(response.status_code == 200):
                new_response = response.content.decode("utf-8")
                new_response = response.content.replace(b"'", b'"')
                dict = json.load(io.BytesIO(new_response))  
#                pretty = json.dumps(dict, indent=4)
#                f.write("\n\n"+ pretty + "\n\n")

                for x in dict["hydra:member"]:
#t                        print(x["endDate"])
                        c_endDate = parse_datetime(x["endDate"])
                        if c_endDate is not None:
                                if timezone.is_naive(c_endDate):
                                        c_endDate = timezone.make_aware(c_endDate, timezone.get_default_timezone())

                        if(DEBUG_WRITE):
                                f.write("      "+str(x) + "\n")
                        l80, created = load_s80_fencing_competitions.objects.update_or_create(
                                at_id = x["@id"],
                                at_type = x["@type"],
                                name = x["name"],
                        defaults={
                                'date_updated':timezone.now(),
                                'endDate':x["endDate"],
                                'calced_endDate':c_endDate,
                                'expiryDate':x["expiryDate"],
                                'competitionType':x["competitionType"],
                                'organisation':x["organisation"],
                                'eventReference':x["eventReference"],
                                'isInternational':x["isInternational"],
                                'id_str':x["id"],})
                        if(l80.date_added == None):
                                load_s80_fencing_competitions.objects.update_or_create(
                                        at_id = x["@id"],
                                        at_type = x["@type"],
                                        name = x["name"],
                                defaults={
                                        'date_added':timezone.now()})
                        if('series' in x):
                                y = x['series']
                                if(y is not None and y["@id"] is not None):
                                        l80s, created = load_s80_fencing_competitions_series.objects.update_or_create(
                                                fc = l80,
                                                at_id = y["@id"],
                                                at_type = y["@type"],
                                        defaults={
                                                'date_updated':timezone.now(),
                                                'id_str':y["id"],
                                                'tag':y["tag"],})
                                        if(l80s.date_added == None):
                                                load_s80_fencing_competitions_series.objects.update_or_create(
                                                        fc = l80,
                                                        at_id = y["@id"],
                                                        at_type = y["@type"],
                                                defaults={
                                                        'date_added':timezone.now()})
        else:
                f.write("ERROR--> Get_S80_Fencing_Competitions: ERROR - No 200 response\n\n\n")
        f.write("    Completed: Get_S80_Fencing_Competitions: " + str(s_date) + " " + str(e_date) + " at: "+ str(timezone.now()) + "\n\n\n")
def create_or_update_s80_fencing_events_category(f, dict, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("         create_or_update_s80_fencing_events_category: " + str(dict) + " " + str(timezone.now()) + "\n")
        category, created = load_s80_fencing_events_category.objects.update_or_create(
                s80_id = dict.get("id"),
                defaults={
#                'weapon':weapon,
#                'ageGroup':age_group,
                'gender':dict.get("gender"),
                'at_id':dict.get("@id"),
                'at_type':dict.get("@type"),
                'name':dict.get("name"),
                'type':dict.get("type")
                })
        if(DEBUG_WRITE):
                f.write("         Completed: create_or_update_s80_fencing_events_category: " + str(dict) + " " + str(timezone.now()) + "\n")
        return(category)
def create_or_update_s80_fencing_events(f, dict, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("         create_or_update_s80_fencing_events: " + str(dict) + " " + str(timezone.now()) + "\n")
        competition = get_s80_fencing_competition_record(f, dict.get("competition"), DEBUG_WRITE)
        category = create_or_update_s80_fencing_events_category(f, dict.get("category"), DEBUG_WRITE)

        category_dict = dict.get("category", {})
        age_group = category_dict.get("ageGroup", {})
        age_name = age_group.get("name") if age_group else None
        weapon_group = category_dict.get("weapon", {})
        weapon_name = weapon_group.get("name") if weapon_group else None

        event, created = load_s80_fencing_events.objects.update_or_create(
                s80_id = dict.get("id"),
                defaults={
                'competition':competition,
                'category':category,
                'weapon':weapon_name,
                'agegroup':age_name,
                'at_id':dict.get("@id"),
                'at_type':dict.get("@type"),
                'name':dict.get("name"),
                'endDate':dict.get("endDate"),
                'multiplier':dict.get("multiplier"),
                'nif':dict.get("nif"),
                'calculatedNif':dict.get("calculatedNif"),
                'numberOfFencers':dict.get("numberOfFencers"),
                'calculatedNumberOfFencers':dict.get("calculatedNumberOfFencers"),
                'ratio':dict.get("ratio"),
                'penalty':dict.get("penalty"),
                'status':dict.get("status"),
                'repechageLevel':dict.get("repechageLevel"),
#                'eligibleCategories':dict.get("eligibleCategories"),
                'youngerAgeGroupsEligible':dict.get("youngerAgeGroupsEligible"),
                'comment':dict.get("comment"),
                'realNif':dict.get("realNif"),
                'realNumberOfFencers':dict.get("realNumberOfFencers"),
                'international':dict.get("international")
                })
        if(DEBUG_WRITE):
                f.write("         Completed: create_or_update_s80_fencing_events: " + str(dict) + " " + str(timezone.now()) + "\n")
        return(event)
def Get_S80_Fencing_Events(f, JWT_token_string, s_date, e_date, s80, DEBUG_WRITE):
        f.write("   Get_S80_Fencing_Events: " + str(s_date) + " " + str(e_date) + " at: "+ str(timezone.now()) + "\n")

        headers = {'accept': 'application/ld+json','Authorization': 'Bearer '+str(JWT_token_string)}
        query_params = {'competition.endDate[after]': s_date.strftime("%m/%d/%Y"),'competition.endDate[before]': e_date.strftime("%m/%d/%Y"),}
        if(s80):
                f.write("s80... Sport80 DEBUG = True\n")
                endpoint = 'https://admin-bf-rankings.s80testing.co.uk/api/fencing_events'
        else:
                endpoint = 'https://admin-bf-rankings.sport80.com/api/fencing_events'

        if(DEBUG_WRITE):
                f.write("      s_date: " + str(s_date)+"\n")
                f.write("      e_date: " + str(e_date)+"\n")
                f.write("      endpoint: " + endpoint + "\n")
                f.write("      query_params: " + str(query_params) + "\n")
#                f.write("      headers: " + str(headers) + "\n")

        response = requests.get(endpoint, params=query_params, headers=headers)
        if(DEBUG_WRITE):
                f.write("      response status code: " + str(response.status_code)+"\n")

        if(response.status_code == 200):
                new_response = response.content.decode("utf-8")
                new_response = response.content.replace(b"'", b'"')
                dict = json.load(io.BytesIO(new_response))  
#                pretty = json.dumps(dict, indent=4)
#                f.write("\n\n"+ pretty + "\n\n")

                for x in dict["hydra:member"]:
                        if(DEBUG_WRITE):
                                f.write("      " + str(len(x)) + " " + str(x) + "\n")
                        create_or_update_s80_fencing_events(f, x, DEBUG_WRITE)
        else:
                f.write("ERROR--> Get_S80_Fencing_Events: ERROR - No 200 response\n\n\n")
        f.write("    Completed: Get_S80_Fencing_Events: " + str(s_date) + " " + str(e_date) + " at: "+ str(timezone.now()) + "\n\n\n")
def create_or_update_s80_fencing_fencing_results(f, eve, dict, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("         create_or_update_s80_fencing_fencing_results: " + str(dict) + " " + str(timezone.now()) + "\n")

        fencing_results, created = load_s80_fencing_fencing_results.objects.update_or_create(
                event = eve,
                at_id = dict.get("@id"),
                at_type = dict.get("@type"),
                point = dict.get("point"),
                calculatedPoint = dict.get("calculatedPoint"),
                realPoint = dict.get("realPoint"),
                displayCategory = dict.get("displayCategory"),
                s80_id = dict.get("id"),
                rank = dict.get("rank"),
                side_id = dict.get("side")["id"],
                name = dict.get("side")["name"],
                identifier = dict.get("side")["identifier"],
                country = dict.get("side")["country"]
                )
        if(DEBUG_WRITE):
                f.write("         Completed: create_or_update_s80_fencing_fencing_results: " + str(dict) + " " + str(timezone.now()) + "\n")
        return(fencing_results)
def s80_fencing_results_exist(f, eve, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("         s80_fencing_results_exist: " + str(eve) + " " + str(timezone.now()) + "\n")
        fr = load_s80_fencing_fencing_results.objects.filter(event = eve)
        if(len(fr) == 0):
                fencing_results = False
        else:
                fencing_results = True
        if(DEBUG_WRITE):
                f.write("         Completed: s80_fencing_results_exist: " + str(eve) + " " + str(fencing_results) + " " +str(timezone.now()) + "\n")
        return(fencing_results)

def Get_S80_Event_Results(f, JWT_token_string, s80, DEBUG_WRITE):
        f.write("   Get_S80_Event_Results: " + " at: "+ str(timezone.now()) + "\n")
        if os.environ.get("S80_COMPLETED_DATE_ADDED_BACK") is not None:
                dab = int(os.environ.get("S80_COMPLETED_DATE_ADDED_BACK"))
        else:
                dab = 3
        target_date = timezone.now() - relativedelta(days=dab)
        for qq in load_s80_fencing_events.objects.filter(competition__date_added__gte = target_date):
#                print("qq", qq)
                if (not s80_fencing_results_exist(f, qq, DEBUG_WRITE)):
#                        event_id = qq.s80_id
                        headers = {'accept': 'application/ld+json','Authorization': 'Bearer '+str(JWT_token_string)}
                        query_params = {'event': qq.s80_id,}
                        if(s80):
                                f.write("s80... Sport80 DEBUG = True\n")
                                endpoint = 'https://admin-bf-rankings.s80testing.co.uk/api/fencing_points'
                        else:
                                endpoint = 'https://admin-bf-rankings.sport80.com/api/fencing_points'
                        if(DEBUG_WRITE):
                                f.write("      event_id: " + str(qq.s80_id)+"\n")
                                f.write("      endpoint: " + endpoint + "\n")
                                f.write("      query_params: " + str(query_params) + "\n")
                #                f.write("      headers: " + str(headers) + "\n")
                        response = requests.get(endpoint, params=query_params, headers=headers)
                        if(DEBUG_WRITE):
                                f.write("      response status code: " + str(response.status_code)+"\n")
                        if(response.status_code == 200):
                                new_response = response.content.decode("utf-8")
                                new_response = response.content.replace(b"'", b'"')
                                dict = json.load(io.BytesIO(new_response))  
                #                pretty = json.dumps(dict, indent=4)
                #                f.write("\n\n"+ pretty + "\n\n")

                                for x in dict["hydra:member"]:
                                        if(DEBUG_WRITE):
                                                f.write("      out..." + str(x) + "\n")
                                        create_or_update_s80_fencing_fencing_results(f, qq, x, DEBUG_WRITE)
        else:
                f.write("ERROR--> Get_S80_Event_Results: ERROR - No 200 response\n\n\n")
        f.write("    Completed: Get_S80_Event_Results: at: "+ str(timezone.now()) + "\n\n\n")
def Load_All_S80_Fencing_Competitions(f, access_token, s_date, e_date, S80_DEBUG, DEBUG_WRITE):
        f.write("\nInside Drive_S80_Fencing_Competitions: " + str(timezone.now()) + "\n")
        rng = 30
        f.write("   Start Date: " + str(s_date) + "   End Date: " + str(e_date) + "\n")

        r_start = s_date
        if(r_start + relativedelta(days=rng) > e_date):
                r_end = e_date
        else:
                r_end = r_start + relativedelta(days=rng)
        while(r_start <= e_date):
                if(DEBUG_WRITE):
                        f.write("      Range Start Date: " + str(r_start) + "   Range End Date: " + str(r_end) + " " + str(timezone.now()) + "\n")
                Get_S80_Fencing_Competitions(f, access_token, r_start, r_end, S80_DEBUG, False)
                Get_S80_Fencing_Events(f, access_token, r_start, r_end, S80_DEBUG, DEBUG_WRITE)

                r_start = r_end + relativedelta(days=1)
                if(r_start + relativedelta(days=rng) > e_date):
                        r_end = e_date
                else:
                        r_end = r_start + relativedelta(days=rng)
        Get_S80_Event_Results(f, access_token, S80_DEBUG, DEBUG_WRITE)
        f.write("Completed Load_All_S80_Fencing_Competitions: " + str(timezone.now()) + "\n")
def Clear_Load_Tables():
        load_s80_fencing_competitions.objects.all().delete()
        load_s80_fencing_competitions_series.objects.all().delete()
        load_s80_fencing_events.objects.all().delete()
        load_s80_fencing_events_category.objects.all().delete()
        load_s80_fencing_fencing_results.objects.all().delete()


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

        record_log_data(app_name, funct_name, "Starting")

        DEBUG_WRITE = False
        u_name = os.environ.get("S80_U_NAME")
        u_pass = os.environ.get("S80_U_PASS")
        access_token = os.environ.get("S80_ACCESS_TOKEN")
        s80 = eval(os.environ.get("SPORT80_DEBUG"))
        asn = get_association(f, "British Fencing", DEBUG_WRITE)
        if os.environ.get("S80_COMPLETED_DAYS_BACK") is not None:
                s80_days_back = int(os.environ.get("S80_COMPLETED_DAYS_BACK"))
        else:
                s80_days_back = 5

        if 'reset' in args:
                f.write("   RESETTING... \n")
                tournaments.objects.filter(tourney_inbound = 'S80').delete()
                Clear_Load_Tables()  ###clears all the load tables
        if(len(args) == 2):
                ls_date = Make_String_Timezone_Aware(args[0])
                le_date = Make_String_Timezone_Aware(args[1])
        elif(len(args) > 2):
                ls_date = Make_String_Timezone_Aware(args[1])
                le_date = Make_String_Timezone_Aware(args[2])
        if(1==1):
                f.write("DEBUG_WRITE: " + str(DEBUG_WRITE) + "\n")
                f.write("u_name: " + u_name + "\n")
                f.write("u_pass: " + u_pass + "\n")
                f.write("access_token: " + access_token + "\n")
                f.write("SPORT80:  " + str(s80) + "\n")
                f.write("asn:  " + str(asn.assn_name) + "\n")
                f.write("New Start Date: " + str(ls_date) + "\n")
                f.write("New End Date: " + str(le_date) + "\n")

        record_log_data(app_name, "Get_Rankings_JWT", "Starting")
        JWT_token_string = Get_Rankings_JWT(f, u_name, u_pass, s80, DEBUG_WRITE)
        record_log_data(app_name, "Get_Rankings_JWT", "Completed")

        if(len(JWT_token_string)>0):
                record_log_data(app_name, "Load_All_S80_Fencing_Competitions", "Starting")
                Load_All_S80_Fencing_Competitions(f, JWT_token_string, ls_date, le_date, s80, DEBUG_WRITE)
                record_log_data(app_name, "Load_All_S80_Fencing_Competitions", "Completed")
        else:
                record_error_data(app_name, funct_name, "Error", "Error:  No JWT_token_string")
                f.write("Error:  No JWT_token_string: " + str(timezone.now()) + "\n")

        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()
        record_log_data(app_name, funct_name, "Completed")
 

# python manage.py runscript integrations_load_s80

# python manage.py runscript integrations_load_s80 --script-args reset
# python manage.py runscript integrations_load_s80 --script-args reset 01/01/2023 31/12/2023
# python manage.py runscript integrations_load_s80 --script-args 01/01/2022 12/31/2022



