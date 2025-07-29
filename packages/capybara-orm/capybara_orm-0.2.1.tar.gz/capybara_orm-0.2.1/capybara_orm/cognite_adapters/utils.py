from typing import Literal

from cognite.client.data_classes.data_modeling import (
    View,
    ViewId,
)

from capybara_orm.models import TViewInstance

NODE_PROPERTIES = {"externalId", "space", "createdTime", "deletedTime"}
INTANCE_TYPE = Literal["node", "edge"]


def get_property_ref(
    property: str, view: View | ViewId, instance_type: INTANCE_TYPE = "node"
) -> tuple[str, str, str] | tuple[str, str]:
    return (
        view.as_property_ref(property)
        if property not in NODE_PROPERTIES
        else (instance_type, property)
    )


def get_cognite_instance_ids(
    instance_ids: list[TViewInstance],
) -> list[dict[str, str]]:
    return [
        get_cognite_instance_id(instance_id) for instance_id in instance_ids
    ]


def get_cognite_instance_id(instance_id: TViewInstance) -> dict[str, str]:
    return {"space": instance_id.space, "externalId": instance_id.external_id}
