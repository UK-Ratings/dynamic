#!/usr/bin/env python3

from assn_mgr.models import *
from users.models import User

from integrations.models import *
from tourneys.models import *

from scripts.x_helper_functions import *
from scripts.x_helper_assn_specific import *
from scripts import y_admin_key_tables_load

from django.utils import timezone
from django.db import transaction
from django.db.models import F
import os
import inspect
import re

from dotenv import load_dotenv
from django.conf import settings

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")



def Create_FTL_Tournament_Event_Round_Pool_Assignments(f, load_tourney_pool, tourney_pool, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("         Create_FTL_Tournament_Event_Round_Pool_Assignments: " 
                + " load_pool_name:" + str(load_tourney_pool.number) 
                + " tourney_pool: " + str(tourney_pool.erpd_number) 
                + " " + str(timezone.now()) + "\n")

    erps = event_round_pool_scores.objects.filter(erps_pool_details=tourney_pool).values(
        'erps_left_member_num', 'erps_left_name', 'erps_right_member_num', 'erps_right_name'
    )
    
    combined_list = [
        (erp['erps_left_member_num'], erp['erps_left_name']) for erp in erps
    ] + [
        (erp['erps_right_member_num'], erp['erps_right_name']) for erp in erps
    ]

    unique_list = list(set(combined_list))

    if DEBUG_WRITE:
        f.write("Unique Pool Assignments: " + str(len(unique_list)) + " - " + str(timezone.now()) + "\n")

    updates = []
    for x in unique_list:
        if DEBUG_WRITE:
            f.write("         Working Pool Assignments: " + str(x[0]) + " - " + str(x[1]) + " - " + str(timezone.now()) + "\n")
        erpa, created = event_round_pool_assignments.objects.update_or_create(
            erpa_pool_details=tourney_pool,
            erpa_member_num=x[0],
            erpa_name=x[1],
            defaults={
                'erpa_date_updated': timezone.now(),
                'erpa_date_added': timezone.now()
            }
        )
        updates.append(erpa)

    # Bulk update the records
    if updates:
        with transaction.atomic():
            event_round_pool_assignments.objects.bulk_update(updates, ['erpa_date_updated', 'erpa_date_added'])

    if DEBUG_WRITE:
        f.write("    Completed Create_FTL_Tournament_Event_Round_Pool_Assignments: " + str(timezone.now()) + "\n")
def Process_FTL_Tournament_Event_Round_Pool_Scores(f, load_tourney_pool, tourney_pool, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("         Process_FTL_Tournament_Event_Round_Pool_Scores: " 
                + " load_pool_name:" + str(load_tourney_pool.number) 
                + " tourney_pool: " + str(tourney_pool.erpd_number) 
                + " " + str(load_tourney_pool) 
                + " " + str(timezone.now()) + "\n")

    updates = []
    for z in load_ftl_round_pool_scores.objects.filter(pool_id_index=load_tourney_pool):
        if DEBUG_WRITE:
            f.write("         Working Pool Scores: " + str(z.left_name) + " - " + str(z.right_name) + " - " + str(z.number) + " - " + str(timezone.now()) + "\n")
        erps, created = event_round_pool_scores.objects.update_or_create(
            erps_pool_details=tourney_pool,
            erps_number=z.number,
            defaults={
                'erps_date_updated': timezone.now(),
                'erps_date_added': timezone.now(),
                'erps_left_position': z.left_position,
                'erps_left_member_num': z.left_member_num,
                'erps_left_name': z.left_name,
                'erps_left_score': z.left_score,
                'erps_right_position': z.right_position,
                'erps_right_member_num': z.right_member_num,
                'erps_right_name': z.right_name,
                'erps_right_score': z.right_score,
                'erps_winner_member_num': z.winner_member_num,
                'erps_winner_name': z.winner_name
            }
        )
        updates.append(erps)

    # Bulk update the records
    if updates:
        with transaction.atomic():
            event_round_pool_scores.objects.bulk_update(updates, [
                'erps_date_updated', 'erps_date_added', 'erps_left_position', 'erps_left_member_num',
                'erps_left_name', 'erps_left_score', 'erps_right_position', 'erps_right_member_num',
                'erps_right_name', 'erps_right_score', 'erps_winner_member_num', 'erps_winner_name'
            ])

    if DEBUG_WRITE:
        f.write("    Completed Process_FTL_Tournament_Event_Round_Pool_Scores: " + str(timezone.now()) + "\n")
def Process_FTL_Tournament_Event_Round_Pool_Details(f, load_tourney_round, tourney_round, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("         Process_FTL_Tournament_Event_Round_Pool_Details: " 
                + " load_tourney_name:" + str(load_tourney_round.event_id_index.name) 
                + " tourney_event: " + str(tourney_round.er_event.ev_name) 
                + " " + str(timezone.now()) + "\n")

    updates = []
    for z in load_ftl_pool_round_pool.objects.filter(round_id_index=load_tourney_round):
        if DEBUG_WRITE:
            f.write("         Working Round Details: " + str(z.number) + " - " + str(z.size) + " - " + str(z.finished) + " - " + str(timezone.now()) + "\n")
        try:
            event_round_pool_details.objects.get(erpd_round=tourney_round, erpd_number=z.number)
        except event_round_pool_details.DoesNotExist:
            p_number = base_get_next_system_value('next_event_pool_id')
        else:
            ev = event_round_pool_details.objects.get(erpd_round=tourney_round, erpd_number=z.number)
            p_number = ev.erpd_pool_num

        erpd, created = event_round_pool_details.objects.update_or_create(
            erpd_round=tourney_round,
            erpd_pool_num=p_number,
            erpd_number=z.number,
            defaults={
                'erpd_date_updated': timezone.now(),
                'erpd_date_added': timezone.now(),
                'erpd_pool_identifier': z.pool_id,
                'erpd_size': z.size,
                'erpd_finished': z.finished,
                'erpd_strip': z.strip,
                'erpd_starttime': z.starttime,
                'erpd_starttime_time': z.starttime_time
            }
        )
        updates.append(erpd)
        Process_FTL_Tournament_Event_Round_Pool_Scores(f, z, erpd, DEBUG_WRITE)
        Create_FTL_Tournament_Event_Round_Pool_Assignments(f, z, erpd, DEBUG_WRITE)

    # Bulk update the records
    if updates:
        with transaction.atomic():
            event_round_pool_details.objects.bulk_update(updates, [
                'erpd_date_updated', 'erpd_date_added', 'erpd_pool_identifier', 'erpd_size',
                'erpd_finished', 'erpd_strip', 'erpd_starttime', 'erpd_starttime_time'
            ])

    if DEBUG_WRITE:
        f.write("    Completed Process_FTL_Tournament_Event_Round_Pool_Details: " + str(timezone.now()) + "\n")
def Process_FTL_Tournament_Event_Round_Elim_Scores(f, load_tourney_round, tourney_round, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("         Process_FTL_Tournament_Event_Round_Elim_Scores: " 
                + " load_tourney_name:" + str(load_tourney_round.event_id_index.name) 
                + " tourney_event: " + str(tourney_round.er_event.ev_name) 
                + " " + str(tourney_round.er_r_number)
                + " " + str(timezone.now()) + "\n")

    event_round_pool_elimination_scores.objects.filter(erpes_round=tourney_round).delete()
    
    updates = []
    for z in load_ftl_elimination_scores.objects.filter(round_id_index=load_tourney_round):
        if DEBUG_WRITE:
            f.write("         Working Round Elimination Scores: " + str(z.table) + " - " + str(z.number) + " - " + str(z.strip) + " - " + str(timezone.now()) + "\n")
        ev_round, created = event_round_pool_elimination_scores.objects.update_or_create(
            erpes_round=tourney_round,
            erpes_table=z.table,
            erpes_number=z.number,
            erpes_strip=z.strip,
            defaults={
                'erpes_date_updated': timezone.now(),
                'erpes_date_added': timezone.now(),
                'erpes_stime': z.stime,
                'erpes_score': z.score,
                'erpes_left_seed': z.left_seed,
                'erpes_left_member_num': z.left_member_num,
                'erpes_left_name': z.left_name,
                'erpes_right_seed': z.right_seed,
                'erpes_right_member_num': z.right_member_num,
                'erpes_right_name': z.right_name,
                'erpes_winner_member_num': z.winner_member_num,
                'erpes_winner_name': z.winner_name
            }
        )
        updates.append(ev_round)

    # Bulk update the records
    if updates:
        with transaction.atomic():
            event_round_pool_elimination_scores.objects.bulk_update(updates, [
                'erpes_date_updated', 'erpes_date_added', 'erpes_stime', 'erpes_score', 'erpes_left_seed',
                'erpes_left_member_num', 'erpes_left_name', 'erpes_right_seed', 'erpes_right_member_num',
                'erpes_right_name', 'erpes_winner_member_num', 'erpes_winner_name'
            ])

    if DEBUG_WRITE:   
        f.write("    Completed Process_FTL_Tournament_Event_Round_Elim_Scores: " + str(timezone.now()) + "\n")
def Process_FTL_Tournament_Event_Round_Pool_Results(f, load_tourney_round, tourney_round, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("         Process_FTL_Tournament_Event_Round_Pool_Results: " 
                + " load_tourney_name:" + str(load_tourney_round.event_id_index.name) 
                + " tourney_event: " + str(tourney_round.er_event.ev_name) 
                + " " + str(tourney_round.er_round_num)
                + " " + str(timezone.now()) + "\n")

    updates = []
    for z in load_ftl_round_pool_results.objects.filter(round_id_index=load_tourney_round):
        if DEBUG_WRITE:
            f.write("         Working Pool Results: " + str(z.name) + " - " + str(z.place) + " - " + str(z.v) + " - " + str(timezone.now()) + "\n")
        
        erpr, created = event_round_pool_results.objects.update_or_create(
            erpr_round=tourney_round,
            erpr_place=z.place,
            erpr_name=z.name,
            defaults={
                'erpr_date_updated': timezone.now(),
                'erpr_date_added': timezone.now(),
                'erpr_tie': z.tie,
                'erpr_v': z.v,
                'erpr_m': z.m,
                'erpr_vm': z.vm,
                'erpr_ts': z.ts,
                'erpr_tr': z.tr,
                'erpr_ind': z.ind,
                'erpr_prediction': z.prediction,
                'erpr_member_num': z.member_num,
                'erpr_division': z.division,
                'erpr_country': z.country,
                'erpr_club1': z.club1,
                'erpr_club2': z.club2
            }
        )
        updates.append(erpr)

    # Bulk update the records
    if updates:
        with transaction.atomic():
            event_round_pool_results.objects.bulk_update(updates, [
                'erpr_date_updated', 'erpr_date_added', 'erpr_tie', 'erpr_v', 'erpr_m', 'erpr_vm',
                'erpr_ts', 'erpr_tr', 'erpr_ind', 'erpr_prediction', 'erpr_member_num', 'erpr_division',
                'erpr_country', 'erpr_club1', 'erpr_club2'
            ])

    if DEBUG_WRITE:
        f.write("    Completed Process_FTL_Tournament_Event_Round_Pool_Results: " + str(timezone.now()) + "\n")
def Process_FTL_Tournament_Event_Round_Seeding(f, load_tourney_round, tourney_round, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("         Process_FTL_Tournament_Event_Round_Seeding: " 
                + " load_tourney_name:" + str(load_tourney_round.event_id_index.name) 
                + " tourney_event: " + str(tourney_round.er_event.ev_name) 
                + " " + str(timezone.now()) + "\n")

    event_round_seeding.objects.filter(ers_round=tourney_round).delete()
    
    updates = []
    for z in load_ftl_round_seeding.objects.filter(round_id_index=load_tourney_round):
        if DEBUG_WRITE:
            f.write("         Working Round Seeding: " + str(z.name) + " - " + str(z.seed) + " - " + str(z.member_num) + " - " + str(timezone.now()) + "\n")
        
        see_round, created = event_round_seeding.objects.update_or_create(
            ers_round=tourney_round,
            ers_seed=z.seed,
            ers_name=z.name,
            defaults={
                'ers_date_updated': timezone.now(),
                'ers_date_added': timezone.now(),
                'ers_member_num': z.member_num,
                'ers_division': z.division,
                'ers_country': z.country,
                'ers_club1': z.club1,
                'ers_club2': z.club2,
                'ers_rating': z.rating,
                'ers_exempt': z.exempt,
                'ers_excluded': z.excluded,
                'ers_no_show': z.no_show,
                'ers_eliminated': z.eliminated,
                'ers_advanced': z.advanced,
                'ers_status': z.status
            }
        )
        updates.append(see_round)

    # Bulk update the records
    if updates:
        with transaction.atomic():
            event_round_seeding.objects.bulk_update(updates, [
                'ers_date_updated', 'ers_date_added', 'ers_member_num', 'ers_division', 'ers_country',
                'ers_club1', 'ers_club2', 'ers_rating', 'ers_exempt', 'ers_excluded', 'ers_no_show',
                'ers_eliminated', 'ers_advanced', 'ers_status'
            ])

    if DEBUG_WRITE:
        f.write("    Completed Process_FTL_Tournament_Event_Round_Seeding: " + str(timezone.now()) + "\n")
def Process_FTL_Tournament_Event_Rounds(f, load_tourney_event, tourney_event, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("         Process_FTL_Tournament_Event_Rounds: " 
                + " load_tourney_name:" + str(load_tourney_event.name) 
                + " tourney_event: " + str(tourney_event.ev_name) 
                + " " + str(timezone.now()) + "\n")

    for z in load_ftl_event_rounds.objects.filter(event_id_index=load_tourney_event):
        if DEBUG_WRITE:
            f.write("         Working Round: " + z.round_id + " - " + z.r_number + " - " + z.r_type + " - " + str(timezone.now()) + "\n")
        ev_round = get_event_round(f, DEBUG_WRITE, tourney_event, z.r_number, None)
        ev_round = update_or_create_event_round(f, DEBUG_WRITE, tourney_event, ev_round, z.round_id, 
                                                z.r_number, z.r_type, z.r_finished)
        Process_FTL_Tournament_Event_Round_Seeding(f, z, ev_round, False)
        Process_FTL_Tournament_Event_Round_Pool_Results(f, z, ev_round, False)
        Process_FTL_Tournament_Event_Round_Elim_Scores(f, z, ev_round, False)
        Process_FTL_Tournament_Event_Round_Pool_Details(f, z, ev_round, False)
        populate_initial_elim_scores(ev_round)
    if DEBUG_WRITE:
        f.write("    Completed Process_FTL_Tournament_Event_Rounds: " + str(timezone.now()) + "\n")
def Process_FTL_Tournament_Event_Final_Results(f, asn, assn_recs, load_tourney_event, tourney_event, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("                  Process_FTL_Tournament_Event_Final_Results: " 
                + " load_tourney_name:" + str(load_tourney_event.name) 
                + " tourney_event: " + str(tourney_event.ev_name) 
                + " " + str(timezone.now()) + "\n")
    event_final_results.objects.filter(efr_event=tourney_event).delete()
    
    updates = []
    for x in load_ftl_event_final_results.objects.filter(event_id_index=load_tourney_event):
        dig = re.sub(r'[a-zA-Z]', '', x.place)
        pos = int(dig) if dig.isdigit() else 999

        if DEBUG_WRITE:
            f.write(str(x.name) + " " + str(x.club1) + " " + str(x.member_num) + " " + str(x.place) + " " + str(pos) + "\n")

        amn = get_assn_member_record(f, asn, assn_recs, x.member_num, x.name, "", "", False)
        mem_num = amn.assn_member_number if amn else None
        mem_ident = amn.assn_member_identifier if amn else x.member_num

        if DEBUG_WRITE and amn:
            f.write(str(x.name) + " " + str(x.club1) + " " + str(x.member_num) + " " + str(x.place) + " " + str(pos) 
                    + str(amn.assn_member_number) + " " + str(amn.assn_member_full_name) + " BF identifier:" + str(amn.assn_member_identifier) + "\n")
        elif DEBUG_WRITE:
            f.write("get_assn_member_record returned None\n")

        efr = update_or_create_event_final_result(f, False, tourney_event, None, pos, x.name, x.club1, mem_ident, mem_num)
        updates.append(efr)

    # Bulk update the records
    if updates:
        with transaction.atomic():
            event_final_results.objects.bulk_update(updates, [
                'efr_event', 'efr_final_position', 'efr_given_name', 'efr_given_club', 'efr_given_member_identifier', 'efr_assn_member_number'
            ])

    if DEBUG_WRITE:
        f.write("    Completed Process_FTL_Tournament_Event_Final_Results: " + str(timezone.now()) + "\n")
def Process_FTL_Tournament_Events(f, asn, assn_recs, ftl_tourney, tourney, DEBUG_WRITE, event_found_results):
    f.write("   Process_FTL_Tournament_Events: " + str(ftl_tourney.name) + " " + str(timezone.now()) + "\n")

    for y in load_ftl_tournament_events.objects.filter(tournament_id_index=ftl_tourney):
        for z in event_found_results:
            if not z[0] and z[1] == y.name:
                if DEBUG_WRITE:
                    f.write("      Working Event: " + y.event_id + " - " + y.name + " - " + str(timezone.now()) + "\n")
                es = "Upcoming"
                if y.start_date:
                    es = "Active"
                if y.finished:
                    es = "Completed"
                found_event = get_event(f, DEBUG_WRITE, tourney, y.name, None)

                if not found_event:
                    if DEBUG_WRITE:
                        f.write("         No Event Event - Creating: " + str(timezone.now()) + "\n")
                    e_disp = get_assn_discipline_from_text(f, tourney.tourney_assn, y.name, tourney.tourney_name, "", False)
                    e_gen = get_assn_gender_from_text(f, tourney.tourney_assn, y.name, tourney.tourney_name, "", False)
                    e_type = get_assn_type_from_text(f, tourney.tourney_assn, y.name, tourney.tourney_name, "", False)
                    e_ages = get_assn_ages_from_text(f, tourney.tourney_assn, y.name, tourney.tourney_name, "", False)
                    if DEBUG_WRITE:
                        f.write("         Association Discipline: " + e_disp.discipline_name + " " + str(timezone.now()) + "\n")
                        f.write("         Association Gender: " + e_gen.gender_name + " " + str(timezone.now()) + "\n")
                        f.write("         Association Type: " + e_type.type_category + " " + str(timezone.now()) + "\n")
                        f.write("         Association Ages: " + e_ages.age_category + " " + str(timezone.now()) + "\n")
                    if len(y.s_time) > 0:
                        datetime_str = y.s_date + " " + y.s_time
                        datetime_format = '%Y-%m-%d %H:%M'
                        sdatetime = datetime.strptime(datetime_str, datetime_format)
                        sdatetime_aware = timezone.make_aware(sdatetime, timezone.get_default_timezone())
                    else:
                        datetime_str = y.s_date
                        datetime_format = '%Y-%m-%d'
                        sdatetime = datetime.strptime(datetime_str, datetime_format)
                        sdatetime_aware = timezone.make_aware(sdatetime, timezone.get_default_timezone())

                    found_event = update_or_create_event(f, DEBUG_WRITE, tourney, None, y.name,
                                                         es, e_type, e_disp, e_gen, e_ages, sdatetime_aware)
                else:
                    if DEBUG_WRITE:
                        f.write("         Found Event: " + str(found_event.ev_number) + " - " + found_event.ev_name + " - " + str(timezone.now()) + "\n")
                if found_event:
                    Process_FTL_Tournament_Event_Final_Results(f, asn, assn_recs, y, found_event, DEBUG_WRITE)
                    Process_FTL_Tournament_Event_Rounds(f, y, found_event, DEBUG_WRITE)
                    populate_elimination_match_brackets(f, found_event, DEBUG_WRITE)
                else:
                    f.write("ERROR-EVENT NOT FOUND OR CREATED - Process_FTL_Tournament_Events " + str(timezone.now()) + "\n")
    f.write("    Completed Process_FTL_Tournament_Events: " + str(timezone.now()) + "\n")
def Process_FTL_Tournament(f, asn, assn_recs, x, DEBUG_WRITE, event_found_results):
        f.write("Process_FTL_Tournament: " + " - " + x.name + " - " + x.location + " - " + x.start + " - " + str(timezone.now()) + "\n")
        sys_user = get_system_process_user()
        if os.environ.get("FTL_TOURNAMENT_URL") is not None:
                ftl_tourney_url = os.environ.get("FTL_TOURNAMENT_URL")
        else:
                ftl_tourney_url = None

#        print("   Working Tournament: " + x.tournament_id + " - " + x.name + " - " + x.location + " - " + x.start + " - " + x.end + " " + str(timezone.now()) + "\n")
        if(DEBUG_WRITE):
                f.write("   Working Tournament: " + x.tournament_id + " - " + x.name + " - " + x.location + " - " + x.start + " - " + x.end + " " + str(timezone.now()) + "\n")
        tourney_url = ftl_tourney_url + x.tournament_id + "#today"
        if(x.end_date is not None):
                ts = "Completed"
        else:
                ts = "Active"
        found_tourney = get_tournament(f, DEBUG_WRITE, None, x.name, asn, x.start_date, True, 'FencingTimeLive')
        if found_tourney is None:
                f.write("                             Process_FTL_Tournament: Could not find tournament" + " " + str(x.name) + " " + str(x.start_date) + " " + str(x.id) + " " + str(timezone.now()) + "\n")
        else:
                if(DEBUG_WRITE):
                        f.write("                             Found Tournament: " + str(found_tourney.tourney_name) + " " + str(found_tourney.tourney_status) + " " + str(timezone.now()) + "\n")

        tourney_url = ftl_tourney_url + x.tournament_id + "#today"
        tourney = update_or_create_tournament(f, DEBUG_WRITE, found_tourney, asn, 
                                                        x.name, ts, x.start_date, x.end_date, 
                                                        x.start_date, tourney_url, None, 
                                                        None, False, None, None,
                                                        'FencingTimeLive', False, sys_user)
        if(DEBUG_WRITE):
                f.write("      New Tournament: " + str(tourney.tourney_number) + " - " + tourney.tourney_name + " - " + str(timezone.now()) + "\n")
        Process_FTL_Tournament_Events(f,  asn, assn_recs, x, tourney, DEBUG_WRITE, event_found_results)
        f.write("Completed Process_FTL_Tournament: " + str(timezone.now()) + "\n")

def Process_S80_Tournament_Event_Fencers(f, asn, assn_recs, s80_tourney_event, eve, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("                  Process_S80_Tournament_Event_Fencers: s80_tourney_name:" 
                + str(s80_tourney_event.competition.name) + " " + str(s80_tourney_event.name) 
                + str(timezone.now()) + "\n")
    
    event_final_results.objects.filter(efr_event=eve).delete()
    
    updates = []
    for y in load_s80_fencing_fencing_results.objects.filter(event=s80_tourney_event):
        efr = get_event_final_result(f, DEBUG_WRITE, eve, clean_position(y.rank), y.name)
        amn = get_assn_member_record(f, asn, assn_recs, y.identifier, y.name, "", "", False)
        mem_num = amn.assn_member_number if amn else None
        mem_ident = amn.assn_member_identifier if amn else y.identifier
        efr = update_or_create_event_final_result(f, DEBUG_WRITE, eve, None, clean_position(y.rank), y.name, "", mem_ident, mem_num)
        updates.append(efr)
    
    # Bulk update the records
    if updates:
        with transaction.atomic():
            event_final_results.objects.bulk_update(updates, [
                'efr_event', 'efr_final_position', 'efr_given_name', 'efr_given_club', 'efr_given_member_identifier', 'efr_assn_member_number'
            ])

    if DEBUG_WRITE:
        f.write("                   Complete Process_S80_Tournament_Event_Fencers: upcoming_tourney_name:" 
                + " " + str(eve.ev_tourney.tourney_name) 
                + " " + str(eve.ev_name) + " " + str(timezone.now()) + "\n")
def Process_S80_Tournament_Events(f, asn, assn_recs, s80_tourney, tourney, DEBUG_WRITE, event_found_results):
    if DEBUG_WRITE:
        f.write("            Process_S80_Tournament_Events: s80_tourney_name:" 
                + str(s80_tourney.name) 
                + " " + str(s80_tourney.calced_endDate) 
                + " " + str(timezone.now()) + "\n")

    for x in load_s80_fencing_events.objects.filter(competition=s80_tourney):
        for y in event_found_results:
            if not y[0] and y[1] == x.name:
                if DEBUG_WRITE:
                    f.write("               Process_S80_Tournament_Events: " + str(x.name) 
                            + "   Age Group: " + str(x.agegroup) 
                            + "   Weapon: " + str(x.weapon) + " " + str(timezone.now()) + "\n")
                
                discipline = get_assn_discipline_from_text(f, tourney.tourney_assn, x.weapon, x.name, tourney.tourney_name, False)
                gender = get_assn_gender_from_text(f, tourney.tourney_assn, x.name, tourney.tourney_name, "", False)
                e_type = get_assn_type_from_text(f, tourney.tourney_assn, 'individual', x.name, tourney.tourney_name, False)
                ages = get_assn_ages_from_text(f, tourney.tourney_assn, x.agegroup, x.name, tourney.tourney_name, False)

                lookup_msg = "                  lookups: " + str(discipline.discipline_description) \
                                + "-" + str(gender.gender_description) \
                                + "-" + str(e_type.type_category_description) \
                                + "-" + str(ages.age_category_description) \
                                + " at " + str(timezone.now())
                if "Unknown" in lookup_msg:
                    f.write("WARNING: " + lookup_msg + "\n")
                
                event = update_or_create_event(f, False, tourney, None, 
                                x.name, 'Completed', e_type, discipline, gender, ages, tourney.tourney_start_date)
                Process_S80_Tournament_Event_Fencers(f, asn, assn_recs, x, event, DEBUG_WRITE)
                
                if DEBUG_WRITE:
                    f.write("                Complete Process_S80_Tournament_Events: \n") 

    if DEBUG_WRITE:
        f.write("             Complete Process_S80_Tournament_Events: " + " " + str(s80_tourney.name) + " " + str(s80_tourney.calced_endDate) + " " + str(timezone.now()) + "\n")
def Process_S80_Tournament(f, asn, s80_tourney, DEBUG_WRITE, sys_user, assn_recs, event_found_results):
        if(DEBUG_WRITE):
                f.write("      Process_S80_Tournament: " + " " + str(s80_tourney.name) + " " + str(s80_tourney.endDate) + " " + str(timezone.now()) + "\n")

        tourney = get_tournament(f, DEBUG_WRITE, None, s80_tourney.name, asn, 
                   s80_tourney.calced_endDate, None, "S80")

        if(tourney is None):
                tourney = update_or_create_tournament(f, DEBUG_WRITE, None, asn, s80_tourney.name, 
                                        'Completed', s80_tourney.calced_endDate, s80_tourney.calced_endDate, 
                                        s80_tourney.calced_endDate, "https://bf.sport80.com", 
                                        s80_tourney.eventReference, "", False, "", 
                                        "", "S80", False, sys_user)

        Process_S80_Tournament_Events(f, asn, assn_recs, s80_tourney, tourney, DEBUG_WRITE, event_found_results)
        if(DEBUG_WRITE):
                f.write("       Completed: Process_S80_Tournament: " + " " + str(s80_tourney.name) + " " + str(timezone.now()) + "\n\n")

def Process_Engarde_Tournament_Event_Fencers(f, eve, event_found_results, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("                  Process_Engarde_Tournament_Event_Fencers: " 
                + str(timezone.now()) + "\n")
    
    event_final_results.objects.filter(efr_event=eve).delete()
    
    updates = []
    for y in event_found_results:
        efr = update_or_create_event_final_result(f, DEBUG_WRITE, eve, None, y['position'], y['full_name'], y['club_name'],
                                                  y['assn_member_identifier'], y['assn_member_number'])
        updates.append(efr)
    
    # Bulk update the records
    if updates:
        with transaction.atomic():
            event_final_results.objects.bulk_update(updates, [
                'efr_event', 'efr_final_position', 'efr_given_name', 'efr_given_club', 'efr_given_member_identifier', 'efr_assn_member_number'
            ])

    if DEBUG_WRITE:
        f.write("                   Complete Process_Engarde_Tournament_Event_Fencers: "+ "\n")
def Process_Engarde_Tournament_Event(f, asn, engarde_tourney, tourney, DEBUG_WRITE, event_found_results):
    if DEBUG_WRITE:
        f.write("            Process_Engarde_Tournament_Event: engarde_tourney_name:" 
                + str(engarde_tourney.given_tournament_name) 
                + " " + str(engarde_tourney.titre)
                + " calced_startdate: " + str(engarde_tourney.calced_startdate) 
                + " startdate: " + str(engarde_tourney.startdate) 
                + " startTime: " + str(engarde_tourney.startTime) 
                + " " + str(timezone.now()) + "\n")

    discipline = get_assn_discipline_from_text(f, asn, engarde_tourney.categorie, engarde_tourney.titre, engarde_tourney.given_tournament_name, False)
    gender = get_assn_gender_from_text(f, asn, engarde_tourney.categorie, engarde_tourney.titre, engarde_tourney.given_tournament_name, False)
    e_type = get_assn_type_from_text(f, asn, engarde_tourney.categorie, engarde_tourney.titre, engarde_tourney.given_tournament_name, False)
    ages = get_assn_ages_from_text(f, asn, engarde_tourney.categorie, engarde_tourney.titre, engarde_tourney.given_tournament_name, False)

    if e_type is None:
        e_type = get_assn_type_from_text(f, asn, "Individual", "", "", False)

    if gender is None:
        if engarde_tourney.sexe == 'f':
            gender = get_assn_gender_from_text(f, asn, "Women", "", "", False)
        elif engarde_tourney.sexe == 'm':
            gender = get_assn_gender_from_text(f, asn, "Men", "", "", False)
        elif engarde_tourney.sexe == 'n':
            gender = get_assn_gender_from_text(f, asn, "Mixed", "", "", False)

    if discipline is None:
        if engarde_tourney.arme == 'e':
            discipline = get_assn_discipline_from_text(f, asn, "Epee", "", "", False)
        elif engarde_tourney.arme == 'f':
            discipline = get_assn_discipline_from_text(f, asn, "Foil", "", "", False)
        elif engarde_tourney.arme == 's':
            discipline = get_assn_discipline_from_text(f, asn, "Sabre", "", "", False)

    if e_type.type_category.lower() != 'team':
        lookup_msg = "                  lookups: " + str(discipline.discipline_description) \
                        + "-" + str(gender.gender_description) \
                        + "-" + str(e_type.type_category_description) \
                        + "-" + str(ages.age_category_description) \
                        + " at " + str(timezone.now())
        if "Unknown" in lookup_msg:
            record_error_data('process_tournament', 'Process_Engarde_Tournament_Event', 'warning', lookup_msg)

        if len(engarde_tourney.startTime) > 0:
            datetime_str = engarde_tourney.startdate + " " + engarde_tourney.startTime
            datetime_format = '%Y %m %d %H:%M:%S'
            sdatetime = datetime.strptime(datetime_str, datetime_format)
            sdatetime_aware = timezone.make_aware(sdatetime, timezone.get_default_timezone())
        else:
            datetime_str = engarde_tourney.startdate
            datetime_format = '%Y %m %d'
            sdatetime = datetime.strptime(datetime_str, datetime_format)
            sdatetime_aware = timezone.make_aware(sdatetime, timezone.get_default_timezone())

        eve = update_or_create_event(f, False, tourney, None, 
                engarde_tourney.titre, 'Completed', e_type, discipline, gender, ages, sdatetime_aware)
        Process_Engarde_Tournament_Event_Fencers(f, eve, event_found_results, DEBUG_WRITE)

    if DEBUG_WRITE:
        f.write("       Completed: Process_Engarde_Tournament_Event: "
                + " " + str(engarde_tourney.given_tournament_name)
                + " " + str(engarde_tourney.titre) 
                + " " + str(timezone.now()) + "\n\n")
def Process_Engarde_Tournament(f, asn, engarde_tourney, DEBUG_WRITE, sys_user, event_found_results):
        if(DEBUG_WRITE):
                f.write("      Process_Engarde_Tournament: " + " " + str(engarde_tourney.given_tournament_name) 
                        + " " + str(engarde_tourney.titre)
                        + " " + str(engarde_tourney.calced_startdate) + " " + str(timezone.now()) + "\n")

        tourney = get_tournament(f, DEBUG_WRITE, None, engarde_tourney.given_tournament_name, asn, 
                   engarde_tourney.calced_startdate, None, "Engarde")

        if(tourney is None):
                e_type = get_assn_type_from_text(f, asn, engarde_tourney.given_tournament_name, engarde_tourney.titre, engarde_tourney.categorie, False)
                if(e_type is None or e_type.type_category.lower() == 'individual'):
                        comp_url = 'https://engarde-service.com/tournament/' + engarde_tourney.org + '/' + engarde_tourney.evt
                        tourney = update_or_create_tournament(f, DEBUG_WRITE, None, asn, engarde_tourney.given_tournament_name, 
                                                'Completed', engarde_tourney.calced_startdate, engarde_tourney.calced_startdate, 
                                                engarde_tourney.calced_startdate, comp_url, 
                                                "", "", False, "", 
                                                "", "Engarde", False, sys_user)
        if(tourney is not None):
                Process_Engarde_Tournament_Event(f, asn, engarde_tourney, tourney, DEBUG_WRITE, event_found_results)
        if(DEBUG_WRITE):
                f.write("       Completed: Process_Engarde_Tournament: "
                        + " " + str(engarde_tourney.given_tournament_name)
                        + " " + str(engarde_tourney.titre) 
                        + " " + str(timezone.now()) + "\n\n")

def Process_LPJS_Tournament_Event_Fencers(f, asn, assn_recs, lpjs_tourney_event, eve, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("                  Process_LPJS_Tournament_Event_Fencers: s80_tourney_name:" 
                + str(lpjs_tourney_event.event_name) + str(timezone.now()) + "\n")
    
    event_final_results.objects.filter(efr_event=eve).delete()
    
    updates = []
    for y in load_lpjs_competitions_results_events_fencers.objects.filter(event_results_url=lpjs_tourney_event.event_results_url):
        amn = get_assn_member_record(f, asn, assn_recs, None, y.full_name, "", "", False)
        mem_num = amn.assn_member_number if amn else None
        mem_identifier = amn.assn_member_identifier if amn else None
        efr = update_or_create_event_final_result(f, DEBUG_WRITE, eve, None, clean_position(y.position), y.full_name, "", mem_identifier, mem_num)
        updates.append(efr)
    
    # Bulk update the records
    if updates:
        with transaction.atomic():
            event_final_results.objects.bulk_update(updates, [
                'efr_event', 'efr_final_position', 'efr_given_name', 'efr_given_club', 'efr_given_member_identifier', 'efr_assn_member_number'
            ])

    if DEBUG_WRITE:
        f.write("                   Complete Process_LPJS_Tournament_Event_Fencers: " 
                + " " + str(eve.ev_tourney.tourney_name) 
                + " " + str(eve.ev_name) + " " + str(timezone.now()) + "\n")
def Process_LPJS_Tournament_Events(f, asn, assn_recs, lpjs_tourney, tourney, DEBUG_WRITE, event_found_results):
    if DEBUG_WRITE:
        f.write("            Process_LPJS_Tournament_Events: " 
                + str(lpjs_tourney.competition_name) 
                + " " + str(lpjs_tourney.start_date) 
                + " " + str(timezone.now()) + "\n")

    for x in load_lpjs_competitions_results_events.objects.filter(source_url=lpjs_tourney.competition_url):
        for y in event_found_results:
            if not y[0] and y[1] == x.event_name:
                if DEBUG_WRITE:
                    f.write("               Process_LPJS_Tournament_Events: " + str(x.event_name) 
                            + " " + str(timezone.now()) + "\n")
                
                discipline = get_assn_discipline_from_text(f, asn, x.event_name, lpjs_tourney.competition_name, "", False)
                gender = get_assn_gender_from_text(f, asn, x.event_name, lpjs_tourney.competition_name, "", False)
                e_type = get_assn_type_from_text(f, asn, x.event_name, lpjs_tourney.competition_name, "", False)
                ages = get_assn_ages_from_text(f, asn, x.event_name, lpjs_tourney.competition_name, "", False)

                lookup_msg = "                  lookups: " + str(discipline.discipline_description) \
                                + "-" + str(gender.gender_description) \
                                + "-" + str(e_type.type_category_description) \
                                + "-" + str(ages.age_category_description) \
                                + " at " + str(timezone.now())
                if "Unknown" in lookup_msg:
                    record_error_data('process_tournament', 'Process_LPJS_Tournament_Events', 'warning', lookup_msg)
                
                event = update_or_create_event(f, False, tourney, None, 
                                x.event_name, 'Completed', e_type, discipline, gender, ages, tourney.tourney_start_date)
                Process_LPJS_Tournament_Event_Fencers(f, asn, assn_recs, x, event, DEBUG_WRITE)
                
                if DEBUG_WRITE:
                    f.write("                Complete Process_LPJS_Tournament_Events: \n") 

    if DEBUG_WRITE:
        f.write("             Complete Process_LPJS_Tournament_Events: " + " " + str(lpjs_tourney.competition_name) + " " + str(lpjs_tourney.start_date) + " " + str(timezone.now()) + "\n")
def Process_LPJS_Tournament(f, asn, lpjs_tourney, DEBUG_WRITE, sys_user, assn_recs, event_found_results):
        if(DEBUG_WRITE):
                f.write("      Process_LPJS_Tournament: " + " " + str(lpjs_tourney.competition_name) + " " + str(lpjs_tourney.start_date) + " " + str(timezone.now()) + "\n")

        tourney = get_tournament(f, DEBUG_WRITE, None, lpjs_tourney.competition_name, asn, 
                   lpjs_tourney.start_date, None, "LPJS")

        if(tourney is None):
                tourney = update_or_create_tournament(f, DEBUG_WRITE, None, asn, lpjs_tourney.competition_name, 
                                        'Completed', lpjs_tourney.start_date, lpjs_tourney.start_date, 
                                        lpjs_tourney.start_date, lpjs_tourney.competition_url, 
                                        "", "", False, "", 
                                        "", "LPJS", False, sys_user)

        Process_LPJS_Tournament_Events(f, asn, assn_recs, lpjs_tourney, tourney, DEBUG_WRITE, event_found_results)
        if(DEBUG_WRITE):
                f.write("       Completed: Process_LPJS_Tournament: " + " " + str(lpjs_tourney.competition_name) + " " + str(timezone.now()) + "\n\n")

def Process_S80_Upcoming_Tournament_Event_Fencers(f, upcoming_tourney_event, event, asn, assn_recs, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("                  Process_S80_Upcoming_Tournament_Event_Fencers: upcoming_tourney_name:" 
                + str(upcoming_tourney_event.tournament_id.name) 
                + " " + str(upcoming_tourney_event.full_entry) 
                + " " + str(event.ev_tourney.tourney_name) 
                + " " + str(event.ev_name) + " " + str(timezone.now()) + "\n")

    s80_fencers_count = load_s80_upcoming_tournaments_entries_fencers.objects.filter(entry_id=upcoming_tourney_event).count()
    era_count = event_registered_athletes.objects.filter(era_event=event).count()

    if s80_fencers_count != era_count:
        if event.ev_status.status == "Upcoming":
            event_registered_athletes.objects.filter(era_event=event).delete()
        
        updates = []
        for y in load_s80_upcoming_tournaments_entries_fencers.objects.filter(entry_id=upcoming_tourney_event):
            if len(y.ind_license) > 0:
                era_identifier = y.ind_license
            else:
                amr = get_assn_member_record(f, asn, assn_recs, y.ind_license, y.s80_name, "", "", DEBUG_WRITE)
                if amr is not None:
                    era_identifier = amr.assn_member_identifier
                    era_member_number = amr.assn_member_number
                else:
                    era_identifier = ""                
                    era_member_number = 0
            efr = update_or_create_event_registered_athletes(f, DEBUG_WRITE, event, y.s80_name, y.s80_club, era_identifier, era_member_number)
            updates.append(efr)
        
        # Bulk update the records
        if updates:
            with transaction.atomic():
                event_registered_athletes.objects.bulk_update(updates, [
                    'era_event', 'era_given_name', 'era_given_club', 'era_given_member_identifier', 'era_assn_member_number'
                ])
    else:
        if DEBUG_WRITE:
            f.write("                       Complete Process_S80_Upcoming_Tournament_Event_Fencers: same count to skipping\n") 

    if DEBUG_WRITE:
        f.write("                   Complete Process_S80_Upcoming_Tournament_Event_Fencers: upcoming_tourney_name:" 
                + " " + str(event.ev_tourney.tourney_name) 
                + " " + str(event.ev_name) + " " + str(timezone.now()) + "\n")
def Process_S80_Upcoming_Tournament_Events(f, upcoming_tourney, tourney, asn, assn_recs, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("            Process_S80_Upcoming_Tournament_Events: upcoming_tourney_name:" 
                + str(upcoming_tourney.name) 
                + " " + str(upcoming_tourney.start_date) 
                + " " + str(upcoming_tourney.id) + " " + str(timezone.now()) + "\n")

    for x in load_s80_upcoming_tournaments_entries.objects.filter(tournament_id=upcoming_tourney):
        if DEBUG_WRITE:
            f.write("               Process_S80_Upcoming_Entries: " + str(x.entry_id) 
                    + "   Label: " + str(x.full_label) 
                    + "   Entry: " + str(x.full_entry) + " " + str(timezone.now()) + "\n")
        
        discipline = get_assn_discipline_from_text(f, tourney.tourney_assn, x.full_label, x.full_entry, tourney.tourney_name, False)
        gender = get_assn_gender_from_text(f, tourney.tourney_assn, x.full_label, x.full_entry, tourney.tourney_name, False)
        e_type = get_assn_type_from_text(f, tourney.tourney_assn, x.full_label, x.full_entry, tourney.tourney_name, False)
        ages = get_assn_ages_from_text(f, tourney.tourney_assn, x.full_label, x.full_entry, tourney.tourney_name, False)

        lookup_msg = "                  lookups: " + str(discipline.discipline_description) \
                        + "-" + str(gender.gender_description) \
                        + "-" + str(e_type.type_category_description) \
                        + "-" + str(ages.age_category_description) \
                        + " at " + str(timezone.now())
        if "Unknown" in lookup_msg:
            f.write("WARNING: " + lookup_msg + "\n")
        if DEBUG_WRITE:
            f.write(lookup_msg + "\n")
        
        event = get_event(f, False, tourney, x.full_entry, None)
        if event is None:
            if DEBUG_WRITE:
                f.write("                             Process_S80_Upcoming_Tournament_Events: Could not find event: " 
                        + str(upcoming_tourney.name) + " " + str(x.full_entry) + " " + str(timezone.now()) + "\n")
            ev_status = "Upcoming"
        else:
            if DEBUG_WRITE:
                f.write("                              Found Event: " + str(upcoming_tourney.name) + " " + str(x.full_entry) + " " + str(timezone.now()) + "\n")
            ev_status = event.ev_status.status
        
        event = update_or_create_event(f, False, tourney, event, 
                        x.full_entry, ev_status, e_type, discipline, gender, ages, tourney.tourney_start_date)
        Process_S80_Upcoming_Tournament_Event_Fencers(f, x, event, asn, assn_recs, DEBUG_WRITE)
        # BF_calc_and_write_event_extra_fields(f, event, DEBUG_WRITE)
        # BF_calc_ratings_and_write_event_extra_fields(f, event, DEBUG_WRITE)
        if DEBUG_WRITE:
            f.write("                Complete Process_S80_Upcoming_Entries: \n") 

    if DEBUG_WRITE:
        f.write("             Complete Process_S80_Upcoming_Tournament_Events: " + " " + str(upcoming_tourney.name) + " " + str(upcoming_tourney.start_date) + " " + str(upcoming_tourney.id) + " " + str(timezone.now()) + "\n")
def Process_S80_Upcoming_Tournament(f, asn, upcoming_tourney, DEBUG_WRITE, sys_user, assn_recs):
        if(DEBUG_WRITE):
                f.write("      Process_S80_Upcoming_Tournament: " + " " + str(upcoming_tourney.name) + " " + str(upcoming_tourney.start_date) + " " + str(upcoming_tourney.id) + " " + str(timezone.now()) + "\n")

        tourney = get_tournament(f, DEBUG_WRITE, None, upcoming_tourney.name, asn, upcoming_tourney.start_date, True, 'upcomingS80')
        if tourney is None:
                f.write("                             Process_S80_Upcoming_Tournament: Could not find tournament" + " " + str(upcoming_tourney.name) + " " + str(upcoming_tourney.start_date) + " " + str(upcoming_tourney.id) + " " + str(timezone.now()) + "\n")
                tourney_status = "Upcoming"
        else:
                if(DEBUG_WRITE):
                        f.write("                             Found Tournament: " + str(tourney.tourney_name) + " " + str(tourney.tourney_status) + " " + str(timezone.now()) + "\n")
                tourney_status = tourney.tourney_status.status

        tourney = update_or_create_tournament(f, DEBUG_WRITE, tourney, asn, upcoming_tourney.name, 
                                tourney_status, upcoming_tourney.start_date, upcoming_tourney.end_date, 
                                upcoming_tourney.entry_closing, upcoming_tourney.url, 
                                upcoming_tourney.licence_id,
                                "", False, upcoming_tourney.entry_link, 
                                upcoming_tourney.event_entry_list_url, "upcomingS80", True, sys_user)

        addr = update_or_create_address(f, DEBUG_WRITE, upcoming_tourney.venuename, upcoming_tourney.venueaddr1, 
                                        upcoming_tourney.venueaddr2, upcoming_tourney.venueaddr3, 
                                        upcoming_tourney.venueaddrcity, 
                                        upcoming_tourney.venueaddrregion, 
                                        "", upcoming_tourney.venueaddrpostcode, 
                                        "", "GBR")
        t_addr = tournament_address(tourney=tourney,tourney_addr=addr).save()

#        tourney_apply_latest_assn_member_numbers(f, asn, tourney, assn_recs, DEBUG_WRITE)
        Process_S80_Upcoming_Tournament_Events(f, upcoming_tourney, tourney, asn, assn_recs, DEBUG_WRITE)
        if(DEBUG_WRITE):
                f.write("       Completed: Process_S80_Upcoming_Tournament: " + " " + str(upcoming_tourney.name) + " " + str(upcoming_tourney.tournament_id) + " " + str(timezone.now()) + "\n\n")

def Process_In_Range_S80_Upcoming_Events(f, asn, assn_recs, r_start, r_end, DEBUG_WRITE):
        f.write("\n Process_In_Range_S80_Upcoming_Events: " + str(timezone.now()) + "\n")
        sys_user = get_system_process_user()
#        assn_recs = association_members.objects.filter(assn = asn).values_list('assn_member_full_name', flat=True)

        for x in load_s80_upcoming_tournaments.objects.filter(start_date__gte = r_start, start_date__lte = r_end).order_by('start_date'):
                if "Admin -" not in x.sanction_name:
                        if(x.event_entry_list_url is not None):
                                print("   S80 Upcoming Load to Tournaments: " + str(x.name) + " start date: " + str(x.start_date) + " at " + str(timezone.now()) + "\n")
                                f.write("   S80 Upcoming Load to Tournaments: " + str(x.name) + " start date: " + str(x.start_date) + " at " + str(timezone.now()) + "\n")
                                Process_S80_Upcoming_Tournament(f, asn, x, DEBUG_WRITE, sys_user, assn_recs)

        f.write(" Completed Process_In_Range_S80_Upcoming_Events: " + str(timezone.now()) + "\n")
def Process_In_Range_FTL(f, asn, assn_recs, r_start, r_end, DEBUG_WRITE):
        f.write("      Working FTL " + str(r_start) + " to " + str(r_end) + "\n")
#        for x in load_ftl_tournaments.objects.filter(start_date__gte = r_start, 
#                        end_date__lte = r_end).order_by('start_date'):
        for x in load_ftl_tournaments.objects.filter(start_date__gte = r_start, 
                        start_date__lte = r_end).order_by('start_date'):
                if (1==1):
#                if("Hampshire" in x.name):      
                        event_found_results = []
                        print("Load to Tournaments Tournament FTL: " + x.tournament_id + " - " + x.name + " - " + x.location + " - " + x.start + " - " + x.end + " " + str(timezone.now()) + "\n")
                        if(DEBUG_WRITE):
                                f.write("         Load to Tournaments Tournament FTL: " + x.tournament_id + " - " + x.name + " - " + x.location + " - " + x.start + " - " + x.end + " " + str(timezone.now()) + "\n")
                        events_to_check = load_ftl_tournament_events.objects.filter(tournament_id_index = x)
                        for y in events_to_check:
                                final_recs = load_ftl_event_final_results.objects.filter(
                                        event_id_index = y).values('place', 'name', 'club1', 'member_num')
                                event_final_results = list(final_recs)
                                for z in event_final_results:
                                        z['position'] = clean_position(z['place'])
                                        z['full_name'] = z['name']
                                        z['club_name'] = z['club1']
                                        z['assn_member_identifier'] = z['member_num']
                                        amn = get_assn_member_record(f, asn, assn_recs, z['member_num'], z['name'], "", "", False)
                                        if(amn is not None):
                                                z['assn_member_number'] = amn.assn_member_number
                                        else:
                                                z['assn_member_number'] = None
                                event_final_results_sorted = sorted(event_final_results, key=lambda x: x['position'])
                                if(DEBUG_WRITE):
                                        f.write("            Working Event: " + y.name + "--- Athlete Count: " + str(len(event_final_results)) + "\n")
                                event_found, eve = Event_Exists(f, asn, x.name, y.name, x.start_date, event_final_results_sorted, len(event_final_results_sorted), DEBUG_WRITE)
                                event_found_results.append([event_found, y.name])

                        all_true = False
                        all_false = False
                        if all(result[0] for result in event_found_results):
                                all_true = True
                        if all(not result[0] for result in event_found_results):
                                all_false = True
                        if not all_true and not all_false:
                                msg = "Mixed event_found_results.  Tournament: " + x.name + " " + str(timezone.now())
                                record_error_data('process_tournament', 'Process_In_Range_FTL', 'warning', msg)
                        if(not all_true):
                                #event_found_results tells you which events to create
                                Process_FTL_Tournament(f, asn, assn_recs, x, DEBUG_WRITE, event_found_results)
def Process_In_Range_S80(f, asn, assn_recs, r_start, r_end, DEBUG_WRITE):
        f.write("      Working S80 \n")
        sys_user = get_system_process_user()

        for x in load_s80_fencing_competitions.objects.filter(isInternational = False, 
                        calced_endDate__gte = r_start, 
                        calced_endDate__lte = r_end).order_by('calced_endDate'):
                if (1==1):
#                if("Hampshire" in x.name):      
                        event_found_results = []
                        print("Load to Tournaments Tournament S80: " + x.at_id + " - " + x.name + " - " + x.isInternational + " - " + str(x.calced_endDate) + " - " + str(timezone.now()) + "\n")
                        if(DEBUG_WRITE):
                                f.write("         Load to Tournaments Tournament S80: " + x.at_id + " - " + x.name + " - " + x.isInternational + " - " + str(x.calced_endDate) + " " + str(timezone.now()) + "\n")
                        events_to_check = load_s80_fencing_events.objects.filter(competition = x)
                        for y in events_to_check:
                                final_recs = load_s80_fencing_fencing_results.objects.filter(
                                        event = y).values('rank', 'name', 'identifier')
                                event_final_results = list(final_recs)
                                for z in event_final_results:
                                        z['position'] = clean_position(z['rank'])
                                        z['full_name'] = z['name']
                                        z['club_name'] = ""
                                        z['assn_member_identifier'] = z['identifier']
                                        amn = get_assn_member_record(f, asn, assn_recs, z['identifier'], z['name'], "", "", False)
                                        if(amn is not None):
                                                z['assn_member_number'] = amn.assn_member_number
                                        else:
                                                z['assn_member_number'] = None
                                event_final_results_sorted = sorted(event_final_results, key=lambda x: x['position'])
                                if(DEBUG_WRITE):
                                        f.write("            Working Event: " + y.name + "--- Athlete Count: " + str(len(event_final_results)) + "\n")
                                event_found, eve = Event_Exists(f, asn, x.name, y.name, x.calced_endDate, event_final_results_sorted, len(event_final_results_sorted), DEBUG_WRITE)
                                event_found_results.append([event_found, y.name])

                        all_true = False
                        all_false = False
                        if all(result[0] for result in event_found_results):
                                all_true = True
#                                print("All True")
                        if all(not result[0] for result in event_found_results):
                                all_false = True
#                                print("All False")
                        if not all_true and not all_false:
#                                print("Mixed")
                                msg = "Mixed event_found_results.  Tournament: " + x.name + " " + str(timezone.now())
                                record_error_data('process_tournament', 'Process_In_Range_S80', 'warning', msg)
                        if(not all_true):
                                #event_found_results tells you which events to create
                                Process_S80_Tournament(f, asn, x, DEBUG_WRITE, sys_user, assn_recs, event_found_results)
def Process_In_Range_Engarde(f, asn, assn_recs, r_start, r_end, DEBUG_WRITE):
        f.write("      Working Engarde \n")
        sys_user = get_system_process_user()

        #Engarde is different - Stored at event level.
        for x in load_engarde_event.objects.filter(calced_startdate__gte = r_start, 
                        calced_startdate__lte = r_end).order_by('calced_startdate'):
                if (1==1):
##                if("Hampshire" in x.name):      
                        event_found_results = []
                        print("Load to Tournaments Engarde Tournament / Event Engarde: " + str(x.given_tournament_name) + " Event Name: "+ str(x.titre) + " START_DATE: " + str(x.calced_startdate))
                        if(DEBUG_WRITE):
                                f.write("         Load to Tournaments Engarde Tournament / Event Engarde: " + str(x.given_tournament_name) + " Event Name: "+ str(x.titre) + " START_DATE: " + str(x.calced_startdate)+" at: "+ str(timezone.now()) + "\n")
                        final_recs = load_engarde_final_results.objects.filter(org = x.org, evt = x.evt, compe = x.compe, titre = x.titre, startdate = x.startdate
                                ).annotate(charpos=F('position')).values('charpos', 'first_name', 'last_name', 'club_name')
                        event_final_results = list(final_recs)
                        for z in event_final_results:
                                z['position'] = clean_position(z['charpos'])
                                z['full_name'] = z['last_name'] + " " + z['first_name']
                                amn = get_assn_member_record(f, asn, assn_recs, None, z['full_name'], z['first_name'], z['last_name'], False)
                                if(amn is not None):
                                        z['assn_member_identifier'] = amn.assn_member_identifier
                                        z['assn_member_number'] = amn.assn_member_number
                                else:
                                        z['assn_member_identifier'] = None
                                        z['assn_member_number'] = None
                        event_final_results_sorted = sorted(event_final_results, key=lambda x: x['position'])
                        if(DEBUG_WRITE):
                                f.write("            Working Tournament / Event: " + str(x.given_tournament_name) + " Event Name: "+ str(x.titre) + "--- Athlete Count: " + str(len(event_final_results)) + "\n")
                                for zz in event_final_results_sorted:
                                        f.write("               " + str(zz['position']) + " " 
                                        + str(zz['full_name']) + " " + str(zz['club_name']) 
                                        + " identifier: " + str(zz['assn_member_identifier'])
                                        + " number: " + str(zz['assn_member_number']) + "\n")
                        event_found, eve = Event_Exists(f, asn, x.given_tournament_name, x.titre, x.calced_startdate, event_final_results_sorted, len(event_final_results_sorted), DEBUG_WRITE)
                        if(not event_found):
                                Process_Engarde_Tournament(f, asn, x, DEBUG_WRITE, sys_user, event_final_results_sorted)
def Process_In_Range_LPJS(f, asn, assn_recs, r_start, r_end, DEBUG_WRITE):
        f.write("      Working LPJS \n")
        sys_user = get_system_process_user()

        for x in load_lpjs_competitions_results.objects.filter(start_date__gte = r_start, 
                        start_date__lte = r_end).order_by('start_date'):
                if (1==1):
#                if("Hampshire" in x.name):      
                        event_found_results = []
                        print("Load to Tournaments Tournament LPJS: " + x.competition_name + " - " + str(x.start_date) + " - " + str(timezone.now()))
                        if(DEBUG_WRITE):
                                f.write("          Load to Tournaments Tournament LPJS: " + x.competition_name + " - " + str(x.start_date) + " - " + str(timezone.now()) + "\n")
                        events_to_check = load_lpjs_competitions_results_events.objects.filter(source_url = x.competition_url)
#                        print(len(events_to_check))
                        for y in events_to_check:
                                final_recs = load_lpjs_competitions_results_events_fencers.objects.filter(
                                        event_results_url = y.event_results_url).annotate(charpos=F('position')).values('charpos', 'full_name', 'club_name')
                                event_final_results = list(final_recs)
                                if(len(event_final_results) > 0):
                                        for z in event_final_results:
                                                z['position'] = clean_position(z['charpos'])
                                                amn = get_assn_member_record(f, asn, assn_recs, None, z['full_name'], "", "", False)
                                                if(amn is not None):
                                                        z['assn_member_identifier'] = amn.assn_member_identifier
                                                        z['assn_member_number'] = amn.assn_member_number
                                                else:
                                                        z['assn_member_identifier'] = None
                                                        z['assn_member_number'] = None
                                        event_final_results_sorted = sorted(event_final_results, key=lambda x: x['position'])
                                        if(DEBUG_WRITE):
                                                f.write("            Working Event: " + y.event_name + "--- Athlete Count: " + str(len(event_final_results)) + "\n")
                                        event_found, eve = Event_Exists(f, asn, x.competition_name, y.event_name, x.start_date, event_final_results_sorted, len(event_final_results_sorted), DEBUG_WRITE)
                                        event_found_results.append([event_found, y.event_name])
                        if(len(event_found_results) > 0):
                                all_true = False
                                all_false = False
                                if all(result[0] for result in event_found_results):
                                        all_true = True
#                                        print("All True")
                                if all(not result[0] for result in event_found_results):
                                        all_false = True
#                                        print("All False")
                                if not all_true and not all_false:
#                                        print("Mixed")
                                        msg = "Mixed event_found_results.  Tournament: " + x.competition_name + " " + str(timezone.now())
                                        record_error_data('process_tournament', 'Process_In_Range_LPJS', 'warning', msg)
                                if(not all_true):
                                        #event_found_results tells you which events to create
                                        Process_LPJS_Tournament(f, asn, x, DEBUG_WRITE, sys_user, assn_recs, event_found_results)

def UK_Process_Tournaments(f, s_date, e_date, DEBUG_WRITE):
#        record_log_data("process_tournaments.py", "UK_Process_Tournaments", "started: " + str(timezone.now()))
        f.write("\n\n\nUK_Process_Tournaments: " + str(datetime.now()) + "\n")
        rng = 10
        f.write("Start Date: " + str(s_date) + "   End Date: " + str(e_date) + "\n")

        asn = get_association(f, "British Fencing", DEBUG_WRITE)
        assn_recs = association_members.objects.filter(assn = asn).values_list('assn_member_full_name', flat=True)

        r_start = s_date
        if(r_start + relativedelta(days=rng) > e_date):
                r_end = e_date
        else:
                r_end = r_start + relativedelta(days=rng)
        while(r_start <= e_date):
                f.write("   Range Start Date: " + str(r_start) + "   Range End Date: " + str(r_end) + "\n")
                record_log_data("load_to_tournaments.py", "Process_UK_Tournaments", 
                        "running for Range Start Date: " + str(r_start) 
                        + " Range End Date: " + str(r_end) + " at: " + str(timezone.now()))

                #delete inbounds
                tournaments.objects.filter(tourney_start_date__gte=r_start,tourney_start_date__lte=r_end,
                        tourney_inbound__in=['upcomingS80', 'upcomingLPJS', 'upcomingDurham']).delete()

                Process_In_Range_FTL(f, asn, assn_recs, r_start, r_end, False)
                Process_In_Range_Engarde(f, asn, assn_recs, r_start, r_end, False)
                Process_In_Range_LPJS(f, asn, assn_recs, r_start, r_end, False)
                Process_In_Range_S80(f, asn, assn_recs, r_start, r_end, False)
                Process_In_Range_S80_Upcoming_Events(f, asn, assn_recs, r_start, r_end, False)

                r_start = r_end + relativedelta(days=1)
                if(r_start + relativedelta(days=rng) > e_date):
                        r_end = e_date
                else:
                        r_end = r_start + relativedelta(days=rng)

        f.write("Completed: UK_Process_Tournaments: " + str(datetime.now()) + "\n")
#        record_log_data("load_to_tournaments.py", "UK_Process_Tournaments", "completed: " + str(timezone.now()))


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
        if os.environ.get("DURHAM_TOURNAMENT_PROCESS_DAY_TO_LOAD") is not None:
                process_days_back = int(os.environ.get("DURHAM_TOURNAMENT_PROCESS_DAY_TO_LOAD"))
        else:
                process_days_back = None
        if os.environ.get("S80_UPCOMING_DAYS_OUT") is not None:
                process_days_out = int(os.environ.get("S80_UPCOMING_DAYS_OUT"))
        else:
                process_days_out = None

        force_overwrite = False

        asn = get_association(f, "British Fencing", DEBUG_WRITE)
        if(DEBUG_WRITE):
                f.write("DEBUG_WRITE: " + str(DEBUG_WRITE) + "\n")
                f.write("asn:  " + str(asn.assn_name) + "\n")
                f.write("process_days_back:  " + str(process_days_back) + "\n")

        if(process_days_back is not None and process_days_out is not None):
                if 'reset' in args:
#                        record_log_data(app_name, "y_admin_key_tables_backup.run()", "Starting")
#                        y_admin_key_tables_backup.run()
#                        record_log_data(app_name, "y_admin_key_tables_backup.run()", "Completed")

                        record_log_data(app_name, "Copying Backup Files", "Starting")
                        zbackup_dir = os.path.join(settings.BASE_DIR, "zbackupfiles/")
                        dump_dir = os.path.join(settings.BASE_DIR, "dumps/")
                        copy_zbackup_files_if_exist(f, zbackup_dir, dump_dir, True)
                        record_log_data(app_name, "Copying Backup Files", "Complete")

                        tournaments.objects.all().delete()
                        
                        force_overwrite = True
                        record_log_data(app_name, "y_admin_key_tables_load.run()", "Starting")
                        y_admin_key_tables_load.run()
                        record_log_data(app_name, "y_admin_key_tables_load.run()", "Completed")

                if(len(args) == 2):  #dates only
                        ls_date = Make_String_Timezone_Aware(args[0])
                        le_date = Make_String_Timezone_Aware(args[1])
                if(len(args) > 2):
                        ls_date = Make_String_Timezone_Aware(args[1])
                        le_date = Make_String_Timezone_Aware(args[2])
                if(len(args) == 0): # run with defaults
                        ls_date = timezone.now() - relativedelta(days=int(process_days_back)) 
                        le_date = timezone.now() + relativedelta(days=process_days_out)
                if(DEBUG_WRITE):
                        f.write("force override: " + str(force_overwrite) + "\n")
                        f.write("New Start Date: " + str(ls_date) + "\n")
                        f.write("New End Date: " + str(le_date) + "\n")

                DEBUG_WRITE = False

                record_log_data(app_name, "load_to_tournaments", "Starting")
                UK_Process_Tournaments(f, ls_date, le_date, DEBUG_WRITE)
                record_log_data(app_name, "load_to_tournaments", "Completed")

        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()
#        record_log_data(app_name, funct_name, "Completed")


# python manage.py runscript load_to_tournaments
# python manage.py runscript load_to_tournaments --script-args reset
# python manage.py runscript load_to_tournaments --script-args 01/01/2024 12/31/2024
# python manage.py runscript load_to_tournaments --script-args reset 01/01/2022 01/15/2022

# python manage.py runscript load_to_tournaments --script-args 06/10/2024 06/30/2024

# nohup python manage.py runscript load_to_tournaments --script-args 06/10/2024 06/30/2029 &


#realNIF and realPoints are the correct values.  Some events have a realNIF value of 1!
#ok.  very rare occurance.  Probably human error on S80 system.  


#SELECT fc.name, fc."endDate", fe.multiplier, fe.nif, fe."calculatedNif", fe."realNif", fe.*  
#FROM public.integrations_load_s80_fencing_events fe, integrations_load_s80_fencing_competitions fc
#where fc.id = fe.competition_id
#and fe."realNif" like '1'
#and fe.international = 'False'
#ORDER BY fc.name ASC #

#                                Birmingham International 	British Open Chanpionships      British U23 Foil Championships
#        multiplier = 			1							1                               300
#        nif = 					Null						700                             1 or null
#        calculatedNIF = 		405							22                              133 or null or 1
#        realNIF = 				405							700                             1

