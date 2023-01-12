import slab
import pathlib
from os import listdir
import mne
# create result files


def get_file_paths(root_path):
    participants = listdir(root_path)
    file_paths = {participant: [] for participant in participants}
    for participant in file_paths:
        folder_path = root_path + '/' + participant + '/'
        file_paths[participant] = [folder_path + f for f in listdir(folder_path)]
    return file_paths


def get_all_results(root_path='C:/Behavioural'):
    file_paths = get_file_paths(root_path=root_path)
    result_files = {participant: [] for participant in file_paths}
    for participant in file_paths:
        for file in file_paths[participant]:
            result_files[participant].append(slab.ResultsFile.read_file(file))
    return result_files


def get_stage_results(stage, root_path='C:/Behavioural'):
    file_paths = get_file_paths(root_path=root_path)
    stage_result_files = {participant: [] for participant in file_paths}
    for participants in file_paths:
        for file in file_paths[participants]:
            if stage == 'experiment':
                is_experiment = slab.ResultsFile.read_file(file, tag='stage') == 'experiment'
                if is_experiment:
                    stage_result_files[participants].append(slab.ResultsFile.read_file(file))
            elif stage == 'test':
                is_experiment = slab.ResultsFile.read_file(file, tag='stage') == 'test'
                if is_experiment:
                    stage_result_files[participants].append(slab.ResultsFile.read_file(file))
            elif stage == 'training':
                is_experiment = slab.ResultsFile.read_file(file, tag='stage') == 'training'
                if is_experiment:
                    stage_result_files[participants].append(slab.ResultsFile.read_file(file))
    return stage_result_files


def get_uso_ids(result_files):
    uso_ids = {participant: [] for participant in result_files}
    for participant in result_files:
        for file in result_files[participant]:
            for dictionary in file:
                if 'sequence' in dictionary:
                    uso_ids[participant].append(dictionary['sequence']['data'])
    return uso_ids


def concatenate_uso_ids(uso_ids):
    uso_ids_con = {participant: [] for participant in uso_ids}
    for participant in uso_ids:
        for round in uso_ids[participant]:
            # uso_ids_con[participant].append([{'sound_id': None}])
            for index in round:
                uso_ids_con[participant].append(index)
    return uso_ids_con


def get_trials(result_files):
    trials = {participant: [] for participant in result_files}
    for participant in result_files:
        for file in result_files[participant]:
            for dictionary in file:
                if 'sequence' in dictionary:
                    trials[participant].append(dictionary['sequence']['trials'])
    return trials


def concatenate_trials(trials):
    trials_con = {participant: [] for participant in trials}
    for participant in trials:
        for round in trials[participant]:
            # trials_con[participant].append(None)
            for trial in round:
                trials_con[participant].append(trial)
    return trials_con


def combine_trials_and_uso_ids(trials_con, uso_ids_con):
    combination = {participant: [] for participant in trials_con}
    for participant in uso_ids_con:
        for index in uso_ids_con[participant]:
            combination[participant].append(index[0])
    for participant in combination:
        for idx, dictionary in enumerate(combination[participant]):
            dictionary.update({'condition': trials_con[participant][idx]})
    return combination


def insert_ignored_indexes(result_files):
    eeg_data_path = pathlib.Path('C:/EEG/USO/data')
    ids = listdir(eeg_data_path)
    epoch_data = [mne.read_epochs('C:/EEG/USO/data/' + i + '/epochs/' + i + '-epo.fif') for i in ids]
    ignored_indexes = {participant: [] for participant in ids}
    for participant_idx, participant in enumerate(ignored_indexes):
        if participant in epoch_data[participant_idx].filename:
            for epoch_idx, epoch in enumerate(epoch_data[participant_idx].drop_log):
                if 'IGNORED' in epoch:
                    ignored_indexes[participant].append(epoch_idx)
    for participant in ignored_indexes:
        for idx in ignored_indexes[participant]:
            result_files[participant].insert(idx, {'sound_id': None,
                                                   'condition': None})
    return result_files
















