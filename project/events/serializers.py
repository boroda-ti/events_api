from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    """
    Event model serializer.
    """
    
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['organizer', 'is_approved', 'created_at', 'updated_at']