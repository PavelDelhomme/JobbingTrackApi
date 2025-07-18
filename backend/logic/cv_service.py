class CvService:
    @staticmethod
    def ensure_single_primary(cv):
        if cv.is_primary:
            cv.__class__.objects.filter(user=cv.user, is_primary=True)\
                .exclude(pk=cv.pk).update(is_primary=False)
