README

**The author of this codebase approaches the Qanon phenomenon from a skeptical perspective. The author views "Q" as a hoax, LARP, or operation. That said, the code offered by this repository is a simple set of aggregating and summary scripts using python 3.**

## Summary 

This python 3 codebase produces summary visualizations and analyses of the historical Qanon drops from the imageboards 4chan, 8chan, and 8kun.  It offers the ability to aggregate drop counts by hour of day, day of week, and to break out those datasets by tripcode (drop signature). It allows for the ability to vary these figures and analyses by any timezone on the globe. The hope is that this information will give clues to the location of the poster and that the code will provide a foundation for further analysis.

The author was able to run the code in python 3.7.5.

## Detailed Instructions

Make sure the python packages in `requirements.txt` are installed. You may want to do this within a python virtual environment.

Next, make sure the dataset `posts.json` is located in the subfolder `data/all_drops`.  You may want to replace the existing file with the latest version of [the dataset](https://keybase.pub/qntmpkts/data/json/posts.json).

Open the file `timezones.yaml` and uncomment the timezones for which you want the script to generate graphs and summary analyses.

The entrypoint to the code is `analyze.py.` Usage is as follows.

>usage: analyze.py [-h] [--reformat_json] [--split\_by\_tripcode]
                  [--make\_bar\_graphs]

>Print time of day and day of week data for the Q posts

> optional arguments:
> 
>  -h, --help	      
> show this help message and exit
> 
>  --reformat\_json      
> Reformat the json input as a tsv file (does not include the text of the drops themselves).
> 
>  --split\_by\_tripcode  
> Split parsed qanon input into tsv files by tripcode. Assumes
                       --reformat\_json has already been called.
                                            
>  --make\_bar\_graphs    
> Produces bargraphs (png format) and summary tables (tsv format) to show hour of day and day of week drop patterns. Call --reformat\_json and --split\_by\_tripcode first.
                       
Calling the script without arguments will run all three stages in order.

The output will appear in the following subfolders:

| Output Type | File Format | SubFolder |
|--------|-------------|------------
| all output       |  tsv     |  data/all_drops |
| output split by tripcode |tsv| data/by_tripcode|
| all output by hour of day (as bar graph) | png | pngs/all_drops/hod |
| all output by day of week (as bar graph) | png| pngs/all_drops/dow |
| all output by hour of day | tsv | analysis/all_drops/hod |
| all output by day of week | tsv | analysis/all_drops/dow |
| output by tripcode, day of week (as bar graph) | png | pngs/by_tripcode/dow |
| output by tripcode, hour of day (as bar graph) | png | pngs/by_tripcode/hod|
| output by tripcode, day of week | tsv | analysis/by_tripcode/dow |
| output by tripcode, hour of day | tsv | analysis/by_tripcode/hod  |

## Further Information

You can reach the code author at abigail.xyzw@gmail.com.
