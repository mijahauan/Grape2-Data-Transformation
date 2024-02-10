# Grape2-Data-Transformation
Some scripts to process Grape 2 data for WWV5, WWV10, and WWV20.

Invoke transform_v2.py as follows: python3 transform_v2.py input_raw_data.csv output-ready-data.csv.
python3 transform_v2.py 2024-01-25T080000Z_N0000033_RAWDATA.csv 2024-01-25T080000Z_N0000033-ready.csv
Keep the datetime in the filenames.

Then invoke graph_all3_v2.py as follows:
python3 graph_all3_v2.py 2024-01-25T080000Z_N0000033-ready.csv
This will produce 2 graphs for each of wwv5, wwv10, and wwv15 showing frequency components and a spectrogram.

The import statements in each python file will inform you of what libraries, e.g., matplotlib to install.
