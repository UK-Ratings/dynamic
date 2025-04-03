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

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")

def record_stand_analysis(stand, analysis_number, analysis_title, sa_analysis_value, sa_analysis_type):
#        print(f"record_stand_analysis: {stand.s_number} {analysis_number} {analysis_title} {sa_analysis_value} {sa_analysis_type}")
        if(analysis_number is not None):
                up, created = stand_analysis.objects.update_or_create(
                        sa_stand=stand,
                        sa_analysis_number=analysis_number,
                        defaults={
                                'sa_analysis_title': analysis_title,
                                'sa_analysis_value': sa_analysis_value,
                                'sa_analysis_type': sa_analysis_type,
                                'sa_analysis_datetime': timezone.now(),
                        })
        else:
                if(analysis_title is not None):
                        up, created = stand_analysis.objects.update_or_create(
                                sa_stand=stand,
                                sa_analysis_title=analysis_title,
                                defaults={
                                        'sa_analysis_number': analysis_number,
                                        'sa_analysis_value': sa_analysis_value,
                                        'sa_analysis_type': sa_analysis_type,
                                        'sa_analysis_datetime': timezone.now(),
                                })
#        if created:
#                print(f"Created: {up.sa_analysis_title} {up.sa_analysis_value} {up.sa_analysis_type}")
#        else:
#                print(f"Updated: {up.sa_analysis_title} {up.sa_analysis_value} {up.sa_analysis_type}")

def get_stand_analysis(stand, analysis_number, analysis_title):
        sa = None
        if(analysis_number is not None):
                try:
                        sa = stand_analysis.objects.get(sa_stand=stand, sa_analysis_number=analysis_number)
                except stand_analysis.DoesNotExist:
                        sa = None
        if sa is None:
                if(analysis_title is not None):
                        try:
                                sa = stand_analysis.objects.get(sa_stand=stand, sa_analysis_title=analysis_title)
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

def stand_analysis_price(event_name):
        try:
                rxe = rx_event.objects.get(re_name=event_name)
        except rx_event.DoesNotExist:
                rxe = None

        stand_not_found = 0
        stands_found = 0
        if(rxe is not None):
                stand_analysis.objects.filter(sa_stand__s_rx_event = rxe).delete()
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
                                record_stand_analysis(fs.sl_stand, 10, 'Stand Zone', str(x.est_Stand_Area), 'string')
                                record_stand_analysis(fs.sl_stand, 20, 'Customer Type', str(x.est_Customer_Type), 'string')
                                if(fs.sl_x_length is not None and fs.sl_y_length is not None):
                                        st_area = str(fs.sl_y_length) + "x" + str(fs.sl_x_length)
                                else:
                                        st_area = "Unknown"
#                                print(f"Stand Area: {st_area}")
                                record_stand_analysis(fs.sl_stand, 30, 'Stand Area', st_area, 'string')
#                                print(f"est_Total_Net_Amount: {x.est_Total_Net_Amount} fs.sl_x_length: {fs.sl_x_length} fs.sl_y_length: {fs.sl_y_length}")
                                record_stand_analysis(fs.sl_stand, 40, 'Net Price', str(float(x.est_Total_Net_Amount)), 'float')
                                record_stand_analysis(fs.sl_stand, 50, 'Price Per sq ft', str(float(float(x.est_Total_Net_Amount)/float(fs.sl_x_length * fs.sl_y_length))), 'float')
        print(f"Stand not found: {stand_not_found}, Stands found: {stands_found}")                        

def build_stand_gradient(event_name):
        try:
                rxe = rx_event.objects.get(re_name=event_name)
        except rx_event.DoesNotExist:
                rxe = None

        extremes_to_delete = 10
        stand_count = 0
        average_sq_price_total = 0.0
        max_price = 0.0
        min_price = 999999999.0
        price_list = []
        if(rxe is not None):
                for xx in stands.objects.filter(s_rx_event=rxe):
                        sa_analysis_number, sa_analysis_title, price = get_stand_analysis(xx, None, 'Price Per sq ft')
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
                        sa_analysis_number, sa_analysis_title, price = get_stand_analysis(xx, None, 'Price Per sq ft')
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
