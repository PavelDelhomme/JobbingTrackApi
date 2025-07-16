class Event(BaseModel):
    """Événement lié à Application, Call, FollowUp ou Interview."""
    event_type_ref_id = models.CharField(max_length=36)
    start_ts          = models.BigIntegerField()
    end_ts            = models.BigIntegerField(null=True, blank=True)
    
    # Objet lié (un seul ID + son type)
    related_object_id   = models.CharField(max_length=36)
    related_object_type = models.CharField(max_length=50)   # ENUM : APPLICATION, CALL, INTERVIEW, FOLLOWUP

    description = models.TextField(blank=True)

    class Meta:
        db_table = 'events'
