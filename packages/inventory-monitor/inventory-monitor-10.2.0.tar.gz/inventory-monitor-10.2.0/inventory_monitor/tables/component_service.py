import django_tables2 as tables
from netbox.tables import NetBoxTable

from inventory_monitor.helpers import NumberColumn
from inventory_monitor.models import ComponentService


class ComponentServiceTable(NetBoxTable):
    asset = tables.Column(linkify=True)
    contract = tables.Column(linkify=True)
    service_price = NumberColumn(accessor="service_price")
    service_status = tables.TemplateColumn(
        template_code="""
            {% include 'inventory_monitor/inc/status_badge.html' with status_type='service' %}
        """,
        verbose_name="Service Status",
        orderable=False,
    )

    class Meta(NetBoxTable.Meta):
        model = ComponentService
        fields = (
            "pk",
            "id",
            "service_start",
            "service_end",
            "service_status",
            "service_param",
            "service_price",
            "service_category",
            "service_category_vendor",
            "asset",
            "contract",
            "comments",
            "actions",
        )
        default_columns = (
            "id",
            "contract",
            "service_start",
            "service_end",
            "service_price",
            "service_category",
            "service_category_vendor",
            "service_param",
            "actions",
        )
