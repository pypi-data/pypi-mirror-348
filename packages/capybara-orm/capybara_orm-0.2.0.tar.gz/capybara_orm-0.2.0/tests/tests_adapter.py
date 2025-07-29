import datetime
import json
from typing import Annotated

from pydantic import Field

from capybara_orm import ViewInstance, col, select

from .hubs import generate_engine


class DescribableEntity(ViewInstance):
    name: str | None = None
    description: str | None = None


class ReportingSite(DescribableEntity):
    time_zone: DescribableEntity | None = None


class EventDetail(ViewInstance):
    ref_metric_code: DescribableEntity | None = None
    ref_event_code: DescribableEntity | None = None
    ref_sub_category_l1: DescribableEntity | None = None
    ref_sub_category_l2: DescribableEntity | None = None
    ref_sub_category_l3: DescribableEntity | None = None
    ref_sub_category_l4: DescribableEntity | None = None
    ref_sub_category_l5: DescribableEntity | None = None
    ref_equipment: DescribableEntity | None = None
    ref_discipline: DescribableEntity | None = None


class Event(ViewInstance):
    __view_external_id__ = "OEEEvent"
    __instance_spaces_prefix__ = "OEE-"

    start_date_time: datetime.datetime | None = None
    ref_site: ReportingSite | None = None
    ref_unit: DescribableEntity | None = None
    ref_reporting_line: DescribableEntity | None = None
    ref_reporting_location: DescribableEntity | None = None
    ref_product: DescribableEntity | None = None
    ref_material: DescribableEntity | None = None
    ref_process_type: DescribableEntity | None = None
    ref_oee_event_detail: Annotated[
        list[EventDetail],
        Field(default_factory=list, alias="refOEEEventDetail"),
    ]


adapter = generate_engine()

filter = col(Event.start_date_time).gt_(datetime.datetime(2025, 3, 1)) & col(
    Event.ref_site
).nested_(DescribableEntity.external_id == "STS-CLK")


statement = select(Event).limit(50).where(filter)

result = [
    item.model_dump(mode="json") for item in adapter.query_all_pages(statement)
]
print(len(result))
json.dump(
    result,
    open("test.json", "w"),
)
