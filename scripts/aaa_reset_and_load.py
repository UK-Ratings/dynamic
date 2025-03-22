#!/usr/bin/env python3

from django.utils import timezone
from django.contrib import messages
import os
from dotenv import load_dotenv
from django.conf import settings
from django.db.models import Max

from base.models import *
from scripts.aaa_helper_functions import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")

def get_next_stand_id():
    max_id = stands.objects.aggregate(max_id=Max('s_id'))['max_id']
    return (max_id or 0) + 1

def create_stand(eve, stand_name, stand_number, x, y, x_length, y_length):

        st, created = stands.objects.update_or_create(s_id=get_next_stand_id(), defaults={
                's_rx_event': eve[0], 's_name': stand_name, 's_number': stand_number,
                's_stand_fill_color':'#99B3CF', 's_stand_outline_color':'black', 's_text_color':'#000000'})
        sl = stand_location.objects.update_or_create(sl_stand=st, defaults={
                                'sl_x':x, 'sl_y':y, 'sl_x_length':x_length, 'sl_y_length':y_length})


def populate_for_test():
#        f.write("populate_for_test: " + str(timezone.now()) + "\n")
        record_log_data("aaa_load_test_data.py", "populate_for_test", "populate_for_test")

        eve = rx_event.objects.update_or_create(re_name='ISC West 2025')

        if(1==1):  #row 7
                row_amt = 300

                create_stand(eve, 'Stand 1', '1', 20, (row_amt - 0), 10, -10)
                create_stand(eve, 'Stand 2', '2', 20, (row_amt - 10), 10, -10)
                create_stand(eve, 'Stand 3', '3', 20, (row_amt - 20), 10, -10)
                create_stand(eve, 'Stand 4', '4', 20, (row_amt - 30), 10, -10)
                create_stand(eve, 'Stand 5', '5', 30, (row_amt - 0), 10, -10)
                create_stand(eve, 'Stand 6', '6', 30, (row_amt - 10), 10, -10)
                create_stand(eve, 'Stand 7', '7', 30, (row_amt - 20), 10, -20)

                create_stand(eve, 'Stand 1', '1', 50, (row_amt - 0), 10, -10)
                create_stand(eve, 'Stand 2', '2', 50, (row_amt - 10), 10, -10)
                create_stand(eve, 'Stand 3', '3', 50, (row_amt - 20), 10, -10)
                create_stand(eve, 'Stand 4', '4', 50, (row_amt - 30), 10, -10)
                create_stand(eve, 'Stand 5', '5', 60, (row_amt - 0), 10, -10)
                create_stand(eve, 'Stand 6', '6', 60, (row_amt - 10), 10, -10)
                create_stand(eve, 'Stand 7', '7', 60, (row_amt - 20), 10, -20)

                create_stand(eve, 'Stand 3', '3', 80, (row_amt - 0), 10, -30)
                create_stand(eve, 'Stand 4', '4', 80, (row_amt - 30), 10, -10)
                create_stand(eve, 'Stand 5', '5', 90, (row_amt - 0), 10, -20)
                create_stand(eve, 'Stand 6', '6', 90, (row_amt - 20), 10, -20)

                create_stand(eve, 'Stand 3', '3', 110, (row_amt - 0), 10, -20)
                create_stand(eve, 'Stand 4', '4', 110, (row_amt - 20), 10, -20)
                create_stand(eve, 'Stand 5', '5', 120, (row_amt - 0), 10, -20)
                create_stand(eve, 'Stand 6', '6', 120, (row_amt - 20), 10, -20)

                create_stand(eve, 'Stand 3', '3', 140, (row_amt - 0), 10, -20)
                create_stand(eve, 'Stand 4', '4', 140, (row_amt - 20), 10, -20)
                create_stand(eve, 'Stand 5', '5', 150, (row_amt - 0), 10, -20)
                create_stand(eve, 'Stand 6', '6', 150, (row_amt - 20), 10, -20)

                create_stand(eve, 'Stand 1', '1', 170, (row_amt - 0), 10, -10)
                create_stand(eve, 'Stand 2', '2', 170, (row_amt - 10), 10, -10)
                create_stand(eve, 'Stand 3', '3', 170, (row_amt - 20), 10, -20)
                create_stand(eve, 'Stand 5', '5', 180, (row_amt - 0), 10, -10)
                create_stand(eve, 'Stand 6', '6', 180, (row_amt - 10), 10, -10)
                create_stand(eve, 'Stand 7', '7', 180, (row_amt - 20), 10, -20)

                create_stand(eve, 'Stand 1', '1', 200, (row_amt - 0), 10, -20)
                create_stand(eve, 'Stand 3', '3', 200, (row_amt - 20), 10, -20)
                create_stand(eve, 'Stand 5', '5', 210, (row_amt - 0), 10, -10)
                create_stand(eve, 'Stand 6', '6', 210, (row_amt - 10), 10, -10)
                create_stand(eve, 'Stand 7', '7', 210, (row_amt - 20), 10, -20)

                create_stand(eve, 'Stand 1', '1', 230, (row_amt - 0), 40, -40)
                create_stand(eve, 'Stand 1', '1', 280, (row_amt - 0), 30, -40)
                create_stand(eve, 'Stand 1', '1', 320, (row_amt - 0), 80, -40)
                create_stand(eve, 'Stand 1', '1', 410, (row_amt - 0), 100, -50)
                create_stand(eve, 'Stand 1', '1', 520, (row_amt - 0), 60, -50)
                create_stand(eve, 'Stand 1', '1', 590, (row_amt - 0), 40, -50)
                create_stand(eve, 'Stand 1', '1', 640, (row_amt - 0), 30, -50)
                create_stand(eve, 'Stand 1', '1', 680, (row_amt - 0), 30, -50)
                create_stand(eve, 'Stand 1', '1', 720, (row_amt - 0), 30, -40)
                create_stand(eve, 'Stand 1', '1', 760, (row_amt - 0), 30, -30)

                create_stand(eve, 'Stand 1', '1', 800, (row_amt - 0), 20, -10)
                create_stand(eve, 'Stand 1', '1', 830, (row_amt - 0), 20, -30)
                create_stand(eve, 'Stand 1', '1', 860, (row_amt - 0), 20, -30)
                create_stand(eve, 'Stand 1', '1', 890, (row_amt - 0), 20, -30)

                create_stand(eve, 'Stand 1', '1', 920, (row_amt - 0), 10, -20)
                create_stand(eve, 'Stand 2', '2', 920, (row_amt - 20), 10, -20)
                create_stand(eve, 'Stand 6', '6', 930, (row_amt - 0), 10, -20)
                create_stand(eve, 'Stand 7', '7', 930, (row_amt - 20), 10, -20)

                create_stand(eve, 'Stand 1', '1', 950, (row_amt - 0), 10, -20)
                create_stand(eve, 'Stand 2', '2', 950, (row_amt - 20), 10, -20)
                create_stand(eve, 'Stand 6', '6', 960, (row_amt - 0), 10, -20)
                create_stand(eve, 'Stand 7', '7', 960, (row_amt - 20), 10, -20)

                create_stand(eve, 'Stand 1', '1', 980, (row_amt - 0), 10, -10)
                create_stand(eve, 'Stand 2', '2', 980, (row_amt - 10), 10, -10)
                create_stand(eve, 'Stand 3', '3', 980, (row_amt - 20), 10, -20)
                create_stand(eve, 'Stand 5', '5', 990, (row_amt - 0), 10, -10)
                create_stand(eve, 'Stand 6', '6', 990, (row_amt - 10), 10, -10)
                create_stand(eve, 'Stand 7', '7', 990, (row_amt - 20), 10, -10)
                create_stand(eve, 'Stand 7', '7', 990, (row_amt - 30), 10, -10)

                create_stand(eve, 'Stand 5', '5', 1010, (row_amt - 0), 10, -10)
                create_stand(eve, 'Stand 6', '6', 1010, (row_amt - 10), 10, -10)
                create_stand(eve, 'Stand 7', '7', 1010, (row_amt - 20), 10, -10)
                create_stand(eve, 'Stand 7', '7', 1010, (row_amt - 30), 10, -10)
                create_stand(eve, 'Stand 5', '5', 1020, (row_amt - 0), 10, -10)

        if(1==1):  #row 7
                create_stand(eve, 'Stand 1', '1', 590, 240, 40, -40)
                create_stand(eve, 'Stand 1', '1', 590, 190, 40, -30)
                create_stand(eve, 'Stand 1', '1', 590, 160, 40, -30)
                create_stand(eve, 'Stand 1', '1', 590, 120, 40, -40)
                create_stand(eve, 'Stand 1', '1', 590, 70, 40, -40)
                create_stand(eve, 'Stand 1', '1', 590, 20, 40, -10)

        if(1==1):  #row 7
                create_stand(eve, 'Stand 1', '1', 640, 310, 30, 30)
                create_stand(eve, 'Stand 1', '1', 640, 350, 30, 30)
                create_stand(eve, 'Stand 1', '1', 640, 390, 30, 40)
                create_stand(eve, 'Stand 1', '1', 640, 440, 40, 20)
                create_stand(eve, 'Stand 1', '1', 640, 460, 40, 20)
                create_stand(eve, 'Stand 1', '1', 640, 490, 30, 30)

                create_stand(eve, 'Stand 1', '1', 655, 540, 20, 30)
                create_stand(eve, 'Stand 1', '1', 655, 580, 20, 30)
                create_stand(eve, 'Stand 1', '1', 655, 620, 20, 20)
                create_stand(eve, 'Stand 1', '1', 655, 650, 20, 20)
                create_stand(eve, 'Stand 1', '1', 655, 680, 20, 20)


#        for x in rx_event.objects.all():
#                print(x.re_name)
#                for y in stands.objects.filter(s_rx_event=x):
#                        print(y.s_name)
#                        for z in stand_location.objects.filter(sl_stand=y):
#                                print(z.sl_x, z.sl_y, z.sl_x_length, z.sl_y_length)



def reset_test_data():
#        f.write("reset tables: " + str(timezone.now()) + "\n")
        rx_event.objects.all().delete()

def run(*args):

        db_host_name = str(settings.DATABASES['default']['HOST'])
        db_name = str(settings.DATABASES['default']['NAME'])
        path_logs = os.path.join(settings.BASE_DIR, "logs/")
        path_input = os.path.join(settings.BASE_DIR, "scripts/")

        logs_filename = path_logs+"_"+os.path.splitext(os.path.basename(__file__))[0] + ".txt"

#        f = open(logs_filename, "w", encoding='utf-8')
#        f.write("Starting " + logs_filename + str(timezone.now()) + "\n")
#        f.write("database_host_name: " + db_host_name + "\n")
#        f.write("database_name: " + db_name + "\n")

        record_log_data("aaa_reset_and_load.py", "reset data", "reset data")
        reset_test_data()
        record_log_data("aaa_reset_and_load.py", "load data", "load data")
        populate_for_test()

#        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
#        f.close()
 

#python manage.py runscript aaa_reset_and_load
