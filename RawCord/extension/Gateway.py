import websocket
import json
import threading, asyncio
import time


ws = websocket.WebSocket()
ws.connect('wss://gateway.discord.gg/?v=6&encoding=json')

def Connect_Gateway(token,show_event):
    def send_json_request(ws, request):
        ws.send(json.dumps(request))

    def recieve_json_response(ws):
        response = ws.recv()
        if response:
            return json.loads(response)

    def heartbeat(interval, ws):
        if show_event==True:    print('Heartbeat Begin')
        while True:
            time.sleep(interval)
            heartbeatJSON = {
                "op": 1,
                "d": "null"
            }
            send_json_request(ws, heartbeatJSON)
            if show_event==True:    print("Heartbeat Rent")

    event = recieve_json_response(ws)

    heartbeat_interval = event['d']['heartbeat_interval'] / 1000
    threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

    payload = {
        'op': 2,
        "d": {
            "token": token,
            "properties": {
                "$os": "windows",
                "$browser": "chrome",
                "$device": 'pc'
            }
        }
    }
    send_json_request(ws, payload)

async def listen(show_event):
    async def recieve_json_response(ws):
        response = ws.recv()
        if response:
            return json.loads(response)

    while True:
        # print("\n\t\tWaiting Event\n")
        event = await recieve_json_response(ws)
        # print(f"\n\t\tReceived Event\n")

        try:

            op_code = event['op']
            if op_code == 11:
                if show_event==True:    print('Heartbeat Received')
            # API Injection
            if event["t"] == "READY":
                if show_event==True:    print("Connected to Gateway...")
            return event["t"],event["d"]
        except Exception as e:
            print(f"Exception Caught and passed: {e}")

from .Channel import Message
async def GatewayStart(token,header,commands,show_event=False):
    Connect_Gateway(token,show_event=show_event)
    while True:
        event = await asyncio.create_task(listen(show_event=show_event))
        if show_event==True:    print("Event Type>>>",event[0])
        if event[0] == 'MESSAGE_CREATE':
            for i in commands:
                commmand_name = i["command_name"]
                if commmand_name == event[1]["content"].split()[0]:
                    i["function"](Message(**{**event[1],**{"__client__":header}}),*event[1]["content"].split()[1:])
