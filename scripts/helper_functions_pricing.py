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


def pricing_rules_record(rxe, p_run_id, p_number, p_title, p_value, p_type, p_start_datetime, p_end_datetime):
        if(p_run_id is not None) and (rxe is not None):
                if(p_number is not None):
                        up, created = pricing_rules.objects.update_or_create(
                                prb_event=rxe,
                                prb_run_id=p_run_id,
                                prb_number=p_number,
                                defaults={
                                        'prb_title': p_title,
                                        'prb_value': p_value,
                                        'prb_type': p_type,
                                        'prb_start_datetime': p_start_datetime,
                                        'prb_end_datetime': p_end_datetime
                                })
                else:
                        max_number = pricing_rules.objects.filter(prb_event=rxe,prb_run_id=p_run_id).aggregate(Max('prb_number'))
                        if max_number['prb_number__max'] is None:
                                p_number = 100
                        else:
                                p_number = int(max_number['prb_number__max']) + 10                
                        if(p_title is not None):
                                up, created = pricing_rules.objects.update_or_create(
                                        prb_event=rxe,
                                        prb_run_id=p_run_id,
                                        prb_title=p_title,
                                        defaults={
                                                'prb_number': p_number,
                                                'prb_value': p_value,
                                                'prb_type': p_type,
                                                'prb_start_datetime': p_start_datetime,
                                                'prb_end_datetime': p_end_datetime
                                        })
def pricing_rules_get(rxe, p_run_id, p_number, p_title):
        pr_number = None
        pr_title = None
        pr_value = None
        pr_start_date = None
        pr_end_date = None
        pr = None
        if(p_run_id is not None) and (rxe is not None):
                if(p_number is not None):
                        try:
                                pr = pricing_rules.objects.get(prb_event=rxe, prb_run_id=p_run_id, prb_number=p_number)
                        except pricing_rules.DoesNotExist:
                                pr = None
                if(pr is None) and (p_title is not None):
                        try:
                                pr = pricing_rules.objects.get(prb_event=rxe, prb_run_id=p_run_id, prb_title=p_title)
                        except pricing_rules.DoesNotExist:
                                pr = None
                if(pr is not None):
                        pr_number = pr.prb_number
                        pr_title = pr.prb_title
                        pr_start_date = pr.prb_start_datetime
                        pr_end_date = pr.prb_end_datetime
                        if(pr.prb_type == 'integer'):
                                try:
                                        pr_value = int(pr.prb_value)
                                except ValueError:
                                        pr_value = 0
                        if(pr.prb_type == 'float'):
                                try:
                                        pr_value = round(float(pr.prb_value),2)
                                except ValueError:
                                        pr_value = 0.0
                        if(pr.prb_type == 'string'):
                                pr_value = str(pr.prb_value)
                        if(pr.prb_type == 'datetime'):
                                pr_value = timezone.datetime.strptime(pr.prb_value, "%Y-%m-%d %H:%M:%S.%f")
                        if(pr.prb_type == 'boolean'):
                                pr_value = bool(pr.prb_value)
                return pr_number, pr_title, pr_value, pr_start_date, pr_end_date
def pricing_rules_get_all_data(rxe, p_run_id):
        pr_data = []
        pr_recs = pricing_rules.objects.filter(prb_event=rxe, prb_run_id=p_run_id).order_by('prb_number')
        for q in pr_recs:
                pr_number, pr_title, pr_value, pr_start_date, pr_end_date = pricing_rules_get(rxe, p_run_id, q.prb_number, q.prb_title) 
                pr_data.append([pr_number, pr_title, pr_value, pr_start_date, pr_end_date])
        return pr_data


def load_pr(rxe):

        default_start_date = timezone.make_aware(datetime.datetime(2024, 4, 12, 0, 0, 0))
        default_end_date = timezone.make_aware(datetime.datetime(2025, 4, 4, 0, 0, 0))

        pricing_rules_record(rxe, 0, None, 'Base Sq Price', '30.0', 'float', default_start_date, default_end_date)
        pricing_rules_record(rxe, 0, None, 'Corners: 1', '1', 'float', default_start_date, default_end_date)
        pricing_rules_record(rxe, 0, None, 'Corners: 2', '2', 'float', default_start_date, default_end_date)
        pricing_rules_record(rxe, 0, None, 'Corners: 3', '4', 'float', default_start_date, default_end_date)
        pricing_rules_record(rxe, 0, None, 'Corners: 4', '8', 'float', default_start_date, default_end_date)
        pricing_rules_record(rxe, 0, None, 'Corners: 0', '1', 'float', default_start_date, default_end_date)

        pricing_rules_record(rxe, 0, None, 'Stand Zone: Premium 1', '20', 'float', default_start_date, default_end_date)
        pricing_rules_record(rxe, 0, None, 'Stand Zone: Standard 1', '2', 'float', default_start_date, default_end_date)
        pricing_rules_record(rxe, 0, None, 'Stand Zone: Standard 2', '4', 'float', default_start_date, default_end_date)
        pricing_rules_record(rxe, 0, None, 'Stand Zone: Standard 3', '6', 'float', default_start_date, default_end_date)
        pricing_rules_record(rxe, 0, None, 'Stand Zone: Standard 4', '8', 'float', default_start_date, default_end_date)
        pricing_rules_record(rxe, 0, None, 'Stand Zone: Standard 5', '10', 'float', default_start_date, default_end_date)
        pricing_rules_record(rxe, 0, None, 'Stand Zone: Standard 6', '12', 'float', default_start_date, default_end_date)
        pricing_rules_record(rxe, 0, None, 'Stand Zone: Target Market 1', '14', 'float', default_start_date, default_end_date)
        pricing_rules_record(rxe, 0, None, 'Stand Zone: Target Market 8', '16', 'float', default_start_date, default_end_date)

        pricing_rules_record(rxe, 0, None, 'Floor Plan Sector: 3 Alarm', '1', 'float', default_start_date, default_end_date)
        pricing_rules_record(rxe, 0, None, 'Floor Plan Sector: Cyber Security n ConIOT', '2', 'float', default_start_date, default_end_date)
        pricing_rules_record(rxe, 0, None, 'Floor Plan Sector: Drones and Robotics', '4', 'float', default_start_date, default_end_date)
        pricing_rules_record(rxe, 0, None, 'Floor Plan Sector: Emerging Tech', '8', 'float', default_start_date, default_end_date)
        pricing_rules_record(rxe, 0, None, 'Floor Plan Sector: International Sourcing', '16', 'float', default_start_date, default_end_date)
        pricing_rules_record(rxe, 0, None, 'Floor Plan Sector: Public Safety', '20', 'float', default_start_date, default_end_date)
        pricing_rules_record(rxe, 0, None, 'Floor Plan Sector: Smart Home', '24', 'float', default_start_date, default_end_date)

        start_date = timezone.make_aware(datetime.datetime(2024, 4, 12, 0, 0, 0))
        end_date = timezone.make_aware(datetime.datetime(2024, 6, 12, 0, 0, 0))
        pricing_rules_record(rxe, 0, None, 'Early Brid Discount', '-.10', 'float', start_date, end_date)
        pricing_rules_record(rxe, 0, None, 'Price Increase', '10.0', 'float', default_start_date, default_end_date)
        pricing_rules_record(rxe, 0, None, 'Price Decrease', '15.9', 'float', default_start_date, default_end_date)
#        for x in pricing_rules.objects.filter(prb_event=rxe).order_by('prb_run_id','prb_number'):
#                print(f"Pricing Rules: {x.prb_run_id} {x.prb_number} {x.prb_title} {x.prb_value} {x.prb_type} {x.prb_start_datetime} {x.prb_end_datetime}")


def pricing_copy_base(rxe, p_run_id):
        for x in pricing_rules.objects.filter(prb_event=rxe, prb_run_id=0).order_by('prb_number'):
                pricing_rules_record(rxe, p_run_id, x.prb_number, x.prb_title, x.prb_value, x.prb_type, x.prb_start_datetime, x.prb_end_datetime)


