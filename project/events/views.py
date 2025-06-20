from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .models import Event
from .serializers import EventSerializer
from .permissions import IsOrganizerOrReadOnly
from .utils import send_event_approved_email, send_event_created_email, send_event_delete_email

class EventListOrCreateAPIView(APIView):
    """
    View to retrieve events or create new event.

    Methods: GET, POST
    Permission: Authenticated or Read Only 

    GET:
    List all approved events (or all if admin). Supports filtering by:
    - `search` (title, description)
    - `location`
    - `start_date`, `end_date` (ISO format)
    - `is_approved` (admin only)
    - `ordering` by `date`, `title`

    POST:
    Create a new event. Automatically sets the current user as the organizer.
    Email notification is sent after creation.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        if request.user.is_staff:
            events = Event.objects.all()

        else:
            events = Event.objects.filter(is_approved=True)

        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if start_date:
            events = events.filter(date__gte=parse_datetime(start_date))

        if end_date:
            events = events.filter(date__lte=parse_datetime(end_date))

        search = request.GET.get("search")
        if search:
            events = events.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        location = request.GET.get("location")
        if location:
            events = events.filter(location__icontains=location)

        is_approved = request.GET.get("is_approved")
        if is_approved and request.user.is_staff:
            events = events.filter(is_approved=is_approved.lower() == "true")

        ordering = request.GET.get("ordering")
        allowed_fields = ['date', 'title', '-date', '-title']
        if ordering in allowed_fields:
            events = events.order_by(ordering)

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = EventSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(organizer=request.user)
            send_event_created_email.delay(request.user.email, serializer.data["title"])
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)


class EventDetailAPIView(APIView):
    """
    View to retrieve, update and delete event.

    Methods: GET, PATCH, DELETE
    Permission: Authenticated, Organizer or Read Only 

    GET:
    Retrieve a single event by ID. If not approved, only organizer or admin can access it.

    PATCH:
    Update an event (partial). Only organizer or admin can modify.
    Admin can approve it via separate endpoint.

    DELETE:
    Delete an event. Only organizer or admin allowed.
    Email notification is sent after deletion.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOrganizerOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Event, pk=pk)

    def get(self, request, pk):
        event = self.get_object(pk)

        if not event.is_approved and not request.user.is_staff and event.organizer != request.user:
            return Response({"detail": "Not approved yet."}, status=403)
        
        serializer = EventSerializer(event)
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        event = self.get_object(pk)

        if not request.user.is_staff and event.organizer != request.user:
            return Response({"detail": "Admin and Organizer only."}, status=403)

        serializer = EventSerializer(event, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(organizer=event.organizer)
            return Response(serializer.data, status=200)
        
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        event = self.get_object(pk)

        if not request.user.is_staff and event.organizer != request.user:
            return Response({"detail": "Admin and Organizer only."}, status=403)
        
        event.delete()

        send_event_delete_email.delay(event.organizer.email, event.title)
        return Response({"detail": "Event deleted."}, status=204)



class EventApproveAPIView(APIView):
    """
    View for approving event.

    Methods: POST
    Permission: Admin

    POST:
    Approve a pending event by ID.
    Sends notification email to the organizer.
    """

    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)

        if event.is_approved:
            return Response({"detail": "Already approved."}, status=400)
        
        event.is_approved = True
        event.save()

        send_event_approved_email.delay(event.organizer.email, event.title)
        return Response({"detail": "Event approved."}, status=200)
    

class EventUnApproveListAPIView(APIView):
    """
    View to retrieve unapproving events.

    Methods: GET
    Permission: Admin

    GET:
    List all unapproved events.
    """

    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        events = Event.objects.filter(is_approved=False)
        serializer = EventSerializer(events, many=True)
        return Response({"unapproved_events": serializer.data}, status=200)