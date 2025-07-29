import strawberry_django
from netbox.graphql.filter_mixins import BaseFilterMixin

from netbox_cesnet_services_plugin.filtersets import (
    BGPConnectionFilterSet,
    LLDPNeighborFilterSet,
    LLDPNeighborLeafFilterSet,
)
from netbox_cesnet_services_plugin.models import (
    BGPConnection,
    LLDPNeighbor,
    LLDPNeighborLeaf,
)


@strawberry_django.filter(LLDPNeighbor, lookups=True)
class LLDPNeigborFilter(BaseFilterMixin):
    class Meta:
        filterset_class = LLDPNeighborFilterSet


@strawberry_django.filter(LLDPNeighborLeaf, lookups=True)
class LLDPNeigborLeafFilter(BaseFilterMixin):
    class Meta:
        filterset_class = LLDPNeighborLeafFilterSet


@strawberry_django.filter(BGPConnection, lookups=True)
class BGPConnectionFilter(BaseFilterMixin):
    class Meta:
        filterset_class = BGPConnectionFilterSet
