#!/usr/bin/env python3

from scripts.x_helper_functions import *
from scripts.x_helper_assn_specific import *

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

from dotenv import load_dotenv
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")


def Get_Rankings_JWT(f, u_name, u_pass, S80_DEBUG, DEBUG_WRITE):
        f.write("Get JWT: " + str(timezone.now()) + "\n")
        token_out = ""
        headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = '_username='+u_name+'&_password='+u_pass

        if(S80_DEBUG):
                f.write("S80_DEBUG = True\n")
                response = requests.post('https://admin-bf-rankings.s80testing.co.uk/api/login_check', headers=headers, data=data)
        else:
                response = requests.post('https://admin-bf-rankings.sport80.com/api/login_check', headers=headers, data=data)

        if(DEBUG_WRITE):
                f.write("   response status code: " + str(response.status_code)+"\n")
#        f.write("response.content: " + str(response.content)+"\n")
        if(response.status_code == 200):
                new_response = response.content.decode("utf-8")
                dict = json.loads(new_response)

                token_string=dict["token"].encode("ascii","ignore")
                token_out = dict["token"]
        else:
                f.write(" Get JWT: Error - No 200 response\n\n\n")
        if(DEBUG_WRITE):
                f.write(" Get JWT: " + str(token_out)+"\n")
        return(token_out)

def Load_S80_Sanctioned_Events(f, dict, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("            Recording S80 Sanctioned Events: " + str(dict.get("name"))+ " "+ str(dict.get("start_date")) + "   " +str(timezone.now()) + "\n")

        real_lat_long = False
        orig_source = "Sport80"
        orig_source_url = "https://bf.sport80.com/public/events"

        if(dict['addr_latitude'] == None):
                lat, long, real_lat_long = GetLatLong(f, dict.get("venueaddrpostcode"), DEBUG_WRITE=False)
                if(real_lat_long == False):
                       lat, long, real_lat_long = GetLatLong(f, dict.get("addr_postcode"), DEBUG_WRITE=False)
        else:
                lat = dict['addr_latitude']
                long = dict['addr_longitude']
                if(DEBUG_WRITE):
                        f.write("               from record:  lat: " + str(lat) + " long: " + str(long) +"\n")
        
        if(DEBUG_WRITE):
                f.write("               lat: " + str(lat) + " long: " + str(long) + " real: " + str(real_lat_long)+"\n")

        tournament_id, created = load_s80_upcoming_tournaments.objects.update_or_create(
                        source = orig_source, source_url = orig_source_url,
                        tournament_id = dict.get("id"),
                        defaults={
                        'date_updated':timezone.now(),
                        'name':dict.get("name"),
                        'status':dict.get("status"),
                        'sanction_name':dict.get("sanction_name"),
                        'licence_id':dict.get("licence_id"),
                        'start_date': Make_String_Timezone_Aware(dict.get("start_date")),
                        'end_date': Make_String_Timezone_Aware(dict.get("end_date")),
                        'max_age':dict.get("max_age"),
                        'min_age':dict.get("min_age"),
                        'entry_closing': Make_String_Timezone_Aware(dict.get("entry_closing")),
                        'url':dict.get("url"),
                        'entry_link':dict.get("entry_link"),
                        'event_entry_list_url':dict.get("event_entry_list_url"),
                        'level':dict.get("level"),
                        'venuewebsite':dict.get("venuewebsite"),
                        'venuename':dict.get("venuename"),
                        'venueaddr1':dict.get("venueaddr1"),
                        'venueaddr2':dict.get("venueaddr2"),
                        'venueaddr3':dict.get("venueaddr3"),
                        'venueaddrcity':dict.get("venueaddrcity"),
                        'venueaddrregion':dict.get("venueaddrregion"),
                        'venueaddrpostcode':dict.get("venueaddrpostcode"),
                        'venuelongitude':long,
                        'venuelatitude':lat,
                        'rankingevent':str_2_bool(dict.get("rankingevent")),
                        'mensindepee':str_2_bool(dict.get("mensindepee")),
                        'mensindfoil':str_2_bool(dict.get("mensindfoil")),
                        'mensindsabre':str_2_bool(dict.get("mensindsabre")),
                        'womensindepee':str_2_bool(dict.get("womensindepee")),
                        'womensindfoil':str_2_bool(dict.get("womensindfoil")),
                        'womensindsabre':str_2_bool(dict.get("womensindsabre")),
                        'mensteamepee':str_2_bool(dict.get("mensteamepee")),
                        'mensteamfoil':str_2_bool(dict.get("mensteamfoil")),
                        'mensteamsabre':str_2_bool(dict.get("mensteamsabre")),
                        'womensteamepee':str_2_bool(dict.get("womensteamepee")),
                        'womensteamfoil':str_2_bool(dict.get("womensteamfoil")),
                        'womensteamsabre':str_2_bool(dict.get("womensteamsabre")),
                        'mensindepeeagecategories':dict.get("mensindepeeagecategories"),
                        'mensindfoilagecategories':dict.get("mensindfoilagecategories"),
                        'mensindsabreagecategories':dict.get("mensindsabreagecategories"),
                        'womensindepeeagecategories':dict.get("womensindepeeagecategories"),
                        'womensindfoilagecategories':dict.get("womensindfoilagecategories"),
                        'womensindsabreagecategories':dict.get("womensindsabreagecategories"),
                        'mensteamepeeagecategories':dict.get("mensteamepeeagecategories"),
                        'mensteamfoilagecategories':dict.get("mensteamfoilagecategories"),
                        'mensteamsabreagecategories':dict.get("mensteamsabreagecategories"),
                        'womensteamepeeagecategories':dict.get("womensteamepeeagecategories"),
                        'womensteamfoilagecategories':dict.get("womensteamfoilagecategories"),
                        'womensteamsabreagecategories':dict.get("womensteamsabreagecategories")
                        })
        if(DEBUG_WRITE):
                f.write("               Checking date_added\n")
        if(tournament_id.date_added == None):
                if(DEBUG_WRITE):
                        f.write("               Updating date added\n")
                load_s80_upcoming_tournaments.objects.update_or_create(
                        source = orig_source, source_url = orig_source_url,
                        tournament_id = dict.get("id"),
                        defaults={
                        'date_added':timezone.now()})                
        if(DEBUG_WRITE):
                f.write("             Completed: Recording S80 Sanctioned Events: " + str(dict.get("name"))+ " "+ str(dict.get("start_date")) + "   " +str(timezone.now()) + "\n")
def Get_S80_Sanctioned_Events(f, access_token, s_date, e_date, S80_DEBUG, DEBUG_WRITE):
        f.write("         Get S80 Sanctioned Events: " + str(s_date) + " " + str(e_date) + " at: "+ str(timezone.now()) + "\n")

        headers = {'accept': 'application/ld+json',}
        query_params = {
                'access_token': access_token,
                'from_date': s_date,
                'to_date': e_date,}

        if(S80_DEBUG):
                f.write("S80_DEBUG = True\n")
                endpoint = 'https://bf.s80testing.co.uk/api/sanctioned_events' 
        else:
                endpoint = 'https://bf.sport80.com/api/sanctioned_events' 

        if(DEBUG_WRITE):
                f.write("            endpoint: " + str(endpoint)+"\n")
#                f.write("            query_params: " + str(query_params)+"\n")
#                f.write("            headers: " + str(headers)+"\n")
                f.write("            s_date: " + str(s_date)+"\n")
                f.write("            e_date: " + str(e_date)+"\n")

        response = requests.get(endpoint, params=query_params)
        if(DEBUG_WRITE):
                f.write("            response status code: " + str(response.status_code)+"\n")
#        f.write("response.content: " + str(response.content)+"\n")
        if(response.status_code == 200):
                new_response = response.content.decode("utf-8")
#                new_response = new_response.replace("\/", "/")
#                f.write("new_response: " + str(new_response)+"\n")
                idx = new_response.find('{')
                if(idx == -1):
                        f.write("          Get_S80_Sanctioned_Events: ERROR - NO EVENTS IN SPORT80\n\n\n")
                else:
                        st_idx = 0
                        dict_string = new_response[idx:]
#                        f.write("dict_string: " + str(dict_string)+"\n")
                        while(st_idx == 0):
                                full_record = False
                                while (full_record == False):
                                        a = 0
                                        start_curly = 0
                                        end_curly = 0
                                        while(a < len(dict_string)):
                                                if dict_string[a] == "{":
                                                        start_curly = start_curly + 1
                                                if dict_string[a] == "}":
                                                        end_curly = end_curly + 1
                                                        if(end_curly == start_curly):
                                                                end_idx = a
                                                                a = len(dict_string)
                                                                full_record = True                        
                                                a = a + 1
                                dict_record = dict_string[st_idx:end_idx+1]
                                dict_string = dict_string[end_idx+2:]
#                                f.write("\n\n\ndict_record: " + str(dict_record)+"\n\n\n")
                                try:
                                        dict = json.loads(dict_record)
                                except:
                                        f.write("          Get_S80_Sanctioned_Events:  ERROR - Couldn't process event\n")
                                        f.write("              dict_record: " + dict_record + "\n\n\n\n")
                                else:                                        
                                        dict = json.loads(dict_record)
                                        if(len(dict)==132):
                                                Load_S80_Sanctioned_Events(f, dict, DEBUG_WRITE)
                                                b = 1
                                        else:
                                                f.write("          Get_S80_Sanctioned_Events: ERROR:  number of keys: " + str(len(dict)) + "\n")
                                                f.write("              dict_record: " + dict_record + "\n\n\n\n")
                                st_idx = str(dict_string).find('{')
        else:
                f.write("          Get_S80_Sanctioned_Events: ERROR - No 200 response\n\n\n")
        f.write("         Completed: Get S80 Sanctioned Events: " + str(s_date) + " " + str(e_date) + " at: "+ str(timezone.now()) + "\n")
def Drive_S80_Sanctioned_Events(f, access_token, s_date, e_date, S80_DEBUG, DEBUG_WRITE):
        f.write("\nInside Drive S80_Sanctioned_Events: " + str(timezone.now()) + "\n")
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
                Get_S80_Sanctioned_Events(f, access_token, r_start, r_end, S80_DEBUG, DEBUG_WRITE)

                r_start = r_end + relativedelta(days=1)
                if(r_start + relativedelta(days=rng) > e_date):
                        r_end = e_date
                else:
                        r_end = r_start + relativedelta(days=rng)
        f.write("Completed Drive S80_Sanctioned_Events: " + str(timezone.now()) + "\n")
def Get_S80_Load_Entries_Fencers(f, JWT_token_string, tourney, entry, weapon_name, msg, msg_value, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("         Get Get_S80_Entries_Fencers: " + " " + str(tourney.name)
                        + " weapon_name=" + str(weapon_name) 
                        + " entries=" + str(entry.entry_id) 
                        + " msg=" + str(msg) 
                        + " msg_value=" + msg_value + " " + str(timezone.now()) + "\n")
        load_s80_upcoming_tournaments_entries_fencers.objects.filter(entry_id = entry.id).delete()

        headers = {
        'accept': 'application/ld+json',
        'Authorization': 'Bearer '+str(JWT_token_string)
        }
        data = '{"columns":[],"filters":{"'+str(msg)+'":['+str(msg_value)+']}}'#
        endpoint = 'https://bf.sport80.com/api/public/events/locator/entries/'+str(tourney.tournament_id)+'/'+str(entry.entry_id)+'?data=1'

        if(DEBUG_WRITE):
                f.write("            headers: " + str(headers) + "\n")
                f.write("            end point: " + str(endpoint) + "\n")
                f.write("            data value: " + str(data) + "\n")
        response = requests.post(endpoint, headers=headers, data=data)
        if(DEBUG_WRITE):
                f.write("            response status code: " + str(response.status_code)+"\n")
#                        f.write("            response.content: " + str(response.content)+"\n")

        if(response.status_code == 200):
                dict = json.load(io.BytesIO(response.content))  
#                        if(DEBUG_WRITE):
#                                f.write("            json.dump: " + str(json.dumps(dict, indent=4)))
                if(dict["data"]):
                        for y in dict["data"]:
                                if("club" in y):
                                        n_cut = str(y["name"]).find(" ")
                                        c_name = str(y["name"])[n_cut+1:].upper() + " " + str(y["name"])[:n_cut].title()
                                        if(DEBUG_WRITE):
                                                f.write("            y_name: " + str(y["name"])
                                                        + " c_name: " + str(c_name)
                                                        + " club: " + str(y["club"]) + "\n")
                                        fencer, created = load_s80_upcoming_tournaments_entries_fencers.objects.update_or_create(
                                                entry_id = entry,
                                                s80_id = y["id"],
                                                s80_name = y["name"].title(),
                                                s80_club = y["club"].title(),
                                                defaults={
                                                        'corrected_name':c_name,
                                                        'corrected_gender' : "",
                                                        'corrected_club' : "",
                                                        'ind_license': "",
                                                        'ind_nif': 0,
                                                        'ind_weapon': weapon_name,
                                                        'ind_rating': ""
                                                })
                                else:
                                        if(DEBUG_WRITE):
                                                f.write("            Skipping... No club\n")
                else:
                        if(DEBUG_WRITE):
                                f.write("            Skipping... No entries\n")
        else:
                f.write("            Get_S80_Load_Entries_Fencers ERROR: response status code: " + str(response.status_code)+"\n")
        if(DEBUG_WRITE):
                f.write("         Complete Get_S80_Load_Entries_Fencers: " + str(tourney.name)+ " "+ str(tourney.start_date) + " " + str(tourney.event_entry_list_url) + " " + str(timezone.now()) + "\n")
def Get_S80_Load_Upcoming_Entries(f, JWT_token_string, asn, tourney, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      Get_S80_Load_Upcoming_Entries: " + str(tourney.name)+ " "+ str(tourney.start_date) + " " + str(tourney.event_entry_list_url) + " " + str(timezone.now()) + "\n")

        entries_url = tourney.event_entry_list_url
        q_loc = entries_url.rfind("?")
        s_loc = entries_url.rfind("/")
        entries_id = entries_url[s_loc+1:q_loc]
        if(DEBUG_WRITE):
                f.write("         Entries_id: " + str(entries_id) + "\n")

        headers = {
        'accept': 'application/ld+json',
        'Authorization': 'Bearer '+str(JWT_token_string)
        }
        endpoint = 'https://bf.sport80.com/api/public/events/locator/entries/'+str(tourney.tournament_id)+'/'+str(entries_id)
        if(DEBUG_WRITE):
                f.write("         endpoint: " + str(endpoint)+"\n")
#                f.write("         headers: " + str(headers)+"\n")

        response = requests.get(endpoint, headers=headers)
        if(DEBUG_WRITE):
                f.write("         response status code: " + str(response.status_code)+"\n")
#                f.write("         response.content: " + str(response.content)+"\n")

        if(response.status_code == 200):
                dict = json.load(io.BytesIO(response.content))  
#                        f.write("         json.dump: " + str(json.dumps(dict, indent=4)) + "\n\n")
                if(dict["has_filters"]):
                        for y in dict["filters"]:
                                label_value = str(y["label"])
                                gen = get_assn_gender_from_text(f, asn, str(y["label"]), "", "", DEBUG_WRITE)
                                gender_name = gen.gender_name
                                for z in y["items"]:
                                        wea_cut = str(z["text"]).find("(")
                                        entry_value = str(z["text"])
                                        entry_name = str(z["text"])
                                        discipline = get_assn_discipline_from_text(f, asn, entry_name, label_value, tourney.name, DEBUG_WRITE)
                                        entries = str(z["text"])[wea_cut:]
#                                                f.write(str(z["text"]) + "::" + entry_name + "::" + weapon_name + "::" + entries +" \n")    #weapon and entries --> "Foil (28/112 Entries)"
#                                                f.write(str(z["value"])+"\n")   # need for data entries search value --> "175526"
                                        if(DEBUG_WRITE):
                                                f.write("               tourney: " + str(tourney) + "\n")
                                                f.write("               entries_id: " + str(entries_id) + "\n")
                                                f.write("               y[name]: " + str(y["name"]) + "\n")
                                                f.write("               z[value]: " + str(z["value"]) + "\n")
                                                f.write("               gender_name: " + str(gender_name) + "\n")
                                                f.write("               label_value: " + str(label_value) + "\n")
                                                f.write("               entry_value: " + str(entry_value) + "\n")
                                                f.write("               weapon_name: " + str(discipline.discipline_name) + "\n")
                                                f.write("               entries: " + str(entries) + "\n")
                                                
                                        load_s80_upcoming_tournaments_entries.objects.filter(tournament_id = tourney.tournament_id, 
                                                        entry_id = entries_id, msg = str(y["name"]), msg_value = str(z["value"])).delete()
                                        if(DEBUG_WRITE):
                                                f.write("   writing record" + "\n")
                                        try:
                                                entry, created = load_s80_upcoming_tournaments_entries.objects.update_or_create(
                                                                tournament_id = tourney,
                                                                entry_id = entries_id,
                                                                msg  = str(y["name"]),
                                                                msg_value = str(z["value"]),
                                                                defaults={
                                                                        'gender_name':gender_name,
                                                                        'full_label':label_value,
                                                                        'full_entry':entry_value,
                                                                        'weapon_name':discipline.discipline_name,
                                                                        'entries':entries
                                                                })
                                        except:
                                                f.write("Error:  " + str(tourney.name) + " " + str(y["name"]) + " " + str(z["value"]) + "\n")
                                        else:
                                                if(DEBUG_WRITE):
                                                        f.write("   going to load entries fencers" + "\n")
                                                Get_S80_Load_Entries_Fencers(f, JWT_token_string, tourney, entry, discipline.discipline_name, str(y["name"]), str(z["value"]), False)
                else:
                        if(DEBUG_WRITE):
                                f.write("No filters so skipping\n")
        if(DEBUG_WRITE):
                f.write("       Completed Get_S80_Load_Upcoming_Entries: " + str(tourney.name)+ " "+ str(tourney.start_date) + " " + str(tourney.event_entry_list_url) + " " + str(timezone.now()) + "\n")
def Load_All_S80_Upcoming_Events(f, JWT_token_string, asn, st_date, DEBUG_WRITE):
        f.write("\nLoad_All_S80_Upcoming_Events: " + str(timezone.now()) + "\n")
        f.write("   Start Date: " + str(st_date) + "\n")
#        f.write("   Start Date data type: " + str(type(st_date)) + "\n")
#        if timezone.is_naive(st_date):
#                st_date = timezone.make_aware(st_date, timezone.get_current_timezone())
#        f.write("   Start Date: " + str(st_date) + "\n")
#        f.write("   Start Date data type: " + str(type(st_date)) + "\n")
        
        up_tourneys = load_s80_upcoming_tournaments.objects.filter(start_date__gte=st_date)
        f.write("   uptourney length: " + str(up_tourneys.count()) + "\n")

        for xx in up_tourneys:
#                f.write("      inside uptourney length: " + str(up_tourneys.count()) + "\n")
#                f.write("      inside xx: " + str(xx) + "\n")
                if(DEBUG_WRITE):
                        f.write("   Looking at: " + str(xx.name) + " start date: " + str(xx.start_date) + " at " + str(timezone.now()) + "\n")
                if(xx.event_entry_list_url is not None):
                        f.write("   Loading: " + str(xx.name) + " start date: " + str(xx.start_date) + " at " + str(timezone.now()) + "\n")
                        Get_S80_Load_Upcoming_Entries(f, JWT_token_string, asn, xx, DEBUG_WRITE)
        f.write(" Completed Load_All_S80_Upcoming_Events: " + str(timezone.now()) + "\n")


def Clear_Upcoming_Tables():
        load_s80_upcoming_tournaments.objects.all().delete()
        load_s80_upcoming_tournaments_entries.objects.all().delete()
        load_s80_upcoming_tournaments_entries_fencers.objects.all().delete()

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

        DEBUG_WRITE = True
        u_name = os.environ.get("S80_U_NAME")
        u_pass = os.environ.get("S80_U_PASS")
        access_token = os.environ.get("S80_ACCESS_TOKEN")
        s80 = eval(os.environ.get("SPORT80_DEBUG"))
        asn = get_association(f, "British Fencing", DEBUG_WRITE)
        s80_upcoming_days_back = int(os.environ.get("S80_UPCOMING_DAYS_BACK"))
        s80_upcoming_days_out = int(os.environ.get("S80_UPCOMING_DAYS_OUT"))

        if(1==1):
                f.write("DEBUG_WRITE: " + str(DEBUG_WRITE) + "\n")
                f.write("u_name: " + u_name + "\n")
                f.write("u_pass: " + u_pass + "\n")
                f.write("access_token: " + access_token + "\n")
                f.write("SPORT80:  " + str(s80) + "\n")
                f.write("asn:  " + str(asn.assn_name) + "\n")
                f.write("s80_upcoming_days_back:  " + str(s80_upcoming_days_back) + "\n")
                f.write("s80_upcoming_days_out:  " + str(s80_upcoming_days_out) + "\n")

        if 'reset' in args:
                f.write("   RESETTING... \n")
                tournaments.objects.filter(tourney_inbound = 'upcomingS80').delete()
                Clear_Upcoming_Tables()  ###clears all the load tables

        if(len(args) == 2):
                ls_date = Make_String_Timezone_Aware(args[0])
                le_date = Make_String_Timezone_Aware(args[1])
        elif(len(args) > 2):
                ls_date = Make_String_Timezone_Aware(args[1])
                le_date = Make_String_Timezone_Aware(args[2])
        if(1==1):
                f.write("USES THIS New Start Date: " + str(ls_date) + "\n")
                f.write("USES THIS New End Date: " + str(le_date) + "\n")

        record_log_data(app_name, "Get_Rankings_JWT", "Starting")
        JWT_token_string = Get_Rankings_JWT(f, u_name, u_pass, s80, DEBUG_WRITE)
        record_log_data(app_name, "Get_Rankings_JWT", "Completed")

        record_log_data(app_name, "Drive_S80_Sanctioned_Events", "Starting")
        Drive_S80_Sanctioned_Events(f, access_token, ls_date, le_date, s80, False)
        record_log_data(app_name, "Drive_S80_Sanctioned_Events", "Completed")

        if(len(JWT_token_string)>0):
                record_log_data(app_name, "Load_All_S80_Upcoming_Events", "Starting")
                Load_All_S80_Upcoming_Events(f, JWT_token_string, asn, ls_date, DEBUG_WRITE)
                record_log_data(app_name, "Load_All_S80_Upcoming_Events", "Completed")

        else:
                record_error_data(app_name, funct_name, "Error", "Error:  No JWT_token_string")
                f.write("Error:  No JWT_token_string: " + str(timezone.now()) + "\n")

        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()
        record_log_data(app_name, funct_name, "Completed")
 


# python manage.py runscript integrations_load_s80_upcoming

# python manage.py runscript integrations_load_s80_upcoming --script-args reprocess
# python manage.py runscript integrations_load_s80_upcoming --script-args reset
# python manage.py runscript integrations_load_s80_upcoming --script-args reset 01/01/2023 31/12/2023
# python manage.py runscript integrations_load_s80_upcoming --script-args 01/01/2022 12/31/2022


