from typing import Sequence

from fastapi.encoders import jsonable_encoder
from sqlalchemy import Delete, select, update


#
# class ChatRepository(BaseDatabaseRepository):
#     async def save_crossroad(self, record: CrossroadUploadSchema) -> CrossroadSchema:
#         new_crossroad = Crossroad(**record.model_dump())
#         self._session.add(new_crossroad)
#         await self._session.flush()
#
#         return CrossroadSchema.model_validate(new_crossroad)
#
#     async def get_crossroad_by_id(self, crossroad_id: int) -> CrossroadSchema | None:
#         crossroad = await self._session.get(Crossroad, crossroad_id)
#
#         return CrossroadSchema.model_validate(crossroad) if crossroad else None
#
#     async def get_crossroads_data(self) -> Sequence[GetCrossroadDataSchema]:
#         query = select(Crossroad, MainStreet).join(MainStreet, Crossroad.main_street_id == MainStreet.id)
#         result_query = await self._session.execute(query)
#
#         scalars = result_query.fetchmany()
#
#         return [
#             GetCrossroadDataSchema.model_validate(jsonable_encoder(main_street) | jsonable_encoder(crossroad))
#             for crossroad, main_street in scalars
#         ]
#
#     async def get_crossroads_by_main_street_ids(self, main_street_ids: Sequence[int]) -> Sequence[CrossroadSchema]:
#         query = select(Crossroad).filter(Crossroad.main_street_id.in_(main_street_ids))
#         result_query = await self._session.execute(query)
#
#         return [CrossroadSchema.model_validate(crossroad) for crossroad in result_query.scalars().all()]
#
#     async def update_crossroads(self, crossroads: Sequence[CrossroadUpdateSchema]) -> None:
#         updates = [crossroad.model_dump() for crossroad in crossroads]
#         await self._session.execute(update(Crossroad), updates)
#
#         await self._session.flush()
#
#     async def delete_all(self) -> None:
#         await self._session.execute(Delete(Crossroad))
#         await self._session.flush()
