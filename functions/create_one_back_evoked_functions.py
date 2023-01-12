import pathlib
from os import listdir
import mne
import json
import numpy as np
eeg_data_path = pathlib.Path('C:/EEG/USO/data')
ids = listdir(eeg_data_path)
print('reading in epoch data')
epoch_data = [mne.read_epochs('C:/EEG/USO/data/' + i + '/epochs/' + i + '-epo.fif') for i in ids]
print('reading in selection file')
epoch_selection_file = open('data/one_back_uso_epochs_new_new.json')
epoch_result_idx = json.load(epoch_selection_file)
print('finished')


def convert_result_idx_to_actual_epoch_idx(exclude, result_idx=epoch_result_idx):
    actual_epoch_idx = {}
    for participant_idx, participant_id in enumerate(result_idx):
        if participant_id not in exclude:
            epochs = [[list() for i in range(6)] for j in range(6)]
            for current_idx, current_condition in enumerate(result_idx[participant_id]):
                for one_back_idx, one_back_condition in enumerate(current_condition):
                    for idx in one_back_condition:
                        idx_array = epoch_data[participant_idx].selection == idx
                        if np.any(idx_array):
                            epoch_idx = np.where(idx_array)[0][0]
                            epochs[current_idx][one_back_idx].append(epoch_idx)
            actual_epoch_idx.update({participant_id: epochs})
    return actual_epoch_idx


def exclude_participants_from_epoch_data(exclude_idx):
    epoch_data_excl = epoch_data
    for index in sorted(exclude_idx, reverse=True):
        del epoch_data_excl[index]
    return epoch_data_excl


def pick_epochs(actual_epoch_idx, current_condition, one_back_condition, epoch_data_selection):
    epochs_per_condition = []
    for participant_idx, participant_id in enumerate(actual_epoch_idx):
        picked_epoch_idx = actual_epoch_idx[participant_id][current_condition][one_back_condition]
        epochs_per_condition.append(epoch_data_selection[participant_idx][picked_epoch_idx])
    return epochs_per_condition


def create_picked_epochs_dictionary(actual_epoch_idx, epoch_data_selection,
                                    current_conditions, one_back_conditions):
    print('picking epochs...')
    epochs_per_condition = [[list() for i in current_conditions] for j in one_back_conditions]
    for current_condition in current_conditions:
        for one_back_condition in one_back_conditions:
            epochs_per_condition[current_condition][one_back_condition] = pick_epochs(actual_epoch_idx=actual_epoch_idx,
                                                                                      epoch_data_selection=epoch_data_selection,
                                                                                      current_condition=current_condition,
                                                                                      one_back_condition=one_back_condition)
    print('finished')
    return epochs_per_condition


def create_evoked(type, epochs, current_conditions, one_back_conditions):
    evoked = [[list() for i in current_conditions] for j in one_back_conditions]
    print('Creating evokeds...')
    for current_condition in current_conditions:
        for one_back_condition in one_back_conditions:
            evoked_participant_list = []
            for participant in epochs[current_condition][one_back_condition]:
                evoked_participant = participant.average()
                evoked_participant_list.append(evoked_participant)
                if type == 'all':
                    evoked_all = mne.combine_evoked(evoked_participant_list, weights='equal')
                    evoked[current_condition][one_back_condition] = evoked_all
                else:
                    evoked[current_condition][one_back_condition] = evoked_participant_list
    print('Finished creating evokeds')
    return evoked

''''

mne.viz.plot_compare_evokeds(evokeds=evoked[0], picks='FCz')
del evoked_adjust[0][0]

evoked = []
for idx, participant in enumerate(epochs_1_2_per_participant):
    evoked.append(epochs_1_2_per_participant[idx].average())


evoked_all = mne.combine_evoked(evoked, weights='equal')
mne.viz.plot_compare_evokeds(evoked_all, picks='FCz', ci=False)
'''










