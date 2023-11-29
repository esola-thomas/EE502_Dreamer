# %%
import json
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
import heartpy as hp
import pickle
import json

# %%
dataset_dir = "../../data_set"
data_dir = {}
processed_data_dir = {}
for file in os.listdir(dataset_dir):
    f = os.path.join(dataset_dir, file)
    participant_num = f.split('.')[-2].split("subject_")[-1]
    f_open = open(f)
    data_dir["participant_" + participant_num] = json.load(f_open)
    f_open.close()
    print("Loaded " + str(file))

# %%
def plot_raw(participant_num, clip_num):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 8))
    fig.suptitle('clip #'+str(clip_num) , fontsize=15)
    
    axes[0].plot(data_dir['participant_'+str(participant_num)]['ECG']['baseline'][clip_num][0:1024])
    axes[0].set_title('participant_'+str(participant_num) + ' baseline')
    
    axes[1].plot(data_dir['participant_'+str(participant_num)]['ECG']['stimuli'][clip_num][0:1024])
    axes[1].set_title('participant_'+str(participant_num) + ' stimuli')
    
    
def plot_raw_filtered(participant_num, clip_num):
    
    processed_data_dir['participant_'+str(participant_num)] = {}
    processed_data_dir['participant_'+str(participant_num)]['ECG'] = {} 
    processed_data_dir['participant_'+str(participant_num)]['ECG']['stimuli'] = {} 
    processed_data_dir['participant_'+str(participant_num)]['ECG']['baseline'] = {} 
#     processed_data_dir['participant_'+str(participant_num)]['ECG']['stimuli'][clip_num]

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 8))
    fig.suptitle('clip #'+str(clip_num) , fontsize=15)
    
    ch1 = [row[0] for row in data_dir['participant_'+str(participant_num)]['ECG']['baseline'][clip_num]]
    ch2 = [row[1] for row in data_dir['participant_'+str(participant_num)]['ECG']['baseline'][clip_num]]
    
    
    ch1_filtered = hp.remove_baseline_wander(ch1, 256)
    ch2_filtered = hp.remove_baseline_wander(ch2, 256)
    result = np.column_stack((ch1_filtered, ch2_filtered))
    
    processed_data_dir['participant_'+str(participant_num)]['ECG']['baseline'][str(clip_num)] = result
    
    axes[0].plot(result[0:1024])
    axes[0].set_title('participant_'+str(participant_num) + ' baseline')
    
    ch1 = [row[0] for row in data_dir['participant_'+str(participant_num)]['ECG']['stimuli'][clip_num]]
    ch2 = [row[1] for row in data_dir['participant_'+str(participant_num)]['ECG']['stimuli'][clip_num]]
    
    ch1_filtered = hp.remove_baseline_wander(ch1, 256)
    ch2_filtered = hp.remove_baseline_wander(ch2, 256)
    result = np.column_stack((ch1_filtered, ch2_filtered))
    axes[1].plot(result[0:1024])
    axes[1].set_title('participant_'+str(participant_num) + ' stimuli')
    
    processed_data_dir['participant_'+str(participant_num)]['ECG']['stimuli'][str(clip_num)] = result
    
    

# %%
for i in range(1,2):
        plot_raw(1, i)
#matplotlib.pyplot.close()

# %% [markdown]
# ### Generate .pkl with data from all participants

# %%
def drop_EEG_data ():
    for participant in data_dir:
        data_dir[participant].pop('EEG')
        print(participant + " Dropped EEG Data")
        
drop_EEG_data ()

# %%
with open('../../data_set_raw_ECG/raw_data_dict.pkl', 'wb') as f:
    pickle.dump(data_dir, f)

with open('../../data_set_raw_ECG/raw_data_dict.json', 'w') as f:
    json.dump(data_dir, f)

# %%
data_dir['participant_23']['ECG'].keys()
len(data_dir['participant_23']['ECG']['baseline'])

# %%



