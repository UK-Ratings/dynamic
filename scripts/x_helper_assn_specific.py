#!/usr/bin/env python3

from base.models import *
from django.utils import timezone
from django.utils.translation import get_language
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, DatabaseError


from scripts.x_helper_functions import *

from assn_mgr.models import *    
from club_mgr.models import *
from base.models import *
from tourneys.models import *
from integrations.models import *

import math
import os
import requests
import json
import io
import re
from django.forms.models import model_to_dict
from django.db.models.functions import Cast

from django.urls import reverse
from django.db.models import Q

from dotenv import load_dotenv
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")


def clean_position(char_pos):
# Remove any alphabetic characters from ers_seed
        dig = re.sub(r'\D', '', char_pos)
        if(len(dig) > 0):
                if dig.isdigit():
                        pos = int(dig)
        else:
                pos = 999
        return pos
def Event_Exists(f, asn, tourney_name, event_name, tourney_start_date, check_event_results, eve_results_count, DEBUG_WRITE):
        fcnt_start = datetime.now()
        found_event = False
        eve = None
        max_events = 0
        checked_in_detail = 0
        count_percent_error = .50

        event_to_check_days_before_and_after = int(os.environ.get("DURHAM_EVENT_EXISTS_DAYS_BEFORE_AFTER"))      
        results_accuracy = int(os.environ.get("DURHAM_EVENT_EXISTS_RESULTS_ACCURACY"))            #open up to cover when two systems keep numbers differently (DNF as example)
        same_event_min_hit = int(os.environ.get("DURHAM_EVENT_EXISTS_SAME_MIN_HIT"))          #number of exact same names in same positions to be the same event
        total_recs_to_check = int(os.environ.get("DURHAM_EVENT_EXISTS_REC_TO_CHECK"))
        #only uses the records with efr_assn_member_number.  If None or Null or 0 then record ignored 

        pot_start_date = tourney_start_date - relativedelta(days=event_to_check_days_before_and_after)
        pot_end_date = tourney_start_date + relativedelta(days=event_to_check_days_before_and_after)

        if(DEBUG_WRITE):
                f.write("               Running Event_Exists: " + str(fcnt_start)
                        + " event_to_check_days_before_and_after: " + str(event_to_check_days_before_and_after)
                        + " results_accuracy: " + str(results_accuracy)
                        + " same_event_min_hit: " + str(same_event_min_hit)
                        + " pot_start_date: " + str(pot_start_date)
                        + " pot_end_date: " + str(pot_end_date)
                        + " total_recs_to_check: " + str(total_recs_to_check) + "\n")
        if(DEBUG_WRITE):
                f.write("                    "  
                        + " Tourney Name: " + str(tourney_name)
                        + " Event Name: " + str(event_name)
                        + " Start Date: " + str(tourney_start_date) 
                        + " check_event_results Count: " + str(len(check_event_results))
                        + " Results Count: " + str(eve_results_count) + "\n")  

        potential_events = events.objects.filter(ev_tourney__tourney_start_date__gte = pot_start_date,
                        ev_tourney__tourney_start_date__lt = pot_end_date).exclude(ev_tourney__tourney_inbound__icontains='upcoming')
        max_checked = len(potential_events)
        if(DEBUG_WRITE):
                f.write("               Potential Event Count: " + str(max_checked) + "\n")  

        for x in potential_events:
                if(not found_event):
                        efr_count = event_final_results.objects.filter(efr_event = x).count()
                        if(DEBUG_WRITE):
                                f.write("                Checking Potential Event: " + str(x.ev_tourney.tourney_name) 
                                        + " " + str(x.ev_name) + " total event_final_result records:" + str(efr_count) + "\n")
                        if(1==1):
#                        if(eve_results_count >= (efr_count*(1-count_percent_error)) and eve_results_count <= (efr_count*(1+count_percent_error))):
                                #same number of results, so worth checking
                                #dropped due to being too restrictive
                                e_disp = get_assn_discipline_from_text(f, asn, event_name, tourney_name, "", False)
                                e_gen = get_assn_gender_from_text(f, asn, event_name, tourney_name, "", False)
                                e_type = get_assn_type_from_text(f, asn, event_name, tourney_name, "", False)
                                e_ages = get_assn_ages_from_text(f, asn, event_name, tourney_name, "", False)
                                if(DEBUG_WRITE):
                                        f.write("                   Event Association Discipline: " + e_disp.discipline_name + " " + str(timezone.now()) + "\n")
                                        f.write("                   Event Association Gender: " + e_gen.gender_name + " " + str(timezone.now()) + "\n")
                                        f.write("                   Event Association Type: " + e_type.type_category + " " + str(timezone.now()) + "\n")
                                        f.write("                   Event Association Ages: " + e_ages.age_category + " " + str(timezone.now()) + "\n")
                                if(1==1):
#                                if((x.ev_assn_discipline == e_disp) and (x.ev_assn_gender == e_gen) and
#                                                        (x.ev_assn_type == e_type) and (x.ev_assn_ages == e_ages)):
                                #may need to drop this if too restrictive
                                        checked_in_detail = checked_in_detail + 1
                                        number_checked = 0
                                        number_same = 0
                                        eve_final_res = event_final_results.objects.filter(efr_event=x
                                                ).values('efr_final_position', 'efr_given_name', 'efr_assn_member_number', 'efr_given_member_identifier'
                                                ).order_by('efr_final_position')[:total_recs_to_check]
                                        eve_final_results = list(eve_final_res)

                                        for c in check_event_results[:total_recs_to_check]:
                                                found_efr = False
                                                if(DEBUG_WRITE):
                                                        f.write("                  Checking Event Results: " 
                                                                + str(c['position']) + " " + str(c['full_name']) + " " 
                                                                + str(c['assn_member_identifier']) + " " 
                                                                + str(c['assn_member_number']) + "\n")
                                                for y in eve_final_results:
                                                        if(not found_efr and (c['position'] == y['efr_final_position'])):
                                                                if(DEBUG_WRITE):
                                                                        f.write("                     Checking existing EFRs: " 
                                                                                + str(y['efr_final_position']) 
                                                                                + " " + str(y['efr_given_name']) 
                                                                                + " " + str(y['efr_assn_member_number']) 
                                                                                + " " + str(y['efr_given_member_identifier']) + "\n")
                                                                if(y['efr_assn_member_number'] is not None):
                                                                        if(c['assn_member_number'] == y['efr_assn_member_number']):
                                                                                number_same = number_same + 1
                                                                                found_efr = True
                                                                if(not found_efr):
                                                                        if(c['assn_member_identifier'] == y['efr_given_member_identifier']):
                                                                                number_same = number_same + 1
                                                                                found_efr = True
                                                number_checked = number_checked + 1
                                        if(number_same > 0):
                                                if((float(number_same) / float(number_checked)) >= 
                                                (float(same_event_min_hit) / float(total_recs_to_check))):
                                                        if(DEBUG_WRITE):
                                                                f.write("                  Found a match: "
                                                                + " tournament name: " + str(x.ev_tourney.tourney_name)
                                                                + " event name: " + str(x.ev_name)
                                                                + " Found Event Association Discipline: " + x.ev_assn_discipline.discipline_name
                                                                + " Found Event Association Gender: " + x.ev_assn_gender.gender_name
                                                                + " Found Event Association Type: " + x.ev_assn_type.type_category
                                                                + " Found Event Association Ages: " + x.ev_assn_ages.age_category
                                                                + " same_event_min_hit: " + str(same_event_min_hit)
                                                                + " total_recs_to_check: " + str(total_recs_to_check)
                                                                + " number_same: " + str(number_same)
                                                                + " number_checked: " + str(number_checked) 
                                                                + "\n")

                                                        found_event = True
                                                        eve = x

        fcnt_end = datetime.now()
        time_inside = fcnt_end - fcnt_start
        if(DEBUG_WRITE):
                f.write("                Event_Exists Total Time (secs): " + str(time_inside.seconds) 
                        + " Event Found: " + str(found_event)
                        + " Event: " + str(eve)
                        + " total events: " + str(max_checked)
                        + " checked in detail: " + str(checked_in_detail) + "\n")
        return(found_event, eve)

def BF_athlete_build_grid_base_data(mem_rec):
        results_detail = []

        def fetch_results(discipline=None):
                filters = {
                        'erps_pool_details__erpd_round__er_event__ev_tourney__tourney_assn': mem_rec.assn,
                        'erps_left_assn_member_number': mem_rec.assn_member_number
                }
                if discipline:
                        filters['erps_pool_details__erpd_round__er_event__ev_assn_discipline'] = discipline

                mem_pool_results = event_round_pool_scores.objects.filter(**filters).order_by('-id') | \
                                event_round_pool_scores.objects.filter(
                                erps_pool_details__erpd_round__er_event__ev_tourney__tourney_assn=mem_rec.assn,
                                erps_left_assn_member_number=mem_rec.assn_member_number,
                                **({'erps_pool_details__erpd_round__er_event__ev_assn_discipline': discipline} if discipline else {})
                                ).order_by('-id')

                filters = {
                        'erpes_round__er_event__ev_tourney__tourney_assn': mem_rec.assn,
                        'erpes_right_assn_member_number': mem_rec.assn_member_number
                }
                if discipline:
                        filters['erpes_round__er_event__ev_assn_discipline'] = discipline

                mem_head_to_head_results = event_round_pool_elimination_scores.objects.filter(**filters).order_by('-id') | \
                                                event_round_pool_elimination_scores.objects.filter(
                                                erpes_round__er_event__ev_tourney__tourney_assn=mem_rec.assn,
                                                erpes_right_assn_member_number=mem_rec.assn_member_number,
                                                **({'erpes_round__er_event__ev_assn_discipline': discipline} if discipline else {})
                                                ).order_by('-id')

                filters = {
                        'efr_event__ev_tourney__tourney_assn': mem_rec.assn,
                        'efr_assn_member_number': mem_rec.assn_member_number
                }
                if discipline:
                        filters['efr_event__ev_assn_discipline'] = discipline

                mem_final_results = event_final_results.objects.filter(**filters).order_by('-efr_event__ev_start_date')

                return mem_pool_results, mem_head_to_head_results, mem_final_results

    # Fetch results for all disciplines
        mem_pool_results, mem_head_to_head_results, mem_final_results = fetch_results()
        if mem_final_results.exists():
                results_detail.append(["All", mem_pool_results, mem_head_to_head_results, mem_final_results])

    # Fetch results for each specific discipline
        for discipline in association_discipline.objects.filter(assn=mem_rec.assn).order_by('discipline_name'):
                if(discipline.discipline_name != "Unknown"):
                        mem_pool_results, mem_head_to_head_results, mem_final_results = fetch_results(discipline)
                        if mem_final_results.exists():
                                results_detail.append([discipline.discipline_name, mem_pool_results, mem_head_to_head_results, mem_final_results])
#        for q in results_detail:
#                print(q[0], len(q[1]), len(q[2]), len(q[3]))

        return results_detail
def BF_athlete_build_ordered_results(mem_rec):
        ordered_detail = []

#        print(mem_rec.assn_member_identifier)
#        print(mem_rec.assn_member_number)

        for y in association_discipline.objects.filter(assn = mem_rec.assn).order_by('discipline_name'):
                if(y.discipline_name != "Unknown"):
        #                print(y.discipline_name)
                        mem_final_results = []
                        mem_final_results = event_final_results.objects.filter(efr_event__ev_tourney__tourney_assn = mem_rec.assn,
                                        efr_assn_member_number = mem_rec.assn_member_number,
                                        efr_event__ev_assn_discipline = y).order_by('efr_event__ev_start_date')
                        if(len(mem_final_results) > 0):
                                discipline_detail = []
                                discipline_detail.append(y.discipline_name)
                                discipline_detail.append(mem_final_results)
                                ordered_detail.append(discipline_detail)
#        for q in ordered_detail:
#                print(q[0], len(q[1]))
#                for r in q[1]:
#                        print(r.efr_event.ev_tourney.tourney_number, r.efr_event.ev_tourney.tourney_name, r.efr_event.ev_name, r.efr_final_position)
        return ordered_detail
def BF_athlete_build_grid(st_year, row_titles):
        win_loss_stats = {}
        year = datetime.today().year
        y = st_year-1
        tot_row_scores = []
        tot_row_title = []
        while(y <= year+1):
                tot_row_scores.append(0)
                y = y + 1

        tot_row_title.append("Prior " + str(st_year))
        y = st_year
        while(y <= year):
                tot_row_title.append(str(y))
                y = y + 1
        tot_row_title.append("Total")
        
        tot_row = []
        tot_row.append(tot_row_title)

        win_loss_stats['Title'] = tot_row_title
        win_loss_stats['Title2'] = tot_row_title
        for c in row_titles:
                win_loss_stats[c] =  tot_row_scores
        return(win_loss_stats)
def BF_athlete_grid_h2h(mem_rec, win_loss_stats, tot_col, st_year, queryh2h):
        for x in queryh2h:
                h2h_year = x.erpes_round.er_event.ev_start_date.year

                grid_year = h2h_year - st_year + 1
                if(grid_year) < 1:
                        grid_year = 0
#                print(x.erpes_winner_member_num,mem_rec.assn_member_identifier)
                if(x.erpes_winner_member_num==mem_rec.assn_member_identifier):
                        lst = win_loss_stats["Victories"].copy()
                        lst[grid_year] = lst[grid_year] + 1
                        lst[tot_col] = lst[tot_col] + 1
                        win_loss_stats["Victories"] = lst
                        lst = win_loss_stats["DE Victories"].copy()
                        lst[grid_year] = lst[grid_year] + 1
                        lst[tot_col] = lst[tot_col] + 1
                        win_loss_stats["DE Victories"] = lst
                else:
                        lst = win_loss_stats["Losses"].copy()
                        lst[grid_year] = lst[grid_year] + 1
                        lst[tot_col] = lst[tot_col] + 1
                        win_loss_stats["Losses"] = lst
                        lst = win_loss_stats["DE Losses"].copy()
                        lst[grid_year] = lst[grid_year] + 1
                        lst[tot_col] = lst[tot_col] + 1
                        win_loss_stats["DE Losses"] = lst
        return win_loss_stats
def BF_athlete_grid_pool(mem_rec, win_loss_stats, tot_col, st_year, querypool):
        for x in querypool:
                h2h_year = x.erps_pool_details.erpd_round.er_event.ev_start_date.year

                grid_year = h2h_year - st_year + 1
                if(grid_year) < 1:
                        grid_year = 0
#                print(x.erps_winner_assn_member_number, mem_rec.assn_member_number)
                if(x.erps_winner_assn_member_number == mem_rec.assn_member_number):
                        lst = win_loss_stats["Victories"].copy()
                        lst[grid_year] = lst[grid_year] + 1
                        lst[tot_col] = lst[tot_col] + 1
                        win_loss_stats["Victories"] = lst
                        lst = win_loss_stats["Pool Victories"].copy()
                        lst[grid_year] = lst[grid_year] + 1
                        lst[tot_col] = lst[tot_col] + 1
                        win_loss_stats["Pool Victories"] = lst
                else:
                        lst = win_loss_stats["Losses"].copy()
                        lst[grid_year] = lst[grid_year] + 1
                        lst[tot_col] = lst[tot_col] + 1
                        win_loss_stats["Losses"] = lst
                        lst = win_loss_stats["Pool Losses"].copy()
                        lst[grid_year] = lst[grid_year] + 1
                        lst[tot_col] = lst[tot_col] + 1
                        win_loss_stats["Pool Losses"] = lst
        return win_loss_stats
def BF_athlete_calc_percentages(win_loss_stats, tot_col):
        wn = win_loss_stats["Victories"].copy()
        ls = win_loss_stats["Losses"].copy()
        wr = win_loss_stats["Win Ratio"].copy()
        x = 0
        while x <= tot_col:
            if(wn[x] + ls[x] > 0):
                wr[x] = wn[x] / (wn[x] + ls[x])
                wr[x] = int((wr[x] * 100))
            x = x + 1
        win_loss_stats["Win Ratio"] = wr

        wn = win_loss_stats["DE Victories"].copy()
        ls = win_loss_stats["DE Losses"].copy()
        wr = win_loss_stats["DE Win Ratio"].copy()
        x = 0
        while x <= tot_col:
            if(wn[x] + ls[x] > 0):
                wr[x] = wn[x] / (wn[x] + ls[x])
                wr[x] = int((wr[x] * 100))
            x = x + 1
        win_loss_stats["DE Win Ratio"] = wr

        wn = win_loss_stats["Pool Victories"].copy()
        ls = win_loss_stats["Pool Losses"].copy()
        wr = win_loss_stats["Pool Win Ratio"].copy()
        x = 0
        while x <= tot_col:
            if(wn[x] + ls[x] > 0):
                wr[x] = wn[x] / (wn[x] + ls[x])
                wr[x] = int((wr[x] * 100))
            x = x + 1
        win_loss_stats["Pool Win Ratio"] = wr
        return win_loss_stats
def BF_athlete_grid_finishes(finish_stats, tot_col, st_year, queryresults):
        for x in queryresults:
                h2h_year = x.efr_event.ev_start_date.year
                grid_year = h2h_year - st_year + 1
                if(grid_year) < 1:
                        grid_year = 0
                if(x.efr_final_position == 1):
                        lst = finish_stats["Gold"].copy()
                        lst[grid_year] = lst[grid_year] + 1
                        lst[tot_col] = lst[tot_col] + 1
                        finish_stats["Gold"] = lst
                if(x.efr_final_position == 2):
                        lst = finish_stats["Silver"].copy()
                        lst[grid_year] = lst[grid_year] + 1
                        lst[tot_col] = lst[tot_col] + 1
                        finish_stats["Silver"] = lst
                if(x.efr_final_position == 3):
                        lst = finish_stats["Bronze"].copy()
                        lst[grid_year] = lst[grid_year] + 1
                        lst[tot_col] = lst[tot_col] + 1
                        finish_stats["Bronze"] = lst
                if(x.efr_final_position >= 4) and (x.efr_final_position <= 8):
                        lst = finish_stats["Top 8"].copy()
                        lst[grid_year] = lst[grid_year] + 1
                        lst[tot_col] = lst[tot_col] + 1
                        finish_stats["Top 8"] = lst
                if(x.efr_final_position >= 9) and (x.efr_final_position <= 16):
                        lst = finish_stats["Top 16"].copy()
                        lst[grid_year] = lst[grid_year] + 1
                        lst[tot_col] = lst[tot_col] + 1
                        finish_stats["Top 16"] = lst
                if(x.efr_final_position >= 17) and (x.efr_final_position <= 32):
                        lst = finish_stats["Top 32"].copy()
                        lst[grid_year] = lst[grid_year] + 1
                        lst[tot_col] = lst[tot_col] + 1
                        finish_stats["Top 32"] = lst
                if(x.efr_final_position >= 33) and (x.efr_final_position <= 64):
                        lst = finish_stats["Top 64"].copy()
                        lst[grid_year] = lst[grid_year] + 1
                        lst[tot_col] = lst[tot_col] + 1
                        finish_stats["Top 64"] = lst

                lst = finish_stats["Total"].copy()
                lst[grid_year] = lst[grid_year] + 1
                lst[tot_col] = lst[tot_col] + 1
                finish_stats["Total"] = lst
        return finish_stats
def BF_athlete_grid_scoring_h2h(mem_rec, scoring_stats, tot_col, st_year, easy_de, close_de, queryh2h):
        for x in queryh2h:
                h2h_year = x.erpes_round.er_event.ev_start_date.year
                grid_year = h2h_year - st_year + 1
                if(x.erpes_score is not None):
                        minus = x.erpes_score.find('-')
                        if(minus > 0):
                                sc_diff = abs(int(x.erpes_score[:minus-1].strip()) - int(x.erpes_score[minus+1:].strip()))
                        else:
                                sc_diff = 16
                else:
                        sc_diff = 16
                if(grid_year) < 1:
                        grid_year = 0
                if(x.erpes_winner_member_num==mem_rec.assn_member_identifier):
                        lst = scoring_stats["Total wins"].copy()
                        lst[grid_year] = lst[grid_year] + 1
                        lst[tot_col] = lst[tot_col] + 1
                        scoring_stats["Total wins"] = lst
                        if(sc_diff >= easy_de):
                                lst = scoring_stats["Easy wins"].copy()
                                lst[grid_year] = lst[grid_year] + 1
                                lst[tot_col] = lst[tot_col] + 1
                                scoring_stats["Easy wins"] = lst
                        else:
                                if(sc_diff <= close_de):
                                        lst = scoring_stats["Close wins"].copy()
                                        lst[grid_year] = lst[grid_year] + 1
                                        lst[tot_col] = lst[tot_col] + 1
                                        scoring_stats["Close wins"] = lst
                else:
                        lst = scoring_stats["Total losses"].copy()
                        lst[grid_year] = lst[grid_year] + 1
                        lst[tot_col] = lst[tot_col] + 1
                        scoring_stats["Total losses"] = lst
                        if(sc_diff >= easy_de):
                                lst = scoring_stats["Big losses"].copy()
                                lst[grid_year] = lst[grid_year] + 1
                                lst[tot_col] = lst[tot_col] + 1
                                scoring_stats["Big losses"] = lst
                        else:
                                if(sc_diff <= close_de):
                                        lst = scoring_stats["Close losses"].copy()
                                        lst[grid_year] = lst[grid_year] + 1
                                        lst[tot_col] = lst[tot_col] + 1
                                        scoring_stats["Close losses"] = lst
        return scoring_stats
def BF_athlete_calc_scoring_percentages(scoring_stats, tot_col):
        tw = scoring_stats["Total wins"].copy()
        ew = scoring_stats["Easy wins"].copy()
        ewp = scoring_stats["Easy wins as percent of all wins"].copy()
        x = 0
        while x <= tot_col:
                if(tw[x] > 0):
                        ewp[x] = int((ew[x] / tw[x])*100)
                x = x + 1
        scoring_stats["Easy wins as percent of all wins"] = ewp
        ew = scoring_stats["Close wins"].copy()
        ewp = scoring_stats["Close wins as percent of all wins"].copy()
        x = 0
        while x <= tot_col:
                if(tw[x] > 0):
                        ewp[x] = int((ew[x] / tw[x])*100)
                x = x + 1
        scoring_stats["Close wins as percent of all wins"] = ewp
        tl = scoring_stats["Total losses"].copy()
        cl = scoring_stats["Close losses"].copy()
        clp = scoring_stats["Close losses as percent of all losses"].copy()
        x = 0
        while x <= tot_col:
                if(tl[x] > 0):
                        clp[x] = int((cl[x] / tl[x])*100)
                x = x + 1
        scoring_stats["Close losses as percent of all losses"] = clp
        cl = scoring_stats["Big losses"].copy()
        clp = scoring_stats["Big losses as percent of all losses"].copy()
        x = 0
        while x <= tot_col:
                if(tl[x] > 0):
                        clp[x] = int((cl[x] / tl[x])*100)
                x = x + 1
        scoring_stats["Big losses as percent of all losses"] = clp
        return scoring_stats
def BF_athlete_grid_scoring_pool(mem_rec, scoring_stats, tot_col, st_year, easy_pool, close_pool, querypool):
        for x in querypool:
                h2h_year = x.erps_pool_details.erpd_round.er_event.ev_start_date.year
                grid_year = h2h_year - st_year + 1
                if(grid_year) < 1:
                        grid_year = 0
                if(x.erps_left_score is not None):
                        lc = int(x.erps_left_score)
                else:
                        lc = 0
                if(x.erps_right_score is not None):
                        rc = int(x.erps_right_score)
                else:
                        rc = 0
                sc_diff = abs(lc - rc)
                if(x.erps_winner_assn_member_number == mem_rec.assn_member_number):
                        lst = scoring_stats["Total wins"].copy()
                        lst[grid_year] = lst[grid_year] + 1
                        lst[tot_col] = lst[tot_col] + 1
                        scoring_stats["Total wins"] = lst
                        if(sc_diff >= easy_pool):
                                lst = scoring_stats["Easy wins"].copy()
                                lst[grid_year] = lst[grid_year] + 1
                                lst[tot_col] = lst[tot_col] + 1
                                scoring_stats["Easy wins"] = lst
                        else:
                                if(sc_diff <= close_pool):
                                        lst = scoring_stats["Close wins"].copy()
                                        lst[grid_year] = lst[grid_year] + 1
                                        lst[tot_col] = lst[tot_col] + 1
                                        scoring_stats["Close wins"] = lst
                else:
                        lst = scoring_stats["Total losses"].copy()
                        lst[grid_year] = lst[grid_year] + 1
                        lst[tot_col] = lst[tot_col] + 1
                        scoring_stats["Total losses"] = lst
                        if(sc_diff >= easy_pool):
                                lst = scoring_stats["Big losses"].copy()
                                lst[grid_year] = lst[grid_year] + 1
                                lst[tot_col] = lst[tot_col] + 1
                                scoring_stats["Big losses"] = lst
                        else:
                                if(sc_diff <= close_pool):
                                        lst = scoring_stats["Close losses"].copy()
                                        lst[grid_year] = lst[grid_year] + 1
                                        lst[tot_col] = lst[tot_col] + 1
                                        scoring_stats["Close losses"] = lst
        return scoring_stats
def BF_athlete_add_nif_avg(win_loss_stats, st_year, queryresults):
        nifs = {}
        nif_totals = [0,0]
        nifs[st_year-1] =  nif_totals
        for x in queryresults:
                h2h_year = x.efr_event.ev_start_date.year
                if(h2h_year >= st_year):
                        nifs[h2h_year] =  nif_totals
        tot_year = datetime.today().year + 1
        nifs[tot_year] =  nif_totals

        for x in queryresults:
                h2h_year = x.efr_event.ev_start_date.year
                nif_value = get_event_extra_field_value(None, x.efr_event, 'NIF', False)
                if(nif_value is None):
                        nif_value = 0
#                print(nif_value, nif_value_str)
                if(h2h_year < st_year):
                        h2h_year = st_year - 1
                if(nif_value > 0):
                        lst = nifs[h2h_year].copy()

                        lst[0] = lst[0] + nif_value
                        lst[1] = lst[1] + 1
                        nifs[h2h_year] = lst

        #total all years into current_year+1
        for key,value in nifs.items():
                if(key < tot_year):
                        lst = nifs[tot_year].copy()
                        lst[0] = lst[0] + value[0]
                        lst[1] = lst[1] + value[1]
                        nifs[tot_year] = lst

        tot_val = nifs.get(tot_year)
        if(tot_val[1] == 0):    #need to delete Title2s
                win_loss_stats.pop("Title2")
        else:
                for key,value in nifs.items():
                        grid_year = key - st_year + 1
                        if(grid_year) < 1:
                                grid_year = 0
                        lst = win_loss_stats['Title2'].copy()
                        if(value[1] > 0):
                                lst[grid_year] = "Avg NIF: " + str(int(value[0]/value[1]))
                        else:
                                lst[grid_year] = "Avg NIF: 0"
                        win_loss_stats['Title2'] = lst
        return win_loss_stats
def BF_athlete_build_all_grids(mem_rec, st_year, easy_pool, easy_de, close_pool, close_de, results_detail, ordered_results):
        athlete_performance = []
        year_performance = []
        for xx in results_detail:
                win_loss_stats = {}
                finish_stats = {}
                pool_scoring_stats = {}
                de_scoring_stats = {}

                rw = ["Victories", "Losses", "Win Ratio", "Pool Victories", "Pool Losses", 
                        "Pool Win Ratio", "DE Victories", "DE Losses", "DE Win Ratio"]
                win_loss_stats = BF_athlete_build_grid(st_year, rw)
#                print(xx[0], win_loss_stats)
                tot_col = len(win_loss_stats['Victories'])-1
#                print("xx[0]", xx[0])
#                print("xx[1]", xx[1])
#                print("xx[2]", xx[2])
#                print("xx[3]", xx[3])
                win_loss_stats = BF_athlete_grid_h2h(mem_rec, win_loss_stats, tot_col, st_year, xx[2])
                win_loss_stats = BF_athlete_grid_pool(mem_rec, win_loss_stats, tot_col, st_year, xx[1])
                win_loss_stats = BF_athlete_calc_percentages(win_loss_stats, tot_col)
#                print(xx[0], win_loss_stats)
                for qq in ordered_results:
                        if qq[0] == xx[0]:
                                win_loss_stats = BF_athlete_add_nif_avg(win_loss_stats, st_year, qq[1])
#                                print(xx[0], win_loss_stats)
#                print(xx[0], win_loss_stats, "\n")

                rw = ["Gold", "Silver", "Bronze", "Top 8", "Top 16", "Top 32", "Top 64", "Total"]
                finish_stats = BF_athlete_build_grid(st_year, rw)
#                print(xx[0], finish_stats)
                finish_stats = BF_athlete_grid_finishes(finish_stats, tot_col, st_year, xx[3])
                if(xx[0] == 'All'):
                        for key, value in finish_stats.items():
                                yp=[]
                                ln = len(value)
                                yp.append(key)
                                yp.append(value[ln-2])
                                year_performance.append(yp)
#                print(xx[0], finish_stats, "\n")

                rw = ["Total wins", "Easy wins", "Easy wins as percent of all wins", 
                        "Close wins", "Close wins as percent of all wins", 
                        "Total losses", "Close losses", "Close losses as percent of all losses", 
                        "Big losses", "Big losses as percent of all losses"]
                de_scoring_stats = BF_athlete_build_grid(st_year, rw)
                de_scoring_stats = BF_athlete_grid_scoring_h2h(mem_rec, de_scoring_stats, tot_col, st_year, easy_de, close_de, xx[2])
                de_scoring_stats = BF_athlete_calc_scoring_percentages(de_scoring_stats, tot_col)
#                print(xx[0], de_scoring_stats)

                rw = ["Total wins", "Easy wins", "Easy wins as percent of all wins", 
                        "Close wins", "Close wins as percent of all wins", 
                        "Total losses", "Close losses", "Close losses as percent of all losses", 
                        "Big losses", "Big losses as percent of all losses"]
                pool_scoring_stats = BF_athlete_build_grid(st_year, rw)
                pool_scoring_stats = BF_athlete_grid_scoring_pool(mem_rec, pool_scoring_stats, tot_col, st_year, easy_pool, close_pool, xx[1])
                pool_scoring_stats = BF_athlete_calc_scoring_percentages(pool_scoring_stats, tot_col)
#                print(xx[0], pool_scoring_stats)

                ap_record = []
                ap_record.append(xx[0])
                ap_record.append(win_loss_stats)
                ap_record.append(finish_stats)
                ap_record.append(de_scoring_stats)
                ap_record.append(pool_scoring_stats)
                athlete_performance.append(ap_record)
        return(athlete_performance, year_performance)
def BF_athlete_linreg(X, Y):
        """
        return a,b in solution to y = ax + b such that root mean square distance between trend line and original points is minimized
        """
        N = len(X)
        Sx = Sy = Sxx = Syy = Sxy = 0.0
        for x, y in zip(X, Y):
            Sx = Sx + x
            Sy = Sy + y
            Sxx = Sxx + x*x
            Syy = Syy + y*y
            Sxy = Sxy + x*y
        det = Sxx * N - Sx * Sx
        return (Sxy * N - Sy * Sx)/det, (Sxx * Sy - Sx * Sxy)/det
def BF_athlete_build_plot(o_results):
        labels = []
        data1 = []
        data2 = []
        data2_label = ""
        data1_label = ""

        data1_label = 'Performance'
        q = 1
        for x in o_results:
                nif_value = get_event_extra_field_value(None, x.efr_event, 'NIF', False)
                if(nif_value is None):
                        nif_value = 0
                if(nif_value > 0):
                        graph_val = int(100 * (1 - (x.efr_final_position  /  nif_value)))
#                        print(graph_val, x.efr_final_position, nif_value, x.efr_event.ev_tourney.tourney_number, x.efr_event.ev_tourney.tourney_name, x.efr_event.ev_name)      
                        if(graph_val > 0):
                                labels.append(q)
                                data1.append(graph_val)
                                q = q + 1
        if(q>3):
                data2_label = 'Trend'
                a,b = BF_athlete_linreg(range(len(data1)),data1)  #your x,y are switched from standard notation
                data2=[a*index + b for index in range(len(data1))]
        return labels, data1, data2, data1_label, data2_label
def BF_athlete_get_current_ratings_and_rankings(mem_rec):
        current_ratings = []
        current_rankings = []
        cur_rating_rowa = []
        cur_ranking_rowa = []

        genders = None
        if(mem_rec.assn_member_gender.lower() == None):
                gen = None
        elif(mem_rec.assn_member_gender.lower() == 'f'):
                gen = association_genders.objects.get(assn = mem_rec.assn, gender_name = 'Women')
        else:
                gen = association_genders.objects.get(assn = mem_rec.assn, gender_name = 'Men')
        rps = bf_member_rank_points.objects.filter(bfmr_gender = gen).values('bfmr_ages__age_category').distinct('bfmr_ages__age_category')
        disciplines = association_discipline.objects.filter(assn=mem_rec.assn).order_by('discipline_name')

        c_ratings = BF_get_all_assn_member_extra_current_ratings(None, mem_rec, False)
        for x in c_ratings:
                cur_rating_rowd = [mem_rec.assn.assn_name, x[0], x[1]+x[2]]
                cur_rating_rowa.append(cur_rating_rowd)

        for y in disciplines:
                for rp in rps:
#                        print(timezone.now())
                        ranking = BF_get_rank(None, mem_rec, y.discipline_name, gen.gender_name, rp['bfmr_ages__age_category'], False)
#                        print(timezone.now())
                        if ranking is not None and ranking != 999:
                                cur_ranking_rowd = [
                                        mem_rec.assn.assn_name,
                                        y.discipline_name,
                                        rp['bfmr_ages__age_category'],
                                        ranking
                                ]
                                cur_ranking_rowa.append(cur_ranking_rowd)

        if cur_ranking_rowa:
#                print(cur_ranking_rowa)
                current_rankings.append([mem_rec.assn_member_identifier, cur_ranking_rowa])
        if cur_rating_rowa:
#                print(cur_rating_rowa)
                current_ratings.append([mem_rec.assn_member_identifier, cur_rating_rowa])

        return current_ratings, current_rankings
def BF_athlete_get_upcoming_events(mem_rec, max_records):
#        print("assnn_member_bumber", mem_rec.assn_member_number)
#        print("assn_member_identifier", mem_rec.assn_member_identifier)
        upcoming_events = []
        u_events = event_registered_athletes.objects.filter(era_assn_member_number = mem_rec.assn_member_number,
                        era_event__ev_start_date__gte = timezone.now()
                        ).order_by('-era_event__ev_start_date')[:max_records]
        for qq in u_events:
            up_events_row = []
            up_events_row.append(qq.era_event.ev_tourney.tourney_number)
            up_events_row.append(qq.era_event.ev_tourney.tourney_name)
            up_events_row.append(qq.era_event.ev_start_date)
            up_events_row.append(qq.era_event.ev_name)
            event_diff = get_event_extra_field_value(None, qq.era_event, 'Difficulty', False)
            up_events_row.append(event_diff)
            upcoming_events.append(up_events_row)
        return upcoming_events

def zzzBF_athlete_get_potential_events(part_disc, max_records):
        potential_events = []
        pot_ev_cnt = 0
        t_inbound = ['upcomingS80', 'upcomingLPJS', 'upcomingDurham']
        for aa in part_disc:
            for bb in events.objects.filter(ev_assn_discipline = aa[0], ev_assn_gender = aa[1],
                                        ev_tourney__tourney_inbound__in=t_inbound, 
                                        ev_start_date__gte = timezone.now()).order_by('ev_start_date'):
                if(bb.ev_start_date > timezone.now() and pot_ev_cnt < max_records):
                    potential_events_row = []
                    potential_events_row.append(bb.ev_tourney.tourney_number)
                    potential_events_row.append(bb.ev_tourney.tourney_name)
                    potential_events_row.append(bb.ev_start_date)
                    potential_events_row.append(bb.ev_name)
                    potential_events_row.append(bb.ev_assn_ages.age_category)
                    potential_events.append(potential_events_row)
                    pot_ev_cnt += 1
        return potential_events
def BF_athlete_get_potential_events_using_last_events(last_events, max_records):

        potential_events = []
        disp_age_gender = []
        unique_combinations = set()

#        print("last events", len(last_events))
        for x in last_events:
                t_number = x[0]
                t = get_tournament(None, False, t_number, None, None, None, None, None)
                gen = association_genders.objects.get(assn = t.tourney_assn, gender_name__iexact = "mixed")
                
                combination = (x[9], x[10], x[11])
                if combination not in unique_combinations:
                        unique_combinations.add(combination)
                        disp_age_gender.append(combination)
                combination = (x[9], x[10], gen)
                if combination not in unique_combinations:
                        unique_combinations.add(combination)
                        disp_age_gender.append(combination)
#        for x in last_events:
#                print(x[9], x[10], x[11])
#        for x in disp_age_gender:
#                print(x)

        t_inbound = ['upcomingS80', 'upcomingLPJS', 'upcomingDurham']
        for aa in disp_age_gender:
            pot_events = events.objects.filter(ev_assn_discipline = aa[0], ev_assn_ages = aa[1],
                                            ev_assn_gender = aa[2], 
                                            ev_tourney__tourney_inbound__in=t_inbound,
                                            ev_start_date__gte = timezone.now()).order_by('ev_start_date')
            for bb in pot_events:
                potential_events_row = []
                potential_events_row.append(bb.ev_tourney.tourney_number)
                potential_events_row.append(bb.ev_tourney.tourney_name)
                potential_events_row.append(bb.ev_start_date)
                potential_events_row.append(bb.ev_name)
                potential_events_row.append(bb.ev_assn_ages.age_category)
                event_diff = get_event_extra_field_value(None, bb, 'Difficulty', False)
                potential_events_row.append(event_diff)
                potential_events.append(potential_events_row)

        potential_events = sorted(potential_events, key=lambda event: event[2])
#        print("potential_events", len(potential_events))

        return potential_events[:max_records]
def BF_athlete_get_last_events(mem_rec, max_records):
        last_events = []
        participating_disciplines = []
        if(mem_rec.assn_member_number is not None):
                l_events = event_final_results.objects.filter(efr_assn_member_number = mem_rec.assn_member_number,
                        efr_event__ev_start_date__lte = timezone.now()
                        ).order_by('-efr_event__ev_start_date')[:max_records]
        else:
                l_events = None
        for qq in l_events:
                event_NIF = get_event_extra_field_value(None, qq.efr_event, 'NIF', False)
                event_athletes = get_event_extra_field_value(None, qq.efr_event, 'Fencers', False)
                prev_rating = get_efr_extra_field_value(None, qq, 'efr_previous_rating', False)
#                print(qq.efr_event.ev_name, "prev_rating", prev_rating)
                rating = get_efr_extra_field_value(None, qq, 'efr_rating', False)
                rating_date = get_efr_extra_field_value(None, qq, 'efr_award_date', False)
#                event_athletes = event_final_results.objects.filter(efr_event = qq.efr_event).count()
                if (qq.efr_event.ev_assn_discipline, qq.efr_event.ev_assn_gender) not in participating_disciplines:
                        participating_disciplines.append((qq.efr_event.ev_assn_discipline, qq.efr_event.ev_assn_gender))
                last_events_row = []
                last_events_row.append(qq.efr_event.ev_tourney.tourney_number)
                last_events_row.append(qq.efr_event.ev_tourney.tourney_name)
                last_events_row.append(qq.efr_event.ev_name)
                last_events_row.append(qq.efr_final_position)
                last_events_row.append(event_NIF)
                last_events_row.append(event_athletes)
                last_events_row.append(prev_rating)
                last_events_row.append(rating)
                last_events_row.append(rating_date)
                last_events_row.append(qq.efr_event.ev_assn_discipline)
                last_events_row.append(qq.efr_event.ev_assn_ages)
                last_events_row.append(qq.efr_event.ev_assn_gender)
                last_events_row.append(qq.efr_event.ev_number)
                last_events.append(last_events_row)
        return last_events, participating_disciplines
def get_assn_member_extra_field(f, asn_member, ex_field_name, ex_field_value5, ex_field_value4, ex_field_value3, ex_field_value2, ex_field_value1, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      get_assn_extra_field: " + str(ex_field_name) + " " + str(ex_field_value5) + " " + str(ex_field_value4) + " " + str(ex_field_value3) + " " + str(asn_member) + " " + str(timezone.now()) + "\n")

#        print(asn_member, ex_field_name, ex_field_value5, ex_field_value4, ex_field_value3, ex_field_value2, ex_field_value1)
        if(ex_field_name == "Current Rating"):
                #needs 5
                try:
                        amef = association_member_extra_fields.objects.get(
                                assn_member=asn_member, 
                                assn_member_field_name__iexact=ex_field_name.lower(),
                                assn_member_field5_value__iexact=ex_field_value5.lower())
                except association_member_extra_fields.DoesNotExist:
                        amef = None        
        if(ex_field_name == "Rating History"):
                #needs 5 and 4
                try:
                        amef = association_member_extra_fields.objects.get(
                                assn_member=asn_member, 
                                assn_member_field_name__iexact=ex_field_name.lower(),
                                assn_member_field5_value__iexact=ex_field_value5.lower(),
                                assn_member_field4_value__iexact=ex_field_value4.lower())
                except association_member_extra_fields.DoesNotExist:
                        amef = None        
        if(ex_field_name == "BF Ranking"):
                #needs 5
                try:
                        amef = association_member_extra_fields.objects.get(
                                assn_member=asn_member, 
                                assn_member_field_name__iexact=ex_field_name.lower(),
                                assn_member_field5_value__iexact=ex_field_value5.lower(),
                                assn_member_field2_value__iexact = ex_field_value2.lower(),
                                assn_member_field1_value__iexact = ex_field_value1.lower())
                except association_member_extra_fields.DoesNotExist:
                        amef = None        
        if(DEBUG_WRITE):
                f.write(" COMPLETE: get_assn_extra_field: " + str(amef) + " " + str(timezone.now()) + "\n")
        return (amef)


def BF_get_all_assn_member_extra_rating_history(f, asn_member, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("      BF_get_all_assn_member_extra_rating_history: " + str(asn_member) + " " + str(timezone.now()) + "\n")
    
    ex_field_name = "Rating History"
    ratings_history = []
    
    uc_ef = association_member_extra_fields.objects.filter(
        assn_member=asn_member,
        assn_member_field_name=ex_field_name,
    ).select_related('assn_member')

    for x in uc_ef:
        award_date = Make_Timezone_String_Timezone_Aware(x.assn_member_field1_value)
        award_end_date = Make_Timezone_String_Timezone_Aware(x.assn_member_field2_value)
        if(x.assn_member_field5_value.lower() != 'unknown'):
                ratings_history.append([
                        x.assn_member_field4_value,             #event number  - ev_number
                        x.assn_member_field5_value,             #discipline name
                        x.assn_member_field3_value,             #rating
                        award_date,                             #award_date
                        award_end_date,                         #award_end_date
                        str(award_end_date.year)[2:4] if award_end_date else "" #award_end_date as 2 digit year
                ])
    if DEBUG_WRITE:
        f.write(" COMPLETE: BF_get_all_assn_member_extra_rating_history: " + str(len(ratings_history)) + " " + str(timezone.now()) + "\n")
    return ratings_history

def zzzBF_get_all_assn_member_extra_current_ratings(f, asn_member, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("      BF_get_all_assn_member_extra_current_ratings: " + str(asn_member) + " " + str(timezone.now()) + "\n")
    
    ex_field_name = "Current Rating"
    current_ratings = []
    
    uc_ef = association_member_extra_fields.objects.filter(
        assn_member=asn_member,
        assn_member_field_name=ex_field_name,
    ).select_related('assn_member')

    for x in uc_ef:
        award_date = Make_Timezone_String_Timezone_Aware(x.assn_member_field1_value)
        if(x.assn_member_field5_value.lower() != 'unknown'):
                current_ratings.append([
                        x.assn_member_field5_value,
                        x.assn_member_field3_value,
                        str(award_date.year)[2:4] if award_date else ""
                ])
    if DEBUG_WRITE:
        f.write(" COMPLETE: BF_get_all_assn_member_extra_current_ratings: " + str(len(current_ratings)) + " " + str(timezone.now()) + "\n")
    return current_ratings

def BF_get_all_assn_member_extra_current_ratings(f, asn_member, DEBUG_WRITE):
        if DEBUG_WRITE:
                f.write("      BF_get_all_assn_member_extra_current_ratings: " + str(asn_member) + " " + str(timezone.now()) + "\n")
    
        ex_field_name = "Current Rating"
        current_ratings = []

        uc_ef = association_member_extra_fields.objects.filter(
                assn_member=asn_member,
                assn_member_field_name=ex_field_name,
                ).select_related('assn_member')

        if(len(uc_ef) > 0):
                for x in uc_ef:
                        award_date = Make_Timezone_String_Timezone_Aware(x.assn_member_field1_value)
                        if(x.assn_member_field5_value.lower() != 'unknown'):
                                current_ratings.append([
                                        x.assn_member_field5_value,
                                        x.assn_member_field3_value,
                                        str(award_date.year)[2:4] if award_date else ""
                                ])
        else:
                for y in association_discipline.objects.filter(assn = asn_member.assn):
                        if(y.discipline_name.lower() != 'unknown'):
                                no_date = timezone.now()
                                current_ratings.append([
                                                y.discipline_name, 'U',
                                                str(timezone.now().year)[2:4]
                                        ])

        if DEBUG_WRITE:
                f.write(" COMPLETE: BF_get_all_assn_member_extra_current_ratings: " + str(len(current_ratings)) + " " + str(timezone.now()) + "\n")
        return current_ratings
def zzzBF_get_current_rating_with_two_digit_year(f, asn_member, discipline_name, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("      BF_get_current_rating_with_two_digit_year: " + str(asn_member) + " " + str(timezone.now()) + "\n")
    
    ex_field_name = "Current Rating"
    rating = "U"
    aw_date = ""
    current_ratings = []
    
    uc_ef = association_member_extra_fields.objects.filter(
        assn_member=asn_member,
        assn_member_field_name=ex_field_name,
        assn_member_field5_value__iexact=discipline_name.lower()
    ).select_related('assn_member')

    uc_ef_cnt = uc_ef.count()
#    for x in uc_ef:
#            print(x.assn_member_field1_value, x.assn_member_field2_value, x.assn_member_field3_value)
    if uc_ef_cnt == 1:
        for x in uc_ef:
                award_date = Make_Timezone_String_Timezone_Aware(x.assn_member_field2_value)
                rating = uc_ef[0].assn_member_field3_value
                aw_date = str(award_date.year)[2:4] if award_date else ""
                current_ratings.append([
                        x.assn_member_field5_value,
                        x.assn_member_field3_value,
                        str(award_date.year)[2:4] if award_date else ""
                ])

        rating = uc_ef[0].assn_member_field3_value
        award_date = Make_Timezone_String_Timezone_Aware(uc_ef[0].assn_member_field2_value)
        aw_date = str(award_date.year)[2:4] if award_date else ""
    elif uc_ef_cnt > 1:
            f.write("ERROR - BF_get_current_rating_with_two_digit_year RETURNED x RECORDS: " + str(uc_ef_cnt) + "\n")
    if DEBUG_WRITE:
        f.write(" COMPLETE: BF_get_current_rating_with_two_digit_year: " + str(rating) + " " + " " + str(timezone.now()) + "\n")
    return rating, aw_date, current_ratings
def BF_update_or_create_current_rating(f, asn_member, discipline_name, new_rating, rating_date, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      BF_update_or_create_current_rating: " + str(asn_member) 
                        + " " + str(asn_member.assn_member_identifier)
                        + " " + str(discipline_name)
                        + " " + str(new_rating)
                        + " " + str(rating_date)
                        + " " + str(timezone.now()) + "\n")
        ex_field_name = "Current Rating"
        ex_field_seq = 100

        if os.environ.get("BF_RATING_TIME_LENGTH_YEARS") is not None:
                rt_years = int(os.environ.get("BF_RATING_TIME_LENGTH_YEARS"))
        else:
                rt_years = 0
        st_date = rating_date
        en_date = rating_date + relativedelta(years=rt_years)
        c_rate = new_rating

        if(asn_member is not None):
                uc_ef, created = association_member_extra_fields.objects.update_or_create(
                        assn_member=asn_member,
                        assn_member_field_name = ex_field_name,
                        assn_member_field5_value = discipline_name,
                        defaults={
                                'assn_member_field_date_updated': timezone.now(),
                                'assn_member_field_sequence': ex_field_seq,
                                'assn_member_field_active': True,
                                'assn_member_field_group': ex_field_name,
                                'assn_member_field_name': ex_field_name,
                                'assn_member_field1_type': "timezone",
                                'assn_member_field1_value': str(st_date),
                                'assn_member_field2_type': "timezone",
                                'assn_member_field2_value': str(en_date),
                                'assn_member_field3_type': "string",
                                'assn_member_field3_value': c_rate,
                                'assn_member_field4_type': "",
                                'assn_member_field4_value': "",
                                'assn_member_field5_type': "string"
#                                'assn_member_field5_value': ""
                                })
        if(DEBUG_WRITE):
                f.write(" COMPLETE: BF_update_or_create_current_rating: " + str(uc_ef) + " " + str(created) + " " + str(timezone.now()) + "\n")
        return (uc_ef)
def BF_update_or_create_rating_history(f, asn_member, event, discipline_name, new_rating, rating_date, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      BF_update_or_create_rating_history: " + str(asn_member.assn_member_identifier) + " " + str(timezone.now()) + "\n")
        ex_field_name = "Rating History"
        ex_field_seq = 110

        if os.environ.get("BF_RATING_TIME_LENGTH_YEARS") is not None:
                rt_years = int(os.environ.get("BF_RATING_TIME_LENGTH_YEARS"))
        else:
                rt_years = 0
        st_date = rating_date
        en_date = rating_date + relativedelta(years=rt_years)
        c_rate = new_rating

        if(asn_member is not None):
                uc_ef, created = association_member_extra_fields.objects.update_or_create(
                assn_member=asn_member,
                assn_member_field_name=ex_field_name,
                assn_member_field5_value = discipline_name,
                assn_member_field4_value = event.ev_number,
                assn_member_field3_value = c_rate,
                assn_member_field2_value = str(en_date),
                assn_member_field1_value = str(st_date),
                defaults={
                        'assn_member_field_date_updated': timezone.now(),
                        'assn_member_field_sequence': ex_field_seq,
                        'assn_member_field_active': True,
                        'assn_member_field_group': ex_field_name,
                        'assn_member_field1_type': "timezone",
                        'assn_member_field2_type': "timezone",
                        'assn_member_field3_type': "string",
                        'assn_member_field4_type': "ev_number",
                        'assn_member_field5_type': "string"})

        if(DEBUG_WRITE):
                f.write(" COMPLETE: BF_update_or_create_rating_history: " + str(uc_ef) + " created: " + str(created) + " " + str(timezone.now()) + "\n")
                f.write("    " + str(uc_ef.assn_member_field_name) + " " + str(uc_ef.assn_member_field5_value) + "\n")
                f.write("    " + str(uc_ef.assn_member_field5_value) + " " + str(uc_ef.assn_member_field4_value) + "\n")
                f.write("    " + str(uc_ef.assn_member_field3_value) + " " + str(uc_ef.assn_member_field2_value) + "\n")
                f.write("    " + str(uc_ef.assn_member_field1_value) + " " + str(uc_ef.assn_member.assn_member_identifier) + "\n")
        return (uc_ef)
def BF_update_or_create_bf_ranking(f, asn_member, discipline_name, gender_name, age_name, ranking, ranking_date, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      BF_update_or_create_bf_ranking: " + str(asn_member) + " " + str(timezone.now()) + "\n")
        ex_field_name = "BF Ranking"
        ex_field_seq = 130
        uc_ef = None

        if(asn_member is not None):
                uc_ef, created = association_member_extra_fields.objects.update_or_create(
                        assn_member=asn_member,
                        assn_member_field_name = ex_field_name,
                        assn_member_field5_value = discipline_name,
                        assn_member_field4_value = str(ranking),
                        assn_member_field3_value = str(ranking_date),
                        assn_member_field2_value = gender_name,
                        assn_member_field1_value = age_name,
                        defaults={
                                'assn_member_field_date_updated': timezone.now(),
                                'assn_member_field_sequence': ex_field_seq,
                                'assn_member_field_active': True,
                                'assn_member_field_group': ex_field_name,
                                'assn_member_field1_type': "string",
                                'assn_member_field2_type': "string",
                                'assn_member_field3_type': "timezone",
                                'assn_member_field4_type': "integer",
                                'assn_member_field5_type': "string"
                                })
        if(DEBUG_WRITE):
                f.write(" COMPLETE: BF_update_or_create_bf_ranking: " + str(uc_ef) + " " + str(created) + " " + str(timezone.now()) + "\n")
        return (uc_ef)
def BF_delete_bf_ranking(f, discipline_name, gender_name, age_name, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      BF_delete_bf_ranking: " + str(timezone.now()) + "\n")
        ex_field_seq = 130

        association_member_extra_fields.objects.filter(assn_member_field_sequence = ex_field_seq,
                        assn_member_field5_value = discipline_name,
                        assn_member_field2_value = gender_name,
                        assn_member_field1_value = age_name).delete()
        if(DEBUG_WRITE):
                f.write(" COMPLETE: BF_delete_bf_ranking: " + str(timezone.now()) + "\n")
def BF_get_rank(f, asn_member, discipline_name, gender_name, age_name, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      BF_get_rank: " + str(asn_member) + " " + str(timezone.now()) + "\n")
        ex_field_name = "BF Ranking"
        ex_field_seq = 130
        
        uc_ef = association_member_extra_fields.objects.filter(
                assn_member=asn_member,
                assn_member_field_sequence=ex_field_seq,
                        assn_member_field5_value = discipline_name,
                        assn_member_field2_value = gender_name,
                        assn_member_field1_value = age_name)
 
        if(uc_ef.count() == 1):
                ranking = uc_ef[0].assn_member_field4_value
        else:
                ranking = 999

        if(DEBUG_WRITE):
                f.write(" COMPLETE: BF_get_rank: " + str(ranking) + " " + str(timezone.now()) + "\n")
        return (ranking)

def BF_get_rating_at_specific_date_from_assn_member_extra_field(f, asn_member, discipline_name, rating_date, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      BF_get_rating_at_specific_date_from_assn_member_extra_field: " + str(asn_member) + " " + str(timezone.now()) + "\n")
        ex_field_name = "Rating History"
        rating = "U"
        rating_list = []
        ev_num = None
        event = None
        award_year = ""
        award_year_end = ""

        if(DEBUG_WRITE):
                f.write("      in: " + str(asn_member) + " "+ str(discipline_name) + " "+ str(rating_date) + " " + str(timezone.now()) + "\n")

        uc_ef = association_member_extra_fields.objects.filter(
                assn_member=asn_member,
                assn_member_field_name=ex_field_name,
                assn_member_field5_value__iexact=discipline_name.lower())
#        if(DEBUG_WRITE):
#                f.write("      uc_ef count: " + str(uc_ef.count()) + " " + str(timezone.now()) + "\n")

        for x in uc_ef:
#                if(DEBUG_WRITE):
#                        f.write("      x: " + str(x) + " " + str(timezone.now()) + "\n")
                try:
                        events.objects.get(ev_number=int(x.assn_member_field4_value))
                except events.DoesNotExist:
                        x.delete()
                        if(DEBUG_WRITE):
                                f.write("       deleting field value 4: " + str(x.assn_member_field4_value) + "\n")
                else:
#                        if(DEBUG_WRITE):
#                                f.write("       found event x: " + str(x) + "\n")
                        rating_list.append([
                                        x.assn_member_field1_value, 
                                        x.assn_member_field2_value, 
                                        x.assn_member_field3_value, 
                                        x.assn_member_field4_value, 
                                        x.assn_member_field5_value,
                                        Make_Timezone_String_Timezone_Aware(x.assn_member_field1_value),
                                        Make_Timezone_String_Timezone_Aware(x.assn_member_field2_value)])
        sorted_rating_list = sorted(rating_list, key=lambda x: (x[5]))
        for y in sorted_rating_list:
                if(DEBUG_WRITE):
                        f.write("       sorted_rating_list: " + str(y[3]) + " full string: " + str(y) + "\n")
                if(y[5] <= rating_date):
                        if(DEBUG_WRITE):
                                f.write("        found assn_member_field1_value less than rating date: " + str(y[5]) + " " + str(rating_date)+"\n")
                        if(y[2].upper() <= rating.upper() and y[5] <= rating_date):
                                if(DEBUG_WRITE):
                                        f.write("         found rating y[2]... less than or equal to rating...  " + str(y[2]) + " " + str(rating)+"\n")
                                rating = y[2]
                                ev_num = y[3]
                                award_year = str(y[5].year)[2:4] if y[5] else ""
                                award_year_end = str(y[6].year)[2:4] if y[6] else ""
                                if(DEBUG_WRITE):
                                        f.write("           found rating: " + str(rating) + " ev_number: " + str(ev_num) + " rating_date: " + str(award_year) + " yo: " + str(award_year_end) + "\n")
        if(DEBUG_WRITE):
                f.write("            Now looking for event: " + str(rating) + " ev_number: " + str(ev_num) + "\n")
        if(ev_num is not None):
                event = events.objects.get(ev_number=ev_num)
                if(DEBUG_WRITE):
                        f.write("             Found event: " + str(event) + " " + str(event.ev_number) + " " + str(timezone.now()) + "\n")

        if(DEBUG_WRITE):
                f.write("       COMPLETE: BF_get_rating_at_specific_date_from_assn_member_extra_field: " 
                        + str(asn_member) + " " + str(asn_member.assn_member_identifier) + " " + str(discipline_name) + " "+ str(rating_date) + " " + str(timezone.now())
                        + str(rating) + " " + str(event) + str(timezone.now()) + "\n")
        return (rating, award_year, award_year_end, event)

def BF_clear_tourney_event_and_final_result_ratings_extra_fields(f, s_date, e_date, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      BF_clear_event_and_final_result_ratings_extra_fields: " + str(s_date) + " to " + str(e_date) + str(timezone.now()) + "\n")

        if(s_date is None):
                for x in tournaments.objects.all():
                        tournament_extra_fields.objects.filter(tef_tourney = x).delete()
                        for y in events.objects.filter(ev_tourney = x):
                                event_extra_fields.objects.filter(eev_event = y).delete()
                                for z in event_final_results.objects.filter(efr_event = y):
                                        event_final_results_extra_fields.objects.filter(efr_event_final_results = z).delete()
        else:
#                for x in tournaments.objects.filter(tourney_start_date__gte = s_date, tourney_end_date__lte = e_date):
                for x in tournaments.objects.filter(tourney_start_date__gte = s_date):
                        x.tourney_potential_rating = ""
                        x.tourney_final_rating = ""
                        x.save()
                        tournament_extra_fields.objects.filter(tef_tourney = x).delete()
                        for y in events.objects.filter(ev_tourney = x):
                                event_extra_fields.objects.filter(eev_event = y).delete()
                                for z in event_final_results.objects.filter(efr_event = y):
                                        event_final_results_extra_fields.objects.filter(efr_event_final_results = z).delete()
        if(DEBUG_WRITE):
                f.write("      BF_clear_event_and_final_result_ratings_extra_fields: " + str(s_date) + " to " + str(e_date) + str(timezone.now()) + "\n")
def BF_clear_assn_member_history_recalc_current_rating(f, s_date, e_date, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("\nBF_clear_assn_member_history_recalc_current_rating: " + str(s_date) + " to " + str(e_date) + str(timezone.now()) + "\n")

        asn = get_association(None, "British Fencing", False)
        if s_date is None:
                if(DEBUG_WRITE):
                        f.write("   resetting all history and current rating: " + str(timezone.now()) + "\n")
                try:
                        # Get all association members
                        members = association_members.objects.filter(assn = asn)

                        # Delete 'current rating' records in bulk
                        association_member_extra_fields.objects.filter(
                        assn_member__in=members,
                        assn_member_field_name__iexact='current rating'
                        ).delete()

                        # Delete 'rating history' records in bulk
                        association_member_extra_fields.objects.filter(
                        assn_member__in=members,
                        assn_member_field_name__iexact='rating history'
                        ).delete()

                        f.write("BF_clear_assn_member_history_recalc_current_rating: deleted records\n")

#                        print("Records deleted successfully.")
                except Exception as e:
                        f.write("BF_clear_assn_member_history_recalc_current_rating: occurred deleting records\n")
                        record_error_data('x_helper_assn_specific', 'BF_clear_assn_member_history_recalc_current_rating', 'error', "occurred deleting records")
                        print(f"An error occurred: {e}")

                if(DEBUG_WRITE):
                        cr_left_count = association_member_extra_fields.objects.filter(
                                                assn_member__in=members,
                                                assn_member_field_name__iexact='current rating').count()

                        cr_left_count = association_member_extra_fields.objects.filter(
                                        assn_member__in=members,
                                        assn_member_field_name__iexact='rating history').count()
                        f.write("    DONE resetting all history and current rating: " + str(timezone.now()) + "\n")
                        f.write("     current ratings in assn_mem_extra: " + str(cr_left_count) 
                                + " rating history: " + str(cr_left_count) + " " + "\n")
        else:
                if(DEBUG_WRITE):
                        f.write("   resetting SOME histories and recalculating: " + str(s_date) + " to " + str(e_date) + str(timezone.now()) + "\n")
#                members = association_members.objects.filter(assn = asn, assn_member_identifier__in = ('136150', '136151', '137822'))
                members = association_members.objects.filter(assn = asn)
                assn_members_ex_fields = association_member_extra_fields.objects.filter(assn_member__in = members, assn_member_field_name__in = ('Rating History', 'Current Rating')).values('assn_member').distinct()
#                print("    members count: ", str(members.count()), " assn_membner_ex_fields count: ", str(assn_members_ex_fields.count()))

                if(DEBUG_WRITE):
                        f.write("    members count: " + str(members.count()) + " " + " assn_membner_ex_fields count: " + str(assn_members_ex_fields.count()) + " " + str(timezone.now()) + "\n")

                for w in assn_members_ex_fields:
#                        if(x.assn_member_identifier in ('136150', '136151', '137822')):
                        if(1==1):
                                x = association_members.objects.get(id = w['assn_member'])
                                if(DEBUG_WRITE):
                                        f.write("\n\n      working on: " + str(x.assn_member_identifier) + " " + str(x.assn_member_full_name) + " " + str(timezone.now()) + "\n")
                                association_member_extra_fields.objects.filter(assn_member = x, assn_member_field_name__iexact = 'current rating').delete()
                                association_member_extra_fields.objects.annotate(
                                        field1_value_datetime=Cast('assn_member_field1_value', output_field=models.DateTimeField())
                                                ).filter(
                                                assn_member=x,
                                                assn_member_field_name__iexact='rating history',
                                                field1_value_datetime__gte=s_date,
                                                field1_value_datetime__lte=e_date
                                                ).delete()
                                for y in association_discipline.objects.filter(assn = asn):
                                        if(y.discipline_name.lower() != 'unknown'):
                                                current_rating, award_year, award_year_end, ev = BF_get_rating_at_specific_date_from_assn_member_extra_field(f, x, 
                                                                y.discipline_name, s_date, False)
                                                if(DEBUG_WRITE):
                                                        f.write("         get rating at specific date results from assn member record... discipline name: " + str(y.discipline_name) + " current rating: " + str(current_rating) + " event: " + str(ev) + " " + str(timezone.now()) + "\n")      
        #                        BF_update_or_create_rating_history(f, amr, eve, eve.ev_assn_discipline.discipline_name, f_rating, eve.ev_start_date, True)
                                                if ev is not None:
                                                        cr = BF_update_or_create_current_rating(f, x, y.discipline_name, current_rating, ev.ev_start_date, True)
                                if(DEBUG_WRITE):
                                        f.write("       DONE working on: " + str(x.assn_member_identifier) + " " + str(x.assn_member_full_name) + " " + str(timezone.now()) + "\n")
                                        f.write("         whats left: Assn Member Current Rating" + str(timezone.now()) + "\n")
                                        assn_ratings_current = BF_get_all_assn_member_extra_current_ratings(f, x, False)
                                        for qq in assn_ratings_current:
                                                f.write("            " + str(qq) + "\n")
                                        f.write("         whats left: Rating History" + str(timezone.now()) + "\n")
                                        assn_rating_history = BF_get_all_assn_member_extra_rating_history(f, x, False)
                                        for qq in assn_rating_history:
                                                f.write("            " + str(qq) + "\n")

        if(DEBUG_WRITE):
                f.write("      BF_clear_assn_member_history_recalc_current_rating: " + str(s_date) + " to " + str(e_date) + str(timezone.now()) + "\n")

def apply_rating_overrides(f, eve, current_rating, total_fencers, DEBUG_WRITE):
#        DEBUG_WRITE = True
        new_rating = None
        event_nif = get_event_extra_field_value(f, eve, 'NIF', False)
        if(DEBUG_WRITE):
                f.write("                     apply_rating_overrides: " + str(current_rating)
                                        + "tournament assn name: " + str(eve.ev_tourney.tourney_assn.assn_name)
                                        + "tournament name: " + str(eve.ev_tourney.tourney_name)
                                        + "event name: " + str(eve.ev_name) 
                                        + " a4_event_assn_age_category description: " + str(eve.ev_assn_ages.age_category_description)
                                        + "total_fencers: " + str(total_fencers)
                                        + " NIF: " + str(event_nif) 
                                        + " start date: " + str(eve.ev_start_date)                                         
                                        + "\n")
        if(DEBUG_WRITE):
                f.write("                     apply_rating_overrides a4 query values: " 
                                        + " a4_assn: " + str(eve.ev_tourney.tourney_assn)
                                        + " a4_event_assn_type: " + str(eve.ev_assn_type)
                                        + " a4_event_assn_discipline: " + str(eve.ev_assn_discipline)
                                        + " a4_event_assn_gender: " + str(eve.ev_assn_gender)
                                        + " a4_event_assn_age_category: " + str(eve.ev_assn_ages)
                                        + " a4_event_assn_age_category description: " + str(eve.ev_assn_ages.age_category_description)
                                        + " a4_end_date__gte: " + str(eve.ev_start_date)
                                        + "\n")
        if(eve.ev_assn_discipline.discipline_name.lower() in ('saber', 'sabre')):
                try:
                        a4 = admin_a4_minimums.objects.get(
                                a4_assn = eve.ev_tourney.tourney_assn,
                                a4_event_assn_type = eve.ev_assn_type,
                                a4_event_assn_discipline__discipline_name__in = ('Saber', 'Sabre'),
                                a4_event_assn_gender = eve.ev_assn_gender,
                                a4_event_assn_age_category__age_category_description__iexact = eve.ev_assn_ages.age_category_description.lower(),
                                a4_end_date__gte = eve.ev_start_date)
                except admin_a4_minimums.DoesNotExist:
                        a4 = None
                        if(DEBUG_WRITE):
                                f.write("                        apply_rating_overrides: admin_a4_minimum sabre does not exist\n")
                        new_rating = None
        else:
                try:
                        a4 = admin_a4_minimums.objects.get(
                                a4_assn = eve.ev_tourney.tourney_assn,
                                a4_event_assn_type = eve.ev_assn_type,
                                a4_event_assn_discipline = eve.ev_assn_discipline,
                                a4_event_assn_gender = eve.ev_assn_gender,
                                a4_event_assn_age_category__age_category_description__iexact = eve.ev_assn_ages.age_category_description.lower(),
                                a4_end_date__gte = eve.ev_start_date)
                except admin_a4_minimums.DoesNotExist:
                        a4 = None
                        if(DEBUG_WRITE):
                                f.write("                        apply_rating_overrides: admin_a4_minimum does not exist\n")
                        new_rating = None
        if(a4 is not None):
                if(DEBUG_WRITE):
                        f.write("                        apply_rating_overrides: admin_a4_minimum a4 nif: " 
                                + str(a4.a4_nif) + " event_nif: " + str(event_nif) + "\n")
                        f.write("                        apply_rating_overrides: admin_a4_minimum a4 min fencers: " 
                                + str(a4.a4_total_fencers) + " total_fencers: " + str(total_fencers) + "\n")
                if(event_nif >= a4.a4_nif) or (total_fencers >= a4.a4_total_fencers):
                        new_rating = "A4"
                ex_field_value = "Found A4 Override: " + " Tourney: " + str(eve.ev_tourney.tourney_name) \
                        + " Event: " + str(eve.ev_name) + " Total Fencers: " + str(total_fencers) \
                        + " NIF: " + str(event_nif) + " start date: " + str(eve.ev_start_date) \
                        + " A4 NIF: " + str(a4.a4_nif)
                update_or_create_event_extra_field(f, eve, "A4 Override Flag", ex_field_value, False)

        adt = admin_deleted_tournaments.objects.filter(
                        adt_tourney_assn_name = eve.ev_tourney.tourney_assn.assn_name,
                        adt_tourney_name = eve.ev_tourney.tourney_name,
                        adt_tourney_inbound = eve.ev_tourney.tourney_inbound,
                        adt_tourney_start_date = eve.ev_tourney.tourney_start_date,
                        adt_tourney_end_date = eve.ev_tourney.tourney_end_date)
        if (adt is not None and len(adt) > 0):
                ex_field_value = "Found admin_deleted_tournaments: " + " Tourney: " + str(eve.ev_tourney.tourney_name) \
                        + " Event: " + str(eve.ev_name) + " start date: " + str(eve.ev_tourney.tourney_start_date) \
                        + " end date: " + str(eve.ev_tourney.tourney_end_date)
                update_or_create_event_extra_field(f, eve, "admin_deleted_tournaments", ex_field_value, False)
                new_rating = "NR"
        if (eve.ev_hide_from_ratings_calc == True):
                ex_field_value = "Found admin_deleted_events: " + " Tourney: " + str(eve.ev_tourney.tourney_name) \
                        + " Event: " + str(eve.ev_name) + " start date: " + str(eve.ev_tourney.tourney_start_date) \
                        + " end date: " + str(eve.ev_tourney.tourney_end_date)
                update_or_create_event_extra_field(f, eve, "admin_deleted_events", ex_field_value, False)
                new_rating = "NR"

        if(eve.ev_assn_type.type_category.lower() == 'team'):
                ex_field_value = "Found team event - ignoring: " + " Tourney: " + str(eve.ev_tourney.tourney_name) \
                        + " Event: " + str(eve.ev_name) + " team event: " + eve.ev_assn_type.type_category
                update_or_create_event_extra_field(f, eve, "team_event", ex_field_value, False)
                new_rating = "NR"

#        print("cat_desc", eve.ev_assn_ages.age_category_description.lower())
        if(eve.ev_assn_ages.age_category_description.lower() in 
                                ('unknown', 'under 5', 'under 6', 'under 7',
                                'under 8', 'under 9', 'under 10', 'under 11',
                                'under 12', 'under 13', 'under 14')):
                ex_field_value = "Found underage - ignoring: " + " Tourney: " + str(eve.ev_tourney.tourney_name) \
                        + " Event: " + str(eve.ev_name) + " age: " + eve.ev_assn_ages.age_category_description
#                print(ex_field_value)
                update_or_create_event_extra_field(f, eve, "underage_event", ex_field_value, False)
#                ignore_event = False
                new_rating = "NR"

        # check for 1 and 2 - if not there, do not rating
        if(eve.ev_tourney.tourney_inbound in ('FencingTimeLive', 'S80', 'LPJS', 'Engarde', 'Durham')):
                pos = event_final_results.objects.filter(efr_event = eve, efr_final_position__in = (1,2))
                if(len(pos) < 2) and ():
                        ex_field_value = "Missing first and second position in event_final_results- ignoring: " + " Tourney: " + str(eve.ev_tourney.tourney_name) \
                                + " Event: " + str(eve.ev_name) 
                        print(ex_field_value)
                        update_or_create_event_extra_field(f, eve, "missing finalists", ex_field_value, False)
        #                ignore_event = False
                        new_rating = "NR"

        if(DEBUG_WRITE):
                f.write("                      Completed apply_rating_overrides: " + str(current_rating)
                                        + "--tournament name: " + str(eve.ev_tourney.tourney_name)
                                        + "--event name: " + str(eve.ev_name) 
                                        + "--new_rating: " + str(new_rating) 
                                        + "--total_fencers: " + str(total_fencers) + "\n")
#        print(new_rating, eve.ev_assn_type.type_category, eve.ev_assn_ages.age_category_description)
        return(new_rating)#ignore_event)

def BF_calc_potential_rating(f, eve, fencers_dict, tot_fencers, assn_recs, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("\n               BF_calc_potential_rating: " + str(eve.ev_name) + " " + str(timezone.now()) + "\n")
        pot_rating = "NR"
        start_a = 0
        start_b = 0
        start_c = 0
        start_d = 0
        start_e = 0
        result_evt = None
        result_assn_mbr_num = None
        result_given_mbr_id = None
        result_given_mbr_name = None
        result_given_mbr_club = None
        result_current_rating = None
        result_final_position = None
        tot_athletes = 0

        for q in fencers_dict:
                tot_athletes = tot_athletes + 1
                if('efr_final_position' in q):
                        if(1==0):
                                f.write("Working EFR: " + str(q) + "\n")
                        result_evt = q['efr_event']
                        result_assn_mbr_num = q['efr_assn_member_number']
                        result_given_mbr_id = q['efr_given_member_identifier']
                        result_given_mbr_name = q['efr_given_name']
                        result_given_mbr_club = q['efr_given_club']
                        result_final_position = q['efr_final_position']
                else:
                        if(1==0):
                                f.write("Working ERA" + str(q) + "\n")
                        result_evt = q['era_event']
                        result_assn_mbr_num = q['era_assn_member_number']
                        result_given_mbr_id = q['era_given_member_identifier']
                        result_given_mbr_name = q['era_given_name']
                        result_given_mbr_club = q['era_given_club']
                        result_final_position = None

                current_rating = "U"
                amr = None
                ev = None
                if(result_assn_mbr_num is not None):
                        amr = get_assn_member_record_by_assn_member_number(f, eve.ev_tourney.tourney_assn, result_assn_mbr_num, False)
#                if(amr is None):
#                        get_assn_member_record(f, eve.ev_tourney.tourney_assn, assn_recs, result_given_mbr_id, result_given_mbr_name, "", "", DEBUG_WRITE)                       
                if(amr is not None):
                        if(eve.ev_start_date is not None):
                                s_date = eve.ev_start_date - relativedelta(hours=1)
                        else:
                                s_date = None
#                        s_date = timezone.now()
                        if(eve.ev_assn_discipline is not None and s_date is not None):
                                current_rating, award_date, award_date_end, ev = BF_get_rating_at_specific_date_from_assn_member_extra_field(f, amr, 
                                        eve.ev_assn_discipline.discipline_name, s_date, False)
#                                current_rating = 'A'
                        if(1==0):
                                f.write("Current Rating Return:  "
                                                + "---eve.ev_start_date: " + str(eve.ev_start_date)
                                                + "---s_date: " + str(s_date)
                                                + "---eve.ev_assn_discipline.discipline_name: " + str(eve.ev_assn_discipline.discipline_name)
                                                + "---Retreived Current Rating: " + str(current_rating)
                                                + "\n")

                if(amr is None):
                        if(1==0):
                                f.write("Association Member Record Not Found:  "
                                        + "---Given Member Identifier: " + str(result_given_mbr_id)
                                        + "---Given Name: " + str(result_given_mbr_name)
                                        + " Final Position: " + str(result_final_position) + "\n")
                else:
                        if(1==0):
                                f.write("Current Rating: " + str(current_rating)
                                        + "---Given Member Identifier: " + str(result_given_mbr_id)
                                        + " Mem ID: " + str(amr.assn_member_identifier)
                                        + "---Given Name: " + str(result_given_mbr_name)
                                        + " Full Name: " + str(amr.assn_member_full_name)
                                        + " Current Rating: " + str(current_rating)
                                        + " Final Position: " + str(result_final_position) 
                                        + "\n")
                
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


        #we know how many, off to event rating calc
        tot_a_or_better = start_a
        tot_b_or_better = tot_a_or_better + start_b
        tot_c_or_better = tot_b_or_better + start_c
        tot_d_or_better = tot_c_or_better + start_d
        tot_e_or_better = tot_d_or_better + start_e

        if(tot_athletes == 0):
                pot_rating = "NR"
        if(tot_athletes > 0 and tot_athletes < 6):
                pot_rating = "U"
        if(tot_athletes >=6):
                pot_rating = "E1"
        if((tot_athletes >=15) and (tot_e_or_better >= 4)):
                pot_rating = "D1"
        if((tot_athletes >=15) and tot_e_or_better >= 6 \
           and tot_d_or_better >= 4 and tot_c_or_better >= 2 ):
                pot_rating = "C1"
        if((tot_athletes >=25) and tot_e_or_better >= 8 and tot_d_or_better >= 4):
                pot_rating = "C2"
        if((tot_athletes >=64) and tot_e_or_better >= 36 and tot_d_or_better >= 24):
                pot_rating = "C3"
        if((tot_athletes >=15) and tot_d_or_better >= 6 \
           and tot_c_or_better >= 4 and tot_b_or_better >= 2 ):
                pot_rating = "B1"
        if((tot_athletes >=25) and tot_d_or_better >= 6 \
           and tot_c_or_better >= 4 and tot_b_or_better >= 2 ):
                pot_rating = "B2"
        if((tot_athletes >=64) and tot_d_or_better >= 36 and tot_c_or_better >= 24):
                pot_rating = "B3"
        if((tot_athletes >=15) and tot_c_or_better >= 6 \
           and tot_b_or_better >= 4 and tot_a_or_better >= 2 ):
                pot_rating = "A1"
        if((tot_athletes >=25) and tot_c_or_better >= 6 \
           and tot_b_or_better >= 4 and tot_a_or_better >= 2 ):
                pot_rating = "A2"
        if((tot_athletes >=64) and tot_c_or_better >= 36 and tot_b_or_better >= 24):
                pot_rating = "A3"
        if((tot_athletes >=64) and tot_c_or_better >= 36 and tot_b_or_better >= 24 and tot_a_or_better >= 12):
                pot_rating = "A4"

        if(DEBUG_WRITE):
                f.write("                  Calcing STARTING Rating\n")
                f.write("                     Tournament Name: " + str(eve.ev_tourney.tourney_name) + " Event Name: " + str(eve.ev_name) + "\n")
                f.write("                     Total Fencers: " + str(tot_athletes) + "\n")
                f.write("                     STARTING: " + str(start_a) + ", " + str(start_b) + ", " + str(start_c)  + ", " + str(start_d) + ", " + str(start_e) + "\n")
                f.write("                     TOTALS:  " + str(tot_a_or_better) + ", " + str(tot_b_or_better) + ", " + str(tot_c_or_better) + ", " + str(tot_d_or_better) + ", " + str(tot_e_or_better) + "\n")
                f.write("                  Potential Rating: " + str(pot_rating) + "\n")
        override_rating = apply_rating_overrides(f, eve, pot_rating, tot_athletes, DEBUG_WRITE)
        if(DEBUG_WRITE):
                f.write("                  Overrides:  Potential Rating: " + str(override_rating) + "\n")
#                f.write("                  Overrides:  Ignore Event: " + str(ignore_event) + "\n")
        if(override_rating is not None):
                pot_rating = override_rating

        start_u = tot_athletes - (start_a + start_b + start_c + start_d + start_e)
        ex_field_value = "Total Fencers: " + str(tot_athletes) + "; As: " + str(start_a) + " Bs: " + str(start_b) + " Cs: " + str(start_c) + " Ds: " + str(start_d) + " Es: " + str(start_e) + " Us: " + str(start_u)
        update_or_create_event_extra_field(f, eve, "Potential Rating", pot_rating, False)
        update_or_create_event_extra_field(f, eve, "Potential Rating Distribution", ex_field_value, False)

        if(DEBUG_WRITE):
                f.write("               BF_calc_potential_rating: " + str(eve) + " " + str(pot_rating) 
                        + str(timezone.now()) + "\n")
def BF_calc_final_rating(f, eve, fencers_dict, tot_fencers, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("\n               BF_calc_final_rating: " + str(eve) + " " + str(timezone.now()) + "\n")
        end_rating = "NR"
        top_8_a = 0
        top_8_b = 0
        top_8_c = 0
        top_8_d = 0
        top_8_e = 0
        top_12_a = 0
        top_12_b = 0
        top_12_c = 0
        top_12_d = 0
        top_12_e = 0
        start_a = 0
        start_b = 0
        start_c = 0
        start_d = 0
        start_e = 0

        for q in fencers_dict:
                current_rating = "U"
                amr = None
                ev = None
                if(q['assn_member_number'] is not None):
                        amr = get_assn_member_record_by_assn_member_number(f, eve.ev_tourney.tourney_assn, q['assn_member_number'], False)
                if(amr is not None):
                        if(eve.ev_start_date is not None):
                                s_date = eve.ev_start_date - relativedelta(hours=1)
                        else:
                                s_date = None
                        if(eve.ev_assn_discipline is not None and s_date is not None):
                                current_rating, award_date, award_date_end, ev = BF_get_rating_at_specific_date_from_assn_member_extra_field(f, amr, 
                                eve.ev_assn_discipline.discipline_name, s_date, False)
                if(amr is None):
                        if(1==0):
                                f.write("Association Member Record Not Found:  " 
                                        + "---Given Member Identifier: " + str(q['efr_given_member_identifier'])
                                        + "---Given Name: " + str(q['efr_given_name'])
                                        + " Final Position: " + str(q['efr_final_position']) + "\n")
                else:
                        if(1==0):
                                f.write("Current Rating: " + str(current_rating)
                                        + "---Given Member Identifier: " + str(q['efr_given_member_identifier'])
                                        + " Mem ID: " + str(amr.assn_member_identifier)
                                        + "---Given Name: " + str(q['efr_given_name'])
                                        + " Full Name: " + str(amr.assn_member_full_name)
                                        + " Final Position: " + str(q['efr_final_position']) + "\n")
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

                if(q['efr_final_position'] <= 8):
                        if(current_rating == "A"):
                                top_8_a = top_8_a + 1
                        if(current_rating == "B"):
                                top_8_b = top_8_b + 1
                        if(current_rating == "C"):
                                top_8_c = top_8_c + 1
                        if(current_rating == "D"):
                                top_8_d = top_8_d + 1
                        if(current_rating == "E"):
                                top_8_e = top_8_e + 1
                if(q['efr_final_position'] <= 12):
                        if(current_rating == "A"):
                                top_12_a = top_12_a + 1
                        if(current_rating == "B"):
                                top_12_b = top_12_b + 1
                        if(current_rating == "C"):
                                top_12_c = top_12_c + 1
                        if(current_rating == "D"):
                                top_12_d = top_12_d + 1
                        if(current_rating == "E"):
                                top_12_e = top_12_e + 1

        pot_rating = get_event_extra_field_value(f, eve, 'Potential Rating', False)

        if(tot_fencers == 0):
                end_rating = "NR"
        if(tot_fencers > 0 and tot_fencers < 6):
                end_rating = "U"
        if(tot_fencers >=6):
                end_rating = "E1"
        if(tot_fencers >= 15 and ((top_8_a+top_8_b+top_8_c+top_8_d+top_8_e) >= 2)
           and pot_rating in ["D1","C1","C2","C3","B1","B2","B3","A1","A2","A3","A4"]):
                end_rating = "D1"
        if(tot_fencers >= 15 \
                and ((top_8_a+top_8_b+top_8_c) >=2) \
                and ((top_8_a+top_8_b+top_8_c+top_8_d) >=4)
                and pot_rating in ["C1","C2","C3","B1","B2","B3","A1","A2","A3","A4"]):
                end_rating = "C1"
        if(tot_fencers >= 25 \
                and ((top_8_a+top_8_b+top_8_c+top_8_d) >=4)
                and pot_rating in ["C2","C3","B2","B3","A2","A3","A4"]):
                end_rating = "C2"
        if(tot_fencers >= 64 \
                and ((top_8_a+top_8_b+top_8_c+top_8_d) >=4) \
                and ((top_12_a+top_12_b+top_12_c+top_12_d+top_12_e) >=4)
                and pot_rating in ["C3","B3","A3","A4"]):
                end_rating = "C3"
        if(tot_fencers >= 15 \
                and ((top_8_a+top_8_b) >=2) \
                and ((top_8_a+top_8_b+top_8_c) >=4)
                and pot_rating in ["B1","B2","B3","A1","A2","A3","A4"]):
                end_rating = "B1"
        if(tot_fencers >= 25 \
                and ((top_8_a+top_8_b) >=2) \
                and ((top_8_a+top_8_b+top_8_c) >=4)
                and pot_rating in ["B2","B3","A2","A3","A4"]):
                end_rating = "B2"
        if(tot_fencers >= 64 \
                and ((top_8_a+top_8_b+top_8_c) >=4) \
                and ((top_12_a+top_12_b+top_12_c+top_12_d) >=4)
                and pot_rating in ["B3","A3","A4"]):
                end_rating = "B3"
        if(tot_fencers >= 15 \
                and ((top_8_a) >=2) \
                and ((top_8_a+top_8_b) >=4)
                and pot_rating in ["A1","A2","A3","A4"]):
                end_rating = "A1"
        if(tot_fencers >= 25 \
                and ((top_8_a) >=2) \
                and ((top_8_a+top_8_b) >=4)
                and pot_rating in ["A2","A3","A4"]):
                end_rating = "A2"
        if(tot_fencers >= 64 \
                and ((top_8_a+top_8_b) >=4) \
                and ((top_12_a+top_12_b+top_12_c) >=4)
                and pot_rating in ["A3","A4"]):
                end_rating = "A3"
        if(tot_fencers >= 64 \
                and ((top_8_a) >=4) \
                and ((top_12_a+top_12_b) >=4)
                and pot_rating in ["A4"]):
                end_rating = "A4"

#        print(eve.ev_tourney.tourney_name, eve.ev_name, "pot_rating", pot_rating,"end_rating", end_rating, tot_fencers, top_8_a+top_8_b)

        override_rating = apply_rating_overrides(f, eve, end_rating, tot_fencers, DEBUG_WRITE)
        if(override_rating is not None):
                end_rating = override_rating

        if(1==1):
                update_or_create_event_extra_field(f, eve, "Final Rating", end_rating, False)
                start_u = tot_fencers - (start_a + start_b + start_c + start_d + start_e)
                ex_field_value = "Total Fencers: " + str(tot_fencers) + "; As: " + str(start_a) + "; Bs: " + str(start_b) + "; Cs: " + str(start_c) + "; Ds: " + str(start_d) + "; Es: " + str(start_e) + "; Us: " + str(start_u)
                update_or_create_event_extra_field(f, eve, "Final Rating Distribution", ex_field_value, False)
                ex_field_value = "Total Fencers: " + str(tot_fencers) + "; As: " + str(top_8_a) + "; Bs: " + str(top_8_b) + "; Cs: " + str(top_8_c) + "; Ds: " + str(top_8_d) + "; Es: " + str(top_8_e) 
                update_or_create_event_extra_field(f, eve, "Final Rating Top 8 Distribution", ex_field_value, False)
                ex_field_value = "Total Fencers: " + str(tot_fencers) + "; As: " + str(top_12_a) + "; Bs: " + str(top_12_b) + "; Cs: " + str(top_12_c) + "; Ds: " + str(top_12_d) + "; Es: " + str(top_12_e) 
                update_or_create_event_extra_field(f, eve, "Final Rating Top 12 Distribution", ex_field_value, False)

                if(DEBUG_WRITE):
                        f.write("                  Calcing FINAL Rating\n")
                        f.write("                     Tournament Name: " + str(eve.ev_tourney.tourney_name) + " Event Name: " + str(eve.ev_name) + "\n")
                        f.write("                     Total Fencers: " + str(tot_fencers) + "\n")
                        f.write("                     Final Rating: " + str(end_rating) + "\n")               

        if(DEBUG_WRITE):
                f.write("                   BF_calc_final_rating: " + str(eve.ev_name) + "---final rating:" + str(end_rating)
                        + " " + str(timezone.now()) + "\n")

def zzzBF_calc_difficulty(f, eve, fencers_dict, tot_fencers, check_date, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("\n               BF_calc_difficulty: " + str(eve) + " " + str(timezone.now()) + "\n")
        start_a = 0
        start_b = 0
        start_c = 0
        start_d = 0
        start_e = 0
        event_difficulty = 0.0

        for q in fencers_dict:
                try:
                        amr = association_members.objects.get(assn_member_number = q['assn_member_number'])
                except association_members.DoesNotExist:
                        amr = None
                        current_rating = "U"
                else:
                        if(eve.ev_assn_discipline is not None and eve.ev_start_date is not None):
                                current_rating, award_date, award_date_end, ev = BF_get_rating_at_specific_date_from_assn_member_extra_field(f, amr, 
                                        eve.ev_assn_discipline.discipline_name, check_date, False)
                if(amr is None):
                        if(1==0):
                                f.write("Association Member Record Not Found:  " 
                                        + "---Given Member Identifier: " + str(q.efr_given_member_identifier)
                                        + "---Given Name: " + str(q.efr_given_name)
                                        + " Final Position: " + str(q.efr_final_position) + "\n")
                else:
                        if(1==0):
                                f.write("Current Rating: " + str(current_rating)
                                        + "---Given Member Identifier: " + str(q.efr_given_member_identifier)
                                        + " Mem ID: " + str(amr.assn_member_identifier)
                                        + "---Given Name: " + str(q.efr_given_name)
                                        + " Full Name: " + str(amr.assn_member_full_name)
                                        + " Final Position: " + str(q.efr_final_position) + "\n")
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

                ev_points = ((start_a * a_points) + (start_b * b_points) + (start_c * c_points) + (start_d * d_points) + (start_e * e_points))
                if(float(tot_fencers) > 0):
                        c_pts = float(ev_points) / (float(tot_fencers) * float(a_points))
                else:
                        c_pts = 0.0
                event_difficulty = float(c_pts) * 100.0

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
                        f.write("                  Calcing FINAL Rating\n")
                        f.write("                     Tournament Name: " + str(eve.ev_tourney.tourney_name) + " Event Name: " + str(eve.ev_name) + "\n")
                        f.write("                     Total Fencers: " + str(tot_fencers) + "\n")
                        f.write("                     Difficulty: " + str(event_difficulty) + " " + str(ev_points) + " " + str(tot_fencers) + " " + str(c_pts) + "\n")
        if(DEBUG_WRITE):
                f.write("                   BF_calc_difficulty: " + str(eve.ev_name) 
                        + "---Difficulty: " + str(event_difficulty) + " " + str(timezone.now()) + "\n")


def BF_final_transform(f, end_rating, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      BF_final_transform: " + str(end_rating) + " " + str(timezone.now()) + "\n")
        if(end_rating in ("U", "NR", "Not Rated Yet", None)):
                a_s = 0
                b_s = 0
                c_s = 0
                d_s = 0
                e_s = 0
        if(end_rating == "E1"):
                a_s = 0
                b_s = 0
                c_s = 0
                d_s = 0
                e_s = 1
        if(end_rating == "D1"):
                a_s = 0
                b_s = 0
                c_s = 0
                d_s = 1
                e_s = 3
        if(end_rating == "C1"):
                a_s = 0
                b_s = 0
                c_s = 1
                d_s = 3
                e_s = 4
        if(end_rating == "C2"):
                a_s = 0
                b_s = 0
                c_s = 1
                d_s = 3
                e_s = 4
        if(end_rating == "C3"):
                a_s = 0
                b_s = 0
                c_s = 4
                d_s = 4
                e_s = 8
        if(end_rating == "B1"):
                a_s = 0
                b_s = 1
                c_s = 3
                d_s = 2
                e_s = 2
        if(end_rating == "B2"):
                a_s = 0
                b_s = 1
                c_s = 3
                d_s = 4
                e_s = 4
        if(end_rating == "B3"):
                a_s = 0
                b_s = 4
                c_s = 4
                d_s = 8
                e_s = 16
        if(end_rating == "A1"):
                a_s = 1
                b_s = 1
                c_s = 2
                d_s = 2
                e_s = 2
        if(end_rating == "A2"):
                a_s = 1
                b_s = 3
                c_s = 4
                d_s = 2
                e_s = 2
        if(end_rating == "A3"):
                a_s = 4
                b_s = 4
                c_s = 8
                d_s = 8
                e_s = 8
        if(end_rating == "A4"):
                a_s = 8
                b_s = 8
                c_s = 8
                d_s = 8
                e_s = 16
        if(DEBUG_WRITE):
                f.write("A range = " + "1" + " - " + str(a_s) + "\n")
                f.write("B range = " + str(1+a_s) + " - " + str(a_s+b_s) + "\n")
                f.write("C range = " + str(1+a_s+b_s) + " - " + str(a_s+b_s+c_s) + "\n")
                f.write("D range = " + str(1+a_s+b_s+c_s) + " - " + str(a_s+b_s+c_s+d_s) + "\n")
                f.write("E range = " + str(1+a_s+b_s+c_s+d_s) + " - " + str(a_s+b_s+c_s+d_s+e_s) + "\n")
        if(DEBUG_WRITE):
                f.write("      BF_final_transform: " + str(timezone.now()) + "\n")
        return(a_s, b_s, c_s, d_s, e_s)
def BF_apply_event_ratings_to_fencers(f, eve, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      bf_apply_event_ratings_to_fencers: " + str(eve) + " " + str(timezone.now()) + "\n")
        final_rating = get_event_extra_field_value(f, eve, "Final Rating", DEBUG_WRITE)
        a_s, b_s, c_s, d_s, e_s = BF_final_transform(f, final_rating, DEBUG_WRITE)
        asn = eve.ev_tourney.tourney_assn
        assn_recs = association_members.objects.filter(assn = asn).values_list('assn_member_full_name', flat=True)

        fencers = event_final_results.objects.filter(efr_event = eve).order_by('efr_final_position')
        for q in fencers:
                amr = get_assn_member_record_by_assn_member_number(f, asn, q.efr_assn_member_number, DEBUG_WRITE)
                if(amr is not None):
                        day_before = eve.ev_start_date - relativedelta(hours=1)

                        q_rating, q_award_date, q_award_date_end, q_event = BF_get_rating_at_specific_date_from_assn_member_extra_field(f, amr, eve.ev_assn_discipline.discipline_name, day_before, DEBUG_WRITE)

                        f_rating = "U"
                        f_pos = q.efr_final_position
                        if((f_pos >= 1) and (f_pos<=a_s)):
                                f_rating = "A"
                        if((f_pos >= 1+a_s) and (f_pos<=a_s+b_s)):
                                f_rating = "B"
                        if((f_pos >= 1+a_s+b_s) and (f_pos<=a_s+b_s+c_s)):
                                f_rating = "C"
                        if((f_pos >= 1+a_s+b_s+c_s) and (f_pos<=a_s+b_s+c_s+d_s)):
                                f_rating = "D"
                        if((f_pos >= 1+a_s+b_s+c_s+d_s) and (f_pos<=a_s+b_s+c_s+d_s+e_s)):
                                f_rating = "E"
                        if(1 == 1):
                                f.write("            STARTING Fencer Rating\n")
                                f.write("            Tournament Name: " + str(eve.ev_tourney.tourney_name) 
                                        + " Event Name: " + str(eve.ev_name)+"\n")
                                f.write("            Final Position: " + str(q.efr_final_position)
                                        + " Final Position: " + str(f_pos) + ", " + str(f_rating)
                                        + " Given License: " + str(q.efr_given_member_identifier)
                                        + " Member Identifier: " + str(amr.assn_member_identifier)
                                        + " Given Full Name: " + str(q.efr_given_name)
                                        + " Member Full Name: " + str(amr.assn_member_full_name) + "\n")
                        if os.environ.get("BF_RATING_TIME_LENGTH_YEARS") is not None:
                                rt_years = int(os.environ.get("BF_RATING_TIME_LENGTH_YEARS"))
                        else:
                                rt_years = 0
                        en_date = eve.ev_start_date# + relativedelta(years=rt_years)

                        update_or_create_efr_extra_field(f, q, 'efr_previous_rating', q_rating, DEBUG_WRITE)
                        update_or_create_efr_extra_field(f, q, 'efr_rating', f_rating, DEBUG_WRITE)
                        update_or_create_efr_extra_field(f, q, 'efr_award_date', en_date, DEBUG_WRITE)
                        rh = BF_update_or_create_rating_history(f, amr, eve, eve.ev_assn_discipline.discipline_name, f_rating, eve.ev_start_date, True)

#                        if(f_rating <= q_rating):
                        BF_update_or_create_current_rating(f, amr, eve.ev_assn_discipline.discipline_name, f_rating, eve.ev_start_date, DEBUG_WRITE)
        if(DEBUG_WRITE):
                f.write("       COMPLETE: bf_apply_event_ratings_to_fencers: " + str(eve) + " " + str(timezone.now()) + "\n")
def BF_calc_ratings_and_write_event_extra_fields(f, eve, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("            BF_calc_ratings_and_write_event_extra_fields: " + str(eve) + " " + str(timezone.now()) + "\n")
        efr_fencers_dict = []
        era_fencers_dict = []
        efr_tot_fencers = 0
        era_tot_fencers = 0
        assn_recs = association_members.objects.filter(assn = eve.ev_tourney.tourney_assn).values_list('assn_member_full_name', flat=True)

        if(eve is not None):
#                print(eve.ev_name)
                if(event_final_results.objects.filter(efr_event=eve).count() > 0):      
                        fencers = event_final_results.objects.filter(efr_event=eve).order_by('efr_given_name')
                        efr_tot_fencers = fencers.count()
#                        efr_tot_fencers = get_event_extra_field_value(f, eve, 'Fencers', False)
                        efr_fencers_dict = [model_to_dict(tt) for tt in fencers]
                        for qq in efr_fencers_dict:
                                qq['assn_member_number'] = qq['efr_assn_member_number']
                if(event_registered_athletes.objects.filter(era_event=eve).count() > 0):      
                        fencers = event_registered_athletes.objects.filter(era_event=eve).order_by('era_given_name')
                        era_tot_fencers = fencers.count()
                        era_fencers_dict = [model_to_dict(tt) for tt in fencers]
                        for qq in era_fencers_dict:
                                qq['assn_member_number'] = qq['era_assn_member_number']

                if(efr_tot_fencers > 0 or (efr_tot_fencers == 0 and era_tot_fencers == 0)):
                        BF_calc_potential_rating(f, eve, efr_fencers_dict, efr_tot_fencers, assn_recs, True)
                        BF_calc_final_rating(f, eve, efr_fencers_dict, efr_tot_fencers, DEBUG_WRITE)
                        BF_apply_event_ratings_to_fencers(f, eve, DEBUG_WRITE)
                else:
                        if(era_tot_fencers > 0):
                                BF_calc_potential_rating(f, eve, era_fencers_dict, era_tot_fencers, assn_recs, DEBUG_WRITE)
                                BF_apply_event_ratings_to_fencers(f, eve, DEBUG_WRITE)
        if(DEBUG_WRITE):
                f.write("      BF_calc_ratings_and_write_event_extra_fields: " + str(eve) + " " + str(timezone.now()) + "\n")
def BF_tournament_extra_field_value_build_ratings(f, tourney, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      tournament_extra_field_value_build_ratings: " + str(tourney) + " " + str(timezone.now()) + "\n")
        fin_str = ""
        pot_str = ""

        for eve in events.objects.filter(ev_tourney = tourney).order_by('ev_assn_gender', 'ev_assn_discipline'):
                rat_string = eve.ev_assn_gender.gender_description[0].upper()
                rat_string = rat_string + eve.ev_assn_discipline.discipline_name[0].upper() + "-"
                fin_str = fin_str + rat_string + get_event_extra_field_value(f, eve, 'Final Rating', False) + " "
                pot_str = pot_str + rat_string + get_event_extra_field_value(f, eve, 'Potential Rating', False) + " "
#        print(tourney.tourney_name, fin_str, pot_str)
        update_or_create_tournament_extra_field(f, tourney, "Potential Ratings", pot_str, DEBUG_WRITE)
        update_or_create_tournament_extra_field(f, tourney, "Final Ratings", fin_str, DEBUG_WRITE)
        #Performance only reason we are storing this twice...
        ttt = tournaments.objects.get(id = tourney.id)
        ttt.tourney_potential_rating = pot_str
        ttt.tourney_final_rating = fin_str
#        print(ttt.tourney_potential_rating, ttt.tourney_final_rating)
        ttt.save()


def UK_Apply_NIF_Points_To_Final_Results(f, asn, assn_recs, s80_event, durham_event, DEBUG_WRITE):
#        record_log_data("process_tournaments.py", "UK_Apply_NIF_Points_To_Final_Results", "started: " + str(timezone.now()))
        f.write("         UK_Apply_NIF_Points_To_Final_Results: " + str(s80_event) + " to " + str(durham_event) + " " + str(datetime.now()) + "\n")

        athlete_processed = 0
        s80_results = load_s80_fencing_fencing_results.objects.filter(event = s80_event)  
        for z in s80_results:
                if(z.realPoint is not None and len(z.realPoint) > 0 and int(z.realPoint) > 0):
#                        print(z.realPoint)
                        pos = clean_position(z.rank)
                        amn = get_assn_member_record(f, asn, assn_recs, z.identifier, z.name, "", "", False)
                        if(amn is None):
                                msg = "Cannot find athlete for NIF: " + str(z.rank) + " " + str(z.identifier) + " " + str(z.name) + " " + str(z.realPoint) + " - " + str(timezone.now())
                                record_error_data('process_tournament', 'UK_Apply_NIF_Points_To_Final_Results', 'error', msg)
                                if(DEBUG_WRITE):
                                        f.write("            UK_Apply_NIF_Points_To_Final_Results: " + msg + "\n")
                        else:
                                efr = event_final_results.objects.filter(efr_event = durham_event, efr_assn_member_number = amn.assn_member_number)
                                if(len(efr) == 1):
                                        rec = update_or_create_efr_extra_field(f, efr[0], "efr_final_points", str(z.realPoint), DEBUG_WRITE)
                                        athlete_processed += 1
                                if(len(efr) == 0):
                                        msg = "Cannot find athlete for NIF in Event Final Results: " + str(z.rank) + " " + str(z.identifier) + " " + str(z.name) + " - " + str(timezone.now())
                                        record_error_data('process_tournament', 'UK_Apply_NIF_Points_To_Final_Results', 'error', msg)
                                        if(DEBUG_WRITE):
                                                f.write("                 UK_Apply_NIF_Points_To_Final_Results: " + msg + "\n")
                                if(len(efr) > 1):
                                        msg = "More than 1 athlete found for NIF in Event Final Results: " + str(z.rank) + " " + str(z.identifier) + " " + str(z.name) + " - " + str(timezone.now())
                                        record_error_data('process_tournament', 'UK_Apply_NIF_Points_To_Final_Results', 'error', msg)
                                        if(DEBUG_WRITE):
                                                f.write("                 UK_Apply_NIF_Points_To_Final_Results: " + msg + "\n")
                else:
                        msg = "No RealPoint for athlete for NIF: " + str(z.rank) + " " + str(z.identifier) + " " + str(z.name) + " " + str(z.realPoint) + " - " + str(timezone.now())
                        if(DEBUG_WRITE):
                                f.write("            UK_Apply_NIF_Points_To_Final_Results: " + msg + "\n")

        f.write("         Completed: UK_Apply_NIF_Points_To_Final_Results. Total S80 results: " + str(len(s80_results)) + " total processed: " + str(athlete_processed) + " " + str(datetime.now()) + "\n")
#        record_log_data("process_tournaments.py", "UK_Apply_NIF_Points_To_Final_Results", "completed: " + str(athlete_processed) + " of " + str(len(s80_results)) + " " + str(timezone.now()))
def UK_Apply_NIFs(f, s_date, e_date, DEBUG_WRITE):
        record_log_data("process_tournaments.py", "UK_Apply_NIFs", "started: " + str(timezone.now()))
        f.write("\n\n\nUK_Apply_NIFs: " + str(s_date) + " to " + str(e_date) + " " + str(datetime.now()) + "\n")

        asn = get_association(f, "British Fencing", DEBUG_WRITE)
        assn_recs = association_members.objects.filter(assn = asn).values_list('assn_member_full_name', flat=True)

        for x in load_s80_fencing_competitions.objects.filter(isInternational = False, 
                        calced_endDate__gte = s_date, 
                        calced_endDate__lte = e_date).order_by('calced_endDate'):
                if (1==1):
#                if("Hampshire" in x.name):      
                        event_found_results = []
#                        print("UK_Apply_NIFs Processing Tournament S80: " + x.at_id + " - " + x.name + " - " + x.isInternational + " - " + str(x.calced_endDate) + " - " + str(timezone.now()) + "\n")
                        if(DEBUG_WRITE):
                                f.write("   UK_Apply_NIFs Processing Tournament S80: " + x.at_id + " - " + x.name + " - " + x.isInternational + " - " + str(x.calced_endDate) + " " + str(timezone.now()) + "\n")
                        events_to_check = load_s80_fencing_events.objects.filter(competition = x)
                        for y in events_to_check:
                                if(DEBUG_WRITE):
                                        f.write("      Working Event: " + y.name + " realNIF: " + str(y.realNif) + "\n")
                                if(y.realNif is not None and len(y.realNif) > 0 and int(y.realNif) > 0):
                                        final_recs = load_s80_fencing_fencing_results.objects.filter(
                                                event = y).values('rank', 'name', 'identifier')
                                        ef_results = list(final_recs)
                                        for z in ef_results:
                                                z['position'] = clean_position(z['rank'])
                                                z['full_name'] = z['name']
                                                z['club_name'] = ""
                                                z['assn_member_identifier'] = z['identifier']
                                                amn = get_assn_member_record(f, asn, assn_recs, z['identifier'], z['name'], "", "", False)
                                                if(amn is not None):
                                                        z['assn_member_number'] = amn.assn_member_number
                                                else:
                                                        z['assn_member_number'] = None
                                        event_final_results_sorted = sorted(ef_results, key=lambda x: x['position'])
                                        if(DEBUG_WRITE):
                                                f.write("      Working Event: " + y.name + "--- Athlete Count: " + str(len(event_final_results_sorted)) + "\n")
                                        event_found, eve = Event_Exists(f, asn, x.name, y.name, x.calced_endDate, event_final_results_sorted, len(event_final_results_sorted), DEBUG_WRITE)

                                        if(not event_found):
                                                msg = "Cannot find S80 event for NIF: " + x.at_id + " - " + x.name + " - " + x.isInternational + " - " + str(x.calced_endDate) + " - " + str(timezone.now())
                                                record_error_data('process_tournament', 'UK_Apply_NIFs', 'error', msg)
                                                if(DEBUG_WRITE):
                                                        f.write("                  UK_Apply_NIFs: " + msg + "\n")
                                        else:
                                                if(DEBUG_WRITE):
                                                        f.write("         Event Found: " + eve.ev_tourney.tourney_name + " " + eve.ev_name + " for s80 event: " 
                                                                + x.at_id + " - " + x.name + " - " + x.isInternational + " - " + str(x.calced_endDate) + " - " + str(timezone.now()) + "\n")
                                                event_NIF = get_event_extra_field_value(f, eve, 'NIF', False)
#                                                print(y.realNif, event_NIF)
                                                if(event_NIF is None or int(event_NIF) != int(y.realNif)):
                                                        msg = "NIF Mismatch: " + str(y.realNif) + " " + str(event_NIF) + " " + str(x.at_id) + " - " + str(x.name) + " - " + str(timezone.now())
                                                        if(DEBUG_WRITE):
                                                                f.write("                  UK_Apply_NIFs: " + msg + "\n")
                                                        update_or_create_event_extra_field(f, eve, 'NIF', y.realNif, False)
                                                        update_or_create_event_extra_field(f, eve, "BF Ranking Points", "True", DEBUG_WRITE)
                                                        UK_Apply_NIF_Points_To_Final_Results(f, asn, assn_recs, y, eve, DEBUG_WRITE)
                                                else:
                                                        msg = "NIF Match So Skipping: " + str(y.realNif) + " " + str(event_NIF) + " " + str(x.at_id) + " - " + str(x.name) + " - " + str(timezone.now())
                                                        if(DEBUG_WRITE):
                                                                f.write("                  UK_Apply_NIFs: " + msg + "\n")

        f.write("Completed: UK_Apply_NIFs: " + str(datetime.now()) + "\n")
        record_log_data("process_tournaments.py", "UK_Apply_NIFs", "completed: " + str(timezone.now()))
def UK_Apply_Fencer_Count_To_Event(f, s_date, e_date, DEBUG_WRITE):
        record_log_data("process_tournaments.py", "UK_Apply_Fencer_Count_To_Event", "started: " + str(timezone.now()))
        f.write("\n\n\nUK_Apply_Fencer_Count_To_Event: " + str(s_date) + " to " + str(e_date) + " " + str(datetime.now()) + "\n")

        for x in tournaments.objects.filter(tourney_start_date__gte = s_date, tourney_start_date__lte = e_date).order_by('tourney_start_date'): 
                if (1==1):
#                if("Hampshire" in x.name):      
                        for y in events.objects.filter(ev_tourney = x):                                
#                                print("Processing event: " + y.ev_tourney.tourney_name + " - " + y.ev_name + " - " + str(timezone.now()))
                                if(DEBUG_WRITE):
                                        f.write("   Processing event: " + y.ev_tourney.tourney_name + " - " + y.ev_name + " - " + str(timezone.now()) + "\n")
                                event_fencers = get_event_extra_field_value(f, y, 'Fencers', False)
                                if(event_fencers is None or int(event_fencers) == 0):
                                        ev_fencers = event_final_results.objects.filter(efr_event = y).count()
                                        if ev_fencers > 0:
                                                update_or_create_event_extra_field(f, y, 'Fencers', ev_fencers, False)
                                                if(DEBUG_WRITE):
                                                        f.write("         Event Fencers Updated: Final Results Count: " + str(ev_fencers) 
                                                        + " stored value: " + str(get_event_extra_field_value(f, y, 'Fencers', False)) + "\n")
                                        else:
                                                if(DEBUG_WRITE):
                                                        f.write("         Event Fencers NOT Updated: Event Final Results Count: " + str(ev_fencers) + "\n")
                                else:
                                        if(DEBUG_WRITE):
                                                f.write("         Event Fencers NOT Updated due to value already in place and no override: " + str(event_fencers) 
                                                + " stored value: " + str(get_event_extra_field_value(f, y, 'Fencers', False)) + "\n")

        f.write("Completed: UK_Apply_Fencer_Count_To_Event: " + str(datetime.now()) + "\n")
        record_log_data("process_tournaments.py", "UK_Apply_Fencer_Count_To_Event", "completed: " + str(timezone.now()))

def BF_get_current_user_and_licenses(request):
        current_user = []
        user_licenses = []

        if request.user.is_authenticated:
                current_user = User.objects.get(id=request.user.id)
                user_licenses = custom_user_assn_memberships.objects.filter(cuser=current_user).order_by('cuser_assn_member__assn_member_full_name')

        return (current_user, user_licenses)

def BF_Create_Assn(f, DEBUG_WRITE):
        next_assn_id = base_get_next_system_value('next_assn_id')
        asnnew = associations(assn_number=next_assn_id, assn_name='British Fencing', assn_status='active', 
                assn_url='www.britishfencing.com', 
                assn_phone='02087423032', assn_email='info@britishfencing.com', assn_description='British Fencing')
        asnnew.save()
        asn = get_association(f, "British Fencing", DEBUG_WRITE)
        lg_id = language.objects.get(language_code='en-us')

        association_geographies(assn=asn, geo_category='Domestic', geo_category_description='Domestic').save()
        association_geographies(assn=asn, geo_category='International', geo_category_description='International').save()
        association_geographies(assn=asn, geo_category='Unknown', geo_category_description='Unknown').save()

        association_ages(assn=asn, age_category='all_ages', age_category_description='All Ages').save()
        association_ages(assn=asn, age_category='Under 5', age_category_description='Under 5').save()
        association_ages(assn=asn, age_category='Under 6', age_category_description='Under 6').save()
        association_ages(assn=asn, age_category='Under 7', age_category_description='Under 7').save()
        association_ages(assn=asn, age_category='Under 8', age_category_description='Under 8').save()
        association_ages(assn=asn, age_category='Under 9', age_category_description='Under 9').save()
        association_ages(assn=asn, age_category='Under 10', age_category_description='Under 10').save()
        association_ages(assn=asn, age_category='Under 11', age_category_description='Under 11').save()
        association_ages(assn=asn, age_category='Under 12', age_category_description='Under 12').save()
        association_ages(assn=asn, age_category='Under 13', age_category_description='Under 13').save()
        association_ages(assn=asn, age_category='Under 14', age_category_description='Under 14').save()
        association_ages(assn=asn, age_category='Under 15', age_category_description='Under 15').save()
        association_ages(assn=asn, age_category='Under 16', age_category_description='Under 16').save()
        association_ages(assn=asn, age_category='Under 17', age_category_description='Under 17').save()
        association_ages(assn=asn, age_category='Under 18', age_category_description='Under 18').save()
        association_ages(assn=asn, age_category='Under 19', age_category_description='Under 19').save()
        association_ages(assn=asn, age_category='Under 20', age_category_description='Under 20').save()
        association_ages(assn=asn, age_category='Under 21', age_category_description='Under 21').save()
        association_ages(assn=asn, age_category='Under 22', age_category_description='Under 22').save()
        association_ages(assn=asn, age_category='Under 23', age_category_description='Under 23').save()
        association_ages(assn=asn, age_category='U5', age_category_description='Under 5').save()
        association_ages(assn=asn, age_category='U6', age_category_description='Under 6').save()
        association_ages(assn=asn, age_category='U7', age_category_description='Under 7').save()
        association_ages(assn=asn, age_category='U8', age_category_description='Under 8').save()
        association_ages(assn=asn, age_category='U9', age_category_description='Under 9').save()
        association_ages(assn=asn, age_category='U10', age_category_description='Under 10').save()
        association_ages(assn=asn, age_category='U11', age_category_description='Under 11').save()
        association_ages(assn=asn, age_category='U12', age_category_description='Under 12').save()
        association_ages(assn=asn, age_category='U13', age_category_description='Under 13').save()
        association_ages(assn=asn, age_category='U14', age_category_description='Under 14').save()
        association_ages(assn=asn, age_category='U15', age_category_description='Under 15').save()
        association_ages(assn=asn, age_category='U16', age_category_description='Under 16').save()
        association_ages(assn=asn, age_category='U17', age_category_description='Under 17').save()
        association_ages(assn=asn, age_category='U18', age_category_description='Under 18').save()
        association_ages(assn=asn, age_category='U19', age_category_description='Under 19').save()
        association_ages(assn=asn, age_category='U20', age_category_description='Under 20').save()
        association_ages(assn=asn, age_category='U21', age_category_description='Under 21').save()
        association_ages(assn=asn, age_category='U22', age_category_description='Under 22').save()
        association_ages(assn=asn, age_category='U23', age_category_description='Under 23').save()
        association_ages(assn=asn, age_category='U-5', age_category_description='Under 5').save()
        association_ages(assn=asn, age_category='U-6', age_category_description='Under 6').save()
        association_ages(assn=asn, age_category='U-7', age_category_description='Under 7').save()
        association_ages(assn=asn, age_category='U-8', age_category_description='Under 8').save()
        association_ages(assn=asn, age_category='U-9', age_category_description='Under 9').save()
        association_ages(assn=asn, age_category='U-10', age_category_description='Under 10').save()
        association_ages(assn=asn, age_category='U-11', age_category_description='Under 11').save()
        association_ages(assn=asn, age_category='U-12', age_category_description='Under 12').save()
        association_ages(assn=asn, age_category='U-13', age_category_description='Under 13').save()
        association_ages(assn=asn, age_category='U-14', age_category_description='Under 14').save()
        association_ages(assn=asn, age_category='U-15', age_category_description='Under 15').save()
        association_ages(assn=asn, age_category='U-16', age_category_description='Under 16').save()
        association_ages(assn=asn, age_category='U-17', age_category_description='Under 17').save()
        association_ages(assn=asn, age_category='U-18', age_category_description='Under 18').save()
        association_ages(assn=asn, age_category='U-19', age_category_description='Under 19').save()
        association_ages(assn=asn, age_category='U-20', age_category_description='Under 20').save()
        association_ages(assn=asn, age_category='U-21', age_category_description='Under 21').save()
        association_ages(assn=asn, age_category='U-22', age_category_description='Under 22').save()
        association_ages(assn=asn, age_category='U-23', age_category_description='Under 23').save()

        association_ages(assn=asn, age_category='Over 16', age_category_description='Over 16').save()
        association_ages(assn=asn, age_category='O16', age_category_description='Over 16').save()
        association_ages(assn=asn, age_category='O-16', age_category_description='Over 16').save()

        association_ages(assn=asn, age_category='Cadet', age_category_description='Cadet').save()
        association_ages(assn=asn, age_category='Junior', age_category_description='Junior').save()
        association_ages(assn=asn, age_category='Senior', age_category_description='Senior').save()
        association_ages(assn=asn, age_category='Veteran', age_category_description='Veteran').save()
        association_ages(assn=asn, age_category='Unknown', age_category_description='Unknown').save()

        association_types(assn=asn, type_category='Individual', type_category_description='Individual').save()
        association_types(assn=asn, type_category='Team', type_category_description='Team').save()
        association_types(assn=asn, type_category='Unknown', type_category_description='Unknown').save()

        association_discipline(assn=asn, discipline_name='Foil', discipline_description='Weapon: Foil').save()
        association_discipline(assn=asn, discipline_name='Epee', discipline_description='Weapon: Epee').save()
        association_discipline(assn=asn, discipline_name='Sabre', discipline_description='Weapon: Sabre').save()
        association_discipline(assn=asn, discipline_name='Unknown', discipline_description='Weapon: Unknown').save()

        association_genders(assn=asn, gender_name='Men', gender_description='Men').save()
        association_genders(assn=asn, gender_name='Women', gender_description='Women').save()
        association_genders(assn=asn, gender_name='Mixed', gender_description='Mixed').save()
        association_genders(assn=asn, gender_name='Unknown', gender_description='Unknown').save()

        if(1==1):

                association_countries.objects.create(assn=asn, country_three_letter='AFG', country_name='Afghanistan').save()
                association_countries.objects.create(assn=asn, country_three_letter='ALB', country_name='Albania').save()
                association_countries.objects.create(assn=asn, country_three_letter='ALG', country_name='Algeria').save()
                association_countries.objects.create(assn=asn, country_three_letter='ASA', country_name='American Samoa').save()
                association_countries.objects.create(assn=asn, country_three_letter='AND', country_name='Andorra').save()
                association_countries.objects.create(assn=asn, country_three_letter='ANG', country_name='Angola').save()
                association_countries.objects.create(assn=asn, country_three_letter='ANT', country_name='Antigua & Barbuda').save()
                association_countries.objects.create(assn=asn, country_three_letter='ARG', country_name='Argentina').save()
                association_countries.objects.create(assn=asn, country_three_letter='ARM', country_name='Armenia').save()
                association_countries.objects.create(assn=asn, country_three_letter='ARU', country_name='Aruba').save()
                association_countries.objects.create(assn=asn, country_three_letter='ART', country_name='Athlete Refugee Team').save()
                association_countries.objects.create(assn=asn, country_three_letter='ANZ', country_name='Australasia').save()
                association_countries.objects.create(assn=asn, country_three_letter='AUS', country_name='Australia').save()
                association_countries.objects.create(assn=asn, country_three_letter='AUT', country_name='Austria').save()
                association_countries.objects.create(assn=asn, country_three_letter='AZE', country_name='Azerbaijan').save()
                association_countries.objects.create(assn=asn, country_three_letter='BAH', country_name='Bahamas').save()
                association_countries.objects.create(assn=asn, country_three_letter='BRN', country_name='Bahrain').save()
                association_countries.objects.create(assn=asn, country_three_letter='BAN', country_name='Bangladesh').save()
                association_countries.objects.create(assn=asn, country_three_letter='BAR', country_name='Barbados').save()
                association_countries.objects.create(assn=asn, country_three_letter='BLR', country_name='Belarus').save()
                association_countries.objects.create(assn=asn, country_three_letter='BEL', country_name='Belgium').save()
                association_countries.objects.create(assn=asn, country_three_letter='BIZ', country_name='Belize').save()
                association_countries.objects.create(assn=asn, country_three_letter='BEN', country_name='Benin').save()
                association_countries.objects.create(assn=asn, country_three_letter='BER', country_name='Bermuda').save()
                association_countries.objects.create(assn=asn, country_three_letter='BHU', country_name='Bhutan').save()
                association_countries.objects.create(assn=asn, country_three_letter='BOH', country_name='Bohemia').save()
                association_countries.objects.create(assn=asn, country_three_letter='BOL', country_name='Bolivia').save()
                association_countries.objects.create(assn=asn, country_three_letter='BIH', country_name='Bosnia-Herzegovina').save()
                association_countries.objects.create(assn=asn, country_three_letter='BOT', country_name='Botswana').save()
                association_countries.objects.create(assn=asn, country_three_letter='BRA', country_name='Brazil').save()
                association_countries.objects.create(assn=asn, country_three_letter='IVB', country_name='British Virgin Islands').save()
                association_countries.objects.create(assn=asn, country_three_letter='BRU', country_name='Brunei').save()
                association_countries.objects.create(assn=asn, country_three_letter='BUL', country_name='Bulgaria').save()
                association_countries.objects.create(assn=asn, country_three_letter='BUR', country_name='Burkina Faso').save()
                association_countries.objects.create(assn=asn, country_three_letter='BDI', country_name='Burundi').save()
                association_countries.objects.create(assn=asn, country_three_letter='CAM', country_name='Cambodia').save()
                association_countries.objects.create(assn=asn, country_three_letter='CMR', country_name='Cameroon').save()
                association_countries.objects.create(assn=asn, country_three_letter='CAN', country_name='Canada').save()
                association_countries.objects.create(assn=asn, country_three_letter='CPV', country_name='Cape Verde').save()
                association_countries.objects.create(assn=asn, country_three_letter='CAY', country_name='Cayman Islands').save()
                association_countries.objects.create(assn=asn, country_three_letter='CAF', country_name='Central African Republic').save()
                association_countries.objects.create(assn=asn, country_three_letter='CHA', country_name='Chad').save()
                association_countries.objects.create(assn=asn, country_three_letter='CHI', country_name='Chile').save()
                association_countries.objects.create(assn=asn, country_three_letter='CHN', country_name='China').save()
                association_countries.objects.create(assn=asn, country_three_letter='COL', country_name='Colombia').save()
                association_countries.objects.create(assn=asn, country_three_letter='COM', country_name='Comoros').save()
                association_countries.objects.create(assn=asn, country_three_letter='CGO', country_name='Congo-Brazzaville').save()
                association_countries.objects.create(assn=asn, country_three_letter='COK', country_name='Cook Islands').save()
                association_countries.objects.create(assn=asn, country_three_letter='CRC', country_name='Costa Rica').save()
                association_countries.objects.create(assn=asn, country_three_letter='CIV', country_name='Cote d Ivoire').save()
                association_countries.objects.create(assn=asn, country_three_letter='CRO', country_name='Croatia').save()
                association_countries.objects.create(assn=asn, country_three_letter='CUB', country_name='Cuba').save()
                association_countries.objects.create(assn=asn, country_three_letter='CYP', country_name='Cyprus').save()
                association_countries.objects.create(assn=asn, country_three_letter='CZE', country_name='Czech Republic').save()
                association_countries.objects.create(assn=asn, country_three_letter='TCH', country_name='Czechoslovakia').save()
                association_countries.objects.create(assn=asn, country_three_letter='COD', country_name='Democratic Republic of the Congo').save()
                association_countries.objects.create(assn=asn, country_three_letter='DEN', country_name='Denmark').save()
                association_countries.objects.create(assn=asn, country_three_letter='DJI', country_name='Djibouti').save()
                association_countries.objects.create(assn=asn, country_three_letter='DMA', country_name='Dominica').save()
                association_countries.objects.create(assn=asn, country_three_letter='DOM', country_name='Dominican Republic').save()
                association_countries.objects.create(assn=asn, country_three_letter='TLS', country_name='East Timor').save()
                association_countries.objects.create(assn=asn, country_three_letter='ECU', country_name='Ecuador').save()
                association_countries.objects.create(assn=asn, country_three_letter='EGY', country_name='Egypt').save()
                association_countries.objects.create(assn=asn, country_three_letter='ESA', country_name='El Salvador').save()
                association_countries.objects.create(assn=asn, country_three_letter='GEQ', country_name='Equatorial Guinea').save()
                association_countries.objects.create(assn=asn, country_three_letter='ERI', country_name='Eritrea').save()
                association_countries.objects.create(assn=asn, country_three_letter='EST', country_name='Estonia').save()
                association_countries.objects.create(assn=asn, country_three_letter='SWZ', country_name='Eswatini').save()
                association_countries.objects.create(assn=asn, country_three_letter='ETH', country_name='Ethiopia').save()
                association_countries.objects.create(assn=asn, country_three_letter='FSM', country_name='Federal States of Micronesia').save()
                association_countries.objects.create(assn=asn, country_three_letter='FIJ', country_name='Fiji').save()
                association_countries.objects.create(assn=asn, country_three_letter='FIN', country_name='Finland').save()
                association_countries.objects.create(assn=asn, country_three_letter='FRA', country_name='France').save()
                association_countries.objects.create(assn=asn, country_three_letter='GAB', country_name='Gabon').save()
                association_countries.objects.create(assn=asn, country_three_letter='GAM', country_name='Gambia').save()
                association_countries.objects.create(assn=asn, country_three_letter='GEO', country_name='Georgia').save()
                association_countries.objects.create(assn=asn, country_three_letter='GDR', country_name='German Democratic Republic').save()
                association_countries.objects.create(assn=asn, country_three_letter='GER', country_name='Germany').save()
                association_countries.objects.create(assn=asn, country_three_letter='GHA', country_name='Ghana').save()
                association_countries.objects.create(assn=asn, country_three_letter='GBR', country_name='Great Britain').save()
                association_countries.objects.create(assn=asn, country_three_letter='GRE', country_name='Greece').save()
                association_countries.objects.create(assn=asn, country_three_letter='GRN', country_name='Grenada').save()
                association_countries.objects.create(assn=asn, country_three_letter='GUM', country_name='Guam').save()
                association_countries.objects.create(assn=asn, country_three_letter='GUA', country_name='Guatemala').save()
                association_countries.objects.create(assn=asn, country_three_letter='GUI', country_name='Guinea').save()
                association_countries.objects.create(assn=asn, country_three_letter='GBS', country_name='Guinea Bissau').save()
                association_countries.objects.create(assn=asn, country_three_letter='GUY', country_name='Guyana').save()
                association_countries.objects.create(assn=asn, country_three_letter='HAI', country_name='Haiti').save()
                association_countries.objects.create(assn=asn, country_three_letter='HON', country_name='Honduras').save()
                association_countries.objects.create(assn=asn, country_three_letter='HKG', country_name='Hong Kong').save()
                association_countries.objects.create(assn=asn, country_three_letter='HUN', country_name='Hungary').save()
                association_countries.objects.create(assn=asn, country_three_letter='ISL', country_name='Iceland').save()
                association_countries.objects.create(assn=asn, country_three_letter='IOA', country_name='Independent Olympic Athletes').save()
                association_countries.objects.create(assn=asn, country_three_letter='IND', country_name='India').save()
                association_countries.objects.create(assn=asn, country_three_letter='INA', country_name='Indonesia').save()
                association_countries.objects.create(assn=asn, country_three_letter='IRI', country_name='Iran').save()
                association_countries.objects.create(assn=asn, country_three_letter='IRQ', country_name='Iraq').save()
                association_countries.objects.create(assn=asn, country_three_letter='IRL', country_name='Ireland').save()
                association_countries.objects.create(assn=asn, country_three_letter='ISR', country_name='Israel').save()
                association_countries.objects.create(assn=asn, country_three_letter='ITA', country_name='Italy').save()
                association_countries.objects.create(assn=asn, country_three_letter='JAM', country_name='Jamaica').save()
                association_countries.objects.create(assn=asn, country_three_letter='JPN', country_name='Japan').save()
                association_countries.objects.create(assn=asn, country_three_letter='JOR', country_name='Jordan').save()
                association_countries.objects.create(assn=asn, country_three_letter='KAZ', country_name='Kazakhstan').save()
                association_countries.objects.create(assn=asn, country_three_letter='KEN', country_name='Kenya').save()
                association_countries.objects.create(assn=asn, country_three_letter='KIR', country_name='Kiribati').save()
                association_countries.objects.create(assn=asn, country_three_letter='KOS', country_name='Kosovo').save()
                association_countries.objects.create(assn=asn, country_three_letter='KUW', country_name='Kuwait').save()
                association_countries.objects.create(assn=asn, country_three_letter='KGZ', country_name='Kyrgyzstan').save()
                association_countries.objects.create(assn=asn, country_three_letter='LAO', country_name='Laos').save()
                association_countries.objects.create(assn=asn, country_three_letter='LAT', country_name='Latvia').save()
                association_countries.objects.create(assn=asn, country_three_letter='LIB', country_name='Lebanon').save()
                association_countries.objects.create(assn=asn, country_three_letter='LES', country_name='Lesotho').save()
                association_countries.objects.create(assn=asn, country_three_letter='LBR', country_name='Liberia').save()
                association_countries.objects.create(assn=asn, country_three_letter='LBA', country_name='Libya').save()
                association_countries.objects.create(assn=asn, country_three_letter='LBA', country_name='Libya').save()
                association_countries.objects.create(assn=asn, country_three_letter='LIE', country_name='Liechtenstein').save()
                association_countries.objects.create(assn=asn, country_three_letter='LTU', country_name='Lithuania').save()
                association_countries.objects.create(assn=asn, country_three_letter='LUX', country_name='Luxembourg').save()
                association_countries.objects.create(assn=asn, country_three_letter='MAD', country_name='Madagascar').save()
                association_countries.objects.create(assn=asn, country_three_letter='MAW', country_name='Malawi').save()
                association_countries.objects.create(assn=asn, country_three_letter='MAS', country_name='Malaysia').save()
                association_countries.objects.create(assn=asn, country_three_letter='MDV', country_name='Maldives').save()
                association_countries.objects.create(assn=asn, country_three_letter='MLI', country_name='Mali').save()
                association_countries.objects.create(assn=asn, country_three_letter='MLT', country_name='Malta').save()
                association_countries.objects.create(assn=asn, country_three_letter='MHL', country_name='Marshall Islands').save()
                association_countries.objects.create(assn=asn, country_three_letter='MTN', country_name='Mauritania').save()
                association_countries.objects.create(assn=asn, country_three_letter='MRI', country_name='Mauritius').save()
                association_countries.objects.create(assn=asn, country_three_letter='MEX', country_name='Mexico').save()
                association_countries.objects.create(assn=asn, country_three_letter='MDA', country_name='Moldova').save()
                association_countries.objects.create(assn=asn, country_three_letter='MON', country_name='Monaco').save()
                association_countries.objects.create(assn=asn, country_three_letter='MGL', country_name='Mongolia').save()
                association_countries.objects.create(assn=asn, country_three_letter='MNE', country_name='Montenegro').save()
                association_countries.objects.create(assn=asn, country_three_letter='MAR', country_name='Morocco').save()
                association_countries.objects.create(assn=asn, country_three_letter='MOZ', country_name='Mozambique').save()
                association_countries.objects.create(assn=asn, country_three_letter='MYA', country_name='Myanmar').save()
                association_countries.objects.create(assn=asn, country_three_letter='NAM', country_name='Namibia').save()
                association_countries.objects.create(assn=asn, country_three_letter='NRU', country_name='Nauru').save()
                association_countries.objects.create(assn=asn, country_three_letter='NEP', country_name='Nepal').save()
                association_countries.objects.create(assn=asn, country_three_letter='NED', country_name='Netherlands').save()
                association_countries.objects.create(assn=asn, country_three_letter='AHO', country_name='Netherlands Antilles').save()
                association_countries.objects.create(assn=asn, country_three_letter='NZL', country_name='New Zealand').save()
                association_countries.objects.create(assn=asn, country_three_letter='NCA', country_name='Nicaragua').save()
                association_countries.objects.create(assn=asn, country_three_letter='NIG', country_name='Niger').save()
                association_countries.objects.create(assn=asn, country_three_letter='NGR', country_name='Nigeria').save()
                association_countries.objects.create(assn=asn, country_three_letter='NBO', country_name='North Borneo').save()
                association_countries.objects.create(assn=asn, country_three_letter='PRK', country_name='North Korea').save()
                association_countries.objects.create(assn=asn, country_three_letter='MKD', country_name='North Macedonia').save()
                association_countries.objects.create(assn=asn, country_three_letter='YAR', country_name='North Yemen').save()
                association_countries.objects.create(assn=asn, country_three_letter='NOR', country_name='Norway').save()
                association_countries.objects.create(assn=asn, country_three_letter='OAR', country_name='Olympic Athletes from Russia').save()
                association_countries.objects.create(assn=asn, country_three_letter='OMA', country_name='Oman').save()
                association_countries.objects.create(assn=asn, country_three_letter='PAK', country_name='Pakistan').save()
                association_countries.objects.create(assn=asn, country_three_letter='PLW', country_name='Palau').save()
                association_countries.objects.create(assn=asn, country_three_letter='PLE', country_name='Palestine').save()
                association_countries.objects.create(assn=asn, country_three_letter='PAN', country_name='Panama').save()
                association_countries.objects.create(assn=asn, country_three_letter='PNG', country_name='Papua New Guinea').save()
                association_countries.objects.create(assn=asn, country_three_letter='PAR', country_name='Paraguay').save()
                association_countries.objects.create(assn=asn, country_three_letter='PER', country_name='Peru').save()
                association_countries.objects.create(assn=asn, country_three_letter='PHI', country_name='Philippines').save()
                association_countries.objects.create(assn=asn, country_three_letter='POL', country_name='Poland').save()
                association_countries.objects.create(assn=asn, country_three_letter='POR', country_name='Portugal').save()
                association_countries.objects.create(assn=asn, country_three_letter='PUR', country_name='Puerto Rico').save()
                association_countries.objects.create(assn=asn, country_three_letter='QAT', country_name='Qatar').save()
                association_countries.objects.create(assn=asn, country_three_letter='ROU', country_name='Romania').save()
                association_countries.objects.create(assn=asn, country_three_letter='RUS', country_name='Russia').save()
                association_countries.objects.create(assn=asn, country_three_letter='ROC', country_name='Russian Olympic Committee').save()
                association_countries.objects.create(assn=asn, country_three_letter='RWA', country_name='Rwanda').save()
                association_countries.objects.create(assn=asn, country_three_letter='SAA', country_name='Saar').save()
                association_countries.objects.create(assn=asn, country_three_letter='SKN', country_name='Saint Kitts and Nevis').save()
                association_countries.objects.create(assn=asn, country_three_letter='LCA', country_name='Saint Lucia').save()
                association_countries.objects.create(assn=asn, country_three_letter='VIN', country_name='Saint Vincent and Grenadines').save()
                association_countries.objects.create(assn=asn, country_three_letter='SAM', country_name='Samoa').save()
                association_countries.objects.create(assn=asn, country_three_letter='SMR', country_name='San Marino').save()
                association_countries.objects.create(assn=asn, country_three_letter='STP', country_name='Sao Tome and Principe').save()
                association_countries.objects.create(assn=asn, country_three_letter='KSA', country_name='Saudi Arabia').save()
                association_countries.objects.create(assn=asn, country_three_letter='SEN', country_name='Senegal').save()
                association_countries.objects.create(assn=asn, country_three_letter='SRB', country_name='Serbia').save()
                association_countries.objects.create(assn=asn, country_three_letter='SCG', country_name='Serbia and Montenegro').save()
                association_countries.objects.create(assn=asn, country_three_letter='SEY', country_name='Seychelles').save()
                association_countries.objects.create(assn=asn, country_three_letter='SLE', country_name='Sierra Leone').save()
                association_countries.objects.create(assn=asn, country_three_letter='SIN', country_name='Singapore').save()
                association_countries.objects.create(assn=asn, country_three_letter='SVK', country_name='Slovakia').save()
                association_countries.objects.create(assn=asn, country_three_letter='SLO', country_name='Slovenia').save()
                association_countries.objects.create(assn=asn, country_three_letter='SOL', country_name='Solomon Islands').save()
                association_countries.objects.create(assn=asn, country_three_letter='SOM', country_name='Somalia').save()
                association_countries.objects.create(assn=asn, country_three_letter='RSA', country_name='South Africa').save()
                association_countries.objects.create(assn=asn, country_three_letter='KOR', country_name='South Korea').save()
                association_countries.objects.create(assn=asn, country_three_letter='SSD', country_name='South Sudan').save()
                association_countries.objects.create(assn=asn, country_three_letter='VNM', country_name='South Vietnam').save()
                association_countries.objects.create(assn=asn, country_three_letter='YMD', country_name='South Yemen').save()
                association_countries.objects.create(assn=asn, country_three_letter='URS', country_name='Soviet Union').save()
                association_countries.objects.create(assn=asn, country_three_letter='ESP', country_name='Spain').save()
                association_countries.objects.create(assn=asn, country_three_letter='SRI', country_name='Sri Lanka').save()
                association_countries.objects.create(assn=asn, country_three_letter='SUD', country_name='Sudan').save()
                association_countries.objects.create(assn=asn, country_three_letter='SUR', country_name='Suriname').save()
                association_countries.objects.create(assn=asn, country_three_letter='SWE', country_name='Sweden').save()
                association_countries.objects.create(assn=asn, country_three_letter='SUI', country_name='Switzerland').save()
                association_countries.objects.create(assn=asn, country_three_letter='SYR', country_name='Syria').save()
                association_countries.objects.create(assn=asn, country_three_letter='TPE', country_name='Taiwan').save()
                association_countries.objects.create(assn=asn, country_three_letter='TJK', country_name='Tajikistan').save()
                association_countries.objects.create(assn=asn, country_three_letter='TAN', country_name='Tanzania').save()
                association_countries.objects.create(assn=asn, country_three_letter='ROT', country_name='Team of Refugee Olympic Athletes').save()
                association_countries.objects.create(assn=asn, country_three_letter='THA', country_name='Thailand').save()
                association_countries.objects.create(assn=asn, country_three_letter='TOG', country_name='Togo').save()
                association_countries.objects.create(assn=asn, country_three_letter='TGA', country_name='Tonga').save()
                association_countries.objects.create(assn=asn, country_three_letter='TTO', country_name='Trinidad and Tobago').save()
                association_countries.objects.create(assn=asn, country_three_letter='TUN', country_name='Tunisia').save()
                association_countries.objects.create(assn=asn, country_three_letter='TUR', country_name='Turkey').save()
                association_countries.objects.create(assn=asn, country_three_letter='TKM', country_name='Turkmenistan').save()
                association_countries.objects.create(assn=asn, country_three_letter='TUV', country_name='Tuvalu').save()
                association_countries.objects.create(assn=asn, country_three_letter='UGA', country_name='Uganda').save()
                association_countries.objects.create(assn=asn, country_three_letter='UKR', country_name='Ukraine').save()
                association_countries.objects.create(assn=asn, country_three_letter='EUN', country_name='Unified Team').save()
                association_countries.objects.create(assn=asn, country_three_letter='UAE', country_name='United Arab Emirates').save()
                association_countries.objects.create(assn=asn, country_three_letter='UAR', country_name='United Arab Republic').save()
                association_countries.objects.create(assn=asn, country_three_letter='UAR', country_name='United Arab Republic').save()
                association_countries.objects.create(assn=asn, country_three_letter='USA', country_name='United States of America').save()
                association_countries.objects.create(assn=asn, country_three_letter='URU', country_name='Uruguay').save()
                association_countries.objects.create(assn=asn, country_three_letter='UZB', country_name='Uzbekistan').save()
                association_countries.objects.create(assn=asn, country_three_letter='VAN', country_name='Vanuatu').save()
                association_countries.objects.create(assn=asn, country_three_letter='VEN', country_name='Venezuela').save()
                association_countries.objects.create(assn=asn, country_three_letter='VIE', country_name='Vietnam').save()
                association_countries.objects.create(assn=asn, country_three_letter='ISV', country_name='Virgin Islands').save()
                association_countries.objects.create(assn=asn, country_three_letter='FRG', country_name='West Germany').save()
                association_countries.objects.create(assn=asn, country_three_letter='BWI', country_name='West Indies Federation').save()
                association_countries.objects.create(assn=asn, country_three_letter='YEM', country_name='Yemen').save()
                association_countries.objects.create(assn=asn, country_three_letter='YUG', country_name='Yugoslavia').save()
                association_countries.objects.create(assn=asn, country_three_letter='ZAM', country_name='Zambia').save()
                association_countries.objects.create(assn=asn, country_three_letter='ZIM', country_name='Zimbabwe').save()

        return(asn)


def BF_daily_validate_current_rating(f, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("\nBF_daily_validate_current_rating: " + str(timezone.now()) + "\n")

        asn = get_association(None, "British Fencing", False)
        assn_recs = association_members.objects.filter(assn = asn).values_list('assn_member_full_name', flat=True)
        disciplines = association_discipline.objects.filter(assn = asn).exclude(discipline_name = 'Unknown')
        if os.environ.get("BF_RATING_TIME_LENGTH_YEARS") is not None:
                rt_years = int(os.environ.get("BF_RATING_TIME_LENGTH_YEARS"))
        else:
                rt_years = 0
        oldest_event_start_date = timezone.now() - relativedelta(years=rt_years)
#        oldest_event_start_date = timezone.now() - relativedelta(years=2)

#        if(1==1):
#                amr = get_assn_member_record(None, asn, assn_recs, '105955', 'BARKER Christopher', None, None, False)
#                c_ratings = BF_get_all_assn_member_extra_current_ratings(f, amr, True)
#                for x in c_ratings:
#                        print(x)

        for amr in association_members.objects.filter(assn = asn):        
                if(DEBUG_WRITE):
                        f.write("  Working on: " + str(amr.assn_member_full_name) + " " + str(amr.assn_member_identifier) + " " + str(timezone.now()) + "\n")
                uc_ef = association_member_extra_fields.objects.filter(
                        assn_member=amr, assn_member_field_name='Current Rating').delete()
                last_events, participating_disciplines = BF_athlete_get_last_events(amr, 10000)
                f.write("   Total Events: " + str(len(last_events)) + " " + str(timezone.now()) + "\n")
                for q in disciplines:
                        best_rating = 'Z'
                        best_year = 99
                        for x in last_events[::-1]:
#                                print (x)
                                if(q == x[9]):
#                                        print("inside")
                                        try:
                                                eve = events.objects.get(ev_number = x[12])
                                        except:
                                                if(DEBUG_WRITE):
                                                        f.write("ERROR:  Cannot find event: " + str(x) + "\n")
                                        else:
                                                if(eve.ev_start_date >= oldest_event_start_date):
                                                        new_rating = x[7][:1]
                                                        new_year = int(x[8])
                                                        if(DEBUG_WRITE):
                                                                f.write("    Working Event: " + str(eve.ev_name)  + str(eve.ev_start_date)  + str(oldest_event_start_date) + "\n")
                                                        if((new_rating < best_rating) or (new_rating == best_rating and new_year > best_year)):
                                                                if(DEBUG_WRITE):
                                                                        f.write("      Better Rating:  Orig: " + str(best_rating) + " " + str(best_year) + " Found: " + str(new_rating) + " " + str(new_year) + "\n")
                                                                BF_update_or_create_current_rating(f, amr, eve.ev_assn_discipline.discipline_name, x[7], eve.ev_start_date, DEBUG_WRITE)
                                                                best_year = new_year
                                                                best_rating = new_rating
                                                else:
                                                        if(DEBUG_WRITE):
                                                                f.write("      Skipping Event: " + str(eve.ev_name)  + str(eve.ev_start_date)  + str(oldest_event_start_date) + "\n")

#                c_ratings = BF_get_all_assn_member_extra_current_ratings(f, amr, True)
#                for x in c_ratings:
#                        print(x)
        if(DEBUG_WRITE):
                f.write("       COMPLETE: BF_daily_validate_current_rating: " + str(timezone.now()) + "\n")


