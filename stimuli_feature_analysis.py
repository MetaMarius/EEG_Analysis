import pandas as pd
import matplotlib as plt
USO_csv = pd.read_csv('data/USO_features.csv')

USO_csv.plot(kind='scatter',
             x='dist_group',
             y='onset_delay')

plt.show()
ids = [3, 10, 25, 18, 20, 14, 19, 27, 21, 17, 22,  5,  7,  2, 28, 11]
specific_id = 11
USO_csv[USO_csv.USO_id == specific_id].plot(kind='scatter', x='dist_group', y='onset_delay')


