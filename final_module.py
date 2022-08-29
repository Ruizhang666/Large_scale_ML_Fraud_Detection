import pyarrow.parquet as pq
import s3fs
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import numpy as np

s3 = s3fs.S3FileSystem()

path="s3://ds102-i-love-dsc102-scratch/label_correct"

labels = pq.ParquetDataset(path, filesystem=s3).read_pandas().to_pandas()


cleaned_data=pd.read_parquet("new.parquet")


# Join the data 
prepared_data=pd.merge(cleaned_data,labels,how='left',left_on=["19"],right_on=["_c0"]).drop(["19","_c0"],axis=1)



# Train_test split
y=np.array(prepared_data[["label"]].fillna(0))
X=prepared_data.drop("label",axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y)


# train the model
clf = LogisticRegression().fit(X_train, y_train)

# Print out the score !
clf.score(X_test, y_test)

