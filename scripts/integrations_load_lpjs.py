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
from bs4 import BeautifulSoup
import xmltodict

from dotenv import load_dotenv
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")


def Get_LPJS_Load_Competition_Results_Event_Fencers(f, event_url, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      Get_LPJS_Load_Competition_Results_Event_Fencers.  Event_URL: " + event_url + " " + str(datetime.now()) + "\n")

        endpoint = event_url
        response = requests.get(endpoint)
        if(DEBUG_WRITE):
                f.write("      LPJS Status Code: " + str(response.status_code) + "\n")
#        f.write("      LPJS Content: " + str(response.content) + "\n\n\n\n")

        f_event_str = ""
        if(response.status_code == 200):
#                f_event_str = str(response.content)
#                f_event_str = f_event_str.replace("\'", "'")
                f_event_str = str(response.content.decode('unicode-escape'))
#                f.write("Here we go: " + f_event_str)
                while (f_event_str.find('<td') != -1):
                        open_bracket = f_event_str.find('<td')
                        f_event_str = f_event_str[open_bracket+3:]
                        open_bracket = f_event_str.find('>')
                        f_event_str = f_event_str[open_bracket+1:]
#                        f.write("f_event_str: " + f_event_str + "\n\n\n")
                        close_bracket = f_event_str.find('</td')
#                        f.write("close_bracket: "+ str(close_bracket)+ "\n")
                        position_str = f_event_str[:close_bracket]
#                        f.write("position_str: "+ position_str + "\n")
                        f_event_str = f_event_str[close_bracket:]
#                        f.write("f_event_str: " + f_event_str + "\n\n\n")

                        open_bracket = f_event_str.find('<td')
                        f_event_str = f_event_str[open_bracket+3:]
                        open_bracket = f_event_str.find('>')
                        f_event_str = f_event_str[open_bracket+1:]
#                        f.write("f_event_str: " + f_event_str + "\n\n\n")
                        close_bracket = f_event_str.find('</i>')
#                        f.write("close_bracket: "+ str(close_bracket)+ "\n")
                        icon_str = f_event_str[:close_bracket]
#                        f.write("lpjs_pos_str: "+ lpjs_pos_str + "\n")
                        f_event_str = f_event_str[close_bracket:]
#                        f.write("f_event_str: " + f_event_str + "\n\n\n")

                        open_bracket = f_event_str.find('<td')
                        f_event_str = f_event_str[open_bracket+3:]
                        open_bracket = f_event_str.find('>')
                        f_event_str = f_event_str[open_bracket+1:]
#                        f.write("f_event_str: " + f_event_str + "\n\n\n")
                        close_bracket = f_event_str.find('</td')
#                        f.write("close_bracket: "+ str(close_bracket)+ "\n")
                        name_str_all = f_event_str[:close_bracket]
#                        f.write("name_str: "+ name_str + "\n")
                        f_event_str = f_event_str[close_bracket:]
#                        f.write("f_event_str: " + f_event_str + "\n\n\n")
                        o_bracket = name_str_all.find('>')
                        c_bracket = name_str_all.find('</a>')
                        name_str = name_str_all[o_bracket+1:c_bracket]

                        open_bracket = f_event_str.find('<td')
                        f_event_str = f_event_str[open_bracket+3:]
                        open_bracket = f_event_str.find('>')
                        f_event_str = f_event_str[open_bracket+1:]
#                        f.write("f_event_str: " + f_event_str + "\n\n\n")
                        close_bracket = f_event_str.find('</td')
#                        f.write("close_bracket: "+ str(close_bracket)+ "\n")
                        club_str_all = f_event_str[:close_bracket]
#                        f.write("club_str: "+ club_str + "\n")
                        f_event_str = f_event_str[close_bracket:]
#                        f.write("f_event_str: " + f_event_str + "\n\n\n")
                        o_bracket = club_str_all.find('>')
                        c_bracket = club_str_all.find('</a>')
                        club_str = club_str_all[o_bracket+1:c_bracket]

                        if(position_str.isnumeric()):
#                                f.write("         position_str: "+ position_str
#                                + " icon_str: " + icon_str
#                                + " name_str: " + name_str
#                                + " club_str: "+ club_str + "\n")
                                load_lpjs_competitions_results_events_fencers.objects.update_or_create(
                                        event_results_url = event_url,
                                        full_name = name_str,
                                        position = position_str,
                                        defaults={
                                        'source':"LPJS",
                                        'club_name':club_str,
                                        'date_added':timezone.now()
                                        })
                        else:
                                if(DEBUG_WRITE):
                                        f.write("         SKIPPING position_str: "+ position_str+"\n")

def Get_LPJS_Load_Competition_Results_Events(f, s_date, e_date, DEBUG_WRITE):
        f.write("\n\nGet_LPJS_Load_Competition_Results_Events: start_date: " +str(s_date) + " to: " + str(e_date) + " " + str(datetime.now()) + "\n")

        for x in load_lpjs_competitions_results.objects.all():
                if(DEBUG_WRITE):
                        f.write("Comp Name: " + str(x.competition_name) + " comp_url: " + x.competition_url + "\n")

                endpoint = x.competition_url
                response = requests.get(endpoint)
                if(DEBUG_WRITE):
                        f.write("LPJS Status Code: " + str(response.status_code) + "\n")
#                f.write("LPJS Content: " + str(response.content) + "\n\n\n\n\n")
                if(response.status_code == 200):
#                        f_event_str = str(response.content)
                        f_event_str = str(response.content.decode('unicode-escape'))
#                        f.write("Here we go: " + f_event_str)
                        

                        while (f_event_str.find('//leonpauljuniorseries.co.uk/results/view/') != -1):
                                open_bracket = f_event_str.find('//leonpauljuniorseries.co.uk/results/view/')
                                f_event_str = f_event_str[open_bracket:]
        #                        f.write("f_event_str: " + f_event_str + "\n\n\n")
                                close_bracket = f_event_str.find('">')
        #                        f.write("close_bracket: "+ str(close_bracket)+ "\n")
                                event_results_url_str = "https:" + f_event_str[:close_bracket]
        #                        f.write("position_str: "+ position_str + "\n")
                                f_event_str = f_event_str[close_bracket:]
        #                        f.write("f_event_str: " + f_event_str + "\n\n\n")

                                open_bracket = f_event_str.find('U')
                                f_event_str = f_event_str[open_bracket:]
        #                        f.write("f_event_str: " + f_event_str + "\n\n\n")
                                close_bracket = f_event_str.find('</')
        #                        f.write("close_bracket: "+ str(close_bracket)+ "\n")
                                event_results_name_str = f_event_str[:close_bracket]
        #                        f.write("position_str: "+ position_str + "\n")
                                f_event_str = f_event_str[close_bracket:]
        #                        f.write("f_event_str: " + f_event_str + "\n\n\n")

#                                f.write("   LPJS_Load_Competitions_Events_Result  event_results_name_str: "+ event_results_name_str
#                                        + "   event_results_url_str: "+ event_results_url_str+ "\n")
                                load_lpjs_competitions_results_events.objects.update_or_create(
                                        event_results_url = event_results_url_str,
                                        event_name = event_results_name_str,
                                        defaults={
                                        'source':"LPJS",
                                        'source_url':x.competition_url,
                                        'date_added':timezone.now(),
                                        })
                                Get_LPJS_Load_Competition_Results_Event_Fencers(f, event_results_url_str, DEBUG_WRITE)

def Get_LPJS_Load_Competitions_Results(f, s_date, e_date, DEBUG_WRITE):
        f.write("Get_LPJS_Load_Competitions_Results: " + str(datetime.now()) + "\n")

        x = s_date.year

        while x <= e_date.year:
#                endpoint = 'https://leonpauljuniorseries.co.uk/results'
                endpoint = 'https://leonpauljuniorseries.co.uk/results?syear='+str(x)+'&submit=Search'
#                f.write("Year: " + str(x) + "\n")
#                f.write("endpoint: " + endpoint + "\n")
                response = requests.get(endpoint)
                if(DEBUG_WRITE):
                        f.write("endpoint: " + endpoint + "\n")
                        f.write("LPJS Status Code: " + str(response.status_code) + "\n")
        #        f.write("LPJS Content: " + str(response.content) + "\n\n\n\n")
        
                f_event_str = ""
                if(response.status_code == 200):
        #                af_event_str = str(response.content)
                        af_event_str = str(response.content.decode('unicode-escape'))
        #                f.write("Here we go: " + af_event_str)

                        
                        while (af_event_str.find('<h3>') != -1):
                                open_bracket = af_event_str.find('<h3>')
                                f_event_str = af_event_str[open_bracket+4:]
                                close_bracket = f_event_str.find('<h3>')
                                if(close_bracket == -1):  
                                        f_event_str = af_event_str[open_bracket:]
                                        af_event_str = ""
                                else:
                                        f_event_str = af_event_str[open_bracket:open_bracket+close_bracket-1]
                                        af_event_str = af_event_str[open_bracket+close_bracket:]

                                open_bracket = f_event_str.find('<h3>')
                                close_bracket = f_event_str.find('</h3>')
                                month_year_str = f_event_str[open_bracket+4:close_bracket]
                                f_event_str = f_event_str[close_bracket:]
#                                f.write("month_year_str: " + month_year_str + "\n")

                                while (f_event_str.find('<td>') != -1):
                                        open_bracket = f_event_str.find('<td>')
                                        f_event_str = f_event_str[open_bracket+4:]
                #                        f.write("f_event_str: " + f_event_str + "\n\n\n")
                                        close_bracket = f_event_str.find('</td>')
                #                        f.write("close_bracket: "+ str(close_bracket)+ "\n")
                                        day_str_d = f_event_str[:close_bracket]
                #                        f.write("position_str: "+ position_str + "\n")
                                        f_event_str = f_event_str[close_bracket:]
                #                        f.write("f_event_str: " + f_event_str + "\n\n\n")
                                        day_only = day_str_d[:len(day_str_d)-2]
                                        day_str = day_only + " " + month_year_str
                                        st_date = datetime.strptime(day_str, "%d %B %Y")
                                        tz = pytz.timezone("UTC")
                                        st_date = tz.localize(st_date)


                                        open_bracket = f_event_str.find('<td>')
                                        f_event_str = f_event_str[open_bracket+4:]
                #                        f.write("f_event_str: " + f_event_str + "\n\n\n")
                                        close_bracket = f_event_str.find('</td>')
                #                        f.write("close_bracket: "+ str(close_bracket)+ "\n")
                                        competition_str = f_event_str[:close_bracket]
                #                        f.write("name_str: "+ name_str + "\n")
                                        f_event_str = f_event_str[close_bracket:]
                #                        f.write("f_event_str: " + f_event_str + "\n\n\n")

                                        open_bracket = f_event_str.find('<a href=')
                                        f_event_str = f_event_str[open_bracket+9:]
                #                        f.write("f_event_str: " + f_event_str + "\n\n\n")
                                        close_bracket = f_event_str.find('">')
                #                        f.write("close_bracket: "+ str(close_bracket)+ "\n")
                                        competition_url_str = f_event_str[:close_bracket]
                #                        f.write("club_str: "+ club_str + "\n")
                                        f_event_str = f_event_str[close_bracket:]
                #                        f.write("f_event_str: " + f_event_str + "\n\n\n")

                                        if(st_date >= s_date and st_date <= e_date):
                                                if(DEBUG_WRITE):
                                                        f.write("day_str: "+ day_str + " st_date:" + str(st_date)
                                                                + " competition_str: "+ competition_str
                                                                + " competition_url_str: "+ competition_url_str + "\n")
                                                load_lpjs_competitions_results.objects.update_or_create(
                                                        competition_name = competition_str,
                                                        start_date = st_date,
                                                        defaults={
                                                        'source': "LPJS",
                                                        'source_url': "https://leonpauljuniorseries.co.uk/results",
                                                        'end_date':None,
                                                        'competition_url':"https://leonpauljuniorseries.co.uk/"+competition_url_str,
                                                        'date_added':timezone.now(),
                                                        'date_updated':timezone.now()
                                                        })
                                        else:
                                                if(DEBUG_WRITE):
                                                        f.write("SKIPPING:  "+ competition_str
                                                                + " competition_url_str: "+ competition_url_str + "\n")
                x += 1


def Clear_Load_Tables():

        load_lpjs_competitions_results.objects.all().delete()
        load_lpjs_competitions_results_events.objects.all().delete()
        load_lpjs_competitions_results_events_fencers.objects.all().delete()


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
        if os.environ.get("LPJS_DAYS_BACK") is not None:
                lpjs_days = os.environ.get("LPJS_DAYS_BACK")
        else:
                lpjs_days = None

        load_data = True
        if(len(args) == 1) and (args[0] == "reset"):
                tournaments.objects.filter(tourney_inbound = 'LPJS').delete()
                Clear_Load_Tables()
                if(DEBUG_WRITE):
                        f.write("   RESET INCLUDING LOAD TABLES... \n")
                ls_date = Make_String_Timezone_Aware("01/01/2022")
        else:
                ls_date = timezone.now() - relativedelta(days=int(lpjs_days))
        le_date = timezone.now() - relativedelta(days=1)

        f.write("DEBUG_WRITE: " + str(DEBUG_WRITE) + "\n")
        f.write("Load data: " + str(load_data) + "\n")
        f.write("lpjs_days_back:  " + str(lpjs_days) + "\n")
        f.write("New Start Date: " + str(ls_date) + "\n")
        f.write("New End Date: " + str(le_date) + "\n\n\n")

        if(load_data):
                record_log_data(app_name, "Get_LPJS_Load_Competitions_Results", "Starting")
                Get_LPJS_Load_Competitions_Results(f, ls_date, le_date, DEBUG_WRITE)
                record_log_data(app_name, "Get_LPJS_Load_Competitions_Results", "Completed")

                record_log_data(app_name, "Get_LPJS_Load_Competition_Results_Events", "Starting")
                Get_LPJS_Load_Competition_Results_Events(f, ls_date, le_date, DEBUG_WRITE)
                record_log_data(app_name, "Get_LPJS_Load_Competition_Results_Events", "Completed")

        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()
        record_log_data(app_name, funct_name, "Completed")
 


# python manage.py runscript integrations_load_lpjs

# python manage.py runscript integrations_load_lpjs --script-args reset
