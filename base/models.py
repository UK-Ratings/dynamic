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

class rx_event_group(models.Model):
    reg_name = models.CharField("RX Event Group Name", max_length=300)

class rx_event(models.Model):
    re_event_group = models.ForeignKey(rx_event_group, blank=True, null=True, on_delete=models.CASCADE)
    re_name = models.CharField("RX Event Name", max_length=300)
    re_floor_length = models.IntegerField("RX Event Floor Length", blank=True, null=True)
    re_floor_height = models.IntegerField("RX Event Floor Height", blank=True, null=True)
    re_event_start_date = models.DateTimeField("RX Event Start Date", blank=True, null=True)
    re_event_end_date = models.DateTimeField("RX Event End Date", blank=True, null=True)

class event_stand_count_by_date(models.Model):
    escby_rx_event = models.ForeignKey(rx_event, blank=True, null=True, on_delete=models.CASCADE)
    escby_date = models.DateTimeField("escby date", blank=True, null=True)
    escby_x_length = models.IntegerField("escby x length")
    escby_y_length = models.IntegerField("escby y length")
    escby_stand_status = models.CharField("escby stand status", max_length=50, blank=True, null=True, )
    escby_stand_count = models.IntegerField("escby Stand Count", blank=True, null=True)
    class Meta:
        indexes = [
            models.Index(fields=['escby_rx_event','escby_date', 'escby_stand_status', 'escby_x_length', 'escby_y_length'], name='escby_index1'),
            ]

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

class event_sales_transactions_grouped(models.Model):
    estg_event = models.ForeignKey(rx_event, blank=True, null=True, on_delete=models.CASCADE)
    estg_Stand_Area = models.CharField("Stand Area", max_length=300, blank=True, null=True, )
    estg_Number_of_Corners = models.CharField("Number of Corners", max_length=300, blank=True, null=True, )
    estg_Stand_Zone = models.CharField("Stand Zone", max_length=300, blank=True, null=True, )
    estg_Floor_Plan_Sector = models.CharField("Floor Plan Sector", max_length=300, blank=True, null=True, )
    estg_Packages_Sold = models.CharField("Packages Sold", max_length=300, blank=True, null=True, )
    estg_count = models.IntegerField("Count", blank=True, null=True)
    estg_min = models.FloatField("Min", blank=True, null=True)
    estg_max = models.FloatField("Max", blank=True, null=True)
    estg_avg = models.FloatField("Avg", blank=True, null=True)
    estg_median = models.FloatField("Median", blank=True, null=True)

class stands_attribute_data(models.Model):
    sad_event = models.ForeignKey(rx_event, blank=True, null=True, on_delete=models.CASCADE)
    sad_stand_name = models.CharField("Stand Name", max_length=300, blank=True, null=True, )
    sad_title = models.CharField("Stand Title", max_length=300, blank=True, null=True, )
    sad_value = models.CharField("Stand Value", max_length=300, blank=True, null=True, )
    sad_data_type = models.CharField("Stand Data Type", max_length=300, blank=True, null=True, )
    sad_datetime = models.DateTimeField("Stand Date Time", blank=True, null=True)
    class Meta:
        indexes = [
            models.Index(fields=['sad_event','sad_stand_name','sad_title'], name='stands_attribute_data_index1'),
            ]

#remove s_stand_status and others???  Store in stand_attributes???
class stands(models.Model):
    s_id = models.IntegerField(null=True, blank=True)
    s_rx_event = models.ForeignKey(rx_event, blank=True, null=True, on_delete=models.CASCADE)
    s_name = models.CharField("stand name", max_length=300, blank=True, null=True, )
    s_number = models.CharField("stand number", max_length=300, blank=True, null=True, )
    class Meta:
        indexes = [
            models.Index(fields=['s_rx_event','s_number'], name='stand_index1'),
            models.Index(fields=['s_rx_event','s_name'], name='stand_index2'),
            ]


# will use these for identification and to match to the rules in time
class stand_attributes(models.Model):
    sa_stand = models.ForeignKey(stands, blank=True, null=True, on_delete=models.CASCADE)
    sa_number = models.IntegerField("stand attribute number")
    sa_title = models.CharField("stand attribute title", max_length=300, blank=True, null=True, )    
    sa_value = models.CharField("stand attribute value", max_length=300, blank=True, null=True, )
    sa_type = models.CharField("stand attribute type", max_length=50, blank=True, null=True, )
    sa_datetime = models.DateTimeField("stand attribute datetime", blank=True, null=True)
    class Meta:
        indexes = [
            models.Index(fields=['sa_stand','sa_number'], name='stand_attributes_index1'),
            models.Index(fields=['sa_stand','sa_title'], name='stand_attributes_index2'),
        ]

class stand_analysis(models.Model):
    sa_stand = models.ForeignKey(stands, blank=True, null=True, on_delete=models.CASCADE)
    sa_run_id = models.IntegerField("monte carlo run id", blank=True, null=True)
    sa_analysis_number = models.IntegerField("analysis number")
    sa_analysis_title = models.CharField("analysis title", max_length=300, blank=True, null=True, )
    sa_analysis_value = models.CharField("analysis value", max_length=300, blank=True, null=True, )
    sa_analysis_type = models.CharField("analysis type", max_length=50, blank=True, null=True, )
    sa_analysis_datetime = models.DateTimeField("analysis datetime", blank=True, null=True)
    class Meta:
        indexes = [
            models.Index(fields=['sa_stand', 'sa_run_id','sa_analysis_number'], name='stand_analysis_index1'),
            models.Index(fields=['sa_stand', 'sa_run_id', 'sa_analysis_title'], name='stand_analysis_index2'),
        ]


class pricing_rules(models.Model):
    prb_event = models.ForeignKey(rx_event, blank=True, null=True, on_delete=models.CASCADE)
    prb_run_id = models.IntegerField("monto carlo run id", blank=True, null=True)
    prb_number = models.IntegerField("pricing rule base number")
    prb_title = models.CharField("pricing rule base title", max_length=300, blank=True, null=True, )    
    prb_value = models.CharField("pricing rule base value", max_length=300, blank=True, null=True, )
    prb_type = models.CharField("pricing rule base type", max_length=50, blank=True, null=True, )
    prb_start_datetime = models.DateTimeField("pricing rule base start datetime", blank=True, null=True)
    prb_end_datetime = models.DateTimeField("pricing rule base end datetime", blank=True, null=True)
    class Meta:
        indexes = [
            models.Index(fields=['prb_event', 'prb_run_id','prb_number'], name='prb_index1'),
            models.Index(fields=['prb_event', 'prb_run_id','prb_title'], name='prb_index2'),
        ]

