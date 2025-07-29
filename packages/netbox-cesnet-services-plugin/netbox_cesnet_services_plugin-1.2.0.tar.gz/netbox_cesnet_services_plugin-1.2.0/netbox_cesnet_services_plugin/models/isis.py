from dcim.models import Device, Interface
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import JSONField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet


# Add to your choices.py file
class ISISNeighborStatusChoices(ChoiceSet):
    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"
    STATUS_PLANNED = "planned"
    STATUS_FAILED = "failed"

    CHOICES = [
        (STATUS_ACTIVE, _("Active")),
        (STATUS_INACTIVE, _("Inactive")),
        (STATUS_PLANNED, _("Planned")),
        (STATUS_FAILED, _("Failed")),
    ]

    colors = {
        STATUS_ACTIVE: "green",
        STATUS_INACTIVE: "orange",
        STATUS_PLANNED: "blue",
        STATUS_FAILED: "red",
    }


class ISISNeighbor(NetBoxModel):
    """
    ISIS neighbor relationship between network devices.
    """

    local_device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        verbose_name=_("Local Device"),
        help_text=_("Device where the ISIS relationship was discovered"),
        related_name="isis_neighbors_local",
        null=False,
        blank=False,
    )
    local_interface = models.ForeignKey(
        Interface,
        on_delete=models.CASCADE,
        verbose_name=_("Local Interface"),
        help_text=_("Local interface participating in the ISIS relationship"),
        related_name="isis_neighbors_local",
        null=False,
        blank=False,
    )
    remote_device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        verbose_name=_("Remote Device"),
        help_text=_("Remote ISIS device"),
        related_name="isis_neighbors_remote",
        null=False,
        blank=False,
    )

    # ISIS specific fields
    state = models.CharField(
        max_length=50,
        verbose_name=_("State"),
        help_text=_("ISIS neighbor state"),
        default="Up",
    )
    holdtime = models.IntegerField(
        verbose_name=_("Hold Time"),
        help_text=_("ISIS neighbor holdtime in seconds"),
        null=True,
        blank=True,
    )
    type = models.CharField(
        max_length=10,
        verbose_name=_("Type"),
        help_text=_("ISIS neighbor type (L1, L2, L1L2)"),
        null=True,
        blank=True,
    )
    snpa = models.CharField(
        max_length=50,
        verbose_name=_("SNPA"),
        help_text=_("Subnetwork Point of Attachment"),
        null=True,
        blank=True,
    )
    ietf_nsf = models.CharField(
        max_length=50,
        verbose_name=_("IETF NSF"),
        help_text=_("IETF Non-Stop Forwarding status"),
        null=True,
        blank=True,
    )

    imported_data = JSONField(
        verbose_name=_("Imported Data"),
        help_text=_("Raw data imported from device"),
        null=True,
        blank=True,
    )

    status = models.CharField(
        verbose_name=_("Status"),
        max_length=50,
        choices=ISISNeighborStatusChoices,
        default=ISISNeighborStatusChoices.STATUS_ACTIVE,
    )

    vrf = models.CharField(
        max_length=100,
        verbose_name=_("VRF"),
        help_text=_("VRF instance name"),
        default="default",
        blank=True,
    )

    area_id = models.CharField(
        max_length=100,
        verbose_name=_("Area ID"),
        help_text=_("ISIS area identifier"),
        null=True,
        blank=True,
    )

    comments = models.TextField(verbose_name=_("Comments"), blank=True)

    def get_absolute_url(self):
        return reverse(
            "plugins:netbox_cesnet_services_plugin:isisneighbor", kwargs={"pk": self.pk}
        )

    class Meta:
        verbose_name = _("ISIS Neighbor")
        verbose_name_plural = _("ISIS Neighbors")
        ordering = ["local_device", "local_interface", "remote_device"]
        unique_together = ["local_device", "local_interface", "remote_device"]

    def __str__(self):
        return f"{self.local_device} - {self.local_interface} <-> {self.remote_device} ({self.type})"

    def clean(self):
        super().clean()

        validation_errors = {}
        if self.local_interface.device.id != self.local_device.id:
            validation_errors["local_interface"] = _(
                "Interface does not belong to specified local device"
            )

        if validation_errors:
            raise ValidationError(validation_errors)

    def get_status_color(self):
        return ISISNeighborStatusChoices.colors.get(self.status)
