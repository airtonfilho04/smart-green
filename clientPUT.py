import logging
import asyncio
import Adafruit_DHT
import RPi.GPIO as GPIO
import time

from aiocoap import *

class Sensor:
    def __init__(self, pino=4):
        self.pino = pino
        self.sensor = Adafruit_DHT.DHT11
        self.temp = None
        self.umid = None
        GPIO.setmode(GPIO.BOARD)

    def lerDados():
        self.umid, self.temp = Adafruit_DHT.read_retry(self.sensor, self.pino)
        if (self.umid is not None and self.temp is not None):
            print("Leitura realizada com sucesso\n")
        else:
            print("Erro na leitura!\n")
        return self.umid, self.temp    

logging.basicConfig(level=logging.INFO)

async def main():
    """Perform a single PUT request to localhost on the default port, URI
    "/other/block". The request is sent 2 seconds after initialization.

    The payload is bigger than 1kB, and thus sent as several blocks."""

    sensor = Sensor(4)

    context = await Context.create_client_context()

    await asyncio.sleep(2)

    while(1):
        umid, temp = sensor.lerDados();

        payload = ("Temperatura = " + str(temp) + " Umidade = " + str(umid) + "\n")
        request = Message(code=PUT, payload=payload, uri="coap://10.0.0.181/other/block")

        response = await context.request(request).response

        print('Result: %s\n%r'%(response.code, response.payload))

        time.sleep(10);

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
