from django.shortcuts import render
from rest_framework import viewsets, status
from django.db.models import Q
from .models import Availability, Interview
from .serializers import AvailabilitySerializer, InterviewSerializer
from rest_framework.response import Response

class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        available_date = request.data.get('available_date')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        # Check for time order
        if end_time <= start_time:
            return Response({'status': 'conflict', 'message': 'End time must be after start time.'}, status=400)
        
        # Check the new availability if exists before

        # if the  new included in the old, do nothing
        availability = Availability.objects.filter(
            user=user_id,
            available_date=available_date,
            start_time__lt=start_time,
            end_time__gt=end_time,
            # status='not booked'
        )       
        if availability.exists():
            return Response({'status': 'neutral', 'message': 'The availability is already exists'}, status=200)

        # if the old included in the new, update the old if not booked
        availability = Availability.objects.filter(
            user=user_id,
            available_date=available_date,
            start_time__gt=start_time,
            end_time__lt=end_time,
            status='not booked'
        ).first()

        if availability:
            availability.start_time = start_time
            availability.end_time = end_time
            availability.save()
            return Response({'status': 'merging', 'message': 'The availability is modified'}, status=200)
        
        # if booked, 1.split the new to before and after or 2. not allowing
        availability = Availability.objects.filter(
            user=user_id,
            available_date=available_date,
            start_time__gt=start_time,
            end_time__lt=end_time,
            status='booked'
        ).first()

        if availability:
            super().create(request, start_time=start_time, end_time=availability.start_time,  *args, **kwargs)
            super().create(request, start_time=availability.end_time, end_time=end_time,  *args, **kwargs)
            return Response({'status': 'creating', 'message': 'new availabilities were created before and after the existing'}, status=200)
            return Response({'status': 'conflict', 'message': 'there is a booked interview in this period'}, status=200)

        
        # if new overlaps the old, split the new
        availability = Availability.objects.filter(
            user=user_id,
            available_date=available_date,
            start_time__lt=end_time,
            end_time__gt=start_time,
            # status='not booked'
        ).first()
        if availability:
            # if start_time >= availability.start_time:
            #     start_time = availability.end_time
            # else:
            #     end_time = availability.start_time

            # response =  super().create(request, *args, **kwargs)
            # return Response({'status': 'spliting', 'message': 'The new availability is splited'}, status=200)
            return Response({'status': 'conflict', 'message': 'Overlapped avaialabilities is not allowed'}, status=400)

        response =  super().create(request, *args, **kwargs)
        return response

class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer

    def create(self, request, *args, **kwargs):
        interviewer_id = request.data.get('interviewer')
        interviewee_id = request.data.get('interviewee')
        scheduled_date = request.data.get('scheduled_date')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        # Prevent self-booking
        if interviewer_id == interviewee_id:
            return Response({'status': 'error', 'message': 'A user cannot book an interview with themselves.'}, status=400)
        
        # Check for time order
        if end_time <= start_time:
            return Response({'status': 'conflict', 'message': 'End time must be after start time.'}, status=400)

        # Fetch interviews for interviewer and interviewee to check for conflicts
        interviewer_conflicts = Interview.objects.filter(
            interviewer=interviewer_id,
            scheduled_date=scheduled_date,
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        interviewee_conflicts = Interview.objects.filter(
            interviewee=interviewee_id,
            scheduled_date=scheduled_date,
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        # Check for any conflicts
        if interviewer_conflicts.exists() or interviewee_conflicts.exists():
            return Response({'status': 'conflict', 'message': 'The interviewer or interviewee has an overlapping interview.'}, status=400)

        # Check interviewer's availability
        interviewer_availability = Availability.objects.filter(
            user=interviewer_id,
            available_date=scheduled_date,
            start_time__lte=start_time,
            end_time__gte=end_time,
            status='not booked'
        ).first()

        if not interviewer_availability:
            return Response({'status': 'conflict', 'message': 'Interviewer is not available at this time.'}, status=400)

        # Check interviewee's availability
        interviewee_availability = Availability.objects.filter(
            user=interviewee_id,
            available_date=scheduled_date,
            start_time__lte=start_time,
            end_time__gte=end_time,
            status='not booked'
        ).first()

        if not interviewee_availability:
            return Response({'status': 'conflict', 'message': 'Interviewee is not available at this time.'}, status=400)

        # If no conflicts, proceed with scheduling

        data = request.data
        new = Interview(interviewer_id=data['interviewer'], interviewee_id=data['interviewee'], interviewer_availability_id=interviewer_availability.id, interviewee_availability_id=interviewee_availability.id, scheduled_date=data['scheduled_date'], start_time=data['start_time'], end_time=data['end_time'], status=data['status'])
        new.save()

        interviewer_availability.status = 'booked'
        interviewer_availability.save()

        interviewee_availability.status = 'booked'
        interviewee_availability.save()

        serializer = InterviewSerializer(new)
        return Response(serializer.data)
        return response
