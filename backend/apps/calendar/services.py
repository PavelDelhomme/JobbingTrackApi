from django.db import transaction
import uuid
import time
from datetime import datetime, timedelta
from apps.events.models import Event
from apps.calendar.models import Calendar

class CalendarService:
    @staticmethod
    def default_calendar(user):
        """Récupère ou crée le calendrier par défaut de l'utilisateur"""
        cal, _ = Calendar.objects.get_or_create(
            user=user, is_default=True,
            defaults={"name": "Calendrier principal"}
        )
        return cal
    
    @staticmethod
    def events_between(user, start_ts, end_ts):
        """Récupère les événements entre deux timestamps"""
        return Event.objects.filter(
            user=user,
            start_ts__gte=start_ts,
            start_ts__lte=end_ts,
            is_deleted=False
        )
    
    @staticmethod
    @transaction.atomic
    def set_as_default(calendar):
        """Définit un calendrier comme calendrier par défaut"""
        # Désactive l'ancien calendrier par défaut de l'utilisateur
        Calendar.objects.filter(
            user=calendar.user, is_default=True
        ).exclude(pk=calendar.pk).update(is_default=False)
        
        calendar.is_default = True
        calendar.save(update_fields=['is_default'])
    
    @staticmethod
    @transaction.atomic
    def create_or_update_calendar(data, user):
        """Crée ou met à jour un calendrier"""
        from apps.common.sync import SyncService
        calendar, created = SyncService.update_from_client(
            'calendar.Calendar',
            data,
            user
        )
        return calendar, created
    
    @staticmethod
    def get_upcoming_events(user, days=7):
        """Récupère les événements à venir pour l'utilisateur"""
        # Calculer la date de début (maintenant) et de fin (dans X jours)
        now_ts = int(datetime.now().timestamp() * 1000)
        end_ts = int((datetime.now() + timedelta(days=days)).timestamp() * 1000)
        
        # Récupérer les événements
        events = Event.objects.filter(
            user=user,
            event_ts__gte=now_ts,
            event_ts__lte=end_ts,
            is_deleted=False
        ).order_by('event_ts')
        
        return events
    
    @staticmethod
    def get_events_by_day(user, start_date, end_date):
        """Récupère les événements groupés par jour"""
        # Convertir les dates en timestamps
        start_ts = int(start_date.timestamp() * 1000)
        end_ts = int(end_date.timestamp() * 1000)
        
        # Récupérer les événements
        events = Event.objects.filter(
            user=user,
            event_ts__gte=start_ts,
            event_ts__lte=end_ts,
            is_deleted=False
        ).order_by('event_ts')
        
        # Grouper par jour
        events_by_day = {}
        for event in events:
            # Convertir le timestamp en date
            event_date = datetime.fromtimestamp(event.event_ts / 1000).date()
            day_key = event_date.strftime("%Y-%m-%d")
            
            if day_key not in events_by_day:
                events_by_day[day_key] = []
                
            events_by_day[day_key].append(event)
        
        return events_by_day