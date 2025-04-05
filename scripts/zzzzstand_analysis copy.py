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
from math import sqrt
import random


from base.models import *
from users.models import *
from scripts.helper_functions import *
from scripts.event_analysis import *

from django.db.models import Max

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")



def stand_record_analysis_record(stand, run_id, analysis_number, analysis_title, sa_analysis_value, sa_analysis_type):
#possible problem here if analysis_number is None.  Not calculating next up
#        print(f"stand_record_analysis_record: {stand.s_number} {analysis_number} {analysis_title} {sa_analysis_value} {sa_analysis_type}")
        if(stand is not None and run_id is not None):
                if(analysis_number is not None):
                        up, created = stand_analysis.objects.update_or_create(
                                sa_stand=stand,
                                sa_run_id=run_id,
                                sa_analysis_number=analysis_number,
                                defaults={
                                        'sa_analysis_title': analysis_title,
                                        'sa_analysis_value': sa_analysis_value,
                                        'sa_analysis_type': sa_analysis_type,
                                        'sa_analysis_datetime': timezone.now(),
                                })
                else:
                        max_analysis_number = stand_analysis.objects.filter(sa_stand=stand,sa_run_id=run_id).aggregate(Max('sa_analysis_number'))
                        if max_analysis_number['sa_analysis_number__max'] is None:
                                a_number = 100
                        else:
                                a_number = int(max_analysis_number['sa_analysis_number__max']) + 10                
                        if(analysis_title is not None):
                                up, created = stand_analysis.objects.update_or_create(
                                        sa_stand=stand,
                                        sa_run_id=run_id,
                                        sa_analysis_title=analysis_title,
                                        defaults={
                                                'sa_analysis_number': a_number,
                                                'sa_analysis_value': sa_analysis_value,
                                                'sa_analysis_type': sa_analysis_type,
                                                'sa_analysis_datetime': timezone.now(),
                                        })

def stand_get_analysis_record(stand, run_id, analysis_number, analysis_title):
        sa = None
        if(analysis_number is not None):
                try:
                        sa = stand_analysis.objects.get(sa_stand=stand, sa_run_id = run_id, sa_analysis_number=analysis_number)
                except stand_analysis.DoesNotExist:
                        sa = None
        if sa is None:
                if(analysis_title is not None):
                        try:
                                sa = stand_analysis.objects.get(sa_stand=stand, sa_run_id = run_id, sa_analysis_title=analysis_title)
                        except stand_analysis.DoesNotExist:
                                sa = None
        sa_analysis_number = None
        sa_analysis_title = None
        sa_analysis_value = None
        if sa is not None:
                sa_analysis_number = sa.sa_analysis_number
                sa_analysis_title = sa.sa_analysis_title
                if(sa.sa_analysis_type == 'integer'):
                        try:
                                sa_analysis_value = int(sa.sa_analysis_value)
                        except ValueError:
                                sa_analysis_value = 0
                if(sa.sa_analysis_type == 'float'):
                        try:
                                sa_analysis_value = round(float(sa.sa_analysis_value),2)
                        except ValueError:
                                sa_analysis_value = 0.0
                if(sa.sa_analysis_type == 'string'):
                        sa_analysis_value = str(sa.sa_analysis_value)
                if(sa.sa_analysis_type == 'datetime'):
                        sa_analysis_value = timezone.datetime.strptime(sa.sa_analysis_value, "%Y-%m-%d %H:%M:%S.%f")
                if(sa.sa_analysis_type == 'boolean'):
                        sa_analysis_value = bool(sa.sa_analysis_value)
        return sa_analysis_number, sa_analysis_title, sa_analysis_value

def stand_get_all_analysis_records(stand, run_id):
        stand_data = []
        sa = None
        try:
                sa = stand_analysis.objects.filter(sa_stand=stand, sa_run_id = run_id)
        except stand_analysis.DoesNotExist:
                sa = None
        for q in sa:
                sa_analysis_number, sa_analysis_title, sa_analysis_value = stand_get_analysis_record(stand, q.sa_run_id, q.sa_analysis_number, q.sa_analysis_title) 
                stand_data.append([sa_analysis_number,sa_analysis_title,sa_analysis_value])
        return stand_data

def stand_calc_and_store_gradient(st, run_id, sq_price, min_price, max_price):
        sa_analysis_number, sa_analysis_title, price = stand_get_analysis_record(st, run_id, None, 'Price Per sq ft')
#        print(f"stand_calc_and_store_gradient: {st.s_number} {sq_price} {min_price} {max_price} {price}")
        if(price is None):
                cprice = 0.0
        else:
                try:
                        cprice = float(price)
                except (ValueError, TypeError):
                        cprice = 0.0
        if(cprice == 0.0):
                calc_gr = 0
        else:
                if(cprice < min_price):
                        calc_gr = 1
                else:
                        if(cprice < sq_price):
                                calc_gr = (((cprice - min_price) / (sq_price-min_price))*100) / 2
                        else:
                                calc_gr = 50 + (((cprice - sq_price) / (max_price-sq_price))*100)/2
        try:
                calc_gr = int(calc_gr)
        except (ValueError, TypeError):
                calc_gr = 0
        if(calc_gr > 100):
                calc_gr = 100
        if(calc_gr < 0):
                calc_gr = 0
#        print(f"calc_gr: {calc_gr}")
        stand_record_analysis_record(st, run_id, 300, 'Sq Foot Gradient', str(int(calc_gr)), 'integer')

def stand_analysis_price(rxe, run_id):

        stand_not_found = 0
        stands_found = 0
        if(rxe is not None):
                stand_analysis.objects.filter(sa_stand__s_rx_event = rxe, sa_run_id = run_id).delete()
                for x in event_sales_transactions.objects.filter(est_event = rxe):
#                        print(f"Stand: {x.est_Stand_Name_Cleaned} Customer Type: {x.est_Customer_Type} Stand Area: {x.est_Stand_Name_Dim_Cleaned} Net Price: {x.est_Total_Net_Amount}")
                        st = stand_location.objects.filter(sl_stand__s_rx_event=rxe, sl_stand__s_number=x.est_Stand_Name_Cleaned)
                        if(len(st) > 0):
                                stands_found += 1
                        else:
                                st = stand_location.objects.filter(sl_stand__s_rx_event=rxe, sl_stand__s_name__iexact=x.est_Company_Name.lower())
                        if(len(st) == 0):
                                stand_not_found += 1
#                                print(f"Stand: {x.est_Stand_Name_Cleaned} not found in stand_location")
#                                print(f"    est_Company_Name: {x.est_Company_Name}, est_Stand_Name_Length_Width: {x.est_Stand_Name_Length_Width} est_Stand_Name_Cleaned: {x.est_Stand_Name_Cleaned}")
#                                print(f"    est_Stand_Name_Dim_Cleaned: {x.est_Stand_Name_Dim_Cleaned} est_Total_Net_Amount: {x.est_Total_Net_Amount}")
#                                print(f"    Stand: {x.est_Stand_Name_Cleaned} Customer Type: {x.est_Customer_Type} Stand Area: {x.est_Stand_Name_Dim_Cleaned} Net Price: {x.est_Total_Net_Amount}")
                        for fs in st:
#                                print(f"fs.sl_x_length: {fs.sl_x_length} fs.sl_y_length: {fs.sl_y_length}")
                                stand_record_analysis_record(fs.sl_stand, run_id, 10, 'Stand Zone', str(x.est_Stand_Area), 'string')
                                stand_record_analysis_record(fs.sl_stand, run_id, 20, 'Customer Type', str(x.est_Customer_Type), 'string')
                                if(fs.sl_x_length is not None and fs.sl_y_length is not None):
                                        st_area = str(fs.sl_y_length) + "x" + str(fs.sl_x_length)
                                else:
                                        st_area = "Unknown"
#                                print(f"Stand Area: {st_area}")
                                stand_record_analysis_record(fs.sl_stand, run_id, 30, 'Stand Area', st_area, 'string')
#                                print(f"est_Total_Net_Amount: {x.est_Total_Net_Amount} fs.sl_x_length: {fs.sl_x_length} fs.sl_y_length: {fs.sl_y_length}")
                                stand_record_analysis_record(fs.sl_stand, run_id, 40, 'Net Price', str(float(x.est_Total_Net_Amount)), 'float')
                                stand_record_analysis_record(fs.sl_stand, run_id, 50, 'Price Per sq ft', str(float(float(x.est_Total_Net_Amount)/float(fs.sl_x_length * fs.sl_y_length))), 'float')
                                stand_calc_and_store_gradient(fs.sl_stand, run_id, 129.49, 68.42, 246.55)
        print(f"Stand not found: {stand_not_found}, Stands found: {stands_found}")                        


def stand_analysis_price_apply_monte_carlo(sales_rec, given_stand, run_id):

        for fs in stand_location.objects.filter(sl_stand = given_stand):
                stand_record_analysis_record(fs.sl_stand, run_id, 10, 'Stand Zone', str(sales_rec.est_Stand_Area), 'string')
                stand_record_analysis_record(fs.sl_stand, run_id, 20, 'Customer Type', str(sales_rec.est_Customer_Type), 'string')
                if(fs.sl_x_length is not None and fs.sl_y_length is not None):
                        st_area = str(fs.sl_y_length) + "x" + str(fs.sl_x_length)
                        st_area_total = float(fs.sl_x_length * fs.sl_y_length)
                else:
                        st_area = "Unknown"
                        st_area_total = 1
                stand_record_analysis_record(fs.sl_stand, run_id, 30, 'Sold Stand Area', st_area, 'string')
                stand_record_analysis_record(fs.sl_stand, run_id, 40, 'Sold Net Price', str(float(sales_rec.est_Total_Net_Amount)), 'float')
                stand_record_analysis_record(fs.sl_stand, run_id, 50, 'Sold Price Per sq ft', str(float(float(sales_rec.est_Total_Net_Amount)/st_area_total)), 'float')
                stand_record_analysis_record(fs.sl_stand, run_id, 60, 'Corners', str(sales_rec.est_Number_of_Corners), 'string')
                stand_record_analysis_record(fs.sl_stand, run_id, 61, 'Stand Zone', str(sales_rec.est_Stand_Zone), 'string')
                stand_record_analysis_record(fs.sl_stand, run_id, 62, 'Floor Plan Sector', str(sales_rec.est_Floor_Plan_Sector), 'string')

                rxe = given_stand.s_rx_event
                p_title = "Base Sq Price"
                base_number, base_title, base_value, base_start_date, base_end_date = pricing_rules_get(rxe, run_id, None, p_title) 
                try:
                        cnr = int(sales_rec.est_Number_of_Corners)
                except (ValueError, TypeError):
                        cnr = 1
                p_title = "Corners: " + str(cnr)
                corners_number, corners_title, corners_value, corners_start_date, corners_end_date = pricing_rules_get(rxe, run_id, None, p_title) 

                p_title = "Stand Zone: " + str(sales_rec.est_Stand_Zone).strip()
                sz_number, sz_title, sz_value, sz_start_date, sz_end_date = pricing_rules_get(rxe, run_id, None, p_title) 

                p_title = "Floor Plan Sector: " + str(sales_rec.est_Floor_Plan_Sector).strip()
                fps_number, fps_title, fps_value, fps_start_date, fps_end_date = pricing_rules_get(rxe, run_id, None, p_title) 

                all_rules = ""
                mc_price = 0.0
                if(base_title is not None):
                        all_rules += str(base_title) + ": " + str(base_value) + ", "
                        mc_price = base_value * st_area_total
                if(corners_title is not None):
                        all_rules += str(corners_title) + ": " + str(corners_value) + ", "
                        mc_price = mc_price * corners_value
                if(sz_title is not None):
                        all_rules += str(sz_title) + ": " + str(sz_value) + ", "
#                        mc_price = mc_price * sz_value
                if(fps_title is not None):
                        all_rules += str(fps_title) + ": " + str(fps_value) + ", "
#                        mc_price = mc_price * fps_value

                stand_record_analysis_record(fs.sl_stand, run_id, 240, 'Net Price', str(float(mc_price)), 'float')
                stand_record_analysis_record(fs.sl_stand, run_id, 250, 'Price Per sq ft', str(float(float(mc_price)/st_area_total)), 'float')
                stand_calc_and_store_gradient(fs.sl_stand, run_id, 129.49, 68.42, 246.55)
#                stand_calc_and_store_gradient(fs.sl_stand, run_id, 40, 1, 80)
                stand_record_analysis_record(fs.sl_stand, run_id, 260, 'MC Rules Applied', all_rules, 'string')
                sa_analysis_number, sa_analysis_title, sa_analysis_value = stand_get_analysis_record(fs.sl_stand, run_id, None, 'Sq Foot Gradient')
#                print(f"{sa_analysis_number} {sa_analysis_title} {sa_analysis_value}")
#                for ppp in stand_get_all_analysis_records(fs.sl_stand, run_id):
#                        print(f"{ppp[0]} {ppp[1]} {ppp[2]}")
#        pricing_rules_record(rxe, 0, None, 'Base Sq Price', '30.0', 'float', default_start_date, default_end_date)
#        pricing_rules_record(rxe, 0, None, 'Corners: 1', '1', 'float', default_start_date, default_end_date)
#        pricing_rules_record(rxe, 0, None, 'Stand Zone: Standard 4', '8', 'float', default_start_date, default_end_date)
#        pricing_rules_record(rxe, 0, None, 'Floor Plan Sector: Drones and Robotics', '1', 'float', default_start_date, default_end_date)





def build_stand_gradient(rxe, run_id):

        extremes_to_delete = 10
        stand_count = 0
        average_sq_price_total = 0.0
        max_price = 0.0
        min_price = 999999999.0
        price_list = []
        if(rxe is not None):
                for xx in stands.objects.filter(s_rx_event=rxe):
                        sa_analysis_number, sa_analysis_title, price = stand_get_analysis_record(xx, run_id, None, 'Price Per sq ft')
                        try:
                                cor_price = float(price)
                        except (ValueError, TypeError):
                                cor_price = 0.0
                        if(cor_price > 0):
                                price_list.append(cor_price)
#                                stand_count += 1
#                                average_sq_price_total += cor_price
#                        if(cor_price >= max_price):
#                                max_price = cor_price
#                        if(cor_price <= min_price and cor_price != 0.0):
#                                min_price = cor_price
                price_list.sort()
                if(len(price_list) > extremes_to_delete*2):
                        price_list = price_list[extremes_to_delete:-extremes_to_delete]
                average_sq_price = sum(price_list) / len(price_list)
                max_price = price_list[-1]
                min_price = price_list[0]
                if(min_price < 0.0):
                        min_price = 1
                print(f"Average sq price: {average_sq_price}, stand_count: {stand_count}, Max Price: {max_price} Min Price: {min_price}")
                for xx in stands.objects.filter(s_rx_event=rxe):
                        sa_analysis_number, sa_analysis_title, price = stand_get_analysis_record(xx, run_id, None, 'Price Per sq ft')
                        if(price is None):
                                cprice = 0.0
                        else:
                                try:
                                        cprice = float(price)
                                except (ValueError, TypeError):
                                        cprice = 0.0
                        if(cprice == 0.0):
                                calc_gr = 0
                        else:
                                if(cprice < min_price):
                                        calc_gr = 1
                                else:
                                        if(cprice < average_sq_price):
                                                calc_gr = (((cprice - min_price) / (average_sq_price-min_price))*100) / 2
                                        else:
                                                calc_gr = 50 + (((cprice - average_sq_price) / (max_price-average_sq_price))*100)/2
                        try:
                                calc_gr = int(calc_gr)
                        except (ValueError, TypeError):
                                calc_gr = 0
                        if(calc_gr > 100):
                                calc_gr = 100
                        if(calc_gr < 0):
                                calc_gr = 0
                        xx.s_stand_price_gradient = int(calc_gr)
                        xx.save()
                        stand_record_analysis_record(xx, run_id, None, 'Sq Foot Gradient All', str(int(calc_gr)), 'integer')

