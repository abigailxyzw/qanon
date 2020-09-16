import pandas as pd
import datetime
import os
import pdb
from parse_json import parse_json
import yaml
import sys

def read_timezones():
    
    script_folderpath=os.path.dirname(os.path.abspath(__file__))
    yaml_filepath=os.path.join(script_folderpath, 'timezones.yaml') 

    timezones_dict = {}
    with open(yaml_filepath, 'r') as fh:
        timezones=yaml.safe_load(fh)
    for t in timezones:
        k = t.replace('/', '_')
        timezones_dict[k] = t
    
    return timezones_dict


def read_all_drops():
    script_folderpath=os.path.dirname(os.path.abspath(__file__))
    tsv_filepath=os.path.join(script_folderpath, 'data/all_drops/all_drops.tsv') 
    drops_df=read_basic_input(tsv_filepath)
    return drops_df

def read_basic_input(tsv_filepath):
    
    dtype={'name':str, 'trip_code':str, 'drop_number':int, 'post_id':str, 'timestamp':str, 'user_id':str, 'source':str, 'link':str}
    basic_df=pd.read_csv(filepath_or_buffer=tsv_filepath, dtype=dtype, sep='\t')
    basic_df['timestamp'] = pd.to_datetime(basic_df['timestamp'], utc=True)
    return basic_df

def split_by_tripcode_df(basic_df):
    tripcode_dict={}
    basic_df=basic_df.fillna(value={'trip_code': 'nocode'})
    
    tripcode_groups = basic_df.groupby('trip_code')
    for k,v in tripcode_groups.groups.items():
        tripcode_df=basic_df.loc[v].copy()
        tripcode_dict[k]=tripcode_df
    return tripcode_dict 

def split_by_tripcode():
    script_folderpath=os.path.dirname(os.path.abspath(__file__))

    tripcode_folderpath=os.path.join(script_folderpath, 'data/by_tripcode')

    basic_df=read_all_drops()
    tripcode_dict=split_by_tripcode_df(basic_df)

    for k,tripcode_df in tripcode_dict.items():
        tripcode_filepath=os.path.join(tripcode_folderpath, '%s.tsv' % k)
        tripcode_df.to_csv(tripcode_filepath, index=False, sep='\t')


def day_of_week_count(input_df, tz=None):
    copy_df=input_df.copy()
    if tz is not None:
        copy_df['timestamp'] = copy_df['timestamp'].dt.tz_convert(tz)
    copy_df['day_of_week'] = copy_df['timestamp'].dt.day_name()
    grouped = copy_df.groupby('day_of_week')
    dow_df=grouped['drop_number'].count()
    cats = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_df=dow_df.reindex(cats) 
    return dow_df

def hour_of_day_count(input_df, tz=None, debug=False):
    copy_df=input_df.copy()
    utc_timestamps=copy_df['timestamp']
    if tz is not None:
        copy_df['timestamp'] = copy_df['timestamp'].dt.tz_convert(tz)
    hours=range(24)
    copy_df['hour_of_day'] = copy_df['timestamp'].dt.hour
    grouped = copy_df.groupby('hour_of_day')
    tod_df=grouped['drop_number'].count()
    if debug:
        for k, v in grouped.groups.items():
            sys.stderr.write(tz + ', Hour: ' + str(k)+'\n')
            sys.stderr.write(str(utc_timestamps[v]) + '\n')
    tod_df=tod_df.reindex(hours, fill_value=0)
    return tod_df

def read_tripcode_files():
    script_folderpath=os.path.dirname(os.path.abspath(__file__))
    tripcode_folderpath=os.path.join(script_folderpath, 'data/by_tripcode')

    tripcode_dataframes={}
    for tripcode_filename in os.listdir(tripcode_folderpath):
        tripcode_filepath=os.path.join(tripcode_folderpath, tripcode_filename)
        trip_code = get_tripcode_from_filename(tripcode_filename)
        tripcode_df=read_basic_input(tripcode_filepath)
        tripcode_dataframes[trip_code]=tripcode_df
    return tripcode_dataframes
     
def read_hod_tripcode(fp_in):
    combined_df=pd.read_csv(filepath_or_buffer=fp_in, index_col=0, sep='\t')
    return combined_df

def read_dow_tripcode(fp_in):
    combined_df=pd.read_csv(filepath_or_buffer=fp_in, index_col=0, sep='\t')
    return combined_df

def combine_hod_data(hod_dict, tripcode=False):
    hod_df=pd.DataFrame()
    for k,v in hod_dict.items():
        v.fillna(0, inplace=True)
        as_df=pd.DataFrame(v)
        as_df['hour_of_day'] = as_df.index
        if tripcode:
            tc, tz=k
            #if tc=='!2jsTvXXmXs':
                #pdb.set_trace()
            as_df['timezone']=tz
            as_df['tripcode']=tc
            pivoted=as_df.pivot(index=['timezone', 'tripcode'], columns='hour_of_day', values='drop_number')
        else:
            as_df['timezone']=k
            pivoted=as_df.pivot(index='timezone', columns='hour_of_day', values='drop_number')
        hod_df = pd.concat([pivoted,hod_df])
    hod_df=hod_df.reset_index()
    hod_df.sort_values(by=0, inplace=True)
    return hod_df

def combine_dow_data(dow_dict, tripcode=False):
    dow_df=pd.DataFrame()
    for k,v in dow_dict.items():
        v.fillna(0, inplace=True)
        as_df=pd.DataFrame(v)
        as_df['day_of_week'] = as_df.index
        if tripcode:
            tc, tz = k
            as_df['timezone'] = tz
            as_df['tripcode'] = tc
            pivoted=as_df.pivot(index=['timezone', 'tripcode'], columns='day_of_week', values='drop_number')
        else:
            as_df['timezone'] = k 
            pivoted=as_df.pivot(index='timezone', columns='day_of_week', values='drop_number')
        dow_df = pd.concat([pivoted,dow_df])
    dow_df=dow_df[['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']]
    dow_df=dow_df.reset_index()
    dow_df.sort_values(by=['Monday'], inplace=True)
    return dow_df

def get_tripcode_from_filename(fn):
    return os.path.splitext(fn)[0]



