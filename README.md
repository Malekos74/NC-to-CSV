# NC to CSV
### Descrption:
This code is used to convert a ECMWF .NC file into multiple CSV files that can later be used or saved on MongoDB
### Input
  - Path to the NC file you want to convert
  - Path to the directory where you want to create a 'csv_files' folder where the conversion will occur
### Output
  - A folder will be created in the directory where there will be a folder for each time step
  - Each time step folder will contain all attributes each one in a CSV file
  - Each CSV file will be a latitude * longitude table where all observations will be saved (In scientific formatting)
### Notes
  - Be careful when inputting the path where the data will get saved, if you input a correct path (The path exists but you don't want to use that)
    the program will create the result folder there.
  - This script is tailored for the ECMWF NC files. They are readily available [here](https://data.aicnic.cn//ECMWF//)
