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

        create_stand(eve, 'Stand 1', '1', 20, 120, 10, -10)
        create_stand(eve, 'Stand 2', '2', 20, 110, 10, -10)
        create_stand(eve, 'Stand 3', '3', 20, 100, 10, -10)
        create_stand(eve, 'Stand 4', '4', 20, 90, 10, -10)
        create_stand(eve, 'Stand 5', '5', 30, 120, 10, -10)
        create_stand(eve, 'Stand 6', '6', 30, 110, 10, -10)
        create_stand(eve, 'Stand 7', '7', 30, 100, 10, -20)

        create_stand(eve, 'Stand 1', '1', 50, 120, 10, -10)
        create_stand(eve, 'Stand 2', '2', 50, 110, 10, -10)
        create_stand(eve, 'Stand 3', '3', 50, 100, 10, -10)
        create_stand(eve, 'Stand 4', '4', 50, 90, 10, -10)
        create_stand(eve, 'Stand 5', '5', 60, 120, 10, -10)
        create_stand(eve, 'Stand 6', '6', 60, 110, 10, -10)
        create_stand(eve, 'Stand 7', '7', 60, 100, 10, -20)

        create_stand(eve, 'Stand 3', '3', 80, 120, 10, -30)
        create_stand(eve, 'Stand 4', '4', 80, 90, 10, -10)
        create_stand(eve, 'Stand 5', '5', 90, 120, 10, -20)
        create_stand(eve, 'Stand 6', '6', 90, 100, 10, -20)

        create_stand(eve, 'Stand 3', '3', 110, 120, 10, -20)
        create_stand(eve, 'Stand 4', '4', 110, 100, 10, -20)
        create_stand(eve, 'Stand 5', '5', 120, 120, 10, -20)
        create_stand(eve, 'Stand 6', '6', 120, 100, 10, -20)

        create_stand(eve, 'Stand 3', '3', 140, 120, 10, -20)
        create_stand(eve, 'Stand 4', '4', 140, 100, 10, -20)
        create_stand(eve, 'Stand 5', '5', 150, 120, 10, -20)
        create_stand(eve, 'Stand 6', '6', 150, 100, 10, -20)

        create_stand(eve, 'Stand 1', '1', 170, 120, 10, -10)
        create_stand(eve, 'Stand 2', '2', 170, 110, 10, -10)
        create_stand(eve, 'Stand 3', '3', 170, 100, 10, -20)
        create_stand(eve, 'Stand 5', '5', 180, 120, 10, -10)
        create_stand(eve, 'Stand 6', '6', 180, 110, 10, -10)
        create_stand(eve, 'Stand 7', '7', 180, 100, 10, -20)

        create_stand(eve, 'Stand 1', '1', 200, 120, 10, -20)
        create_stand(eve, 'Stand 3', '3', 200, 100, 10, -20)
        create_stand(eve, 'Stand 5', '5', 210, 120, 10, -10)
        create_stand(eve, 'Stand 6', '6', 210, 110, 10, -10)
        create_stand(eve, 'Stand 7', '7', 210, 100, 10, -20)

        create_stand(eve, 'Stand 1', '1', 230, 120, 40, -40)
        create_stand(eve, 'Stand 1', '1', 280, 120, 30, -40)
        create_stand(eve, 'Stand 1', '1', 320, 120, 80, -40)
        create_stand(eve, 'Stand 1', '1', 410, 120, 100, -50)
        create_stand(eve, 'Stand 1', '1', 520, 120, 40, -50)
        create_stand(eve, 'Stand 1', '1', 570, 120, 30, -50)
        create_stand(eve, 'Stand 1', '1', 610, 120, 30, -50)
        create_stand(eve, 'Stand 1', '1', 650, 120, 30, -40)
        create_stand(eve, 'Stand 1', '1', 690, 120, 30, -30)

        create_stand(eve, 'Stand 1', '1', 730, 120, 20, -10)
        create_stand(eve, 'Stand 1', '1', 760, 120, 20, -30)
        create_stand(eve, 'Stand 1', '1', 790, 120, 20, -30)
        create_stand(eve, 'Stand 1', '1', 820, 120, 20, -30)

        create_stand(eve, 'Stand 1', '1', 850, 120, 10, -20)
        create_stand(eve, 'Stand 2', '2', 850, 100, 10, -20)
        create_stand(eve, 'Stand 6', '6', 860, 120, 10, -20)
        create_stand(eve, 'Stand 7', '7', 860, 100, 10, -20)

        create_stand(eve, 'Stand 1', '1', 880, 120, 10, -20)
        create_stand(eve, 'Stand 2', '2', 880, 100, 10, -20)
        create_stand(eve, 'Stand 6', '6', 890, 120, 10, -20)
        create_stand(eve, 'Stand 7', '7', 890, 100, 10, -20)

        create_stand(eve, 'Stand 1', '1', 910, 120, 10, -10)
        create_stand(eve, 'Stand 2', '2', 910, 110, 10, -10)
        create_stand(eve, 'Stand 3', '3', 910, 100, 10, -20)
        create_stand(eve, 'Stand 5', '5', 920, 120, 10, -10)
        create_stand(eve, 'Stand 6', '6', 920, 110, 10, -10)
        create_stand(eve, 'Stand 7', '7', 920, 100, 10, -10)
        create_stand(eve, 'Stand 7', '7', 920, 90, 10, -10)

        create_stand(eve, 'Stand 5', '5', 940, 120, 10, -10)
        create_stand(eve, 'Stand 6', '6', 940, 110, 10, -10)
        create_stand(eve, 'Stand 7', '7', 940, 100, 10, -10)
        create_stand(eve, 'Stand 7', '7', 940, 90, 10, -10)
        create_stand(eve, 'Stand 5', '5', 950, 120, 10, -10)


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
