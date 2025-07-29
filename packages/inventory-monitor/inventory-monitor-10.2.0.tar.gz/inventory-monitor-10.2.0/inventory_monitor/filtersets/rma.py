import django_filters
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet

from inventory_monitor.models import RMA


class RMAFilterSet(NetBoxModelFilterSet):
    q = django_filters.CharFilter(method="search")
    rma_number = django_filters.CharFilter(lookup_expr="icontains")
    status = django_filters.MultipleChoiceFilter(
        choices=RMA.status.field.choices,
    )

    class Meta:
        model = RMA
        fields = [
            "id",
            "rma_number",
            "asset_id",
            "original_serial",
            "replacement_serial",
            "status",
            "date_issued",
            "date_replaced",
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(rma_number__icontains=value)
            | Q(original_serial__icontains=value)
            | Q(replacement_serial__icontains=value)
            | Q(issue_description__icontains=value)
            | Q(vendor_response__icontains=value)
        )
