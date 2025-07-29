from pebblenet.Maryland.eotb_data import get_eotb_stations, eotb_stations_to_json
from pebblenet.Maryland.noaa_data import process_noaa_rt_stations

def process_eotb_data():
    chesapeake_stations = ["BLTM2", "CHCM2", "TCBM2", "FSKM2", "CPVM2", "APAM2",
                           "44063", "TPLM2", "BSLM2", "CAMM2", "44062", "COVM2",
                           "SLIM2", "BISM2", "PPTM2", "44042"]
    eotb_station_loc, eotb_stations = get_eotb_stations()
    monthly_data: str = eotb_stations_to_json(['CB10', 'CB11', 'WT51', 'CB32', 'WT41', 'CB31']) #json formatted string
    return monthly_data

def process_noaa_data():
    chesapeake_stations = ["BLTM2", "FSKM2", "TCBM2", "LTQM2", "CHCM2", "CPVM2",
                           "ARAM2", "44063", "TPLM2", "CXLM2", "CAMM2", "BISM2",
                           "44042", "SLIM2", "COVM2", "44062", "BRIM2", "BSLM2"]
    real_time_data: str = process_noaa_rt_stations(chesapeake_stations) #json formatted string
    return real_time_data

if __name__ == "__main__":
    process_noaa_data()
