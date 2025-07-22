import uuid
import time
from .models import FollowUp

class FollowUpService:
    @staticmethod
    def create_or_update_followup(followup, user):
        if followup.id:
            FollowUp.objects.filter(id=followup.id).update(**followup.__dict__)
        else:
            followup.id = str(uuid.uuid4())
            followup.user = user
            followup.created_at = int(time.time() * 1000)
            followup.updated_at = int(time.time() * 1000)
            followup.save()

        return followup
    