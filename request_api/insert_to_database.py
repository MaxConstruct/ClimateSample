import pandas as pd
from setting import csv_path
from sqlalchemy import create_engine
import numpy as np
# %%
engine = create_engine('mysql+mysqlconnector://root@localhost/weatheranalysisdb')
#%%
analysis_csv_ls = list(csv_path.glob('csv/*.csv'))
dfs = [pd.read_csv(path, index_col=0) for path in analysis_csv_ls]
#%%
dfs[-1].index = np.arange(0, len(dfs[-1].index))
dfs[2].index = np.arange(0, len(dfs[2].index))
#%%
for i, df in enumerate(dfs):
    df.to_sql(analysis_csv_ls[i].stem.title(), con=engine, if_exists='replace')
