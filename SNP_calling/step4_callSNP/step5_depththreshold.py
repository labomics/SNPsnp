import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import re
import scipy
from scipy.stats import pearsonr, spearmanr
from scipy.stats import wilcoxon,mannwhitneyu
import statistics
from sklearn.mixture import GaussianMixture 
from sklearn import mixture
from scipy.stats import norm
from scipy.stats import expon
from sklearn.neighbors import KernelDensity
from pomegranate import *
import math


with open("subdepth.txt",'w') as outpf:
    with open("strains.txt",'r') as inpf1:
        for line1 in inpf1:
            line1 = line1.strip()
            if re.match("#",line1):
                continue
            genome = line1
            threhold = 100000
            for i in range(3):
                genes = pd.read_csv("./depth/%s.bed"%(genome),sep='\t',header=None)
                genes.columns = ['contig','site','depth']
                genes=genes[genes['depth']!=0]
                X = np.array(genes['depth']).reshape(-1,1)
                model = GeneralMixtureModel.from_samples([ExponentialDistribution,NormalDistribution],  n_components=2,X=X)
                if json.loads(str(model))['weights'][0] == 0:
                    continue
                if json.loads(str(model))['weights'][0] > 0.9:
                    continue
                a = model.distributions
                explambda = a[0].parameters[0]
                expth = float(expon.ppf(0.5,scale=1/explambda))
                normloc = a[1].parameters[0]
                normmu = a[1].parameters[1]
                normth1 = float(norm.ppf(0.1,loc=normloc,scale=normmu))
                if expth <= normth1:
                    th = expth
                elif expth > normth1:
                    th = normth1
                if threhold == int(th+0.5):
                    continue
                threhold = int(th+0.5)
                x1=np.arange(1, 8000, 1)
                model.probability(x1)
                x2=x1.reshape(-1,1)
                model.predict_proba(x2)
                respons = pd.DataFrame(model.predict_proba(x2))
                respons.columns=["left","right"]
                outpf.write("%s\t%s\t%s\t%s\t%s\n"%(genome,threhold,model.distributions[0].parameters[0],model.distributions[1].parameters[0],json.loads(str(model))['weights']))
                print(genome,threhold,model.distributions[0].parameters[0],model.distributions[1].parameters[0],json.loads(str(model))['weights'])
                plt.figure()
                plt.title('%s'%(genome))
                plt.hist(X, 1000, density=True, histtype='stepfilled', alpha=0.4)
                plt.fill_between(x1,0,model.probability(x1))
