import hashlib
import time
from django.apps import apps
from django.db import transaction
from apps.common.models.sync import SyncLedger

class SyncService:
    @staticmethod
    def generate_hash(obj):
        """Génère un hash basé sur l'ID et updated_at"""
        # Pour les BigIntegerField, nous utilisons directement la valeur
        if hasattr(obj, 'updated_at') and isinstance(obj.updated_at, int):
            timestamp = obj.updated_at
        else:
            timestamp = int(obj.updated_at.timestamp() * 1000)
        data = f"{obj.id}{timestamp}"
        return hashlib.md5(data.encode()).hexdigest()

    @staticmethod
    def get_ledger(user, model_label):
        try:
            return SyncLedger.objects.get(user=user, model_name=model_label)
        except SyncLedger.DoesNotExist:
            return None
    
    @staticmethod
    def changed_since(model_label, user, ts):
        """Retourne les objets modifiés avec leur hash"""
        model = apps.get_model(model_label)
        
        # Convertir ts en millisecondes si nécessaire
        if ts and ts < 1000000000000:  # Si en secondes, convertir en ms
            ts = ts * 1000
            
        # Filtrer les objets modifiés depuis le timestamp
        query = model.objects.filter(user=user, is_deleted=False)
        
        # Adapter le filtre selon le type de champ updated_at
        field_instance = model._meta.get_field('updated_at')
        if field_instance.get_internal_type() == 'BigIntegerField':
            query = query.filter(updated_at__gt=ts)
        else:
            # Pour DateTimeField, convertir le timestamp en datetime
            from datetime import datetime
            dt = datetime.fromtimestamp(ts / 1000)
            query = query.filter(updated_at__gt=dt)
            
        return [(obj, SyncService.generate_hash(obj)) for obj in query]
    
    
    @staticmethod
    def update_ledger(user, model_label, new_hash):
        ledger, _ = SyncLedger.objects.update_or_create(
            user=user,
            model_name=model_label,
            defaults={'last_hash': new_hash}
        )
        return ledger
    
    @staticmethod
    @transaction.atomic
    def update_from_client(model_name, data, user):
        """
        Met à jour ou crée un objet à partir des données du client
        
        Args:
            model_name: Nom du modèle (ex: 'applications.Application')
            data: Dictionnaire des données à mettre à jour
            user: Utilisateur propriétaire des données
            
        Returns:
            Tuple (objet, created) - l'objet mis à jour et un booléen indiquant s'il a été créé
        """
        model = apps.get_model(model_name)
        
        # Extraire l'ID et le vérifier
        obj_id = data.get('id')
        if not obj_id:
            raise ValueError("L'ID est requis pour la synchronisation")
        
        # Préparer les données en gérant les relations
        defaults = SyncService._prepare_relation_data(model, data)
        
        # Ajouter l'utilisateur
        defaults['user'] = user
        
        # Mettre à jour ou créer l'objet
        with transaction.atomic():
            obj, created = model.objects.update_or_create(
                id=obj_id,
                defaults=defaults
            )
            
            # Mettre à jour les relations M2M si nécessaire
            SyncService._update_m2m_relations(obj, data)
            
        return obj, created
    
    @staticmethod
    def _prepare_relation_data(model, data):
        """
        Prépare les données en remplaçant les ID de FK par les objets réels
        """
        defaults = {}
        
        for field_name, value in data.items():
            # Ignorer l'ID principal et les champs spéciaux
            if field_name in ['id', 'user'] or field_name.endswith('_ids'):
                continue
                
            field = None
            try:
                field = model._meta.get_field(field_name)
            except:
                # Si le champ n'existe pas directement, vérifier s'il s'agit d'un ID de FK
                if field_name.endswith('_id') and not field_name.endswith('_ids'):
                    relation_name = field_name[:-3]  # Enlever '_id'
                    try:
                        field = model._meta.get_field(relation_name)
                        if field.is_relation and field.many_to_one:
                            # C'est une FK, récupérer l'objet lié
                            if value:  # Si l'ID n'est pas None
                                related_model = field.related_model
                                try:
                                    related_obj = related_model.objects.get(id=value)
                                    defaults[relation_name] = related_obj
                                except related_model.DoesNotExist:
                                    # Ignorer les références à des objets inexistants
                                    pass
                            continue
                    except:
                        pass
            
            # Traitement standard pour les champs normaux
            if field and not field.is_relation:
                defaults[field_name] = value
            elif field and field.is_relation and field.many_to_one:
                # Pour les ForeignKey, on attend l'objet pas l'ID
                if value:
                    related_model = field.related_model
                    try:
                        related_obj = related_model.objects.get(id=value)
                        defaults[field_name] = related_obj
                    except related_model.DoesNotExist:
                        # Ignorer les références à des objets inexistants
                        pass
        
        return defaults
    
    @staticmethod
    def _update_m2m_relations(obj, data):
        """
        Met à jour les relations many-to-many à partir des listes d'IDs
        """
        for field_name, value in data.items():
            if field_name.endswith('_ids') and isinstance(value, list):
                relation_name = field_name[:-4]  # Enlever '_ids'
                
                try:
                    # Vérifier si c'est un champ M2M
                    field = obj._meta.get_field(relation_name)
                    if field.is_relation and field.many_to_many:
                        # Récupérer les objets liés
                        related_model = field.related_model
                        related_objects = related_model.objects.filter(id__in=value)
                        
                        # Mettre à jour la relation
                        getattr(obj, relation_name).set(related_objects)
                except:
                    # Ce n'est pas un champ M2M, ignorer
                    pass