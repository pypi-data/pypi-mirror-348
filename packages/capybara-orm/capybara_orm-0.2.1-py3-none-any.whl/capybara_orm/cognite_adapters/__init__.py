from typing import Any

from cognite.client import CogniteClient

from capybara_orm.cognite_adapters.optimizer import QueryOptimizer
from capybara_orm.config import DataModelId
from capybara_orm.models import TViewInstance
from capybara_orm.statements import Statement

from .query_mapper import QueryMapper
from .query_result_mapper import (
    QueryResultMapper,
)
from .view_mapper import ViewMapper


class CogniteAdapter:
    def __init__(
        self, cognite_client: CogniteClient, data_model_id: DataModelId
    ):
        self._cognite_client = cognite_client

        dm = cognite_client.data_modeling.data_models.retrieve(
            ids=data_model_id.as_tuple(),
            inline_views=True,
        ).latest_version()
        view_mapper = ViewMapper(dm.views)
        self._query_mapper = QueryMapper(view_mapper)
        self._result_mapper = QueryResultMapper(view_mapper)
        self._optmizer = QueryOptimizer(cognite_client)

    def query(
        self, statement: Statement[TViewInstance], all_pages: bool
    ) -> tuple[list[dict[str, Any]], str | None]:
        self._optmizer.optimize(statement)
        cognite_query = self._query_mapper.map(statement)
        view_external_id = statement.entity.get_view_external_id()

        data: list[dict[str, Any]] = []
        while True:
            query_result = self._cognite_client.data_modeling.instances.query(
                cognite_query
            )

            page_result, next_cursor = self._result_mapper.map_nodes(
                view_external_id, query_result
            )

            data.extend(page_result)

            last_page = len(page_result) < statement.limit_ or not next_cursor
            next_cursor_ = None if last_page else next_cursor
            cognite_query.cursors = {view_external_id: next_cursor_}

            if not all_pages or last_page:
                return data, next_cursor
