1) In the "../../data/raw" folder (relative to this README.md), create a "wfabba" folder. Finalized directory will be the following:
    "../../data/raw/wfabba"
    
2) Within "../../data/raw/wfabba", create the following folders:
    "GOES-16-2019", "GOES-16-2020", "GOES-16-2021", "GOES-16-Jan-2021","GOES-17-2019", "GOES-17-2020", "GOES-17-2021", "GOES-17-Jan-2021"

3) To get the WFABBA GOES-16 2021 - present data, please run the following: 
    wget -r --no-parent --reject "index.html*" https://sdge.sdsc.edu/data/wfabba/goes-16/
    
4) To get the WFABBA GOES-17 2021 - present data, please run the following: 
    wget -r --no-parent --reject "index.html*" https://sdge.sdsc.edu/data/wfabba/goes-17/ 

5) In the directory where the previous 2 commands were running, navigate to the following directory: "sdge.sdsc.edu/data/wfabba"
   Copy the contents of the "sdge.sdsc.edu/data/wfabba/goes-16" folder into "../../data/raw/wfabba/GOES-16-2021" (relative to this README.md).
   Copy the contents of the "sdge.sdsc.edu/data/wfabba/goes-17" folder into "../../data/raw/wfabba/GOES-17-2021" (relative to this README.md).
    
5) Download the WFABBA GOES-16/GOES-17 data from 2019, 2020, and January 2021 from here: https://swat.sdsc.edu/nc/s/Z38QTAMAaMJyycw
   The text files will be in .tar.gz files, so they will need to be extracted.
    
6) Copy the extracted files into their respective folders in "../../data/raw/wfabba/", i.e. GOES-16 2019 data into "../../data/raw/wfabba/GOES-16-2019"

```python

```
