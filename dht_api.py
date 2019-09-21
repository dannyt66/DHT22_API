# API stuff
from flask import Flask
from flask_restful import Resource, Api
import json

# Sensor Stuff
import Adafruit_DHT

# Build configuration map
with open('config.json', 'r') as cfile:
    config = json.load(cfile)

# Run Flask app
app = Flask(__name__)
api = Api(app)


class Temperature(Resource):
    def get(self, temperature_unit):
        temperature, humidity = get_temp()

        if temperature_unit == "farenheit":
            temperature = temperature * 9/5.0 + 32

        return {
            'temperature': temperature,
            'unit': temperature_unit
        }


api.add_resource(Temperature, "/temperature/<temperature_unit>")

if __name__ == "__main__":
    sensor_args = {
        'DHT11': Adafruit_DHT.DHT11,
        'DHT22': Adafruit_DHT.DHT22,
        'AM2302': Adafruit_DHT.AM2302
    }

    if config["sensor"] is not None:
        config["sensor"] == sensor_args[config["sensor"]]
    else:
        print("You must supply a sensor configuration. Exiting.")
        exit()

    if config["pin"] is None:
        print("You must specify the pin your sensor is attacted to. Exiting.")
        exit()

    if config["port"] is None:
        print("You must supply a port to listen on. Exiting.")
        exit()

    app.run(port=config["port"])


def get_temp(sensor, pin):
    temperature, humidity = Adafruit_DHT.read_retry(sensor, pin)

    return temperature, humidity

