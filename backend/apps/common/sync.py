import hashlib
import time
import uuid
from django.apps import apps
from django.db import transaction
from backend.apps.common.serializers_registry import get_serializer_for_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.common.models.sync import SyncLedger
#from apps.common.serializers_registry import get_serializer_for_model
#from rest_framework.decorators import api_view, permission_classes
#from rest_framework.response import Response
#from rest_framework.permissions import IsAuthenticated
#from logic.sync_service import SyncService


MODELS = {
    "applications": "applications.Application",
    "companies":    "companies.Company",
    "calls":        "calls.Call",
    "followups":    "followups.FollowUp",
    "interviews":   "interviews.Interview",
    "contacts":     "contacts.Contact",
    "cvs":          "cvs.Cv",
    "events":       "events.Event",
    "profiles":     "profiles.UserProfile",
    "references":   "references.Reference",
    "calendar":     "calendar.Calendar",
    "user_settings": "profiles.UserSettings"    
}


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
        if ts and ts < 1000000000000: # Si en secondes, convertir en ms
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
        Met à jouer ou crée un objet à partir des données du client
        """
        model = apps.get_model(model_name)

        # Extraire l'ID et le vérifier
        obj_id = data.get('id')
        if not obj_id:
            # Générer un ID si non fourni
            obj_id = str(uuid.uuid4())
            data['id'] = obj_id
        
        # Préparer les données en gérant les relations
        defaults = SyncService._prepare_relation_data(model, data)

        # Ajouter l'utilisateur
        defaults['user'] = user

        # Timestamps par défaut si non fournis
        current_ts = int(time.time() * 1000)
        if 'created_at' not in defaults:
            defaults['created_at'] = current_ts
        if 'updated_at' not in defaults:
            defaults['updated_at'] = current_ts
        
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
                    relation_name = field_name[:-3] # Enlever '_id'
                    try:
                        field = model._meta.get_field(relation_name)
                        if field.is_relation and field.many_to_one:
                            # C'est une FK, récupérer l'objet lié
                            if value: # Si l'ID n'est pas None
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
                relation_name = field_name[:-4] # Enlever '_ids'

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
    


def serialize_instance(instance, request):
    """
    Sérialise un objet à l’aide du ModelSerializer enregistré
    """
    serializer_cls = get_serializer_for_model(type(instance))
    if not serializer_cls:
        # Fallback très léger : return __dict__ (sans _state)
        data = vars(instance).copy()
        data.pop('_state', None)
        return data
    return serializer_cls(instance, context={'request': request}).data


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sync_endpoint(request):
    """
    Endpoint pour récupérer les modifications du serveur
    """
    since = int(request.query_params.get("updated_after", 0))
    payload = {}
    
    for key, label in MODELS.items():
        changes = []
        ledger = SyncService.get_ledger(request.user, label)
        last_hash = ledger.last_hash if ledger else None
        
        # Récupère les objets modifiés avec leur hash
        changed_objects = SyncService.changed_since(label, request.user, since)
        
        for obj, new_hash in changed_objects:
            # Envoie seulement si hash différent ou pas de ledger
            if not last_hash or new_hash != last_hash:
                changes.append({
                    "id": str(obj.id),
                    "data": serialize_instance(obj, request), ## Modifie moi cela s'il te plait donc
                    "hash": new_hash
                })
        
        payload[key] = changes
        
        # Met à jour le ledger avec le dernier hash si nécessaire
        if changed_objects:
            SyncService.update_ledger(
                request.user,
                label,
                changed_objects[-1][1] # Dernier hash
            )
            
    return Response(payload)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def client_sync_endpoint(request):
    """
    Endpoit pour recevoir les mises à jour du client
    """
    result = {
        "status": "success",
        "processed": {},
        "errors": {}
    }
    
    client_data = request.data
    
    # Pour chaque type d'entité
    for entity_type, items in client_data.items():
        # Déterminer le modèle correspondant
        model_name = MODELS.get(entity_type)
        if not model_name:
            result["errors"][entity_type] = f"Type d'entité inconnu: {entity_type}"
            continue
            
        processed = []
        errors = []
        
        # Traiter chaque item
        for item_data in items:
            try:
                # Selon le type d'entité, utiliser le service approprié
                if entity_type == "applications":
                    from apps.applications.services import ApplicationService
                    obj, created = ApplicationService.create_or_update_application(
                        item_data, request.user
                    )
                elif entity_type == "calls":
                    from apps.calls.services import CallService
                    obj, created = CallService.create_or_update_call(
                        item_data, request.user
                    )
                elif entity_type == "followups":
                    from apps.followups.services import FollowUpService
                    obj, created = FollowUpService.create_or_update_followup(
                        item_data, request.user
                    )
                elif entity_type == "interviews":
                    from apps.interviews.services import InterviewService
                    obj, created = InterviewService.create_or_update_interview(
                        item_data, request.user
                    )
                else:
                    # Pour les autres types, utiliser le SyncService standard
                    obj, created = SyncService.update_from_client(
                        model_name,
                        item_data,
                        request.user
                    )
                
                # Enregistrer l'objet et son hash
                processed.append({
                    "id": str(obj.id),
                    "created": created,
                    "hash": SyncService.generate_hash(obj)
                })
            except Exception as e:
                errors.append({
                    "id": item_data.get("id", "unknown"),
                    "error": str(e)
                })
                
        result["processed"][entity_type] = processed
        if errors:
            result["errors"][entity_type] = errors
    
    return Response(result)