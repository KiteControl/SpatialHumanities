import pandas as pd
import scipy.spatial.distance
from scipy.spatial.distance import cdist
import numpy as np

unfall_data = pd.read_csv('/content/sample_data/sample_unfall.csv', delimiter=';')
demografische_data1 = pd.read_csv('/content/sample_data/sample_demographic.csv', delimiter=';')
demografische_data1[['x_mp_1km', 'y_mp_1km']] = demografische_data1[['x_mp_1km', 'y_mp_1km']].astype(float)

def finde_naechsten_datenpunkt(unfall, daten):
    unfall_koordinaten = [[unfall["LINREFX"], unfall["LINREFY"]]]
    datenpunkte_koordinaten = daten[['x_mp_1km', 'y_mp_1km']].astype(float)
    datenpunkte_koordinaten = datenpunkte_koordinaten.to_numpy().reshape(-1, 2)
    distanzen = cdist(unfall_koordinaten, datenpunkte_koordinaten, metric='euclidean')
    index_naechster_datenpunkt = distanzen.argmin()
    # print('#############################')
    # print(naechster_datenpunkt)
    return daten.iloc[index_naechster_datenpunkt]

naechster_datenpunkt = finde_naechsten_datenpunkt(unfall_data.iloc[0], demografische_data1)
# Füge demografische Daten zu den Unfalldaten hinzu
# demografische_data1['Klassierte Werte im 1 Kilometer-Gitter'] = ''

unfall_data['x_mp_1km'] = ''
unfall_data['y_mp_1km'] = ''
unfall_data['Einwohner'] = ''
unfall_data['unter18_A'] = ''
unfall_data['ab65_A'] = ''


for index, unfall in unfall_data.iterrows():
    print('#############################')
    print(naechster_datenpunkt)
    naechster_datenpunkt = finde_naechsten_datenpunkt(unfall, demografische_data1)
    unfall_data.at[index, 'x_mp_1km'] = naechster_datenpunkt['x_mp_1km']
    unfall_data.at[index, 'y_mp_1km'] = naechster_datenpunkt['y_mp_1km']
    unfall_data.at[index, 'Einwohner'] = naechster_datenpunkt['Einwohner']
    unfall_data.at[index, 'unter18_A'] = naechster_datenpunkt['unter18_A']
    unfall_data.at[index, 'ab65_A'] = naechster_datenpunkt['ab65_A']

# Speichere das Ergebnis als CSV
unfall_data.to_csv('/content/sample_data/unfalldaten_mit_demografischen_daten.csv', index=False)

