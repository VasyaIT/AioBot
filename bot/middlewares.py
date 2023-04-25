# import asyncio
#
# from aiogram import Dispatcher, types
# from aiogram.dispatcher.middlewares import BaseMiddleware
# from aiogram.utils.exceptions import Throttled
# from aiogram.dispatcher.handler import CancelHandler, current_handler
#
#
# class ThrottlingMiddleware(BaseMiddleware):
#     def __init__(self, limit: int = 5):
#         BaseMiddleware.__init__(self)
#         self.rate_limit = limit
#
#     async def on_process_message(self, message: types.Message, data: dict):
#         dp = Dispatcher.get_current()
#
#         try:
#             await dp.throttle(key='antiflood', rate=self.rate_limit)
#         except Throttled as _t:
#             raise CancelHandler()
