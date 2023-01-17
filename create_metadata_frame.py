import pandas as pd
import mne
from os import listdir
import pathlib
import json
eeg_data_path = pathlib.Path('C:/EEG/pre-processing/data')
ids = listdir(eeg_data_path)
print('reading in epoch data')
epoch_data = [mne.read_epochs('C:/EEG/pre-processing/data/' + i + '/epochs/' + i + '-epo.fif') for i in ids]
print('finished reading in epoch data')
USO_csv = pd.read_csv('data/USO_features.csv')
file = open('data/uso_ids_and_conditions_new_new.json')  # read in json dictionary of index list for id and condition
uso_ids_and_conditions = json.load(file)


meta