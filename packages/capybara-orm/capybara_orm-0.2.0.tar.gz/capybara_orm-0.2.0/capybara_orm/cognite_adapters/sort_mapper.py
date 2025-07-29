from cognite.client.data_classes.data_modeling import InstanceSort, View

from capybara_orm.cognite_adapters.utils import get_property_ref
from capybara_orm.constants import SORT_DIRECTION
from capybara_orm.statements.expressions import Column


class SortMapper:
    def map(
        self,
        sort_clauses: list[tuple[Column, SORT_DIRECTION]],
        root_view: View,
    ) -> list[InstanceSort]:
        return [
            InstanceSort(
                property=get_property_ref(column.property, root_view),
                direction=direction,
                nulls_first=direction == "descending",
            )
            for column, direction in sort_clauses
        ]
