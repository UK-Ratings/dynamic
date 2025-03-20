#!/usr/bin/env python3

from assn_mgr.models import *
from base.models import *
from scripts.x_helper_functions import *
from django.utils import timezone
from datetime import datetime


import requests
import json
import os
from dotenv import load_dotenv
from django.db import transaction

from django.conf import settings

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")

# python manage.py runscript assn_mgr_s80_load_members_clubs


def zzzpopulate_s80_clubs(f, DEBUG_WRITE):
        f.write("\n\nPOPULATE S80 CLUBS: " + str(timezone.now()) + "\n")

        for x in s80_load_club_records.objects.all():
                if(1==1):  #conversions
                        if(x.start_date is not None):
                                start_date = datetime.strptime(x.start_date, "%Y-%m-%dT%H:%M:%S%z")
                        else:
                                start_date = None
                        if(x.joined_date is not None):
                                joined_date = datetime.strptime(x.joined_date, "%Y-%m-%dT%H:%M:%S%z")
                        else:
                                joined_date = None
                        if(x.exp_date is not None):
                                exp_date = datetime.strptime(x.exp_date, "%Y-%m-%dT%H:%M:%S%z")
                        else:
                                exp_date = None
                        if(x.valid is not None):
                                r_valid = eval(x.valid)
                        else:
                                r_valid = False
                        if(x.suspended is not None):
                                r_suspended = eval(x.suspended)
                        else:
                                r_suspended = False

                s80_club_records.objects.update_or_create(
                        contact_uuid_s80 = x.contact_uuid,
                        defaults = {
                        'uuid_s80': x.uuid,
                        'add_on_uuid_s80': x.add_on_uuid,
                        'add_on_name': x.add_on_name,
                        'add_on_type_uuid_s80': x.add_on_type_uuid,
                        'add_on_type_name': x.add_on_type_name,
                        'add_on_region': x.add_on_region,
                        'add_on_region_org_uuid_s80': x.add_on_region_org_uuid,
                        'name': x.name,
                        'joined_date': joined_date,
                        'start_date': start_date,
                        'exp_date': exp_date,
                        'email': x.email,
                        'phone': x.phone,
                        'primary_address_line1': x.primary_address_line1,
                        'primary_address_line2': x.primary_address_line2,
                        'primary_address_line3': x.primary_address_line3,
                        'primary_address_city': x.primary_address_city,
                        'primary_address_region': x.primary_address_region,
                        'primary_address_region_abbr': x.primary_address_region_abbr,
                        'primary_address_postal_code': x.primary_address_postal_code,
                        'primary_address_country': x.primary_address_country,
                        'img_url': x.img_url,
                        'valid': r_valid,
                        'suspended': r_suspended,
                        'identity_number': x.identity_number,
                        'identity_number_name': x.identity_number_name,
                        }
                )
def zzzpopulate_s80_memberships(f, DEBUG_WRITE):
        f.write("\n\nPOPULATE S80 MEMBERSHIPS: " + str(timezone.now()) + "\n")

        for x in s80_load_membership_records.objects.all():
                if(1==1):  #conversions
                        if(x.dob is not None):
                                dob = datetime.strptime(x.dob, "%Y-%m-%dT%H:%M:%S%z")
                        else:
                                dob = None
                        if(x.start_date is not None):
                                start_date = datetime.strptime(x.start_date, "%Y-%m-%dT%H:%M:%S%z")
                        else:
                                start_date = None
                        if(x.joined_date is not None):
                                joined_date = datetime.strptime(x.joined_date, "%Y-%m-%dT%H:%M:%S%z")
                        else:
                                joined_date = None
                        if(x.exp_date is not None):
                                exp_date = datetime.strptime(x.exp_date, "%Y-%m-%dT%H:%M:%S%z")
                        else:
                                exp_date = None
                        if(x.valid is not None):
                                r_valid = eval(x.valid)
                        else:
                                r_valid = False
                        if(x.suspended is not None):
                                r_suspended = eval(x.suspended)
                        else:
                                r_suspended = False
                        if(x.identity_number is not None):
                                i_number = eval(x.identity_number)
                        else:
                                i_number = 0

                s80_membership_records.objects.update_or_create(
                        uuid_s80 = x.uuid,
                        defaults = {
                        'contact_uuid_s80': x.contact_uuid,
                        'add_on_uuid_s80': x.add_on_uuid,
                        'add_on_name': x.add_on_name,
                        'add_on_type_uuid_s80': x.add_on_type_uuid,
                        'add_on_type_name': x.add_on_type_name,
                        'add_on_region': x.add_on_region,
                        'add_on_region_org_uuid_s80': x.add_on_region_org_uuid,
                        'first_name': x.first_name,
                        'last_name': x.last_name.upper(),
                        'dob': dob,
                        'gender': x.gender,
                        'joined_date': joined_date,
                        'start_date': start_date,
                        'exp_date': exp_date,
                        'email': x.email,
                        'phone': x.phone,
                        'primary_address_line1': x.primary_address_line1,
                        'primary_address_line2': x.primary_address_line2,
                        'primary_address_line3': x.primary_address_line3,
                        'primary_address_city': x.primary_address_city,
                        'primary_address_region': x.primary_address_region,
                        'primary_address_region_abbr': x.primary_address_region_abbr,
                        'primary_address_postal_code': x.primary_address_postal_code,
                        'primary_address_country': x.primary_address_country,
                        'img_url': x.img_url,
                        'valid': r_valid,
                        'suspended': r_suspended,
                        'identity_number': i_number,
                        'identity_number_name': x.identity_number_name
                        })
def zzzmore_than_one_club_in_membership_data(f, mem_rec, mem_rec_clubs, invalid_clubs, DEBUG_WRITE):
#due to complexity, took this out of the main process_s80_membership_clubs
#will always return 1 club
        if(DEBUG_WRITE):
                f.write("ERROR 2: Found more than one club in S80 membership data: Going for first valid club" + "\n")
                f.write("       mem_rec.identity_number: " + str(mem_rec.identity_number) + " first_name: " + str(mem_rec.first_name) + " last_name: " + str(mem_rec.last_name)+ "\n")
                for r in mem_rec_clubs:
                        f.write("          mem_rec_clubs: " + str(r.membership_uuid.identity_number) +
                                " add_on_clubs_name: " + str(r.add_on_clubs_name) + 
                                " add_on_clubs_uuid: " + str(r.add_on_clubs_uuid) +
                                " add_on_clubs_primary: " + str(r.add_on_clubs_primary) + 
                                "\n")

        orig_mem_rec_clubs = mem_rec_clubs[:]
        mem_rec_clubs_copy = mem_rec_clubs[:]
        if(DEBUG_WRITE):
                f.write("       more than one club to check: " + str(len(mem_rec_clubs)) + "\n")
        if(DEBUG_WRITE):
                for d in mem_rec_clubs_copy:
                        f.write("               mem_rec_clubs_copy: " + d.add_on_clubs_name + " " + d.add_on_clubs_uuid + "\n")
        for club in invalid_clubs:
                for mem_rec_c in mem_rec_clubs_copy:
                        if(mem_rec_c.add_on_clubs_name == club.name):
#                        if(mem_rec_c.add_on_clubs_uuid == club.contact_uuid_s80):
                                if(DEBUG_WRITE):
                                        f.write("       Info 2a: Club in membership record not valid.  Deleteing: \n")
                                        f.write("            mem_rec.identity_number: " + str(mem_rec.identity_number) + " membership_uuid: " + "\n")
                                        f.write("            invalid club: " + club.name + " " + club.contact_uuid_s80 + " " + str(club.valid) + "\n" )
                                        f.write("            mem_rec_c: " + str(mem_rec_c) + "\n")
                                        f.write("            records in mem_rec_clubs: " + str(len(mem_rec_clubs)) + "\n")
                                mem_rec_clubs.remove(mem_rec_c)
                                if(DEBUG_WRITE):
                                        f.write("            records in mem_rec_clubs after delete: " + str(len(mem_rec_clubs)) + "\n")

        if(len(mem_rec_clubs) == 0):
                if(DEBUG_WRITE):
                        f.write("   Info 2b: No valid clubs.  Going back to first club: \n")
                        f.write("      First club: " + orig_mem_rec_clubs[0].add_on_clubs_name + " " + orig_mem_rec_clubs[0].add_on_clubs_uuid + " " + "\n" )
                club_recs = s80_club_records.objects.filter(name=orig_mem_rec_clubs[0].add_on_clubs_name)
        elif(len(mem_rec_clubs) > 1):
                if(DEBUG_WRITE):
                        f.write("   Info 2c: More than 1 valid clubs.  Going back to first valid club: \n")
                        f.write("      First club: " + mem_rec_clubs[0].add_on_clubs_name + " " + mem_rec_clubs[0].add_on_clubs_uuid + " " + "\n" )
                club_recs = s80_club_records.objects.filter(name=mem_rec_clubs[0].add_on_clubs_name)
        else:
                if(DEBUG_WRITE):
                        f.write("   Info 2d: 1 valid club.  Using that club: \n")
                        f.write("      valid club: " + mem_rec_clubs[0].add_on_clubs_name + " " + mem_rec_clubs[0].add_on_clubs_uuid + " " + "\n" )
                club_recs = s80_club_records.objects.filter(name=mem_rec_clubs[0].add_on_clubs_name)
        if(DEBUG_WRITE):
                f.write("   Leaving Error 2, Multiple Clubs\n")
#        print(club_recs)
        if(DEBUG_WRITE):
                for r in club_recs:
                        f.write("     club_recs = r.name: " + str(r.name) + "\n")

        return(club_recs)
def zzzload_s80_memberships(f, access_token, records_per_page, record_offset, S80_DEBUG, DEBUG_WRITE):
        f.write("\n\n\nLOAD S80 MEMBERSHIPS: " + str(timezone.now()) + "\n")

        headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer '+access_token,
        }

        params = {
        'valid': 'false',                       #true is only active memberships; false is all memberships
        'limit': str(records_per_page),          #number of records to return
        'offset': str(record_offset),          #record offset
        }

        if(S80_DEBUG):
                ep_url = 'https://bf.s80testing.co.uk'
                endpoint = 'https://bf.s80testing.co.uk/api/ext/c_add_on/all/competitor/aef66d86-b810-4b8d-873a-bae0715b0081'
        else:
                ep_url = 'https://bf.sport80.com'
                endpoint = 'https://bf.sport80.com/api/ext/c_add_on/all/competitor/aef66d86-b810-4b8d-873a-bae0715b0081'

#        f.write("endpoint: " + str(endpoint)+"\n")
#        f.write("params: " + str(params)+"\n")
#        f.write("headers: " + str(headers)+"\n")

        response = requests.get(endpoint,params=params,headers=headers,)
        f.write("response status code: " + str(response.status_code)+"\n")
 
        if response.status_code == 200:
                json_object = json.loads(response.text)
                total_membership_records = json_object['total']
                f.write("total_membership_records: " + str(total_membership_records) + "\n")
                next_endpoint = json_object['links']['next']
                xxxx = 0
                while next_endpoint is not None:
 #                       query_membership_records = json_object['count']
 #                       f.write("query_membership_records: " + str(query_membership_records) + "\n")
                        for x in json_object['data']:
                                if(DEBUG_WRITE):
                                        pretty_json = json.dumps(x, indent=4)
                                        f.write(pretty_json)

                                mr, created = s80_load_membership_records.objects.update_or_create(
                                        uuid = x['uuid'],
                                        defaults = {
                                        'contact_uuid': x['contact_uuid'],
                                        'add_on_uuid': x['add_on_uuid'],
                                        'add_on_name': x['add_on_name'],
                                        'add_on_type_uuid': x['add_on_type_uuid'],
                                        'add_on_type_name': x['add_on_type_name'],
                                        'add_on_region': x['add_on_region'],
                                        'add_on_region_org_uuid': x['add_on_region_org_uuid'],
                                        'first_name': x['first_name'],
                                        'last_name': x['last_name'],
                                        'dob': x['dob'],
                                        'gender': x['gender'],
                                        'joined_date': x['joined_date'],
                                        'start_date': x['start_date'],
                                        'exp_date': x['exp_date'],
                                        'email': x['email'],
                                        'phone': x['phone'],
                                        'primary_address_line1': x['primary_address']['line1'],
                                        'primary_address_line2': x['primary_address']['line2'],
                                        'primary_address_line3': x['primary_address']['line3'],
                                        'primary_address_city': x['primary_address']['city'],
                                        'primary_address_region': x['primary_address']['region'],
                                        'primary_address_region_abbr': x['primary_address']['region_abbr'],
                                        'primary_address_postal_code': x['primary_address']['postal_code'],
                                        'primary_address_country': x['primary_address']['country'],
                                        'img_url': x['img_url'],
                                        'valid': x['valid'],
                                        'suspended': x['suspended'],
                                        'identity_number': x['identity_number'],
                                        'identity_number_name': x['identity_number_name'],
                                        })
                                if(len(x['add_on_clubs']) > 1):
                                        if(DEBUG_WRITE):
                                                f.write("\nEXCEPTION 2: MORE THAN ONE CLUB IN LOAD DATA\n")
                                                pretty_json = json.dumps(x, indent=4)
                                                f.write(pretty_json)
                                if(len(x['add_on_clubs']) == 0):
                                        if(DEBUG_WRITE):
                                                f.write("\nEXCEPTION 1: NO CLUBS IN LOAD DATA\n")
                                                pretty_json = json.dumps(x, indent=4)
                                                f.write(pretty_json)
                                for y in x['add_on_clubs']:
                                        s80_load_membership_records_clubs.objects.update_or_create(
                                                membership_uuid = mr,
                                                add_on_clubs_name = y['name'],
                                                add_on_clubs_uuid = y['uuid'],
                                                add_on_clubs_primary = y['primary'],
                                                )

                        if(json_object['links']['next'] is None):
                                next_endpoint = None
                        else:
                                next_endpoint = ep_url+json_object['links']['next']
                                f.write("\nnext_query: " + str(next_endpoint) + "\n")

                                response = requests.get(next_endpoint, headers=headers)
                                f.write("response status code: " + str(response.status_code)+" " + str(timezone.now()) + "\n")
                                json_object = json.loads(response.text)
                        xxxx += 1
                        if(xxxx > 300000):   #only for testing
                                next_endpoint = None
def zzzload_s80_clubs(f, access_token, records_per_page, record_offset, S80_DEBUG, DEBUG_WRITE):
        f.write("\n\nLOAD S80 CLUBS: " + str(timezone.now()) + "\n")

        headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer '+access_token,
        }

        params = {
        'valid': 'false',                       #true is only active memberships; false is all memberships
        'limit': str(records_per_page),          #number of records to return
        'offset': str(record_offset),          #record offset
        }

        if(S80_DEBUG):
                ep_url = 'https://bf.s80testing.co.uk'
                endpoint = 'https://bf.s80testing.co.uk/api/ext/c_add_on/all/org/0cf44083-f6de-43ce-bace-b441d64548f5'
        else:
                ep_url = 'https://bf.sport80.com'
                endpoint = 'https://bf.sport80.com/api/ext/c_add_on/all/org/0cf44083-f6de-43ce-bace-b441d64548f5'

#        f.write("endpoint: " + str(endpoint)+"\n")
#        f.write("params: " + str(params)+"\n")
#        f.write("headers: " + str(headers)+"\n")

        response = requests.get(endpoint,params=params,headers=headers,)
        f.write("response status code: " + str(response.status_code)+"\n")
 
        if response.status_code == 200:
                json_object = json.loads(response.text)
                total_membership_records = json_object['total']
                f.write("total_club_records: " + str(total_membership_records) + "\n")
                next_endpoint = json_object['links']['next']
                while next_endpoint is not None:
 #                       query_membership_records = json_object['count']
 #                       f.write("query_membership_records: " + str(query_membership_records) + "\n")
                        for x in json_object['data']:
                                if(DEBUG_WRITE):
                                        pretty_json = json.dumps(x, indent=4)
                                        f.write(pretty_json)
                                s80_load_club_records.objects.update_or_create(
                                        contact_uuid = x['contact_uuid'],
                                        defaults = {
                                        'uuid': x['uuid'],
                                        'add_on_uuid': x['add_on_uuid'],
                                        'add_on_name': x['add_on_name'],
                                        'add_on_type_uuid': x['add_on_type_uuid'],
                                        'add_on_type_name': x['add_on_type_name'],
                                        'add_on_region': x['add_on_region'],
                                        'add_on_region_org_uuid': x['add_on_region_org_uuid'],
                                        'name': x['name'],
                                        'joined_date': x['joined_date'],
                                        'start_date': x['start_date'],
                                        'exp_date': x['exp_date'],
                                        'email': x['email'],
                                        'phone': x['phone'],
                                        'primary_address_line1': x['primary_address']['line1'],
                                        'primary_address_line2': x['primary_address']['line2'],
                                        'primary_address_line3': x['primary_address']['line3'],
                                        'primary_address_city': x['primary_address']['city'],
                                        'primary_address_region': x['primary_address']['region'],
                                        'primary_address_region_abbr': x['primary_address']['region_abbr'],
                                        'primary_address_postal_code': x['primary_address']['postal_code'],
                                        'primary_address_country': x['primary_address']['country'],
                                        'img_url': x['img_url'],
                                        'valid': x['valid'],
                                        'suspended': x['suspended'],
                                        'identity_number': x['identity_number'],
                                        'identity_number_name': x['identity_number_name'],
                                        }
                                )

                        if(json_object['links']['next'] is None):
                                next_endpoint = None
                        else:
                                next_endpoint = ep_url+json_object['links']['next']
                                f.write("next_query: " + str(next_endpoint) + "\n")
#                                print("next_query: " + str(next_endpoint) + "\n")

                                response = requests.get(next_endpoint, headers=headers)
                                f.write("response status code: " + str(response.status_code)+" " + str(timezone.now()) + "\n")
                                json_object = json.loads(response.text)
def oldpopulate_s80_membership_clubs(f, DEBUG_WRITE):
        f.write("\n\nPOPULATE S80 MEMBERSHIP CLUBS: " + str(timezone.now()) + "\n")

        def_club = os.environ.get("SPORT80_ERROR_CLUB")
        error_club = s80_club_records.objects.filter(name__contains = def_club)
        if(DEBUG_WRITE):
                f.write("error_club: " + str(error_club) + "\n")  

        invalid_clubs = s80_club_records.objects.filter(valid=False)
        if(DEBUG_WRITE):
                for r in invalid_clubs:
                        f.write("iiinvalid_clubs: " + str(r.name) + " contact_uuid: " + str(r.contact_uuid_s80) + " " + str(r.valid) + "\n")
        for q in s80_load_membership_records.objects.all():
                if(1 == 1):
#                if(q.identity_number == '136970'):
                        club_recs = []
                        mem_rec = s80_membership_records.objects.get(uuid_s80=q.uuid)
                        if(DEBUG_WRITE):
                                f.write("   mem_rec: " + str(mem_rec.identity_number) + " " + str(mem_rec.first_name) + " " + str(mem_rec.last_name) + "\n")
                        mem_rec_clubs = list(s80_load_membership_records_clubs.objects.filter(membership_uuid=q))
                        if(DEBUG_WRITE):
                                for tt in mem_rec_clubs:
                                        f.write("    mem_rec_clubs: " + tt.add_on_clubs_name + " " + tt.add_on_clubs_uuid + "\n")

                        if(len(mem_rec_clubs) > 1):
                                if(DEBUG_WRITE):
                                        f.write("      INFO 11: More than one club in s80_load_membership_records_club \n")
                                club_recs = more_than_one_club_in_membership_data(f, mem_rec, mem_rec_clubs, invalid_clubs, DEBUG_WRITE)
                        elif(len(mem_rec_clubs) == 0):
                                if(DEBUG_WRITE):
                                        f.write("      ERROR 1: No clubs in s80_load_membership_records_club: \n")
                                        f.write("            x: " + str(q) + "\n")
                                        f.write("            mem_rec.identity_number: " + str(mem_rec.identity_number) + "\n")
                                        f.write("            going to default club\n")
                                club_recs = error_club
                        else:
                                if(DEBUG_WRITE):
                                        f.write("      INFO 12: One club listed in s80_load_membership_records_club\n")
                                club_recs = s80_club_records.objects.filter(contact_uuid_s80=mem_rec_clubs[0].add_on_clubs_uuid)
                                if(DEBUG_WRITE):
                                        f.write("      club_recs count: " + str(len(club_recs)) + "\n")

                        if(DEBUG_WRITE):
                                f.write("        club_recs: " + str(club_recs) + "\n")                              
                        if(len(club_recs) == 0):
                                if(DEBUG_WRITE):
                                        f.write("        ERROR 3: Could not find club in S80 Clubs: " + mem_rec_clubs[0].add_on_clubs_name + " " + mem_rec_clubs[0].add_on_clubs_uuid + "\n")
                                        f.write("         mem_rec_clubs: " + str(mem_rec_clubs[0]) + "\n")
                                        f.write("         mem_rec.identity_number: " + str(mem_rec.identity_number) + " membership_uuid: " + str(mem_rec_clubs[0].membership_uuid.uuid) + "\n")
                                        f.write("         going to default error club\n")
                                club_recs = error_club

                        if(DEBUG_WRITE):
                                f.write("          GOING INTO WRITE" + "\n")                              
                                for qq in club_recs:
                                        f.write("            identity_number: " + str(mem_rec.identity_number) + " club_recs: " + str(qq.name) + "\n")
                        if(1==1):  #conversions
                                if(len(mem_rec_clubs) > 0):
                                        if(mem_rec_clubs[0].add_on_clubs_primary is not None):
                                                r_primary = eval(mem_rec_clubs[0].add_on_clubs_primary)
                                        else:
                                                r_primary = False
                                else:
                                        r_primary = True
                        s80_membership_records_clubs.objects.update_or_create(
                                membership_uuid = mem_rec,
                                add_on_clubs_name = club_recs[0].name,
                                add_on_clubs_uuid = club_recs[0],
                                add_on_clubs_primary = r_primary,
                                )
###here
def wrkload_s80_memberships(f, access_token, records_per_page, record_offset, S80_DEBUG, DEBUG_WRITE):
        f.write("\n\n\nLOAD S80 MEMBERSHIPS: " + str(timezone.now()) + "\n")

        headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer '+access_token,
        }

        params = {
        'valid': 'false',                       #true is only active memberships; false is all memberships
        'limit': str(records_per_page),          #number of records to return
        'offset': str(record_offset),          #record offset
        }

        if(S80_DEBUG):
                ep_url = 'https://bf.s80testing.co.uk'
                endpoint = 'https://bf.s80testing.co.uk/api/ext/c_add_on/all/competitor/aef66d86-b810-4b8d-873a-bae0715b0081'
        else:
                ep_url = 'https://bf.sport80.com'
                endpoint = 'https://bf.sport80.com/api/ext/c_add_on/all/competitor/aef66d86-b810-4b8d-873a-bae0715b0081'

#        f.write("endpoint: " + str(endpoint)+"\n")
#        f.write("params: " + str(params)+"\n")
#        f.write("headers: " + str(headers)+"\n")

        response = requests.get(endpoint,params=params,headers=headers,)
        f.write("response status code: " + str(response.status_code)+"\n")
 
        if response.status_code == 200:
                json_object = json.loads(response.text)
                total_membership_records = json_object['total']
                f.write("total_membership_records: " + str(total_membership_records) + "\n")
                next_endpoint = json_object['links']['next']
                xxxx = 0
                while next_endpoint is not None:
 #                       query_membership_records = json_object['count']
 #                       f.write("query_membership_records: " + str(query_membership_records) + "\n")
                        for x in json_object['data']:
                                if(DEBUG_WRITE):
                                        pretty_json = json.dumps(x, indent=4)
                                        f.write(pretty_json)

                                mr, created = s80_load_membership_records.objects.update_or_create(
                                        uuid = x['uuid'],
                                        defaults = {
                                        'contact_uuid': x['contact_uuid'],
                                        'add_on_uuid': x['add_on_uuid'],
                                        'add_on_name': x['add_on_name'],
                                        'add_on_type_uuid': x['add_on_type_uuid'],
                                        'add_on_type_name': x['add_on_type_name'],
                                        'add_on_region': x['add_on_region'],
                                        'add_on_region_org_uuid': x['add_on_region_org_uuid'],
                                        'first_name': x['first_name'],
                                        'last_name': x['last_name'],
                                        'dob': x['dob'],
                                        'gender': x['gender'],
                                        'joined_date': x['joined_date'],
                                        'start_date': x['start_date'],
                                        'exp_date': x['exp_date'],
                                        'email': x['email'],
                                        'phone': x['phone'],
                                        'primary_address_line1': x['primary_address']['line1'],
                                        'primary_address_line2': x['primary_address']['line2'],
                                        'primary_address_line3': x['primary_address']['line3'],
                                        'primary_address_city': x['primary_address']['city'],
                                        'primary_address_region': x['primary_address']['region'],
                                        'primary_address_region_abbr': x['primary_address']['region_abbr'],
                                        'primary_address_postal_code': x['primary_address']['postal_code'],
                                        'primary_address_country': x['primary_address']['country'],
                                        'img_url': x['img_url'],
                                        'valid': x['valid'],
                                        'suspended': x['suspended'],
                                        'identity_number': x['identity_number'],
                                        'identity_number_name': x['identity_number_name'],
                                        })
                                if(len(x['add_on_clubs']) > 1):
                                        if(DEBUG_WRITE):
                                                f.write("\nEXCEPTION 2: MORE THAN ONE CLUB IN LOAD DATA\n")
                                                pretty_json = json.dumps(x, indent=4)
                                                f.write(pretty_json)
                                if(len(x['add_on_clubs']) == 0):
                                        if(DEBUG_WRITE):
                                                f.write("\nEXCEPTION 1: NO CLUBS IN LOAD DATA\n")
                                                pretty_json = json.dumps(x, indent=4)
                                                f.write(pretty_json)
                                for y in x['add_on_clubs']:
                                        s80_load_membership_records_clubs.objects.update_or_create(
                                                membership_uuid = mr,
                                                add_on_clubs_name = y['name'],
                                                add_on_clubs_uuid = y['uuid'],
                                                add_on_clubs_primary = y['primary'],
                                                )

                        if(json_object['links']['next'] is None):
                                next_endpoint = None
                        else:
                                next_endpoint = ep_url+json_object['links']['next']
                                f.write("\nnext_query: " + str(next_endpoint) + "\n")

                                response = requests.get(next_endpoint, headers=headers)
                                f.write("response status code: " + str(response.status_code)+" " + str(timezone.now()) + "\n")
                                json_object = json.loads(response.text)
                        xxxx += 1
                        if(xxxx > 300000):   #only for testing
                                next_endpoint = None



def load_s80_memberships(f, access_token, records_per_page, record_offset, S80_DEBUG, DEBUG_WRITE):
    f.write("\n\n\nLOAD S80 MEMBERSHIPS: " + str(timezone.now()) + "\n")

    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + access_token,
    }

    params = {
        'valid': 'false',  # true is only active memberships; false is all memberships
        'limit': str(records_per_page),  # number of records to return
        'offset': str(record_offset),  # record offset
    }

    if S80_DEBUG:
        ep_url = 'https://bf.s80testing.co.uk'
        endpoint = 'https://bf.s80testing.co.uk/api/ext/c_add_on/all/competitor/aef66d86-b810-4b8d-873a-bae0715b0081'
    else:
        ep_url = 'https://bf.sport80.com'
        endpoint = 'https://bf.sport80.com/api/ext/c_add_on/all/competitor/aef66d86-b810-4b8d-873a-bae0715b0081'

    response = requests.get(endpoint, params=params, headers=headers)
    f.write("response status code: " + str(response.status_code) + "\n")

    if response.status_code == 200:
        json_object = response.json()
        total_membership_records = json_object['total']
        f.write("total_membership_records: " + str(total_membership_records) + "\n")
        next_endpoint = json_object['links']['next']
        xxxx = 0

        while next_endpoint is not None:
            updates = []
            club_updates = []

            for x in json_object['data']:
                if DEBUG_WRITE:
                    pretty_json = json.dumps(x, indent=4)
                    f.write(pretty_json)

                mr, created = s80_load_membership_records.objects.update_or_create(
                    uuid=x['uuid'],
                    defaults={
                        'contact_uuid': x['contact_uuid'],
                        'add_on_uuid': x['add_on_uuid'],
                        'add_on_name': x['add_on_name'],
                        'add_on_type_uuid': x['add_on_type_uuid'],
                        'add_on_type_name': x['add_on_type_name'],
                        'add_on_region': x['add_on_region'],
                        'add_on_region_org_uuid': x['add_on_region_org_uuid'],
                        'first_name': x['first_name'],
                        'last_name': x['last_name'],
                        'dob': x['dob'],
                        'gender': x['gender'],
                        'joined_date': x['joined_date'],
                        'start_date': x['start_date'],
                        'exp_date': x['exp_date'],
                        'email': x['email'],
                        'phone': x['phone'],
                        'primary_address_line1': x['primary_address']['line1'],
                        'primary_address_line2': x['primary_address']['line2'],
                        'primary_address_line3': x['primary_address']['line3'],
                        'primary_address_city': x['primary_address']['city'],
                        'primary_address_region': x['primary_address']['region'],
                        'primary_address_region_abbr': x['primary_address']['region_abbr'],
                        'primary_address_postal_code': x['primary_address']['postal_code'],
                        'primary_address_country': x['primary_address']['country'],
                        'img_url': x['img_url'],
                        'valid': x['valid'],
                        'suspended': x['suspended'],
                        'identity_number': x['identity_number'],
                        'identity_number_name': x['identity_number_name'],
                    }
                )

                for y in x['add_on_clubs']:
                    club_updates.append(s80_load_membership_records_clubs(
                        membership_uuid=mr,  # Use the instance of s80_load_membership_records
                        add_on_clubs_name=y['name'],
                        add_on_clubs_uuid=y['uuid'],
                        add_on_clubs_primary=y['primary'],
                    ))

            # Bulk update the records
            with transaction.atomic():
                s80_load_membership_records.objects.bulk_create(updates, ignore_conflicts=True)
                s80_load_membership_records_clubs.objects.bulk_create(club_updates, ignore_conflicts=True)

            if json_object['links']['next'] is None:
                next_endpoint = None
            else:
                next_endpoint = ep_url + json_object['links']['next']
                f.write("\nnext_query: " + str(next_endpoint) + "\n")

                response = requests.get(next_endpoint, headers=headers)
                f.write("response status code: " + str(response.status_code) + " " + str(timezone.now()) + "\n")
                json_object = response.json()

            xxxx += 1
            if xxxx > 300000:  # only for testing
                next_endpoint = None

    if DEBUG_WRITE:
        f.write("Completed: LOAD S80 MEMBERSHIPS: " + str(timezone.now()) + "\n")
def load_s80_clubs(f, access_token, records_per_page, record_offset, S80_DEBUG, DEBUG_WRITE):
    f.write("\n\nLOAD S80 CLUBS: " + str(timezone.now()) + "\n")

    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + access_token,
    }

    params = {
        'valid': 'false',  # true is only active memberships; false is all memberships
        'limit': str(records_per_page),  # number of records to return
        'offset': str(record_offset),  # record offset
    }

    if S80_DEBUG:
        ep_url = 'https://bf.s80testing.co.uk'
        endpoint = 'https://bf.s80testing.co.uk/api/ext/c_add_on/all/org/0cf44083-f6de-43ce-bace-b441d64548f5'
    else:
        ep_url = 'https://bf.sport80.com'
        endpoint = 'https://bf.sport80.com/api/ext/c_add_on/all/org/0cf44083-f6de-43ce-bace-b441d64548f5'

    response = requests.get(endpoint, params=params, headers=headers)
    f.write("response status code: " + str(response.status_code) + "\n")

    if response.status_code == 200:
        json_object = response.json()
        total_club_records = json_object['total']
        f.write("total_club_records: " + str(total_club_records) + "\n")
        next_endpoint = json_object['links']['next']

        while next_endpoint is not None:
            updates = []

            for x in json_object['data']:
                if DEBUG_WRITE:
                    pretty_json = json.dumps(x, indent=4)
                    f.write(pretty_json)

                updates.append(s80_load_club_records(
                    contact_uuid=x['contact_uuid'],
                    uuid=x['uuid'],
                    add_on_uuid=x['add_on_uuid'],
                    add_on_name=x['add_on_name'],
                    add_on_type_uuid=x['add_on_type_uuid'],
                    add_on_type_name=x['add_on_type_name'],
                    add_on_region=x['add_on_region'],
                    add_on_region_org_uuid=x['add_on_region_org_uuid'],
                    name=x['name'],
                    joined_date=x['joined_date'],
                    start_date=x['start_date'],
                    exp_date=x['exp_date'],
                    email=x['email'],
                    phone=x['phone'],
                    primary_address_line1=x['primary_address']['line1'],
                    primary_address_line2=x['primary_address']['line2'],
                    primary_address_line3=x['primary_address']['line3'],
                    primary_address_city=x['primary_address']['city'],
                    primary_address_region=x['primary_address']['region'],
                    primary_address_region_abbr=x['primary_address']['region_abbr'],
                    primary_address_postal_code=x['primary_address']['postal_code'],
                    primary_address_country=x['primary_address']['country'],
                    img_url=x['img_url'],
                    valid=x['valid'],
                    suspended=x['suspended'],
                    identity_number=x['identity_number'],
                    identity_number_name=x['identity_number_name'],
                ))

            # Bulk update the records
            with transaction.atomic():
                s80_load_club_records.objects.bulk_create(updates, ignore_conflicts=True)

            if json_object['links']['next'] is None:
                next_endpoint = None
            else:
                next_endpoint = ep_url + json_object['links']['next']
                f.write("next_query: " + str(next_endpoint) + "\n")

                response = requests.get(next_endpoint, headers=headers)
                f.write("response status code: " + str(response.status_code) + " " + str(timezone.now()) + "\n")
                json_object = response.json()

    if DEBUG_WRITE:
        f.write("Completed: LOAD S80 CLUBS: " + str(timezone.now()) + "\n")
def create_blank_s80_club_records(f):
        def_club = os.environ.get("SPORT80_ERROR_CLUB")
        s80_club_records.objects.update_or_create(
                name = def_club,
                defaults = {}
                )
def populate_s80_clubs(f, DEBUG_WRITE):
    f.write("\n\nPOPULATE S80 CLUBS: " + str(timezone.now()) + "\n")

    updates = []
    for x in s80_load_club_records.objects.all():
        start_date = datetime.strptime(x.start_date, "%Y-%m-%dT%H:%M:%S%z") if x.start_date else None
        joined_date = datetime.strptime(x.joined_date, "%Y-%m-%dT%H:%M:%S%z") if x.joined_date else None
        exp_date = datetime.strptime(x.exp_date, "%Y-%m-%dT%H:%M:%S%z") if x.exp_date else None
        r_valid = eval(x.valid) if x.valid is not None else False
        r_suspended = eval(x.suspended) if x.suspended is not None else False

        mr, created = s80_club_records.objects.update_or_create(
            contact_uuid_s80=x.contact_uuid,
            defaults={
                'uuid_s80': x.uuid,
                'add_on_uuid_s80': x.add_on_uuid,
                'add_on_name': x.add_on_name,
                'add_on_type_uuid_s80': x.add_on_type_uuid,
                'add_on_type_name': x.add_on_type_name,
                'add_on_region': x.add_on_region,
                'add_on_region_org_uuid_s80': x.add_on_region_org_uuid,
                'name': x.name,
                'joined_date': joined_date,
                'start_date': start_date,
                'exp_date': exp_date,
                'email': x.email,
                'phone': x.phone,
                'primary_address_line1': x.primary_address_line1,
                'primary_address_line2': x.primary_address_line2,
                'primary_address_line3': x.primary_address_line3,
                'primary_address_city': x.primary_address_city,
                'primary_address_region': x.primary_address_region,
                'primary_address_region_abbr': x.primary_address_region_abbr,
                'primary_address_postal_code': x.primary_address_postal_code,
                'primary_address_country': x.primary_address_country,
                'img_url': x.img_url,
                'valid': r_valid,
                'suspended': r_suspended,
                'identity_number': x.identity_number,
                'identity_number_name': x.identity_number_name,
            }
        )

    if DEBUG_WRITE:
        f.write("Completed: POPULATE S80 CLUBS: " + str(timezone.now()) + "\n")
def populate_s80_memberships(f, DEBUG_WRITE):
    f.write("\n\nPOPULATE S80 MEMBERSHIPS: " + str(timezone.now()) + "\n")

    updates = []
    cnt = 0
    for x in s80_load_membership_records.objects.all():
        dob = datetime.strptime(x.dob, "%Y-%m-%dT%H:%M:%S%z") if x.dob else None
        start_date = datetime.strptime(x.start_date, "%Y-%m-%dT%H:%M:%S%z") if x.start_date else None
        joined_date = datetime.strptime(x.joined_date, "%Y-%m-%dT%H:%M:%S%z") if x.joined_date else None
        exp_date = datetime.strptime(x.exp_date, "%Y-%m-%dT%H:%M:%S%z") if x.exp_date else None
        r_valid = eval(x.valid) if x.valid is not None else False
        r_suspended = eval(x.suspended) if x.suspended is not None else False
        i_number = eval(x.identity_number) if x.identity_number is not None else 0

        mr, created = s80_membership_records.objects.update_or_create(
            uuid_s80=x.uuid,
            defaults={
            'contact_uuid_s80':x.contact_uuid,
            'add_on_uuid_s80':x.add_on_uuid,
            'add_on_name':x.add_on_name,
            'add_on_type_uuid_s80':x.add_on_type_uuid,
            'add_on_type_name':x.add_on_type_name,
            'add_on_region':x.add_on_region,
            'add_on_region_org_uuid_s80':x.add_on_region_org_uuid,
            'first_name':x.first_name,
            'last_name':x.last_name.upper(),
            'dob':dob,
            'gender':x.gender,
            'joined_date':joined_date,
            'start_date':start_date,
            'exp_date':exp_date,
            'email':x.email,
            'phone':x.phone,
            'primary_address_line1':x.primary_address_line1,
            'primary_address_line2':x.primary_address_line2,
            'primary_address_line3':x.primary_address_line3,
            'primary_address_city':x.primary_address_city,
            'primary_address_region':x.primary_address_region,
            'primary_address_region_abbr':x.primary_address_region_abbr,
            'primary_address_postal_code':x.primary_address_postal_code,
            'primary_address_country':x.primary_address_country,
            'img_url':x.img_url,
            'valid':r_valid,
            'suspended':r_suspended,
            'identity_number':i_number,
            'identity_number_name':x.identity_number_name,
        })
        if(cnt % 1000 == 0):
                f.write("POPULATE S80 MEMBERSHIPS cnt: " + str(cnt) + " " + str(timezone.now()) + "\n")
#                print("POPULATE S80 MEMBERSHIPS cnt: " + str(cnt) + " " + str(timezone.now()) + "\n")
        cnt += 1
    if DEBUG_WRITE:
        f.write("Completed: POPULATE S80 MEMBERSHIPS: " + str(timezone.now()) + "\n")


def zzzmore_than_one_club_in_membership_data(f, mem_rec, mem_rec_clubs, invalid_clubs, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("ERROR 2: Found more than one club in S80 membership data: Going for first valid club\n")
        f.write(f"       mem_rec.identity_number: {mem_rec.identity_number} first_name: {mem_rec.first_name} last_name: {mem_rec.last_name}\n")
        for r in mem_rec_clubs:
            f.write(f"          mem_rec_clubs: {r.membership_uuid.identity_number} add_on_clubs_name: {r.add_on_clubs_name} add_on_clubs_uuid: {r.add_on_clubs_uuid} add_on_clubs_primary: {r.add_on_clubs_primary}\n")

    orig_mem_rec_clubs = mem_rec_clubs[:]
    mem_rec_clubs_copy = mem_rec_clubs[:]
    if DEBUG_WRITE:
        f.write(f"       more than one club to check: {len(mem_rec_clubs)}\n")
        for d in mem_rec_clubs_copy:
            f.write(f"               mem_rec_clubs_copy: {d.add_on_clubs_name} {d.add_on_clubs_uuid}\n")

    invalid_club_names = {club.name for club in invalid_clubs}
    mem_rec_clubs = [mem_rec_c for mem_rec_c in mem_rec_clubs_copy if mem_rec_c.add_on_clubs_name not in invalid_club_names]

    if DEBUG_WRITE:
        f.write(f"            records in mem_rec_clubs after delete: {len(mem_rec_clubs)}\n")

    if not mem_rec_clubs:
        if DEBUG_WRITE:
            f.write("   Info 2b: No valid clubs.  Going back to first club:\n")
            f.write(f"      First club: {orig_mem_rec_clubs[0].add_on_clubs_name} {orig_mem_rec_clubs[0].add_on_clubs_uuid}\n")
        club_recs = s80_club_records.objects.filter(name=orig_mem_rec_clubs[0].add_on_clubs_name)
    elif len(mem_rec_clubs) > 1:
        if DEBUG_WRITE:
            f.write("   Info 2c: More than 1 valid clubs.  Going back to first valid club:\n")
            f.write(f"      First club: {mem_rec_clubs[0].add_on_clubs_name} {mem_rec_clubs[0].add_on_clubs_uuid}\n")
        club_recs = s80_club_records.objects.filter(name=mem_rec_clubs[0].add_on_clubs_name)
    else:
        if DEBUG_WRITE:
            f.write("   Info 2d: 1 valid club.  Using that club:\n")
            f.write(f"      valid club: {mem_rec_clubs[0].add_on_clubs_name} {mem_rec_clubs[0].add_on_clubs_uuid}\n")
        club_recs = s80_club_records.objects.filter(name=mem_rec_clubs[0].add_on_clubs_name)

    if DEBUG_WRITE:
        f.write("   Leaving Error 2, Multiple Clubs\n")
        for r in club_recs:
            f.write(f"     club_recs = r.name: {r.name}\n")

    return club_recs


def one_or_more_club_in_membership_data(f, mem_rec_clubs, invalid_club_names, error_club, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("            one_or_more_club_in_membership_data: " + "\n")

    invalid_club_names_set = set(invalid_club_names)
    club_rec = error_club
    if DEBUG_WRITE:
        f.write("               error_club: " + error_club.name + "\n")

    for x in mem_rec_clubs:
        if DEBUG_WRITE:
            f.write("               mem_rec_clubs: " + x.add_on_clubs_name + " " + x.add_on_clubs_uuid + "\n")
        if x.add_on_clubs_name is not None and x.add_on_clubs_name not in invalid_club_names_set:
            try:
                club_rec = s80_club_records.objects.get(name=x.add_on_clubs_name)
                if DEBUG_WRITE:
                    f.write("               found first good club name: " + str(club_rec.name) + "\n")
                return club_rec
            except s80_club_records.DoesNotExist:
                club_rec = error_club
                f.write("                  ERROR 2: club_rec.DoesNotExist: " + x.add_on_clubs_name + "\n")

    return club_rec
def populate_s80_membership_clubs(f, DEBUG_WRITE):
    f.write("\n\nPOPULATE S80 MEMBERSHIP CLUBS: " + str(timezone.now()) + "\n")

    def_club = os.environ.get("SPORT80_ERROR_CLUB")
    error_club = s80_club_records.objects.filter(name__contains=def_club).first()
    if DEBUG_WRITE:
        f.write("error_club: " + str(error_club) + "\n")

    invalid_club_names = s80_club_records.objects.filter(valid=False).values_list('name', flat=True)
    if DEBUG_WRITE:
        for name in invalid_club_names:
            f.write("invalid_club: " + name + "\n")

    updates = []
    identity_numbers = s80_load_membership_records.objects.values_list('identity_number', flat=True)
    id_num_cnt = len(identity_numbers)
    cnt = 0
    for k in identity_numbers:
        if k is not None:
            if DEBUG_WRITE:
                f.write("\nidentity_number: " + str(k) + "\n")
            try:
                idf = s80_membership_records.objects.get(identity_number=k)
                good_to_process = True
            except s80_membership_records.DoesNotExist:
                good_to_process = False
                if DEBUG_WRITE:
                    f.write("      ERROR 1: Could not find membership record: " + str(k) + " in s80_membership_records\n")
            if good_to_process:
                s80lmrc = s80_load_membership_records_clubs.objects.filter(membership_uuid__identity_number=k)
                if DEBUG_WRITE:
                    f.write("   len(s80lmrc): " + str(len(s80lmrc)) + "\n")
                    for v in s80lmrc:
                        f.write("      s80lmrc: " + str(v.add_on_clubs_name) + " " + str(v.add_on_clubs_uuid) + "\n")
                if len(s80lmrc) > 0:
                    club_rec = one_or_more_club_in_membership_data(f, s80lmrc, invalid_club_names, error_club, DEBUG_WRITE)
                else:
                    club_rec = error_club
                if DEBUG_WRITE:
                    f.write("club_rec name: " + str(club_rec.name) + "\n")
                mr, created = s80_membership_records_clubs.objects.update_or_create(
                        membership_uuid=idf,
                        defaults={
                        'add_on_clubs_name':club_rec.name,
                        'add_on_clubs_uuid':club_rec,
                        'add_on_clubs_primary':True,
                })

        if cnt % 1000 == 0:
            if DEBUG_WRITE:
                f.write("cnt: " + str(cnt) + " " + str(id_num_cnt) + " " + str(timezone.now()) + "\n")
#            print("cnt: " + str(cnt), id_num_cnt, timezone.now())
        cnt += 1

    if DEBUG_WRITE:
        f.write("Completed: POPULATE S80 MEMBERSHIP CLUBS: " + str(timezone.now()) + "\n")



def zzzpopulate_s80_membership_clubs(f, DEBUG_WRITE):
    f.write("\n\nPOPULATE S80 MEMBERSHIP CLUBS: " + str(timezone.now()) + "\n")
    updates = []

    def_club = os.environ.get("SPORT80_ERROR_CLUB")
    error_club = s80_club_records.objects.filter(name__contains=def_club).first()
    if DEBUG_WRITE:
        f.write("error_club: " + str(error_club) + "\n")

    invalid_clubs = s80_club_records.objects.filter(valid=False)
    if DEBUG_WRITE:
        for r in invalid_clubs:
            f.write("invalid_clubs: " + str(r.name) + " contact_uuid: " + str(r.contact_uuid_s80) + " " + str(r.valid) + "\n")

    updates = []
    for q in s80_load_membership_records.objects.all():
        club_recs = []
        mem_rec = s80_membership_records.objects.get(uuid_s80=q.uuid)
        if DEBUG_WRITE:
            f.write("   mem_rec: " + str(mem_rec.identity_number) + " " + str(mem_rec.first_name) + " " + str(mem_rec.last_name) + "\n")
        mem_rec_clubs = list(s80_load_membership_records_clubs.objects.filter(membership_uuid=q))
        if DEBUG_WRITE:
            for tt in mem_rec_clubs:
                f.write("    mem_rec_clubs: " + tt.add_on_clubs_name + " " + tt.add_on_clubs_uuid + "\n")

        if len(mem_rec_clubs) > 1:
            if DEBUG_WRITE:
                f.write("      INFO 11: More than one club in s80_load_membership_records_club \n")
            club_recs = more_than_one_club_in_membership_data(f, mem_rec, mem_rec_clubs, invalid_clubs, DEBUG_WRITE)
        elif len(mem_rec_clubs) == 0:
            if DEBUG_WRITE:
                f.write("      ERROR 1: No clubs in s80_load_membership_records_club: \n")
                f.write("            x: " + str(q) + "\n")
                f.write("            mem_rec.identity_number: " + str(mem_rec.identity_number) + "\n")
                f.write("            going to default club\n")
            club_recs = [error_club]
        else:
            if DEBUG_WRITE:
                f.write("      INFO 12: One club listed in s80_load_membership_records_club\n")
            club_recs = s80_club_records.objects.filter(contact_uuid_s80=mem_rec_clubs[0].add_on_clubs_uuid)
            if DEBUG_WRITE:
                f.write("      club_recs count: " + str(len(club_recs)) + "\n")

        if DEBUG_WRITE:
            f.write("        club_recs: " + str(club_recs) + "\n")
        if len(club_recs) == 0:
            if DEBUG_WRITE:
                f.write("        ERROR 3: Could not find club in S80 Clubs: " + mem_rec_clubs[0].add_on_clubs_name + " " + mem_rec_clubs[0].add_on_clubs_uuid + "\n")
                f.write("         mem_rec_clubs: " + str(mem_rec_clubs[0]) + "\n")
                f.write("         mem_rec.identity_number: " + str(mem_rec.identity_number) + " membership_uuid: " + str(mem_rec_clubs[0].membership_uuid.uuid) + "\n")
                f.write("         going to default error club\n")
            club_recs = [error_club]

        if DEBUG_WRITE:
            f.write("          GOING INTO WRITE" + "\n")
            for qq in club_recs:
                f.write("            identity_number: " + str(mem_rec.identity_number) + " club_recs: " + str(qq.name) + "\n")

        r_primary = eval(mem_rec_clubs[0].add_on_clubs_primary) if len(mem_rec_clubs) > 0 and mem_rec_clubs[0].add_on_clubs_primary is not None else False

        mr, created = s80_membership_records_clubs.objects.update_or_create(
            membership_uuid=mem_rec,
            defaults={
            'add_on_clubs_name':club_recs[0].name,
            'add_on_clubs_uuid':club_recs[0],
            'add_on_clubs_primary':r_primary,
        })

    # Bulk update the records
#    with transaction.atomic():
#        s80_membership_records_clubs.objects.bulk_create(updates, ignore_conflicts=True)

    if DEBUG_WRITE:
        f.write("Completed: POPULATE S80 MEMBERSHIP CLUBS: " + str(timezone.now()) + "\n")


def delete_s80_load_tables():
        s80_load_club_records.objects.all().delete()
        s80_load_membership_records.objects.all().delete()
        s80_load_membership_records_clubs.objects.all().delete()   

def delete_s80_tables():
        s80_club_records.objects.all().delete()
        s80_membership_records.objects.all().delete()
        s80_membership_records_clubs.objects.all().delete()


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

        DEBUG_WRITE = False
        load_dotenv()

        s80 = eval(os.environ.get("SPORT80_DEBUG"))
        f.write("SPORT80_DEBUG:  " + str(s80) + "\n")
        access_token = os.environ.get("SPORT80_MEMBERSHIP_ACCESS_TOKEN")

        record_log_data("assn_mgr_s80_load_membership_clubs", "Application", "Starting")

        #do not run during testing to save time
        record_log_data("assn_mgr_s80_load_membership_clubs", "delete_s80_load_tables", "Starting")
        delete_s80_load_tables()  #do not delete during testing to save time
        record_log_data("assn_mgr_s80_load_membership_clubs", "delete_s80_load_tables", "Completed")

        record_log_data("assn_mgr_s80_load_membership_clubs", "load_s80_clubs", "Starting")
        load_s80_clubs(f, access_token, 50, 0, s80, DEBUG_WRITE)
        record_log_data("assn_mgr_s80_load_membership_clubs", "load_s80_clubs", "Completed")

        record_log_data("assn_mgr_s80_load_membership_clubs", "load_s80_memberships", "Starting")
        load_s80_memberships(f, access_token, 50, 0, s80, DEBUG_WRITE)
        record_log_data("assn_mgr_s80_load_membership_clubs", "load_s80_memberships", "Completed")

        delete_s80_tables()  #only for testing

        record_log_data("assn_mgr_s80_load_membership_clubs", "create_blank_s80_club_records", "Starting")
        create_blank_s80_club_records(f)
        record_log_data("assn_mgr_s80_load_membership_clubs", "create_blank_s80_club_records", "Completed")

        record_log_data("assn_mgr_s80_load_membership_clubs", "populate_s80_clubs", "Starting")
        populate_s80_clubs(f, DEBUG_WRITE)
        record_log_data("assn_mgr_s80_load_membership_clubs", "populate_s80_clubs", "Completed")

        record_log_data("assn_mgr_s80_load_membership_clubs", "populate_s80_memberships", "Starting")
        populate_s80_memberships(f, DEBUG_WRITE)
        record_log_data("assn_mgr_s80_load_membership_clubs", "populate_s80_memberships", "Completed")

        record_log_data("assn_mgr_s80_load_membership_clubs", "populate_s80_membership_clubs", "Starting")
        populate_s80_membership_clubs(f, DEBUG_WRITE)
        record_log_data("assn_mgr_s80_load_membership_clubs", "populate_s80_membership_clubs", "Completed")

        record_log_data("assn_mgr_s80_load_membership_clubs", "Application", "Completed")

        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()
 
        #Email log file
#        send_attachment(fname)
#        os.remove(fname)

#python manage.py runscript assn_mgr_s80_load_members_clubs

#dev
#assn_mgr_s80_club_records 1156
#assn_mgr_s80_membership_records 75359
#assn_mgr_s80_membership_records_clubs 75372


