import pika

class Manager:
    def __init__(self, default_user, default_password, host) -> object:
        self.__default_user = default_user
        self.__default_password = default_password
        self.__host = host
        
    def connection(self):
        credentials = pika.PlainCredentials(self.__default_user, self.__default_password)
        parameters = pika.ConnectionParameters(self.__host, credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        return connection

    def channel(self):
        connection = self.connection()
        channel = connection.channel()
        return channel
    
    def create_queue(self, queue_name):
        queue = self.channel()
        return queue.queue_declare(queue=queue_name, durable=True)

    def declare_exchange(self, exchange, types):
        return self.channel().exchange_declare(exchange=exchange, exchange_type=types)

    def publish_message(self, exchange, routing, body):
        return self.channel().basic_publish(exchange=exchange, routing_key=routing, body=body, properties=pika.BasicProperties(
            delivery_mode=2
        ))

    def queue_bind(self, exchange, queue_name):
        self.channel.queue_bind(exchange=exchange, queue=queue_name)

    def basic_consume(self, queue_name, callback, auto_act=True):
        return self.channel().basic_consume(queue=queue_name, on_message_callback=callback)
    
    def consuming(self):
        self.channel().start_consuming()

    def close_connection(self):
        self.connection().close()

    def basic_qos(self, prefetch_count):
        self.connection().channel().basic_qos(prefetch_count=prefetch_count)


 