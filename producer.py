from kafka import KafkaProducer
from pyspark.ml.classification import RandomForestClassificationModel
from pyspark.sql import SparkSession
import json, os
from pyspark.ml.feature import VectorAssembler
os.chdir("Project")
from data import get_transaction
import time
import pandas as pd
import random

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

producer1 = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=json_serializer)
producer2 = KafkaProducer(bootstrap_servers=['localhost:9092'], 
                         value_serializer=json_serializer)


if __name__ == "__main__":
    spark = SparkSession.builder.appName('transactions_overview').getOrCreate()
    rf2=RandomForestClassificationModel.load("model2")
    transactions=[]
    batch_length=10
    sleep_time=1
    while 0 == 0:
        #get transactions
        for i in range(batch_length): transactions.append(get_transaction()) 
        transactions=pd.DataFrame(transactions)
        transactions=spark.createDataFrame(transactions)
        
        #convert transactions to dataframe
        feature_list=[col for col in transactions.columns if col!='Label']
        va = VectorAssembler(inputCols=feature_list, outputCol="features")
        test=va.transform(transactions)
        test=test.select(['features', 'label'])
        
        #use model to determine class
        pred = rf2.transform(test)
        
        #send messages to corresponding consumer
        valid=pred.filter(pred.prediction=='0.0')
        valid_transactions=valid.toJSON()
        for valid_transaction in valid_transactions.collect():
            producer1.send("valid_transactions", valid_transaction)
            producer1.flush()
        
        flagged=pred.filter(pred.prediction=='1.0')
        flagged_transactions=flagged.toJSON()
        for flagged_transaction in flagged_transactions.collect():
            producer2.send("flagged_transactions", flagged_transaction)
            producer2.flush()
        
        #empty transactions and wait for next batch
        transactions=[]
        time.sleep(sleep_time)
        
        