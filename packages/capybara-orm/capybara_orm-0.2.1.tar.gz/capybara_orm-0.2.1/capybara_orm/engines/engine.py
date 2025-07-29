from typing import Any

from cognite.client import CogniteClient

from capybara_orm.cognite_adapters import CogniteAdapter
from capybara_orm.config import DataModelId
from capybara_orm.models import PaginatedResult, TViewInstance, ValidationMode
from capybara_orm.statements import Statement


class Engine:
    def __init__(
        self,
        cognite_client: CogniteClient,
        data_model_id: DataModelId,
    ):
        self._cognite_adapter = CogniteAdapter(cognite_client, data_model_id)

    def query(
        self,
        statement: Statement[TViewInstance],
        validation_mode: ValidationMode = "raiseOnError",
    ) -> PaginatedResult[TViewInstance]:
        data, next_cursor = self._cognite_adapter.query(statement, False)

        return PaginatedResult(
            data=self._validate_data(statement.entity, data, validation_mode),
            next_cursor=next_cursor,
            has_next_page=next_cursor is not None,
        )

    def query_all_pages(
        self,
        statement: Statement[TViewInstance],
        validation_mode: ValidationMode = "raiseOnError",
    ) -> list[TViewInstance]:
        if statement.cursor_:
            raise ValueError("Cursor should be none when querying all pages")

        data, _ = self._cognite_adapter.query(statement, True)

        return self._validate_data(statement.entity, data, validation_mode)

    def _validate_data(
        self,
        entity: type[TViewInstance],
        data: list[dict[str, Any]],
        validation_mode: ValidationMode,
    ) -> list[TViewInstance]:
        result: list[TViewInstance] = []
        for item in data:
            try:
                result.append(entity.model_validate(item))
            except Exception:
                if validation_mode == "ignoreOnError":
                    continue
                raise
        return result
