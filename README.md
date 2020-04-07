# Detecting Political Bias Using Deep Learning
Detecting Political Bias in Speeches and News Articles in the US Using Deep Learning Methods 

Notes on Convote scraped dataset:
The test, development, and training sets were scraped from the Convote ```data_stage_three``` folder.

The data is stored in CSVs in the format ```text,party``` e.g. ```data,label```.

In the ```raw``` folder is the the raw textual data. 
The raw textual data has a lot of commas, so a semicolon ```;``` is used as a delimeter between text and party.

The ```stripped``` folder has the same text stripped of commas, and a comma ```,``` delimeter is used between text and party.