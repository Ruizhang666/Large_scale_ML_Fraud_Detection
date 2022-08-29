import dask.dataframe as dd
from dask_ml.preprocessing import Categorizer, DummyEncoder
import dask.array as da
import numpy as np
from dask_ml.preprocessing import StandardScaler
from distributed import Client,LocalCluster,performance_report



def clean():
	## Read in the data
	df=dd.read_csv("historical_data_2009Q1.txt",delimiter="|",header=None,dtype={25: 'object'})

	## Drop the unnecessary columns 
	columns_dropped_table1=[1,3,16,18,23,24,26]
	new1=df.drop(columns_dropped_table1,axis=1)

	# making the piplines for later transformation
	cat=Categorizer()
	one_hot=DummyEncoder()

	# precompute it so that we can assign/manipulate values to the dataframe 
	new1=new1.compute()

	# We need to partition the data first 
	new1_categorical=[2,7-1,8-1,14-1,15-1,16-1,18-1,21-1,23-1,26-1,28-1,29-1,30-1,31-1]
	mid=set(new1.columns)
	new1_as_is=list(mid.difference(set(new1_categorical)))

	new1_as_is=list(set(new1_as_is).difference(set([19])))

	new1_id=[19]

	new1_cat=new1[new1_categorical]
	new1_num=new1[new1_as_is]
	new1_id=new1[new1_id]


	# We need to make sure that the columns that are about to one-hot encoded are coverted to str
	# I would not impute the missingness since I trust the quality of the data and 
	# I believe that the missing value means something in terms of one hot encoding  
	for i in new1_categorical:
		new1_cat[i]=new1[i].astype(str)

	# Transform the categorical variables into one-hot encoded form  
	cat.fit(new1_cat)
	new1_cat=cat.transform(new1_cat)
	one_hot.fit(new1_cat)
	result_dataframe=one_hot.transform(new1_cat)

	# Join the table: numerical and one-hot encoder 
	result = dd.concat([new1_num,result_dataframe],axis=1)
	result = result.compute()

	# Standardize 
	std=StandardScaler()
	std.fit(result)
	result=std.transform(result)

	# if we want to impute the missingness with mean, you just fill 0s here since our data is standardized 
	result=result.fillna(0)

	# combine the as-is feature and one-hot feature 
	path="s3://ds102-i-love-dsc102-scratch/cleaned_1/"
	result = dd.concat([new1_id,result],axis=1)
	result.columns=result.columns.astype(str)
	output = dd.to_parquet(result,path)

if __name__=="__main__":
	cluster=LocalCluster(dashboard_address=":9001")
	client = Client(cluster)
	with performance_report(filename="dask-report_1.html"):
		clean()
