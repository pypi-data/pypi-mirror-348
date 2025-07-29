# PebbleNet

A Python toolkit for collecting and processing water quality data from the Chesapeake Bay, integrating data from NOAA stations and Maryland's Eyes on the Bay monitoring program.

## Overview

This project provides tools to fetch and process:
- Real-time data from NOAA monitoring stations around the Chesapeake Bay
- Monthly water quality measurements from Maryland's Eyes on the Bay program

## Features

- **NOAA Data Collection**
  - Real-time weather and water quality measurements
  - Automatic data aggregation and daily averaging
  - Parameters include: wind speed/direction, water temperature, air temperature, pressure, and more

- **Eyes on the Bay Integration**
  - Monthly water quality measurements
  - Parameters include: dissolved oxygen, water temperature, secchi depth, salinity, and pH
  - Station location mapping

## Data Sources

- **NOAA Stations**: Real-time data from stations including:
  - BLTM2 (Baltimore)
  - CHCM2 (Cambridge)
  - TCBM2 (Tolchester Beach)
  - And more...

- **Eyes on the Bay Stations**: Monthly data from stations including:
  - CB10
  - CB11
  - WT51
  - CB32
  - WT41
  - CB31

## Output Format

### NOAA Data
Data is returned in JSON format, structured for easy integration with visualization tools:

```json
{
    "name": "WTMP",
    "labels": ["Jan 01", "Jan 02"],
    "values": [12.3, 12.5]
}
```

### Eyes on the Bay Data
Data is returned in JSON format with station, parameter, and monthly measurements:

```json
{
    "CB10": {
        "bdo": {
            "January": {
                "Surface": "9.8",
                "Bottom": "9.5",
                "Mean": "9.65",
                "StDev": "0.21",
                "Count": "2"
            },
            "February": {
                ...
            }
        },
        "wt": {
            ...
        }
    }
}
```
## Dependencies

- Python 3.x
- requests
- beautifulsoup4
