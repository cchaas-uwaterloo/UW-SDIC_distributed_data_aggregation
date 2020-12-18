# PI_LORD_Interface_Proj
For GTAA CBM project with SDIC lab. Client code to transfer data from deployed sensors to PI server and perform configuration and data processing functions.

## Overview
This package has been developped for the SDIC lab in the department of Civil and Environmental Engineering at the University of Waterloo as part of the Condition Based Modelling 
project in partnership with the Greater Toronto Airport Authority. It inlcudes modules for: 
1. Configuring the network of LORD sensors deployed at the airport 
2. Retrieving data written to LORD SensorCloud remote storage service by the deployed sensors
3. Performing processing operations on the collected data 
4. Writting raw and derived data to the SDIC PI server 
5. Retrieving and updating data from the SDIC PI server

This package remains under development.

## Contents 
- Installation and Setup  
- Modules 
  - Applications
  - Config
  - Data
  - Downloaders
  - Microstrain_data_diagnostics 
  - Operations
  - PI-Web-API-Client-Python
  - PI_Interface
  - Sensing_Config 
  - Tests
  - Util
- Oustanding Issues 
- TODO

## Installation and Setup
To run this package, just clone the source files and add the base directory to the Python path on your machine. 

## Modules

### Applications
Directory for main code meant to perform a task e.g. run a data analysis, update values in PI, etc. 

### Config 
Directory for configuration files e.g. list of links for updating SPC values for PI points in csv format. 

### Data
Data analysis file output. Meant to store convenient references to data analysis results. If any large files are added, make sure to add them to .gitignore. If they are larger than the Github file size limit, pushes to remote of the whole repository can be blocked.

### Downloaders
Interfaces with sensor software to access collected data. Currently implemented: 
- LMS_text_reader.py : read from text file exports from LMS 
- Node_data_reader.py : read data from Microstrain sensors internal storage 
- SensorCloud_reader.py : read data from LORD SensorCloud 
- WSDA_Downloader_Reader.py : (empty) data aggregator memory can currently only be accessed through legacy WSDA Data Downloader tool from LORD (accessed through SensorConnect), apparently an SDK will be coming out soon so we could make a custom accessor 

All downloaders will return a list of named tuples or data values and timestamps (something like this) :  
list(namedtuple('dataPoint', ['value', 'timestamp']))

This format can be passed directly to the basic feature calculation and output methods or converted to a Pandas framework for more complex operations.

### Microstrain_data_Diagnostics
Microstrain library. 

### Operations
Implementation derived data calculations. Currently implemented: 
- Mean 
- RMS 
- Variance
- Crest factor 
- Peak-to-peak
- Kurtosis
- Cumulative sum
- Standard deviation
- Frequency spectrum (just the output of an fft - can be used for mean frequency or other frequency domain operations

There are also two utilities to convert lists to numPy arrays used in all the derived data methods. One is GPU accelerated and more suited to very large data sets.

### PI-Web_API-Client-Python
PI API client library.

### PI_Interface
Methods for interfacing with the PI API. Methods are currently implemented to create new PI points (based on the Point_builder.csv file), delete existing PI points (based on the Point_cleaner.csv file), read data from a PI point, write data to a PI point, and update SPC values in PI for a raw or derived data point. 

Before any operations with the PI API are possible the application program must establish a connection to the server by calling the connectToPIServer method. The client and data server objects retrieved by this method can then be passed as required to the other methods. The necessary credentials for connecting to the SDICPI server are included in the comments in the PI_connection.py file. 

### Sensing_Config
Script for batch configuring the LORD Microstrain sensing network. Can be used as an alternative to SensorConnect for node configuration. An active connection with all the sensing nodes via the WSDA is required. The script is set up to configure: 
- nodes connected to the network
- sampling channels (raw and derived) on each node 
- sampling rates (raw and derived) on each node
- triggers on each node 
- node timeouts 
- network sampling protocol (synchronous/ asynchronous)

### Tests
Directory for unit tests and other scratch code.

### Util
General utilities including: 
- converting LORD -> PI timestamps
- writing data list to a text file
- segmenting data list 
- converting LMS -> PI timestamps

## Outstanding Issues 
**Issue**: LORD -> PI timestamp conversion is slow  
**Description**: the mscl timestamp string() accessor method doesn't work (as far as I can tell). Currently to get the timestamp, the reformatTimestamp method creates a text file, writes the mscl timestamp, reads it from the text file, closes the text file, then does the conversion to PI format. This is very slow. 

**Issue**: WSDA internal time switches time zones  
**Description**: The WSDA internal clock is sometimes not on EST when powered on. This might be due to connecting to my own computer that has timezone issues though. Can eb fixed by setting timezone in the WSDA control pannel. 

## TODO
Next steps:  
- implement conversion to Pandas framework from list of tuples used currently
- finish mean frequency implementation
