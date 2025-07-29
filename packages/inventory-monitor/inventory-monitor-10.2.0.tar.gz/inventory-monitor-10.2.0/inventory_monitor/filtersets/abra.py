import django_filters
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet

from inventory_monitor.models import ABRA, Asset


class ABRAFilterSet(NetBoxModelFilterSet):
    """
    Filterset for ABRA objects providing comprehensive search and filtering capabilities.
    """

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )
    inventory_number = django_filters.CharFilter(lookup_expr="icontains")
    name = django_filters.CharFilter(lookup_expr="icontains")
    serial_number = django_filters.CharFilter(lookup_expr="icontains")
    person_id = django_filters.CharFilter(lookup_expr="icontains")
    person_name = django_filters.CharFilter(lookup_expr="icontains")
    location_code = django_filters.CharFilter(lookup_expr="icontains")
    location = django_filters.CharFilter(lookup_expr="icontains")
    activity_code = django_filters.CharFilter(lookup_expr="icontains")
    user_name = django_filters.CharFilter(lookup_expr="icontains")
    user_note = django_filters.CharFilter(lookup_expr="icontains")
    split_asset = django_filters.CharFilter(lookup_expr="iexact")
    status = django_filters.CharFilter(lookup_expr="iexact")
    asset_id = django_filters.ModelMultipleChoiceFilter(
        field_name="assets",
        queryset=Asset.objects.all(),
        to_field_name="id",
        label="Asset (ID)",
    )

    class Meta:
        model = ABRA
        fields = [
            "id",
            "inventory_number",
            "name",
            "serial_number",
            "person_id",
            "person_name",
            "location_code",
            "location",
            "activity_code",
            "user_name",
            "split_asset",
            "status",
            "asset_id",
        ]

    def search(self, queryset, name, value):
        """
        Perform global search across multiple fields

        Args:
            queryset: Base queryset to filter
            name: Name of the filter parameter
            value: Search term to filter by

        Returns:
            Filtered queryset containing matching ABRA records
        """
        if not value.strip():
            return queryset

        return queryset.filter(
            Q(inventory_number__icontains=value)
            | Q(name__icontains=value)
            | Q(serial_number__icontains=value)
            | Q(person_id__icontains=value)
            | Q(person_name__icontains=value)
            | Q(location_code__icontains=value)
            | Q(location__icontains=value)
            | Q(user_name__icontains=value)
            | Q(user_note__icontains=value)
            | Q(assets__description__icontains=value)
            | Q(assets__serial__icontains=value)
        ).distinct()
