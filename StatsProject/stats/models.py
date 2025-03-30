from django.db import models

class Computer(models.Model):
    computer_id = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    last_seen = models.DateTimeField(auto_now=True)  # Auto-updates on save

class AgentReport(models.Model):  # NEW: Stores each 5-minute agent report
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    apps = models.JSONField()

class SystemMetrics(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    cpu_percent = models.FloatField()
    ram_total = models.BigIntegerField()  # In bytes
    ram_used = models.BigIntegerField()
    ram_percent = models.FloatField()
    timestamp = models.DateTimeField()  # No auto_now_add!

class AppUsage(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    app_name = models.CharField(max_length=255)
    duration = models.IntegerField()  # In seconds
    cpu_usage = models.FloatField()
    ram_usage = models.FloatField()
    timestamp = models.DateTimeField()  # No auto_now_add!