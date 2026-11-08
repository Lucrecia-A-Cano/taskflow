import websocket

ws = websocket.create_connection("ws://127.0.0.1:8000/ws/projects/1/")
ws.send('{"mensaje": "hola desde el cliente"}')
print(ws.recv())
ws.close()