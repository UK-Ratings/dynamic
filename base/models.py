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

class stands(models.Model):
    s_id = models.IntegerField(null=True, blank=True)
    s_rx_event = models.ForeignKey(rx_event, blank=True, null=True, on_delete=models.CASCADE)
    s_name = models.CharField("stand name", max_length=300, blank=True, null=True, )
    s_number = models.CharField("stand number", max_length=300, blank=True, null=True, )
    #Available, Sold, New Sell, Reserved, New Stand
    s_stand_status = models.CharField("stand status", max_length=50, blank=True, null=True, )
    #Base, Price Increase, Price Decrease 
    s_stand_price = models.CharField("stand price", max_length=50, blank=True, null=True, )
    s_stand_price_per_sq_ft = models.DecimalField("stand price per sq ft", max_digits=10, decimal_places=2, blank=True, null=True)
    s_stand_price_gradient = models.IntegerField("stand price gradient", blank=True, null=True)
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




