class Company(BaseModel):
    name          = models.CharField(max_length=255)
    type_ref_id   = models.CharField(max_length=36, null=True, blank=True)
    sector        = models.CharField(max_length=255, blank=True)
    notes         = models.TextField(blank=True)

    # liaisons
    contact_ids     = models.JSONField(default=list, blank=True)
    application_ids = models.JSONField(default=list, blank=True)
    followup_ids    = models.JSONField(default=list, blank=True)
    interview_ids   = models.JSONField(default=list, blank=True)
    call_ids        = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = 'companies'
