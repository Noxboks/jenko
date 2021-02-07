from datetime import datetime
from meteostat import Stations, Daily
from pandas import read_csv, DataFrame, set_option

def _weather_data_extraction(lat, lon):
    start = datetime(2015, 1, 1)
    end = datetime(2021, 1, 16)

    stations = Stations()
    stations = stations.nearby(lat, lon)
    stations = stations.inventory('daily', (start, end))
    station = stations.fetch(1)

    data = Daily(station, start, end)
    data = data.fetch()

    return data

def _extract_weather_power_plants(_dataset):

    _dataset_list = []
    df_average = DataFrame()
    df_average['Global_tavg'] = ""
    df_average['Global_tmin'] = ""
    df_average['Global_tmax'] = ""
    df_average['Global_prcp'] = ""
    df_average['Global_snow'] = ""
    df_average['Global_wdir'] = ""
    df_average['Global_wspd'] = ""
    df_average['Global_wpgt'] = ""
    df_average['Global_pres'] = ""
    df_average['Global_tsun'] = ""

    counter = 0

    for i in range(len(_dataset)):
        print(i)
        latitude = _dataset.at[i, 'latitude']
        longitude = _dataset.at[i, 'longitude']
        name = _dataset.at[i, 'country']

        weather_data = DataFrame(_weather_data_extraction(latitude, longitude)).add_prefix(name + "_"+ str(i) + "_")
        weather_data.columns=['tavg', 'tmin', 'tmax', 'prcp', 'snow',
                              'wdir', 'wspd', 'wpgt', 'pres', 'tsun']

        weather_data = weather_data.fillna(0.0)

        set_option('display.max_columns', 50)

        if i == 0:
            df_average['Global_tmin'] = weather_data['tmin']
            df_average['Global_tmax'] = weather_data['tmax']
            df_average['Global_prcp'] = weather_data['prcp']
            df_average['Global_snow'] = weather_data['snow']
            df_average['Global_wdir'] = weather_data['wdir']
            df_average['Global_wspd'] = weather_data['wspd']
            df_average['Global_wpgt'] = weather_data['wpgt']
            df_average['Global_pres'] = weather_data['pres']
            df_average['Global_tsun'] = weather_data['tsun']
        else:
            df_average['Global_tmin'] += weather_data['tmin']
            df_average['Global_tmax'] += weather_data['tmax']
            df_average['Global_prcp'] += weather_data['prcp']
            df_average['Global_snow'] += weather_data['snow']
            df_average['Global_wdir'] += weather_data['wdir']
            df_average['Global_wspd'] += weather_data['wspd']
            df_average['Global_wpgt'] += weather_data['wpgt']
            df_average['Global_pres'] += weather_data['pres']
            df_average['Global_tsun'] += weather_data['tsun']

        # print(weather_data['tavg'])
        # print("avg")
        # print(df_average)
        # print("---")

        counter += 1

        # print(weather_data)
        # _dataset_list.append(weather_data)

    df_average['Global_tavg'] = df_average['Global_tavg'] / counter
    df_average['Global_tmin'] = df_average['Global_tmin'] / counter
    df_average['Global_tmax'] = df_average['Global_tmax'] / counter
    df_average['Global_prcp'] = df_average['Global_prcp'] / counter
    df_average['Global_snow'] = df_average['Global_snow'] / counter
    df_average['Global_wdir'] = df_average['Global_wdir'] / counter
    df_average['Global_wspd'] = df_average['Global_wspd'] / counter
    df_average['Global_wpgt'] = df_average['Global_wpgt'] / counter
    df_average['Global_pres'] = df_average['Global_pres'] / counter
    df_average['Global_tsun'] = df_average['Global_tsun'] / counter

    #return concat(_dataset_list, join='inner', axis=1)
    return df_average


dataset = read_csv('UE_Global_major_power_plants.csv', delimiter=",", engine='python')
dataset.columns = ['country', 'country_long', 'latitude', 'longitude', 'estimated_generation_gwh']
print(len(dataset))

complete = _extract_weather_power_plants(dataset)
complete = complete.fillna(0.0)
complete.to_csv('weather_data_major_power_plants_LARGE_3_UE_Country.csv', sep=',')
print(complete)

