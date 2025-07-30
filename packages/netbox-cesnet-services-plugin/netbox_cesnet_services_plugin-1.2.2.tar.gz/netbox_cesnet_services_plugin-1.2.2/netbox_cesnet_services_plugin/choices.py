from utilities.choices import ChoiceSet
from django.utils.translation import gettext_lazy as _


class LLDPNeigborStatusChoices(ChoiceSet):

    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"

    CHOICES = (
        (STATUS_ACTIVE, _("Active"), "green"),
        (STATUS_INACTIVE, _("Inactive"), "gray"),
    )


class LLDPNeigborStatusDetailChoices(ChoiceSet):
    """
    Fully connected - both sides found in LLDP data
    OneWay - previous state was fully connected, but one side is not in LLDP data -> after N days switch to unconfirmed or inactive
    Unconfirmed - one side is not in LLDP data, but the other side is. Both sides are in the Netbox.
    None - no detail needed, primary status is inactive. No side is in LLDP data.
    """

    STATUS_ACTIVE = "fully_connected"
    STATUS_UNCONFIRMED = "unconfirmed"
    STATUS_ONEWAY = "oneway"
    STATUS_NONE = "none"

    CHOICES = (
        (STATUS_ACTIVE, _("Active"), "green"),
        (STATUS_UNCONFIRMED, _("Unconfirmed"), "yellow"),
        (STATUS_ONEWAY, _("Oneway"), "orange"),
        (STATUS_NONE, _("None"), "gray"),
    )
