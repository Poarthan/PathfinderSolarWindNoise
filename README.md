# solarWindDataAnalysis

## Plots
All generated plots are in the plots folder, so no need to compile them once again.
```
cd plots
```
Time Series Plot:
```
eog TimeDomain_Comparison_ACEvLPF.png
```
Fast Fourier Transformation Plot:
```
eog ACE_and_LPF_Loglog.png
```

Coherence Plot(NOTE: these were a series of plots with different average segement lengths, the average segment length is stated in the title of the plots):
```
eog co_tests2/ACE_and_LPF_co.png
```
Bode Plot:
```
eog Bode_Phase_Plot.png
eog Bode_Magnitude_Plot.png
```
Noise cancellation plot:
```
eog LPF_Noise_Cancellation.png
```

## Setup
Everything here is designed for a Debian flavored Gnu/Linux operating system. python3, and pip3 need to be installed.
```
sudo apt install python3 python3-pip -y
```
To install all required python modules run:
```
pip install -r requirements.txt
```


## Getting Data
Runing these takes about 10 or so minutes, because there is a lot of data processing with huge datasets. So if you just want the dirend results from the plots go above to the plots

The original ACE data used can be accessed from this website: https://izw1.caltech.edu/ACE/ASC/level2/lvl2DATA_SWEPAM.html. 2016 data, UTC day, hour, min, sec, H+ density, He4/H+, H+ speed, and velocity x,y,z of solar wind ions in GSE coordinates is required.

For easier download just use: https://zenodo.org/record/6955182.

Download the data from the website, extract it to a new directory datafiles:
```
wget https://zenodo.org/record/6955182/files/ACE_data.tar.xz?download=1
mv -iv ACE_data.tar.xz?download=1 ACE_data.tar.xz
mkdir datafiles
tar -xvf ACE_data.tar.xz
mv -iv ACE_data.txt ./datafiles/ACE_data.txt
```
To prepare the ACE data, run:
```
python3 time_gen.py
python3 data_filter_gapFill.py
python3 ACE_Solar_Wind_Data_Calculate.py
```

For the LISA Pathfinder data, download it from this link(https://zenodo.org/record/6954044):
```
wget https://zenodo.org/record/6954044/files/LPF_Force_catalog.tar.xz?download=1
mv -iv LPF_Force_catalog.tar.xz?download=1  LPF_Force_catalog.tar.xz
tar -xvf LPF_Force_catalog.tar.xz
mv -iv ./catalog/ ./datafiles/catalog/
```
LISA Data instructions:
```
cd datafiles/catalog
ls g2_z_* > filenames_g2_z.txt
cd ../..
python3 huge_file_time.py
python3 huge_file_inversefft.py
python3 old_LISA_FULL_GAP_FILL.py
python3 LISA_filter.py
python3 LISA_gap_fill.py
```



## Usage
For the comparison between the 2 datasets run:
```
python3 loglog.py
python3 ACEvLISA_timeDomain.py
```

For Coherence between the datasets:
```
python3 ace_and_lisa_co.py
```

For Bode Plots:
```
python3 bode_plot.py
```

For Noise cancellation Plots:
```
python3 noise_sub.py
```
