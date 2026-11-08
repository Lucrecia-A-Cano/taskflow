import websocket

try:
    ws = websocket.create_connection("ws://127.0.0.1:8000/ws/projects/999/")
    print("Se conectó (esto no debería pasar)")
    ws.close()
except websocket.WebSocketBadStatusException as e:
    print("Conexión rechazada:", e)