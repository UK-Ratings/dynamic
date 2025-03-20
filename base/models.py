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

