from apps.common.serializers import BaseModelSerializer
from .models import (
    Cv, Education, Experience, Skill,
    Language, Project, Certification
)


class EducationSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Education
        fields = "__all__"


class ExperienceSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Experience
        fields = "__all__"


class SkillSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Skill
        fields = "__all__"


class LanguageSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Language
        fields = "__all__"


class ProjectSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Project
        fields = "__all__"


class CertificationSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Certification
        fields = "__all__"


class CvSerializer(BaseModelSerializer):
    educations     = EducationSerializer(many=True, read_only=True)
    experiences    = ExperienceSerializer(many=True, read_only=True)
    skills         = SkillSerializer(many=True, read_only=True)
    languages      = LanguageSerializer(many=True, read_only=True)
    projects       = ProjectSerializer(many=True, read_only=True)
    certifications = CertificationSerializer(many=True, read_only=True)

    class Meta(BaseModelSerializer.Meta):
        model = Cv
        fields = "__all__"
