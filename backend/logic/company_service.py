from apps.references.models import Reference, ReferenceType
from apps.events.models import Event


class CompanyService:
    @staticmethod
    def suggest_type(company):
        if company.sector and not company.type_ref_id:
            ref, _ = Reference.objects.get_or_create(
                user=company.user,
                label="Startup",
                type=ReferenceType.COMPANY_TYPE,
                defaults={"is_default": True}
            )
            company.type_ref_id = ref.id
            company.save(update_fields=["type_ref_id"])

    @staticmethod
    def on_create(company):
        Event.objects.create(
            user=company.user,
            title=f"Société ajoutée : {company.name}",
            event_type_ref_id="EVENT_TYPE_COMPANY_CREATED",
            start_ts=int(company.created_at.timestamp()),
            related_object_id=company.id,
            related_object_type="COMPANY",
        )