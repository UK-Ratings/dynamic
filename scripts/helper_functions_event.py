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
import datetime


from base.models import *
from users.models import *
from scripts.helper_functions import *
from scripts.helper_functions_stand import *

from django.db.models import Max

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")

def create_event_group(group_name):
        try:
                event_group = rx_event_group.objects.get(reg_name=group_name)
        except rx_event_group.DoesNotExist:
                event_group = rx_event_group.objects.create(reg_name=group_name)
        return event_group
def create_event(eg_name, ev_name, ev_start_date, ev_end_date):
        egn = create_event_group(eg_name)
        eve, create = rx_event.objects.update_or_create(re_event_group = egn, 
                re_name=ev_name, defaults={
                're_floor_length': 0, 're_floor_height': 0,
                're_event_start_date': ev_start_date,
                're_event_end_date': ev_end_date})
        return eve
def update_event_length_height(eve, fl_length, fl_height):
        eve.re_floor_length = 1232#fl_length
        eve.re_floor_height = 1052#fl_height
        eve.save()

def event_calculate_avg_sq_price(event_name):
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
                        sa_analysis_number, sa_analysis_title, price = stand_get_analysis_record(xx, None, 'Price Per sq ft')
                        try:
                                cor_price = float(price)
                        except (ValueError, TypeError):
                                cor_price = 0.0
                        if(cor_price > 0):
                                price_list.append(cor_price)
                price_list.sort()
                if(len(price_list) > extremes_to_delete*2):
                        price_list = price_list[extremes_to_delete:-extremes_to_delete]
                average_sq_price = sum(price_list) / len(price_list)
                max_price = price_list[-1]
                min_price = price_list[0]
                if(min_price < 0.0):
                        min_price = 1
                print(f"Average sq price: {average_sq_price}, stand_count: {stand_count}, Max Price: {max_price} Min Price: {min_price}")

