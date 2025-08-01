import paho.mqtt.client as mqtt
import random
import time

broker = 'localhost'
port = 1883
client_id = f'python-mqtt-{random.randint(0, 1000)}'
current_topic = "python/mqtt"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("Conectado al broker MQTT")
        else:
            print(f"Falló la conexión, código de retorno {rc}")
            
    client = mqtt.Client(client_id=client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt.Client, topic: str):
    def on_message(client, userdata, msg):
        print(f"Mensaje recibido: `{msg.payload.decode()}` del topic `{msg.topic}`")

    client.subscribe(topic)
    client.on_message = on_message
    print(f"Suscrito al topic `{topic}`")

def publish(client, topic: str, message: str = "MENSAJE"):
    result = client.publish(topic, message)
    status = result[0]

    if status == 0:
        print(f"Enviado `{message}` al topic `{topic}`")
    else:
        print(f"Falló el envío al topic {topic}")

def menu():
    global current_topic
    client = connect_mqtt()
    client.loop_start()

    while True:
        print("\n===== MENÚ MQTT =====")
        print(f"Topic actual: {current_topic}")
        print("1. Cambiar topic")
        print("2. Suscribirse al topic")
        print("3. Publicar mensajes al topic")
        print("4. Salir")
        opcion = input("Selecciona una opción (1-4): ")

        if opcion == '1':
            nuevo_topic = input("Ingresa el nuevo topic: ").strip()
            if nuevo_topic:
                current_topic = nuevo_topic
                print(f"Topic cambiado a `{current_topic}`")
            else:
                print("Topic no puede estar vacío.")
        elif opcion == '2':
            subscribe(client, current_topic)
        elif opcion == '3':
            mensaje = input("MENSAJE A ENVIAR (por defecto MENSAJE): ")
            publish(client, current_topic, mensaje)
        elif opcion == '4':
            print("Saliendo del programa...")
            client.loop_stop()
            client.disconnect()
            break
        else:
            print("Opción inválida. Intenta de nuevo.")

if __name__ == '__main__':
    menu()
