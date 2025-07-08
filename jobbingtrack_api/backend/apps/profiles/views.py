from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from .models import Profile, CV, Language, Experience, Education, Project
from .serializers import ProfileSerializer, CVSerializer, LanguageSerializer, ExperienceSerializer, EducationSerializer, ProjectSerializer

class CVViewSet(viewsets.ModelViewSet):
    serializer_class = CVSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CV.objects.none()
    
    def get_queryset(self):
        return CV.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def perform_update(self, serializer):
        
        serializer.save(user_id=self.request.user.id)


class UploadCVView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        profile = Profile.objects.filter(user_id=request.user.id).first()
        file = request.FILES.get("file")
        if not profile or not file:
            return Response({"error": "Profile ou fichier manquant"}, status=400)

        cv = CV.objects.create(profile=profile, user_id=request.user.id, file=file)
        return Response(CVSerializer(cv).data, status=201)

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.none()  # 👈 AJOUTE CECI
    
    def get_queryset(self):
        return Profile.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def perform_update(self, serializer):
        serializer.save(user_id=self.request.user.id)

    @action(detail=False, methods=["get"], url_path="archived")
    def archived(self, request):
        return self._list_filtered(is_archived=True, is_deleted=False)

    @action(detail=False, methods=["get"], url_path="active")
    def active(self, request):
        return self._list_filtered(is_archived=False, is_deleted=False)

    @action(detail=False, methods=["get"], url_path="deleted")
    def deleted(self, request):
        return self._list_filtered(is_deleted=True)

    @action(detail=False, methods=["post"], url_path="archive")
    def archive(self, request):
        ids = request.data.get("ids", [])
        qs = self.get_queryset().filter(id__in=ids)
        qs.update(is_archived=True, archived_at=now())
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["post"], url_path="soft-delete")
    def soft_delete(self, request):
        ids = request.data.get("ids", [])
        qs = self.get_queryset().filter(id__in=ids)
        qs.update(is_deleted=True, deleted_at=now())
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["post"], url_path="restore")
    def restore(self, request):
        ids = request.data.get("ids", [])
        qs = self.get_queryset().filter(id__in=ids)
        qs.update(is_deleted=False)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["post"], url_path="delete-forever")
    def delete_forever(self, request):
        ids = request.data.get("ids", [])
        self.get_queryset().filter(id__in=ids).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _list_filtered(self, **filters):
        qs = self.get_queryset().filter(**filters)
        return Response(self.get_serializer(qs, many=True).data)


class LanguageViewSet(viewsets.ModelViewSet):
    serializer_class = LanguageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Language.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def perform_update(self, serializer):
        serializer.save(user_id=self.request.user.id)
        
class ExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Experience.objects.filter(user_id=self.request.user.id)
    
    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def perform_update(self, serializer):
        serializer.save(user_id=self.request.user.id)
    

class EducationViewSet(viewsets.ModelViewSet):
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Education.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def perform_update(self, serializer):
        serializer.save(user_id=self.request.user.id)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def perform_update(self, serializer):
        serializer.save(user_id=self.request.user.id)
