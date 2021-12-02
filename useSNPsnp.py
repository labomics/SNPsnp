import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error 
from sklearn.metrics import r2_score
import joblib
import sys

def standardlize(vmin, vmax, v):
    sv = (v-vmin)/(vmax-vmin)
    return(sv)
def inversestandardlize(vmin, vmax, v):
    origin = v*(vmax-vmin) + vmin
    return(origin)

inputfile = sys.argv[1]
all1 = pd.read_csv(inputfile,sep='\t',header=None)
all1.columns=['Strain','Coverage','Depth','Abundance(%)','Genome length','SNP','SNP density']

vamin = np.array([2.49293595e-01,1.56539869e+00,8.06811373e-01,1.89596000e+06,0.00000000e+00,0.00000000e+00])
vamax = np.array([9.79974624e-01,1.13669851e+04,2.96864023e+01,7.90058000e+06,2.11767000e+05,8.30890853e-02])
ymin = 6733
ymax = 209473

X = all1[['Coverage','Depth','Abundance(%)','Genome length','SNP','SNP density']].values.reshape(-1,6)
X1 = standardlize(vamin,vamax,X)

model1 = joblib.load('SNPsnp.model')
y_pred=model1.predict(X1)
y_predict= inversestandardlize(ymin,ymax,y_pred.reshape(-1, 1))
predictSNP = all1[['Strain','Coverage','Depth','Abundance(%)','Genome length','SNP','SNP density']].join(pd.DataFrame(y_predict,columns=['Saturation number prediction']))
predictSNP.to_csv("predictSNPs.txt",sep='\t',index=0)
