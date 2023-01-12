from functions.create_one_back_evoked_functions import convert_result_idx_to_actual_epoch_idx, \
    exclude_participants_from_epoch_data, create_picked_epochs_dictionary,  create_evoked
import mne
exclude = ['4q868v', 'l6e5vs', 'omfdt1', 'u88rdo']


actual_epoch_idx = convert_result_idx_to_actual_epoch_idx(exclude=exclude)
epoch_data_selection = exclude_participants_from_epoch_data(exclude_idx=[5, 17, 19, 21])

epochs = create_picked_epochs_dictionary(actual_epoch_idx=actual_epoch_idx, epoch_data_selection=epoch_data_selection,
                                         current_conditions=[0, 1, 2, 3, 4, 5], one_back_conditions=[0, 1, 2, 3, 4, 5])

evokeds = create_evoked(type='all', epochs=epochs, current_conditions=[0, 1, 2, 3, 4, 5], one_back_conditions=[0, 1, 2, 3, 4, 5])

mne.viz.plot_compare_evokeds(evokeds=[
    evokeds[5][1],
    evokeds[5][2],
    evokeds[5][3],
    evokeds[5][4],
], picks='FCz')

for current_condition in range(len(evokeds)):
    for back_one_condition in range(len(evokeds[current_condition])):
        evokeds[current_condition][back_one_condition].comment = str(current_condition) + '_' + str(back_one_condition)

mne.write_evokeds('evokeds__one_back_condition_5-ave.fif', evoked=evokeds[5])




