#!/usr/bin/env python3

import cv2
import os

from base.models import *
from django.conf import settings
from django.utils import timezone
from dotenv import load_dotenv
import random


from base.models import *
from users.models import *
from scripts.helper_functions import *
from scripts.helper_functions_pricing import *

from django.db.models import Max


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")

def stand_attributes_record(s_stand, s_number, s_title, s_value, s_type, s_datetime):
#       Stand Status:  Available, Sold, New Sell, Reserved, New Stand
#       Stand Price: Base, Price Increase, Price Decrease 
#        print(f"stand_attribues_record {s_stand} {s_number} {s_title} {s_value} {s_type} {s_datetime}")
        if(s_stand is not None) and ((s_number is not None) or (s_title is not None)):
                if(s_number is not None):
                        up, created = stand_attributes.objects.update_or_create(
                                sa_stand=s_stand,
                                sa_number=s_number,
                                defaults={
                                        'sa_title': s_title,
                                        'sa_value': s_value,
                                        'sa_type': s_type,
                                        'sa_datetime': s_datetime
                                })
                else:
                        max_number = stand_attributes.objects.filter(sa_stand = s_stand).aggregate(Max('sa_number'))
                        if max_number['sa_number__max'] is None:
                                s_number = 100
                        else:
                                s_number = int(max_number['sa_number__max']) + 10                
                        if(s_title is not None):
                                up, created = stand_attributes.objects.update_or_create(
                                        sa_stand=s_stand,
                                        sa_title=s_title,
                                        defaults={
                                                'sa_number': s_number,
                                                'sa_value': s_value,
                                                'sa_type': s_type,
                                                'sa_datetime': s_datetime
                                        })
def stand_attributes_get(st_stand, st_number, st_title):
        s_number = None
        s_title = None
        s_value = None
        s_datetime = None
        sa = None
        if(st_stand is not None) and ((st_number is not None) or (st_title is not None)):
                if(s_number is not None):
                        try:
                                sa = stand_attributes.objects.get(sa_stand=st_stand, sa_number=st_number)
                        except stand_attributes.DoesNotExist:
                                sa = None
                if(sa is None) and (st_title is not None):
                        try:
                                sa = stand_attributes.objects.get(sa_stand=st_stand, sa_title=st_title)
                        except stand_attributes.DoesNotExist:
                                sa = None
                if(sa is not None):
                        s_number = sa.sa_number
                        s_title = sa.sa_title
                        s_datetime = sa.sa_datetime
                        if(sa.sa_type == 'integer'):
                                try:
                                        s_value = int(sa.sa_value)
                                except ValueError:
                                        s_value = 0
                        if(sa.sa_type == 'float'):
                                try:
                                        s_value = round(float(sa.sa_value),2)
                                except ValueError:
                                        s_value = 0.0
                        if(sa.sa_type == 'string'):
                                s_value = str(sa.sa_value)
                        if(sa.sa_type == 'datetime'):
                                s_value = timezone.datetime.strptime(sa.sa_value, "%Y-%m-%d %H:%M:%S.%f")
                        if(sa.sa_type == 'boolean'):
                                s_value = bool(sa.sa_value)
                return s_number, s_title, s_value, s_datetime
def stand_attributes_get_all_data(st_stand):
        sa_data = []
        sa_recs = stand_attributes.objects.filter(sa_stand=st_stand).order_by('sa_number')
        for q in sa_recs:
                s_number, s_title, s_value, s_datetime = stand_attributes_get(q.sa_stand, q.sa_number, q.sa_title) 
                sa_data.append([s_number, s_title, s_value, s_datetime])
        return sa_data
def stand_attributes_get_value(st_stand, st_number, st_title):
        s_number, s_title, s_value, s_datetime = stand_attributes_get(st_stand, st_number, st_title) 
        return(s_value)       


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


def zzzstand_calc_and_store_gradient(st, run_id, sq_price, min_price, max_price, median_price):
        sa_analysis_number, sa_analysis_title, price = stand_get_analysis_record(st, run_id, None, 'Price Per sq')
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
        stand_record_analysis_record(st, run_id, 300, 'Sq Gradient', str(int(calc_gr)), 'integer')

def stand_calc_and_store_gradient(st, run_id):
        sa_analysis_number, sa_analysis_title, sq_price = stand_get_analysis_record(st, run_id, None, 'Price Per sq')
        sa_analysis_number, sa_analysis_title, min_price = stand_get_analysis_record(st, run_id, None, 'Min Price')
        sa_analysis_number, sa_analysis_title, max_price = stand_get_analysis_record(st, run_id, None, 'Max Price')
        sa_analysis_number, sa_analysis_title, median_price = stand_get_analysis_record(st, run_id, None, 'Median Price')

        calc_gr = 0
        if(sq_price is not None and min_price is not None 
           and max_price is not None and median_price is not None):
                try:
                        int(sq_price)
                except (ValueError, TypeError):
                        good_price = False
                else:
                        good_price = True
                if(good_price):
#                        print(f"stand_calc_and_store_gradient: {st.s_number} {sq_price} {min_price} {max_price} {median_price}")
                        if(min_price == 0):
                                calc_gr = 1
                        elif sq_price < min_price:
                                calc_gr = 1
                        elif sq_price > max_price:
                                calc_gr = 100
                        elif sq_price == median_price:
                                calc_gr = 50
                        elif sq_price < median_price:
                                calc_gr = 1 + ((sq_price - min_price) / (median_price - min_price)) * 49
                        else:
                                calc_gr = 50 + ((sq_price - median_price) / (max_price - median_price)) * 50
#        print(f"calc_gr: {calc_gr}")
        stand_record_analysis_record(st, run_id, None, 'Sq Gradient', str(int(calc_gr)), 'integer')

def zzzstand_analysis_price(rxe, run_id):

        stand_not_found = 0
        stands_found = 0
        if(rxe is not None):
                stand_analysis.objects.filter(sa_stand__s_rx_event = rxe, sa_run_id = run_id).delete()
                for x in event_sales_transactions.objects.filter(est_event = rxe):
                        tst = stands.objects.filter(s_rx_event=rxe, s_number=x.est_Stand_Name_Cleaned)
#                        st = stand_location.objects.filter(sl_stand__s_rx_event=rxe, sl_stand__s_number=x.est_Stand_Name_Cleaned)
                        if(len(tst) > 0):
                                stands_found += 1
                        else:
                                tst = stands.objects.filter(s_rx_event=rxe, s_name__iexact=x.est_Company_Name.lower())
                        if(len(tst) == 0):
                                stand_not_found += 1
                        for fs in tst:
                                stand_record_analysis_record(fs, run_id, 10, 'Stand Area', str(x.est_Stand_Area), 'string')
                                stand_record_analysis_record(fs, run_id, 20, 'Customer Type', str(x.est_Customer_Type), 'string')
                                sl_x_length= stand_attributes_get_value(fs, None, 'Stand x length')
                                sl_y_length= stand_attributes_get_value(fs, None, 'Stand y length')
                                if(sl_x_length is not None and sl_y_length is not None):
                                        st_area = str(sl_y_length) + "x" + str(sl_x_length)
                                else:
                                        st_area = "Unknown"
                                stand_record_analysis_record(fs, run_id, 30, 'A Stand Area', st_area, 'string')
                                stand_record_analysis_record(fs, run_id, 40, 'Net Price', str(float(x.est_Total_Net_Amount)), 'float')
                                stand_record_analysis_record(fs, run_id, 50, 'Price Per sq', str(float(float(x.est_Total_Net_Amount)/float(sl_x_length * sl_y_length))), 'float')
                                stand_calc_and_store_gradient(fs, run_id, 129.49, 68.42, 246.55)
#        print(f"Stand not found: {stand_not_found}, Stands found: {stands_found}")                        

def stand_analysis_price_initial(rxe, run_id):
        stand_not_found = 0
        stands_found = 0
        if(rxe is not None):
                stand_analysis.objects.filter(sa_stand__s_rx_event = rxe, sa_run_id = run_id).delete()
                for stt in stands.objects.filter(s_rx_event=rxe):#, s_number = 14059):
                        sl_x_length= stand_attributes_get_value(stt, None, 'Stand x length')
                        sl_y_length= stand_attributes_get_value(stt, None, 'Stand y length')
                        if(sl_x_length is not None and sl_y_length is not None):
                                st_area = str(sl_y_length) + "x" + str(sl_x_length)
                        else:
                                st_area = "Unknown"

                        fs = event_sales_transactions.objects.filter(est_event = rxe, 
                                        est_Stand_Name_Cleaned__iexact = stt.s_number.lower()).first()
                        if fs is None:
                                fs = event_sales_transactions.objects.filter(est_event = rxe, 
                                                est_Company_Name__iexact = stt.s_name.lower()).first()
                        if fs is not None:
                                stands_found += 1
#                                stand_attributes_record(stt, None, '', '', 'string', timezone.now())

                                stand_attributes_record(stt, None, 'Actual Stand Area', st_area, 'string', timezone.now())
                                #must have these to match back to grouped data
                                stand_attributes_record(stt, None, 'Stand Zone', str(fs.est_Stand_Zone), 'string', timezone.now())
                                stand_attributes_record(stt, None, 'Floor Plan Sector', str(fs.est_Floor_Plan_Sector), 'string', timezone.now())
                                stand_attributes_record(stt, None, 'Stand Area', str(fs.est_Stand_Area), 'string', timezone.now())
                                stand_attributes_record(stt, None, 'Number of Corners', str(fs.est_Number_of_Corners), 'string', timezone.now())

                                stand_record_analysis_record(stt, run_id, None, 'Net Price', str(float(fs.est_Total_Net_Amount)), 'float')
                                price_per_sq = float(float(fs.est_Total_Net_Amount)/float(sl_x_length * sl_y_length))
                                stand_record_analysis_record(stt, run_id, None, 'Price Per sq', str(price_per_sq), 'float')

                                estg = event_sales_transactions_grouped.objects.filter(estg_Stand_Zone=fs.est_Stand_Zone, 
                                                estg_Floor_Plan_Sector = fs.est_Floor_Plan_Sector,
                                                estg_Stand_Area = fs.est_Stand_Area, 
                                                estg_Number_of_Corners= fs.est_Number_of_Corners).first()
                                if(estg is not None):
                                        stand_record_analysis_record(stt, run_id, None, 'Min Price', str(float(estg.estg_min)), 'float')
                                        stand_record_analysis_record(stt, run_id, None, 'Max Price', str(float(estg.estg_max)), 'float')
                                        stand_record_analysis_record(stt, run_id, None, 'Avg Price', str(float(estg.estg_avg)), 'float')
                                        stand_record_analysis_record(stt, run_id, None, 'Median Price', str(float(estg.estg_median)), 'float')
                                else:
                                        stand_record_analysis_record(stt, run_id, None, 'Min Price', str(price_per_sq), 'float')
                                        stand_record_analysis_record(stt, run_id, None, 'Max Price', str(price_per_sq), 'float')
                                        stand_record_analysis_record(stt, run_id, None, 'Avg Price', str(price_per_sq), 'float')
                                        stand_record_analysis_record(stt, run_id, None, 'Median Price', str(price_per_sq), 'float')
                                stand_calc_and_store_gradient(stt, run_id)

                        else:
                                stand_not_found += 1
#                        sv = stand_attributes_get_all_data(stt)
#                        for qq in sv:
#                                print(f"{qq[0]} {qq[1]} {qq[2]} {qq[3]}")
#                        sa = stand_get_all_analysis_records(stt, run_id)
#                        for qq in sa:
#                                print(f"{qq[0]} {qq[1]} {qq[2]}")

def stand_analysis_price_apply_monte_carlo(sales_rec, given_stand, run_id):

#        for fs in stand_location.objects.filter(sl_stand = given_stand):
        for st in stands.objects.filter(id = given_stand.id):
                sl_x_length= stand_attributes_get_value(st, None, 'Stand x length')
                sl_y_length= stand_attributes_get_value(st, None, 'Stand y length')

                stand_record_analysis_record(st, run_id, 10, 'Stand Zone', str(sales_rec.est_Stand_Area), 'string')
                stand_record_analysis_record(st, run_id, 20, 'Customer Type', str(sales_rec.est_Customer_Type), 'string')
                if(sl_x_length is not None and sl_y_length is not None):
                        st_area = str(sl_y_length) + "x" + str(sl_x_length)
                        st_area_total = float(sl_x_length * sl_y_length)
                else:
                        st_area = "Unknown"
                        st_area_total = 1
                stand_record_analysis_record(st, run_id, 30, 'Sold Stand Area', st_area, 'string')
                stand_record_analysis_record(st, run_id, 40, 'Sold Net Price', str(float(sales_rec.est_Total_Net_Amount)), 'float')
                stand_record_analysis_record(st, run_id, 50, 'Sold Price Per sq', str(float(float(sales_rec.est_Total_Net_Amount)/st_area_total)), 'float')
                stand_record_analysis_record(st, run_id, 60, 'Corners', str(sales_rec.est_Number_of_Corners), 'string')
                stand_record_analysis_record(st, run_id, 61, 'Stand Zone', str(sales_rec.est_Stand_Zone), 'string')
                stand_record_analysis_record(st, run_id, 62, 'Floor Plan Sector', str(sales_rec.est_Floor_Plan_Sector), 'string')

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

                stand_record_analysis_record(st, run_id, 240, 'Net Price', str(float(mc_price)), 'float')
                stand_record_analysis_record(st, run_id, 250, 'Price Per sq', str(float(float(mc_price)/st_area_total)), 'float')
                stand_calc_and_store_gradient(st, run_id, 129.49, 68.42, 246.55)
#                stand_calc_and_store_gradient(fs.sl_stand, run_id, 40, 1, 80)
                stand_record_analysis_record(st, run_id, 260, 'MC Rules Applied', all_rules, 'string')
                sa_analysis_number, sa_analysis_title, sa_analysis_value = stand_get_analysis_record(st, run_id, None, 'Sq Gradient')
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
                        sa_analysis_number, sa_analysis_title, price = stand_get_analysis_record(xx, run_id, None, 'Price Per sq')
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
                        sa_analysis_number, sa_analysis_title, price = stand_get_analysis_record(xx, run_id, None, 'Price Per sq')
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
                        stand_record_analysis_record(xx, None, 'Sq Gradient', str(int(calc_gr)), 'integer', timezone.now())


#                        xx.s_stand_price_gradient = int(calc_gr)
#                        xx.save()
#                        stand_record_analysis_record(xx, run_id, None, 'Sq Gradient All', str(int(calc_gr)), 'integer')





def create_stand(eve, stand_name, stand_number, x, y, x_length, y_length):
#        if(stand_number == "2123" or stand_name == "Verkada"):
#                print("create_stand: ", stand_name, stand_number, x, y, x_length, y_length)
        st, created = stands.objects.update_or_create(s_rx_event= eve, 
                        s_name=stand_name,
                        s_number=stand_number)
#        ,
#                        defaults={
#                                's_stand_status':'Available', 
#                                's_stand_price':'Base',
#                                's_stand_price_gradient': random.randint(0, 100),})

#        sl = stand_location.objects.update_or_create(sl_stand=st, defaults={
#                                'sl_x':x, 'sl_y':y, 'sl_x_length':x_length, 'sl_y_length':y_length})
        stand_attributes_record(st, None, 'Stand x', str(x), 'float', timezone.now())
        stand_attributes_record(st, None, 'Stand y', str(y), 'float', timezone.now())
        stand_attributes_record(st, None, 'Stand x length', str(x_length), 'float', timezone.now())
        stand_attributes_record(st, None, 'Stand y length', str(y_length), 'float', timezone.now())
        stand_attributes_record(st, None, 'Stand Status', 'Available', 'string', timezone.now())
        stand_attributes_record(st, None, 'Stand Price', 'Base', 'string', timezone.now())
#        stand_attributes_record(st, None, 'Stand Price Gradient', str(random.randint(0, 100)), 'integer', timezone.now())


def build_stand_counts_by_date(rxe, ev_date):
    event_stand_count_by_date.objects.filter(escby_rx_event=rxe, escby_date=ev_date).delete()
#    for s in stand_location.objects.filter(sl_stand__s_rx_event=rxe):
    for st in stands.objects.filter(s_rx_event=rxe):
        sl_x_length = stand_attributes_get_value(st, None, 'Stand x length')
        sl_y_length = stand_attributes_get_value(st, None, 'Stand y length')
        stand_status = stand_attributes_get_value(st, None, 'Stand Status')

#        print(ev_date, s.sl_stand.s_stand_status, s.sl_x_length, s.sl_y_length)
        # Use get_or_create to fetch or create the object
        obj, created = event_stand_count_by_date.objects.get_or_create(
            escby_rx_event=rxe,
            escby_date=ev_date,
            escby_x_length=abs(sl_x_length),
            escby_y_length=abs(sl_y_length),
            escby_stand_status=stand_status,
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

def stand_build_sale_analysis(sales_t, st_info, run_id):
        analysis_set = []

        if(1==1): #sales data section
                analysis_set.append(["Stand: "+str(st_info.s_number), 'center', 'top'])

                analysis_set.append(["SALES ATTRIBUTES", 'left', 'top'])
                analysis_set.append(["Company Name: " + str(sales_t.est_Company_Name), 'left', 'top'])
                analysis_set.append(["Origin Country: " + str(sales_t.est_Recipient_Country), 'left', 'top'])
                analysis_set.append(["Customer Type: " + str(sales_t.est_Customer_Type), 'left', 'top'])
                analysis_set.append(["Opportunity Type: " + str(sales_t.est_Opportunity_Type), 'left', 'top'])
                analysis_set.append(["Opportunity Owner: " + str(sales_t.est_Opportunity_Owner), 'left', 'top'])
                analysis_set.append([str(sales_t.est_Stand_Name_Length_Width), 'left', 'top'])
                analysis_set.append(["Stand Name: " + str(sales_t.est_Stand_Name_Cleaned), 'left', 'top'])
                analysis_set.append(["Modified Date: " + str(sales_t.est_Last_Modified_Date), 'left', 'top'])
                analysis_set.append(["Total Net Amount: " + str(sales_t.est_Total_Net_Amount), 'left', 'top'])
                analysis_set.append(["Order Created Date: " + str(sales_t.est_Order_Created_Date), 'left', 'top'])
                analysis_set.append(["Packages Sold: " + str(sales_t.est_Packages_Sold), 'left', 'top'])
                analysis_set.append(["Products Sold", 'left', 'top'])
                p_name = sales_t.est_Product_Name.split(", ")
                for q in p_name:
                        analysis_set.append(["   " + str(q), 'left', 'top'])
                analysis_set.append(["----", 'left', 'top'])
                analysis_set.append(["Stand Dimenstions: " + str(sales_t.est_Stand_Name_Dim_Cleaned), 'left', 'top'])
                analysis_set.append(["Stand Area: " + str(sales_t.est_Stand_Area), 'left', 'top'])
                analysis_set.append(["Stand Corners: " + str(sales_t.est_Number_of_Corners), 'left', 'top'])
                analysis_set.append(["Stand Zone: " + str(sales_t.est_Stand_Zone), 'left', 'top'])
                analysis_set.append(["Stand Sector: " + str(sales_t.est_Floor_Plan_Sector), 'left', 'top'])
                analysis_set.append(["Stand Sharer Entitlements: " + str(sales_t.est_Sharer_Entitlements), 'left', 'top'])
                analysis_set.append(["Stand Sharer Companies: " + str(sales_t.est_Sharer_Companies), 'left', 'top'])
                analysis_set.append(["----", 'left', 'top'])
                analysis_set.append(["Products Sold", 'left', 'top'])
                p_name = sales_t.est_Product_Name.split(", ")
                for q in p_name:
                        analysis_set.append(["   " + str(q), 'left', 'top'])

        if (1==1):  #Stand Attributes section
                stand_attributes_recs = stand_attributes_get_all_data(st_info)
                analysis_set.append([" ", 'left', 'top'])
                analysis_set.append(["STAND ATTRIBUTES", 'left', 'top'])
                for q in stand_attributes_recs:
                        analysis_set.append([str(q[1]+": "+str(q[2])), 'left', 'top'])
#                analysis_set.append(["Stand Status: "+ str(stand_attributes_get_value(st_info, None, 'Stand Status')), 'left', 'top'])
#                analysis_set.append(["Stand Price: "+str(stand_attributes_get_value(st_info, None, 'Stand Price')), 'left', 'top'])


        if (1==1):  #Overall Pricing
                analysis_set.append([" ", 'left', 'top'])
                analysis_set.append(["ACTUAL PRICING BY TYPE", 'left', 'top'])
                estg = event_sales_transactions_grouped.objects.filter(estg_Stand_Zone=sales_t.est_Stand_Zone, estg_Floor_Plan_Sector = sales_t.est_Floor_Plan_Sector,
                                estg_Stand_Area = sales_t.est_Stand_Area, estg_Number_of_Corners= sales_t.est_Number_of_Corners)
                if(len(estg) > 0):
                        for eee in estg:
                                analysis_set.append(["Stand Zone: " + str(eee.estg_Stand_Zone), 'left', 'top'])
                                analysis_set.append(["Floor Plan Sector: " + str(eee.estg_Floor_Plan_Sector), 'left', 'top'])
                                analysis_set.append(["Stand Area: " + str(eee.estg_Stand_Area), 'left', 'top'])
                                analysis_set.append(["Number of Corners: " + str(eee.estg_Number_of_Corners), 'left', 'top'])
                                analysis_set.append(["Median Price per sq: " + str(eee.estg_median), 'left', 'top'])
                                analysis_set.append(["Avg Price per sq: " + str(eee.estg_avg), 'left', 'top'])
                                analysis_set.append(["Min Price per sq: " + str(eee.estg_min), 'left', 'top'])  
                                analysis_set.append(["Max Price per sq: " + str(eee.estg_max), 'left', 'top'])                                
                                analysis_set.append(["Total Sold at Event: " + str(eee.estg_count), 'left', 'top'])                                

        if (1==1):  #Analysis Section
                mc = False
                stand_analysis_recs = stand_get_all_analysis_records(st_info, run_id)
                if(len(stand_analysis_recs) == 0):
                        stand_analysis_price_apply_monte_carlo(sales_t, st_info, run_id)
                        stand_analysis_recs = stand_get_all_analysis_records(st_info, run_id)
                        mc = True

                if(len(stand_analysis_recs) > 0):
                        analysis_set.append([" ", 'left', 'top'])

                        if(mc):
                                analysis_set.append(["MONTE CARLO STAND ANALYSIS", 'left', 'top'])
                        else:
                                analysis_set.append(["STAND ANALYSIS", 'left', 'top'])
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

