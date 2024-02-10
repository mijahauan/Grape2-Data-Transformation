import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import re

def extract_calibration_offsets(input_csv_path):
    """
    Extracts calibration offsets from the specified CSV file.

    Args:
        input_csv_path (str): The path to the input CSV file.

    Returns:
        list: A list of calibration offset values extracted from the file.
    """
    with open(input_csv_path, 'r') as file:
        for line in file:
            if line.startswith('# A/D Zero Cal Data'):
                parts = line.strip().split('Data')
                if len(parts) > 1:
                    cal_offsets_str = parts[1].strip()
                    cal_offsets = [int(offset.strip(), 16) for offset in cal_offsets_str.split(',') if offset.strip()]
                    return cal_offsets
    return []

def append_data_to_single_file(data_buffer, output_filename):
    """
    Appends buffered data to a single output file with a column for each receiver, plus a timestamp column.

    Args:
        data_buffer (dict): A dictionary containing buffered data for each receiver and timestamps.
        output_filename (str): The name of the output file to append the data to.
    """
    # Create a DataFrame ensuring the column order
    df = pd.DataFrame(data_buffer, columns=['timestamp', 'wwv5', 'wwv10', 'wwv15'])
    
    # Check if the file exists to determine if headers should be written
    try:
        with open(output_filename, 'x') as f:  # Attempt to create the file
            df.to_csv(f, index=False)  # If successful, write with header
    except FileExistsError:
        with open(output_filename, 'a') as f:  # File exists, append without header
            df.to_csv(f, index=False, header=False)

def process_and_append_data(input_csv_path, cal_offsets, output_filename):
    """
    Processes the CSV file and appends the processed data to an output file.

    Args:
        input_csv_path (str): The path to the input CSV file.
        cal_offsets (list): The calibration offsets for data adjustment.
        output_filename (str): The filename for the output CSV with processed data for all stations.
    """
    samples_processed = 0
    data_buffer = {'timestamp': [], 'wwv5': [], 'wwv10': [], 'wwv15': []}

    with open(input_csv_path, 'r') as file:
        for _ in range(25):  # Skip metadata lines
            next(file)

        current_timestamp = None
        for line in file:
            line = line.strip()
            if not line or line.startswith('C'):  # Skip empty and checksum lines
                continue
            if line.startswith('T'):
                current_timestamp = line[1:]  # Extract timestamp
                continue

            data = line.split(',')
            if len(data) == 3 and all(data):  # Process valid data lines
                for i, value in enumerate(data):
                    hex_value = int(value, 16)
                    signed_val = hex_value - 0x8000
                    calibrated_val = signed_val + (0x8000 - cal_offsets[i])
                    data_buffer[f'wwv{5*(i+1)}'].append(calibrated_val)
                data_buffer['timestamp'].append(current_timestamp)
                samples_processed += 1

            if samples_processed == 8000:  # Append and reset after each second of data
                append_data_to_single_file(data_buffer, output_filename)
                samples_processed = 0
                data_buffer = {'timestamp': [], 'wwv5': [], 'wwv10': [], 'wwv15': []}

def main():
    """
    Main entry point of the script. Parses command line arguments to read input and write processed data.
    """
    parser = argparse.ArgumentParser(description="Process radio observation data into a single file.")
    parser.add_argument("input_csv_path", help="The path to the input CSV file containing the observation data.")
    parser.add_argument("output_filename", help="The filename for the output CSV containing processed data for all stations.")
    
    args = parser.parse_args()
    
    cal_offsets = extract_calibration_offsets(args.input_csv_path)
    process_and_append_data(args.input_csv_path, cal_offsets, args.output_filename)

    print("Processing completed. Output file generated.")

if __name__ == "__main__":
    main()

