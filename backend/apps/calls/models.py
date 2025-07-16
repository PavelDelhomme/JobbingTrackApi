class Call(BaseModel):
    title           = models.CharField(max_length=255)
    call_ts         = models.BigIntegerField()                 # timestamp
    company_id      = models.CharField(max_length=36, null=True, blank=True)
    company_name    = models.CharField(max_length=255, blank=True)
    contact_id      = models.CharField(max_length=36, null=True, blank=True)
    contact_name    = models.CharField(max_length=255, blank=True)

    # si l’appel crée une candidature
    application_id  = models.CharField(max_length=36, null=True, blank=True)

    call_type_ref_id = models.CharField(max_length=36, null=True, blank=True)
    notes            = models.TextField(blank=True)

    class Meta:
        db_table = 'calls'
