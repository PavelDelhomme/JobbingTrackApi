from django.db import models
from .base import BaseModel

class AbstractLinking(BaseModel):
    """
    Modèle abstrait pour les relations many-to-many personnalisées
    """
    class Meta:
        abstract = True

class ContactApplicationLink(AbstractLinking):
    contact_id = models.CharField(max_length=36)
    application_id = models.CharField(max_length=36)
    role = models.CharField(max_length=100, blank=True)  # ex: Manager / RH / Tech lead

    class Meta:
        unique_together = ("contact_id", "application_id")
        db_table = "contact_application_links"


class CallContactLink(AbstractLinking):
    call_id = models.CharField(max_length=36)
    contact_id = models.CharField(max_length=36)

    class Meta:
        unique_together = ("call_id", "contact_id")
        db_table = "call_contact_links"

class CompanyContactLink(AbstractLinking):
    company_id = models.CharField(max_length=36)
    contact_id = models.CharField(max_length=36)

    class Meta:
        unique_together = ("company_id", "contact_id")
        db_table = "company_contact_links"

class ApplicationEventLink(AbstractLinking):
    application_id = models.CharField(max_length=36)
    event_id = models.CharField(max_length=36)

    class Meta:
        unique_together = ("application_id", "event_id")
        db_table = "application_event_links"

class InterviewContactLink(AbstractLinking):
    interview_id = models.CharField(max_length=36)
    contact_id = models.CharField(max_length=36)

    class Meta:
        unique_together = ("interview_id", "contact_id")
        db_table = "interview_contact_links"

class FollowUpContactLink(AbstractLinking):
    followup_id = models.CharField(max_length=36)
    contact_id = models.CharField(max_length=36)

    class Meta:
        unique_together = ("followup_id", "contact_id")
        db_table = "followup_contact_links"

class FollowUpEventLink(AbstractLinking):
    followup_id = models.CharField(max_length=36)
    event_id = models.CharField(max_length=36)

    class Meta:
        unique_together = ("followup_id", "event_id")
        db_table = "followup_event_links"

class InterviewEventLink(AbstractLinking):
    interview_id = models.CharField(max_length=36)
    event_id = models.CharField(max_length=36)

    class Meta:
        unique_together = ("interview_id", "event_id")
        db_table = "interview_event_links"

class UserCompanyLink(AbstractLinking):
    user_id = models.CharField(max_length=36)
    company_id = models.CharField(max_length=36)

    class Meta:
        unique_together = ("user_id", "company_id")
        db_table = "user_company_links"

class UserApplicationLink(AbstractLinking):
    user_id = models.CharField(max_length=36)
    application_id = models.CharField(max_length=36)

    class Meta:
        unique_together = ("user_id", "application_id")
        db_table = "user_application_links"

class UserEventLink(AbstractLinking):
    user_id = models.CharField(max_length=36)
    event_id = models.CharField(max_length=36)

    class Meta:
        unique_together = ("user_id", "event_id")
        db_table = "user_event_links"

class UserInterviewLink(AbstractLinking):
    user_id = models.CharField(max_length=36)
    interview_id = models.CharField(max_length=36)

    class Meta:
        unique_together = ("user_id", "interview_id")
        db_table = "user_interview_links"

class UserFollowUpLink(AbstractLinking):
    user_id = models.CharField(max_length=36)
    followup_id = models.CharField(max_length=36)

    class Meta:
        unique_together = ("user_id", "followup_id")
        db_table = "user_followup_links"

class CompanyApplicationLink(AbstractLinking):
    company_id     = models.CharField(max_length=36)
    application_id = models.CharField(max_length=36)

    class Meta:
        unique_together = ('company_id', 'application_id')
        db_table = 'company_application_links'
