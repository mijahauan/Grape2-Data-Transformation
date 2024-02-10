# Grape2-Data-Transformation
## Some scripts to process Grape 2 data for WWV5, WWV10, and WWV20.

### Invoke transform_v2.py as follows: 
python3 transform_v2.py <path_to_input_raw_data.csv> <path_to_output_ready_data.csv>

For instance:

  ```python3 transform_v2.py 2024-01-25T080000Z_N0000033_RAWDATA.csv 2024-01-25T080000Z_N0000033-ready.csv```
  
The scripts use the datetime in the filenames so retain that usage.

## Invoke graph_all3_v2.py as follows: 
python3 graph_all3_v2.py <path_to_output_CSV_from_transform_v2.py.csv> 

For instance:

  ```python3 graph_all3_v2.py 2024-01-25T080000Z_N0000033-ready.csv```
  
This will produce PNG files containing 2 graphs for each of wwv5, wwv10, and wwv15.  One shows frequency components and the other a spectrogram. You will find examples of these above.

The import statements in each python file will inform you of what libraries (e.g., matplotlib, scipy, numpy) to install.
