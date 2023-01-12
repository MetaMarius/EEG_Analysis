from functions.result_file_functions import get_all_results, get_stage_results, get_uso_ids, get_trials, concatenate_trials, concatenate_uso_ids, combine_trials_and_uso_ids, insert_ignored_indexes

# create result files #
result_files = get_all_results()
experiment_result_files = get_stage_results(stage='experiment')
uso_ids = get_uso_ids(result_files=experiment_result_files)
trials = get_trials(result_files=experiment_result_files)
trials_con = concatenate_trials(trials=trials)
uso_ids_con = concatenate_uso_ids(uso_ids=uso_ids)
uso_ids_and_conditions = combine_trials_and_uso_ids(trials_con=trials_con, uso_ids_con=uso_ids_con)
plus_ignored_indexes = insert_ignored_indexes(result_files=uso_ids_and_conditions)





