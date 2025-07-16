class Application(BaseModel):
    title            = models.CharField(max_length=255)
    company_id       = models.CharField(max_length=36)
    company_name     = models.CharField(max_length=255)      # accès rapide
    application_ts   = models.BigIntegerField()              # timestamp
    location         = models.CharField(max_length=255, blank=True)

    # références
    platform_ref_id  = models.CharField(max_length=36, null=True, blank=True)
    status_ref_id    = models.CharField(max_length=36)
    type_ref_id      = models.CharField(max_length=36)
    contract_ref_id  = models.CharField(max_length=36, null=True, blank=True)

    # relations (listes d’IDs)
    contact_ids   = models.JSONField(default=list, blank=True)
    followup_ids  = models.JSONField(default=list, blank=True)
    interview_ids = models.JSONField(default=list, blank=True)
    call_ids      = models.JSONField(default=list, blank=True)
    event_ids     = models.JSONField(default=list, blank=True)

    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'applications'
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'