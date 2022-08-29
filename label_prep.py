# Import the necessary components 
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import udf
import pyspark.sql.functions as F
from pyspark.sql.functions import col


# Read the data first 
monthly_performance = spark.read.option("header", False).option("delimiter",'|').csv("s3://ds102-i-love-dsc102-scratch/historical_data_time_2009Q1.txt")


# Define a helper and later convert that helper to user-defined function in spark
def check_col4(x):
    if x!="R":
        x=int(x)
    if x==0:
        return 0
    elif x==1:
        return 0
    elif x==2:
        return 0
    else:
        return 1

def check_col9(x):
	if x==3: 
		return 1
	elif x==6:
		return 1
	elif x==9:
		return 1
	else: 
		return 0


def default(x):
	if x>=1:
		return 1
	else: 
		return 0

udf_myFunction1 = udf(check_col4, IntegerType())
udf_myFunction2 = udf(check_col9, IntegerType())
udf_myFunction3 = udf(default, IntegerType())



# Apply Function to dataframe and get the labels 
monthly_performance=monthly_performance.withColumn('default_status_04', udf_myFunction1(monthly_performance._c3))
monthly_performance=monthly_performance.withColumn('default_status_09', udf_myFunction2(monthly_performance._c8))
monthly_performance=monthly_performance.withColumn("default_status",monthly_performance.default_status_04+monthly_performance.default_status_09)
monthly_performance=monthly_performance.withColumn("label",udf_myFunction3(monthly_performance.default_status))
out=monthly_performance.groupBy("_c0").agg(F.max("label")).select("_c0","max(label)")
out = out.select(col("_c0"),col("max(label)").alias("label"))

out.write.format("parquet").mode("overwrite").save("s3://ds102-i-love-dsc102-scratch/label_correct")

