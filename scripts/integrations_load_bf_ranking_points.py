#!/usr/bin/env python3

from scripts.x_helper_functions import *
from scripts.x_helper_assn_specific import *

from integrations.models import *
from tourneys.models import *

from bs4 import BeautifulSoup
import inspect
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from datetime import datetime
import dateutil.parser
from decouple import config


import pytz
import requests
import os
from dotenv import load_dotenv
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")



def derive_values_from_url(f, complete_url, DEBUG_WRITE):
        asn = get_association(f, "British Fencing", DEBUG_WRITE)

        gender_found = None
        for x in association_genders.objects.filter(assn=asn).order_by('-gender_name'):
                if (x.gender_name.lower() in complete_url.lower() and gender_found is None):
                        gender_found = x
        if(gender_found is None):
                gender_found = association_genders.objects.filter(assn=asn, gender_name = "Unknown")
                record_error_data("integrations_load_bf_ranking_points", derive_values_from_url, "Error", "Error:  Could not find gender from URL: " + str(complete_url))

        discipline_found = None
        for x in association_discipline.objects.filter(assn=asn):
                if (x.discipline_name.lower() in complete_url.lower() and discipline_found is None):
                        discipline_found = x
        if(discipline_found is None):
                discipline_found = association_discipline.objects.filter(assn=asn, discipline_name = "Foil")
                record_error_data("integrations_load_bf_ranking_points", derive_values_from_url, "Error", "Error:  Could not find discipline from URL: " + str(complete_url))

        type_found = association_types(assn=asn, type_category='Individual')

        age_found = None
        for x in association_ages.objects.filter(assn=asn):
                if (x.age_category.lower() in complete_url.lower() and age_found is None):
                        age_found = x
        if(age_found is None):
                age_found = association_ages.objects.filter(assn=asn, age_category = "Senior")
                record_error_data("integrations_load_bf_ranking_points", derive_values_from_url, "Error", "Error:  Could not find age from URL: " + str(complete_url))

        if(DEBUG_WRITE):
                f.write("derive_values_from_url: " + str(gender_found.gender_name) 
                        + " " + str(discipline_found.discipline_name)
                        + " " + str(type_found.type_category)
                        + " " + str(age_found.age_category) + "\n")
        return(gender_found, discipline_found, type_found, age_found)       

def Load_BF_Ranking(f, url, url_type, DEBUG_WRITE):
        f.write("Load_BF_Ranking:  " + str(timezone.now()) + " " + url + "\n")

        asn = get_association(f, "British Fencing", DEBUG_WRITE)
        assn_recs = association_members.objects.filter(assn = asn).values_list('assn_member_full_name', flat=True)
        rnk = requests.get(url)
        if rnk.status_code != 200:
                f.write("Request failed with status code: " + str(rnk.status_code) + "\n")
        else:
                gen, disp, r_type, age = derive_values_from_url(f, url, DEBUG_WRITE)

                bf_member_rank_points.objects.filter(bfmr_gender = gen,
                        bfmr_discipline = disp, bfmr_type = r_type,
                        bfmr_ages = age).delete()
                BF_delete_bf_ranking(f, disp.discipline_name, gen.gender_name, age.age_category, DEBUG_WRITE)

                rnk_soup = BeautifulSoup(rnk.content, 'html.parser')
                rnk_table = (rnk_soup.find("table"))
                try:
                        rnk_table.find_all('tr')
                except:
                        f.write("No final results for URL: " + url + "\n")
                else:          
                        row_count = 1      
                        for row in rnk_table.find_all('tr'):    
                                columns = row.find_all('td')
                                if(columns != []):
                                        if(row_count == 1):
                                                up_date = columns[0].text.strip()
                                        elif(row_count == 2):
                                                cat = columns[0].text.strip() 
                                                up_date2 = columns[1].text.strip()
#                                                Clear_BF_Rank_Points(f, cat)
                                        elif((row_count > 5 and url_type == 'new') or (row_count > 5 and url_type == 'old')):
                                                try: 
                                                        columns[4].text.strip()
                                                except:
                                                        f.write("skipping input row\n")
                                                else:
                                                        rank = columns[0].text.strip()
                                                        name = columns[1].text.strip()
                                                        yob = columns[2].text.strip()
                                                        club = columns[3].text.strip()
                                                        license = columns[4].text.strip()
                                                        total_points = columns[5].text.strip()
                                                        dom_points = columns[6].text.strip()
                                                        dom_events = columns[7].text.strip()
                                                        intl_points = columns[8].text.strip()
                                                        intl_events = columns[9].text.strip()

#                                                        if(1==0):
                                                        if(DEBUG_WRITE):
                                                                f.write("                rank: " + str(rank) 
                                                                        + " name: " + str(name)
                                                                        + " yob: " + str(yob)
                                                                        + " club: " + str(club)
                                                                        + " license: " + str(license)
                                                                        + " total_points: " + str(total_points)
                                                                        + " dom_points: " + str(dom_points)
                                                                        + " dom_events: " + str(dom_events)
                                                                        + " intl_points: " + str(intl_points)
                                                                        + " intl_events: " + str(intl_events) + "\n")
                                                        amr = get_assn_member_record(f, asn, assn_recs, str(license), str(name), "", "", DEBUG_WRITE)
                                                        if(amr is not None):
                                                                bfrp, created = bf_member_rank_points.objects.update_or_create(
                                                                        bfmr_rank = rank, bfmr_license = license,
                                                                        defaults={
                                                                        'bfmr_assn_member' : amr,
                                                                        'bfmr_type' : None,
                                                                        'bfmr_gender' : gen,
                                                                        'bfmr_discipline' : disp,
                                                                        'bfmr_ages' : age,
                                                                        'bfmr_total_points' : total_points,
                                                                        'bfmr_dom_points' : dom_points,
                                                                        'bfmr_dom_events' : dom_events,
                                                                        'bfmr_intl_points' : intl_points,
                                                                        'bfmr_intl_events' : intl_events,
                                                                        'bfmr_update_date' : timezone.now()
                                                                        }) 
                                                                BF_update_or_create_bf_ranking(f, amr, disp.discipline_name, gen.gender_name, age.age_category, rank, timezone.now(), DEBUG_WRITE)
                                                        else:
                                                                record_error_data("integrations_load_bf_ranking_points", "Load_BF_Ranking", "Error", "Error:  Could not find member: " + str(name) + " " + str(license))
                                row_count = row_count + 1


def Load_Latest_BF_Rankings(f, DEBUG_WRITE):
        Load_BF_Ranking(f, 'https://www.britishfencing.com/wp-content/uploads/live-ranking/senior-mens-foil.html', 'new', DEBUG_WRITE)
        Load_BF_Ranking(f, 'https://www.britishfencing.com/wp-content/uploads/live-ranking/u23-mens-foil.html', 'new', DEBUG_WRITE)
        Load_BF_Ranking(f, 'https://www.britishfencing.com/wp-content/uploads/live-ranking/senior-womens-foil.html', 'new', DEBUG_WRITE)
        Load_BF_Ranking(f, 'https://www.britishfencing.com/wp-content/uploads/live-ranking/u23-womens-foil.html', 'new', DEBUG_WRITE)

        Load_BF_Ranking(f, 'https://www.britishfencing.com/wp-content/uploads/live-ranking/senior-mens-epee.html', 'new', DEBUG_WRITE)
        Load_BF_Ranking(f, 'https://www.britishfencing.com/wp-content/uploads/live-ranking/u23-mens-epee.html', 'new', DEBUG_WRITE)
        Load_BF_Ranking(f, 'https://www.britishfencing.com/wp-content/uploads/live-ranking/senior-womens-epee.html', 'new', DEBUG_WRITE)
        Load_BF_Ranking(f, 'https://www.britishfencing.com/wp-content/uploads/live-ranking/u23-womens-epee.html', 'new', DEBUG_WRITE)

        Load_BF_Ranking(f, 'https://www.britishfencing.com/wp-content/uploads/live-ranking/senior-mens-sabre.html', 'new', DEBUG_WRITE)
        Load_BF_Ranking(f, 'https://www.britishfencing.com/wp-content/uploads/live-ranking/u23-mens-sabre.html', 'new', DEBUG_WRITE)
        Load_BF_Ranking(f, 'https://www.britishfencing.com/wp-content/uploads/live-ranking/senior-womens-sabre.html', 'new', DEBUG_WRITE)
        Load_BF_Ranking(f, 'https://www.britishfencing.com/wp-content/uploads/live-ranking/u23-womens-sabre.html', 'new', DEBUG_WRITE)

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

        record_log_data(app_name, funct_name, "Starting")
        DEBUG_WRITE = False

        if(DEBUG_WRITE):
                f.write("DEBUG_WRITE: " + str(DEBUG_WRITE) + "\n")

        if 'load' in args:
                cmd_count = len(args) -1
                f.write("Loading Specific Ranking: " + str(args[cmd_count]) + " " + str(datetime.now()) + "\n")
                record_log_data(app_name, "Load_BF_Ranking", "Starting")
                Load_BF_Ranking(f, args[cmd_count], 'old', DEBUG_WRITE)
                record_log_data(app_name, "Load_BF_Ranking", "Complete")
        else:
                f.write("Loading All Rankings: " + str(datetime.now()) + "\n")
                record_log_data(app_name, "Load_Latest_BF_Rankings", "Starting")
                Load_Latest_BF_Rankings(f, DEBUG_WRITE)
                record_log_data(app_name, "Load_Latest_BF_Rankings", "Complete")

        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()
        record_log_data(app_name, funct_name, "Completed")


# python manage.py runscript integrations_load_bf_ranking_points

# python manage.py runscript integrations_load_bf_ranking_points --script-args load https://www.britishfencing.com/wp-content/uploads/ranking/cadet-womens-epee-02-10-2023-0815.html
