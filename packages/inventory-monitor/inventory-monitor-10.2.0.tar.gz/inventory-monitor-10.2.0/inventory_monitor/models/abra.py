from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel

from inventory_monitor.models.asset import Asset

ABRA_CSV_MAPPING = {
    "INVENT_CIS": "inventory_number",
    "NAZEV": "name",
    "CVYR": "serial_number",
    "OSOBA_OSCISLO": "person_id",
    "OSOBA": "person_name",
    "KOD_UMISTENI": "location_code",
    "UMISTENI": "location",
    "AKTIVITA": "activity_code",
    "NAZEV_UZIV": "user_name",
    "POZN_UZIV": "user_note",
    "DELENY_MAJETEK": "split_asset",
    "STAV": "status",
}


class ABRA(NetBoxModel):
    """
    Model representing inventory items imported from ABRA system

    Contains data directly mapped from the ABRA export CSV structure.
    """

    # Fields from CSV
    inventory_number = models.CharField(
        max_length=64,
        verbose_name="Inventory Number (Asset Number)",
        help_text="External asset identifier (INVENT_CIS)",
    )
    name = models.CharField(
        max_length=255, verbose_name="Name", help_text="Item name/description (NAZEV)"
    )
    serial_number = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Serial Number",
        help_text="Serial or production number (CVYR)",
    )
    person_id = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name="Person ID",
        help_text="ID of the person responsible for this item (OSOBA_OSCISLO)",
    )
    person_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Person Name",
        help_text="Name of the person responsible for this item (OSOBA)",
    )
    location_code = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name="Location Code",
        help_text="Code representing the location of this item (KOD_UMISTENI)",
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Location",
        help_text="Description of item location (UMISTENI)",
    )
    activity_code = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name="Activity Code",
        help_text="Activity code (AKTIVITA)",
    )
    user_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="User Name",
        help_text="Name of the user (NAZEV_UZIV)",
    )
    user_note = models.TextField(
        blank=True,
        null=True,
        verbose_name="User Notes",
        help_text="Notes from the user (POZN_UZIV)",
    )
    split_asset = models.CharField(
        # max_length=1,
        blank=True,
        null=True,
        verbose_name="Split Asset",
        help_text="Whether this is a split/shared asset (DELENY_MAJETEK): A=Yes, N=No",
    )
    status = models.CharField(
        # max_length=1,
        blank=True,
        null=True,
        verbose_name="Status",
        help_text="Current status of the item (STAV): 1=Active, 0=Inactive",
    )

    ############## EXTRA FIELDS
    assets = models.ManyToManyField(
        to=Asset,
        related_name="abra_assets",
        blank=True,
        verbose_name="Assets",
        help_text="Associated internal asset records",
    )

    class Meta:
        ordering = ("inventory_number", "name")
        verbose_name = "ABRA Asset"
        verbose_name_plural = "ABRA Assets"
        indexes = [
            models.Index(fields=["inventory_number"], name="abra_invnum_idx"),
            models.Index(fields=["serial_number"], name="abra_serial_idx"),
            models.Index(fields=["person_id"], name="abra_personid_idx"),
            models.Index(fields=["location_code"], name="abra_loccode_idx"),
            models.Index(fields=["status"], name="abra_status_idx"),
        ]
        # unique_together = [["inventory_number"]]

    def __str__(self):
        return f"{self.inventory_number}: {self.name}"

    def get_absolute_url(self):
        return reverse("plugins:inventory_monitor:abra", args=[self.pk])
