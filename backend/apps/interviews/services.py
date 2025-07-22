from django.db import transaction

class InterviewService:
    @staticmethod
    @transaction.atomic
    def create_or_update_interview(data, user):
        """
        Crée ou met à jour une candidature avec gestion des entités liées
        """
        pass