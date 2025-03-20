#!/usr/bin/env python3

from scripts.x_helper_functions import *


from integrations.models import *
from tourneys.models import *

import inspect
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from datetime import datetime
import dateutil.parser
from decouple import config
import re


import pytz
import requests
import os
from dotenv import load_dotenv
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")


def pool_details(f, ftl_header, ftl_event, ftl_round, ftl_pool, ftl_endpoint, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("pool_details: " 
                        + str(ftl_pool.pool_id) + " " 
                        + str(ftl_event.event_id) + " " 
                        + str(ftl_round.round_id) + " " 
                        +str(timezone.now()) + "\n")

        end_point_list = []
#        end_point_list.append("https://oqqwr9a3mj.execute-api.us-east-2.amazonaws.com/v1/poolresults/" + ftl_event.event_id + "/" + ftl_round.round_id)
#        end_point_list.append("https://oqqwr9a3mj.execute-api.us-east-2.amazonaws.com/v1/pools/details/" + ftl_event.event_id + "/" + ftl_round.round_id + "/" + ftl_pool.pool_id)
#        end_point_list.append("https://oqqwr9a3mj.execute-api.us-east-2.amazonaws.com/v1/pools/details/" + ftl_round.round_id + "/" + ftl_pool.pool_id)
#        end_point_list.append("https://oqqwr9a3mj.execute-api.us-east-2.amazonaws.com/v1/pools/details/" + ftl_pool.pool_id)
#        end_point_list.append("https://oqqwr9a3mj.execute-api.us-east-2.amazonaws.com/v1/pool/details/" + ftl_event.event_id + "/" + ftl_round.round_id + "/" + ftl_pool.pool_id)
#        end_point_list.append("https://oqqwr9a3mj.execute-api.us-east-2.amazonaws.com/v1/pool/details/" + ftl_round.round_id + "/" + ftl_pool.pool_id)
#        end_point_list.append("https://oqqwr9a3mj.execute-api.us-east-2.amazonaws.com/v1/pool/details/" + ftl_pool.pool_id)
#        end_point_list.append("https://oqqwr9a3mj.execute-api.us-east-2.amazonaws.com/v1/pools/detail/" + ftl_event.event_id + "/" + ftl_round.round_id + "/" + ftl_pool.pool_id)
#        end_point_list.append("https://oqqwr9a3mj.execute-api.us-east-2.amazonaws.com/v1/pools/detail/" + ftl_round.round_id + "/" + ftl_pool.pool_id)
#        end_point_list.append("https://oqqwr9a3mj.execute-api.us-east-2.amazonaws.com/v1/pools/detail/" + ftl_pool.pool_id)
#        end_point_list.append("https://oqqwr9a3mj.execute-api.us-east-2.amazonaws.com/v1/pooldetails/" + ftl_event.event_id + "/" + ftl_round.round_id + "/" + ftl_pool.pool_id)
#        end_point_list.append("https://oqqwr9a3mj.execute-api.us-east-2.amazonaws.com/v1/pooldetails/" + ftl_round.round_id + "/" + ftl_pool.pool_id)
#        end_point_list.append("https://oqqwr9a3mj.execute-api.us-east-2.amazonaws.com/v1/pooldetails/" + ftl_pool.pool_id)
        end_point_list.append("https://fencingtimelive.com/pools/details/8C16C49FD1DA4793A4A28A23C595EA0B/530C93DC10304620875DF6B51E29E903/71F94BD5FAE1400F8FF9B7343C4D1A90")

        for x in end_point_list:
                f.write(str(x) + "\n")
                response = requests.get(x, headers=ftl_header)
                if(DEBUG_WRITE):
                        f.write("  response status code: " + str(response.status_code)+"\n")
                response.encoding = 'utf-8'
                print(response.content)
#                for y in response.json():
#                        if(DEBUG_WRITE):
#                                f.write("                               " + str(y) + "\n")

#        f.write("response.content: " + str(response.content)+"\n")
 #       if(response.status_code != 200):
#                f.write("ERROR:  blah - No 200 response.  Status Code: " + str(response.status_code) + "\n")






def clear_tables():
        load_ftl_tournaments.objects.all().delete()
        load_ftl_tournament_events.objects.all().delete()
        load_ftl_event_rounds.objects.all().delete()
        load_ftl_round_seeding.objects.all().delete()
        load_ftl_pool_round_pool.objects.all().delete()
        load_ftl_round_pool_results.objects.all().delete()
        load_ftl_round_pool_scores.objects.all().delete()
        load_ftl_elimination_scores.objects.all().delete()
        load_ftl_event_final_results.objects.all().delete()

def Load_FTL_Round_Pool_Scores(f, ftl_header, ftl_event, ftl_round, ftl_pool, ftl_endpoint, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("                           Load_FTL_Round_Pool_Scores: " 
                        + str(ftl_pool.pool_id) + " " 
                        + str(ftl_event.event_id) + " " 
                        + str(ftl_round.round_id) + " " 
                        +str(timezone.now()) + "\n")

        endpoint = ftl_endpoint + "poolscores/" + ftl_event.event_id + "/" + ftl_round.round_id + "/" + ftl_pool.pool_id
#        endpoint = "https://oqqwr9a3mj.execute-api.us-east-2.amazonaws.com/v1/poolscores/" + ftl_event.event_id + "/" + ftl_round.round_id + "/" + ftl_pool.pool_id
        response = requests.get(endpoint, headers=ftl_header)

        if(DEBUG_WRITE):
                f.write("                              response status code: " + str(response.status_code)+"\n")
#        f.write("response.content: " + str(response.content)+"\n")
        if(response.status_code != 200):
                f.write("ERROR:  Load_FTL_Round_Pool_Scores - No 200 response.  Status Code: " + str(response.status_code) + "\n")
        else:
                response.encoding = 'utf-8'
                for x in response.json():
                        if(DEBUG_WRITE):
#                                f.write("                               " + str(x) + "\n")
                                f.write("                                Working Load_FTL_Round_Pool_Scores: " 
                                        + str(x["number"]) + " " + str(ftl_pool.pool_id) + str(timezone.now()) + "\n")

                        pool_scores_id, created = load_ftl_round_pool_scores.objects.update_or_create(
                                pool_id_index = ftl_pool,
                                number = x["number"],
                                defaults={
                                'date_updated':timezone.now(),
                                'left_position':x["left_position"],
                                'left_member_num':x["left_member_num"],
                                'left_name':x["left_name"],
                                'left_score':x["left_score"],
                                'right_position':x["right_position"],
                                'right_member_num':x["right_member_num"],
                                'right_name':x["right_name"],
                                'right_score':x["right_score"],
                                'winner_member_num':x["winner_member_num"],
                                'winner_name':x["winner_name"]})
                
#    #                        if(DEBUG_WRITE):
##                                f.write("               Checking date_added\n")
                        if(pool_scores_id.date_added == None):
##                                if(DEBUG_WRITE):
##                                        f.write("               Updating date added\n")
                                load_ftl_round_pool_scores.objects.update_or_create(
                                        pool_id_index = ftl_pool,
                                        number = x["number"],                                        
                                        defaults={
                                                'date_added':timezone.now()})                
        if(DEBUG_WRITE):
                f.write("                            Completed: Load_FTL_Round_Pool_Scores: " 
                        + str(ftl_pool.pool_id) + " " + str(ftl_event.event_id) + " " 
                        + str(ftl_round.round_id) + " " + str(timezone.now()) + "\n")
def Load_FTL_Round_Pool_Results(f, ftl_header, ftl_event, ftl_round, ftl_pool, ftl_endpoint, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("                           Load_FTL_Round_Pool_Results: " 
                        + str(ftl_pool.pool_id) + " " 
                        + str(ftl_event.event_id) + " " 
                        + str(ftl_round.round_id) + " " 
                        +str(timezone.now()) + "\n")

        endpoint = ftl_endpoint + "poolresults/" + ftl_event.event_id + "/" + ftl_round.round_id
#        endpoint = "https://oqqwr9a3mj.execute-api.us-east-2.amazonaws.com/v1/poolresults/" + ftl_event.event_id + "/" + ftl_round.round_id
        response = requests.get(endpoint, headers=ftl_header)

        if(DEBUG_WRITE):
                f.write("                              response status code: " + str(response.status_code)+"\n")
#        f.write("response.content: " + str(response.content)+"\n")
        if(response.status_code != 200):
                f.write("ERROR:  Load_FTL_Round_Pool_Results - No 200 response.  Status Code: " + str(response.status_code) + "\n")
        else:
                response.encoding = 'utf-8'
                for x in response.json():
#                        if(1==1):
                        if(DEBUG_WRITE):
#                                f.write("                               " + str(x) + "\n")
                                f.write("                                Working Load_FTL_Round_Pool_Results: " 
                                        + str(x["place"]) + " " + str(x["name"]) + " " + str(x["tie"]) + str(timezone.now()) + "\n")

                        pool_results_id, created = load_ftl_round_pool_results.objects.update_or_create(
                                round_id_index = ftl_round,
                                place = x["place"],
                                name = x["name"],
                                tie = x["tie"],
                                defaults={
                                'date_updated':timezone.now(),
                                'v':x["v"],
                                'm':x["m"],
                                'vm':x["vm"],
                                'ts':x["ts"],
                                'tr':x["tr"],
                                'ind':x["ind"],
                                'prediction':x["prediction"],
                                'member_num':x["member_num"],
                                'division':x["division"],
                                'country':x["country"],
                                'club1':str(x["club1"])[0:90],
                                'club2':str(x["club2"])[0:90]})
                
    #                        if(DEBUG_WRITE):
#                                f.write("               Checking date_added\n")
                        if(pool_results_id.date_added == None):
#                                if(DEBUG_WRITE):
#                                        f.write("               Updating date added\n")
                                load_ftl_round_pool_results.objects.update_or_create(
                                        round_id_index = ftl_round,
                                        place = x["place"],
                                        tie = x["tie"],                                        
                                        name = x["name"],
                                        defaults={
                                                'date_added':timezone.now()})                
        if(DEBUG_WRITE):
                f.write("                            Completed: Load_FTL_Round_Pool_Results: " 
                        + str(ftl_pool.pool_id) + " " + str(ftl_event.event_id) + " " 
                        + str(ftl_round.round_id) + " " + str(timezone.now()) + "\n")
def Load_FTL_Pool_Round_Pools(f, ftl_header, ftl_event, ftl_round, ftl_endpoint, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("                     Load_FTL_Pool_Round_Pools: " 
                        + str(ftl_event.event_id) + " " 
                        + str(ftl_round.round_id) + " " 
                        +str(timezone.now()) + "\n")

        endpoint = ftl_endpoint + "pools/" + ftl_event.event_id + "/" + ftl_round.round_id
#        endpoint = "https://oqqwr9a3mj.execute-api.us-east-2.amazonaws.com/v1/pools/" + ftl_event.event_id + "/" + ftl_round.round_id
        response = requests.get(endpoint, headers=ftl_header)

        if(DEBUG_WRITE):
                f.write("                        response status code: " + str(response.status_code)+"\n")
#        f.write("response.content: " + str(response.content)+"\n")
        if(response.status_code != 200):
                f.write("ERROR:  Load_FTL_Pool_Round_Pools - No 200 response.  Status Code: " + str(response.status_code) + "\n")
        else:
                response.encoding = 'utf-8'
                for x in response.json():
                        if(DEBUG_WRITE):
#                                f.write("                         " + str(x) + "\n")
                                f.write("                          Working Pool Round Pool: " 
                                        + str(x["pool_id"]) + " " + str(ftl_round.round_id) + str(timezone.now()) + "\n")

                        if(x["startTime"] == None):
                                st = None
                        else:
                                st = timezone.make_aware(dateutil.parser.parse(x["startTime"]))

                        prp_id, created = load_ftl_pool_round_pool.objects.update_or_create(
                                round_id_index = ftl_round,
                                pool_id = x["pool_id"],
                                defaults={
                                'date_updated':timezone.now(),
                                'number':x["number"],
                                'size':x["size"],
                                'finished':x["finished"],
                                'strip':x["strip"],
                                'starttime':x['startTime'],
                                'starttime_time':st})
        
    #                        if(DEBUG_WRITE):
#                                f.write("               Checking date_added\n")
                        if(prp_id.date_added == None):
#                                if(DEBUG_WRITE):
#                                        f.write("               Updating date added\n")
                                load_ftl_pool_round_pool.objects.update_or_create(
                                round_id_index = ftl_round,
                                pool_id = x["pool_id"],
                                        defaults={
                                        'date_added':timezone.now()})

                        Load_FTL_Round_Pool_Scores(f, ftl_header, ftl_event, ftl_round, prp_id, ftl_endpoint, DEBUG_WRITE)
                        Load_FTL_Round_Pool_Results(f, ftl_header, ftl_event, ftl_round, prp_id, ftl_endpoint, DEBUG_WRITE)
                        #MISSING ONE...
                        #Pool Details - pool_details.  Will need to BeautifulSoup it.
                        #https://fencingtimelive.com/pools/details/8C16C49FD1DA4793A4A28A23C595EA0B/530C93DC10304620875DF6B51E29E903/71F94BD5FAE1400F8FF9B7343C4D1A90
        if(DEBUG_WRITE):
                f.write("                      Completed: Load_FTL_Pool_Round_Pools: " + str(ftl_round.round_id) + " " +str(timezone.now()) + "\n")
def Load_FTL_Round_Seeding(f, ftl_header, ftl_event, ftl_round, ftl_endpoint, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("                     Load_FTL_Round_Seeding: " 
                        + str(ftl_event.event_id) + " " 
                        + str(ftl_round.round_id) + " " 
                        +str(timezone.now()) + "\n")

        endpoint = ftl_endpoint + "seeding/" + ftl_event.event_id + "/" + ftl_round.round_id
#        endpoint = "https://oqqwr9a3mj.execute-api.us-east-2.amazonaws.com/v1/seeding/" + ftl_event.event_id + "/" + ftl_round.round_id
        response = requests.get(endpoint, headers=ftl_header)

        if(DEBUG_WRITE):
                f.write("                        response status code: " + str(response.status_code)+"\n")
#        f.write("response.content: " + str(response.content)+"\n")
        if(response.status_code != 200):
                f.write("ERROR:  Load_FTL_Round_Seeding - No 200 response.  Status Code: " + str(response.status_code) + "\n")
        else:
                response.encoding = 'utf-8'
                for x in response.json():
                        if(DEBUG_WRITE):
#                                f.write("                         " + str(x) + "\n")
                                f.write("                          Working Round: " 
                                        + str(x["seed"]) + " " + str(ftl_round.round_id) + str(timezone.now()) + "\n")

                        seed_id, created = load_ftl_round_seeding.objects.update_or_create(
                                round_id_index = ftl_round,
                                seed = x["seed"],
                                name = x["name"],
                                defaults={
                                'date_updated':timezone.now(),
                                'member_num':x["member_num"],
                                'division':x["division"],
                                'country':x["country"],
                                'club1':str(x["club1"])[0:90],
                                'club2':str(x["club2"])[0:90],
                                'rating':x["rating"],
                                'exempt':x["exempt"],
                                'excluded':x["excluded"],
                                'no_show':x["no_show"],
                                'eliminated':x["eliminated"],
                                'advanced':x["advanced"],
                                'status':x["status"]})
        
    #                        if(DEBUG_WRITE):
#                                f.write("               Checking date_added\n")
                        if(seed_id.date_added == None):
#                                if(DEBUG_WRITE):
#                                        f.write("               Updating date added\n")
                                load_ftl_round_seeding.objects.update_or_create(
                                        round_id_index = ftl_round,
                                        seed = x["seed"],
                                        name = x["name"],
                                        defaults={
                                        'date_added':timezone.now()})                
        if(DEBUG_WRITE):
                f.write("                      Completed: Load_FTL_Round_Seeding: " + str(ftl_round.round_id) + " " +str(timezone.now()) + "\n")
def Load_FTL_Elimination_Scores(f, ftl_header, ftl_event, ftl_round, ftl_endpoint, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("                     Load_FTL_Elimination_Scores: " 
                        + str(ftl_event.event_id) + " " 
                        + str(ftl_round.round_id) + " " 
                        +str(timezone.now()) + "\n")

        endpoint = ftl_endpoint + "elimscores/" + ftl_event.event_id + "/" + ftl_round.round_id
#        endpoint = "https://oqqwr9a3mj.execute-api.us-east-2.amazonaws.com/v1/elimscores/" + ftl_event.event_id + "/" + ftl_round.round_id
        response = requests.get(endpoint, headers=ftl_header)

        if(DEBUG_WRITE):
                f.write("                        response status code: " + str(response.status_code)+"\n")
#        f.write("response.content: " + str(response.content)+"\n")
        if(response.status_code != 200):
                f.write("ERROR:  Load_FTL_Elimination_Scores - No 200 response.  Status Code: " + str(response.status_code) + "\n")
        else:
                response.encoding = 'utf-8'
                for x in response.json():
                        if(DEBUG_WRITE):
#                                f.write("                         " + str(x) + "\n")
                                f.write("                          Working Load_FTL_Elimination_Scores: " 
                                        + str(x["table"]) + " " + str(x["number"]) + " "  + str(ftl_round.round_id) + str(timezone.now()) + "\n")

                        if(x["time"] == None):
                                st = None
                        else:
                                st = timezone.make_aware(dateutil.parser.parse(x["time"]))

                        es_id, created = load_ftl_elimination_scores.objects.update_or_create(
                                round_id_index = ftl_round,
                                table = x["table"],
                                number = x["number"],
                                defaults={
                                'date_updated':timezone.now(),
                                'strip':x["strip"],
                                'stime':st,
                                'score':x["score"],
                                'left_seed':x["left_seed"],
                                'left_member_num':x["left_member_num"],
                                'left_name':x["left_name"],
                                'right_seed':x["right_seed"],
                                'right_member_num':x["right_member_num"],
                                'right_name':x["right_name"],
                                'winner_member_num':x["winner_member_num"],
                                'winner_name':x["winner_name"]})
        
    #                        if(DEBUG_WRITE):
#                                f.write("               Checking date_added\n")
                        if(es_id.date_added == None):
#                                if(DEBUG_WRITE):
#                                        f.write("               Updating date added\n")
                                load_ftl_elimination_scores.objects.update_or_create(
                                        round_id_index = ftl_round,
                                        table = x["table"],
                                        number = x["number"],
                                        defaults={
                                        'date_added':timezone.now()})
        if(DEBUG_WRITE):
                f.write("                      Completed: Load_FTL_Elimination_Scores: " + str(ftl_round.round_id) + " " +str(timezone.now()) + "\n")
def Load_FTL_Event_Final_Results(f, ftl_header, ftl_event, ftl_endpoint, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("                     Load_FTL_Event_Final_Results: " 
                        + str(ftl_event.event_id) + " " + str(timezone.now()) + "\n")

        endpoint = ftl_endpoint + "results/" + ftl_event.event_id
#        endpoint = "https://oqqwr9a3mj.execute-api.us-east-2.amazonaws.com/v1/results/" + ftl_event.event_id
        response = requests.get(endpoint, headers=ftl_header)

        if(DEBUG_WRITE):
                f.write("                        response status code: " + str(response.status_code)+"\n")
#        f.write("response.content: " + str(response.content)+"\n")
        if(response.status_code != 200):
                f.write("ERROR:  Load_FTL_Event_Final_Results - No 200 response.  Status Code: " + str(response.status_code) + "\n")
        else:
                response.encoding = 'utf-8'
                load_ftl_event_final_results.objects.filter(event_id_index = ftl_event).delete()
                for x in response.json():
                        if(DEBUG_WRITE):
#                                f.write("                         " + str(x) + "\n")
                                f.write("                          Working Load_FTL_Event_Final_Results: " 
                                        + str(x["place"]) + " " + str(x["name"]) + " "  + str(ftl_event.event_id) + str(timezone.now()) + "\n")
                        efr_id, created = load_ftl_event_final_results.objects.update_or_create(
                                event_id_index = ftl_event,
                                place = x["place"],
                                name = x["name"],
                                defaults={
                                'date_updated':timezone.now(),
                                'club1':str(x["club1"])[0:90],
                                'club2':str(x["club2"])[0:90],
                                'division':x["division"],
                                'country':x["country"],
                                'member_num':x["member_num"],
                                'old_rating':x["old_rating"]})
        
    #                        if(DEBUG_WRITE):
#                                f.write("               Checking date_added\n")
                        if(efr_id.date_added == None):
#                                if(DEBUG_WRITE):
#                                        f.write("               Updating date added\n")
                                load_ftl_event_final_results.objects.update_or_create(
                                        event_id_index = ftl_event,
                                        place = x["place"],
                                        name = x["name"],
                                        defaults={
                                                'date_added':timezone.now()})
        if(DEBUG_WRITE):
                f.write("                      Completed: Load_FTL_Event_Final_Results: " + str(ftl_event.event_id) + " " +str(timezone.now()) + "\n")

def Load_FTL_Event_Rounds(f, ftl_header, ftl_event, ftl_endpoint, DEBUG_WRITE):
#        DEBUG_WRITE = True
        if(DEBUG_WRITE):
                f.write("                  Load_FTL_Event_Rounds: " + str(ftl_event.event_id) + " " +str(timezone.now()) + "\n")

        endpoint = ftl_endpoint + "rounds/" + ftl_event.event_id
#        endpoint = "https://oqqwr9a3mj.execute-api.us-east-2.amazonaws.com/v1/rounds/" + ftl_event.event_id
        response = requests.get(endpoint, headers=ftl_header)

        if(DEBUG_WRITE):
                f.write("                     response status code: " + str(response.status_code)+"\n")
#        f.write("response.content: " + str(response.content)+"\n")
        if(response.status_code != 200):
                f.write("ERROR:  Load_FTL_Event_Rounds - No 200 response.  Status Code: " + str(response.status_code) + "\n")
        else:
                response.encoding = 'utf-8'
                for x in response.json():
                        if(DEBUG_WRITE):
#                                f.write("                      " + str(x) + "\n")
                                f.write("                       Working Round: " + x["event_id"] + " - " + x["round_id"] + " " + str(timezone.now()) + "\n")
                        round_id, created = load_ftl_event_rounds.objects.update_or_create(
                                round_id = x["round_id"],
                                event_id = x["event_id"],
                                defaults={
                                'date_updated':timezone.now(),
                                'event_id_index':ftl_event,
                                'r_number':x["number"],
                                'r_type':x["type"],
                                'r_finished':x["finished"]})
        
    #                        if(DEBUG_WRITE):
#                                f.write("               Checking date_added\n")
                        if(round_id.date_added == None):
#                                if(DEBUG_WRITE):
#                                        f.write("               Updating date added\n")
                                load_ftl_event_rounds.objects.update_or_create(
                                        round_id = x["round_id"],
                                        event_id = x["event_id"],
                                                defaults={
                                                'date_added':timezone.now()})
                        Load_FTL_Pool_Round_Pools(f, ftl_header, ftl_event, round_id, ftl_endpoint, DEBUG_WRITE)
                        Load_FTL_Round_Seeding(f, ftl_header, ftl_event, round_id, ftl_endpoint, DEBUG_WRITE) 
                        Load_FTL_Elimination_Scores(f, ftl_header, ftl_event, round_id, ftl_endpoint, DEBUG_WRITE)
                        Load_FTL_Event_Final_Results(f, ftl_header, ftl_event, ftl_endpoint, DEBUG_WRITE)
        if(DEBUG_WRITE):
                f.write("                   Completed: Load_FTL_Event_Rounds: " + str(ftl_event.event_id) + " " +str(timezone.now()) + "\n")
def Load_FTL_Tournament_Events(f, ftl_header, ftl_tourney, ftl_endpoint, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("            Load_FTL_Tournament_Events: " + str(ftl_tourney.tournament_id) + " " +str(timezone.now()) + "\n")

        endpoint = ftl_endpoint + "events/" + ftl_tourney.tournament_id
#        endpoint = "https://oqqwr9a3mj.execute-api.us-east-2.amazonaws.com/v1/events/" + ftl_tourney.tournament_id
        response = requests.get(endpoint, headers=ftl_header)

        if(DEBUG_WRITE):
                f.write("               response status code: " + str(response.status_code)+"\n")
#        f.write("response.content: " + str(response.content)+"\n")
        if(response.status_code != 200):
                f.write("ERROR:  Load_FTL_Tournament_Events - No 200 response.  Status Code: " + str(response.status_code) + "\n")
        else:
                response.encoding = 'utf-8'
                for x in response.json():
                        found_event = False
                        t_start = timezone.now()
                        if(DEBUG_WRITE):
                                f.write("                Working Event: " + x["event_id"] + " - " + x["name"] + " " + str(timezone.now()) + "\n")
###DEBUG ONLY
#                        try:
#                                load_ftl_tournament_events.objects.get(tournament_id_index = ftl_tourney,event_id = x["event_id"])
#                        except:
#                                found_event = False
#                        else:
#                                found_event = True
###DEBUG ONLY
#                        if(not found_event):
                        if(x["finish_time"] == None):
                                ft = None
                        else:
                                ft = timezone.make_aware(dateutil.parser.parse(x["finish_time"]))

                        event_id, created = load_ftl_tournament_events.objects.update_or_create(
                                event_id = x["event_id"],
                                tournament_id = x["tournament_id"],
                                defaults={
                                'date_updated':timezone.now(),
                                'tournament_id_index':ftl_tourney,
                                'name':x["name"],
                                's_date':x["date"],
                                's_time':x["time"],
                                'start_date': timezone.make_aware(dateutil.parser.parse(x["date"]+"T"+x["time"])),
                                'size':x["size"],
                                'finished':x["finished"],
                                'finish_time':ft})

#                        if(DEBUG_WRITE):
#                                f.write("               Checking date_added\n")
                        if(event_id.date_added == None):
#                                if(DEBUG_WRITE):
#                                        f.write("               Updating date added\n")
                                load_ftl_tournament_events.objects.update_or_create(
                                        event_id = x["event_id"],
                                        tournament_id = x["tournament_id"],
                                        defaults={
                                        'date_added':timezone.now()})                
                        Load_FTL_Event_Rounds(f, ftl_header, event_id, ftl_endpoint, False)
        if(DEBUG_WRITE):
                f.write("             Completed Load_FTL_Tournament_Events: " + str(ftl_tourney.tournament_id) + " " +str(timezone.now()) + "\n")
def Load_FTL_Tournaments_In_Range(f, ftl_header, r_start, r_end, ftl_endpoint, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      Load_FTL_Tournaments_In_Range: " + str(r_start)+ " " + str(r_end) + " " +str(timezone.now()) + "\n")
        print("      Load_FTL_Tournaments_In_Range: " + str(r_start)+ " " + str(r_end) + " " +str(timezone.now()))

        endpoint = ftl_endpoint + "tournaments?"
#        endpoint = "https://oqqwr9a3mj.execute-api.us-east-2.amazonaws.com/v1/tournaments?"
        query_params = {"from": str(r_start), "to": str(r_end)}
        if(DEBUG_WRITE):
                f.write("         endpoint: " + str(endpoint)+ " " + str(ftl_header) + " " + str(query_params) + "\n")

        response = requests.get(endpoint, params=query_params, headers=ftl_header)
        if(DEBUG_WRITE):
                f.write("         response status code: " + str(response.status_code)+"\n")
#        f.write("response.content: " + str(response.content)+"\n")
        if(response.status_code != 200):
                f.write("ERROR:  Load_FTL_Tournaments_In_Range - No 200 response.  Status Code: " + str(response.status_code) + "\n")
        else:
                response.encoding = 'utf-8'
                for x in response.json():
                        if (1==1):
#                        if("leon paul d" in x["name"].lower()):
#                                        "welsh open 2022",
#                                      "sussex open 2022",
#                                      "10th leon paul foil open",
#                                      "birmingham international fencing tournament 2024", 
#                                      "exeter open 2024"
#                                      )):

                                t_start = timezone.now()
                                print("Loading Tournament FTL: " + x["name"] + " - " + x["start"]+ " - " + str(timezone.now()))

                                if(DEBUG_WRITE):
                                        f.write("         Working Tournament: " + x["tournament_id"] + " - " + x["name"] + " - " + x["location"] + " - " + x["start"]+ " - " + x["end"]+ " " + str(timezone.now()) + "\n")

                                tournament_id, created = load_ftl_tournaments.objects.update_or_create(
                                                tournament_id = x["tournament_id"],
                                                defaults={
                                                'date_updated':timezone.now(),
                                                'name':x["name"],
                                                'location':x["location"],
                                                'start':x["start"],
                                                'end':x["end"],
                                                'start_date': timezone.make_aware(dateutil.parser.parse(x["start"])),
                                                'end_date': timezone.make_aware(dateutil.parser.parse(x["end"]))})
                                if(tournament_id.date_added == None):
                                        load_ftl_tournaments.objects.update_or_create(
                                                tournament_id = x["tournament_id"],
                                                defaults={
                                                'date_added':timezone.now()})                
                                Load_FTL_Tournament_Events(f, ftl_header, tournament_id, ftl_endpoint, DEBUG_WRITE)
        if(DEBUG_WRITE):
                f.write("       Completed: Load_FTL_Tournaments_In_Range: " + str(r_start)+ " "+ str(r_end) + "   " +str(timezone.now()) + "\n")
def Drive_FTL_Tournaments(f, app_name, ftl_header, s_date, e_date, ftl_endpoint, DEBUG_WRITE):
        f.write("\nDrive_FTL_Tournaments: Start Date: " + str(s_date) + " End Date: " + str(e_date) + " " + str(timezone.now()) + "\n")
        rng = 10

        r_start = s_date
        if(r_start + relativedelta(days=rng) > e_date):
                r_end = e_date
        else:
                r_end = r_start + relativedelta(days=rng)
        while(r_start <= e_date):
                if(DEBUG_WRITE):
                        f.write("   Range Start Date: " + str(r_start) + "   Range End Date: " + str(r_end) + " " + str(timezone.now()) + "\n")
                record_log_data(app_name, "Load_FTL_Tournaments_In_Range", "Starting: " + str(r_start) + " - " + str(r_end))
                Load_FTL_Tournaments_In_Range(f, ftl_header, r_start, r_end, ftl_endpoint, False)
                r_start = r_end + relativedelta(days=1)
                if(r_start + relativedelta(days=rng) > e_date):
                        r_end = e_date
                else:
                        r_end = r_start + relativedelta(days=rng)
        f.write("Completed Drive_FTL_Tournaments: " + str(timezone.now()) + "\n")

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
        DEBUG_WRITE = True
        if(1==1): #get the values from the .env file
                if os.environ.get("FTL_X_API_KEY") is not None:
                        header={"x-api-key" : os.environ.get("FTL_X_API_KEY")}
                else:
                        header = None
                if os.environ.get("FTL_ENDPOINT") is not None:
                        ftl_end = os.environ.get("FTL_ENDPOINT")
                else:
                        ftl_end = None
                if os.environ.get("FTL_DAYS_BACK") is not None:
                        ftl_days_back = os.environ.get("FTL_DAYS_BACK")
                else:
                        ftl_days_back = None
                if os.environ.get("FTL_TOURNAMENT_URL") is not None:
                        ftl_tourney_url = os.environ.get("FTL_TOURNAMENT_URL")
                else:
                        ftl_tourney_url = None

        asn = get_association(f, "British Fencing", DEBUG_WRITE)
        if(DEBUG_WRITE):
                f.write("DEBUG_WRITE: " + str(DEBUG_WRITE) + "\n")
#                f.write("header: " + str(header) + "\n")
                f.write("endpoint: " + str(ftl_end) + "\n")
                f.write("days back: " + str(ftl_days_back) + "\n")
                f.write("asn:  " + str(asn.assn_name) + "\n")

        if(header is None or ftl_end is None or ftl_days_back is None or ftl_tourney_url is None):
                record_error_data(app_name, funct_name, "Error", "Error:  FTL ENV VALUES MISSING")
                f.write("\n\n\n\nError:  FTL ENV VALUES MISSING: " + str(timezone.now()) + "\n")
        else:
                if 'reset' in args:
                        f.write("   RESETTING... \n")
                        tournaments.objects.filter(tourney_inbound = 'FencingTimeLive').delete()
                        clear_tables()  ###clears all the load tables
                if(len(args) == 2):
                        ls_date = Make_String_Timezone_Aware(args[0])
                        le_date = Make_String_Timezone_Aware(args[1])
                elif(len(args) > 2):
                        ls_date = Make_String_Timezone_Aware(args[1])
                        le_date = Make_String_Timezone_Aware(args[2])
                if(1==1):
                        f.write("New Start Date: " + str(ls_date) + "\n")
                        f.write("New End Date: " + str(le_date) + "\n")

                record_log_data(app_name, "Drive_FTL_Tournaments", "Starting")
                Drive_FTL_Tournaments(f, app_name, header, ls_date, le_date, ftl_end, DEBUG_WRITE)
                record_log_data(app_name, "Drive_FTL_Tournaments", "Completed")

        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()
        record_log_data(app_name, funct_name, "Completed")


# python manage.py runscript integrations_load_ftl
# python manage.py runscript integrations_load_ftl --script-args reset
# python manage.py runscript integrations_load_ftl --script-args reset 01/01/2023 31/12/2023
# python manage.py runscript integrations_load_ftl --script-args 05/01/2024 12/31/2024

