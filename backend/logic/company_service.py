from apps.references.models import Reference, ReferenceType

class CompanyService:
    @staticmethod
    def suggest_type(company):
        if company.sector and not company.type_ref_id:
            default, _ = Reference.objects.get_or_create(
                user=company.user,
                label='Start-up',
                type=ReferenceType.COMPANY_TYPE
            )
            company.type_ref_id = default.id
            company.save(update_fields=['type_ref_id'])
