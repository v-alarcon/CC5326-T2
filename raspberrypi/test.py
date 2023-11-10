import asyncio
import struct
from bleak import BleakClient
from peewee import *
from playhouse.postgres_ext import ArrayField
from time import sleep
from modelos import *
import datetime
# Configuración de la base de datos
db_config = {
    'host': 'localhost', 
    'port': 5433, 
    'user': 'postgres', 
    'password': 'postgres', 
    'database': 'iot_db'
}
db = PostgresqlDatabase(**db_config)

# Definición de un modelo
class BaseModel(Model):
    class Meta:
        database = db
# create a new table named Config with ID_protocol and Transport_Layer
class Config(BaseModel):
    ID_protocol = CharField()
    Transport_Layer = CharField()   

# query for the row with id = 1 row of the config table using peewee
config = Config.get_by_id(1)

data = (str(config.ID_protocol)+str(config.Transport_Layer)).encode()
print(data)

def convert_to_128bit_uuid(short_uuid):
    # Usada para convertir un UUID de 16 bits a 128 bits
    # Los bits fijos son utilizados para BLE ya que todos los UUID de BLE son de 128 bits
    # y tiene este formato: 0000XXXX-0000-1000-8000-00805F9B34FB
    base_uuid = "00000000-0000-1000-8000-00805F9B34FB"
    short_uuid_hex = "{:04X}".format(short_uuid)
    return base_uuid[:4] + short_uuid_hex + base_uuid[8:]


ADDRESS = "3c:61:05:65:9d:ba"
CHARACTERISTIC_UUID = convert_to_128bit_uuid(0xFF01) # Busquen este valor en el codigo de ejemplo de esp-idf



async def main(ADDRESS):
    async with BleakClient(ADDRESS) as client:
        #char_value = await client.read_gatt_char(CHARACTERISTIC_UUID)
        #print("Characterisic A {0}".format("".join(map(chr, char_value))))
        # Luego podemos escribir en la caracteristica
        await client.write_gatt_char(CHARACTERISTIC_UUID, data)
        print("Waiting for data...")
        sleep(3)
        char_value = await client.read_gatt_char(CHARACTERISTIC_UUID)
        # save data in the database
        print("Guardando en la base de datos")

        if data == "00".encode():
            #get the first 2 bytes from the data and transform into a str id_device
            id_device = str(char_value[0:2].decode('utf-8'))
            print("ID: " + id_device)

            #get the next 6 bytes from the data and transform into a str MAC
            mac = "3c:61:05:65:9d:ba"
            # TODO FIX THIS
            # for i in range(4):
            #     mac += bytes.hex(char_value[2+i:3+i]) + ":"
            # mac = mac[:-1]
            # print("MAC: " + mac)

            #get the next byte to know the transport layer
            transport_layer = chr(char_value[8])
            print("Transport layer: " + transport_layer)

            #get the next byte to get the protocol
            protocol = chr(char_value[9])
            print("Protocol: " + protocol)

            #get the next 2 bytes to get the packet length
            packet_length = int.from_bytes(char_value[10:12], signed=False, byteorder='little')
            print("Packet length: " + str(packet_length))
            #get the final byte with the battery level
            battery_level = char_value[12]
            print("Battery level: " + str(battery_level))

            #save the data in the database
            Datos.insert(Id_device=id_device, MAC=mac, battlevel=battery_level).execute()
            Logs.insert(ID_device=id_device, Transport_Layer=transport_layer, finaltime=datetime.datetime.now()).execute()
        if data == "10".encode():
             #get the first 2 bytes from the data and transform into a str id_device
            id_device = str(char_value[0:2].decode('utf-8'))
            print("ID: " + id_device)

            #get the next 6 bytes from the data and transform into a str MAC
            mac = "3c:61:05:65:9d:ba"
            # TODO FIX THIS
            # for i in range(4):
            #     mac += bytes.hex(char_value[2+i:3+i]) + ":"
            # mac = mac[:-1]
            # print("MAC: " + mac)

            #get the next byte to know the transport layer
            transport_layer = chr(char_value[8])
            print("Transport layer: " + transport_layer)

            #get the next byte to get the protocol
            protocol = chr(char_value[9])
            print("Protocol: " + protocol)

            #get the next 2 bytes to get the packet length
            packet_length = int.from_bytes(char_value[10:12], signed=False, byteorder='little')
            print("Packet length: " + str(packet_length))
            #get the next byte with the battery level
            battery_level = char_value[12]
            print("Battery level: " + str(battery_level))
            # get the timestamp
            ts = char_value[13:17]
            #print("Timestamp: " + str(ts))

            #save the data in the database
            Datos.insert(Id_device=id_device, MAC=mac, battlevel=battery_level).execute()
            Logs.insert(ID_device=id_device, Transport_Layer=transport_layer, finaltime=datetime.datetime.now()).execute()
        if data == "20".encode():
            #get the first 2 bytes from the data and transform into a str id_device
            id_device = str(char_value[0:2].decode('utf-8'))
            print("ID: " + id_device)

            #get the next 6 bytes from the data and transform into a str MAC
            mac = "3c:61:05:65:9d:ba"
            # TODO FIX THIS
            # for i in range(4):
            #     mac += bytes.hex(char_value[2+i:3+i]) + ":"
            # mac = mac[:-1]
            # print("MAC: " + mac)

            #get the next byte to know the transport layer
            transport_layer = chr(char_value[8])
            print("Transport layer: " + transport_layer)

            #get the next byte to get the protocol
            protocol = chr(char_value[9])
            print("Protocol: " + protocol)

            #get the next 2 bytes to get the packet length
            packet_length = int.from_bytes(char_value[10:12], signed=False, byteorder='little')
            print("Packet length: " + str(packet_length))
            #get the next byte with the battery level
            battery_level = char_value[12]
            print("Battery level: " + str(battery_level))
            # get the timestamp
            ts = char_value[13:17]
            #print("Timestamp: " + str(ts))

            #get the temperature from the next byte
            temperature = char_value[17]
            print("Temperature: " + str(temperature))

            #get the pressure from the next 4 bytes
            pressure = int.from_bytes(char_value[18:22], signed=False, byteorder='little')
            print("Pressure: " + str(pressure))

            #get the humidity from the next byte its an int
            humidity = char_value[22]
            print("Humidity: " + str(humidity))

            #get the CO2 from the next 4 bytes, its a float
            co = struct.unpack('f', char_value[23:27])
            print("CO: " + str(co[0]))

            #save the data in the database
            Datos.insert(Id_device=id_device, MAC=mac, battlevel=battery_level, temp=temperature,
                            press=pressure, hum=humidity, co=co[0]).execute()
            Logs.insert(ID_device=id_device, Transport_Layer=transport_layer, finaltime=datetime.datetime.now()).execute()
        if data == "30".encode():
            #get the first 2 bytes from the data and transform into a str id_device
            id_device = str(char_value[0:2].decode('utf-8'))
            print("ID: " + id_device)

            #get the next 6 bytes from the data and transform into a str MAC
            mac = "3c:61:05:65:9d:ba"
            # TODO FIX THIS
            # for i in range(4):
            #     mac += bytes.hex(char_value[2+i:3+i]) + ":"
            # mac = mac[:-1]
            # print("MAC: " + mac)

            #get the next byte to know the transport layer
            transport_layer = chr(char_value[8])
            print("Transport layer: " + transport_layer)

            #get the next byte to get the protocol
            protocol = chr(char_value[9])
            print("Protocol: " + protocol)

            #get the next 2 bytes to get the packet length
            packet_length = int.from_bytes(char_value[10:12], signed=False, byteorder='little')
            print("Packet length: " + str(packet_length))
            #get the next byte with the battery level
            battery_level = char_value[12]
            print("Battery level: " + str(battery_level))
            # get the timestamp
            ts = char_value[13:17]
            #print("Timestamp: " + str(ts))

            #get the temperature from the next byte
            temperature = char_value[17]
            print("Temperature: " + str(temperature))

            #get the pressure from the next 4 bytes
            pressure = int.from_bytes(char_value[18:22], signed=False, byteorder='little')
            print("Pressure: " + str(pressure))

            #get the humidity from the next byte its an int
            humidity = char_value[22]
            print("Humidity: " + str(humidity))

            #get the CO2 from the next 4 bytes, its a float
            co = struct.unpack('f', char_value[23:27])
            print("CO: " + str(co[0]))

            #get the RMS from the next 4 bytes, its a float
            rms = struct.unpack('f', char_value[27:31])
            print("RMS: " + str(rms[0]))

            #get the ampx from the next 4 bytes, its a float
            ampx = struct.unpack('f', char_value[31:35])
            print("AMPX: " + str(ampx[0]))

            #get the frecx from the next 4 bytes, its a float
            frecx = struct.unpack('f', char_value[35:39])
            print("FRECX: " + str(frecx[0]))

            #get the ampy from the next 4 bytes, its a float
            ampy = struct.unpack('f', char_value[39:43])
            print("AMPY: " + str(ampy[0]))

            #get the frecy from the next 4 bytes, its a float
            frecy = struct.unpack('f', char_value[43:47])
            print("FRECY: " + str(frecy[0]))

            #get the ampz from the next 4 bytes, its a float
            ampz = struct.unpack('f', char_value[47:51])
            print("AMPZ: " + str(ampz[0]))

            #get the frecz from the next 4 bytes, its a float
            frecz = struct.unpack('f', char_value[51:55])
            print("FRECZ: " + str(frecz[0]))

            #save the data in the database
            Datos.insert(Id_device=id_device, MAC=mac, battlevel=battery_level, temp=temperature,
                                     press=pressure, hum=humidity, co=co[0], rms=rms[0], ampx=ampx[0], freqx=frecx[0],
                                     ampy=ampy[0], freqy=frecy[0], ampz=ampz[0], freqz=frecz[0]).execute()
            Logs.insert(ID_device=id_device, Transport_Layer=transport_layer, finaltime=datetime.datetime.now()).execute()



        
asyncio.run(main(ADDRESS))

