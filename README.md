# G09_screening
Script to do the screening of Gaussian09 .log files

## What this script do?
This script checks every output file from the Gaussian 09 Software in the folder and checks if the calculation terminated normally and all frequencies are real. Then, it creates and separates those files in 4 folders:
- finished outputs
  - For the files that terminated normally and has only real frequencies
- Imaginary_frequency
  - If it has imaginary frequencie
- Frequency_fail
  - If it failed to calculate the frequencies
- Geometry_fail
  - If it fail to converge the geometry

After that, it generates a "report.txt" file with the name of each file in each folder. 
