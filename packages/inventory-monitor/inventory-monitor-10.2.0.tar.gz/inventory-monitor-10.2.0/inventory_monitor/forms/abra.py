from django import forms
from django.utils.translation import gettext as _
from netbox.forms import NetBoxModelFilterSetForm, NetBoxModelForm
from utilities.forms.fields import (
    CommentField,
    DynamicModelMultipleChoiceField,
    TagFilterField,
)
from utilities.forms.rendering import FieldSet

from inventory_monitor.models import ABRA, Asset


class ABRAForm(NetBoxModelForm):
    """
    Form for creating and editing ABRA objects
    """

    comments = CommentField(label="Comments")
    assets = DynamicModelMultipleChoiceField(
        queryset=Asset.objects.all(),
        required=False,
        label="Associated Assets",
    )

    fieldsets = (
        FieldSet(
            "inventory_number",
            "name",
            "serial_number",
            name=_("Asset Identification"),
        ),
        FieldSet(
            "person_id",
            "person_name",
            name=_("Person Information"),
        ),
        FieldSet(
            "location_code",
            "location",
            name=_("Location Information"),
        ),
        FieldSet(
            "activity_code",
            "user_name",
            "user_note",
            name=_("Usage Information"),
        ),
        FieldSet(
            "split_asset",
            "status",
            "assets",
            name=_("Status"),
        ),
        FieldSet("tags", name=_("Tags")),
    )

    class Meta:
        model = ABRA
        fields = (
            "inventory_number",
            "name",
            "serial_number",
            "person_id",
            "person_name",
            "location_code",
            "location",
            "activity_code",
            "user_name",
            "user_note",
            "split_asset",
            "status",
            "assets",
            "tags",
            "comments",
        )


class ABRAFilterForm(NetBoxModelFilterSetForm):
    """
    Filter form for ABRA objects
    """

    model = ABRA

    fieldsets = (
        FieldSet("q", "filter_id", "tag", name=_("Misc")),
        FieldSet(
            "inventory_number",
            "name",
            "serial_number",
            name=_("Asset Identification"),
        ),
        FieldSet(
            "person_id",
            "person_name",
            name=_("Person Information"),
        ),
        FieldSet(
            "location_code",
            "location",
            name=_("Location Information"),
        ),
        FieldSet(
            "activity_code",
            "user_name",
            name=_("Usage Information"),
        ),
        FieldSet(
            "split_asset",
            "status",
            "asset_id",
            name=_("Status"),
        ),
    )

    tag = TagFilterField(model)
    inventory_number = forms.CharField(required=False)
    name = forms.CharField(required=False)
    serial_number = forms.CharField(required=False)
    person_id = forms.CharField(required=False)
    person_name = forms.CharField(required=False)
    location_code = forms.CharField(required=False)
    location = forms.CharField(required=False)
    activity_code = forms.CharField(required=False)
    user_name = forms.CharField(required=False)
    split_asset = forms.CharField(required=False)
    status = forms.CharField(required=False)
    asset_id = DynamicModelMultipleChoiceField(
        queryset=Asset.objects.all(), required=False, label=_("Assets")
    )
