
# async def get_redis_client():
#     r = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
#     try:
#         yield r
#     finally:
#         await r.close()


# async def get_csv_repository() -> CsvFileRepository:
#     return CsvFileRepository()
#
#
# async def get_chat_repository(
#     redis: Redis = Depends(get_redis_client)
# ) -> ChatRepository:
#     return ChatRepository(redis)


# async def play_bot_service(repository: ChatRepository = Depends(get_chat_repository)):
#     return BotService(repository)


# async def play_chat_service(repository: ChatRepository = Depends(get_chat_repository)):
#     return ChatService(repository)


# async def play_csv_service(repository: CsvFileRepository = Depends(get_csv_repository)):
#     return CsvService(repository)

 # добавить зависимсоть httpx асинк клиент она в двух сервисах

