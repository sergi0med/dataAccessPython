import pickle
import pandas as pd
from Customer import *
def saveCustomer(f,oC):
    f.seek(0, 2)
    oC.posFile=f.tell()
    pickle.dump(oC, f)


def modifyCustomer(f,oC):
    f.seek(oC.posFile,0)
    pickle.dump(oC, f)

def readCustomer(f,lC):
    df = pd.read_csv(f)
    l = df.values.tolist()
    for custo in l:
        lC.append(Customer(custo[0], custo[1], custo[2],custo[3], custo[4],-1))

