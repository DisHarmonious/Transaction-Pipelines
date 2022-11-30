from kafka import KafkaConsumer
import json


if __name__ == "__main__":
    consumer1=KafkaConsumer("valid_transactions",
                           bootstrap_servers="localhost:9092",
                           auto_offset_reset='earliest',
                           group_id="group-a")
    print("starting consumer 1:")
    for msg in consumer1:
        temp = json.loads(msg.value)
        temp2 = list(temp.values())
        print(temp)
        print(temp2)