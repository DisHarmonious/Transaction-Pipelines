from kafka import KafkaConsumer
import json


if __name__ == "__main__":
    consumer2=KafkaConsumer("flagged_transactions",
                           bootstrap_servers="localhost:9092",
                           auto_offset_reset='earliest',
                           group_id="group-b")
    print("starting consumer 2:")
    for msg in consumer2:
        temp = json.loads(msg.value)
        temp2 = list(temp.values())
        print(temp)
        print(temp2)