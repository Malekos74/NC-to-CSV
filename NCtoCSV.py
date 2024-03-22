""" 
    This code is used to convert a ECMWF .NC file into multiple CSV files that can later be used or saved on MongoDB
    
    IN:
        - Path to the NC file you want to convert
        - Path to the directory where you want to create a 'csv_files' folder where the conversion will occur

    OUT:
        - A folder will be created in the directory where there will be a folder for each time step
        - Each time step folder will contain all attributes each one in a CSV file
        - Each CSV file will be a latitude * longitude table where all observations will be saved (In scientific formatting)
    
    NB:
        - Be careful when inputting the path where the data will get saved, if you input a correct path (The path exists but you don't want to use that)
          the program will create the result folder there. 
    
[Malek Miled]
"""
import os
import netCDF4 as nc
import pandas as pd
import numpy as np

from tqdm import tqdm
from CSVtoJSON import csv_to_json


# Prints info about the NC file and returns the number of time_values
def extract_info(NCfile):
    print("\n")
    # Extract the time variable data
    time_values = NCfile.variables['time'][:]
    print(f"Number of time Values: {len(time_values)}")
    longitude_values = NCfile.variables['longitude'][:]
    print(f"Number of longitudes: {len(longitude_values)}")
    latitude_values = NCfile.variables['latitude'][:]
    print(f"Number of latitudes: {len(latitude_values)}")
    
    print("\n")
    return time_values

# Convert and format date values to be used as folder names
def format_date(NCfile):
    # Extract time values
    time_values = extract_info(NCfile)
    
    # Convert time values to datetime
    base_time = pd.to_datetime('1900-01-01 00:00:00', format='%Y-%m-%d %H:%M:%S')
    time_values_datetime = base_time + pd.to_timedelta(time_values, unit='h')
    
    formatted_dates = []
    
    for timestep_value in time_values_datetime:
        # Format the timestep value for a file name
        formatted_timestep = timestep_value.strftime("%Y-%m-%d_%H-%M-%S")
        formatted_dates.append(formatted_timestep)
        
    return formatted_dates

# Function to extract and save data for each time value with a progress bar
def extract_date(NCfile, dates, output_directory):
    total_steps = len(dates) * (len(NCfile.variables) - 3)  # Total number of time steps times the number of variables (excluding longitude, latitude, and time)
    
    with tqdm(total=total_steps, desc="Processing", unit="step") as pbar:
        for (i, date) in enumerate(dates):
            
            # Array to store variable names
            variable_names = []
            
            # Create a folder for each time value
            time_folder = os.path.join(output_directory, f"{date}")
            os.makedirs(time_folder, exist_ok=True)

            # Extract longitude data
            longitude_values = NCfile.variables['longitude'][:]

            # Extract data for the current time value
            for variable_name, variable_data in NCfile.variables.items():
                # Skip non-data variables (e.g., dimensions)
                if variable_name in ['longitude', 'latitude', 'time']:
                    continue
                
                # Append variable name to the list
                variable_names.append(variable_name)

                # Extract data for the current variable
                variable_values = variable_data[i]

                # Create data array including longitude values in the first row
                data_array = np.vstack([longitude_values, variable_values])

                # Save the variable data to a CSV file inside the time folder
                csv_filename = os.path.join(time_folder, f"{variable_name}.csv")
                np.savetxt(csv_filename, data_array, delimiter=",")

                # Update progress bar
                pbar.set_description(f"Time step {i + 1}/{len(dates)}")
                pbar.set_postfix({"Variable": variable_name})
                pbar.update(1)
             
            # TODO call function   
            # Convert CSV's into JSON
            # Call function to convert CSV files to JSON
            csv_to_json(variable_names, time_folder)

# All the heavy lifting    
def run_conversion():
    # Input the path of the NC file
    NCpath = input("Input the path of the NC file you want to convert into CSV's: ")

    # Check if the file exists
    if not os.path.isfile(NCpath):
        print("Error: File not found.")
    else:
        # Open the NetCDF file
        NCfile = nc.Dataset(NCpath, 'r')

        # Input the path where the 'csv_files' folder should be created
        output_directory = input("Input the path where you want to create the folder 'csv_files' (Press Enter for current directory): ")

        # If the user input is empty, use the current directory
        if not output_directory:
            output_directory = os.getcwd()

        # Check if the directory exists
        if not os.path.isdir(output_directory):
            print("Error: Output directory does not exist.")
        else:
            # Combine the path with 'csv_files'
            output_directory = os.path.join(output_directory, 'csv_files')
            
            # Format the dates
            formatted_dates = format_date(NCfile)

            # Extract and save data for each time value
            extract_date(NCfile, formatted_dates, output_directory)

            # Close the NetCDF file
            NCfile.close()

if __name__ == '__main__':
    run_conversion()