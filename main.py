from confluent_kafka import Consumer, KafkaError
from datetime import datetime, timedelta
import time

# Configuración del consumidor de Kafka
kafka_config = {
    'bootstrap.servers': 'kafka:9092',  # Cambia por tu servidor Kafka
    'group.id': 'my-consumer-group',
    'auto.offset.reset': 'earliest',
}

# Tópico de CDC desde Debezium (MySQL)
cdc_topic = 'mysql-connector.db_movies_neflix_transact.movie'  # Cambia esto según tu config

# Función para imprimir notificación en consola
def print_notification(message):
    print(f"ALERTA: {message}")

# Inicializar el consumidor de Kafka
consumer = Consumer(kafka_config)
print('Kafka Consumer has been initiated...')
print('Available topics to consume: ', consumer.list_topics().topics)

consumer.subscribe([cdc_topic])

# Guardar el timestamp del último cambio recibido
last_change_time = datetime.now()

try:
    while True:
        msg = consumer.poll(timeout=1.0)  # Esperar por mensajes

        if msg is None:
            # No hay mensaje nuevo
            current_time = datetime.now()
            # Si han pasado más de 10 minutos sin recibir un mensaje
            if current_time - last_change_time > timedelta(seconds=30):
                print_notification("No se han detectado cambios en los últimos 10 minutos en CDC.")
                last_change_time = current_time  # Resetear el contador tras imprimir

        elif msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # Fin de la partición, sin nuevos mensajes
                continue
            else:
                print(f"Error de Kafka: {msg.error()}")
                continue
        else:
            # Mensaje recibido, actualizar el tiempo del último cambio
            print(f"Mensaje recibido: {msg.value()}")
            last_change_time = datetime.now()

        time.sleep(1)  # Evitar uso excesivo de CPU

except KeyboardInterrupt:
    pass

finally:
    # Cerrar el consumidor al terminar
    consumer.close()
