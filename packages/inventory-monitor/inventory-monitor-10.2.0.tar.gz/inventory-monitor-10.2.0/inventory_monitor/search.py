from netbox.search import SearchIndex, register_search

from inventory_monitor.models import (
    Asset,
    AssetType,
    ComponentService,
    Contract,
    Contractor,
    Invoice,
    Probe,
)


@register_search
class ContractIndex(SearchIndex):
    model = Contract

    fields = (("name", 100), ("name_internal", 100), ("comments", 5000))
    display_attrs = ("name", "name_internal")


@register_search
class ContractorIndex(SearchIndex):
    model = Contractor

    fields = (
        ("name", 100),
        ("company", 100),
        ("address", 5000),
    )  # Removed duplicate "address" field
    display_attrs = ("name", "company")


@register_search
class InvoiceIndex(SearchIndex):
    model = Invoice
    fields = (
        ("name", 100),
        ("name_internal", 100),
        ("project", 300),
        ("comments", 5000),
    )
    display_attrs = ("name", "project")


@register_search
class ProbeIndex(SearchIndex):
    model = Probe

    fields = (
        ("device_descriptor", 100),
        ("site_descriptor", 100),
        ("location_descriptor", 100),
        ("name", 100),
        ("serial", 100),
        ("description", 5000),
        ("comments", 5000),
    )
    display_attrs = ("name", "device_descriptor", "site_descriptor")


@register_search
class AssetIndex(SearchIndex):
    model = Asset

    fields = (
        ("serial", 100),
        ("partnumber", 100),
        ("description", 5000),
        ("asset_number", 5000),
        ("comments", 5000),
    )
    display_attrs = ("serial", "partnumber")


@register_search
class ComponentServiceIndex(SearchIndex):
    model = ComponentService

    fields = (
        ("service_category", 100),
        ("service_category_vendor", 100),
        ("comments", 5000),
    )
    display_attrs = ("service_category",)


@register_search
class AssetTypeIndex(SearchIndex):
    model = AssetType
    fields = (
        ("name", 100),
        ("slug", 110),
        ("description", 500),
    )
    display_attrs = ("name", "description")
