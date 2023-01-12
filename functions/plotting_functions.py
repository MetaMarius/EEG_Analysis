import mne
import sys
eeg_tools_path = 'C:/Users/mariu/PycharmProjects/FreefieldLab/eeg_tools/src/eeg_tools'
sys.path.append(eeg_tools_path)
import pathlib
import os
from os import listdir
import settings
from analysis import get_evokeds

# getting data #

eeg_data_path = pathlib.Path('C:/EEG/USO/data')
ids = listdir(eeg_data_path)

# evokeds
evokeds, evokeds_avrgd = get_evokeds(settings.ids, settings.root_dir, return_average=True)
evokeds.pop('deviant')
evokeds_avrgd.pop('deviant')

raw_data = [mne.io.read_raw_fif('C:/EEG/USO/data/' + i + '/raw/' + i + '_raw.fif') for i in ids[0:2]]
epoch_data = [mne.read_epochs('C:/EEG/USO/data/' + i + '/epochs/' + i + '-epo.fif') for i in ids]

mne.read_evokeds(f"{folder_path}\\{id}-ave.fif", condition=condition)

def plot_evoked_per_condition(averaged=True, picks='FCz'):
    if averaged:
        mne.viz.plot_compare_evokeds(evokeds_avrgd, picks=picks, ci=False)
    else:
        mne.viz.plot_compare_evokeds(evokeds, picks=picks, ci=False)


def plot_raw(participant=int):
    raw_data[participant].plot()
