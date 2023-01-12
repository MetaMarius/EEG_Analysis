import pathlib
import mne
from os import listdir
import json
import numpy as np
file = open('data/uso_ids_and_conditions_new_new.json')  # read in json dictionary of index list for id and condition
uso_ids_and_conditions = json.load(file)
exclude_ids = [28, 27, 25, 22, 18, 17, 14, 11, 10, 7, 5, 3]  # declare sound ids to be excluded
exclude_participant = ['4q868v', 'l6e5vs', 'omfdt1', 'u88rdo']  # declare participants to be exclude due to unmatching index


idx_list_ids_excluded = {'USO/1': {participant: [] for participant in uso_ids_and_conditions},
                         'USO/2': {participant: [] for participant in uso_ids_and_conditions},
                         'USO/3': {participant: [] for participant in uso_ids_and_conditions},
                         'USO/4': {participant: [] for participant in uso_ids_and_conditions},
                         'USO/5': {participant: [] for participant in uso_ids_and_conditions}}  # create empty dict for indexes

for participant in uso_ids_and_conditions:  # get the indexes where condition and sound id meets the requirement
    for idx, epoch in enumerate(uso_ids_and_conditions[participant]):
        if epoch['condition'] == 1:
            idx_list_ids_excluded['USO/1'][participant].append(idx)
        if epoch['condition'] == 2:
            idx_list_ids_excluded['USO/2'][participant].append(idx)
        if epoch['condition'] == 3:
            idx_list_ids_excluded['USO/3'][participant].append(idx)
        if epoch['condition'] == 4:
            idx_list_ids_excluded['USO/4'][participant].append(idx)
        if epoch['condition'] == 5:
            if epoch['sound_id'] not in exclude_ids:
                idx_list_ids_excluded['USO/5'][participant].append(idx)


# create epoch data
eeg_data_path = pathlib.Path('C:/EEG/USO/data')
ids = listdir(eeg_data_path)
print('reading in epoch data')
epoch_data = [mne.read_epochs('C:/EEG/USO/data/' + i + '/epochs/' + i + '-epo.fif') for i in ids]

# convert result indexes to actual epoch indexes
actual_epoch_idx = {'USO/1': {participant: [] for participant in uso_ids_and_conditions},
                    'USO/2': {participant: [] for participant in uso_ids_and_conditions},
                    'USO/3': {participant: [] for participant in uso_ids_and_conditions},
                    'USO/4': {participant: [] for participant in uso_ids_and_conditions},
                    'USO/5': {participant: [] for participant in uso_ids_and_conditions}}

for condition in idx_list_ids_excluded:
    for participant_idx, participant_id in enumerate(idx_list_ids_excluded[condition]):
        if participant_id not in exclude_participant:
            for idx in idx_list_ids_excluded[condition][participant_id]:
                idx_array = epoch_data[participant_idx].selection == idx
                if np.any(idx_array):
                    epoch_idx = np.where(idx_array)[0][0]
                    actual_epoch_idx[condition][participant_id].append(epoch_idx)

del uso_ids_and_conditions
del idx_list_ids_excluded
del file
del ids
del listdir
del idx_array

# pick epochs
picked_epochs = {'USO/1': {participant: [] for participant in actual_epoch_idx['USO/1']},
                 'USO/2': {participant: [] for participant in actual_epoch_idx['USO/2']},
                 'USO/3': {participant: [] for participant in actual_epoch_idx['USO/3']},
                 'USO/4': {participant: [] for participant in actual_epoch_idx['USO/4']},
                 'USO/5': {participant: [] for participant in actual_epoch_idx['USO/5']}}

for condition in actual_epoch_idx:
    for participant_idx, participant in enumerate(actual_epoch_idx[condition]):
        picked_epochs[condition][participant] = (epoch_data[participant_idx][actual_epoch_idx[condition][participant]])

# exclude participants
for participant in exclude_participant:
    for condition in picked_epochs:
        del picked_epochs[condition][participant]

# create evoked
evoked_misaligned_USO_excl = {'USO/1': [],
                              'USO/2': [],
                              'USO/3': [],
                              'USO/4': [],
                              'USO/5': []}
for condition in picked_epochs:
    for participant in picked_epochs[condition]:
        evoked_misaligned_USO_excl[condition].append(picked_epochs[condition][participant].average())

evoked_misaligned_USO_excl_avrgd = {'USO/1': [],
                                    'USO/2': [],
                                    'USO/3': [],
                                    'USO/4': [],
                                    'USO/5': []}

for condition in evoked_misaligned_USO_excl_avrgd:
    evoked_misaligned_USO_excl_avrgd[condition] = mne.grand_average(evoked_misaligned_USO_excl[condition])

mne.viz.plot_compare_evokeds(evokeds=evoked_misaligned_USO_excl, ci=False, picks='FCz',
                             title='every USO in condition 5 excluded where any onset delay occured - FCz')



