from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Availability(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('not booked', 'Not Booked'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interviews_availability')
    available_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='not booked')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Availability for {self.user} on {self.available_date} from {self.start_time} to {self.end_time}"

class Interview(models.Model):
    STATUS_CHOICES = [
        ('matched', 'Matched'),
        ('current', 'Current'),
        ('completed', 'Completed'),
    ]

    interviewer = models.ForeignKey(User, related_name='interviews_interviewer', on_delete=models.CASCADE)
    interviewee = models.ForeignKey(User, related_name='interviews_interviewee', on_delete=models.CASCADE)
    interviewer_availability = models.ForeignKey(Availability, related_name='interviews_interviewer_availability', on_delete=models.CASCADE)
    interviewee_availability = models.ForeignKey(Availability, related_name='interviews_interviewee_availability', on_delete=models.CASCADE)
    scheduled_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='matched')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.end_time <= self.start_time:
            raise ValidationError('End time must be after start time.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Interview on {self.scheduled_date} between {self.interviewer} and {self.interviewee}"
