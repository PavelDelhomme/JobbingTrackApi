class Interview(BaseModel):
    interview_ts     = models.BigIntegerField()
    application_id   = models.CharField(max_length=36)
    company_id       = models.CharField(max_length=36)
    location         = models.CharField(max_length=255, blank=True)

    style_ref_id     = models.CharField(max_length=36, null=True, blank=True)
    type_ref_id      = models.CharField(max_length=36, null=True, blank=True)
    status_ref_id    = models.CharField(max_length=36, null=True, blank=True)

    contact_ids      = models.JSONField(default=list, blank=True)
    notes_pre        = models.TextField(blank=True)
    notes_during     = models.TextField(blank=True)
    notes_post       = models.TextField(blank=True)

    tests_needed     = models.BooleanField(default=False)
    tests_done       = models.BooleanField(default=False)

    class Meta:
        db_table = 'interviews'
