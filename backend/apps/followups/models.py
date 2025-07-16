class FollowUp(BaseModel):
    followup_ts     = models.BigIntegerField()
    application_id  = models.CharField(max_length=36)
    company_id      = models.CharField(max_length=36)
    contact_id      = models.CharField(max_length=36, null=True, blank=True)

    platform_ref_id = models.CharField(max_length=36, null=True, blank=True)
    type_ref_id     = models.CharField(max_length=36)
    status_ref_id   = models.CharField(max_length=36, null=True, blank=True)
    notes           = models.TextField(blank=True)

    # appel créé automatiquement ?
    call_id         = models.CharField(max_length=36, null=True, blank=True)

    class Meta:
        db_table = 'followups'
