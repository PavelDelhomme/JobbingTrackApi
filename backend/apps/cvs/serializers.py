from apps.common.serializers import BaseModelSerializer
from .models import *

class SkillSerializer(BaseModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class EducationSerializer(BaseModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class ExperienceSerializer(BaseModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'

class CvSerializer(BaseModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    educations = EducationSerializer(many=True, read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)

    class Meta:
        model = Cv
        fields = ['id', 'title', 'summary', 'skills', 'educations', 'experiences']
