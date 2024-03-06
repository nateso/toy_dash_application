import pandas as pd
import json
import pickle
import geopandas as gpd
from datetime import datetime

def import_geo_poverty_data(pvty_pth, geo_pth, cntry_code='KHM'):
    mpi_df = pd.read_csv(pvty_pth)
    mpi_df = mpi_df[mpi_df.iso_country_code == cntry_code].reset_index(drop=True)

    # load the geodata
    with open(geo_pth) as f:
        cntry_geojson = json.load(f)
    geodata = gpd.GeoDataFrame.from_features(cntry_geojson['features'])

    # assume that the subnational regions are in the same order as they are in mpi_df (i.e., alphabetical)
    geodata['subnational_region'] = mpi_df['subnational_region']

    # merge the poverty data to the shapefile
    pvty_data = pd.merge(geodata, mpi_df[['subnational_region', 'mpi_region', 'hr_poor', 'hr_severe_poverty']],
                         on='subnational_region', how='left')

    return pvty_data

def import_project_data(project_pth):
    project_df = pd.read_csv(project_pth)
    # format the funding
    project_df['funding_format'] = [str(i / 1000000) + " Mio. USD" for i in project_df['funding']]

    return project_df

def import_indicator_df(indicator_pth):
    indicator_df = pd.read_csv(indicator_pth)
    indicator_df = indicator_df.loc[~indicator_df.project_id.isna(), :].reset_index(drop=True)
    indicator_df['ts'] = pd.to_datetime(indicator_df['date'], format='%Y-%m-%d')
    return indicator_df


