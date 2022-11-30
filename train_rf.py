from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.classification import RandomForestClassificationModel
from sklearn.metrics import confusion_matrix
from pyspark.sql import SparkSession
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.sql.types import FloatType
import pyspark.sql.functions as F
import pandas as pd
from pyspark.ml import Pipeline
from pyspark.ml.tuning import CrossValidator
from pyspark.ml.evaluation import ClassificationEvaluator
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


spark = SparkSession.builder.appName('rf_model').getOrCreate()
data = spark.read.csv('Project\creditcard.csv', header = True, inferSchema = True)
data=data.drop('Time')

feature_list=[col for col in data.columns if col!='Label']

va = VectorAssembler(inputCols=feature_list, outputCol="features")
va_df = va.transform(data)
va_df = va_df.select(['features', 'label'])

(train, test) = va_df.randomSplit([0.8, 0.2])

rfc = RandomForestClassifier(featuresCol="features", labelCol="label")
rfc = rfc.fit(train)






