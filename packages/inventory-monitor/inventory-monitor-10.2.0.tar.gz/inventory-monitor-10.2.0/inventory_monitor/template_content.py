"""
Template Extensions and Views for Inventory Monitor Plugin.

This module provides NetBox UI customizations including:
- Template extensions for displaying inventory data
- Custom views for assets and probes
- Dynamic view registration for different model types
"""

from dcim.models import Device, Location, Module, Rack, Site
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from netbox.plugins import PluginTemplateExtension
from netbox.views import generic
from utilities.views import ViewTab, register_model_view

from inventory_monitor.filtersets import AssetFilterSet, ProbeFilterSet
from inventory_monitor.models import Asset, Contract, Contractor, Probe
from inventory_monitor.tables import AssetTable, ProbeTable

# Load plugin configuration settings
plugin_settings = settings.PLUGINS_CONFIG.get("inventory_monitor", {})


class TenantContractorExtension(PluginTemplateExtension):
    """Display contractor information on tenant detail page."""

    models = ["tenancy.tenant"]

    def left_page(self):
        """Show contractor details in the left sidebar."""
        # Find contractor associated with this tenant
        contractor = Contractor.objects.filter(
            tenant_id=self.context["object"].pk
        ).first()

        # Count contracts if contractor exists
        contracts_count = contractor.contracts.count() if contractor else 0

        return self.render(
            "inventory_monitor/inc/tenant_contractor_extension.html",
            extra_context={
                "contractor": contractor,
                "contracts_count": contracts_count,
            },
        )


class AbraAssetsExtension(PluginTemplateExtension):
    """Display assets information on abra detail page."""

    models = ["inventory_monitor.abra"]

    def full_width_page(self):
        """Show asset details in the full_width_page."""
        return self.render(
            "inventory_monitor/inc/abra_asset_extension.html",
        )


class ProbeAssetExtension(PluginTemplateExtension):
    """Display assets with matching serial number on probe detail page."""

    models = ["inventory_monitor.probe"]

    def right_page(self):
        """Display matching assets in the full width section of the page."""
        probe = self.context["object"]

        # Find assets that match any of these criteria:
        # 1. Current asset serial matches probe serial
        # 2. Asset has an RMA where original_serial matches probe serial
        # 3. Asset has an RMA where replacement_serial matches probe serial
        matching_assets = Asset.objects.filter(
            Q(serial=probe.serial)
            | Q(rmas__original_serial=probe.serial)
            | Q(rmas__replacement_serial=probe.serial)
        ).distinct()

        # Create asset table for display
        asset_table = AssetTable(matching_assets)

        return self.render(
            "inventory_monitor/inc/probe_asset_extension.html",
            extra_context={
                "assets": matching_assets,
                "asset_table": asset_table,
                "assets_count": matching_assets.count(),
            },
        )


class AssetDuplicates(PluginTemplateExtension):
    """Show potential duplicate assets with the same serial number or RMA relationships."""

    models = ["inventory_monitor.asset"]

    def full_width_page(self):
        """Display duplicate assets in the full width section of the page."""
        current_asset = self.context["object"]

        # Instead of combining querysets, let's get all potential candidates first
        # Then filter them in Python to avoid SQL-level combination issues
        potential_duplicates_ids = set()

        # Track different duplicate types separately
        direct_duplicates_ids = set()
        rma_duplicates_ids = set()
        reverse_rma_duplicates_ids = set()

        # Find direct duplicates (same serial)
        if current_asset.serial:
            direct_dups = (
                Asset.objects.filter(serial=current_asset.serial)
                .exclude(id=current_asset.id)
                .values_list("id", flat=True)
            )

            direct_duplicates_ids.update(direct_dups)
            potential_duplicates_ids.update(direct_dups)

        # Find assets that have this serial in their RMAs
        if current_asset.serial:
            rma_dups = (
                Asset.objects.filter(
                    Q(rmas__original_serial=current_asset.serial)
                    | Q(rmas__replacement_serial=current_asset.serial)
                )
                .exclude(id=current_asset.id)
                .values_list("id", flat=True)
                .distinct()
            )

            rma_duplicates_ids.update(rma_dups)
            potential_duplicates_ids.update(rma_dups)

        # Find assets where this asset's serial appears in their RMA records
        if (
            current_asset.serial
            and hasattr(current_asset, "rmas")
            and current_asset.rmas.exists()
        ):
            # Get the RMA serials
            original_serials = [
                s
                for s in list(
                    current_asset.rmas.values_list("original_serial", flat=True)
                )
                if s
            ]
            replacement_serials = [
                s
                for s in list(
                    current_asset.rmas.values_list("replacement_serial", flat=True)
                )
                if s
            ]

            if original_serials or replacement_serials:
                # Create a list of all serials to search for
                all_serials = original_serials + replacement_serials

                # Get assets with matching serials in a single query
                reverse_rma_dups = (
                    Asset.objects.filter(serial__in=all_serials)
                    .exclude(id=current_asset.id)
                    .values_list("id", flat=True)
                    .distinct()
                )

                reverse_rma_duplicates_ids.update(reverse_rma_dups)
                potential_duplicates_ids.update(reverse_rma_dups)

        # Now that we have all IDs, fetch the full asset objects in a single query
        all_duplicates = Asset.objects.filter(id__in=list(potential_duplicates_ids))

        # Calculate counts
        direct_duplicates_count = len(direct_duplicates_ids)
        rma_duplicates_count = len(rma_duplicates_ids)
        reverse_rma_duplicates_count = len(reverse_rma_duplicates_ids)

        return self.render(
            "inventory_monitor/inc/asset_duplicates_extension.html",
            extra_context={
                "current_asset": current_asset,
                "duplicates": all_duplicates,
                "duplicates_count": len(potential_duplicates_ids),
                "direct_duplicates_count": direct_duplicates_count,
                "rma_duplicates_count": rma_duplicates_count,
                "reverse_rma_duplicates_count": reverse_rma_duplicates_count,
            },
        )


@register_model_view(Asset, name="probes", path="probes")
class AssetProbesView(generic.ObjectChildrenView):
    """Provides a 'Probes' tab on asset detail pages showing related probe records."""

    queryset = Asset.objects.all()
    child_model = Probe
    table = ProbeTable
    filterset = ProbeFilterSet
    template_name = "generic/object_children.html"
    hide_if_empty = False
    tab = ViewTab(
        label="Probes",
        badge=lambda obj: obj.get_related_probes().count(),
        permission="inventory_monitor.view_probe",
    )

    def get_children(self, request, parent):
        """Retrieve all probes related to this asset."""
        return parent.get_related_probes()


@register_model_view(Contract, name="assets", path="assets")
class ContractAssetsView(generic.ObjectChildrenView):
    """View to display assets ordered through this contract."""

    queryset = Contract.objects.all()
    child_model = Asset
    filterset = AssetFilterSet
    table = AssetTable
    template_name = "generic/object_children.html"
    hide_if_empty = False
    tab = ViewTab(
        label="Assets",
        badge=lambda obj: obj.assets.count(),
        permission="inventory_monitor.view_asset",
    )

    def get_children(self, request, parent):
        """Get assets where this contract is the order_contract."""
        return parent.assets.all()


class AssignedAssetsView(generic.ObjectChildrenView):
    """Base class for views that display assets assigned to any object type."""

    child_model = Asset
    table = AssetTable
    template_name = "generic/object_children.html"
    filterset = AssetFilterSet
    hide_if_empty = False

    def get_children(self, request, parent):
        """Get assets assigned to this object using the ContentType framework."""
        content_type = ContentType.objects.get_for_model(parent)
        return Asset.objects.filter(
            assigned_object_type=content_type, assigned_object_id=parent.pk
        )


def register_asset_view_for_models(*models):
    """
    Factory function to register asset views for multiple models.

    Dynamically creates view classes for each model to avoid duplicating code.
    Each view shows assets assigned to objects of that model type.

    Args:
        *models: List of models to register asset views for

    Returns:
        list: Created view classes
    """
    views = []

    for model in models:
        # Create class name based on model name
        class_name = f"{model.__name__}AssetsView"

        # Create view class dynamically
        view_class = type(
            class_name,
            (AssignedAssetsView,),
            {
                "queryset": model.objects.all(),
                "tab": ViewTab(
                    label="Assets",
                    badge=lambda obj, model=model: Asset.objects.filter(
                        assigned_object_type=ContentType.objects.get_for_model(model),
                        assigned_object_id=obj.pk,
                    ).count(),
                    permission="inventory_monitor.view_asset",
                ),
            },
        )

        # Register view with model
        register_model_view(model, name="assets", path="assets")(view_class)
        views.append(view_class)

    return views


# Register asset views for all models that can have assets assigned
register_asset_view_for_models(Site, Location, Rack, Device, Module)

# Template extensions to be registered by the plugin
template_extensions = [
    ProbeAssetExtension,
    TenantContractorExtension,
    AssetDuplicates,
    AbraAssetsExtension,
]
