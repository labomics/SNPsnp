import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error 
from sklearn.metrics import r2_score
import joblib
import sys


inputfile = sys.argv[1]
all1 = pd.read_csv(inputfile,sep='\t',header=None)
all1.columns=['Strain','Coverage','Depth','Abundance(%)','Genome length','SNP','SNP density']

X = all1[['Coverage','Depth','Abundance(%)','Genome length','SNP','SNP density']].values.reshape(-1,6)

model1 = joblib.load('SNPsnp.model')
y_predict= model1.predict(X)
predictSNP = all1[['Strain','Coverage','Depth','Abundance(%)','Genome length','SNP','SNP density']].join(pd.DataFrame(y_predict,columns=['Saturation number prediction']))
predictSNP.to_csv("predictSNPs.txt",sep='\t',index=0)
