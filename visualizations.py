import matplotlib.pyplot as plt
import pandas as pd
import pdb
from utils import *
import os
import sys

def plot_hod():
    script_folderpath=os.path.dirname(os.path.abspath(__file__))

    png_alldrops_folderpath =os.path.join(script_folderpath, 'pngs/all_drops/hod')
    png_tripcodes_folderpath=os.path.join(script_folderpath, 'pngs/by_tripcode/hod')
    
    analysis_alldrops_folderpath=os.path.join(script_folderpath, 'analysis/all_drops/hod')
    analysis_tripcode_folderpath=os.path.join(script_folderpath, 'analysis/by_tripcode/hod')
    alldrops_combined_filepath=os.path.join(analysis_alldrops_folderpath, 'combined.tsv')
    tripcode_combined_filepath=os.path.join(analysis_tripcode_folderpath, 'combined.tsv')
  
    alldrops_hod_dict = {}
    tc_hod_dict = {}

    #plot for the entire dataset
    all_drops_df=read_all_drops()
    timezones=read_timezones()
    for timezone_name, tz in timezones.items():
        print("Making all drops Hour of day pngs for %s" % tz)
        png_filepath =os.path.join(png_alldrops_folderpath, '%s.png' % timezone_name)
        my_hod_df=hour_of_day_count(all_drops_df, tz)
        alldrops_hod_dict[timezone_name] = my_hod_df
        make_hod_png(tz, my_hod_df, png_filepath)
    
    #plot for trip code
    tripcode_dict=read_tripcode_files()
    for tripcode, tripcode_df in tripcode_dict.items():
        for timezone_name, tz in timezones.items():
            print("Making %s Hour of day pngs for %s" % (tripcode, tz))
            png_filepath =os.path.join(png_tripcodes_folderpath, '%s_%s.png' % (tripcode, timezone_name))
            my_hod_df=hour_of_day_count(tripcode_df, tz)
            tc_hod_dict[(tripcode, timezone_name)] = my_hod_df
            make_hod_png(tz, my_hod_df, png_filepath)
   
    #combine analysis and output as tsv
    combined_hod_df=combine_hod_data(alldrops_hod_dict)
    combined_hod_df.to_csv(alldrops_combined_filepath, sep='\t')
 
    combined_hod_tc_df=combine_hod_data(tc_hod_dict, tripcode=True)
    combined_hod_tc_df.to_csv(tripcode_combined_filepath, index=False, sep='\t')

def plot_dow():
    
    script_folderpath=os.path.dirname(os.path.abspath(__file__))

    png_alldrops_folderpath =os.path.join(script_folderpath, 'pngs/all_drops/dow')
    png_tripcode_folderpath=os.path.join(script_folderpath, 'pngs/by_tripcode/dow')

    analysis_alldrops_folderpath=os.path.join(script_folderpath, 'analysis/all_drops/dow')
    analysis_tripcode_folderpath=os.path.join(script_folderpath, 'analysis/by_tripcode/dow')
    alldrops_combined_filepath=os.path.join(analysis_alldrops_folderpath, 'combined.tsv')
    tripcode_combined_filepath=os.path.join(analysis_tripcode_folderpath, 'combined.tsv')

    alldrops_dow_dict = {}
    tc_dow_dict = {}

    all_drops_df=read_all_drops()
    timezones=read_timezones()
    for timezone_name, tz in timezones.items():
        print("Making all drops Day of Week pngs for %s" % tz)
        png_filepath =os.path.join(png_alldrops_folderpath, '%s.png' % (timezone_name))
        my_dow_df=day_of_week_count(all_drops_df, tz)
        alldrops_dow_dict[timezone_name] = my_dow_df
        make_dow_png(tz, my_dow_df, png_filepath)
    
    tripcode_dict=read_tripcode_files()

    for tripcode, tripcode_df in tripcode_dict.items():
        for timezone_name, tz in timezones.items():
            print("Making %s Day of Week pngs for %s" % (tripcode, tz))
            png_filepath =os.path.join(png_tripcode_folderpath, '%s_%s.png' % (tripcode, timezone_name))
            my_dow_df=day_of_week_count(tripcode_df, tz)
            tc_dow_dict[(tripcode, timezone_name)] = my_dow_df
            make_dow_png(tz, my_dow_df, png_filepath)
    
    combined_dow_df=combine_dow_data(alldrops_dow_dict)
    combined_dow_df.to_csv(alldrops_combined_filepath, index=False, sep='\t')
 
    combined_dow_tc_df=combine_dow_data(tc_dow_dict, tripcode=True)
    combined_dow_tc_df.to_csv(tripcode_combined_filepath, index=False, sep='\t')


def make_dow_png(info, dow_df, png_filepath):

    dow_df.plot.bar()
    plt.title(info)
    plt.savefig(png_filepath)
    plt.close()

def make_hod_png(info, hod_df, png_filepath):
    
    hod_df.plot.bar()
    plt.title(info)
    plt.savefig(png_filepath)
    plt.close()


