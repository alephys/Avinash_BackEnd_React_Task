# from kafka import KafkaAdminClient, KafkaProducer
# from kafka.admin import NewTopic

# # Kafka broker addresses
# BROKERS = ['10.1.14.122:9091', '10.1.14.122:9092']  # kafka1 & kafka2 ports

# # Kafka Admin client (for creating/deleting topics)
# admin_client = KafkaAdminClient(
#     bootstrap_servers=BROKERS,
#     client_id='django-app-admin'
# )

# # Kafka Producer (optional, if you want to send messages)
# #producer = KafkaProducer(bootstrap_servers=BROKERS)
