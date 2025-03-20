#!/usr/bin/env python3

from scripts.x_helper_functions import *

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



def Build_Event_Club_Name(f, eve_org, eve_evt, eve_compe):

        given_name = ""
        given_club = "Unknown"

        url = 'https://engarde-service.com/competition/' + eve_org + '/' + eve_evt + '/' + eve_compe
        eve = requests.get(url)
        eve_soup = BeautifulSoup(eve.content, 'html.parser')
#        f.write(str(eve_soup))
        eve_club_soup = eve_soup.find_all("div", class_="banner-titles")
        if(len(eve_club_soup) > 0):
                given_club_hld = eve_club_soup[0].text.strip()
                if(len(given_club_hld) > 0):
#                        if(given_club_hld.isdigit()):
#                                given_club = "Unknown"
#                        else:
                        given_club = given_club_hld
                
        eve_name_soup = eve_soup.find_all("div", class_="tounament-titles")
        if(len(eve_name_soup) > 0):
                given_name = eve_name_soup[0].text.strip()
        return(given_club, given_name)

def Load_Events(f, DEBUG_WRITE):
        f.write("Load Engarde Events: " + str(datetime.now()) + "\n")

        url = "https://engarde-service.com/prog/getCompeForDisplay.php"

        params = {
                'option':'history', 
                'orderby': 'typecompe_date',
#SOMETHING WEIRD ON THEIR MySQL query.  Defaulting to 2000 rows to catch everything.
#                'dateto': "2023-7-28",  #WORKS
#                'datefrom': "2023-7-28",  #WORKS
                'country':'GBR',
                'order':'DESC',
                'nrows':'2000'
        }
#        f.write(url+"\n\n")
        response = requests.post(url, params=params)
#        print(response.text)
        if(response.status_code != 200):
                f.write("ERROR Loading Tournaments.  Status Code = " + str(response.status_code) + "\n")
        else:   #Good status code
                if(response.text[:5] == 'false'):
                        f.write("ERROR Loading Tournaments.  Status Code = " + str(response.status_code) + "\n")
                        f.write("ERROR Message: \n" + str(response.text) + "\n")
                else:
#                        f.write("\n\n\n"+response.text)
                        dict = xmltodict.parse(response.text)
#                        pretty = json.dumps(dict, indent=4)
#                        f.write("\n\n"+ pretty + "\n\n")

                        for x in dict["comps"]["comp"]:
#                                f.write("Loading Event:  "+ str(x["@org"]) + " " + str(x["@evt"]) + " " + str(x["titre"]) + " " + str(x["@compe"]) + " " + str(x["@date"]) + "\n")
                                given_club, given_tourney = Build_Event_Club_Name(f, x["@org"], x["@evt"], x["@compe"])
#                                print("Storing Record: ", datetime.now())
                                # Assuming x["@date"] is in the format 'YYYY MM DD'
                                try:
                                        datetime.strptime(x["@date"], '%Y %m %d')
                                except:
                                        c_startdate = None
                                else:
                                        calced_startdate_naive = datetime.strptime(x["@date"], '%Y %m %d')
                                        c_startdate = timezone.make_aware(calced_startdate_naive, timezone.get_default_timezone())
                                load_engarde_event.objects.update_or_create(
                                                org = x["@org"],
                                                evt = x["@evt"],
                                                titre = x["titre"],
                                                compe = x["@compe"], 
                                                startdate = x["@date"],
                                                calced_startdate = c_startdate,
                                                defaults={
                                                        'sexe':x["@sexe"],
                                                        'arme':x["@arme"],
                                                        'test':x["@test"],
                                                        'estindividuelle':x["@estindividuelle"],
                                                        'live':x["@live"],
                                                        'etype':x["@type"],
                                                        'startTime':x["@startTime"],
                                                        'etat':x["@etat"],
                                                        'pays':x["@pays"],
                                                        'ville':x["@ville"],
                                                        'idsmart':x["@idsmart"],
                                                        'categorie':x["categorie"],
                                                        'content':x["content"],
                                                        'given_club_name':given_club,
                                                        'given_tournament_name':given_tourney,
                                                        })
#                                print("Storing Record Done: ", datetime.now())
def Load_Event_Final_Results(f, DEBUG_WRITE):
        f.write("Load Engarde Event Final Results: " + str(datetime.now()) + "\n")

        for x in load_engarde_event.objects.filter(estindividuelle = '1'): #filter(evt = "exeteropen2023", compe = "mf"):  #.all():
                #If we do not have final_results
                if (load_engarde_final_results.objects.filter(org = x.org, evt = x.evt, compe = x.compe, 
                                                                titre = x.titre,startdate = x.startdate).count() > 0):
                        if(DEBUG_WRITE):
                                f.write("SKIPPING FINAL EVENT RESULTS: https://engarde-service.com/competition/" + x.org + '/' + x.evt + '/' + x.compe + "\n")
                else:
                        url = 'https://engarde-service.com/competition/' + x.org + '/' + x.evt + '/' + x.compe
#                        f.write("PROCESSING FINAL EVENT RESULTS: URL: " + url + "\n")
                        eve = requests.get(url)
                        eve_soup = BeautifulSoup(eve.content, 'html.parser')
        #                f.write(str(eve_soup))
#                        f.write(str(eve_soup.prettify()))
                        eve_table = (eve_soup.find("table"))
        #                print(eve_table)
                        try:
                                eve_table.find_all('tr')
                        except:
                                if(DEBUG_WRITE):
                                        f.write("No final results for URL: " + url + "\n")
                        else:                
                                for row in eve_table.find_all('tr'):
                                        pos = ""    
                                        columns = row.find_all('td')
                                        if(len(columns) >= 3):
                                                pos = columns[0].text.strip() 
                                                l_name = columns[1].text.strip() 
                                                f_name = columns[2].text.strip()
                                        if(len(columns) >= 4):
                                                c_name = columns[3].text.strip()
                                        else:
                                                c_name = "Unknown"
                                        if(len(pos) > 0):
#                                                f.write("Loading Result--> Position: " + pos
#                                                + " Last Name: " + l_name
#                                                + " First Name: " + f_name
#                                                + " Club: " + c_name + "\n")

                                                load_engarde_final_results.objects.update_or_create(
                                                                org = x.org,
                                                                evt = x.evt,
                                                                compe = x.compe, 
                                                                titre = x.titre,
                                                                startdate = x.startdate,

                                                                position = pos, 
                                                                last_name = l_name, 
                                                                first_name = f_name, 
                                                                defaults={
                                                                        'club_name':c_name
                                                                })
                                        else:
                                                if(DEBUG_WRITE):
                                                        f.write("SKIPPING--->" + str(columns) + "\n")



def Clear_Load_Tables():
        load_engarde_event.objects.all().delete()
        load_engarde_final_results.objects.all().delete()

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

        if(len(args) == 1) and (args[0] == "reset"):
                tournaments.objects.filter(tourney_inbound = 'engarde').delete()
                Clear_Load_Tables()  #only used for testing

        record_log_data(app_name, "Load_Events", "Starting")
        Load_Events(f, DEBUG_WRITE)
        record_log_data(app_name, "Load_Events", "Completed")

        record_log_data(app_name, "Load_Event_Final_Results", "Starting")
        Load_Event_Final_Results(f, DEBUG_WRITE)
        record_log_data(app_name, "Load_Event_Final_Results", "Completed")

        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()
        record_log_data(app_name, funct_name, "Completed")
 

# python manage.py runscript integrations_load_engarde
# python manage.py runscript integrations_load_engarde --script-args reset




