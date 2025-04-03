#!/usr/bin/env python3

import cv2
import os
import matplotlib.pyplot as plt
import pandas as pd

from base.models import *
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.utils.translation import get_language
from dotenv import load_dotenv
from datetime import datetime

from base.models import *
from users.models import *

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from dateutil.relativedelta import relativedelta


from scripts import aaa_reset_and_load
from scripts.aaa_helper_functions import *
from scripts.aaa_stand_analysis import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")


def build_stand_counts_by_date(rxe, ev_date):
    event_stand_count_by_date.objects.filter(escby_rx_event=rxe, escby_date=ev_date).delete()
    for s in stand_location.objects.filter(sl_stand__s_rx_event=rxe):
#        print(ev_date, s.sl_stand.s_stand_status, s.sl_x_length, s.sl_y_length)
        # Use get_or_create to fetch or create the object
        obj, created = event_stand_count_by_date.objects.get_or_create(
            escby_rx_event=rxe,
            escby_date=ev_date,
            escby_x_length=abs(s.sl_x_length),
            escby_y_length=abs(s.sl_y_length),
            escby_stand_status=s.sl_stand.s_stand_status,
            defaults={'escby_stand_count': 1}  # Set initial count to 1 if created
        )
        # Increment the count if the object already exists
        if not created:
            obj.escby_stand_count += 1
            obj.save()
def build_stand_counts_as_string(rxe, ev_date):
    output_string = ""
    build_stand_counts_by_date(rxe, ev_date)
    for es in event_stand_count_by_date.objects.filter(escby_rx_event=rxe, escby_date=ev_date
                ).order_by('escby_stand_status', 'escby_x_length', 'escby_y_length'):
        output_string = output_string + (str(es.escby_stand_status) + " " + str(es.escby_x_length) + "x" \
                        + str(es.escby_y_length) + ": " + str(es.escby_stand_count) + "; ")
    return output_string


def run_event_year(event_name, create_images):
        record_log_data("aaa_run_process.py", "run_event_year", "starting...")

        try:
                rxe = rx_event.objects.get(re_name=event_name)
        except rx_event.DoesNotExist:
                record_log_data("aaa_run_process.py", "run_event_year", "Event does not exist: " + event_name)
                return

        st_date = rxe.re_event_start_date - relativedelta(days=365+90)
        ev_date = st_date
        end_date = rxe.re_event_end_date#timezone.make_aware(datetime(2024, 3, 30, 0, 0, 0, 0))
        image_length, image_height, image_margin, header_space, footer_space, image_multiplier, image_multiplier_small, static_floorplan_loc, static_analysis_loc = get_env_values()
        erase_files_in_dir(static_floorplan_loc)

        header_set = []
        header_set.append([rxe.re_name, 'center', 'top'])
        header_set.append(["Las Vegas, NV", 'center', 'top'])
        header_set.append([str(rxe.re_event_start_date.strftime("%d %b %Y")) + " to " + str(rxe.re_event_end_date.strftime("%d %b %Y")), 'center', 'top'])

        to_do = 0
        while ev_date <= end_date and to_do < 3:
#        if (1 == 0):
                if(ev_date == st_date):
                        footer_set = []
                        message_set = []
                        footer_set.append(["INITAL VIEW", 'center', 'top'])
                        footer_set.append([build_stand_counts_as_string(rxe, ev_date), 'left', 'top'])
                        render_floorplan(rxe, header_set, footer_set, message_set, image_multiplier, "Initial")
                else:
                        for x in event_sales_transactions.objects.filter(est_event = rxe,est_Order_Created_Date__gte=ev_date, est_Order_Created_Date__lte=ev_date+relativedelta(days=1)):
                                print(f"event_sales_transactions: {x.est_Order_Created_Date} {x.est_Stand_Name_Cleaned} {x.est_Company_Name}")
                                record_log_data("aaa_run_process.py", "run_event_year", "working date: " + str(ev_date))
                                for fs in stands.objects.filter(s_rx_event=rxe, s_number=x.est_Stand_Name_Cleaned):
#                                        s_stand_status = Available, Sold, New Sell, Reserved, New Stand
#                                        s_stand_price = Base, Price Increase, Price Decrease 
                                        fs.s_stand_status = 'New Sell'
                                        fs.save()

                                        if(create_images == True):
                                                footer_set = []
                                                message_set = []
                                                footer_set.append(["EVENT: Stand Sale: " + str(x.est_Company_Name) + " at: "+str(x.est_Stand_Name_Cleaned) + " on: "+str(ev_date), 'center', 'top'])
                                                footer_set.append(["Las Vegas, NV", 'left', 'top'])
                                                footer_set.append([build_stand_counts_as_string(rxe, ev_date), 'left', 'top'])
                                                if(create_images):
                                                        render_floorplan(rxe, header_set, footer_set, message_set, image_multiplier_small, "NA")
                                        fs.s_stand_status = 'Sold'
                                        fs.save()
#                                        build_stand_counts_by_date(rxe, ev_date)
                                to_do = to_do + 1
                ev_date = ev_date + relativedelta(days=1)
        footer_set = []
        message_set = []
        footer_set.append(["FINAL VIEW", 'center', 'top'])
        footer_set.append(["blah, blah, blah", 'left', 'top'])
        footer_set.append([build_stand_counts_as_string(rxe, ev_date), 'left', 'top'])
        render_floorplan(rxe, header_set, footer_set, message_set, image_multiplier, "Final")

        record_log_data("aaa_run_process.py", "run_event_year", "completed...")


def run(*args):

        db_host_name = str(settings.DATABASES['default']['HOST'])
        db_name = str(settings.DATABASES['default']['NAME'])
        path_logs = os.path.join(settings.BASE_DIR, "logs/")
        path_input = os.path.join(settings.BASE_DIR, "scripts/")

        logs_filename = path_logs+"_"+os.path.splitext(os.path.basename(__file__))[0] + ".txt"

        for x in stands.objects.all():
                stand_analysis.objects.filter(sa_stand=x).delete()
                x.s_stand_status = 'Available' 
                x.s_stand_price = 'Base'
                x.s_stand_price_gradient = random.randint(0, 100)
                x.save()

        record_log_data("aaa_run_process.py", "run", "starting... reset data")
#        aaa_reset_and_load.run()
        record_log_data("aaa_run_process.py", "run", "completed... load data")

        stand_analysis_price('ISC West 2025')
        build_stand_gradient('ISC West 2025')
        record_log_data("aaa_run_process.py", "run", "starting... run_event_year")
        run_event_year('ISC West 2025', True)
        record_log_data("aaa_run_process.py", "run", "complete... run_event_year")

#        create_mov_from_images('floorplans', 'output.mp4')

#        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
#        f.close()

#python manage.py runscript aaa_run_process
