"""
A simple example of an animated plot
"""
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import statsmodels.api as sm
import pandas as pd
import os


#fig, ax = plt.subplots()

def make_movie(df, out_name):
    os.system('rm movies/*.png')
    for i in range(len(df)):
        if i <= 9:
           path = 'movies/00'+str(i)
        elif i > 99:
           path = 'movies/'+str(i)
        else:
           path = 'movies/0'+str(i)
        level_model = sm.tsa.UnobservedComponents(df[0:i+3], level=True, trend=True, stochastic_level=False, stochastic_trend=False, irregular=False)  
        level_results = level_model.fit()
        p = level_results.plot_components(figsize=(15, 12))
        p.savefig(path+'.png')
    os.chdir('movies')
    os.system('ffmpeg -framerate 10 -i %03d.png -s:v 1280x720 -c:v libx264 -profile:v high -crf 1 -pix_fmt yuv420p '+out_name+'.mp4')

raw_data = pd.read_feather('mwats_raw_data_Feb_SQL.fth',nthreads=1)

#### J0953 #####
source_name = 'J0953+0755'
J0953 = raw_data[raw_data.source_id==243604.0]
J0953.index = pd.to_datetime(J0953.time)
J0953 = J0953.sort_values(by='jd')
df = J0953.iloc[:, 15]
make_movie(df, source_name)

### GLEAM J032320+053413 ###
source = 237262.0
source_data = raw_data[raw_data.source_id == source]
source_name = 'GLEAM_J032320+053413'
source_filt = source_data[source_data.distance < 15.0]
source_filt.index = pd.to_datetime(source_filt.time)
source_filt = source_filt.sort_values(by='jd')
df = source_filt.iloc[:, 15]
#make_movie(df, source_name)













