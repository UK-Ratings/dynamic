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

from base.models import *
from users.models import *

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from dateutil.relativedelta import relativedelta


from scripts import aaa_reset_and_load
from scripts.aaa_helper_functions import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")

def run_event():
        record_log_data("aaa_helper_functions.py", "run_event_year", "starting...")

        image_length, image_height, image_margin, header_space, footer_space, image_multiplier, static_floorplan_loc, static_analysis_loc = get_env_values()
        erase_files_in_dir(static_floorplan_loc)

        rxe = rx_event.objects.get(re_name='ISC West 2025')

        for x in event_sales_transactions.objects.filter(est_event=rxe).order_by('est_Order_Created_Date'):
                found_stand = False
                for fs in stands.objects.filter(s_rx_event=rxe, s_number=x.est_Stand_Name_Cleaned):
#                        print(x.est_Order_Created_Date,fs.s_number, fs.s_name, fs.s_rx_event.re_name)

                        fs.s_stand_fill_color = get_color('sold stand outline color')
                        fs.s_stand_outline_color = get_color('sold stand outline color')
                        fs.s_text_color = get_color('sold stand text color')
                        fs.save()
                        found_stand = True
                if found_stand == True:        
                        header_set = []
                        footer_set = []
                        message_set = []
                        header_set.append("ISC West 2025")
                        header_set.append("Las Vegas, NV")
                        header_set.append(str(rxe.re_event_start_date) + " to " + str(rxe.re_event_end_date))

                        footer_set.append("EVENT: Stand Sale: " + str(x.est_Company_Name) + " at: "+str(x.est_Stand_Name_Cleaned))
                        footer_set.append("Las Vegas, NV")
                        footer_set.append("Blah, Blah, Blah")
                        render_floorplan(rxe, header_set, footer_set, message_set)

        record_log_data("aaa_helper_functions.py", "run_event_year", "completed...")






def run_event_year(event_name):
        record_log_data("aaa_helper_functions.py", "run_event_year", "starting...")

        try:
                rxe = rx_event.objects.get(re_name=event_name)
        except rx_event.DoesNotExist:
                record_log_data("aaa_helper_functions.py", "run_event_year", "Event does not exist: " + event_name)
                return

        st_date = rxe.re_event_start_date - relativedelta(days=365+90)
        ev_date = st_date
        end_date = rxe.re_event_end_date + relativedelta(days=7)

        image_length, image_height, image_margin, header_space, footer_space, image_multiplier, static_floorplan_loc, static_analysis_loc = get_env_values()
        erase_files_in_dir(static_floorplan_loc)

        while ev_date <= end_date:
                if(ev_date == st_date):
                        header_set = []
                        footer_set = []
                        message_set = []
                        header_set.append("ISC West 2025")
                        header_set.append("Las Vegas, NV")
                        header_set.append(str(rxe.re_event_start_date) + " to " + str(rxe.re_event_end_date))
                        footer_set.append("INITAL VIEW")
                        render_floorplan(rxe, header_set, footer_set, message_set)
                else:
                        for x in event_sales_transactions.objects.filter(est_event = rxe,est_Order_Created_Date__gte=ev_date, est_Order_Created_Date__lte=ev_date+relativedelta(days=1)):
                                for fs in stands.objects.filter(s_rx_event=rxe, s_number=x.est_Stand_Name_Cleaned):
                #                        print(x.est_Order_Created_Date,fs.s_number, fs.s_name, fs.s_rx_event.re_name)
                                        fs.s_stand_fill_color = get_color('sold stand outline color')
                                        fs.s_stand_outline_color = get_color('sold stand outline color')
                                        fs.s_text_color = get_color('sold stand text color')
                                        fs.save()

                                        header_set = []
                                        footer_set = []
                                        message_set = []
                                        header_set.append("ISC West 2025")
                                        header_set.append("Las Vegas, NV")
                                        header_set.append(str(rxe.re_event_start_date) + " to " + str(rxe.re_event_end_date))
                                        footer_set.append("EVENT: Stand Sale: " + str(x.est_Company_Name) + " at: "+str(x.est_Stand_Name_Cleaned) + " on: "+str(ev_date))
                                        footer_set.append("Las Vegas, NV")
                                        footer_set.append("Blah, Blah, Blah")
                                        render_floorplan(rxe, header_set, footer_set, message_set)
                ev_date = ev_date + relativedelta(days=1)
        record_log_data("aaa_helper_functions.py", "run_event_year", "completed...")


def run(*args):

        db_host_name = str(settings.DATABASES['default']['HOST'])
        db_name = str(settings.DATABASES['default']['NAME'])
        path_logs = os.path.join(settings.BASE_DIR, "logs/")
        path_input = os.path.join(settings.BASE_DIR, "scripts/")

        logs_filename = path_logs+"_"+os.path.splitext(os.path.basename(__file__))[0] + ".txt"

        record_log_data("aaa_run_process.py", "run", "starting... reset data")
        aaa_reset_and_load.run()
        record_log_data("aaa_run_process.py", "run", "completed... load data")

        record_log_data("aaa_run_process.py", "run", "starting... run_event_year")
        run_event_year('ISC West 2025')
        record_log_data("aaa_run_process.py", "run", "complete... run_event_year")

#    create_mov_from_images('images', 'output.mp4')

#        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
#        f.close()

#python manage.py runscript aaa_run_process
