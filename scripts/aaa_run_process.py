#!/usr/bin/env python3

import cv2
import os
import matplotlib.pyplot as plt
import pandas as pd
import csv
import os


from base.models import *
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.utils.translation import get_language
from dotenv import load_dotenv
from datetime import datetime
from django.db.models import Count

from base.models import *
from users.models import *

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from dateutil.relativedelta import relativedelta


from scripts import aaa_reset_and_load
from scripts.helper_functions import *
from scripts.helper_functions_render import *
from scripts.helper_functions_stand import *
from scripts.helper_functions_event import *
from scripts.aaa_reset_and_load import load_stand_attribute_data
from scripts.helper_functions_graphs import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")



def run_event_start(rxe):
        record_log_data("aaa_run_process.py", "run_event_start", "starting...")

        run_id = 0
        analysis_set_top = []
        analysis_set_bottom = []
        st_date = rxe.re_event_start_date
        end_date = rxe.re_event_end_date
        image_length, image_height, image_margin, header_space, footer_space, image_multiplier, image_multiplier_small = get_env_values()

        header_set = []
        header_set.append([rxe.re_name, 'center', 'top'])
        header_set.append(["Las Vegas, NV", 'center', 'top'])
        header_set.append([str(rxe.re_event_start_date.strftime("%d %b %Y")) + " to " + str(rxe.re_event_end_date.strftime("%d %b %Y")), 'center', 'top'])

        if(1==1):#first - straight floor plan
                for fs in stands.objects.filter(s_rx_event=rxe):
                        stand_attributes_record(fs, None, 'Stand Status', 'Available', 'string', timezone.now())
                        stand_record_analysis_record(fs, run_id, None, 'Sq Gradient', "100", "integer")
                footer_set = []
                message_set = []
                footer_set.append(["Initial Stands", 'center', 'top'])
                render_floorplan(rxe, header_set, footer_set, message_set, analysis_set_top, analysis_set_bottom, image_multiplier, "Initial", -1)
        if(1==1):#second - now with sold stands
                st_count = 0
                for fs in stands.objects.filter(s_rx_event=rxe):
                        stand_attributes_record(fs, None, 'Stand Status', 'Available', 'string', timezone.now())
                        stand_record_analysis_record(fs, run_id, None, 'Sq Gradient', "100", "integer")
                for fs in stands.objects.filter(s_rx_event=rxe):
                        for x in event_sales_transactions.objects.filter(est_event = rxe,est_Stand_Name_Cleaned__iexact = fs.s_number.lower().strip()):
                                stand_attributes_record(fs, None, 'Stand Status', 'Sold', 'string', timezone.now())
                                st_count = st_count + 1
                footer_set = []
                message_set = []
                footer_set.append(["Sold Stands: "+str(st_count), 'center', 'top'])
                render_floorplan(rxe, header_set, footer_set, message_set, analysis_set_top, analysis_set_bottom, image_multiplier, "Initial", -1)
        if(1==1):#third - stands missing in sales data
                st_count = 0
                for fs in stands.objects.filter(s_rx_event=rxe):
                        stand_attributes_record(fs, None, 'Stand Status', 'Available', 'string', timezone.now())
#                        stand_attributes_record(fs, None, 'Stand Price Gradient', "1", 'integer', timezone.now())
                        stand_record_analysis_record(fs, run_id, None, 'Sq Gradient', "1", "integer")
                for fs in stands.objects.filter(s_rx_event=rxe):
                        est = event_sales_transactions.objects.filter(est_event = rxe,est_Stand_Name_Cleaned__iexact = fs.s_number.lower().strip())
                        if(len(est) == 0):
                                stand_attributes_record(fs, None, 'Stand Status', 'Sold', 'string', timezone.now())
                                st_count = st_count + 1
                footer_set = []
                message_set = []
                footer_set.append(["Stands with no sales data: "+str(st_count), 'center', 'top'])
                render_floorplan(rxe, header_set, footer_set, message_set, analysis_set_top, analysis_set_bottom, image_multiplier, "Initial", -1)
        if(1==1):#fourth - stands missing net sales data
                st_count = 0
                for fs in stands.objects.filter(s_rx_event=rxe):
                        stand_attributes_record(fs, None, 'Stand Status', 'Available', 'string', timezone.now())
#                        stand_attributes_record(fs, None, 'Stand Price Gradient', "1", 'integer', timezone.now())
                        stand_record_analysis_record(fs, run_id, None, 'Sq Gradient', "1", "integer")
                for fs in stands.objects.filter(s_rx_event=rxe):
                        for ee in event_sales_transactions.objects.filter(est_event = rxe,est_Stand_Name_Cleaned__iexact = fs.s_number.lower().strip()):
                                if((ee.est_Total_Net_Amount is None) or (float(ee.est_Total_Net_Amount) == 0)):
                                        stand_attributes_record(fs, None, 'Stand Status', 'Sold', 'string', timezone.now())
                                        st_count = st_count + 1
                footer_set = []
                message_set = []
                footer_set.append(["Stands with net revenue data: "+str(st_count), 'center', 'top'])
                render_floorplan(rxe, header_set, footer_set, message_set, analysis_set_top, analysis_set_bottom, image_multiplier, "Initial", -1)
        if(1==1):#last - no for each stand attribute
                for fs in stands.objects.filter(s_rx_event=rxe):
#                        stand_attributes_record(fs, None, 'Stand Price Gradient', "1", 'integer', timezone.now())
                        stand_record_analysis_record(fs, run_id, None, 'Sq Gradient', "1", "integer")
                sad = stands_attribute_data.objects.filter(sad_event=rxe).values('sad_title', 'sad_value').annotate(count=Count('sad_value'))
                for x in sad:
                        st_count = 0
                        for fs in stands.objects.filter(s_rx_event=rxe):
                                stand_attributes_record(fs, None, 'Stand Status', 'Available', 'string', timezone.now())
#                        print(f"stands_attribute_data: {x['sad_title']} {x['sad_value']} {x['count']}")
                        for fss in stands.objects.filter(s_rx_event=rxe):
                                attr = stand_attributes_get_value(fss, None, x['sad_title'])
                                if(attr is not None):
                                        if(type(attr) == int):
                                                sv = int(x['sad_value'])
                                        elif(type(attr) == float):
                                                sv = float(x['sad_value'])
                                        elif (type(attr) == str):
                                                sv = str(x['sad_value'])
                                        if(attr == sv):
                                                stand_attributes_record(fss, None, 'Stand Status', 'Sold', 'string', timezone.now())
                                                st_count = st_count + 1
                        footer_set = []
                        message_set = []
                        footer_set.append([str(x['sad_title'])+": " + str(x['sad_value']) + "--> Stands: "+str(st_count), 'center', 'top'])
                        render_floorplan(rxe, header_set, footer_set, message_set, analysis_set_top, analysis_set_bottom, image_multiplier, "Initial", -1)
        record_log_data("aaa_run_process.py", "run_event_start", "completed...")

def run_event_year(rxe, create_images):
        record_log_data("aaa_run_process.py", "run_event_year", "starting...")
        for fs in stands.objects.filter(s_rx_event=rxe):
                stand_attributes_record(fs, None, 'Stand Status', 'Available', 'string', timezone.now())

        run_id = 0
        event_sales_by_run.objects.filter(esbr_run_id = run_id).delete()
        st_date = rxe.re_event_start_date - relativedelta(days=365+90)
        ev_date = st_date
        end_date = rxe.re_event_end_date
        image_length, image_height, image_margin, header_space, footer_space, image_multiplier, image_multiplier_small = get_env_values()

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
#                                print(f"event_sales_transactions: {x.est_Order_Created_Date} {x.est_Stand_Name_Cleaned} {x.est_Company_Name}")
                                record_log_data("aaa_run_process.py", "run_event_year", "working date: " + str(ev_date))
                                if(x.est_Stand_Name_Cleaned is not None):
                                        snc = x.est_Stand_Name_Cleaned.lower().strip()
                                else:
                                        snc = None
                                if(x.est_Company_Name is not None):
                                        cn = x.est_Company_Name.lower().strip()
                                else:
                                        cn = None
                                fss = stands.objects.filter(s_rx_event=rxe, s_number__iexact = snc)
                                if(len(fss) == 0):
                                        fss = stands.objects.filter(s_rx_event=rxe, s_name__iexact = cn)
                                for fs in fss:
                                        stand_attributes_record(fs, None, 'Stand Status', 'New Sell', 'string', timezone.now())

                                        if(create_images == True):
                                                footer_set = []
                                                message_set = []
                                                analysis_set_top = stand_build_sale_analysis(x, fs, run_id)
                                                analysis_set_bottom = []  ###WILL USE MC RUN ID HERE
                                                footer_set.append(["EVENT: Stand Sale: " + str(x.est_Company_Name) + " at: "+str(x.est_Stand_Name_Cleaned) + " on "+str(ev_date.strftime("%d %b %Y")), 'center', 'top'])
                                                footer_set.append(['Darker Green higher Price from Average.  Darker Red lower Price from Average','left', 'top'])
                                                if(create_images):
                                                        render_floorplan(rxe, header_set, footer_set, message_set, analysis_set_top, analysis_set_bottom, image_multiplier_small, "NA", run_id)
                                        stand_attributes_record(fs, None, 'Stand Status', 'Sold', 'string', timezone.now())
                                        sa_analysis_number, sa_analysis_title, rev_amount = stand_get_analysis_record(fs, run_id, None, 'Net Price')
                                        if(rev_amount is None):
                                                rev_amount = 0
                                        event_record_event_sales_by_run(fs, run_id, ev_date, rev_amount)
#                                        event_record_event_sales_by_run(fs, 1, ev_date, rev_amount*1.1)
#                                        event_record_event_sales_by_run(fs, 2, ev_date, rev_amount*-1.1)
#                                        build_stand_counts_by_date(rxe, ev_date)
                                to_do = to_do + 1
                ev_date = ev_date + relativedelta(days=1)
        footer_set = []
        message_set = []
        analysis_set_top = []
        analysis_set_bottom = []
        footer_set.append(["AS SOLD: FINAL VIEW", 'center', 'top'])
        footer_set.append(['Darker Green higher Price from Average.  Darker Red lower Price from Average.  Gray means we do not have a price.','left', 'top'])
        render_floorplan(rxe, header_set, footer_set, message_set, analysis_set_top, analysis_set_bottom, image_multiplier, "Final", run_id)
        record_log_data("aaa_run_process.py", "run_event_year", "completed...")

def run_event_monte_carlo_simulation(rxe, p_number, create_images):
        record_log_data("aaa_run_process.py", "run_event_monte_carlo_simulation", "starting...")

        max_id = event_sales_by_run.objects.aggregate(Max('esbr_run_id'))
        for xx in range(1, max_id['esbr_run_id']+1):
                event_sales_by_run.objects.filter(esbr_run_id = xx).delete()

        st_date = rxe.re_event_start_date - relativedelta(days=365+90)
        ev_date = st_date
        end_date = rxe.re_event_end_date
        image_length, image_height, image_margin, header_space, footer_space, image_multiplier, image_multiplier_small = get_env_values()

        header_set = []
        header_set.append([rxe.re_name, 'center', 'top'])
        header_set.append(["Monte Carlo Simulation Cycle " + str(p_number) + " Start", 'center', 'top'])
        header_set.append([str(rxe.re_event_start_date.strftime("%d %b %Y")) + " to " + str(rxe.re_event_end_date.strftime("%d %b %Y")), 'center', 'top'])

        to_do = 0
        while ev_date <= end_date and to_do < 3:
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
                                        stand_attributes_record(fs, None, 'Stand Status', 'New Sell', 'string', timezone.now())

                                        analysis_set_top = stand_build_sale_analysis(x, fs, p_number)
                                        if(create_images == True):
                                                footer_set = []
                                                message_set = []
                                                analysis_set_bottom = []  ###WILL USE MC RUN ID HERE
                                                footer_set.append(["EVENT: Stand Sale: " + str(x.est_Company_Name) + " at: "+str(x.est_Stand_Name_Cleaned) + " on "+str(ev_date.strftime("%d %b %Y")), 'center', 'top'])
                                                footer_set.append(['Darker Green higher Price from Average.  Darker Red lower Price from Average','left', 'top'])
                                                if(create_images):
                                                        render_floorplan(rxe, header_set, footer_set, message_set, analysis_set_top, analysis_set_bottom, image_multiplier_small, "NA", p_number)
                                        stand_attributes_record(fs, None, 'Stand Status', 'Sold', 'string', timezone.now())
#                                        fs.s_stand_status = 'Sold'
#                                        fs.save()
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

def run_revenue_graph(rxe):
        record_log_data("aaa_run_process.py", "run_revenue_graph", "starting...")
        image_length, image_height, image_margin, header_space, footer_space, image_multiplier, image_multiplier_small = get_env_values()

        header_set = []
        header_set.append([rxe.re_name, 'center', 'top'])
        header_set.append(["Las Vegas, NV", 'center', 'top'])
        header_set.append([str(rxe.re_event_start_date.strftime("%d %b %Y")) + " to " + str(rxe.re_event_end_date.strftime("%d %b %Y")), 'center', 'top'])
        footer_set = []
        footer_set.append(["Revenue by date", 'center', 'top'])

        render_revenue_graph(rxe, header_set, footer_set, image_multiplier)
        record_log_data("aaa_run_process.py", "run_revenue_graph", "completed...")



def write_x_to_csv(x, filename):
    logs_dir = os.path.join(settings.BASE_DIR, 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    file_path = os.path.join(logs_dir, filename)

    with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
                x.est_Company_Name,x.est_Recipient_Country,x.est_Customer_Type,x.est_Opportunity_Type,
                x.est_Opportunity_Owner,x.est_Stand_Name_Length_Width,x.est_Stand_Name_Cleaned,x.est_Stand_Name_Dim_Cleaned,
                x.est_Stand_Area,x.est_Number_of_Corners,x.est_Stand_Zone,x.est_Floor_Plan_Sector,
                x.est_Sharer_Entitlements,x.est_Sharer_Companies,x.est_Last_Modified_Date,x.est_Total_Net_Amount,
                x.est_Order_Created_Date,x.est_Packages_Sold,x.est_Product_Name
            ])

def cut_down_to_emerging_tech(rxe):
        record_log_data("aaa_run_process.py", "cut_down_to_emerging_tech", "starting...")
#        print(f"cut_down_to_emerging_tech stands: {len(stands.objects.filter(s_rx_event=rxe))}")
#        print(f"cut_down_to_emerging_tech stand_attributes: {len(stand_attributes.objects.filter(sa_event=rxe))}")
#        print(f"starting stands: {len(stands.objects.filter(s_rx_event=rxe))}")
#        print(f"starting event_sales_transactions: {len(event_sales_transactions.objects.filter(est_event = rxe))}")
        est = event_sales_transactions.objects.filter(est_event = rxe, est_Floor_Plan_Sector__iexact = 'Emerging Tech')
#        print(f"event_sales_transactions: {len(est)}")
        found_stands = 0
        for x in stands.objects.filter(s_rx_event=rxe):
                found = False
                for y in est:
                        if(x.s_number.lower().strip() == y.est_Stand_Name_Cleaned.lower().strip()):
                                found = True
                                found_stands = found_stands + 1
                if(found == False):
                        stand_analysis.objects.filter(sa_stand=x).delete()
                        stand_attributes.objects.filter(sa_stand=x).delete()
                        x.delete()
        found_sales_transactions = 0
        for x in event_sales_transactions.objects.filter(est_event = rxe):
                found = False
                for y in est:
                        if(x.est_Stand_Name_Cleaned is not None):
                                if(x.est_Stand_Name_Cleaned.lower().strip() == y.est_Stand_Name_Cleaned.lower().strip()):
                                        found = True
                                        found_sales_transactions = found_sales_transactions + 1
                if(found == False):
                        x.delete()
        record_log_data("aaa_run_process.py", "cut_down_to_emerging_tech", "completed...")

def run(*args):

        db_host_name = str(settings.DATABASES['default']['HOST'])
        db_name = str(settings.DATABASES['default']['NAME'])
        path_logs = os.path.join(settings.BASE_DIR, "logs/")
        path_input = os.path.join(settings.BASE_DIR, "scripts/")

        logs_filename = path_logs+"_"+os.path.splitext(os.path.basename(__file__))[0] + ".txt"

        image_length, image_height, image_margin, header_space, footer_space, image_multiplier, image_multiplier_small = get_env_values()

        if os.environ.get("RX_STATIC_FLOORPLAN_LOCATION") is not None:
                erase_files_in_dir(str(os.environ.get("RX_STATIC_FLOORPLAN_LOCATION")))
        if os.environ.get("RX_STATIC_GRAPHS_LOCATION") is not None:
                erase_files_in_dir(str(os.environ.get("RX_STATIC_GRAPHS_LOCATION")))
        if os.environ.get("RX_STATIC_INITIAL_VIEW_LOCATION") is not None:
                erase_files_in_dir(str(os.environ.get("RX_STATIC_INITIAL_VIEW_LOCATION")))

        event_name = "ISC West 2025"
        rxe = get_event(event_name)

        if(1==1): # quick reset
                max_id = event_sales_by_run.objects.aggregate(Max('esbr_run_id'))
                if(max_id['esbr_run_id__max'] is not None):
                        for xx in range(0, max_id['esbr_run_id__max']+1):
                                event_sales_by_run.objects.filter(esbr_run_id = xx).delete()
                for x in stands.objects.all():
                        stand_analysis.objects.filter(sa_stand=x).delete()
                        stand_attributes.objects.filter(sa_stand=x).delete()

#one or other...
        #        record_log_data("aaa_run_process.py", "run", "starting... reset data")
                aaa_reset_and_load.run()
                event_name = "ISC West 2025"
                rxe = get_event(event_name)
#                load_stand_attribute_data(rxe, 'ISC_West25_stand_attributes.xlsx')
        #        record_log_data("aaa_run_process.py", "run", "completed... load data")

                cut_down_to_emerging_tech(rxe)

                event_determine_floorplan_max_length_height(rxe)
                event_group_and_calculate_square_dim_prices(rxe)

                record_log_data("aaa_run_process.py", "run", "starting... run_event_year")
                stand_analysis_price_initial(rxe, 0)  #zero is the actual sold stands and serves as a base
                run_event_start(rxe)
#                for x in stands.objects.filter(s_rx_event=rxe):
#                         stand_print_all_records(x, 0)
                record_log_data("aaa_run_process.py", "run", "complete... run_event_year")

                record_log_data("aaa_run_process.py", "run", "starting... run_event_year")
                stand_analysis_price_initial(rxe, 0)  #zero is the actual sold stands and serves as a base
                run_event_year(rxe, False)
                record_log_data("aaa_run_process.py", "run", "complete... run_event_year")

        record_log_data("aaa_run_process.py", "run", "starting... render_revenue_graph")
        run_revenue_graph(rxe)
        record_log_data("aaa_run_process.py", "run", "complete... render_revenue_graph")


#        if(rx_event is not None):
#                pricing_rules.objects.filter(prb_event = rx_event).delete()
#                load_pr(rx_event)

##                recs = pricing_rules_get_all_data(rx_event, 0)
##                for q in recs:
##                        print(q)

#                for r in range(1, 2):
#                        print("Pricing Rule Base: " + str(r))
#                        pricing_copy_base(rx_event, r)
##                        recs = pricing_rules_get_all_data(rx_event, r)
##                        for q in recs:
##                                print(q)
#                        run_event_monte_carlo_simulation(rx_event, r, False)


#        create_mov_from_images('floorplans', 'output.mp4')

#        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
#        f.close()

#python manage.py runscript aaa_run_process
