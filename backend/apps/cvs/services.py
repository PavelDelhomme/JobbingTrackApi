from django.db import transaction
import uuid
import time
import os
from django.conf import settings

class CvService:
    @staticmethod
    @transaction.atomic
    def create_or_update_cv(data, user, file=None):
        """
        Crée ou met à jour un CV avec gestion du fichier
        """
        # Gérer le fichier si fourni
        if file:
            # Créer le dossier si nécessaire
            user_folder = os.path.join(settings.MEDIA_ROOT, 'cvs', str(user.id))
            os.makedirs(user_folder, exist_ok=True)
            
            # Générer un nom de fichier unique
            filename = f"{uuid.uuid4()}_{file.name}"
            file_path = os.path.join(user_folder, filename)
            
            # Sauvegarder le fichier
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            
            # Mettre à jour le chemin dans les données
            data['file_path'] = f"cvs/{user.id}/{filename}"
            
            # Extraire le type de fichier
            _, ext = os.path.splitext(file.name)
            data['file_type'] = ext.lower()[1:]  # Enlever le point
        
        # Créer ou mettre à jour le CV
        from apps.common.sync import SyncService
        cv, created = SyncService.update_from_client(
            'cvs.Cv',
            data,
            user
        )
        
        return cv, created
    
    @staticmethod
    def add_skill_to_cv(cv_id, skill_data, user):
        """
        Ajoute une compétence au CV
        """
        from apps.cvs.models import Cv, Skill
        
        try:
            cv = Cv.objects.get(id=cv_id, user=user)
            
            # Créer la compétence
            timestamp = int(time.time() * 1000)
            skill = Skill.objects.create(
                id=str(uuid.uuid4()),
                user=user,
                cv=cv,
                name=skill_data.get('name', ''),
                level=skill_data.get('level', 1),
                category=skill_data.get('category', ''),
                created_at=timestamp,
                updated_at=timestamp,
                is_deleted=False,
                is_archived=False
            )
            
            return skill
        except Cv.DoesNotExist:
            return None
    
    @staticmethod
    def add_experience_to_cv(cv_id, experience_data, user):
        """
        Ajoute une expérience professionnelle au CV
        """
        from apps.cvs.models import Cv, Experience
        
        try:
            cv = Cv.objects.get(id=cv_id, user=user)
            
            # Créer l'expérience
            timestamp = int(time.time() * 1000)
            experience = Experience.objects.create(
                id=str(uuid.uuid4()),
                user=user,
                cv=cv,
                title=experience_data.get('title', ''),
                company_name=experience_data.get('company_name', ''),
                location=experience_data.get('location', ''),
                start_date=experience_data.get('start_date', 0),
                end_date=experience_data.get('end_date'),
                is_current=experience_data.get('is_current', False),
                description=experience_data.get('description', ''),
                created_at=timestamp,
                updated_at=timestamp,
                is_deleted=False,
                is_archived=False
            )
            
            return experience
        except Cv.DoesNotExist:
            return None
    
    @staticmethod
    def add_education_to_cv(cv_id, education_data, user):
        """
        Ajoute une formation au CV
        """
        from apps.cvs.models import Cv, Education
        
        try:
            cv = Cv.objects.get(id=cv_id, user=user)
            
            # Créer la formation
            timestamp = int(time.time() * 1000)
            education = Education.objects.create(
                id=str(uuid.uuid4()),
                user=user,
                cv=cv,
                school_name=education_data.get('school_name', ''),
                degree=education_data.get('degree', ''),
                field_of_study=education_data.get('field_of_study', ''),
                location=education_data.get('location', ''),
                start_date=education_data.get('start_date', 0),
                end_date=education_data.get('end_date'),
                is_current=education_data.get('is_current', False),
                description=education_data.get('description', ''),
                created_at=timestamp,
                updated_at=timestamp,
                is_deleted=False,
                is_archived=False
            )
            
            return education
        except Cv.DoesNotExist:
            return None