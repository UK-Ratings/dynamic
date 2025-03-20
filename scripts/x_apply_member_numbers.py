#!/usr/bin/env python3

from assn_mgr.models import *
from users.models import User

from integrations.models import *
from tourneys.models import *

from scripts.x_helper_functions import *
from scripts.x_helper_assn_specific import *

from django.db.models import Count
from django.utils import timezone
from django.db.models import F
import os
import inspect
import re

from dotenv import load_dotenv
from django.conf import settings

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")

def Apply_Member_Numbers(f, asn, assn_recs, combined_set, DEBUG_WRITE):
#        record_log_data("x_apply_member_numbers.py", "Apply_Member_Numbers", "started: " + str(timezone.now()))

        cnt = 0
        if(DEBUG_WRITE):
                f.write("Apply_Member_Numbers_First. Lenght: " + str(len(combined_set)) + " " + str(datetime.now()) + "\n")
        ef = []
        for x in combined_set:
                if(1==1):
#                if(x[1] is not None and 'MCKENZIE' in x[1]):
                        amn1 = get_assn_member_record(f, asn, assn_recs, x[0], x[1], "", "", False)
                        if(amn1 is not None):
                                effr = event_final_results.objects.filter(efr_given_member_identifier=x[0], efr_given_name=x[1])
                                for y in effr:
                                        y.efr_assn_member_number = amn1.assn_member_number
                                        y.save()
                                erpa = event_round_pool_assignments.objects.filter(erpa_member_num=x[0], erpa_name=x[1])
                                for y in erpa:
                                        y.erpa_assn_member_number = amn1.assn_member_number
                                        y.save()
                                erpem = event_round_pool_elimination_matches.objects.filter(erpem_top_member_num=x[0], erpem_top_name=x[1])
                                for y in erpem:
                                        y.erpem_top_assn_member_number = amn1.assn_member_number
                                        y.save()
                                erpem = event_round_pool_elimination_matches.objects.filter(erpem_bottom_member_num=x[0], erpem_bottom_name=x[1])
                                for y in erpem:
                                        y.erpem_bottom_assn_member_number = amn1.assn_member_number
                                        y.save()
                                erpes = event_round_pool_elimination_scores.objects.filter(erpes_left_member_num=x[0], erpes_left_name=x[1])
                                for y in erpes:
                                        y.erpes_left_assn_member_number = amn1.assn_member_number
                                        y.save()
                                erpes = event_round_pool_elimination_scores.objects.filter(erpes_right_member_num=x[0], erpes_right_name=x[1])
                                for y in erpes:
                                        y.erpes_right_assn_member_number = amn1.assn_member_number
                                        y.save()
                                erpes = event_round_pool_elimination_scores.objects.filter(erpes_winner_member_num=x[0], erpes_winner_name=x[1])
                                for y in erpes:
                                        y.erpes_winner_assn_member_number = amn1.assn_member_number
                                        y.save()
                                erpr = event_round_pool_results.objects.filter(erpr_member_num=x[0], erpr_name=x[1])
                                for y in erpr:
                                        y.erpr_assn_member_number = amn1.assn_member_number
                                        y.save()
                                erps = event_round_pool_scores.objects.filter(erps_left_member_num=x[0], erps_left_name=x[1])
                                for y in erps:
                                        y.erps_left_assn_member_number = amn1.assn_member_number
                                        y.save()
                                erps = event_round_pool_scores.objects.filter(erps_right_member_num=x[0], erps_right_name=x[1])
                                for y in erps:
                                        y.erps_right_assn_member_number = amn1.assn_member_number
                                        y.save()
                                erps = event_round_pool_scores.objects.filter(erps_winner_member_num=x[0], erps_winner_name=x[1])
                                for y in erps:
                                        y.erps_winner_assn_member_number = amn1.assn_member_number
                                        y.save()
                                ers = event_round_seeding.objects.filter(ers_member_num=x[0], ers_name=x[1])
                                for y in ers:
                                        y.ers_assn_member_number = amn1.assn_member_number
                                        y.save()
                        cnt = cnt + 1
                        if(cnt % 500 == 0):
                                if(DEBUG_WRITE):
                                        print("completed", cnt, timezone.now())
                                        f.write("   Completed: " + str(cnt) + " " + str(datetime.now()) + "\n")
        if(DEBUG_WRITE):
                f.write("Completed: Apply_Member_Numbers: " + str(datetime.now()) + "\n")
#        record_log_data("x_apply_member_numbers.py", "Apply_Member_Numbers", "completed: " + str(timezone.now()))

def Build_Set(f, force_overwrite, DEBUG_WRITE):
#        record_log_data("x_apply_member_numbers.py", "Build_Set", "started: " + str(timezone.now()))
        f.write("\n\n\n Build_Set: Override: " + str(force_overwrite) + " " + str(datetime.now()) + "\n")
        efrr = []
        erpaa = []
        erpemt = []
        erpemb = []
        erpesl = []
        erpesr = []
        erpesw = []
        erprr = []
        erpsl = []
        erpsr = []
        erpsw = []
        erss = []
        if(force_overwrite):
#                efrr = event_final_results.objects.filter(efr_given_name__icontains='MCKENZIE BURKE').values(given_id=F('efr_given_member_identifier'), given_name=F('efr_given_name')).annotate(count=Count('id'))
                efrr = event_final_results.objects.values(given_id=F('efr_given_member_identifier'), given_name=F('efr_given_name')).annotate(count=Count('id'))
                erpaa = event_round_pool_assignments.objects.values(given_id=F('erpa_member_num'), given_name=F('erpa_name')).annotate(count=Count('id'))
                erpemt = event_round_pool_elimination_matches.objects.values(given_id=F('erpem_top_member_num'), given_name=F('erpem_top_name')).annotate(count=Count('id'))
                erpemb = event_round_pool_elimination_matches.objects.values(given_id=F('erpem_bottom_member_num'), given_name=F('erpem_bottom_name')).annotate(count=Count('id'))
                erpesl = event_round_pool_elimination_scores.objects.values(given_id=F('erpes_left_member_num'), given_name=F('erpes_left_name')).annotate(count=Count('id'))
                erpesr = event_round_pool_elimination_scores.objects.values(given_id=F('erpes_right_member_num'), given_name=F('erpes_right_name')).annotate(count=Count('id'))
                erpesw = event_round_pool_elimination_scores.objects.values(given_id=F('erpes_winner_member_num'), given_name=F('erpes_winner_name')).annotate(count=Count('id'))
                erprr = event_round_pool_results.objects.values(given_id=F('erpr_member_num'), given_name=F('erpr_name')).annotate(count=Count('id'))
                erpsl = event_round_pool_scores.objects.values(given_id=F('erps_left_member_num'), given_name=F('erps_left_name')).annotate(count=Count('id'))
                erpsr = event_round_pool_scores.objects.values(given_id=F('erps_right_member_num'), given_name=F('erps_right_name')).annotate(count=Count('id'))
                erpsw = event_round_pool_scores.objects.values(given_id=F('erps_winner_member_num'), given_name=F('erps_winner_name')).annotate(count=Count('id'))
                erss = event_round_seeding.objects.values(given_id=F('ers_member_num'), given_name=F('ers_name')).annotate(count=Count('id'))
        else:
                efrr = event_final_results.objects.filter(Q(efr_given_member_identifier__isnull=True) | Q(efr_assn_member_number=0)).values(given_id=F('efr_given_member_identifier'), given_name=F('efr_given_name')).annotate(count=Count('id'))
                erpaa = event_round_pool_assignments.objects.filter(erpa_assn_member_number__isnull=True).values(given_id=F('erpa_member_num'), given_name=F('erpa_name')).annotate(count=Count('id'))
                erpemt = event_round_pool_elimination_matches.objects.filter(erpem_top_member_num__isnull=True).values(given_id=F('erpem_top_member_num'), given_name=F('erpem_top_name')).annotate(count=Count('id'))
                erpemb = event_round_pool_elimination_matches.objects.filter(erpem_bottom_member_num__isnull=True).values(given_id=F('erpem_bottom_member_num'), given_name=F('erpem_bottom_name')).annotate(count=Count('id'))
                erpesl = event_round_pool_elimination_scores.objects.filter(erpes_left_member_num__isnull=True).values(given_id=F('erpes_left_member_num'), given_name=F('erpes_left_name')).annotate(count=Count('id'))
                erpesr = event_round_pool_elimination_scores.objects.filter(erpes_right_member_num__isnull=True).values(given_id=F('erpes_right_member_num'), given_name=F('erpes_right_name')).annotate(count=Count('id'))
                erpesw = event_round_pool_elimination_scores.objects.filter(erpes_winner_member_num__isnull=True).values(given_id=F('erpes_winner_member_num'), given_name=F('erpes_winner_name')).annotate(count=Count('id'))
                erprr = event_round_pool_results.objects.filter(erpr_member_num__isnull=True).values(given_id=F('erpr_member_num'), given_name=F('erpr_name')).annotate(count=Count('id'))
                erpsl = event_round_pool_scores.objects.filter(erps_left_member_num__isnull=True).values(given_id=F('erps_left_member_num'), given_name=F('erps_left_name')).annotate(count=Count('id'))
                erpsr = event_round_pool_scores.objects.filter(erps_right_member_num__isnull=True).values(given_id=F('erps_right_member_num'), given_name=F('erps_right_name')).annotate(count=Count('id'))
                erpsw = event_round_pool_scores.objects.filter(erps_winner_member_num__isnull=True).values(given_id=F('erps_winner_member_num'), given_name=F('erps_winner_name')).annotate(count=Count('id'))
                erss = event_round_seeding.objects.filter(ers_member_num__isnull=True).values(given_id=F('ers_member_num'), given_name=F('ers_name')).annotate(count=Count('id'))

        combined_set = list(efrr) + list(erpaa) + list(erpemt) + list(erpemb) + list(erpesl) + list(erpesr) + list(erpesw) + list(erprr) + list(erpsl) + list(erpsr) + list(erpsw) + list(erss)
        combined_set = { (x['given_id'], x['given_name']) for x in combined_set }
        combined_set = sorted(combined_set, key=lambda x: (x[0] or '', x[0] or '0', x[0] or 0, x[1] or ''))
        if(DEBUG_WRITE):
                print('combined_set',len(combined_set))
#        for x in combined_set:
#                if(DEBUG_WRITE):
#                        print(x, x[0], x[1])

        f.write("Completed: Build_Set: " + str(datetime.now()) + "\n")
#        record_log_data("x_apply_member_numbers.py", "Build_Set", "completed: " + str(timezone.now()))
        return(combined_set)

def Determine_Nulls(f):
        f.write("\n\n\n Determine_Nulls " + str(datetime.now()) + "\n")


        erpa = event_round_pool_assignments.objects.filter(erpa_assn_member_number__isnull = True)
        erpem = event_round_pool_elimination_matches.objects.filter(
                (Q(erpem_top_assn_member_number__isnull=True) 
                        | Q(erpem_bottom_assn_member_number__isnull=True)))
        erpes = event_round_pool_elimination_scores.objects.filter(
                (Q(erpes_left_assn_member_number__isnull=True) 
                        | Q(erpes_right_assn_member_number__isnull=True)
                        | Q(erpes_winner_assn_member_number__isnull=True)))
        erpr = event_round_pool_results.objects.filter(erpr_assn_member_number__isnull=True) 
        erps = event_round_pool_scores.objects.filter(
                (Q(erps_left_assn_member_number__isnull=True) 
                        | Q(erps_right_assn_member_number__isnull=True)
                        | Q(erps_winner_assn_member_number__isnull=True)))
        ers = event_round_seeding.objects.filter(ers_assn_member_number__isnull=True) 
        efr = event_final_results.objects.filter(efr_assn_member_number__isnull=True) 

        f.write("\n\n\n\n\n\n All done!  Final count still with nulls... " + str(timezone.now()) + "\n")
        f.write("event_round_pool_assignments length = " + str(erpa.count()) + "\n")
        f.write("event_round_pool_elimination_matches length = " + str(erpem.count()) + "\n")
        f.write("event_round_pool_elimination_scores length = " + str(erpes.count()) + "\n")
        f.write("event_round_pool_results length = " + str(erpr.count()) + "\n")
        f.write("event_round_pool_scores length = " + str(erps.count()) + "\n")
        f.write("event_round_seeding length = " + str(ers.count()) + "\n")
        f.write("event_final_results length = " + str(efr.count()) + "\n")

        f.write("Completed: Determine_Nulls: " + str(datetime.now()) + "\n")

def run(*args):
        if(1==1): #basic setup
                db_host_name = str(settings.DATABASES['default']['HOST'])
                db_name = str(settings.DATABASES['default']['NAME'])
                path_logs = os.path.join(settings.BASE_DIR, "logs/")
                path_input = os.path.join(settings.BASE_DIR, "scripts/")

                logs_filename = path_logs+db_name+"_"+os.path.splitext(os.path.basename(__file__))[0] + ".txt"
                f = open(logs_filename, "w", encoding='utf-8')
                f.write("Starting " + logs_filename + str(timezone.now()) + "\n")
                f.write("database_host_name: " + db_host_name + "\n")
                f.write("database_name: " + db_name + "\n")

                load_dotenv()  #must have to access .env file values

                app_name = os.path.splitext(os.path.basename(__file__))[0]+".py"
                funct_name = inspect.getframeinfo(inspect.currentframe()).function

        DEBUG_WRITE = True
        force_overwrite = False
        asn = get_association(f, "British Fencing", DEBUG_WRITE)
        assn_recs = association_members.objects.filter(assn = asn).values_list('assn_member_full_name', flat=True)

        if 'reset' in args:
                force_overwrite = True

        if(DEBUG_WRITE):
                f.write("DEBUG_WRITE: " + str(DEBUG_WRITE) + "\n")
                f.write("asn:  " + str(asn.assn_name) + "\n")
                f.write("force override: " + str(force_overwrite) + "\n")

        if(DEBUG_WRITE):
                Determine_Nulls(f)

        record_log_data(app_name, "Build_Set", "Starting")
        record_set = Build_Set(f, force_overwrite, DEBUG_WRITE)
        record_log_data(app_name, "Build_Set", "Completed")

        record_log_data(app_name, "Apply_Member_Numbers", "Starting")
        Apply_Member_Numbers(f, asn, assn_recs, record_set, DEBUG_WRITE)
        record_log_data(app_name, "Apply_Member_Numbers", "Completed")

        if(DEBUG_WRITE):
                Determine_Nulls(f)

        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()
#        record_log_data(app_name, funct_name, "Completed")

# python manage.py runscript x_apply_member_numbers
# python manage.py runscript x_apply_member_numbers --script-args reset

