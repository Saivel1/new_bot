from granian import Granian
from granian.constants import Loops, Interfaces

if __name__ == "__main__":
    Granian(
        "app.main:app",
        address="127.0.0.1",
        port=8000,
        interface=Interfaces.ASGI,  # не "asgi", а Interfaces.ASGI
        workers=14,
        loop=Loops.uvloop,          # не "uvloop", а Loops.uvloop
    ).serve()