import pandas as pd
import matplotlib as plt
import mne
import json
import numpy as np
import pathlib
from os import listdir
import numpy
# read in data
USO_csv = pd.read_csv('data/USO_features.csv')
file = open('data/uso_ids_and_conditions_new_new.json')  # read in json dictionary of index list for id and condition
uso_ids_and_conditions = json.load(file)
eeg_data_path = pathlib.Path('C:/EEG/USO/data')
ids = listdir(eeg_data_path)
print('reading in epoch data')
epoch_data = [mne.read_epochs('C:/EEG/USO/data/' + i + '/epochs/' + i + '-epo.fif') for i in ids]
print('finished reading in epoch data')


exclude_participant = ['4q868v', 'l6e5vs', 'omfdt1', 'u88rdo']

# delete participants from epoch data and dictionary
for participant in exclude_participant:
    for participant_idx, epochs in enumerate(epoch_data):
        if participant in epoch_data[participant_idx].filename:
            del epoch_data[participant_idx]
    del uso_ids_and_conditions[participant]

# add actual epoch indexes to dictionary
for participant_idx, participant in enumerate(uso_ids_and_conditions):
    for epoch_idx, epoch in enumerate(uso_ids_and_conditions[participant]):
        idx_array = epoch_data[participant_idx].selection == epoch_idx
        if np.any(idx_array):
            actual_epoch_idx = np.where(idx_array)[0][0]
            uso_ids_and_conditions[participant][epoch_idx].update(actual_epoch_idx=actual_epoch_idx)


# create empty list to store shifted epochs in
shifted_epochs_data = list()
participant_idx = 18
participant = 'zx4v7q'

for participant_idx, participant in enumerate(uso_ids_and_conditions):
    shifted_epochs = list()
    for epoch_idx, epoch in enumerate(uso_ids_and_conditions[participant]):
        if 'actual_epoch_idx' in uso_ids_and_conditions[participant][epoch_idx].keys():
            if uso_ids_and_conditions[participant][epoch_idx]['condition'] != 0:
                USO_csv_filtered = USO_csv.loc[(USO_csv['USO_id'] == uso_ids_and_conditions[participant][epoch_idx]['sound_id']) &
                                               (USO_csv['dist_group'] == uso_ids_and_conditions[participant][epoch_idx]['condition'])]

                onset_delay = USO_csv_filtered.loc[USO_csv_filtered.index[0], 'onset_delay_avg']
                # print(onset_delay)
                if not np.isnan(onset_delay):
                    actual_epoch_idx = uso_ids_and_conditions[participant][epoch_idx]['actual_epoch_idx']
                    shifted_epoch = epoch_data[participant_idx][actual_epoch_idx].copy()
                    index = epoch_data[participant_idx][actual_epoch_idx].time_as_index(onset_delay)
                    shifted_epoch._data = numpy.concatenate((epoch_data[participant_idx][actual_epoch_idx]._data[:, :, index[0]:],
                                                             epoch_data[participant_idx][actual_epoch_idx]._data[:, :, :index[0]]),
                                                            axis=2, out=None, dtype=None, casting="same_kind")
                    shifted_epochs.append(shifted_epoch)


shift_concatenated = mne.concatenate_epochs(shifted_epochs)
shifted_epochs_data.append(shift_concatenated)


shifted_evokeds = {'USO/1': list(),
                 'USO/2': list(),
                 'USO/3': list(),
                 'USO/4': list(),
                 'USO/5': list()}

for participant in shifted_epochs_data:
    participant_evokeds = participant.average(by_event_type=True)
    for i, evokeds in enumerate(participant_evokeds):
        if participant_evokeds[i].comment == 'USO/1':
            shifted_evokeds['USO/1'].append(participant_evokeds[i])
        elif participant_evokeds[i].comment == 'USO/2':
            shifted_evokeds['USO/2'].append(participant_evokeds[i])
        elif participant_evokeds[i].comment == 'USO/3':
            shifted_evokeds['USO/3'].append(participant_evokeds[i])
        elif participant_evokeds[i].comment == 'USO/4':
            shifted_evokeds['USO/4'].append(participant_evokeds[i])
        elif participant_evokeds[i].comment == 'USO/5':
            shifted_evokeds['USO/5'].append(participant_evokeds[i])


mne.viz.plot_compare_evokeds(shifted_evokeds, ci=False)
for condition in shifted_evokeds:
    for participant in shifted_evokeds[condition]:
        participant.shift_time(tshift=0.2, relative=True)

shifted_evokeds_cond_1 = mne.read_evokeds('C:/USO Analysis/evoked/time_shifted_by_onset_delay/time_shifted_by_onset_delay_cond_1-ave.fif')
shifted_evokeds_cond_2 = mne.read_evokeds('C:/USO Analysis/evoked/time_shifted_by_onset_delay/time_shifted_by_onset_delay_cond_2-ave.fif')
shifted_evokeds_cond_3 = mne.read_evokeds('C:/USO Analysis/evoked/time_shifted_by_onset_delay/time_shifted_by_onset_delay_cond_3-ave.fif')
shifted_evokeds_cond_4 = mne.read_evokeds('C:/USO Analysis/evoked/time_shifted_by_onset_delay/time_shifted_by_onset_delay_cond_4-ave.fif')
shifted_evokeds_cond_5 = mne.read_evokeds('C:/USO Analysis/evoked/time_shifted_by_onset_delay/time_shifted_by_onset_delay_cond_5-ave.fif')

combined_evokeds_1 = mne.combine_evoked(shifted_evokeds_cond_1, weights='equal')
combined_evokeds_2 = mne.combine_evoked(shifted_evokeds_cond_2, weights='equal')
combined_evokeds_3 = mne.combine_evoked(shifted_evokeds_cond_3, weights='equal')
combined_evokeds_4 = mne.combine_evoked(shifted_evokeds_cond_4, weights='equal')
combined_evokeds_5 = mne.combine_evoked(shifted_evokeds_cond_5, weights='equal')

combined_evokeds = list()
combined_evokeds.append(combined_evokeds_5)
combined_evokeds.append(combined_evokeds_4)
combined_evokeds.append(combined_evokeds_3)
combined_evokeds.append(combined_evokeds_2)
combined_evokeds.append(combined_evokeds_1)

combined_evokeds_final = mne.combine_evoked(combined_evokeds, weights='equal')
combined_evokeds_final.plot_joint()


evokeds.data = np.roll