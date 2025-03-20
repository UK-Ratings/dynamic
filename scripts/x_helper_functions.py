#!/usr/bin/env python3

from base.models import *
from django.utils import timezone
from django.db import transaction
from dateutil import parser
from django.contrib import messages
from django.utils.translation import get_language
from dateutil.relativedelta import relativedelta
from rapidfuzz import process, fuzz
import pytz
from datetime import datetime
import csv
from django.apps import apps
from django.db import connection
from django.db.models import F, Func, Value
from django.db.models import Q

from assn_mgr.models import *    
from club_mgr.models import *
from base.models import *
from tourneys.models import *
from users.models import *

import math
import os
import requests
import json
import io
import shutil
from django.urls import reverse
from django.core.mail import send_mail, get_connection, EmailMessage
from django.template.loader import render_to_string
from django.utils.translation import get_language

from dotenv import load_dotenv
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")

class ReplaceF(Func):
    function = 'REPLACE'
    template = "%(function)s(%(expressions)s, '-', ' ')"


def copy_zbackup_files_if_exist(f, src_folder, dest_folder, DEBUG_WRITE):
    f.write("copy_zbackup_files_if_exist: " + str(timezone.now()) + "\n")
    # Ensure the destination folder exists
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Iterate over all files in the source folder
    for filename in os.listdir(src_folder):
        src_file = os.path.join(src_folder, filename)
        dest_file = os.path.join(dest_folder, filename)

        # Check if the file exists in the source folder
        if os.path.isfile(src_file):
            try:
                shutil.copy2(src_file, dest_file)
                print(f"Copied {src_file} to {dest_file}")
                f.write(f"Copied {src_file} to {dest_file}")
            except Exception as e:
                print(f"Failed to copy {src_file} to {dest_file}. Reason: {e}")
                f.write(f"Failed to copy {src_file} to {dest_file}. Reason: {e}")
        else:
            print(f"File {src_file} does not exist.")
            f.write(f"File {src_file} does not exist.")


#def get_country_from_ip(ip_address):
#    try:
#        response = requests.get(f'https://ipinfo.io/{ip_address}/json')
#        data = response.json()
#        return data.get('country', 'Unknown')
#    except requests.RequestException as e:
#        return 'Unknown'

#def determine_country(request):
#    ip_address = request.GET.get('ip', '')
#    if ip_address:
#        country = get_country_from_ip(ip_address)
#        return JsonResponse({'ip': ip_address, 'country': country})
#    else:
#        return JsonResponse({'error': 'IP address not provided'}, status=400)
    
def record_page_data(python_app, function_name, request):
        if request.user.is_authenticated:
                cuser = request.user
        else:
                cuser = 'AnonymousUser'
        remote_address = request.META['REMOTE_ADDR']
        user_language = request.META['HTTP_ACCEPT_LANGUAGE']
        user_agent = request.META['HTTP_USER_AGENT']
        user_referer = request.META.get('HTTP_REFERER', '')
        user_language = get_language()
        user_device = request.user_agent.device.family
        user_os = request.user_agent.os.family
        user_browser = request.user_agent.browser.family
        log = log_page_data(
                page_current_datetime = timezone.now(),
                page_python_app = python_app[:100],
                page_function_name = function_name[:500],
                page_user = cuser,
                page_user_ip = remote_address[:100],
                page_user_agent = user_agent[:500],
                page_user_referer = user_referer[:500],
                page_user_language = user_language[:100],
                page_user_device = user_device[:100],
                page_user_os = user_os[:100],
                page_user_browser = user_browser[:100]
                )
        log.save()
def record_log_data(python_app, function_name, function_message):
        log = log_progress_data(
                current_datetime=timezone.now(),
                python_app=python_app,
                function_name=function_name,
                function_message=function_message
        )
        log.save()
def record_message(request, python_app, function_name, fcnt_messages):
        for x in fcnt_messages:
                msg = log_messages(
                        current_datetime=timezone.now(),
                        python_app=python_app,
                        user_name=request.user.username,
                        function_name=function_name,
                        function_message=x[0] + ' ' + x[1]
                )
                msg.save()
                #'silent' will not be displayed
                if x[1] == 'success':
                        messages.success(request, x[0])
                elif x[1] == 'info':
                        messages.info(request, x[0])
                elif x[1] == 'warning':
                        messages.warning(request, x[0])
                elif x[1] == 'error':
                        messages.error(request, x[0])
def record_error_data(python_app, function_name, given_error_level, given_error_message):
        if(given_error_level.lower() in ('info', 'warning', 'error')):
                e_level = given_error_level.title()
                e_message = given_error_message
        else:
                e_level = 'Error'
                e_message = 'Invalid error level: ' + given_error_level
        log = log_error_data(
                current_datetime=timezone.now(),
                python_app=python_app,
                function_name=function_name,
                error_level=e_level,
                error_message=e_message
        )
        log.save()

def process_workflow_args(f, args, process_days_back, process_days_out, DEBUG_WRITE):
        datetime_format = '%m/%d/%Y'
        ls_date = None
        le_date = None
        le_date_future = None
        reset_string = ""
        load_data = True

        if 'noload' in args:
                load_data = False
        if 'reset' in args:
                reset_string = "reset"
                ls_date = Make_String_Timezone_Aware("01/01/2022")
                le_date = timezone.now() + relativedelta(days=1)
                le_date_future = timezone.now() + relativedelta(days=process_days_out)

        found_one_date = False
        for x in args:
                try:
                        Make_String_Timezone_Aware(x)
                except:
                        pass
                else:
                        if(found_one_date == True):
                                le_date = Make_String_Timezone_Aware(x)
                                le_date_future = le_date
                        if(found_one_date == False):
                                ls_date = Make_String_Timezone_Aware(x)
                                found_one_date = True

        if(le_date is None):
                le_date = timezone.now() + relativedelta(days=1)
                le_date_future = timezone.now() + relativedelta(days=process_days_out)

        if(ls_date is None):
                ls_date = timezone.now() - relativedelta(days=int(process_days_back)) 
                le_date = timezone.now() + relativedelta(days=1)
                le_date_future = timezone.now() + relativedelta(days=process_days_out)

        ls_date_str = ls_date.strftime(datetime_format)
        le_date_str = le_date.strftime(datetime_format)
        le_date_future_str = le_date_future.strftime(datetime_format)

        if(DEBUG_WRITE):
                f.write("args: ")
                for qq in args:
                        f.write(str(qq) + " ")
                f.write("\n")

                f.write("New Start Date: " + str(ls_date) + " " + str(ls_date_str) + "\n")
                f.write("New End Date: " + str(le_date) + " " + str(le_date_str) + "\n")
                f.write("New End Date Future: " + str(le_date_future) + " " + str(le_date_future_str) + "\n")
                f.write("reset_string: " + str(reset_string) + "\n")
                f.write("load_data: " + str(load_data) + "\n")

        return ls_date, le_date, le_date_future, reset_string, load_data, ls_date_str, le_date_str, le_date_future_str

def delete_files_in_directory_by_extension(f, directory, fileextension):
    f.write("delete_files_in_directory_by_extension: " + str(timezone.now()) + "\n")
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) and file_path.endswith(fileextension):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            f.write(f"Failed to delete {file_path}. Reason: {e}\n")
    f.write("Completed delete_files_in_directory_by_extension: " + str(fileextension)+" "+ str(timezone.now()) + "\n")

def delete_all_files_in_directory(f, directory):
        f.write("delete_all_files_in_directory: " + str(timezone.now()) + "\n")
        for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                                os.unlink(file_path)
                        elif os.path.isdir(file_path):
                                shutil.rmtree(file_path)
                except Exception as e:
                        f.write(f"Failed to delete {file_path}. Reason: {e}")
        f.write(" Completed delete_all_files_in_directory: " + str(timezone.now()) + "\n")
def comms_email_connection():
    email_connection = get_connection(
        host=os.environ.get("EMAIL_HOST"),
        username=os.environ.get("EMAIL_COMMS_USERNAME"),
        password=os.environ.get("EMAIL_COMMS_PASSWORD"),
        port=os.environ.get("EMAIL_PORT"), 
        use_tls=os.environ.get("EMAIL_USE_TLS"),
        fail_silently=False
    )
    return email_connection

#        email_contact('message name', 'ukratingsinfo@gmail.com', 'message')
def email_contact(message_type, message_name, message_email, message, message_first_name, message_last_name, message_full_name, message_username):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        msg_plain = 'Best Viewed in HTML'
        file_path = 'base/templates/emails'
        if(message_type == 'contact'):
                file_name = 'email_template_contact.html'
                email_title = 'British Fencing - UK Ratings Pilot - Contact'
                attachment_path = os.path.join(project_root, file_path, file_name)
                msg_html = render_to_string(attachment_path, {
                        'message_name': message_name,
                        'message_email': message_email,
                        'message': message,
                })
        elif(message_type == 'new_reg'):
                file_name = 'email_template_new_reg.html'
                email_title = 'British Fencing - UK Ratings Pilot - New Registaration'
                attachment_path = os.path.join(project_root, file_path, file_name)
                msg_html = render_to_string(attachment_path, {
                        'firstname': message_first_name,
                        'lastname': message_last_name,
                        'emailaddress': message_email,                       
                        })
        elif(message_type == 'data_change'):
                file_name = 'email_template_data_change.html'
                email_title = 'British Fencing - UK Ratings Pilot - Your Data Changed'
                attachment_path = os.path.join(project_root, file_path, file_name)
                msg_html = render_to_string(attachment_path, {
                        'firstname': message_first_name,})
        send_mail(
                email_title,
                msg_plain,
                os.environ.get("EMAIL_COMMS_USERNAME"),
                [message_email, os.environ.get("EMAIL_COMMS_USERNAME")],
#                [message_email],
                connection=comms_email_connection(),
                html_message=msg_html
        )
def email_with_attachment(subject, message, recipient_list, file_path, file_name):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        attachment_path = os.path.join(project_root, file_path, file_name)

        fe = os.environ.get("EMAIL_COMMS_USERNAME")
        email = EmailMessage(
                subject,
                message,
                fe,
                recipient_list,
                connection=comms_email_connection()
        )
        if attachment_path:
                email.attach_file(attachment_path)
        email.send()

def send_email_with_attachments(f, subject, message, recipient_list, file_paths, DEBUG_WRITE):
    if(DEBUG_WRITE):
           f.write("send_email_with_attachments: " + subject + " " + str(timezone.now()) + "\n")
    """
    Send an email with multiple file attachments.

    :param subject: Subject of the email
    :param message: Body of the email
    :param from_email: Sender's email address
    :param recipient_list: List of recipient email addresses
    :param file_paths: List of file paths to attach
    """
    email = EmailMessage(subject, message, os.environ.get("EMAIL_COMMS_USERNAME"), recipient_list)
    for file_path in file_paths:
#        if(DEBUG_WRITE):
#            f.write("Attaching file: " + str(file_path) + "\n")
        try:
            with open(file_path, 'rb') as f:
                email.attach(file_path, f.read())
        except Exception as e:
                f.write("Error attaching file {file_path}: {e}" + "\n")
    email.send()
#    if(DEBUG_WRITE):
#           f.write("send_email_with_attachments complete: " + str(timezone.now()) + "\n")


def is_association(asn_number):
#    record_log_data("tourneys-view.py", "is_association", "assn number: " + str(asn_number))
    assn_exists = associations.objects.filter(assn_number=asn_number).exists()
#    record_log_data("tourneys-view.py", "is_association", "assn number: " + str(asn_number) + " result: " + str(assn_exists))
    return assn_exists
def is_association_with_record(asn_number):
#        record_log_data("tourneys-view.py", "is_association_with_record", "assn number: " + str(asn_number))
        try:
                assn_exists = associations.objects.get(assn_number=asn_number)
        except:
                assn_exists = False
#        record_log_data("tourneys-view.py", "is_association_with_record", "assn number: " + str(asn_number) + " result: " + str(assn_exists))
        return assn_exists
def is_member_by_identifier(asn, member_identifier):
#    record_log_data("tourneys-view.py", "is_member", "member number: " + str(member_identifier))
    member_exists = association_members.objects.filter(assn = asn, assn_member_identifier=member_identifier).exists()
#    record_log_data("tourneys-view.py", "is_member", "member number: " + str(member_identifier) + " result: " + str(member_exists))
    return member_exists
def is_member_by_identifier_with_record(asn, member_identifier):
#        record_log_data("tourneys-view.py", "is_member_by_identifier_with_record", "member identifier: " + str(member_identifier))
        try:
                member_exists = association_members.objects.get(assn = asn, assn_member_identifier=member_identifier)
        except:
                member_exists = False
#        record_log_data("tourneys-view.py", "is_member_by_identifier_with_record", "member identifier: " + str(member_identifier) + " result: " + str(member_exists))
        return member_exists
def is_member(asn, member_num):
#    record_log_data("tourneys-view.py", "is_member", "member number: " + str(member_num))
    if(member_num.isnumeric()):
        member_exists = association_members.objects.filter(assn = asn, assn_member_number=member_num).exists()
    else:
        member_exists = False
#    record_log_data("tourneys-view.py", "is_member", "member number: " + str(member_num) + " result: " + str(member_exists))
    return member_exists
def is_member_with_record(asn, member_num):
#        record_log_data("tourneys-view.py", "is_member_with_record", "member number: " + str(member_num))
        if(member_num.isnumeric()):
                try:
                        member_exists = association_members.objects.get(assn = asn, assn_member_number=member_num)
                except:
                        member_exists = False
        else:
                member_exists = False
#        record_log_data("tourneys-view.py", "is_member_with_record", "member number: " + str(member_num) + " result: " + str(member_exists))
        return member_exists
def is_member_number(member_num):
#    record_log_data("tourneys-view.py", "is_member_number", "member number: " + str(member_num))
    if(member_num.isnumeric()):
        try:
                member_exists = association_members.objects.get(assn_member_number=member_num)
        except:
                member_exists = False
    else:
        member_exists = False
#    record_log_data("tourneys-view.py", "is_member_number", "member number: " + str(member_num) + " result: " + str(member_exists))
    return member_exists
def is_member_number_with_record(member_num):
#    record_log_data("tourneys-view.py", "is_member_number_with_record", "member number: " + str(member_num))
    if(member_num.isnumeric()):
        try:
                member_exists = association_members.objects.get(assn_member_number=member_num)
        except:
                member_exists = False
    else:
        member_exists = False
#    record_log_data("tourneys-view.py", "is_member_number_with_record", "member number: " + str(member_num) + " result: " + str(member_exists))
    return member_exists
def is_tourney_admin(tourney_num, user_id):
#    record_log_data("tourneys-view.py", "tourney_admin", "tourney: " + str(tourney_num) + " user: " + str(user_id))
    in_admins_exists = tournament_admins.objects.filter(tourney__tourney_number=tourney_num, tourney_admin__email=user_id).exists()
    is_tourney_admin = in_admins_exists
#    record_log_data("tourneys-view.py", "tourney_admin", "tourney: " + str(tourney_num) + " user: " + str(user_id) + " result: " + str(is_tourney_admin))
    return is_tourney_admin
def is_tourney(tourney_num):
#    record_log_data("tourneys-view.py", "is_tourney", "tourney: " + str(tourney_num))
    in_tourney_exists = tournaments.objects.filter(tourney_number=tourney_num).exists()
#    record_log_data("tourneys-view.py", "is_tourney", "tourney: " + str(tourney_num) + " result: " + str(in_tourney_exists))
    return in_tourney_exists
def is_event(event_num):
#    record_log_data("tourneys-view.py", "is_event", "event: " + str(event_num))
    in_event_exists = events.objects.filter(ev_number=event_num).exists()
#    record_log_data("tourneys-view.py", "is_event", "event: " + str(event_num) + " result: " + str(in_event_exists))
    return in_event_exists
def is_event_round(er_round_n):
#    record_log_data("tourneys-view.py", "is_event_round", "event round: " + str(er_round_n))
    in_event_round_exists = event_rounds.objects.filter(er_round_num=er_round_n).exists()
#    record_log_data("tourneys-view.py", "is_event", "event: " + str(er_round_n) + " result: " + str(in_event_round_exists))
    return in_event_round_exists
def is_event_round_pool(er_pool_n):
#    record_log_data("tourneys-view.py", "is_event_round_pool", "event round pool: " + str(er_pool_n))
    in_event_round_pool_exists = event_round_pool_details.objects.filter(erpd_pool_num=er_pool_n).exists()
#    record_log_data("tourneys-view.py", "is_event_round_pool", "pool: " + str(er_pool_n) + " result: " + str(in_event_round_pool_exists))
    return in_event_round_pool_exists


def get_system_process_user():
        try:
                sys_user = User.objects.get(username='Ftmanageruser@gmail.com')
        except:
                sys_user = None
                record_error_data('x_helper_functions', 'get_system_process_user', 'error', 'cannot find system process user')
        return sys_user
def base_get_next_system_value(sys_val):
        max_id = 0
        obj = system_values.objects.get(value_name=sys_val)
        if obj is not None:
                max_id = obj.value_int
                obj.value_int = max_id + 1
                obj.save()
        return max_id
def base_get_current_language():
    current_language = get_language()
    lg_id = language.objects.get(language_code=current_language)
    return lg_id
def base_get_default_language():
    lg_id = system_values.objects.get(value_name='default_language')
    return lg_id.value_language
def base_get_categories(lg_id):
    if(lg_id is None):
        lg_id = base_get_default_language()
    sv = system_values.objects.filter(value_group='category', value_language=lg_id)
    return sv                                      
def base_get_event_types(lg_id):
    if(lg_id is None):
        lg_id = base_get_default_language()
    sv = system_values.objects.filter(value_group='event_type', value_language=lg_id)
    return sv
def base_get_gender(lg_id):
    if(lg_id is None):
        lg_id = base_get_default_language()
    sv = system_values.objects.filter(value_group='gender', value_language=lg_id)
    return sv
def base_get_weapons(lg_id):
    if(lg_id is None):
        lg_id = base_get_default_language()
    sv = system_values.objects.filter(value_group='weapon', value_language=lg_id)
    return sv
def is_club_admin(club_num, user_id):
#    record_log_data("club_mgr-view.py", "is_club_admin", "club: " + str(club_num) + " user: " +str(user_id))
    in_admins = club_admins.objects.filter(club__club_number=club_num, club_admin__email=user_id)
    if(in_admins.count() > 0):
        is_club_admin = True   
    else:
        is_club_admin = False
#    record_log_data("club_mgr-view.py", "is_club_admin", "club: " + str(club_num) + " user: " +str(user_id) + "result: " + str(is_club_admin)) 
    return(is_club_admin)
def is_club(club_num):
#    record_log_data("club_mgr-view.py", "is_club", "club: " + str(club_num))
    in_club = clubs.objects.filter(club_number=club_num)
    if(in_club.count() > 0):
        is_club = True   
    else:
        is_club = False
#    record_log_data("club_mgr-view.py", "is_club", "club: " + str(club_num) + "result: " + str(is_club)) 
    return(is_club)
def is_club_with_rec(club_num):
#        record_log_data("club_mgr-view.py", "is_club_with_rec", "club: " + str(club_num))
        try:
                club_rec = clubs.objects.get(club_number=club_num)
        except:
                club_rec = False
#        record_log_data("club_mgr-view.py", "is_club_with_rec", "club: " + str(club_num) + "result: " + str(club_rec)) 
        return(club_rec)

def str_2_bool(v):
        return str(v).lower() in ("yes", "true", "t", "1")
def Make_String_Timezone_Aware(dt):   # 12/31/2022 "%m/%d/%Y"
        if(dt is not None and len(dt) > 0):
                dt_dt = parser.parse(dt)

                # Make the timezone object timezone-aware
                dt_aware = timezone.make_aware(dt_dt, timezone.get_default_timezone())
        else:
                dt_aware = None
        return(dt_aware)
def Make_Timezone_String_Timezone_Aware(date_str):
        tz_aware = None

        timezone = pytz.timezone('UTC')
        try:
                tz_aware = datetime.fromisoformat(date_str).astimezone(timezone)
        except:
                record_error_data('x_helper_functions', 'Make_Timezone_String_Timezone_Aware', 'error', 'Invalid timezone string: ' + date_str)
               
        return(tz_aware)

def build_tourney_url(request, tourney):
    base_url = request.build_absolute_uri('/')
    url_path = reverse('tourneys-tourney-detail', args=[str(tourney.tourney_number)]).lstrip('/')
    return(base_url + url_path)
def build_event_url(request, event):
        base_url = request.build_absolute_uri('/')
        if(event_final_results.objects.filter(efr_event=event).exists()):
                url_path = reverse('tourneys-event-final-results', args=[str(event.ev_number)]).lstrip('/')
                return(base_url + url_path)
        elif(event_registered_athletes.objects.filter(era_event=event).exists()):
                url_path = reverse('tourneys-event-registered-athletes', args=[str(event.ev_number)]).lstrip('/')
                return(base_url + url_path)
        elif(event_rounds.objects.filter(er_event=event).exists()):
                er= event_rounds.objects.filter(er_event=event).order_by('er_r_number').first()
                url_path = reverse('tourneys-event-round-info', args=[str(er.er_round_num)]).lstrip('/')
                return(base_url + url_path)
        else:
                return(build_tourney_url(request, event.ev_tourney))

def build_navbar_title_content(request, tourney, event, line1, line2, line3):
        navbar_title_content = []
        line1_uri = '#'
        line2_uri = '#'
        line3_uri = '#'
        if(tourney is not None):
                if line1 == tourney.tourney_name:
                        line1_uri = build_tourney_url(request, tourney)
                if line2 == tourney.tourney_name:
                        line2_uri = build_tourney_url(request, tourney)
                if line3 == tourney.tourney_name:
                        line3_uri = build_tourney_url(request, tourney)
        if(event is not None):
                if line1 == event.ev_name:
                        line1_uri = build_event_url(request, event)
                if line2 == event.ev_name:
                        line2_uri = build_event_url(request, event)
                if line3 == event.ev_name:
                        line3_uri = build_event_url(request, event)

        navbar_title_content.append(line1)
        navbar_title_content.append(line1_uri)
        navbar_title_content.append(line2)
        navbar_title_content.append(line2_uri)
        navbar_title_content.append(line3)
        navbar_title_content.append(line3_uri)
        return navbar_title_content
def build_event_title_icons(request, tourney_record, event_record):
    event_title_icons = []
    base_url = request.build_absolute_uri('/')

    #first is always tournament
    icon_record = []
    icon_record.append('Tournament')
    icon_record.append('bi bi-people')
    icon_record.append(base_url + reverse('tourneys-tourney-detail', args=[str(tourney_record.tourney_number)]).lstrip('/'))
    event_title_icons.append(icon_record)

    for x in event_rounds.objects.filter(er_event=event_record).order_by('er_r_number'):
        icon_record = []
        icon_record.append(x.er_r_type+ ' ' +x.er_r_number)
        icon_record.append('bi bi-border-all')
        icon_record.append(base_url + reverse('tourneys-event-round-info', args=[str(x.er_round_num)]).lstrip('/'))
        event_title_icons.append(icon_record)
        if(x.er_r_type.lower() == 'pool'):
                if(event_round_seeding.objects.filter(ers_round=x).exists()):
                        icon_record = []
                        icon_record.append('Event Round Seeding')
                        icon_record.append('bi bi-list-columns-reverse')
                        icon_record.append(base_url + reverse('tourneys-event-round-seeding', args=[str(x.er_round_num)]).lstrip('/'))
                        event_title_icons.append(icon_record)
                if(event_round_pool_assignments.objects.filter(erpa_pool_details__erpd_round=x).exists()):
                        icon_record = []
                        icon_record.append('Event Round Strip Assignments')
                        icon_record.append('bi bi-clipboard2-check')
                        icon_record.append(base_url + reverse('tourneys-event-round-pool-assignmernts', args=[str(x.er_round_num)]).lstrip('/'))
                        event_title_icons.append(icon_record)
                if(event_round_pool_results.objects.filter(erpr_round=x).exists()):
                        icon_record = []
                        icon_record.append('Event Round Results')
                        icon_record.append('bi bi-list-ol')
                        icon_record.append(base_url + reverse('tourneys-event-round-results', args=[str(x.er_round_num)]).lstrip('/'))
                        event_title_icons.append(icon_record)
                if(event_round_pool_results.objects.filter(erpr_round=x).exists()):
                        icon_record = []
                        icon_record.append('Event Round Grids')
                        icon_record.append('bi bi-grid-3x3')
                        icon_record.append(base_url + reverse('tourneys-event-round-grids', args=[str(x.er_round_num)]).lstrip('/'))
                        event_title_icons.append(icon_record)
                if(event_round_pool_results.objects.filter(erpr_round=x).exists()):
                        icon_record = []
                        icon_record.append('Pool Matches')
                        icon_record.append('bi bi-list-task')
                        icon_record.append(base_url + reverse('tourneys-event-round-poolmatches', args=[str(x.er_round_num)]).lstrip('/'))
                        event_title_icons.append(icon_record)
        else:
                if(event_round_pool_elimination_scores.objects.filter(erpes_round=x).exists()):
                        icon_record = []
                        icon_record.append('Elimination Bracket')
                        icon_record.append('bi bi-tsunami')
                        icon_record.append(base_url + reverse('tourneys-event-elim-bracket', args=[str(x.er_round_num)]).lstrip('/'))
                        event_title_icons.append(icon_record)

    if(event_final_results.objects.filter(efr_event=event_record).exists()):
        icon_record = []
        icon_record.append('Final Results')
        icon_record.append('bi bi-trophy')
        icon_record.append(base_url + reverse('tourneys-event-final-results', args=[str(event_record.ev_number)]).lstrip('/'))
        event_title_icons.append(icon_record)
    return event_title_icons
def build_event_title_icons_svg(request, tourney_record, event_record):
        event_title_icons = []
        event_title_icons_mobile = []
        base_url = request.build_absolute_uri('/')

    #first is always tournament
        icon_record = []
        icon_record.append('Tournament Events')
        icon_record.append("schedule-50.svg")
        icon_record.append(base_url + reverse('tourneys-tourney-detail', args=[str(tourney_record.tourney_number)]).lstrip('/'))
        icon_record.append(50)
        icon_record.append(0)
        event_title_icons.append(icon_record)

        if(event_registered_athletes.objects.filter(era_event=event_record).exists()):
                icon_record = []
                icon_record.append('Registered')
                icon_record.append('clipboard-50.svg')
                icon_record.append(base_url + reverse('tourneys-event-registered-athletes', args=[str(event_record.ev_number)]).lstrip('/'))
                icon_record.append(50)
                icon_record.append(0)
                event_title_icons.append(icon_record)

        cnt = 1
        for x in event_rounds.objects.filter(er_event=event_record).order_by('er_r_number'):
                if(x.er_r_type.lower() == 'pool'):
#                        icon_record = []
#                        icon_record.append('Round: ' + str(x.er_r_type)+ ' ' + str(x.er_r_number))
#                        icon_record.append("documents-50.svg")
#                        icon_record.append(base_url + reverse('tourneys-event-round-info', args=[str(x.er_round_num)]).lstrip('/'))
#                        icon_record.append(50)
#                        icon_record.append(cnt)
#                        event_title_icons.append(icon_record)

                        if(event_round_seeding.objects.filter(ers_round=x).exists()):
                                icon_record = []
                                icon_record.append('Pool ' + str(cnt) + ' - Seeding')
                                icon_record.append('list-50.svg')
                                icon_record.append(base_url + reverse('tourneys-event-round-seeding', args=[str(x.er_round_num)]).lstrip('/'))
                                icon_record.append(30)
                                icon_record.append(cnt)
                                event_title_icons.append(icon_record)
                        if(event_round_pool_assignments.objects.filter(erpa_pool_details__erpd_round=x).exists()):
                                icon_record = []
                                icon_record.append('Pool ' + str(cnt) + ' - Strip Assignments')
                                icon_record.append('report-card-50.svg')
                                icon_record.append(base_url + reverse('tourneys-event-round-pool-assignmernts', args=[str(x.er_round_num)]).lstrip('/'))
                                icon_record.append(30)
                                icon_record.append(cnt)
                                event_title_icons.append(icon_record)
                        if(event_round_pool_results.objects.filter(erpr_round=x).exists()):
                                icon_record = []
                                icon_record.append('Pool ' + str(cnt) + ' - Bout Order')
                                icon_record.append('user-groups-50.svg')
                                icon_record.append(base_url + reverse('tourneys-event-round-poolmatches', args=[str(x.er_round_num)]).lstrip('/'))
                                icon_record.append(30)
                                icon_record.append(cnt)
                                event_title_icons.append(icon_record)
                        if(event_round_pool_results.objects.filter(erpr_round=x).exists()):
                                icon_record = []
                                icon_record.append('Pool ' + str(cnt) + ' - Grids')
                                icon_record.append("grid-50.svg")
                                icon_record.append(base_url + reverse('tourneys-event-round-grids', args=[str(x.er_round_num)]).lstrip('/'))
                                icon_record.append(30)
                                icon_record.append(0)
                                event_title_icons.append(icon_record)
                        if(event_round_pool_results.objects.filter(erpr_round=x).exists()):
                                icon_record = []
                                icon_record.append('Pool ' + str(cnt) + ' - Results')
                                icon_record.append('numbers-50.svg')
                                icon_record.append(base_url + reverse('tourneys-event-round-results', args=[str(x.er_round_num)]).lstrip('/'))
                                icon_record.append(30)
                                icon_record.append(0)
                                event_title_icons.append(icon_record)
                else:
                        if(event_round_pool_elimination_scores.objects.filter(erpes_round=x).exists()):
                                icon_record = []
                                icon_record.append('Elimination Bracket')
                                icon_record.append('tournament-50.svg')
                                icon_record.append(base_url + reverse('tourneys-event-elim-bracket', args=[str(x.er_round_num)]).lstrip('/'))
                                icon_record.append(50)
                                icon_record.append(0)
                                event_title_icons.append(icon_record)
                cnt = cnt + 1

        if(event_final_results.objects.filter(efr_event=event_record).exists()):
                icon_record = []
                icon_record.append('Final Results')
                icon_record.append('medals-50.svg')
                icon_record.append(base_url + reverse('tourneys-event-final-results', args=[str(event_record.ev_number)]).lstrip('/'))
                icon_record.append(50)
                icon_record.append(0)
                event_title_icons.append(icon_record)
        event_title_icons_small_screen = None        
        #Not used - Saving in case need rows after user testing
#        event_title_icons_small_screen = [[None] * 10 for _ in range(10)]
#        if(len(event_title_icons) < 5):
#                event_title_icons_small_screen[0] = event_title_icons
#        else:
#                for x in event_title_icons:
#                        event_title_icons_small_screen[x[4]].append(x)    
        return event_title_icons, event_title_icons_small_screen


#Tournament Functions

def get_next_tournaments(max_records):
        tsd = timezone.now() - relativedelta(days=2)
        t_inbound = ['upcomingS80', 'upcomingLPJS', 'upcomingDurham']
        all_tourneys = tournaments.objects.filter(tourney_inbound__in=t_inbound,
                                                  tourney_start_date__gte = tsd,
                                                  ).order_by('tourney_start_date')
        return(all_tourneys[:max_records])
def is_tournament_with_rec(tourney_num):
#        record_log_data("club_mgr-view.py", "is_tournament_with_rec", "tourney: " + str(tourney_num))
        try:
                tourney_rec = tournaments.objects.get(tourney_number=tourney_num)
        except:
                tourney_rec = False
#        record_log_data("club_mgr-view.py", "is_tourney_with_rec", "tourney: " + str(tourney_num) + "result: " + str(tourney_rec)) 
        return(tourney_rec)
def zzzis_tournament_rated(f, tt, DEBUG_WRITE):
        rated = False
        fr = tournament_extra_fields.objects.filter(tef_tourney = tt, tef_field_name = "Final Ratings")
        if((fr.count() > 0) and (len(fr[0].tef_field1_value) > 1)):
                rated = True
        if(DEBUG_WRITE):
                f.write("tournament_rated: " + str(tt.tourney_name) + "   final_rated:" + str(rated) + " " + str(timezone.now()) + "\n")
        return(rated)
def is_tournament_rated(f, tt, DEBUG_WRITE):
        rated = True
        evs = events.objects.filter(ev_tourney = tt)
        for x in evs:
                final_rating = get_event_extra_field_value(f, x, "Final Rating", DEBUG_WRITE)
                if(final_rating is None or final_rating == 'NR'):
                        rated = False
                if(DEBUG_WRITE):
                        f.write("tournament_rated: " + str(tt.tourney_name) + " " + str(x.ev_name) + " event_rating: " + str(final_rating) + " " + str(timezone.now()) + "\n")
        if(DEBUG_WRITE):
                f.write("tournament_rated: " + str(tt.tourney_name) + "   final_rated:" + str(rated) + " " + str(timezone.now()) + "\n")
        return(rated)
def is_event_complete(f, ev, DEBUG_WRITE):
        if(event_final_results.objects.filter(efr_event = ev).count() > 0):
                efr = True
        else:
                efr = False
        if(DEBUG_WRITE):
                f.write("is_event_complete Returning: " + str(efr) + " for: " + str(ev.ev_name) + " " + str(timezone.now()) + "\n")
        return(efr)
def get_event_final_result(f, DEBUG_WRITE, event, efr_final_position, efr_given_name):
        if(DEBUG_WRITE):  
                f.write("                  get_event_final_result: " + str(event.ev_name) 
                        + " " + str(efr_final_position) + " " + str(efr_given_name) 
                        + " " + str(timezone.now()) + "\n")

        found_efr = None
        if(event != None and efr_final_position != None and efr_given_name != None):
                try:
                        event_final_results.objects.get(efr_event = event, 
                                        efr_final_position = efr_final_position, 
                                        efr_given_name = efr_given_name)
                except:
                        if(DEBUG_WRITE):  
                                f.write("                     Did not get final_event_position: \n")
                else:
                        found_efr = event_final_results.objects.get(efr_event = event, 
                                        efr_final_position = efr_final_position, 
                                        efr_given_name = efr_given_name)

        if(DEBUG_WRITE):  
                f.write("                   complete get_event_final_result: " + str(event.ev_name) 
                        + " " + str(efr_final_position) + " " + str(efr_given_name) 
                        + " " + str(timezone.now()) + "\n")
        return(found_efr)
def create_event_final_results_extra_fields(f, DEBUG_WRITE, efr):
        if(DEBUG_WRITE):  
                f.write("                           create_event_final_results_extra_fields: " + str(efr) + " " + str(timezone.now()) + "\n")

        asn = efr.efr_event.ev_tourney.tourney_assn
        for y in association_event_final_results_extra_fields.objects.filter(assn=asn):
                eef = event_final_results_extra_fields(
                        efr_event_final_results = efr,
                        efr_field_sequence = y.field_sequence,
                        efr_field_name = y.field_name,
                        efr_field_type = y.field_type,
                        efr_field_value = y.field_value,
                        efr_field_group = y.field_group,
                        efr_field_active = y.field_active)
                eef.save()
        if(DEBUG_WRITE):  
                f.write("                               complete create_event_final_results_extra_fields: " + str(efr) + " " + str(timezone.now()) + "\n")
def update_or_create_event_final_result(f, DEBUG_WRITE, event, efr, efr_final_position, efr_given_name, efr_given_club, efr_identifier, efr_assn_member_number):
        #key point:  if efr is None, then it is a new event_final_record.  
        # Use get_event_final_result before calling!
        if(DEBUG_WRITE):  
                f.write("                        update_or_create_event_final_result: " + str(event) 
                        + " " + str(efr) + " " + str(efr_final_position) + " " + str(efr_given_name) 
                        + " " + str(efr_given_club) + " " + str(timezone.now()) + "\n")

        if(efr is None):  #new_event
                new_efr = True
        else:
                new_efr = False

        uc_efr, created = event_final_results.objects.update_or_create(efr_event = event,
                        efr_final_position = efr_final_position, efr_given_name = efr_given_name, 
                        defaults={                        
                        'efr_given_member_identifier':efr_identifier,
                        'efr_assn_member_number':efr_assn_member_number,
                        'efr_given_club':efr_given_club
                        })

        if(new_efr):
                create_event_final_results_extra_fields(f, DEBUG_WRITE, uc_efr)
        if(DEBUG_WRITE):
                f.write("                         update_or_create_event_final_result returning: " + str(uc_efr) 
                        + " " + str(uc_efr.efr_given_name) + " at: " + str(timezone.now()) + "\n")
        return(uc_efr)
def get_event_round(f, DEBUG_WRITE, event, round_name, round_number):
        if(DEBUG_WRITE):  
                f.write("                  get_event_round: " + str(event.ev_name)
                        + " " + str(round_name) + " " + str(round_number) 
                        + " " + str(timezone.now()) + "\n")

        found_round = None
        if(round_number != None):
                try:
                        event_rounds.objects.get(er_round_num = round_number)
                except:
                        if(DEBUG_WRITE):  
                                f.write("                     Did not get_event_round: \n")
                else:
                        found_round = event_rounds.objects.get(er_round_num = round_number)
        if(found_round is None):
                try:
                        event_rounds.objects.get(er_event = event, er_r_number=round_name) 
                except:
                        if(DEBUG_WRITE):  
                                f.write("                     Did not get_event_round: \n")
                else:
                        found_round = event_rounds.objects.get(er_event = event, er_r_number=round_name)

        if(DEBUG_WRITE):  
                f.write("                   get_event_round returning: " + str(found_round) 
                                        + " " + str(event.ev_name) + " " + str(round_number) 
                                        + " " + str(timezone.now()) + "\n")
        return(found_round)
def update_or_create_event_round(f, DEBUG_WRITE, event, round, r_round_identifier, r_round, r_r_type, r_r_finished):
        #key point:  if event is None, then it is a new event.  
        # Use Get_Event_Rounds before calling!

        if(DEBUG_WRITE):  
                f.write("                        update_or_create_rounds: " + str(event.ev_name) 
                        + " " + str(round) + " " + str(r_round) + " " + str(timezone.now()) + "\n")

        if(round is None):  #new_event
                new_round = True
                r_number = base_get_next_system_value('next_event_round_id')
        else:
                new_round = False
                r_number = round.er_round_num
        uc_round, created = event_rounds.objects.update_or_create(er_event = event,
                        er_round_num = r_number, er_round_identifier = r_round_identifier,
                        er_r_number = r_round,
                        defaults={                        
                        'er_date_updated':timezone.now(),
                        'er_r_type':r_r_type,
                        'er_r_finished':r_r_finished,
                        })

        if(new_round or uc_round.er_date_added is None):
                if(DEBUG_WRITE):
                        f.write("                          Updating date added\n")
                event_rounds.objects.update_or_create(
                        id = uc_round.id,
                        defaults={
                        'er_date_added':timezone.now()})                
        if(DEBUG_WRITE):
                f.write("                         update_or_create_rounds returning: " + str(uc_round) 
                        + " " + str(uc_round.er_r_number) + " at: " + str(timezone.now()) + "\n")
        return(uc_round)
def get_event(f, DEBUG_WRITE, tourney, event_name, event_number):
        if(DEBUG_WRITE):  
                f.write("                  get_event: " + str(tourney.tourney_name) 
                        + " " + str(event_name) + " " + str(event_number) 
                        + " " + str(timezone.now()) + "\n")

        found_event = None
        if(event_number != None):
                try:
                        events.objects.get(ev_number = event_number)
                except:
                        if(DEBUG_WRITE):  
                                f.write("                     Did not get event: \n")
                else:
                        found_event = events.objects.get(ev_number = event_number)
        if(found_event is None):
                try:
                        events.objects.get(ev_name = event_name, ev_tourney=tourney) 
                except:
                        found_event = None
                        if(DEBUG_WRITE):  
                                f.write("                     Did not get event: \n")
                else:
                        found_event = events.objects.get(ev_name = event_name, ev_tourney=tourney)

        if(DEBUG_WRITE):  
                f.write("                   get_event returning: " + str(found_event) 
                                        + " " + str(tourney.tourney_name) 
                                        + " " + str(event_name) + " " + str(event_number) 
                                        + " " + str(timezone.now()) + "\n")
        return(found_event)
def zcreate_event_extra_fields(f, DEBUG_WRITE, event):
        if(DEBUG_WRITE):  
                f.write("                           create_event_extra_fields: " + str(event) + " " + str(timezone.now()) + "\n")

        asn = event.ev_tourney.tourney_assn
        for y in association_event_extra_fields.objects.filter(assn=asn):
                eef = event_extra_fields(
                        eev_event = event,
                        eev_field_sequence = y.field_sequence,
                        eev_field_name = y.field_name,
                        eev_field_type = y.field_type,
                        eev_field_value = y.field_value,
                        eev_field_group = y.field_group,
                        eev_field_active = y.field_active)
                eef.save()
        if(DEBUG_WRITE):  
                f.write("                               complete create_event_extra_fields: " + str(event) + " " + str(timezone.now()) + "\n")
def update_or_create_event(f, DEBUG_WRITE, tourney, event, event_name, 
                                ev_status, event_assn_type, event_assn_discipline, 
                                event_assn_gender, event_assn_ages, event_start_date):
        #key point:  if event is None, then it is a new event.  
        # Use Get_Event before calling!
        # if event is not None, then it ignores: event_name

        if(DEBUG_WRITE):  
                f.write("                        update_or_create_event: " + str(event) 
                        + " " + str(event) + " " + str(event_name) + " " + str(timezone.now()) + "\n")

        if(event is None):  #new_event
                new_event = True
                e_number = base_get_next_system_value('next_event_id')
                e_name = event_name
                if(ev_status is None):
                        e_status = event_status.objects.get(status="Upcoming")
                else:
                        e_status = event_status.objects.get(status__iexact=ev_status)
        else:
                new_event = False
                e_number = event.ev_number
                e_name = event.ev_name
                if(ev_status is None):
                        e_status = event.ev_status
                else:
                        e_status = event_status.objects.get(status__iexact=ev_status)

        uc_event, created = events.objects.update_or_create(ev_tourney = tourney,
                        ev_number = e_number, 
                        defaults={           
                        'ev_name':e_name,             
                        'ev_update_date':timezone.now(),
                        'ev_status':e_status,
                        'ev_assn_type':event_assn_type,
                        'ev_assn_discipline':event_assn_discipline,
                        'ev_assn_gender':event_assn_gender,
                        'ev_assn_ages':event_assn_ages,
                        'ev_start_date':event_start_date
                        })
        if(new_event or uc_event.ev_added_date is None):
                if(DEBUG_WRITE):
                        f.write("                          Updating date added\n")
                events.objects.update_or_create(
                        id = uc_event.id,
                        defaults={
                        'ev_added_date':timezone.now()})                
        if(DEBUG_WRITE):
                f.write("                         update_or_create_event returning: " + str(uc_event) 
                        + " " + str(uc_event.ev_name) + " at: " + str(timezone.now()) + "\n")
        return(uc_event)

def zzzget_tournament(f, DEBUG_WRITE, t_number, t_name, t_assn, 
                   t_start_date, t_up, t_inbound):
        s_date = t_start_date - relativedelta(days=90)
        e_date = t_start_date + relativedelta(days=90)
        found_tournament = None
        if(DEBUG_WRITE):  
                f.write("                  get_tournament: " + str(t_number) 
                        + "--" + str(t_name) + "--" + str(t_assn) 
                        + "--" + str(t_assn.assn_name) + "--" + str(t_start_date) 
                        + "--" + str(t_up) + "--" + str(t_inbound) 
                        + "--" + str(timezone.now()) + "\n")
        found_tournament = None
        if(t_number != None):
                try:
                        found_tournament = tournaments.objects.get(tourney_number = t_number)
                except tournaments.DoesNotExist:
                        if(DEBUG_WRITE):  
                                f.write("                     Did not get tournament: \n")
#'upcomingS80', 'upcomingLPJS', 'upcomingDurham'
        if(found_tournament is None and t_inbound == 'upcoming'):
                try:
                        found_tournament = tournaments.objects.get(tourney_name = t_name, tourney_assn=t_assn, 
                                                tourney_start_date__gte=s_date, tourney_start_date__lte=e_date, 
                                                tourney_inbound__iexact='upcoming')
                except tournaments.DoesNotExist:
                        if(DEBUG_WRITE):  
                                f.write("                     Did not get tournament upcoming: \n")
        if(found_tournament is None and t_inbound != 'upcoming'):
                try:
#                        f_tournament = tournaments.objects.filter(
#                                                tourney_name__iexact=t_name.lower(),
#                                                tourney_assn=t_assn,
#                                                tourney_start_date__gte=s_date, tourney_start_date__lte=e_date, 
#                                        ).exclude(tourney_inbound__iexact='upcoming')
#                        print(f_tournament, f_tournament.count())
#                        for x in f_tournament:
#                                if(DEBUG_WRITE):  
#                                        f.write("Found tournament NOT upcoming: " + str(x) + "\n")
                        found_tournament = tournaments.objects.filter(
                                                tourney_name__iexact=t_name.lower(),
                                                tourney_assn=t_assn,
                                                tourney_start_date__gte=s_date, tourney_start_date__lte=e_date, 
                                        ).exclude(tourney_inbound__iexact='upcoming').get()
                except tournaments.DoesNotExist:
                        if(DEBUG_WRITE):  
                                f.write("                     Did not get tournament NOT upcoming: \n")
        if(DEBUG_WRITE):  
                f.write("                   get_tournament returning: " + str(found_tournament) + " " 
                        + str(t_name) + " " + str(t_assn.assn_name) + "" + str(t_start_date) + " " + str(timezone.now()) + "\n")
        return(found_tournament)
def get_tournament(f, DEBUG_WRITE, t_number, t_name, t_assn, 
                   t_start_date, t_up, t_inbound):
        if(t_start_date is None):
               t_start_date = timezone.now()
        s_date = t_start_date - relativedelta(days=90)
        e_date = t_start_date + relativedelta(days=90)
        found_tournament = None
        if(DEBUG_WRITE):  
                f.write("                  get_tournament: " + str(t_number) 
                        + "--" + str(t_name) + "--" + str(t_assn) 
                        + "--" + str(t_assn.assn_name) + "--" + str(t_start_date) 
                        + "--" + str(t_up) + "--" + str(t_inbound) 
                        + "--" + str(timezone.now()) + "\n")
        found_tournament = None
        if(t_number != None):
                try:
                        found_tournament = tournaments.objects.get(tourney_number = t_number)
                except tournaments.DoesNotExist:
                        if(DEBUG_WRITE):  
                                f.write("                     Did not get tournament: \n")
        #'upcomingS80', 'upcomingLPJS', 'upcomingDurham'
        if(found_tournament is None and ('upcoming' in t_inbound)):
                try:
                        found_tournament = tournaments.objects.get(tourney_name = t_name, tourney_assn=t_assn, 
                                                tourney_start_date__gte=s_date, tourney_start_date__lte=e_date, 
                                                tourney_inbound__icontains='upcoming')
                except tournaments.DoesNotExist:
                        if(DEBUG_WRITE):  
                                f.write("                     Did not get tournament upcoming: \n")
        if(found_tournament is None and ('upcoming' not in t_inbound)):
                try:
                        found_tournament = tournaments.objects.filter(
                                                tourney_name__iexact=t_name.lower(),
                                                tourney_assn=t_assn,
                                                tourney_start_date__gte=s_date, tourney_start_date__lte=e_date,
                                                tourney_inbound__iexact=t_inbound 
                                        ).exclude(tourney_inbound__icontains='upcoming').get()
                except tournaments.DoesNotExist:
                        if(DEBUG_WRITE):  
                                f.write("                     Did not get tournament NOT upcoming: \n")
        if(DEBUG_WRITE):  
                f.write("                   get_tournament returning: " + str(found_tournament) + " " 
                        + str(t_name) + " " + str(t_assn.assn_name) + "" + str(t_start_date) + " " + str(timezone.now()) + "\n")
        return(found_tournament)
def update_or_create_tournament(f, DEBUG_WRITE, tourney, tourney_assn, tourney_name, 
                                tourney_status, tourney_start_date, tourney_end_date, 
                                tourney_entry_close_date, tourney_url, tourney_license,
                                tourney_results, tourney_override, tournament_entry_url, 
                                tournament_entry_list_url, tourney_inbound, tourney_upcoming, sys_user):
        #key point:  if tourney is None, then it is a new tournament.  
        # Use Get_Tournament before calling!
        # if tourney is not None, then it ignores: tourney_name, tourney_assn, tourney_start_date

        if(DEBUG_WRITE):  
                f.write("                        update_or_create_tournament: " + str(tourney) 
                        + " " + str(tourney_name) + " " + str(tourney_assn.assn_name) 
                        + " " + str(tourney_start_date) + " at: " + str(timezone.now()) + "\n")

        if(tourney is None):  #new_tournament
                new_tourney = True
                t_number = base_get_next_system_value('next_tournament_id')
                t_start_date = tourney_start_date
                t_assn = tourney_assn
                t_name = tourney_name
                if(tourney_upcoming):
                        t_status = tournament_status.objects.get(status="Upcoming")
                else:
                        t_status = tournament_status.objects.get(status__iexact=tourney_status)
        else:
                new_tourney = False
                t_number = tourney.tourney_number
                t_start_date = tourney.tourney_start_date
                t_assn = tourney.tourney_assn
                t_name = tourney.tourney_name
                if(tourney_upcoming):
                        t_status = tournament_status.objects.get(status="Upcoming")
                else:
                        t_status = tournament_status.objects.get(status__iexact=tourney_status)

        uc_tournament, created = tournaments.objects.update_or_create(
                        tourney_number = t_number, tourney_name = t_name, tourney_assn = t_assn,
                        tourney_start_date = t_start_date,
                        tourney_inbound = tourney_inbound,
                        defaults={
                        'date_updated':timezone.now(),
                        'tourney_status':t_status,
                        'tourney_end_date':tourney_end_date,
                        'tourney_entry_close_date': tourney_entry_close_date,
                        'tourney_url':tourney_url,
                        'tourney_license':tourney_license,
                        'tourney_override':tourney_override,
                        'tourney_results':tourney_results,
                        'tourney_entry_url':tournament_entry_url,
                        'tourney_entry_list_url':tournament_entry_list_url,
                        'tourney_upcoming':tourney_upcoming
                        })

        if(new_tourney or uc_tournament.date_added is None):
                if(DEBUG_WRITE):
                        f.write("                          Updating date added\n")
                tournaments.objects.update_or_create(
                        id = uc_tournament.id,
                        defaults={
                        'date_added':timezone.now()})                
        if(sys_user is not None):
                uc_tournament_user, created = tournament_admins.objects.update_or_create(
                        tourney = uc_tournament, tourney_admin = sys_user)

        if(DEBUG_WRITE):
                f.write("                         update_or_create_tournament returning: " + str(uc_tournament) 
                        + " " + str(uc_tournament.tourney_name) + " " 
                        + str(uc_tournament.tourney_assn.assn_name) 
                        + " " + str(uc_tournament.tourney_start_date) 
                        + " at: " + str(timezone.now()) + "\n")
        return(uc_tournament)
def get_tournament_extra_field_by_id(f, tourney_id, ex_field_name, ex_field_value5, ex_field_value4, ex_field_value3, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      get_tournament_extra_field_by_id: " + str(ex_field_name) + " " 
                        + str(ex_field_value5) + " " + str(ex_field_value4) + " " 
                        + str(ex_field_value3) + " " + str(timezone.now()) + "\n")
#        if(ex_field_name in ("Final Ratings", "Potential Ratings")):
        try:
                tef = tournament_extra_fields.objects.get(
                        tef_tourney__id=tourney_id, 
                        tef_field_name__iexact=ex_field_name.lower())
        except tournament_extra_fields.DoesNotExist:
                tef = None        
        if(DEBUG_WRITE):
                f.write(" COMPLETE: get_tournament_extra_field_by_id: " + str(tef) + " " + str(timezone.now()) + "\n")
        return (tef)

def get_tournament_extra_field(f, tourney, ex_field_name, ex_field_value5, ex_field_value4, ex_field_value3, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      get_tournament_extra_field: " + str(ex_field_name) + " " 
                        + str(ex_field_value5) + " " + str(ex_field_value4) + " " 
                        + str(ex_field_value3) + " " + str(timezone.now()) + "\n")
#        if(ex_field_name in ("Final Ratings", "Potential Ratings")):
        try:
                tef = tournament_extra_fields.objects.get(
                        tef_tourney=tourney, 
                        tef_field_name__iexact=ex_field_name.lower())
        except tournament_extra_fields.DoesNotExist:
                tef = None        
        if(DEBUG_WRITE):
                f.write(" COMPLETE: get_tournament_extra_field: " + str(tef) + " " + str(timezone.now()) + "\n")
        return (tef)
def update_or_create_tournament_extra_field(f, tourney, ex_field_name, ex_field_value, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      update_or_create_tournament_extra_field: " + str(tourney) 
                        + " " + str(ex_field_name) + " " + str(ex_field_value) + " " + str(timezone.now()) + "\n")
        ex_field_seq = 999
        if(ex_field_name == "Final Ratings"):
                ex_field_seq = 110
        if(ex_field_name == "Potential Ratings"):
                ex_field_seq = 100

        if(tourney is not None and ex_field_name is not None):
                uc_ef, created = tournament_extra_fields.objects.update_or_create(
                        tef_tourney=tourney,
                        tef_field_name = ex_field_name,
                        defaults={
                                'tef_field_date_updated': timezone.now(),
                                'tef_field1_value' : ex_field_value,
                                'tef_field_sequence': ex_field_seq,
                                'tef_field_active': True,
                                'tef_field_group': ex_field_name,
                                'tef_field1_type': "string",
                                })
        if(DEBUG_WRITE):
                f.write(" COMPLETE: update_or_create_tournament_extra_field: " + str(uc_ef) + " " + str(created) + " " + str(timezone.now()) + "\n")
        return (uc_ef)

def get_tournament_extra_field_value_by_id(f, tourney_id, ex_field_name, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      get_tournament_extra_field_value_by_id: " + str(ex_field_name) + " " + str(timezone.now()) + "\n")
        if(ex_field_name in ("Final Ratings", "Potential Ratings")):
                tef = get_tournament_extra_field_by_id(f, tourney_id, ex_field_name, "", "", "", DEBUG_WRITE)

        if(ex_field_name == "Final Ratings"):
                if(tef is not None):
                        return (tef.tef_field1_value)
                else:
                        return ("NR")
        if(ex_field_name == "Potential Ratings"):
                if(tef is not None):
                        return (tef.tef_field1_value)
                else:
                        return ("NR")
        return(None)

def get_tournament_extra_field_value(f, tourney, ex_field_name, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      get_tournament_extra_field_value: " + str(ex_field_name) + " " + str(timezone.now()) + "\n")
        if(ex_field_name in ("Final Ratings", "Potential Ratings")):
                tef = get_tournament_extra_field(f, tourney, ex_field_name, "", "", "", DEBUG_WRITE)

        if(ex_field_name == "Final Ratings"):
                if(tef is not None):
                        return (tef.tef_field1_value)
                else:
                        return ("NR")
        if(ex_field_name == "Potential Ratings"):
                if(tef is not None):
                        return (tef.tef_field1_value)
                else:
                        return ("NR")
        return(None)
def get_event_extra_field(f, event, ex_field_name, ex_field_value5, ex_field_value4, ex_field_value3, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      get_event_extra_field: " + str(ex_field_name) + " " 
                        + str(ex_field_value5) + " " + str(ex_field_value4) + " " 
                        + str(ex_field_value3) + " " + str(timezone.now()) + "\n")
#        if(ex_field_name in ("Difficulty", "Final Rating", "Potential Rating", "Fencers", "NIF", "BF Ranking Points")):
        try:
                eef = event_extra_fields.objects.get(
                        eev_event=event, 
                        eev_field_name__iexact=ex_field_name.lower())
        except event_extra_fields.DoesNotExist:
                eef = None        
        if(DEBUG_WRITE):
                f.write(" COMPLETE: get_event_extra_field: " + str(eef) + " " + str(timezone.now()) + "\n")
        return (eef)
def get_event_extra_field_value(f, event, ex_field_name, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      get_event_extra_field_value: " + str(ex_field_name) + " " + str(timezone.now()) + "\n")
        eef = get_event_extra_field(f, event, ex_field_name, "", "", "", DEBUG_WRITE)

        if(ex_field_name == "Difficulty"):
                if(eef is not None):
                        return (float(eef.eev_field1_value))
                else:
                        return (0.00)
        if(ex_field_name == "Final Rating"):
                if(eef is not None):
                        return (eef.eev_field1_value)
                else:
                        return ("NR")
        if(ex_field_name == "Potential Rating"):
                if(eef is not None):
                        return (eef.eev_field1_value)
                else:
                        return ("NR")
        if(ex_field_name == "Fencers"):
                if(eef is not None):
                        return (int(eef.eev_field1_value))
                else:
                        return (0)
        if(ex_field_name == "NIF"):
                if(eef is not None):
                        if(eef.eev_field1_value is not None):
                                return (int(eef.eev_field1_value))
                        else:
                                return(None)
                else:
                        return (0)
        if(ex_field_name == "BF Ranking Points"):
                if(eef is not None):
                        if eef.eev_field1_value == 'True':
                                return (True)
                        else:
                                return (False)
                else:
                        return (True)
        return(eef.eev_field1_value)
def update_or_create_event_extra_field(f, event, ex_field_name, ex_field_value, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      update_or_create_event_extra_field: " + str(event) 
                        + " " + str(ex_field_name) + " " + str(ex_field_value) + " " + str(timezone.now()) + "\n")
        ex_field_seq = 999
        if(ex_field_name == "Difficulty"):
                ex_field_seq = 110
        if(ex_field_name == "Final Rating"):
                ex_field_seq = 100
        if(ex_field_name == "Potential Rating"):
                ex_field_seq = 120
        if(ex_field_name == "Fencers"):
                ex_field_seq = 130
        if(ex_field_name == "NIF"):
                ex_field_seq = 140
        if(ex_field_name == "BF Ranking Points"):
                ex_field_seq = 150
        if(ex_field_name == "Potential Rating Distribution"):
                ex_field_seq = 160
        if(ex_field_name == "Final Rating Distribution"):
                ex_field_seq = 170
        if(ex_field_name == "Final Rating Top 8 Distribution"):
                ex_field_seq = 180
        if(ex_field_name == "Final Rating Top 12 Distribution"):
                ex_field_seq = 190
        if(ex_field_name == "Difficulty Calculation"):
                ex_field_seq = 200

        if(event is not None and ex_field_name is not None):
                uc_ef, created = event_extra_fields.objects.update_or_create(
                        eev_event=event,
                        eev_field_name = ex_field_name,
                        defaults={
                                'eev_field_date_updated': timezone.now(),
                                'eev_field1_value' : ex_field_value,
                                'eev_field_sequence': ex_field_seq,
                                'eev_field_active': True,
                                'eev_field_group': ex_field_name,
                                'eev_field1_type': "string",
                                })
        if(DEBUG_WRITE):
                f.write(" COMPLETE: update_or_create_event_extra_field: " + str(uc_ef) + " " + str(created) + " " + str(timezone.now()) + "\n")
        return (uc_ef)
def get_efr_extra_field(f, efr, ex_field_name, ex_field_value5, ex_field_value4, ex_field_value3, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      get_efr_extra_field: " + str(ex_field_name) + " " 
                        + str(ex_field_value5) + " " + str(ex_field_value4) + " " 
                        + str(ex_field_value3) + " " + str(timezone.now()) + "\n")
        if(ex_field_name in ("efr_final_points", "efr_previous_rating", "efr_rating", "efr_award_date")):
                try:
                        eef = event_final_results_extra_fields.objects.get(
                                efr_event_final_results=efr, 
                                efr_field_name__iexact=ex_field_name.lower())
                except event_final_results_extra_fields.DoesNotExist:
                        eef = None        
        if(DEBUG_WRITE):
                f.write(" COMPLETE: get_efr_extra_field: " + str(eef) + " " + str(timezone.now()) + "\n")
        return (eef)
def get_efr_extra_field_value(f, efr, ex_field_name, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("      get_efr_extra_field_value: " + str(ex_field_name) + " " + str(timezone.now()) + "\n")
#        if(ex_field_name in ("efr_final_points", "efr_previous_rating", "efr_rating", "efr_award_date")):
        eef = get_efr_extra_field(f, efr, ex_field_name, "", "", "", DEBUG_WRITE)

        if(ex_field_name == "efr_final_points"):
                if(eef is not None):
                        return (int(eef.efr_field_value))
                else:
                        return (0)
        if(ex_field_name == "efr_previous_rating"):
                if(eef is not None):
                        return (eef.efr_field_value)
                else:
                        return ("U")
        if(ex_field_name == "efr_rating"):
                if(eef is not None):
                        return (eef.efr_field_value)
                else:
                        return ("U")
        if(ex_field_name == "efr_award_date"):
                if(eef is not None):
                        datetime_str = eef.efr_field_value
                        datetime_format = "%Y-%m-%d %H:%M:%S%z"
                        # Parse the datetime string into a datetime object
                        try:
                                aware_datetime = datetime.strptime(datetime_str, datetime_format)
                                aw_date = str(aware_datetime.year)[2:4]
                                return aw_date
                        except:
                                return (0)
                else:
                        return (0)
        return(None)
def update_or_create_efr_extra_field(f, efr, ex_field_name, ex_field_value, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("                          BF_update_or_create_event_final_results_extra_field: " + str(efr) 
                        + " " + str(ex_field_name) + " " + str(ex_field_value) + " " + str(timezone.now()) + "\n")
        ex_field_seq = 999
        if(ex_field_name == "efr_final_points"):
                ex_field_seq = 10
                ex_field_type = "int"
        if(ex_field_name == "efr_previous_rating"):
                ex_field_seq = 20
                ex_field_type = "string"
        if(ex_field_name == "efr_rating"):
                ex_field_seq = 30
                ex_field_type = "string"
        if(ex_field_name == "efr_award_date"):
                ex_field_seq = 40
                ex_field_type = "datetime"

#        if(ex_field_seq <= 40):
        if(efr is not None and ex_field_name is not None):
                        uc_ef, created = event_final_results_extra_fields.objects.update_or_create(
                                efr_event_final_results=efr,
                                efr_field_name = ex_field_name,
                                defaults={
                                        'efr_field_date_updated': timezone.now(),
                                        'efr_field_value' : str(ex_field_value),
                                        'efr_field_sequence': ex_field_seq,
                                        'efr_field_active': True,
                                        'efr_field_group': ex_field_name,
                                        'efr_field_type': ex_field_type
                                        })
#        else:
#                msg = "Cannot find ex_field_name: " + str(ex_field_name) + " - " + str(timezone.now())
#                record_error_data('process_tournament', 'BF_update_or_create_efr_extra_field', 'error', msg)
#                if(DEBUG_WRITE):
#                        f.write("      BF_update_or_create_efr_extra_fields: " + msg + "\n")
        if(DEBUG_WRITE):
                f.write("                     COMPLETE: BF_update_or_create_event_final_results_extra_field: " + str(uc_ef) + " " + str(created) + " " + str(timezone.now()) + "\n")
        return (uc_ef)


def update_or_create_event_registered_athletes(f, DEBUG_WRITE, event, efr_given_name, efr_given_club, efr_identifier,efr_member_number):
        #key point:  if efr is None, then it is a new event_final_record.  
        # Use get_event_final_result before calling!
        if(DEBUG_WRITE):  
                f.write("                        update_or_create_event_registered_athletes: " + str(event) 
                        + str(efr_given_name) + " " + str(efr_given_club) + " " + str(timezone.now()) + "\n")
        if (efr_identifier is None):
                efr_identifier = 0
        if (efr_member_number is None):
                efr_member_number = 0

        uc_era, created = event_registered_athletes.objects.update_or_create(era_event = event,
                        era_given_name = efr_given_name, 
                        defaults={ 
                        'era_assn_member_number':efr_member_number,                       
                        'era_given_member_identifier':efr_identifier,
                        'era_given_club':efr_given_club
                        })

        if(DEBUG_WRITE):
                f.write("                         update_or_create_event_registered_athletes returning: " + str(uc_era) 
                        + " " + str(uc_era.era_given_name) + " at: " + str(timezone.now()) + "\n")
        return(uc_era)


#Address Functions

def GetLatLong(f, PostCode, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("  Get LatLong2: " + str(timezone.now()) + " PostCode: " + str(PostCode) + "\n")
        lat = 0
        long = 0
        real_lat_long = False
        if(PostCode is not None and len(PostCode) > 0):
        #        Pcode = "EX1 1AA"
        #        endpoint = "https://api.postcodes.io/postcodes/"+str(Pcode)
                if(PostCode[0] != "-"):
                        PCode = PostCode
                else:
                        PCode = PostCode[1:]
                endpoint = "https://api.postcodes.io/postcodes/"+str(PCode)
                lat = 0
                long = 0 

                if(DEBUG_WRITE):
                        f.write("   endpoint: " + endpoint + "\n")
                response = requests.get(endpoint)

                if(DEBUG_WRITE):
                        f.write("   API Status Code: " + str(response.status_code) + "\n")
                if(response.status_code == 200):
                        new_response = response.content.replace(b"'", b'"')
                        try:
                                json.loads(new_response)
                                if(DEBUG_WRITE):
                                        f.write("   Valid JSON\n")
                                dict = json.load(io.BytesIO(new_response))
        #                        pretty_json = json.dumps(dict, indent=4)
        #                        f.write(pretty_json)
                                lat = dict["result"]["latitude"]
                                long = dict["result"]["longitude"]
                        except json.JSONDecodeError:
                                f.write("   Invalid JSON...  Doing it hard way\n")
                                substring_index = response.content.decode('utf-8').find('longitude')
                                if substring_index != -1:
                                        right_side = response.content.decode('utf-8')[substring_index+11:]
                                        long_str = right_side[:right_side.find(",")]
                                substring_index = response.content.decode('utf-8').find('latitude')
                                if substring_index != -1:
                                        right_side = response.content.decode('utf-8')[substring_index+10:]
                                        lat_str = right_side[:right_side.find(",")]
                                if(DEBUG_WRITE):
                                        f.write("   Latitude String: " + str(lat_str)+" Longitude String: " + str(long_str) + "\n")   
                                if(len(lat_str) > 0 and len(long_str) > 0):
                                        try:
                                                float(long_str)
                                        except ValueError:
                                                if(DEBUG_WRITE):
                                                        f.write("   long_str error: " + long_str + "\n")
                                        else:
                                                long = float(long_str)
                                        try:
                                                float(lat_str)
                                        except ValueError:
                                                if(DEBUG_WRITE):
                                                        f.write("   lat_str error: " + lat_str[:20] + "\n")
                                        else:
                                                lat = float(lat_str)
        else:
                        if(DEBUG_WRITE):
                                f.write("   PostCode not long enough.  Defaulting\n")

        if (lat == 0 or long == 0):
                if(DEBUG_WRITE):
                        f.write("   Defaulting to North Sea...\n")
                lat = 52.045569
                long = 2.271475 
        else:
                real_lat_long = True

        if(DEBUG_WRITE):
                f.write("   Latitude: " + str(lat)+" Longitude: " + str(long) + "\n")
        return(lat,long, real_lat_long)
def zzzget_address(f, DEBUG_WRITE, addr_name, addr_line1, addr_line2, addr_line3, addr_city, 
                        addr_region, addr_region_abbr, addr_postal_code, addr_county, addr_country):
        if(DEBUG_WRITE):  
                f.write("                  get_address: " + str(addr_name) + " " + str(addr_line1) + " " + str(addr_postal_code) + " " + str(timezone.now()) + "\n")

        #this is to handle None in data
        if(addr_line1 is None):
                a1 = None
        else:
                a1 = addr_line1.title()
        if(addr_postal_code is None):
                apc = None
        else:
                apc = addr_postal_code.upper()

        try:
                found_address = address.objects.get(address_postcode = apc, address_line_1=a1)
        except:
                found_address = None
                if(DEBUG_WRITE):  
                        f.write("                     Did not get address: " + str(a1) + " " + str(apc) + " " + str(timezone.now()) + "\n")
#        else:
#                found_address = address.objects.get(address_postcode__iexact = apc, address_line_1=a1)

        if(DEBUG_WRITE):  
                f.write("                   get_address returning: " + str(found_address) + " " 
                        + str(a1) + " " + str(apc) + " " + str(timezone.now()) + "\n")
        return(found_address)
def update_or_create_address(f, DEBUG_WRITE, addr_name, addr_line1, addr_line2, addr_line3, addr_city, 
                             addr_region, addr_region_abbr, addr_postal_code, addr_county, addr_country):
    if DEBUG_WRITE:  
        f.write("                  update_or_create_address: " + str(addr_name) + " " + str(addr_line1) + " " + str(addr_postal_code) + " " + str(timezone.now()) + "\n")

    # Handle None in data
    a1 = addr_line1.title() if addr_line1 else None
    apc = addr_postal_code.upper() if addr_postal_code else None

    with transaction.atomic():
        found_address, created = address.objects.update_or_create(
            address_postcode=apc, address_line_1=a1,
            defaults={
                'address_name': addr_name.title() if addr_name else None,
                'address_line_1': addr_line1.title() if addr_line1 else None,
                'address_line_2': addr_line2.title() if addr_line2 else None,
                'address_line_3': addr_line3.title() if addr_line3 else None,
                'address_city': addr_city.title() if addr_city else None,
                'address_region': addr_region.title() if addr_region else None,
                'address_region_abbr': addr_region_abbr.title() if addr_region_abbr else None,
                'address_postcode': addr_postal_code.upper() if addr_postal_code else None,
                'address_county': addr_county.title() if addr_county else None,
                'address_country': addr_country.title() if addr_country else None,
                'address_lat': 52.045569,
                'address_long': 2.271475,
                'address_lat_long_real': False,
                'address_validated': False
            }
        )

    if DEBUG_WRITE:
        action = "created" if created else "updated"
        f.write(f"                     {action} address: {found_address.address_name} {found_address.address_line_1} {found_address.address_postcode} {timezone.now()}\n")
        f.write("                   update_or_create_address returning: " + str(found_address.address_name) + " " + str(found_address.address_line_1) + " " + str(found_address.address_postcode) + " " + str(timezone.now()) + "\n")

    return found_address
def calc_haversine_distance_km(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0
    
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Difference in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Distance in kilometers
    distance = R * c
    
    return distance

def zzzProcess_Addresses(f, all_addresses, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("Process_Addresses: " + str(all_addresses) + str(timezone.now()) + "\n")
    
    tot_addr = address.objects.count()
    if all_addresses:
        addr = address.objects.all().order_by('id')
    else:
        addr = address.objects.all().exclude(address_validated=True).order_by('id')

    if DEBUG_WRITE:
        print("all addresses: ", str(all_addresses) + "\n")
        print("To be processed: ", str(addr.count()) + " of " + str(tot_addr))
    if(1==1):
        f.write("To be processed: " + str(addr.count()) + " " + str(timezone.now()) + " of " + str(tot_addr) + "\n")

    ctr = 0
    batch_size = 500
    updates = []

    for x in addr:
        lat, long, real_latlong = GetLatLong(f, x.address_postcode, False)
#        print(x.address_postcode, lat, long, real_latlong)

        if real_latlong:
            x.address_lat = lat
            x.address_long = long
            x.address_validated = True
            updates.append(x)
        
        ctr += 1
        if ctr % batch_size == 0:
            if DEBUG_WRITE:
#                print("Processed: ", str(ctr))
                f.write("Processed: " + str(ctr) + " " + str(timezone.now()) + "\n")
            # Bulk update
            with transaction.atomic():
                address.objects.bulk_update(updates, ['address_lat', 'address_long', 'address_validated'])
            updates = []

    # Final bulk update for remaining records
    if updates:
        with transaction.atomic():
            address.objects.bulk_update(updates, ['address_lat', 'address_long', 'address_validated'])

    if DEBUG_WRITE:
        f.write(" COMPLETE: Process_Addresses: " + str(timezone.now()) + "\n")
        f.write(" Total Addresses: " + str(tot_addr) + " and address_validated=false: " + str(address.objects.all().exclude(address_validated=True).count()) + "\n")
        f.write("COMPLETE: Process_Addresses: " + str(timezone.now()) + "\n")

#Club Functions

def get_club(f, DEBUG_WRITE, club_number, club_name):

        found_club = None
        if(DEBUG_WRITE):  
                f.write("      get_club: " + str(club_number) + " " + str(club_name) + " " + str(timezone.now()) + "\n")
        try:
                clubs.objects.get(club_number = club_number)
        except:
                found_club = None
                if(DEBUG_WRITE):  
                        f.write("        Did not get club number: " + str(club_number) + " " + str(timezone.now()) + "\n")
        else:
                found_club = clubs.objects.get(club_number = club_number)
                if(DEBUG_WRITE):  
                        f.write("        get_club club_number found: " + str(club_number) + " " + str(found_club) + " " + str(timezone.now()) + "\n")

        if(found_club is None):
                try:
                        clubs.objects.get(club_name__iexact = club_name)
                except:
                        if(DEBUG_WRITE):  
                                f.write("        Did not get club: " + str(club_name) + " " + str(timezone.now()) + "\n")
                else:
                        found_club = clubs.objects.get(club_name__iexact = club_name)
                        if(DEBUG_WRITE):  
                                f.write("        get_club club_name found: " + str(club_name) + " " + str(found_club) + " " + str(timezone.now()) + "\n")

        if(DEBUG_WRITE):  
                f.write("      get_club returning: " + str(found_club) + " " 
                        + str(club_number) + " " + str(club_name) + " "  + str(timezone.now()) + "\n")
        return(found_club)
def get_club_force_association_lookup(f, DEBUG_WRITE, asn, assn_club_name, assn_club_number):
#this is unusual - forces name, club_number, and asn to exist, otherwise found_club = False
#used for loading from systems of record like Sport80
        st_timezone = timezone.now()
        found_club = None
        if(DEBUG_WRITE):
                f.write("         get_club_force_association_lookup: " + " " + str(asn) + " " + str(assn_club_name)
                                        + " " + str(assn_club_number) + " " + str(timezone.now()) + "\n")
        if(asn is None or len(assn_club_name) == 0 or assn_club_number == 0 ):
                f.write("          get_club_force_association_lookup:  Missing fields: " + str(timezone.now()) + "\n")
        else:  
                for a in clubs.objects.filter(club_name = assn_club_name):
                        for c in club_assn_clubs.objects.filter(club = a):
                                am = association_clubs.objects.get(assn_club_number=c.club_assn_club.assn_club_number)
                                if(am.assn == asn and am.assn_club_number == assn_club_number):
                                        found_club = clubs.objects.get(id=a.id)


        diff = timezone.now() - st_timezone
        diff_seconds = diff.total_seconds()
        if(DEBUG_WRITE):  
                f.write("         get_club_force_association_lookup from: " + " " + str(asn) + " " + str(assn_club_name)
                                        + " " + str(assn_club_number) + " " + str(timezone.now()) + "\n")
                if(found_club is None):
                        f.write("      get_club_force_association_lookup RETURNING NONE.  Total Time: " + str(diff_seconds) + " " + str(timezone.now()) + "\n")
                else:
                        f.write("      get_club_force_association_lookup RETURNING: "
                                + str(found_club.club_number)  
                                + " full name:" + str(found_club.club_name) 
                                + " Total Time: " + str(diff_seconds) 
                                + " " + str(timezone.now()) + "\n")
        return(found_club)
def get_update_or_create_club(f, asn, DEBUG_WRITE, found_club,
                                assn_club_number, assn_club_name, assn_club_url, assn_club_status,
                                assn_club_phone, assn_club_email, assn_club_description):
        found_club_new = False
        if(DEBUG_WRITE):
                f.write("      get_update_or_create_club: " + str(assn_club_name) + " " + str(assn_club_number) + " " + str(asn.assn_name) + " " + str(timezone.now()) + "\n")
        if found_club is None: # create club
                next_club_id = base_get_next_system_value('next_club_id')

                if(DEBUG_WRITE):  
                        f.write("         creating club: " + str(next_club_id) + " " + str(assn_club_name) + " " + str(timezone.now()) + "\n")
                found_club_new = True
                found_club = clubs(
                        club_number=None if next_club_id is None else next_club_id,
                        club_name=None if assn_club_name is None else assn_club_name.title(),
                        club_url=None if assn_club_url is None else assn_club_url,
                        club_status=None if assn_club_status is None else assn_club_status,
                        club_phone=None if assn_club_phone is None else assn_club_phone,
                        club_email=None if assn_club_email is None else assn_club_email,
                        club_description=None if assn_club_description is None else assn_club_description)
                found_club.save()

                if(DEBUG_WRITE):  
                        f.write("         created club: " + str(found_club.club_name) + " " + str(timezone.now()) + "\n")

        else:
                if(DEBUG_WRITE):  
                        f.write("         updating club: " + str(found_club.club_name) + " " + str(timezone.now()) + "\n")
#                found_club.club_number=None if assn_club_number is None else assn_club_number
                found_club.club_name=None if assn_club_name is None else assn_club_name.title()
                found_club.club_url=None if assn_club_url is None else assn_club_url
                found_club.club_status=None if assn_club_status is None else assn_club_status
                found_club.club_phone=None if assn_club_phone is None else assn_club_phone
                found_club.club_email=None if assn_club_email is None else assn_club_email
                found_club.club_description=None if assn_club_description is None else assn_club_description
                found_club.save()

        if(DEBUG_WRITE):  
                f.write("       get_update_or_create_club returning: " + str(found_club) + " " 
                        + str(assn_club_name) + " found_club_new=" + str(found_club_new) + str(timezone.now()) + "\n")
        return(found_club, found_club_new)


#Association Functions

def get_association(f, association_name, DEBUG_WRITE):
        try:
                associations.objects.get(assn_name__iexact=association_name)
        except:
                asn = None
                if(DEBUG_WRITE):  #association_ages
                        f.write("   Association does not exist\n")
        else:
                asn = associations.objects.get(assn_name=association_name)
        return(asn)
def move_association_clubs_to_clubs_new_details(f, asn, found_club, assn_club, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("          Setting up new club details: " + str(found_club.club_number) + " " + str(found_club.club_name)
                        + " " + str(assn_club.assn_club_number) + " " + str(assn_club.assn_club_name) 
                        + " " + str(timezone.now()) + "\n")

        assn_cl_ex_fields = association_club_extra_fields.objects.filter(assn_club__assn_club_number=assn_club.assn_club_number)
        if(len(assn_cl_ex_fields) > 0):
                for a in assn_cl_ex_fields:
                        caa, created = club_extra_fields.objects.update_or_create(
                                club=found_club, 
                                club_field_sequence = a.assn_club_field_sequence,
                                club_field_name = a.assn_club_field_name,
                                club_field_type = a.assn_club_field_type,
                                club_field_value = a.assn_club_field_value,
                                club_field_group = a.assn_club_field_group,
                                club_field_active = a.assn_club_field_active)
                if(DEBUG_WRITE):
                        f.write("           created assn_cl_ex_fields: " + str(len(assn_cl_ex_fields)) + " " + str(timezone.now()) + "\n")
        else:
                if(DEBUG_WRITE):
                        f.write("           Setting up DID NOT create assn_cl_ex_fields: " + str(len(assn_cl_ex_fields)) + " " + str(timezone.now()) + "\n")

        cl_addr_first = association_club_address.objects.filter(assn_club__assn_club_number=assn_club.assn_club_number).first()
        if cl_addr_first is not None:
                caa, created = club_address.objects.update_or_create(club=found_club, club_addr=cl_addr_first.assn_club_addr)
                if(DEBUG_WRITE):
                        f.write("           created club_address: " + str(caa) + " " + str(timezone.now()) + "\n")
        else:
                if(DEBUG_WRITE):
                        f.write("           Setting up DID NOT create club_address: " + str(caa) + " " + str(timezone.now()) + "\n")

        assn_cl_admins = association_club_admins.objects.filter(assn_club__assn_club_number=assn_club.assn_club_number)
        if(len(assn_cl_admins) > 0):
                for a in assn_cl_admins:
                        caa, created = club_admins.objects.update_or_create(club=found_club, club_admin = a.assn_club_admin)
                if(DEBUG_WRITE):
                        f.write("           created club_admins: " + str(len(assn_cl_admins)) + " " + str(timezone.now()) + "\n")
        else:
                if(DEBUG_WRITE):
                        f.write("           Setting up DID NOT create club_admins: " + str(len(assn_cl_admins)) + " " + str(timezone.now()) + "\n")

        assn_cl_ages = association_club_ages.objects.filter(assn_club__assn_club_number=assn_club.assn_club_number)
        if(len(assn_cl_ages) > 0):
                for a in assn_cl_ages:
                        caa, created = club_ages.objects.update_or_create(
                                club=found_club, 
                                club_age_name = a.assn_club_age_name,
                                club_age_value = a.assn_club_age_value)
                if(DEBUG_WRITE):
                        f.write("           created club_ages: " + str(len(assn_cl_ages)) + " " + str(timezone.now()) + "\n")
        else:
                if(DEBUG_WRITE):
                        f.write("           Setting up DID NOT create club_ages: " + str(len(assn_cl_ages)) + " " + str(timezone.now()) + "\n")

        assn_cl_disp = association_club_disciplines.objects.filter(assn_club__assn_club_number=assn_club.assn_club_number)
        if(len(assn_cl_disp) > 0):
                for a in assn_cl_disp:
                        caa, created = club_disciplines.objects.update_or_create(
                                club=found_club, 
                                club_discipline_name = a.assn_club_discipline_name,
                                club_discipline_name_value = a.assn_club_discipline_name_value)
                if(DEBUG_WRITE):
                        f.write("           created club disciplines: " + str(len(assn_cl_disp)) + " " + str(timezone.now()) + "\n")
        else:
                if(DEBUG_WRITE):
                        f.write("           Setting up DID NOT create club disciplines: " + str(len(assn_cl_disp)) + " " + str(timezone.now()) + "\n")
        if(DEBUG_WRITE):
                f.write("           Setting up new club details complete: " + str(found_club.club_number) + " " + str(found_club.club_number) + " " + str(found_club.club_name) + " " + str(timezone.now()) + "\n")
def move_association_clubs_to_clubs(f, association_name, DEBUG_WRITE):
        f.write("\nmove_association_clubs_to_clubs: " + str(association_name) + " " + str(timezone.now()) + "\n")

        asn = get_association(f, association_name, DEBUG_WRITE)
        for ac in association_clubs.objects.filter(assn=asn):
                if(DEBUG_WRITE):
                        f.write("   Association Club: " + str(ac.assn_club_number) + " " + str(ac.assn_club_name) + " " + str(timezone.now()) + "\n")
                found_club = get_club(f, DEBUG_WRITE, 0, ac.assn_club_name)
                found_club, found_club_new = get_update_or_create_club(f, asn, DEBUG_WRITE, found_club,
                                ac.assn_club_number, ac.assn_club_name, ac.assn_club_url, ac.assn_club_status,
                                ac.assn_club_phone, ac.assn_club_email, ac.assn_club_description)
                cac, created = club_assn_clubs.objects.update_or_create(club=found_club, club_assn_club=ac)
                if(DEBUG_WRITE):
                        f.write("    Created club_assn_clubs: " + str(cac) + " " + str(timezone.now()) + "\n")
                ca, created = club_assn.objects.update_or_create(club=found_club, club_assn=asn)
                if(DEBUG_WRITE):
                        f.write("    Created club_assn: " + str(ca) + " " + str(timezone.now()) + "\n")
                if(found_club_new):
                        move_association_clubs_to_clubs_new_details(f, asn, found_club, ac, DEBUG_WRITE)
def zzzmove_association_members_to_clubs(f, association_name, DEBUG_WRITE):
        f.write("move_association_members_to_clubs: " + str(association_name) + " " + str(timezone.now()) + "\n")
        asn = get_association(f, association_name, DEBUG_WRITE)

        club_members.objects.filter(club_assn_members__assn = asn).delete()

        for acm in association_club_members.objects.filter(assn_club_members__assn = asn):
                cac = club_assn_clubs.objects.get(club_assn_club = acm.assn_club)
                cm, created = club_members.objects.update_or_create(club = cac.club, club_assn_members = acm.assn_club_members)
def move_association_members_to_clubs(f, association_name, DEBUG_WRITE):
    f.write("move_association_members_to_clubs: " + str(association_name) + " " + str(timezone.now()) + "\n")
    asn = get_association(f, association_name, DEBUG_WRITE)

    with transaction.atomic():
        # Delete existing club members for the association
        club_members.objects.filter(club_assn_members__assn=asn).delete()

        # Collect new club members to be created
        new_club_members = []
        for acm in association_club_members.objects.filter(assn_club_members__assn=asn):
            cac = club_assn_clubs.objects.get(club_assn_club=acm.assn_club)
            new_club_members.append(club_members(
                club=cac.club,
                club_assn_members=acm.assn_club_members
            ))

        # Bulk create new club members
        club_members.objects.bulk_create(new_club_members)

    if DEBUG_WRITE:
        f.write("Completed: move_association_members_to_clubs: " + str(association_name) + " " + str(timezone.now()) + "\n")
def initial_association_club_values_from_association(f, found_club, asn, DEBUG_WRITE):
        if(DEBUG_WRITE):  
                f.write("      initial_association_club_values_from_association: " + str(found_club.assn_club_name) + " " + str(asn.assn_name) + " " + str(timezone.now()) + "\n")

        for a in association_ages.objects.filter(assn=asn):
                association_club_ages.objects.get_or_create(assn_club=found_club, assn_club_age_name=a.age_category_description, assn_club_age_value=True)
        for c in association_discipline.objects.filter(assn=asn):
                association_club_disciplines.objects.get_or_create(assn_club=found_club, assn_club_discipline_name=c.discipline_name, assn_club_discipline_name_value=True)

def get_assn_values_from_three_digits(f, asn, e_one, e_two, e_three, DEBUG_WRITE):
        discipline=None
        gender=None
        e_type=None
        ages=None

        if(('smf' in e_one) or ('smf' in e_two) or ('smf' in e_three)):
                discipline = association_discipline.objects.get(assn=asn, discipline_name = 'Foil')
                gender = association_genders.objects.get(assn=asn, gender_name__iexact = "Mixed")
                e_type = association_types.objects.get(assn=asn, type_category__iexact = "Individual")
                ages = association_ages.objects.get(assn=asn, age_category__iexact = "Senior")
        if (('swf' in e_one) or ('swf' in e_two) or ('swf' in e_three)):
                discipline = association_discipline.objects.get(assn=asn, discipline_name = 'Foil')
                gender = association_genders.objects.get(assn=asn, gender_name__iexact = "Women")
                e_type = association_types.objects.get(assn=asn, type_category__iexact = "Individual")
                ages = association_ages.objects.get(assn=asn, age_category__iexact = "Senior")
        if (('sme' in e_one) or ('sme' in e_two) or ('sme' in e_three)):
                discipline = association_discipline.objects.get(assn=asn, discipline_name = 'Epee')
                gender = association_genders.objects.get(assn=asn, gender_name__iexact = "Mixed")
                e_type = association_types.objects.get(assn=asn, type_category__iexact = "Individual")
                ages = association_ages.objects.get(assn=asn, age_category__iexact = "Senior")
        if (('swe' in e_one) or ('swe' in e_two) or ('swe' in e_three)):
                discipline = association_discipline.objects.get(assn=asn, discipline_name = 'Epee')
                gender = association_genders.objects.get(assn=asn, gender_name__iexact = "Women")
                e_type = association_types.objects.get(assn=asn, type_category__iexact = "Individual")
                ages = association_ages.objects.get(assn=asn, age_category__iexact = "Senior")
        if (('sms' in e_one) or ('sms' in e_two) or ('sms' in e_three)):
                discipline = association_discipline.objects.get(assn=asn, discipline_name = 'Sabre')
                gender = association_genders.objects.get(assn=asn, gender_name__iexact = "Mixed")
                e_type = association_types.objects.get(assn=asn, type_category__iexact = "Individual")
                ages = association_ages.objects.get(assn=asn, age_category__iexact = "Senior")
        if (('sws' in e_one) or ('sws' in e_two) or ('sws' in e_three)):
                discipline = association_discipline.objects.get(assn=asn, discipline_name = 'Sabre')
                gender = association_genders.objects.get(assn=asn, gender_name__iexact = "Women")
                e_type = association_types.objects.get(assn=asn, type_category__iexact = "Individual")
                ages = association_ages.objects.get(assn=asn, age_category__iexact = "Senior")

#        if(discipline is None):
#                record_error_data("x_helper_functions.py", "get_assn_values_from_three_digits", "warning",
#                                 "WARNING: couldnt find SMF, SWF, etc...: "
#                                        + " First Entry: " + str(e_one) 
#                                        + " Second Entry: " + str(e_two) 
#                                        + " Third Entry: " + str(e_three))
        return(discipline, gender, e_type, ages)
def get_assn_discipline_from_text(f, asn, entry_one, entry_two, entry_three, DEBUG_WRITE):
        discipline=None
        if(entry_one is not None):
                e_one = str(entry_one.lower())
        else:
                e_one = ""
        if(entry_two is not None):
                e_two = str(entry_two.lower())
        else:
                e_two = ""
        if(entry_three is not None):
                e_three = str(entry_three.lower())
        else:
                e_three = ""
        if 'é' in e_one:
                e_one = e_one.replace('é', 'e')
        if 'é' in e_two:
                e_two = e_two.replace('é', 'e')
        if 'é' in e_three:
                e_three = e_three.replace('é', 'e')
        if 'saber' in e_one:
                e_one = e_one.replace('saber', 'sabre')
        if 'saber' in e_two.lower():
                e_two = e_two.replace('saber', 'sabre')
        if 'saber' in e_three.lower():
                e_three = e_three.replace('saber', 'sabre')

        if(DEBUG_WRITE):
                f.write("get_assn_discipline_from_text:"  
                        + " First Entry: " + str(entry_one) + " e_one: " + str(e_one)
                        + " Second Entry: " + str(entry_two) + " e_two: " + str(e_two) 
                        + " Third Entry: " + str(entry_three) + " e_three: " + str(e_three) 
                        + " " + str(timezone.now()) + "\n")

        assn_disc = association_discipline.objects.filter(assn=asn)
        for x in assn_disc:
                if(e_one.find(x.discipline_name.lower()) != -1):
                        discipline = x
        if discipline is None:
                for x in assn_disc:
                        if(e_two.find(x.discipline_name.lower()) != -1):
                                discipline = x
        if discipline is None:
                for x in assn_disc:
                        if(e_three.find(x.discipline_name.lower()) != -1):
                                discipline = x
        if(discipline is None):
                discipline, gender, e_type, ages = get_assn_values_from_three_digits(f, asn, e_one, e_two, e_three, DEBUG_WRITE)

        if(discipline is None):
                if(DEBUG_WRITE):
                        f.write("                     get_assn_discipline_from_text: Discipline_Name set to Unknown\n")  
                record_error_data("x_helper_functions.py", "get_discipline", "warning",
                                 "WARNING: Defaulted to Unknown: "
                                        + " First Entry: " + str(e_one) 
                                        + " Second Entry: " + str(e_two) 
                                        + " Third Entry: " + str(e_three))
                discipline = association_discipline.objects.get(assn=asn, discipline_name__iexact = "Unknown")
        else:
                if(DEBUG_WRITE):
                        f.write(" Complete get_assn_discipline_from_text: "  
                                + "discipline_name = " + str(discipline.discipline_name) 
                                + " at " + str(timezone.now()) + "\n")
        return(discipline)
def get_assn_gender_from_text(f, asn, entry_one, entry_two, entry_three, DEBUG_WRITE):
        gender=None

        if(entry_one is not None):
                e_one = str(entry_one.lower())
        else:
                e_one = ""
        if(entry_two is not None):
                e_two = str(entry_two.lower())
        else:
                e_two = ""
        if(entry_three is not None):
                e_three = str(entry_three.lower())
        else:
                e_three = ""

        if(DEBUG_WRITE):
                f.write("get_assn_gender_from_text:"  
                        + " First Entry (lower): " + str(e_one) 
                        + " Second Entry (lower): " + str(e_two) 
                        + " Third Entry (lower): " + str(e_three) 
                        + " " + str(timezone.now()) + "\n")

        assn_gender = association_genders.objects.filter(assn=asn)

        #check e_one first
        for x in assn_gender:
                if(e_one.find(x.gender_name.lower()) != -1):
                        gender = x

        if (gender is None and e_one.find('boy') != -1):
                gender = association_genders.objects.get(assn=asn, gender_name = 'Men')
        if (gender is None and e_one.find('girl') != -1):
                gender = association_genders.objects.get(assn=asn, gender_name = 'Women')
        #check e_two next
        if gender is None:
                for x in assn_gender:
                        if(e_two.find(x.gender_name.lower()) != -1):
                                gender = x
        if (gender is None and e_two.find('boy') != -1):
                gender = association_genders.objects.get(assn=asn, gender_name = 'Men')
        if (gender is None and e_two.find('girl') != -1):
                gender = association_genders.objects.get(assn=asn, gender_name = 'Women')
        #check e_three last
        if gender is None:
                for x in assn_gender:
                        if(e_three.find(x.gender_name.lower()) != -1):
                                gender = x
        if (gender is None and e_three.find('boy') != -1):
                gender = association_genders.objects.get(assn=asn, gender_name = 'Men')
        if (gender is None and e_three.find('girl') != -1):
                gender = association_genders.objects.get(assn=asn, gender_name = 'Women')

        if(gender is None):
                discipline, gender, e_type, ages = get_assn_values_from_three_digits(f, asn, e_one, e_two, e_three, DEBUG_WRITE)
        if(gender is None):
                record_error_data("x_helper_functions.py", "get_assn_gender_from_text", "Warning",
                                 "WARNING: Defaulted to Unknown: "
                                        + " First Entry: " + str(e_one) 
                                        + " Second Entry: " + str(e_two) 
                                        + " Third Entry: " + str(e_three))
#                print(e_one, "---", x.gender_name.lower())
                gender = association_genders.objects.get(assn=asn, gender_name__iexact = "Unknown")
        else:
                if(DEBUG_WRITE):
                        f.write(" Complete get_assn_gender_from_text: "  
                                + "gender_name = " + str(gender.gender_name) 
                                + " at " + str(timezone.now()) + "\n")
        return(gender)
def get_assn_type_from_text(f, asn, entry_one, entry_two, entry_three, DEBUG_WRITE):
        e_type=None

        if(entry_one is not None):
                e_one = str(entry_one.lower())
        else:
                e_one = ""
        if(entry_two is not None):
                e_two = str(entry_two.lower())
        else:
                e_two = ""
        if(entry_three is not None):
                e_three = str(entry_three.lower())
        else:
                e_three = ""

        if(DEBUG_WRITE):
                f.write("get_assn_type_from_text:"  
                        + " First Entry (lower): " + str(e_one) 
                        + " Second Entry (lower): " + str(e_two) 
                        + " Third Entry (lower): " + str(e_three) 
                        + " " + str(timezone.now()) + "\n")

        assn_types = association_types.objects.filter(assn=asn)

        #check e_one first
        for x in assn_types:
                if(e_one.find(x.type_category.lower()) != -1):
                        e_type = x
        #check e_two next
        if e_type is None:
                for x in assn_types:
                        if(e_two.find(x.type_category.lower()) != -1):
                                e_type = x
        #check e_three last
        if e_type is None:
                for x in assn_types:
                        if(e_three.find(x.type_category.lower()) != -1):
                                e_type = x
        if(e_type is None):
                discipline, gender, e_type, ages = get_assn_values_from_three_digits(f, asn, e_one, e_two, e_three, DEBUG_WRITE)
        if(e_type is None):
                if(DEBUG_WRITE):
                        f.write("                     get_assn_type_from_text: Type set to Individual\n")  
#                record_error_data("x_helper_functions.py", "get_assn_type_from_text", "Warning",
#                                 "WARNING: Defaulted to Individual: "
#                                        + " First Entry: " + str(e_one) 
#                                        + " Second Entry: " + str(e_two) 
#                                        + " Third Entry: " + str(e_three))
                e_type = association_types.objects.get(assn=asn, type_category__iexact = "Individual")
        else:
                if(DEBUG_WRITE):
                        f.write(" Complete get_assn_type_from_text: "  
                                + "type = " + str(e_type.type_category) 
                                + " at " + str(timezone.now()) + "\n")
        return(e_type)
def get_assn_ages_from_text(f, asn, entry_one, entry_two, entry_three, DEBUG_WRITE):
        ages=None
        if(entry_one is not None):
                e_one = str(entry_one.lower())
        else:
                e_one = ""
        if(entry_two is not None):
                e_two = str(entry_two.lower())
        else:
                e_two = ""
        if(entry_three is not None):
                e_three = str(entry_three.lower())
        else:
                e_three = ""

        if(DEBUG_WRITE):
                f.write("get_assn_ages_from_text:"  
                        + " First Entry (lower): " + str(e_one) 
                        + " Second Entry (lower): " + str(e_two) 
                        + " Third Entry (lower): " + str(e_three) 
                        + " " + str(timezone.now()) + "\n")

        assn_ages = association_ages.objects.filter(assn=asn)
        #check e_one first
        for x in assn_ages:
                if(e_one.find(x.age_category.lower()) != -1):
                        ages = x
        #check e_two next
        if(ages is None):
                for x in assn_ages:
                        if(e_two.find(x.age_category.lower()) != -1):
                                ages = x
        #check e_three last
        if(ages is None):
                for x in assn_ages:
                        if(e_three.find(x.age_category.lower()) != -1):
                                ages = x

        if(ages is None):
                discipline, gender, e_type, ages = get_assn_values_from_three_digits(f, asn, e_one, e_two, e_three, DEBUG_WRITE)
        if(ages is None):
#                if(DEBUG_WRITE):
                record_error_data("x_helper_functions.py", "get_assn_ages_from_text", "Warning",
                                 "WARNING: Defaulted to all_ages: "
                                        + " First Entry: " + str(e_one) 
                                        + " Second Entry: " + str(e_two) 
                                        + " Third Entry: " + str(e_three))
                ages = association_ages.objects.get(assn=asn, age_category__iexact = "all_ages")
        else:
                if(DEBUG_WRITE):
                        f.write(" Complete get_assn_ages_from_text: "  
                                + "age_category = " + str(ages.age_category) 
                                + " at " + str(timezone.now()) + "\n")
        return(ages)


# Association Member Functions

def is_member_with_rec(member_num):
#        record_log_data("club_mgr-view.py", "is_member_with_rec", "member: " + str(member_num))
        try:
                member_rec = association_members.objects.get(assn_member_number=member_num)
        except:
                member_rec = False
#        record_log_data("club_mgr-view.py", "is_member_with_rec", "member: " + str(member_num) + "result: " + str(member_rec)) 
        return(member_rec)

def zzzfind_association_member_by_name_fuzzy(f, asn, assn_recs, full_name, DEBUG_WRITE):
    fcnt_start = timezone.now()
    match_point = 90 #95
    amr = None
    minimum_full_name_length_to_match = 4

    if DEBUG_WRITE:
        f.write("    find_association_member_by_name_fuzzy starting: " + str(full_name) + " " + str(timezone.now()) + "\n")

    scorers = [
        fuzz.token_set_ratio,
        fuzz.token_sort_ratio,
        fuzz.partial_token_sort_ratio,
        fuzz.token_ratio,
        fuzz.partial_ratio,
        fuzz.QRatio,
        fuzz.ratio
    ]

    fuzzy_proc_extract = []
    for scorer in scorers:
        fuzzy_proc_extract = process.extract(full_name, assn_recs, scorer=scorer, score_cutoff=match_point)
        #gotcha here - going after small full names like 'S R' - need to check for length of full_name and delete if not large enough
        for qq in fuzzy_proc_extract:
                if len(qq[0]) < minimum_full_name_length_to_match:
                        fuzzy_proc_extract.remove(qq)
        if fuzzy_proc_extract:
            break
        if DEBUG_WRITE:
            f.write("                              find_association_member_by_name_fuzzy scorers fuzzy_proc_extract: " + str(fuzzy_proc_extract) + " " + str(timezone.now()) + "\n")

    if not fuzzy_proc_extract:
        if DEBUG_WRITE:
            f.write("                              find_association_member_by_name_fuzzy DID NOT FIND ANY MATCH: " + full_name.lower() + " " + str(timezone.now()) + "\n")
    else:
        if DEBUG_WRITE:
            f.write("                              find_association_member_by_name_fuzzy GT MATCH POINT: " + full_name.lower() + " and found: " + str(fuzzy_proc_extract) + " " + str(timezone.now()) + "\n")
        fuzzy_holder = fuzzy_proc_extract[0][0].replace(",", "")
        if DEBUG_WRITE:
            f.write("                                    fuzzy_holder: " + str(fuzzy_holder) + " " + str(timezone.now()) + "\n")
        amr = association_members.objects.filter(assn=asn, assn_member_full_name__iexact=fuzzy_holder)

        if not amr.exists():
            if DEBUG_WRITE:
                f.write("                              find_association_member_by_name_fuzzy did not find match in bf_rec: " + str(timezone.now()) + "\n")
        else:
            if DEBUG_WRITE:
                f.write("                              find_association_member_by_name_fuzzy bf_rec: " + str(amr[0].assn_member_identifier) + " " + str(timezone.now()) + "\n")

    fcnt_end = timezone.now()
    time_inside = fcnt_end - fcnt_start
    if DEBUG_WRITE:
        f.write("                              find_association_member_by_name_fuzzy Total Time (secs): " + str(time_inside.seconds) 
                + " Start Time: " + str(fcnt_start) 
                + " End Time: " + str(fcnt_end) + "\n") 
    return amr



def find_association_member_by_name_fuzzy(f, asn, assn_recs, full_name, DEBUG_WRITE):
    fcnt_start = timezone.now()
    match_point = 90 #95
    amr = None
    minimum_full_name_length_to_match = 4

    normalized_full_name = full_name.replace('-', ' ')
    normalized_assn_recs = [rec.replace('-', ' ') for rec in assn_recs]

    if DEBUG_WRITE:
        f.write("         STARTING: find_association_member_by_name_fuzzy: " + str(full_name) + " " + str(timezone.now()) + "\n")

    scorers = [
        fuzz.token_set_ratio,
        fuzz.token_sort_ratio,
        fuzz.partial_token_sort_ratio,
        fuzz.token_ratio,
        fuzz.partial_ratio,
        fuzz.QRatio,
        fuzz.ratio
    ]

    fuzzy_proc_extract = []
    for scorer in scorers:
        fuzzy_proc_extract = process.extract(normalized_full_name, normalized_assn_recs, scorer=scorer, score_cutoff=match_point)
        #gotcha here - going after small full names like 'S R' - need to check for length of full_name and delete if not large enough
        for qq in fuzzy_proc_extract:
                if len(qq[0]) < minimum_full_name_length_to_match:
                        fuzzy_proc_extract.remove(qq)
        if fuzzy_proc_extract:
            break
        if DEBUG_WRITE:
            f.write("            name_fuzzy scorers fuzzy_proc_extract: " + str(fuzzy_proc_extract) + " " + str(timezone.now()) + "\n")

    if not fuzzy_proc_extract:
        if DEBUG_WRITE:
            f.write("            name_fuzzy DID NOT FIND ANY MATCH: " + full_name.lower() + " " + str(timezone.now()) + "\n")
    else:
        if DEBUG_WRITE:
            f.write("            name_fuzzy GT MATCH POINT: " + full_name.lower() + " and found: " + str(fuzzy_proc_extract) + " " + str(timezone.now()) + "\n")
        fuzzy_holder = fuzzy_proc_extract[0][0].replace(",", "")
        normalized_fuzzy_holder = fuzzy_holder.replace('-', ' ')
        if DEBUG_WRITE:
            f.write("            normalized_fuzzy_holder: " + str(normalized_fuzzy_holder) + " " + str(timezone.now()) + "\n")
        amr = association_members.objects.annotate(
                normalized_full_name=ReplaceF(F('assn_member_full_name'))
                ).filter(normalized_full_name__iexact=normalized_fuzzy_holder,assn=asn)

    fcnt_end = timezone.now()
    time_inside = fcnt_end - fcnt_start
    if DEBUG_WRITE:
        f.write("         find_association_member_by_name_fuzzy Total Time (secs): " + str(time_inside.seconds) 
                + " Start Time: " + str(fcnt_start) 
                + " End Time: " + str(fcnt_end) + "\n") 
        if amr is not None and amr.exists():
            if DEBUG_WRITE:
                f.write("         Completed: find_association_member_by_name_fuzzy bf_rec: " + str(amr[0].assn_member_identifier) + " " + str(timezone.now()) + "\n")
        else:
            if DEBUG_WRITE:
                f.write("         Completed: find_association_member_by_name_fuzzy did not find match in bf_rec: " + str(timezone.now()) + "\n")
    return amr

def assn_member_name_lookup(f, asn, full_name, DEBUG_WRITE):
    # Checks fullname and splits for name reversal
    if len(full_name) == 0:
        return association_members.objects.none()

    if DEBUG_WRITE:
        f.write("         STARTING:  assn_member_name_lookup--> full_name: " + str(full_name) + " " + str(timezone.now()) + "\n")

    # Prepare the reversed name
    first_space = full_name.find(' ')
    if first_space != -1:
        s_name = full_name[first_space+1:].strip() + " " + full_name[:first_space].strip()
    else:
        s_name = full_name

    # Combine the lookups into a single query
#    amr = association_members.objects.filter(
#        assn=asn,
#        assn_member_full_name__iexact=full_name
#    ) | association_members.objects.filter(
#        assn=asn,
#        assn_member_full_name__iexact=s_name
#    )

    # in time swap the querry above with the one below
    amr = association_members.objects.filter(
        Q(assn=asn) & (Q(assn_member_full_name__iexact=full_name) | Q(assn_member_full_name__iexact=s_name))
        ).distinct()

    if DEBUG_WRITE:
        if amr is not None and amr.exists():
            for x in amr:
                f.write("         COMPLETED: assn_member_name_lookup--> amr: " + str(x.assn_member_full_name) + " " + str(timezone.now()) + "\n")
        else:
            f.write("         COMPLETED: assn_member_name_lookup--> No matching records found " + str(timezone.now()) + "\n")
    return amr
def pick_assn_member_record_from_list(f, amr, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("   STARTING: pick_assn_member_record_from_list: " + str(timezone.now()) + "\n")

    best_rec = None
    if amr.exists():
        # Order the queryset and get the first record
        best_rec = amr.order_by('assn_member_suspended', '-assn_member_valid', '-assn_member_exp_date').first()

    if DEBUG_WRITE:
        if best_rec is not None:
            f.write("   COMPLETED: pick_assn_member_record_from_list RETURNING: " + best_rec.assn_member_full_name + " " + str(timezone.now()) + "\n")
        else:
            f.write("   COMPLETED: pick_assn_member_record_from_list NO RECORDS TO CHECK: " + str(timezone.now()) + "\n")

    return best_rec
def find_association_member_record_by_name(f, asn, assn_recs, full_name, first_name, last_name, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("   STARTING: find_association_member_record_by_name: " + asn.assn_name + " " + str(full_name) + " " + str(timezone.now()) + "\n")
    fcnt_start = timezone.now()
    amr = None

    if full_name and full_name.lower() != "bye":
        amr = assn_member_name_lookup(f, asn, full_name, DEBUG_WRITE)
    if not amr or not amr.exists():
        if first_name and last_name:
            amr = assn_member_name_lookup(f, asn, last_name + " " + first_name, DEBUG_WRITE)

    if not amr or not amr.exists():
        fname = full_name if full_name else last_name + " " + first_name
#        if DEBUG_WRITE:
#            f.write("      fuzzy logic test: " + str(fname) + " " + str(timezone.now()) + "\n")
        amr = find_association_member_by_name_fuzzy(f, asn, assn_recs, fname, DEBUG_WRITE)

    fcnt_end = timezone.now()
    time_inside = fcnt_end - fcnt_start
    if DEBUG_WRITE:
        f.write("   COMPLETED: find_association_member_record_by_name Total Time (secs): " + str(time_inside.seconds) 
                + " Start Time: " + str(fcnt_start) 
                + " End Time: " + str(fcnt_end) + "\n")
    return amr

def get_assn_member_record(f, asn, assn_recs, identifier, full_name, first_name, last_name, DEBUG_WRITE):
    # This routine checks for existence of any assn member record
    # If cannot find, will return None. Will never update a record
    st_timezone = timezone.now()
    assn_record = None

    if DEBUG_WRITE:
        f.write("get_assn_member_record:--->" + str(asn.assn_name) + " " + str(full_name) 
                + " " + str(first_name) + " " + str(last_name) + " " + str(st_timezone) + "\n") 

    if not asn or not (full_name or first_name or last_name):
        f.write("ERROR!  get_assn_member_record:  No names or assn_member_identifier given: " 
                + str(timezone.now()) + " " + str(asn) + " " + str(full_name) 
                + " " + str(first_name) + " " + str(last_name) + "\n")
        return None

    amr = None
    if identifier and identifier.isdigit():
        if DEBUG_WRITE:
            f.write("   looking for digit: " + str(identifier) + "\n")
        amr = association_members.objects.filter(assn=asn, assn_member_identifier__iexact=identifier).order_by('-assn_member_identifier')
    if not amr or not amr.exists():
        if DEBUG_WRITE:
            f.write("   looking for name: " + str(full_name) + " " + str(first_name) + " " + str(last_name) + "\n")
        amr = find_association_member_record_by_name(f, asn, assn_recs, full_name, first_name, last_name, DEBUG_WRITE)

    if DEBUG_WRITE and amr is not None:
        for x in amr:
            f.write("   found amr = " 
                    + str(x.assn_member_identifier) + " " 
                    + str(x.assn_member_first_name) + " "
                    + str(x.assn_member_last_name) + " "
                    + str(x.assn_member_full_name) + " "
                    + str(x.assn_member_number) + " \n")

    if amr:
        assn_record = pick_assn_member_record_from_list(f, amr, DEBUG_WRITE)

    diff_seconds = (timezone.now() - st_timezone).total_seconds()
    if DEBUG_WRITE:
        if not assn_record:
            f.write("COMPLETED: get_assn_member_record RETURNING NONE. Total Time: " + str(diff_seconds) + "\n")
        else:
            f.write("COMPLETED: get_assn_member_record RETURNING: " 
                    + str(assn_record.assn_member_identifier) + " " 
                    + str(assn_record.assn_member_first_name) + " "
                    + str(assn_record.assn_member_last_name) + " "
                    + str(assn_record.assn_member_full_name) + " "
                    + str(assn_record.assn_member_dob) + " "
                    + str(assn_record.assn_member_gender) + " "
                    + " Total Time: " + str(diff_seconds) + "\n")
    return assn_record
def get_assn_member_record_by_assn_member_number(f, asn, asn_member_number, DEBUG_WRITE):
        #This routine checks for existance of any assn member record
        #If cannot find, will return None   ####Will never Update a Record
        amr = None

        if(DEBUG_WRITE):
                f.write("get_assn_member_record_by_assn_member_number:--->" + str(asn.assn_name) + " " + str(asn_member_number) + " " + str(timezone.now()) + "\n") 
        try:
                amr = association_members.objects.get(assn=asn, assn_member_number=asn_member_number)
        except association_members.DoesNotExist:
                amr = None
        if(DEBUG_WRITE):
                f.write(" COMPLETE: get_assn_member_record_by_assn_member_number: " + str(amr) + "\n")
        return(amr)
def get_assn_member_record_by_assn_assn_member_identifier(f, asn, asn_member_identifier, DEBUG_WRITE):
        amr = None

        if(DEBUG_WRITE):
                f.write("get_assn_member_record_by_assn_assn_member_identifier:--->" + str(asn.assn_name) + " " + str(asn_member_identifier) + " " + str(timezone.now()) + "\n") 
        try:
                amr = association_members.objects.get(assn=asn, assn_member_identifier=asn_member_identifier)
        except association_members.DoesNotExist:
                amr = None
        if(DEBUG_WRITE):
                f.write(" COMPLETE: get_assn_member_record_by_assn_assn_member_identifier: " + str(amr) + "\n")
        return(amr)
def event_build_member_array(f, asn, ev, assn_recs, DEBUG_WRITE):
        event_member_array = []
        for y in event_final_results.objects.filter(efr_event = ev):
                amr = get_assn_member_record(f, asn, assn_recs, y.efr_given_member_identifier, y.efr_given_name, "", "", DEBUG_WRITE)
                holder = []
                try:
                        identifier = int(y.efr_given_member_identifier)
                except (AttributeError, ValueError, TypeError):
                        holder.append(None)
                else:
                        holder.append(identifier)
                holder.append(y.efr_given_name)
                holder.append(amr)
                event_member_array.append(holder)
#                f.write("   event_build_member_array: " + str(y.efr_given_member_identifier) + " " + str(y.efr_given_name) + " " + str(holder) + " " + str(amr) + " " + str(timezone.now()) + "\n")
        return(event_member_array)
def event_build_member_array_assn_member_lookup(f, asn, assn_recs, identifier, full_name, first_name, last_name, DEBUG_WRITE, event_member_array):
        amr = None
        found = False
        try:
                id_val = int(identifier)
        except (AttributeError, ValueError, TypeError):
                id_val = 0

        for x in event_member_array:
                if(found == False and id_val > 0 and x[0] is not None and x[0] == id_val):
#                        f.write(str(x[0]) + "++" + str(x[1]) + "++" + str(x[2]) + "\n")
                        amr = x[2]
                        found = True
                if(found == False and full_name is not None and len(full_name) > 0 and x[1].lower() == full_name.lower()):
#                        f.write(str(x[0]) + "%%" + str(x[1]) + "%%" + str(x[2]) + "\n")
                        amr = x[2]
                        found = True
        if not found:
                f.write("not found...  looking up via get_assn_member_record")
                amr = get_assn_member_record(f, asn, assn_recs, identifier, full_name, first_name, last_name, DEBUG_WRITE)
#        f.write("eb amr: " + str(amr) + "\n")
        return(amr)
def tourney_apply_latest_assn_member_numbers(f, asn, tourney, assn_recs, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("   tourney_apply_latest_assn_member_numbers: " + tourney.tourney_name + " " + str(tourney.tourney_start_date) + " " + str(timezone.now()) + "\n")
        for x in events.objects.filter(ev_tourney = tourney):
                eve_cnt = event_final_results.objects.filter(efr_event = x).count()
                if(DEBUG_WRITE):
                        f.write("      Processing...  Event name: " + str(x.ev_name) 
                                + " ev_status: " + str(x.ev_status.status) 
                                + " ev_assn_type: " + str(x.ev_assn_type.type_category) 
                                + " ev_assn_discipline: " + str(x.ev_assn_discipline.discipline_name)
                                + " event_final_results records: " + str(eve_cnt) + " " + str(timezone.now()) + "\n")
                ebma = event_build_member_array(f, asn, x, assn_recs, DEBUG_WRITE)

                #first event_final_results
                for y in event_final_results.objects.filter(efr_event = x):
                        amr = event_build_member_array_assn_member_lookup(f, asn, assn_recs, y.efr_given_member_identifier, y.efr_given_name, "", "", DEBUG_WRITE, ebma)
                        if(amr is not None):
                                amn = amr.assn_member_number
                        else:
                                amn = None
                        y.efr_assn_member_number = amn
                        y.save()
                for a in event_rounds.objects.filter(er_event = x):
                        for b in event_round_seeding.objects.filter(ers_round = a):
                                amr = event_build_member_array_assn_member_lookup(f, asn, assn_recs, b.ers_member_num, b.ers_name, "", "", DEBUG_WRITE, ebma)
                                if(amr is not None):
                                        amn = amr.assn_member_number
                                else:
                                        amn = None
                                b.ers_assn_member_number = amn
                                b.save()
#                        print("event_round_pool_elimination_scores")
                        for c in event_round_pool_elimination_scores.objects.filter(erpes_round = a):
                                amr = event_build_member_array_assn_member_lookup(f, asn, assn_recs, c.erpes_left_member_num, c.erpes_left_name, "", "", DEBUG_WRITE, ebma)
                                if(amr is not None):
                                        amn = amr.assn_member_number
                                else:
                                        amn = None
                                c.erpes_left_assn_member_number = amn
                                amr = event_build_member_array_assn_member_lookup(f, asn, assn_recs, c.erpes_right_member_num, c.erpes_right_name, "", "", DEBUG_WRITE, ebma)
                                if(amr is not None):
                                        amn = amr.assn_member_number
                                else:
                                        amn = None
                                c.erpes_right_assn_member_number = amn
                                amr = event_build_member_array_assn_member_lookup(f, asn, assn_recs, c.erpes_winner_member_num, c.erpes_winner_name, "", "", DEBUG_WRITE, ebma)
                                if(amr is not None):
                                        amn = amr.assn_member_number
                                else:
                                        amn = None
                                c.erpes_winner_assn_member_number = amn
#                                print("saving", c.erpes_winner_assn_member_number, c.erpes_winner_name, c.erpes_right_assn_member_number, c.erpes_right_name)
                                c.save()
                        for d in event_round_pool_results.objects.filter(erpr_round = a):
                                amr = event_build_member_array_assn_member_lookup(f, asn, assn_recs, d.erpr_member_num, d.erpr_name, "", "", DEBUG_WRITE, ebma)
                                if(amr is not None):
                                        amn = amr.assn_member_number
                                else:
                                        amn = None
                                d.erpr_assn_member_number = amn
                                d.save()
                        for e in event_round_pool_elimination_matches.objects.filter(erpem_round = a):
                                amr = event_build_member_array_assn_member_lookup(f, asn, assn_recs, e.erpem_top_member_num, e.erpem_top_name, "", "", DEBUG_WRITE, ebma)
                                if(amr is not None):
                                        amn = amr.assn_member_number
                                else:
                                        amn = None
                                e.erpem_top_member_num = amn
                                amr = event_build_member_array_assn_member_lookup(f, asn, assn_recs, e.erpem_bottom_member_num, e.erpem_bottom_name, "", "", DEBUG_WRITE, ebma)
                                if(amr is not None):
                                        amn = amr.assn_member_number
                                else:
                                        amn = None
                                e.erpem_bottom_member_num = amn
                                amr = event_build_member_array_assn_member_lookup(f, asn, assn_recs, e.erpem_winner_member_num, e.erpem_winner_name, "", "", DEBUG_WRITE, ebma)
                                if(amr is not None):
                                        amn = amr.assn_member_number
                                else:
                                        amn = None
                                e.erpem_winner_member_num = amn
                                e.save()
                        for g in event_round_pool_details.objects.filter(erpd_round = a):
                                for qq in event_round_pool_assignments.objects.filter(erpa_pool_details = g):
                                        amr = event_build_member_array_assn_member_lookup(f, asn, assn_recs, qq.erpa_member_num, qq.erpa_name, "", "", DEBUG_WRITE, ebma)
                                        if(amr is not None):
                                                amn = amr.assn_member_number
                                        else:
                                                amn = None
                                        qq.erpa_assn_member_number = amn
                                        qq.save()
                                for k in event_round_pool_scores.objects.filter(erps_pool_details = g):
                                        amr = event_build_member_array_assn_member_lookup(f, asn, assn_recs, k.erps_left_member_num, k.erps_left_name, "", "", DEBUG_WRITE, ebma)
                                        if(amr is not None):
                                                amn = amr.assn_member_number
                                        else:
                                                amn = None
                                        k.erps_left_assn_member_number = amn
                                        amr = event_build_member_array_assn_member_lookup(f, asn, assn_recs, k.erps_right_member_num, k.erps_right_name, "", "", DEBUG_WRITE, ebma)
                                        if(amr is not None):
                                                amn = amr.assn_member_number
                                        else:
                                                amn = None
                                        k.erps_right_assn_member_number = amn
                                        amr = event_build_member_array_assn_member_lookup(f, asn, assn_recs, k.erps_winner_member_num, k.erps_winner_name, "", "", DEBUG_WRITE, ebma)
                                        if(amr is not None):
                                                amn = amr.assn_member_number
                                        else:
                                                amn = None
                                        k.erps_winner_assn_member_number = amn
                                        k.save()        
def get_association_member_extra_field_by_assn_member(f, asn_member, field_name, DEBUG_WRITE):
        try:
                asn_extra_field_rec = association_member_extra_fields.objects.get(
                                assn_member=asn_member, assn_member_field_name__iexact=field_name.lower())
        except association_member_extra_fields.DoesNotExist:
                asn_extra_field_rec = None
                if DEBUG_WRITE:
                        f.write("Association Member Extra Field does not exist: " + str(asn_member) + " " + str(field_name) + "\n")
        return (asn_extra_field_rec)
#for all tournaments
def apply_assn_member_numbers(f, DEBUG_WRITE):
        for y in associations.objects.filter(assn_name = "British Fencing"):
                if(DEBUG_WRITE):
                        f.write("apply_assn_member_numbers: " + y.assn_name + " " + str(timezone.now()) + "\n")
                assn_recs = association_members.objects.filter(assn = y).values_list('assn_member_full_name', flat=True)

                for x in tournaments.objects.filter(tourney_assn = y, tourney_name__iexact="Norfolk Open 2024"):
                        tourney_apply_latest_assn_member_numbers(f, y, x, assn_recs, DEBUG_WRITE)
                if(DEBUG_WRITE):
                        f.write(" COMPLETE! apply_assn_member_numbers: " + y.assn_name + " " + str(timezone.now()) + "\n")


###BRACKETS

def change_into_bye(seed, participants_count):
        return seed if seed <= participants_count else None
def get_bracket(participants, DEBUG_WRITE):
        participants_count = len(participants)
        rounds = math.ceil(math.log(participants_count) / math.log(2))
        bracket_size = 2 ** rounds
        required_byes = bracket_size - participants_count
#        if(DEBUG_WRITE):
#                print(f'Number of participants: {participants_count}')
#                print(f'Number of rounds: {rounds}')
#                print(f'Bracket size: {bracket_size}')
#                print(f'Required number of byes: {required_byes}')
        if participants_count < 2:
                return []

        matches = [[1, 2]]
        for round in range(1, rounds):
                round_matches = []
                sum = 2 ** (round + 1) + 1
                for match in matches:
                        home = change_into_bye(match[0], participants_count)
                        away = change_into_bye(sum - match[0], participants_count)
                        round_matches.append([home, away])
                        home = change_into_bye(sum - match[1], participants_count)
                        away = change_into_bye(match[1], participants_count)
                        round_matches.append([home, away])
                matches = round_matches
        match_num = 1
        final_matches = []
        for x in matches:
                f_match = []
                f_match.append(match_num)
                f_match.append(x)
                final_matches.append(f_match)
                match_num = match_num + 1
        return(final_matches)
def generate_bracket(number_of_participants, DEBUG_WRITE):
        participants = list(range(1, number_of_participants + 1))
        bracket = get_bracket(participants, DEBUG_WRITE)
#        if(DEBUG_WRITE):
#                print(bracket)
        return(bracket)
def populate_initial_elim_scores(event_round):
        for z in event_round_pool_elimination_scores.objects.filter(erpes_round = event_round):
#            print(z.erpes_score, z.erpes_winner_name, z.erpes_left_name, z.erpes_right_name)
                one_score = 0
                two_score = 0
                if(z.erpes_score is not None):
                        if('-' in z.erpes_score):
#                                print(z.erpes_score)
                                o_score = z.erpes_score.split('-')[0].strip()
                                t_score = z.erpes_score.split('-')[1].strip()
                                if(o_score is not None and o_score.isnumeric()):
                                        one_score = int(o_score)
                                if(t_score is not None and t_score.isnumeric()):
                                        two_score = int(t_score)
                l_winner = False
                r_winner = False
                l_score = 99
                r_score = 99
                if(z.erpes_winner_name is not None):
                        l_winner = False                #assume right wins
                        r_winner = True
                        l_score = min(one_score, two_score)
                        r_score = max(one_score, two_score)
                        if(z.erpes_left_name is not None):
                                if(z.erpes_winner_name.lower() == z.erpes_left_name.lower()):
                                        l_winner = True
                                        r_winner = False
                                        l_score = max(one_score, two_score)
                                        r_score = min(one_score, two_score)

#            print(l_score, l_winner, r_score, r_winner)
                ev_round, created = event_round_pool_elimination_scores.objects.update_or_create(
                        id=z.id,
                        defaults={
                        'erpes_left_score':l_score,
                        'erpes_right_score':r_score,
                        'erpes_left_winner':l_winner,
                        'erpes_right_winner':r_winner
                        })
def populate_initial_elim_matches(event_round):
        event_round_pool_elimination_matches.objects.filter(erpem_round = event_round).delete()
        e_scores = event_round_pool_elimination_scores.objects.filter(erpes_round=event_round)
        if(e_scores):
        #        print("event_round", event_round)
        #        print("e_scores", e_scores)
                max_table = max(int(x.erpes_table) for x in e_scores)
        #        print("max_table", max_table)
                gen_bracket = generate_bracket(max_table, False)
        #        print(gen_bracket)

                for x in e_scores:
                        if int(x.erpes_table) == max_table:
        #                    print(x)
                                for y in gen_bracket:
        #                        print(y, y[0], y[1][0], y[1][1])
        #                        print(table, y, x.erpes_left_name, x.erpes_right_name, x.erpes_left_score, x.erpes_right_score, x.erpes_left_seed, x.erpes_right_seed)

                                        if(x.erpes_left_seed is not None):
                                                ls = int(x.erpes_left_seed)
                                        else:
                                                ls = 0
                                        if(x.erpes_right_seed is not None):
                                                rs = int(x.erpes_right_seed)
                                        else:
                                                rs = 0

                                        if(y[1][0] == ls) or (y[1][1] == ls) or (y[1][0] == rs) or (y[1][1] == rs):
                #                            print("Found", y, x.erpes_left_name, x.erpes_right_name)
                #                            print("match_num", y[0])
                                                match_number = y[0]
                                                match_top = y[1][0]
                                                match_bottom = y[1][1]

                                                ev_round, created = event_round_pool_elimination_matches.objects.update_or_create(
                                                        erpem_round = event_round,
                                                        erpem_table = x.erpes_table,
                                                        erpem_number = x.erpes_number,
                                                        erpem_strip = x.erpes_strip,
                                                        erpem_match_number = match_number, 
                                                        erpem_match_top = match_top, 
                                                        erpem_match_bottom = match_bottom,
                                                        defaults={
                                                        'erpem_date_updated':timezone.now(),
                                                        'erpem_date_added':timezone.now(),
                                                        'erpem_stime':x.erpes_stime,
                                                        'erpem_score':x.erpes_score,
                                                        'erpem_top_seed':x.erpes_left_seed,
                                                        'erpem_top_member_num':x.erpes_left_member_num,
                                                        'erpem_top_name':x.erpes_left_name,
                                                        'erpem_top_score':x.erpes_left_score,
                                                        'erpem_top_winner':False,
                                                        'erpem_bottom_seed':x.erpes_right_seed,
                                                        'erpem_bottom_member_num':x.erpes_right_member_num,
                                                        'erpem_bottom_name':x.erpes_right_name,
                                                        'erpem_bottom_score':x.erpes_right_score,
                                                        'erpem_bottom_winner':False,
                                                        'erpem_winner_member_num':None,
                                                        'erpem_winner_name':x.erpes_winner_name,
                                                        })
#        for z in event_round_pool_elimination_matches.objects.filter(erpem_round = event_round):
#                print(z.erpem_table, z.erpem_number, z.erpem_strip, z.erpem_match_number, z.erpem_match_top, z.erpem_match_bottom, z.erpem_top_name, z.erpem_bottom_name, z.erpem_top_seed, z.erpem_bottom_seed)
def populate_remaining_match_numbers(event_round):
        def get_elim_match_record_winner_name(erpem_round, match_number):
                try:
                        l_found = event_round_pool_elimination_matches.objects.get(
                        erpem_round=erpem_round, 
                        erpem_match_number=match_number
                        )
                        return l_found.erpem_winner_name
                except event_round_pool_elimination_matches.DoesNotExist:
                        return None

        def get_elim_score_record(erpes_round, table, winner):

                try:
                        l_found = event_round_pool_elimination_scores.objects.get(
                                erpes_round=erpes_round, 
                                erpes_table=str(table), 
                                erpes_left_name__iexact=winner)
                except event_round_pool_elimination_scores.DoesNotExist:
                        l_found = None

                try:
                        r_found = event_round_pool_elimination_scores.objects.get(
                                erpes_round=erpes_round, 
                                erpes_table=str(table), 
                                erpes_right_name__iexact=winner)
                except event_round_pool_elimination_scores.DoesNotExist:
                        r_found = None

                return l_found, r_found
            
        e_scores = event_round_pool_elimination_scores.objects.filter(erpes_round=event_round)
        if(e_scores):
                max_table = max(int(x.erpes_table) for x in e_scores)

                c_bracket = int(max_table / 2)
                match_count = c_bracket + 1

                while c_bracket > 1:
                        walk = int(c_bracket / 2) + 1
                        for ww in range(1, walk):
                                w_top = int(match_count - ((c_bracket*2) - (c_bracket) - ww + 1))
                                w_bottom = w_top + 1
                                w_top_name = get_elim_match_record_winner_name(event_round, w_top)
                                w_bottom_name = get_elim_match_record_winner_name(event_round, w_bottom)
        #                        print("mat", match_count, "wtop", w_top, "wtname", w_top_name, "wbottom", w_bottom, "wbname", w_bottom_name)
                                found_top_left, found_top_right = get_elim_score_record(event_round, c_bracket, w_top_name)
                                found_bottom_left, found_bottom_right = get_elim_score_record(event_round, c_bracket, w_bottom_name)
        #                        print("tl", found_top_left, "tr", found_top_right, "bl", found_bottom_left, "br", found_bottom_right)

                                if(found_top_left is not None):
                                        x = found_top_left
                                else:
                                        x = found_top_right
                                if(x is not None):
                                        t_win = False           #assume no one wins
                                        b_win = False
                                        if(x.erpes_winner_name is not None):
                                                t_win = False   #assume bottom wins
                                                b_win = True
                                                if(x.erpes_left_name is not None):
                                                        if (x.erpes_left_name.lower() == x.erpes_winner_name.lower()):
                                                                t_win = True
                                                                b_win = False

                                        if(found_top_left is not None):
                                                e_top_seed = x.erpes_left_seed
                                                e_top_member_num = x.erpes_left_member_num
                                                e_top_name = x.erpes_left_name
                                                e_top_score = x.erpes_left_score
                                                e_top_winner = t_win
                                                e_bottom_seed = x.erpes_right_seed
                                                e_bottom_member_num = x.erpes_right_member_num
                                                e_bottom_name = x.erpes_right_name
                                                e_bottom_score = x.erpes_right_score
                                                e_bottom_winner = b_win
                                                e_winner_member_num = x.erpes_winner_member_num
                                                e_winner_name = x.erpes_winner_name
                                        else:
                                                e_top_seed = x.erpes_right_seed
                                                e_top_member_num = x.erpes_right_member_num
                                                e_top_name = x.erpes_right_name
                                                e_top_score = x.erpes_right_score
                                                e_top_winner = t_win
                                                e_bottom_seed = x.erpes_left_seed
                                                e_bottom_member_num = x.erpes_left_member_num
                                                e_bottom_name = x.erpes_left_name
                                                e_bottom_score = x.erpes_left_score
                                                e_bottom_winner = b_win
                                                e_winner_member_num = x.erpes_winner_member_num
                                                e_winner_name = x.erpes_winner_name

                                        ev_round, created = event_round_pool_elimination_matches.objects.update_or_create(
                                                                erpem_round = event_round,
                                                                erpem_table = x.erpes_table,
                                                                erpem_number = x.erpes_number,
                                                                erpem_strip = x.erpes_strip,
                                                                erpem_match_number = match_count, 
                                                                erpem_match_top = w_top, 
                                                                erpem_match_bottom = w_bottom,
                                                                defaults={
                                                                'erpem_date_updated':timezone.now(),
                                                                'erpem_date_added':timezone.now(),
                                                                'erpem_stime':x.erpes_stime,
                                                                'erpem_score':x.erpes_score,
                                                                'erpem_top_seed':e_top_seed,
                                                                'erpem_top_member_num':e_top_member_num,
                                                                'erpem_top_name':e_top_name,
                                                                'erpem_top_score':e_top_score,
                                                                'erpem_top_winner':e_top_winner,
                                                                'erpem_bottom_seed':e_bottom_seed,
                                                                'erpem_bottom_member_num':e_bottom_member_num,
                                                                'erpem_bottom_name':e_bottom_name,
                                                                'erpem_bottom_score':e_bottom_score,
                                                                'erpem_bottom_winner':e_bottom_winner,
                                                                'erpem_winner_member_num':e_winner_member_num,
                                                                'erpem_winner_name':e_winner_name
                                                                })
                                match_count += 1
                        c_bracket = int(c_bracket / 2)
def populate_elimination_match_brackets(f, tourney_event, DEBUG_WRITE):
        if(DEBUG_WRITE):
                f.write("         populate_elimination_match_brackets: " 
                        + " tourney_event: " + str(tourney_event.ev_name) 
                        + " " + str(timezone.now()) + "\n")

        max_er_r_number_record = event_rounds.objects.filter(er_event=tourney_event, 
                        er_r_type__iexact = "elimination").order_by('-er_r_number').first()
#        print(tourney_event.ev_tourney.tourney_name, tourney_event.ev_name, "max_er_r_number_record", max_er_r_number_record)
        if max_er_r_number_record:
                if(DEBUG_WRITE):
                        f.write("         Max er_r_number Record: " + str(max_er_r_number_record.er_r_number) + " - " + str(timezone.now()) + "\n")
                populate_initial_elim_matches(max_er_r_number_record)
                populate_remaining_match_numbers(max_er_r_number_record)
        if(DEBUG_WRITE):
                f.write("    Completed populate_elimination_match_brackets: " + str(timezone.now()) + "\n")

#validation only
def check_assn_member_number_assignment(f, DEBUG_WRITE):
        for y in associations.objects.filter(assn_name = "British Fencing"):
                if(DEBUG_WRITE):
                        f.write("apply_assn_member_numbers: " + y.assn_name + " " + str(timezone.now()) + "\n")
                for x in tournaments.objects.filter(tourney_assn = y, tourney_name__iexact="Norfolk Open 2024"):
                                for z in events.objects.filter(ev_tourney = x):
                                        for a in event_final_results.objects.filter(efr_event = z):
                                                detail = ("Final Position: " + str(a.efr_final_position)
                                                        + " Given Name: " + str(a.efr_given_name)
                                                        + " efr_given_member_identifier: " + str(a.efr_given_member_identifier)
                                                        + " Member Number: " + str(a.efr_assn_member_number))
                                                amr = association_members.objects.filter(assn=y, assn_member_number = a.efr_assn_member_number)
                                                if(amr.count() == 0):
                                                        detail = "NOT FOUND-->" + detail
                                                else:
                                                        extra_detail = ("ASSN_MEMBER NUMBER: " + str(amr[0].assn_member_number) 
                                                                + " ASSN_MEMBER FULL NAME: " + str(amr[0].assn_member_full_name)
                                                                + " ASSN_MEMBER IDENTIFIER: " + str(amr[0].assn_member_identifier))
                                                        if(a.efr_given_member_identifier is not None and (a.efr_given_member_identifier) > 0):
                                                                if (amr[0].assn_member_identifier == int(a.efr_given_member_identifier)):
                                                                        detail = "MATCH-->" + detail + " -- " + extra_detail
                                                                else:
                                                                        detail = "MISMATCH-->" + detail + " -- " + extra_detail 
                                                        else:
                                                                if (amr[0].assn_member_full_name.lower() == a.efr_given_name.lower()):
                                                                        detail = "MATCH NAME-->" + detail + " -- " + extra_detail
                                                                else:
                                                                        detail = "MISMATCH NAME -->" + detail + " -- " + extra_detail 
                                                f.write("     " + detail + "\n")
def zUpcoming_Events_Update_Assn_Member_Number(f, DEBUG_WRITE):
        f.write("\nUpcoming_Events_Update_Assn_Member_Number: " + str(timezone.now()) + "\n")
        start_date = timezone.now() - relativedelta(days=2)
        prev_assn = None
        for x in tournaments.objects.filter(tourney_start_date__gte = start_date):
                if(prev_assn != x.tourney_assn):
                        assn_member_recs = association_members.objects.filter(assn = x.tourney_assn)
                prev_assn = x.tourney_assn
                f.write("   Processing...  Tournament name: " + str(x.tourney_name) 
                        + " association: " + str(x.tourney_assn.assn_name) 
                        + " tournament status: " + str(x.tourney_status.status) 
                        + " start date: " + str(x.tourney_start_date) 
                        + " at " + str(timezone.now()) + "\n")
                for y in events.objects.filter(ev_tourney = x):
                        if(DEBUG_WRITE):
                                f.write("      Processing...  Event name: " + str(y.ev_name) 
                                        + " ev_status: " + str(y.ev_status.status) 
                                        + " ev_assn_type: " + str(y.ev_assn_type.type_category) 
                                        + " ev_assn_discipline: " + str(y.ev_assn_discipline.discipline_name) 
                                        + " ev_assn_gender: " + str(y.ev_assn_gender.gender_name) 
                                        + " ev_assn_ages: " + str(y.ev_assn_ages.age_category) 
                                        + " at " + str(timezone.now()) + "\n")
                        for z in event_final_results.objects.filter(efr_event = y):
                                if(DEBUG_WRITE):
                                        f.write("         Processing...  Event Final Result: "  
                                                + " efr_final_position: " + str(z.efr_final_position) 
                                                + " efr_given_name: " + str(z.efr_given_name) 
                                                + " efr_given_club: " + str(z.efr_given_club) 
                                                + " efr_assn_member_number: " + str(0) 
                                                + " at " + str(timezone.now()) + "\n")
                                a_member = get_assn_member_record(f, assn_member_recs, 0, z.efr_given_name, "", "", DEBUG_WRITE)
#                                fencer = get_fencer(f, DEBUG_WRITE, z.efr_fencer)
#                                if fencer is not None:

        f.write(" Completed Upcoming_Events_Update_Assn_Member_Number: " + str(timezone.now()) + "\n")


def dump_records_to_file(f, dump_directory, app_name, table_name, file_format, records, DEBUG_WRITE):
        f.write("dump_records_to_file: " 
                + " Directory: " + dump_directory
                + " App_Name: " + app_name
                + " Table_name: " + table_name
                + " File Format: " + file_format
                + " " + str(timezone.now()) + "\n")

        try:
                model = apps.get_model(app_name, table_name)
        except LookupError:
                f.write("Table " + str(table_name) + " does not exist in " + str(app_name) + ".\n")
                return
        output_file = dump_directory + table_name + "_dump." + file_format

        if file_format == 'csv':
                with open(output_file, 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        fields = [field.name for field in model._meta.fields if field.name != 'id']
                        writer.writerow(fields)
                        for record in records:
                                writer.writerow(record)
        else:
                f.write("Unsupported file format: " + file_format + "\n")
                return

        f.write(" Completed dump_records_to_file: " + str(timezone.now()) + "\n")
def dump_table_to_file(f, dump_directory, app_name, table_name, file_format, DEBUG_WRITE):
        f.write("dump_table_to_file: " 
                + " Directory: " + dump_directory
                + " App_Name: " + app_name
                + " Table_name: " + table_name
                + " File Format: " + file_format
                + " " + str(timezone.now()) + "\n")

        try:
                model = apps.get_model(app_name, table_name)
        except LookupError:
                f.write("Table " + str(table_name) + " does not exist in " + str(app_name) + ".\n")
                return
        records = model.objects.all()
        output_file = dump_directory + table_name + "_dump." + file_format

        if file_format == 'csv':
                with open(output_file, 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        fields = [field.name for field in model._meta.fields if field.name != 'id']
                        writer.writerow(fields)
                        for record in records:
                                writer.writerow([getattr(record, field.name) for field in model._meta.fields if field.name != 'id'])
        else:
                f.write("Unsupported file format: " + file_format + "\n")
                return
        f.write(" Completed dump_table_to_file: " + str(timezone.now()) + "\n")

def get_table_record_counts():
    """
    Query record count from all database tables and return the table name and record count in a list.
    """
    table_record_counts = []

    with connection.cursor() as cursor:
        # Get the list of all tables
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            # Query the record count for each table
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            record_count = cursor.fetchone()[0]
            table_record_counts.append((table_name, record_count))

    table_record_counts.sort(key=lambda x: x[1], reverse=True)

    return table_record_counts
