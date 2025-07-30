# 1. Master JSON with datetime - DONE
# 2. In memory saving and calculation - DONE
# 3. Do remaining api integration - DONE
# 4. Docs (after gave the uat prototype)
# 5. Pip upload (after gave the uat prototype)
# 6. Try to add testing (after gave the uat prototype)
# 7. Grayshade Debug logging (after gave the uat prototype)
# 8. Redis API Limit Throttler
# 9. Make uniform variable names across SDK- DONE
# 10. Add code to Github - TODO 
# 11. Broker ws connect 15 min before market open, else won't connect - Done
# 12. Change all inputs and outputs to Pydantic model to avoid any issue
# 13. Cache for mapped broker (client setting not on session db) - TODO check with Shubham sir
# 14. Check stop loss limit logic with Shubham sir TODO
# 

import os
import time
import typing
import logging
import datetime as dt
from pprint import pprint

import quantsapp


# quantsapp.set_stream_logger(level=logging.DEBUG)

# ----------------------------------------------------------------------------------------------------

def _print_header(txt: str):
    _n = os.get_terminal_size().columns
    _char = '-'
    print()
    print(_char*_n)
    print(txt.center(_n, _char))
    print(_char*_n)
    print()

# ----------------------------------------------------------------------------------------------------

# region Get Session ID

_print_header('Get Session ID')

try:
    session_id = quantsapp.Login(
        api_key='u7IoXQbITjy5992_fSSIsg',
        secret_key='5JVRwcgbA3t68wKT',
        # api_key='NUmb7KmVy2jaXy9HYJ4SJw',
        # secret_key='VNQYN0NWrQ9faK6p',
    ).login()
except quantsapp.exceptions.InvalidLoginCredentials as e:
    print(e)
    raise e
else:
    print(f"{session_id = }")

# endregion

# ----------------------------------------------------------------------------------------------------

# region Execution process

# ------------------------------------------------------

# region Get the execution object

_print_header('Connect to Execution obj')

def broker_order_update(update: quantsapp.response.BrokerOrderUpdateWsData) -> typing.Any:
    print(f"Broker Order Update received -> {update}")



qapp_execution = quantsapp.Execution(
    session_id=session_id,
    order_updates_callback=broker_order_update,  # Optional
)

print(f"Market opened = {quantsapp.MarketTimings.is_market_open()}")

quantsapp_ac_details = quantsapp.get_quantsapp_ac_details()
print(f"User details = {quantsapp_ac_details}")
# quantsapp_ac_details.AC_TYPE
# quantsapp_ac_details.USER_ID
# quantsapp_ac_details.API_KEY


# endregion

# ------------------------------------------------------

# region Listing available brokers

_print_header('List Available Brokers')

available_brokers = qapp_execution.list_available_brokers(
    # payload=quantsapp.payload.ListAvailableBrokers(
    #     name_type='str',
    # ),
)
print('Available Brokers to trade:-')  # TODO fix the code only login issue (Eg:- upstock is not allowed in code login)
pprint(available_brokers)
print()

is_choice_login_available = quantsapp.Broker.CHOICE in available_brokers['access_token_login']
is_fivepaisa_login_available = quantsapp.Broker.FIVEPAISA in available_brokers['access_token_login']
print(f"{is_choice_login_available = }")
print(f"{is_fivepaisa_login_available = }")

# endregion

# ------------------------------------------------------

# region Listing mapped broker accounts

# # TODO create a update brokers (with force resync from client)
# # TODO versioning cache not done yet!

# _print_header('List Mapped Brokers')

# try:
#     mapped_brokers = qapp_execution.list_mapped_brokers(
#         # payload=quantsapp.payload.ListMappedBrokers(
#         #     revalidate_token=False,
#         #     from_cache=True,
#         # )
#     )
# except quantsapp.exceptions.NoBrokerAccountsMapped as err:
#     print(err)
# else:
#     print('Mapped Broker:-')
#     pprint(mapped_brokers)

# # TODO add update all margins
# # TOD show the logged-in and logged out users, use update accounts as a separate api call to update validity
# # TODO add get margin for specific accounts - Sir give separate api for this

# endregion

# ------------------------------------------------------

# region Add Broker

# _print_header('Add Broker')

# # 1. DHAN
# try:
#     add_dhan_broker_resp = qapp_execution.add_broker(
#         payload=quantsapp.payload.AddBroker(
#             broker=quantsapp.Broker.DHAN,
#             login_credentials=quantsapp.payload.DhanBrokerLoginCredentials(
#                 access_token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzQ5MDA5MDk0LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMDczNTU3NyJ9.jRIEI5R4CyAJj7BSbMcm-lHXXHzIFeVsPIbIahZeF-RcqIPi0tXiH9Lm5sb26XN13mGUUvQwh0iXUiW_dXmoVQ',
#             ),
#         ),
#     )
# except quantsapp.exceptions.BrokerLoginFailed as err:
#     print(f"Dhan broker failed to add -> {err}")
# else:
#     print(f"Dhan Broker added -> {add_dhan_broker_resp = }")
# print()
# print('-' * 100)
# print()


# # 2. CHOICE
# try:
#     add_choice_broker_resp = qapp_execution.add_broker(
#         payload=quantsapp.payload.AddBroker(
#             broker=quantsapp.Broker.CHOICE,
#             login_credentials=quantsapp.payload.ChoiceBrokerLoginCredentials(
#                 mobile='9833464443',
#                 client_access_token='eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg3NUE3MzQ4NkYwNDA4NDI1NEMwNUQzNzQyRDlDQUYxRTczQkI4QzkiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJkYWU2ODc0MC02MDAwLTQ2ZmItYjQ4NS04YTA4MDVkYWYwOWEiLCJqdGkiOiIzOTUzN2RjOC1hZmQ4LTQwYjMtOGJkYi1mMWM0YjllOGYwMmQiLCJpYXQiOjE3NDQ3OTA0ODksIlVzZXJJZCI6IlgxNTMzNjQiLCJuYmYiOjE3NDQ3OTA0ODksImV4cCI6MTc0NzM4MjQ4OSwiaXNzIjoiRklOWCJ9.KxtyV38n3ZCAD8suTBX0sNwQ-0bKfb6PZ9NmWVelFZ3oig0Jat_B64S4WJiRHc3_zMahO4Dt5PI988DIvG8dy3gtBRW5LDIWDJm8Tkd7kdyrMniP1oAaUxKSjRD3qqIUWKRs7mBDz6NQI1viHKaYh10eK3OsO8vvK0EtLvuUJJIhhUHWAr-ztnvvGj6eVWZLbdSrKBR1V6d2yOGmhsazJdMmikXisVIbmn6k5VrdLkgM68Ug2DWxqC6eqLh2fteogiDoDK6cQ4bJ_puBHBZp4a3DDNe5qLAh5KCSeA4S1QcsPumRyhwVJLfqBnptJ7GPLzCnQa1TdCpaivzTryZ8EA',
#             ),
#         ),
#     )
# except quantsapp.exceptions.BrokerLoginFailed as err:
#     print(f"Choice broker failed to add -> {err}")
# else:
#     print(f"Choice Broker added -> {add_choice_broker_resp = }")
# print()
# print('-' * 100)
# print()


# endregion

# ------------------------------------------------------

# region Delete Broker

# _print_header('Delete Broker')

# # TODO on add or delete, update the local mapped brokers data

# try:
#     broker_delete_resp = qapp_execution.delete_broker(
#         payload=quantsapp.payload.DeleteBroker(
#             broker_client=quantsapp.BrokerClient(
#                 broker=quantsapp.Broker.CHOICE,
#                 client_id='X153364',
#             )
#         )
#     )
# except quantsapp.exceptions.BrokerDeletionFailed as err:
#     print(f"Broker failed to delete -> {err}")
# else:
#     print(f"Broker deleted -> {broker_delete_resp = }")

# endregion

# ------------------------------------------------------

# region Listing Orders

# _print_header('List Orders')

# get_orders_resp = qapp_execution.get_orders(
#     payload=quantsapp.payload.ListOrders(
#         broker_client=quantsapp.payload.BrokerClient(
#             # broker=quantsapp.Broker.DHAN,
#             # client_id='1100735577',
#             broker=quantsapp.Broker.MSTOCK,
#             client_id='MA6232931',
#         ),
#         ascending=False,
#         from_cache=True,
#     ),
# )
# print('Orders Listing:-')
# for idx, order in enumerate(get_orders_resp):
#     print(idx)
#     pprint(order)

# # TODO add a separate method to update all broker orders from API
# # TODO add ref_id api orders listing
# # {"status": "1", "msg": "success", "has_failed": true, "q_ref_id": 21, "routeKey": "broker_orders", "custom_key": "place_order", "ws_msg_type": "qapp_api_gateway_options_success_api_request"}

# endregion

# ------------------------------------------------------

# region Place Orders

# _print_header('Place Orders')

# print('Place Order:-')
# place_order_resp = qapp_execution.place_order(
#     payload=quantsapp.payload.PlaceOrder(
#         broker_accounts=[
#             quantsapp.payload.PlaceOrderBrokerAccounts(
#                 # broker_client=quantsapp.payload.BrokerClient(
#                 #     broker=quantsapp.Broker.MSTOCK,
#                 #     client_id='MA6232931',
#                 # ),
#                 # broker_client=quantsapp.payload.BrokerClient(
#                 #     broker=quantsapp.Broker.CHOICE,
#                 #     client_id='X153364',
#                 # ),
#                 broker_client=quantsapp.payload.BrokerClient(
#                     broker=quantsapp.Broker.DHAN,
#                     client_id='1100735577',
#                 ),
#                 lot_multiplier=1,
#             ),
#         ],
#         exchange=quantsapp.Exchange.NSE_FNO,
#         product=quantsapp.OrderProductType.NORMAL_ORDER,
#         # order_type=quantsapp.OrderType.STOP_LOSS_LIMIT,
#         order_type=quantsapp.OrderType.MARKET,
#         validity=quantsapp.OrderValidity.DAY,
#         legs=[
#             quantsapp.payload.PlaceOrderLeg(
#                 qty=75,
#                 price=5.1,
#                 instrument=quantsapp.Instrument(
#                     symbol='NIFTY',
#                     expiry=dt.datetime(year=2025, month=5, day=22),
#                     instrument_type=quantsapp.InstrumentType.CALL,
#                     strike=25350,  # Only for call or put options
#                 ),
#                 transaction_type=quantsapp.OrderTransactionType.BUY,
#                 # stop_price=5.4,
#             ),
#         ],
#     ),
# )
# pprint(place_order_resp)

# # TODO use order list by ref id to get further details
# # if possible store the ref id on the orders local backup for any future reference


# endregion

# ------------------------------------------------------

# region Modify Order

# _print_header('Modify Order')

# modify_order_resp = qapp_execution.modify_order(
#     order=quantsapp.payload.ModifyOrder(
#         broker_client=quantsapp.payload.BrokerClient(
#             broker=quantsapp.Broker.MSTOCK,
#             client_id='MA6232931',
#         ),
#         b_orderid='33522505191353',
#         e_orderid='1200000030766929',
#         qty=75,
#         price=0.75,
#     ),
# )
# print('Modify Orders:-')
# pprint(modify_order_resp)


# endregion

# ------------------------------------------------------

# region Cancel specific Orders

# _print_header('Cancel Specific Orders')

# cancel_orders_resp = qapp_execution.cancel_orders(
#     payload=quantsapp.payload.CancelOrders(
#         orders=[
#             quantsapp.payload.CancelIndividualBrokerOrder(
#                 broker_client=quantsapp.payload.BrokerClient(
#                     broker=quantsapp.Broker.MSTOCK,
#                     client_id='MA6232931',
#                 ),
#                 order_ids=[
#                     quantsapp.payload.CancelOrderIds(
#                         b_orderid='32222505134820',
#                         e_orderid='1600000193384106',
#                     ),
#                 ],
#             ),
#             # quantsapp.payload.CancelBrokerOrder(
#             #     broker_client=quantsapp.payload.BrokerClient(
#             #         broker=quantsapp.Broker.MSTOCK,
#             #         client_id='MA6232931',
#             #     ),
#             #     order_ids=[
#             #         quantsapp.payload.CancelOrderIds(
#             #             b_orderid='32222505134820',
#             #             e_orderid='1600000193384106',
#             #         ),
#             #     ],
#             # ),
#         ],
#     )
# )
# print('Cancel Orders:-')
# pprint(cancel_orders_resp)

# endregion

# ------------------------------------------------------

# region Cancel All Orders related to one broker account

# _print_header('Cancel All Orders')

# cancel_all_orders_resp = qapp_execution.cancel_all_orders(
#     payload=quantsapp.payload.CancelAllOrders(
#         broker_client=quantsapp.payload.BrokerClient(
#             broker=quantsapp.Broker.MSTOCK,
#             client_id='MA6232931',
#         ),
#     )
# )
# print('Cancel All Orders:-')
# pprint(cancel_all_orders_resp)

# endregion

# ------------------------------------------------------

# region Get Positions

# _print_header('Get Positions')

# get_positions_resp = qapp_execution.get_positions(
#     payload=quantsapp.payload.GetPositions(
#         broker_clients=[
#             quantsapp.payload.BrokerClient(
#                 broker=quantsapp.Broker.MSTOCK,
#                 client_id='MA6232931',
#             ),
#             quantsapp.payload.BrokerClient(
#                 broker=quantsapp.Broker.FIVEPAISA,
#                 client_id='50477264',
#             ),
#             quantsapp.payload.BrokerClient(
#                 broker=quantsapp.Broker.DHAN,
#                 client_id='1100735577',
#             ),
#         ],
#     ),
# )
# print('Get Positions:-')
# pprint(get_positions_resp)

# endregion

# ------------------------------------------------------

# region Get Positions (Combined)

# TODO add option to give direct data and iterator

# _print_header('Get Positions (Combined)')

# get_positions_consolidated_resp = qapp_execution.get_positions_combined(
#     payload=quantsapp.payload.GetPositions(
#         broker_clients=[
#             quantsapp.payload.BrokerClient(
#                 broker=quantsapp.Broker.MSTOCK,
#                 client_id='MA6232931',
#             ),
#             quantsapp.payload.BrokerClient(
#                 broker=quantsapp.Broker.FIVEPAISA,
#                 client_id='50477264',
#             ),
#         ],
#     ),
# )
# print('Get Positions (Combined):-')
# print(list(get_positions_consolidated_resp))
# # for position in get_positions_consolidated_resp:
# #     pprint(position)

# endregion

# ------------------------------------------------------

# region Get Order api log

_print_header('Get Order API log')


get_orders_resp = qapp_execution.get_orders(
    payload=quantsapp.payload.ListOrders(
        broker_client=quantsapp.payload.BrokerClient(
            # broker=quantsapp.Broker.DHAN,
            # client_id='1100735577',
            broker=quantsapp.Broker.MSTOCK,
            client_id='MA6232931',
        ),
        ascending=False,
        from_cache=True,
    ),
)
print('Orders Listing:-')
for idx, order in enumerate(get_orders_resp):
    print(idx)
    pprint(order)

    get_order_api_resp = qapp_execution.get_order_api_log(
        payload=quantsapp.payload.GetOrderLogs(
            broker_client=order['broker_client'],
            instrument=order['instrument'],
            q_usec=order['q_usec'],
        )
    )
    print('Get Order Logs:-')
    for order_log in get_order_api_resp:
        pprint(order_log)

# endregion

# ------------------------------------------------------

# region Get Broker Websocket Connection Status

# _print_header('Get Broker Websocket Connection Status')

# get_broker_ws_conn_status_resp = qapp_execution.get_broker_websocket_conn_status(
#     quantsapp.payload.GetBrokerWebsocketConnectionStatus(
#         broker_client=quantsapp.payload.BrokerClient(
#             broker=quantsapp.Broker.MSTOCK,
#             client_id='MA6232931',
#         ),
#     ),
# )
# print('Get Broker Websocket Connection Status:-')
# pprint(get_broker_ws_conn_status_resp)

# endregion

# ------------------------------------------------------

# region Get Broker Websocket Re-Connect

# _print_header('Get Broker Websocket Re-Connection')

# broker_ws_re_conn_resp = qapp_execution.broker_websocket_reconnect(
#     quantsapp.payload.BrokerWebsocketReConnect(
#         broker_client=quantsapp.payload.BrokerClient(
#             broker=quantsapp.Broker.MSTOCK,
#             client_id='MA6232931',
#         ),
#     ),
# )
# print('Get Broker Websocket Connection Status:-')
# pprint(broker_ws_re_conn_resp)

# endregion

# ------------------------------------------------------

# region Order Book Update

# _print_header('Order Book Update')

# order_book_update_resp = qapp_execution.update_order_book(
#     quantsapp.payload.UpdateOrderBook(
#         broker_client=quantsapp.payload.BrokerClient(
#             broker=quantsapp.Broker.MSTOCK,
#             client_id='MA6232931',
#         ),
#         update_on='positions',
#     ),
# )
# print('Order Book Update:-')
# pprint(order_book_update_resp)

# endregion

# ------------------------------------------------------

# TODO square off in phase 2


# endregion

# ----------------------------------------------------------------------------------------------------
# import quantsapp._logger
# import quantsapp._websocket._utils

# while True:
#     _ws_status = quantsapp._websocket._utils.sdk_websocket_status()
#     quantsapp._logger.qapp_logger.critical(f"{_ws_status = }")
#     if _ws_status['options_main_ws'] is False:
#         print(f"{qapp_execution.list_mapped_brokers() = }")
#     time.sleep(60)

# time.sleep(600)

# print(quantsapp.execution._cache.mapped_brokers)
# print(quantsapp.execution._cache.orders)


# TODO remove expired orders


# TODO Quantsapp Code on public domain
# https://github.com/mohitaneja44/GUI-Quanstapp-using-Tkinter-Library
# https://github.com/M0rfes/quantsapp
# https://github.com/TechfaneTechnologies/QtsApp/tree/main
# https://github.com/sonibind1307/QuantsApp

# https://github.com/mirajgodha/options?tab=readme-ov-file
    # Consolidated total loss and profit across all option strategies across all borkers Charts of profit and loss of total PnL Charts of profit and loss of each stock option strategy -- This is the very important feature i was looking for and was not available any where including Sensibull and Quantsapp.