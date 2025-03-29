from django.db import models

# Create your models here.
class log_page_data(models.Model):
    page_current_datetime = models.DateTimeField("Current Date Time", blank=True, null=True)
    page_python_app = models.CharField(max_length=100, null=True, blank=True)
    page_function_name = models.CharField(max_length=500, null=True, blank=True)
    page_user = models.CharField(max_length=100, null=True, blank=True)
    page_user_ip = models.CharField(max_length=100, null=True, blank=True)
    page_user_agent = models.CharField(max_length=500, null=True, blank=True)
    page_user_referer = models.CharField(max_length=500, null=True, blank=True)
    page_user_language = models.CharField(max_length=100, null=True, blank=True)
    page_user_device = models.CharField(max_length=100, null=True, blank=True)
    page_user_os = models.CharField(max_length=100, null=True, blank=True)
    page_user_browser = models.CharField(max_length=100, null=True, blank=True)
    

class log_progress_data(models.Model):
    current_datetime = models.DateTimeField("Current Date Time", blank=True, null=True)
    python_app = models.CharField(max_length=100, null=True, blank=True)
    function_name = models.CharField(max_length=100, null=True, blank=True)
    function_message = models.CharField(max_length=500, null=True, blank=True)
    class Meta:
        indexes = [
            models.Index(fields=['current_datetime'], name='progress_index1'),]

class log_error_data(models.Model):
    current_datetime = models.DateTimeField("Current Date Time", blank=True, null=True)
    python_app = models.CharField(max_length=100, null=True, blank=True)
    function_name = models.CharField(max_length=100, null=True, blank=True)
    error_level = models.CharField(max_length=50, null=True, blank=True)
    error_message = models.CharField(max_length=500, null=True, blank=True)
    class Meta:
        indexes = [
            models.Index(fields=['current_datetime'], name='error_index1'),]

class log_messages(models.Model):
    current_datetime = models.DateTimeField("Current Date Time", blank=True, null=True)
    python_app = models.CharField(max_length=100, null=True, blank=True)
    user_name = models.CharField(max_length=100, null=True, blank=True)
    function_name = models.CharField(max_length=100, null=True, blank=True)
    function_message = models.CharField(max_length=200, null=True, blank=True)
    class Meta:
        indexes = [
            models.Index(fields=['current_datetime'], name='messages_index1'),]

class rx_event(models.Model):
    re_name = models.CharField("RX Event Name", max_length=300)
    re_floor_length = models.IntegerField("RX Event Floor Length", blank=True, null=True)
    re_floor_height = models.IntegerField("RX Event Floor Height", blank=True, null=True)
    re_event_start_date = models.DateTimeField("RX Event Start Date", blank=True, null=True)
    re_event_end_date = models.DateTimeField("RX Event End Date", blank=True, null=True)








class event_sales_transactions(models.Model):
    est_event = models.ForeignKey(rx_event, blank=True, null=True, on_delete=models.CASCADE)
    est_Company_Name = models.CharField("Company Name", max_length=300, blank=True, null=True, )
    est_Recipient_Country = models.CharField("Recipient Country", max_length=300, blank=True, null=True, )
    est_Customer_Type = models.CharField("Customer Type", max_length=300, blank=True, null=True, )
    est_Opportunity_Type = models.CharField("Opportunity Type", max_length=300, blank=True, null=True, )
    est_Opportunity_Owner = models.CharField("Opportunity Owner", max_length=300, blank=True, null=True, )
    est_Stand_Name_Length_Width = models.CharField("Stand Name Length Width", max_length=300, blank=True, null=True, )
    est_Stand_Name_Cleaned = models.CharField("Stand Name Cleaned", max_length=300, blank=True, null=True, )
    est_Stand_Name_Dim_Cleaned = models.CharField("Stand Name Cleaned", max_length=300, blank=True, null=True, )
    est_Stand_Area = models.CharField("Stand Area", max_length=300, blank=True, null=True, )
    est_Number_of_Corners = models.CharField("Number of Corners", max_length=300, blank=True, null=True, )
    est_Stand_Zone = models.CharField("Stand Zone", max_length=300, blank=True, null=True, )
    est_Floor_Plan_Sector = models.CharField("Floor Plan Sector", max_length=300, blank=True, null=True, )
    est_Sharer_Entitlements = models.CharField("Sharer Entitlements", max_length=300, blank=True, null=True, )
    est_Sharer_Companies = models.CharField("Sharer Companies", max_length=300, blank=True, null=True, )
    est_Last_Modified_Date = models.DateTimeField("Last Modified Date", blank=True, null=True)
    est_Total_Net_Amount = models.CharField("Total Net Amount", max_length=300, blank=True, null=True, )
    est_Order_Created_Date = models.DateTimeField("Order Created Date", blank=True, null=True)
    est_Packages_Sold = models.CharField("Packages Sold", max_length=300, blank=True, null=True, )
    est_Product_Name = models.CharField("Product Name", max_length=300, blank=True, null=True, )

class stands(models.Model):
    s_id = models.IntegerField(null=True, blank=True)
    s_rx_event = models.ForeignKey(rx_event, blank=True, null=True, on_delete=models.CASCADE)
    s_name = models.CharField("stand name", max_length=300, blank=True, null=True, )
    s_number = models.CharField("stand number", max_length=300, blank=True, null=True, )
    s_stand_fill_color = models.CharField("s_stand_fill_color", max_length=50, blank=True, null=True, )
    s_stand_outline_color = models.CharField("s_stand_outline_color", max_length=50, blank=True, null=True, )
    s_text_color = models.CharField("stand text color", max_length=50, blank=True, null=True, )
    class Meta:
        indexes = [
            models.Index(fields=['s_rx_event','s_number'], name='stand_index1'),
            models.Index(fields=['s_rx_event','s_name'], name='stand_index2'),
            ]



class stand_location(models.Model):
    sl_stand = models.ForeignKey(stands, blank=True, null=True, on_delete=models.CASCADE)
    sl_x = models.IntegerField("stand x")
    sl_y = models.IntegerField("stand y")
    sl_x_length = models.IntegerField("stand x length")
    sl_y_length = models.IntegerField("stand y length")




#    models.IntegerField(unique=True)    
#    tourney_assn = models.ForeignKey(associations, on_delete=models.PROTECT)
#    tourney_name = models.CharField("Tournament Name", max_length=300)
#    tourney_inbound = models.CharField("Inbound Tournament", max_length=100, blank=True, null=True)
#    tourney_status = models.ForeignKey(tournament_status, blank=True, null=True, on_delete=models.CASCADE)
#    tourney_start_date = models.DateTimeField("Tournament Start Time", blank=True, null=True)
#    tourney_end_date = models.DateTimeField("Tournament End Time", blank=True, null=True)
#    tourney_entry_close_date = models.DateTimeField("Tournament Entry Close Date", blank=True, null=True)
#    tourney_url = models.CharField(max_length = 100, blank=True, null=True)
#    tourney_license = models.CharField("Tournament License", max_length=100, blank=True, null=True)
#    tourney_results = models.CharField("Tournament Results", max_length=500, blank=True, null=True)
#    tourney_override = models.BooleanField("Tournament Override", default=False)
#    tourney_entry_url = models.CharField(max_length = 100, blank=True, null=True)
#    tourney_entry_list_url = models.CharField(max_length = 100, blank=True, null=True)
#    tourney_upcoming = models.BooleanField("Tournament Upcoming", default=False)
#    tourney_potential_rating = models.CharField(max_length = 300, blank=True, null=True)
#    tourney_final_rating = models.CharField(max_length = 300, blank=True, null=True)
#    date_added = models.DateTimeField(blank=True, null=True)
#    date_updated = models.DateTimeField(blank=True, null=True)
#    class Meta:
#        indexes = [
#            models.Index(fields=['tourney_assn', 'tourney_name', 'tourney_start_date'], name='tourney_index2'),
#            models.Index(fields=['tourney_number', 'tourney_name', 'tourney_assn'], name='tourney_index1'),
#            models.Index(fields=['tourney_start_date'], name='tourney_index5'),
#            models.Index(fields=['tourney_end_date'], name='tourney_index6'),
#            models.Index(fields=['id'], name='tourney_index3'),
#        ]
#    def __str__(self):
#        return f"{self.tourney_name}  ({self.tourney_start_date.strftime('%B %Y')})"
    
#class tournament_extra_fields(models.Model):
#    tef_tourney = models.ForeignKey(tournaments, blank=True, null=True, on_delete=models.CASCADE)
#    tef_field_sequence = models.IntegerField(null=True, blank=True)




