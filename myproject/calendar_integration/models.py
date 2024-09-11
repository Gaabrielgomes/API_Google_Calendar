from django.db import models

class Event(models.Model):
    summary = models.CharField(max_length=255, default='')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f'Summary: {self.summary} | Start time: {self.start_time} | End time: {self.end_time}'
 