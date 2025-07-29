from cognite.client import CogniteClient

from capybara_orm.config import DataModelId
from capybara_orm.models import PaginatedResult, TViewInstance, ValidationMode
from capybara_orm.statements import Statement
from capybara_orm.utils import run_async

from .engine import Engine


class AsyncEngine:
    def __init__(
        self,
        cognite_client: CogniteClient,
        data_model_id: DataModelId,
    ):
        self._engine = Engine(cognite_client, data_model_id)

    async def query_async(
        self,
        statement: Statement[TViewInstance],
        validation_mode: ValidationMode = "raiseOnError",
    ) -> PaginatedResult[TViewInstance]:
        return await run_async(self._engine.query, statement, validation_mode)

    async def query_all_pages_async(
        self,
        statement: Statement[TViewInstance],
        validation_mode: ValidationMode = "raiseOnError",
    ) -> list[TViewInstance]:
        return await run_async(
            self._engine.query_all_pages, statement, validation_mode
        )
