import asyncio
import traceback
import time
import json
import uuid
import sys
import os
import importlib
import random
import websockets
# from websockets.sync.client import connect

# from mako.lookup import TemplateLookup
# from mako.template import Template

project = "sm"
websocket_url = "wss://ws.gluer.io/server"
session_id = f'ws-{str(uuid.uuid4())}'
heartbeat_interval = 5
retry_delay = 5
ws = None

imported_files = {}
methods_map = {}


def set_project(p):
    global project
    project = p


def set_websocket_url(url):
    global websocket_url
    websocket_url = url


# async def start():
    # print("Start")
    # sub_server()
    # await asyncio.get_event_loop().run_until_complete(start_ws())
    # await asyncio.to_thread(queue())

def build_header_from_message(job):
    smh = job["smh"].split(":")
    return {"d": smh[0], "session_id": smh[1].split('>'), "project": smh[2], "plugin": smh[3] or "", "action": smh[4] or ""}


def build_message_from_header(header):
    return f'{header["d"]}:{">".join(header["session_id"])}>{session_id}:{header["project"]}:{header["plugin"] or ""}:{header["action"] or ""}'


async def on_message(wsapp, message):
    global methods_map
    print("MethodsMap",methods_map)

    job = json.loads(message)
    header = build_header_from_message(job)
    job["smh"] = build_message_from_header(header)
    print("header")
    print(header)
    try:
        mtd = None
        print(header["plugin"])
        print(methods_map)
        print(methods_map[header["plugin"]])
        if header["plugin"] in methods_map and header["action"] in methods_map[header["plugin"]]:
            mtd = methods_map[header["plugin"]][header["action"]]
        elif header["plugin"] in imported_files:
            if hasattr(imported_files[header["plugin"]], header["action"]):
                mtd = getattr(
                    imported_files[header["plugin"]], header["action"])
        if mtd:
            ret = None
            if "data" in job:
                ret = mtd(job["data"])
            else:
                ret = mtd(job)
            # print("Pre Process")
            process_dict(ret)
            # print(ret)
            # print("Post Process")
            job["data"] = ret
            # if "htmx" in job:
            #     # print("HTMX found")
            #     try:
            #         act_template = lookup.get_template(
            #             f'{header["plugin"]}/{header["action"]}.mako')
            #         # print("act_template")
            #         # print(act_template)
            #         if act_template:
            #             # print("Template Found")
            #             # print(ret)
            #             # print(job["data"])
            #             job["data"] = act_template.render(data=ret)
            #             # print(job["data"])
            #     except Exception as error:
            #         print(error)
        else:
            job["data"] = {
                "error": f"no server actions found for {header['plugin']}:{header['action']}"
            }
    except Exception as error:
        print("ERROR")
        print(traceback.format_exc())
        # print(error)
        error_handler(job, error)
    # if "ws" in job:

    job["smh"] = "<" + job["smh"][1:]
    # print("Sending job back")
    # print(job["data"])
    # job["d"] = "<"
    await wsapp.send(json.dumps(job))


def on_open(ws):
    print("Opened")
    job = f'{{"smh":"+:{session_id}:{project}","channel":"{session_id},{project}"}}'
    ws.send(job)


def on_error(ws, error):
    print("Error")
    print(ws)
    print(error)
    # job = f'{{"smh":"+:{session_id}:{project}","channel":"{session_id},{project}"}}'
    # ws.send(job)


async def connect():
    global ws
    while True:
            try:
                print(f"Connecting to {websocket_url}...")
                async with websockets.connect(f'{websocket_url}/{project}/{session_id}') as websocket:
                    print(f"Connected to {websocket_url}")

                    # job = f'{{"smh":"+:{session_id}:{project}","channel":"{session_id},{project}"}}'
                    # await websocket.send(job)
                    # print(f"Sent custom message: {custom_message}")

                    # Send a greeting message after successful connection
                    # await websocket.send("Hello, WebSocket server!")

                    while True:
                        try:
                            message = await websocket.recv()
                            if message is None:
                                print("Received None, connection may be closed. Reconnecting...")
                                break # Break the inner loop to reconnect
                            print(f"Received: {message}")
                            await on_message(websocket, message)
                            # You can add your message handling logic here.
                            # For example, you might want to check for specific messages
                            # and respond accordingly.  Or, process the data.
                        except websockets.ConnectionClosedError:
                            print("Connection closed unexpectedly. Reconnecting...")
                            break # Break the inner loop to reconnect
                        except websockets.ConnectionClosedOK:
                            print("Connection closed normally. Reconnecting...")
                            break
                        except Exception as e:
                            print(f"Error receiving message: {e}. Reconnecting...")
                            break # Exit inner loop, try to reconnect
            except ConnectionRefusedError:
                print("Connection refused. Server may not be running or is busy.")
                break # Don't reconnect, since the server refused.  Exit the outer loop
            except OSError as e:
                if e.errno in (54, 61, 64): # Connection reset, connection refused, host down
                    print(f"Network error: {e}.  Attempting to reconnect...")
                else:
                    print(f"OS error: {e}.  Reconnecting...")
            except Exception as e:
                print(f"Error: {e}")
                print("An unexpected error occurred.  Check network, server, and code.")
                #  Consider different strategies here.  For example, you might
                #  want to exit after a few unknown errors, or perhaps
                #  log the error to a file.  For this example, we'll just
                #  keep trying to reconnect.
            # Use exponential backoff to avoid overwhelming the server with rapid reconnect attempts.
            delay = random.uniform(1, 5)  # Introduce some random jitter
            print(f"Reconnecting in {delay:.2f} seconds...")
            await asyncio.sleep(delay)    
    # with connect(websocket_url) as websocket:
        # ws = websocket
        # websocket.send("Hello world!")
        # message = websocket.recv()
        # print(f"Received: {message}")    
    # with connect(websocket_url) as websocket:
    # ws = websocket
    # message = websocket.recv()
    # print(f"Received: {message}")
    # websocket.enableTrace(false)
    # ws = websocket.WebSocketApp(
    #     websocket_url, on_message=on_message, on_open=on_open, on_error=on_error)
    # ws.run_forever(dispatcher=rel, ping_interval=60, ping_timeout=10, reconnect=5,
    #                ping_payload="This is an optional ping payload")

    # rel.dispatch()


lookup = None


def import_directories(path):
    global lookup
    files = os.listdir(path)
    # print(files)
    sys.path.append(path)
    for file in files:
        if file.endswith(".py"):
            try:
                file = file[:-3]
                imported_files.setdefault(file, importlib.import_module(file))
                print(f"Imported {file}")
            except ImportError as err:
                print('Error:', err)
    # lookup = TemplateLookup(directories=[f'{path}/templates'])


def add_method(plugin, action, fn):
    global methods_map
    print("Adding method", plugin, action)
    methods_map.setdefault(plugin, {})
    methods_map[plugin].setdefault(action, fn)

def register_plugin(plugin_name: str, fn_name: str, fn: callable):
    global methods_map    
    """
    Registers a function under a given plugin name.

    Args:
        plugin_name: The name of the plugin.
        fn_name: The name of the function to register.
        fn: The function object.
    """
    fn_map = {fn_name: fn}
    if plugin_name not in methods_map:
        methods_map[plugin_name] = {}
    methods_map[plugin_name].update(fn_map)

def register_object(plugin_name: str, obj: object):
    """
    Registers all methods of an object under a given plugin name.

    Args:
        plugin_name: The name of the plugin.
        obj: The object whose methods will be registered.
    """
    methods = [
        method_name for method_name in dir(obj)
        if callable(getattr(obj, method_name)) and not method_name.startswith("__")
    ]
    print("methods",methods)
    for method_name in methods:
        method = getattr(obj, method_name)
        register_plugin(plugin_name, method_name, method)
    # print('Methods', methods)

def error_handler(job, error):
    job["data"] = {"error": {
        "message": error.content[0]['message'], "code": error.content[0]['errorCode']}}


def set_error_handler(fn):
    global error_handler
    error_handler = fn


def process_dict(data):
    for key, value in data.items():
        # Check if the value has a 'model_dump' method
        if hasattr(value, "model_dump") and callable(getattr(value, "model_dump")):
            # Call model_dump() if it's available and callable
            data[key] = value.model_dump()
        elif isinstance(value, dict):
            # If the value is a nested dictionary, recursively process it
            process_dict(value)
        elif isinstance(value, list):
            # If the value is a list, process each item
            for i, item in enumerate(value):
                if hasattr(item, "model_dump") and callable(getattr(item, "model_dump")):
                    value[i] = item.model_dump()
                elif isinstance(item, dict):
                    process_dict(item)

def start():
    asyncio.run(connect())
    # """
    # Main function to start the WebSocket client.  Allows user to specify the URI.
    # """
    # await start()

# if __name__ == '__main__':
    # asyncio.run(main())
    # print('start')
    # redis.set_user("Teste")
#     try:
#         # loop = asyncio.get_event_loop()
#         # loop.run_until_complete(start())
#         asyncio.run(start())
#     except Exception as error:
#         print(error)
#         traceback.print_exc()
#     # asyncio.run(start())
