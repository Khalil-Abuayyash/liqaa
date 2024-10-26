from django.db import models
# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from users.models import User
from datetime import datetime, date

class Availability(models.Model):
    is_booked = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    available_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()

        # Basic validation for start and end times
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")
        
        if self.available_date < date.today():
            raise ValidationError("Availability cannot be set for past dates.")
        
        # This case to insure the user does not add availability in the past time 
        availability_start_datetime = datetime.combine(self.available_date, self.start_time)
        if availability_start_datetime <= datetime.now() and self.available_date == date.today() :
            raise ValidationError("Availability cannot start in the past.")

        # Check if the availability conflicts with existing entries
        overlapping_availability = Availability.objects.filter(
            user=self.user,
            available_date=self.available_date,
        ).exclude(id=self.id)  

        for availability in overlapping_availability:
            # Convert times to datetime for easier comparison
            current_start = datetime.combine(self.available_date, self.start_time)
            current_end = datetime.combine(self.available_date, self.end_time)
            existing_start = datetime.combine(availability.available_date, availability.start_time)
            existing_end = datetime.combine(availability.available_date, availability.end_time)

            # Case: full overlap or containment
            if (current_start >= existing_start and current_end <= existing_end) or \
               (current_start <= existing_start and current_end >= existing_end):
                raise ValidationError("New availability is within or fully contains an existing availability.")
            
            # Case: partial overlaps
            if (current_start < existing_end and current_end > existing_start):
                raise ValidationError("New availability partially overlaps an existing availability.")
            
        def update_overlapping_availability(self):
            if hasattr(self, 'overlapping_availability'):
                self.overlapping_availability.start_time = self.start_time
                self.overlapping_availability.end_time = self.end_time
                self.overlapping_availability.save()

    def __str__(self):
        return f"Availability for {self.user} on {self.available_date} from {self.start_time} to {self.end_time}"
    
class Interview(models.Model):
    #user m-m, availability 1-m
    STATUS_CHOICES = [
        ('matched', 'Matched'),
        ('current', 'Current'),
        ('completed', 'Completed'),
    ]

    interviewer = models.ForeignKey(User, related_name='interviewer', on_delete=models.CASCADE)
    interviewee = models.ForeignKey(User, related_name='interviewee', on_delete=models.CASCADE)
    interviewer_availability = models.ForeignKey(Availability, related_name='interviewer_availability', on_delete=models.CASCADE)
    interviewee_availability = models.ForeignKey(Availability, related_name='interviewee_availability', on_delete=models.CASCADE)
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