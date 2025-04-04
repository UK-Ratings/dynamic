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
from scripts.helper_functions import *
from scripts.helper_functions_render import *
from scripts.stand_analysis import *
from scripts.event_analysis import *

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

def build_sale_analysis(sales_t, st_info, run_id):
        analysis_set = []

        analysis_set.append(["Stand: "+str(sales_t.est_Stand_Name_Cleaned) + "-" , 'center', 'top'])
        analysis_set.append(["Company Name: " + str(sales_t.est_Company_Name), 'left', 'top'])
        analysis_set.append(["Origin Country: " + str(sales_t.est_Recipient_Country), 'left', 'top'])
        analysis_set.append(["Customer Type: " + str(sales_t.est_Customer_Type), 'left', 'top'])
        analysis_set.append(["Opportunity Type: " + str(sales_t.est_Opportunity_Type), 'left', 'top'])
        analysis_set.append(["Opportunity Owner: " + str(sales_t.est_Opportunity_Owner), 'left', 'top'])
        analysis_set.append([str(sales_t.est_Stand_Name_Length_Width), 'left', 'top'])
        analysis_set.append(["Stand Name: " + str(sales_t.est_Stand_Name_Cleaned), 'left', 'top'])
        analysis_set.append(["Stand Dimenstions: " + str(sales_t.est_Stand_Name_Dim_Cleaned), 'left', 'top'])
        analysis_set.append(["Stand Area: " + str(sales_t.est_Stand_Area), 'left', 'top'])
        analysis_set.append(["Stand Corners: " + str(sales_t.est_Number_of_Corners), 'left', 'top'])
        analysis_set.append(["Stand Zone: " + str(sales_t.est_Stand_Zone), 'left', 'top'])
        analysis_set.append(["Stand Sector: " + str(sales_t.est_Floor_Plan_Sector), 'left', 'top'])
        analysis_set.append(["Stand Sharer Entitlements: " + str(sales_t.est_Sharer_Entitlements), 'left', 'top'])
        analysis_set.append(["Stand Sharer Companies: " + str(sales_t.est_Sharer_Companies), 'left', 'top'])
        analysis_set.append(["Modified Date: " + str(sales_t.est_Last_Modified_Date), 'left', 'top'])
        analysis_set.append(["Total Net Amount: " + str(sales_t.est_Total_Net_Amount), 'left', 'top'])
        analysis_set.append(["Order Created Date: " + str(sales_t.est_Order_Created_Date), 'left', 'top'])
        analysis_set.append(["Packages Sold: " + str(sales_t.est_Packages_Sold), 'left', 'top'])

        analysis_set.append(["Products Sold", 'left', 'top'])
        p_name = sales_t.est_Product_Name.split(",")
        for q in p_name:
                analysis_set.append(["   " + str(q), 'left', 'top'])

        mc = False
        stand_analysis_recs = stand_get_all_analysis_records(st_info, run_id)
        if(len(stand_analysis_recs) == 0):
                stand_analysis_price_apply_monte_carlo(sales_t, st_info, run_id)
                stand_analysis_recs = stand_get_all_analysis_records(st_info, run_id)
                mc = True

        if(len(stand_analysis_recs) > 0):
                analysis_set.append([" ", 'left', 'top'])
                if(mc):
                        analysis_set.append(["Monte Carlo Stand Analysis", 'left', 'top'])
                else:
                        analysis_set.append(["Stand Analysis", 'left', 'top'])
                analysis_set.append([" ", 'left', 'top'])
                for q in stand_analysis_recs:
                        if(q[1] == 'MC Rules Applied'):
                                cut_it = q[2].split(",")
                                analysis_set.append([" ", 'left', 'top'])
                                analysis_set.append(["Monte Carlo Rules Applied", 'left', 'top'])
                                for q2 in cut_it:
                                        analysis_set.append([str(q2), 'left', 'top'])
                        else:
                                analysis_set.append([str(q[1]+": "+str(q[2])), 'left', 'top'])
        return(analysis_set)

def run_event_year(rxe, create_images):
        record_log_data("aaa_run_process.py", "run_event_year", "starting...")

        run_id = 0
        stand_analysis_price(rxe, run_id)
        build_stand_gradient(rxe, run_id)

        st_date = rxe.re_event_start_date - relativedelta(days=365+90)
        ev_date = st_date
        end_date = rxe.re_event_end_date#timezone.make_aware(datetime(2024, 3, 30, 0, 0, 0, 0))
        image_length, image_height, image_margin, header_space, footer_space, image_multiplier, image_multiplier_small, static_floorplan_loc, static_analysis_loc = get_env_values()

        header_set = []
        header_set.append([rxe.re_name, 'center', 'top'])
        header_set.append(["Las Vegas, NV", 'center', 'top'])
        header_set.append([str(rxe.re_event_start_date.strftime("%d %b %Y")) + " to " + str(rxe.re_event_end_date.strftime("%d %b %Y")), 'center', 'top'])

        to_do = 0
        while ev_date <= end_date and to_do < 399999999:
#        if (1 == 0):
                if(ev_date == st_date):
                        analysis_set_top = []
                        analysis_set_bottom = []
                        footer_set = []
                        message_set = []
                        footer_set.append(["AS SOLD: INITAL VIEW", 'center', 'top'])
#                        footer_set.append([build_stand_counts_as_string(rxe, ev_date), 'left', 'top'])
                        render_floorplan(rxe, header_set, footer_set, message_set, analysis_set_top, analysis_set_bottom, image_multiplier, "Initial", run_id)
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
                                                analysis_set_top = build_sale_analysis(x, fs, run_id)
                                                analysis_set_bottom = []  ###WILL USE MC RUN ID HERE
                                                footer_set.append(["EVENT: Stand Sale: " + str(x.est_Company_Name) + " at: "+str(x.est_Stand_Name_Cleaned) + " on "+str(ev_date.strftime("%d %b %Y")), 'center', 'top'])
                                                footer_set.append(['Darker Green higher Price from Average.  Darker Red lower Price from Average','left', 'top'])
                                                if(create_images):
                                                        render_floorplan(rxe, header_set, footer_set, message_set, analysis_set_top, analysis_set_bottom, image_multiplier_small, "NA", run_id)
                                        fs.s_stand_status = 'Sold'
                                        fs.save()
#                                        build_stand_counts_by_date(rxe, ev_date)
                                to_do = to_do + 1
                ev_date = ev_date + relativedelta(days=1)
        footer_set = []
        message_set = []
        analysis_set_top = []
        analysis_set_bottom = []
        footer_set.append(["AS SOLD: FINAL VIEW", 'center', 'top'])
        footer_set.append(['Darker Green higher Price from Average.  Darker Red lower Price from Average','left', 'top'])
        render_floorplan(rxe, header_set, footer_set, message_set, analysis_set_top, analysis_set_bottom, image_multiplier, "Final", run_id)

        record_log_data("aaa_run_process.py", "run_event_year", "completed...")


def run_event_monte_carlo_simulation(rxe, p_number, create_images):
        record_log_data("aaa_run_process.py", "run_event_monte_carlo_simulation", "starting...")

        st_date = rxe.re_event_start_date - relativedelta(days=365+90)
        ev_date = st_date
        end_date = rxe.re_event_end_date#timezone.make_aware(datetime(2024, 3, 30, 0, 0, 0, 0))
        image_length, image_height, image_margin, header_space, footer_space, image_multiplier, image_multiplier_small, static_floorplan_loc, static_analysis_loc = get_env_values()

        header_set = []
        header_set.append([rxe.re_name, 'center', 'top'])
        header_set.append(["Monte Carlo Simulation Cycle " + str(p_number) + " Start", 'center', 'top'])
        header_set.append([str(rxe.re_event_start_date.strftime("%d %b %Y")) + " to " + str(rxe.re_event_end_date.strftime("%d %b %Y")), 'center', 'top'])

        to_do = 0
        while ev_date <= end_date and to_do < 3999999:
#        if (1 == 0):
                if(ev_date == st_date):
                        analysis_set_top = []
                        analysis_set_bottom = []
                        footer_set = []
                        message_set = []
                        footer_set.append(["AS SOLD: INITAL VIEW", 'center', 'top'])
#                        footer_set.append([build_stand_counts_as_string(rxe, ev_date), 'left', 'top'])
                        render_floorplan(rxe, header_set, footer_set, message_set, analysis_set_top, analysis_set_bottom, image_multiplier, "Initial", p_number)
                else:
                        for x in event_sales_transactions.objects.filter(est_event = rxe,est_Order_Created_Date__gte=ev_date, est_Order_Created_Date__lte=ev_date+relativedelta(days=1)):
                                print(f"event_sales_transactions: {x.est_Order_Created_Date} {x.est_Stand_Name_Cleaned} {x.est_Company_Name}")
                                record_log_data("aaa_run_process.py", "run_event_year", "working date: " + str(ev_date))
                                for fs in stands.objects.filter(s_rx_event=rxe, s_number=x.est_Stand_Name_Cleaned):
#                                        s_stand_status = Available, Sold, New Sell, Reserved, New Stand
#                                        s_stand_price = Base, Price Increase, Price Decrease 
                                        fs.s_stand_status = 'New Sell'
                                        fs.save()

                                        analysis_set_top = build_sale_analysis(x, fs, p_number)

                                        if(create_images == True):
                                                footer_set = []
                                                message_set = []
                                                analysis_set_bottom = []  ###WILL USE MC RUN ID HERE
                                                footer_set.append(["EVENT: Stand Sale: " + str(x.est_Company_Name) + " at: "+str(x.est_Stand_Name_Cleaned) + " on "+str(ev_date.strftime("%d %b %Y")), 'center', 'top'])
                                                footer_set.append(['Darker Green higher Price from Average.  Darker Red lower Price from Average','left', 'top'])
                                                if(create_images):
                                                        render_floorplan(rxe, header_set, footer_set, message_set, analysis_set_top, analysis_set_bottom, image_multiplier_small, "NA", p_number)
                                        fs.s_stand_status = 'Sold'
                                        fs.save()
#                                        build_stand_counts_by_date(rxe, ev_date)
                                to_do = to_do + 1
                ev_date = ev_date + relativedelta(days=1)
        footer_set = []
        message_set = []
        analysis_set_top = []
        analysis_set_bottom = []
        footer_set.append(["Monte Carlo Simulation Cycle " + str(p_number) + " Final", 'left', 'top'])
        render_floorplan(rxe, header_set, footer_set, message_set, analysis_set_top, analysis_set_bottom, image_multiplier, "Final", p_number)

        record_log_data("aaa_run_process.py", "run_event_monte_carlo_simulation", "completed...")

def run(*args):

        db_host_name = str(settings.DATABASES['default']['HOST'])
        db_name = str(settings.DATABASES['default']['NAME'])
        path_logs = os.path.join(settings.BASE_DIR, "logs/")
        path_input = os.path.join(settings.BASE_DIR, "scripts/")

        logs_filename = path_logs+"_"+os.path.splitext(os.path.basename(__file__))[0] + ".txt"

        image_length, image_height, image_margin, header_space, footer_space, image_multiplier, image_multiplier_small, static_floorplan_loc, static_analysis_loc = get_env_values()
        erase_files_in_dir(static_floorplan_loc)

        for x in stands.objects.all():
                stand_analysis.objects.filter(sa_stand=x).delete()
                x.s_stand_status = 'Available' 
                x.s_stand_price = 'Base'
                x.s_stand_price_gradient = random.randint(0, 100)
                x.save()

        record_log_data("aaa_run_process.py", "run", "starting... reset data")
#        aaa_reset_and_load.run()
        record_log_data("aaa_run_process.py", "run", "completed... load data")

        event_name = "ISC West 2025"
        rx_event = get_event(event_name)

        record_log_data("aaa_run_process.py", "run", "starting... run_event_year")
        run_event_year(rx_event, False)
        record_log_data("aaa_run_process.py", "run", "complete... run_event_year")


        if(rx_event is not None):
                pricing_rules.objects.filter(prb_event = rx_event).delete()
                load_pr(rx_event)

#                recs = pricing_rules_get_all_data(rx_event, 0)
#                for q in recs:
#                        print(q)

                for r in range(1, 2):
                        print("Pricing Rule Base: " + str(r))
                        pricing_copy_base(rx_event, r)
#                        recs = pricing_rules_get_all_data(rx_event, r)
#                        for q in recs:
#                                print(q)
                        run_event_monte_carlo_simulation(rx_event, r, False)

#        stand_analysis_price(event_name)
#        build_stand_gradient('ISC West 2025')
#        record_log_data("aaa_run_process.py", "run", "starting... run_event_year")
#        run_event_year(rx_event, False)
#        record_log_data("aaa_run_process.py", "run", "complete... run_event_year")

#        create_mov_from_images('floorplans', 'output.mp4')

#        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
#        f.close()

#python manage.py runscript aaa_run_process
