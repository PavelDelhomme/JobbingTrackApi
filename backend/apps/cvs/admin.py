from django.contrib import admin
from .models import (
    Cv, Education, Experience, Skill,
    Language, Project, Certification
)


admin.site.register(Cv)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Skill)
admin.site.register(Language)
admin.site.register(Project)
admin.site.register(Certification)