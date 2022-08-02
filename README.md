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

Coherence Plot(NOTE: these were a series of plots with different average segement lengths, the average segment length is stated in the title of the plots):
```
eog co_tests2/*
```
Bode Plot:
```
eog Bode*
```
Noise cancellation plot:
```
eog LPF_Noise_Cancellation.png
```

##Getting Data
There will some cleaning up of the code for easier use.
ACE data used can be accessed from this website: https://izw1.caltech.edu/ACE/ASC/level2/lvl2DATA_SWEPAM.html. 2016 data, UTC day, hour, min, sec, H+ density, He4/H+, H+ speed, and velocity x,y,z of solar wind ions in GSE coordinates is required.

Download the data from the website, extract it to a new directory datafiles:
```
unzip ~/Downloads/[ACE_data].zip -d ./datafiles
mv -iv ./datafiles/A* ./datafiles/ACE_data.txt
```
To prepare the ACE data, run:
```
python3 time_gen.py
python3 data_filter_gapFill.py
python3 ACE_Solar_Wind_Data_Calculate.py
```

For the LISA Pathfinder data, download it from this link: (to be added)
```
tar -tzf ~/Downloads/g2_lisa_filtered_data.tar.xz
mv -iv ./g2_LPF_full.txt ./datafiles
```
The LPF data will be updated later




## Usage
For the original 4 data plots just run spacecraftDataPlot.py
```
python3 spacecraftDataPlot.py
```

For the Recreation of the Time series domain and the FFT Amplitude Spectrum plots, run:
```
python3 spacecraftTimeDomain.py
```

For the graphs of the full LISA Pathfinder TimeSeriesDomain and FFT Amplitude Spectrum run:
```
python3 full_TimeseriesDomain_plot_with_gaps.py
```
without gaps(this program is still not perfect):
```
python3 LISA_FULL_GAP_FILL.py
python3 full_TimeseriesDomain_plot.py
```

For the ACE dataplots, the data needs to be filtered, force needs to be calculated then plotted, the steps are shown with 2000_dataset as example:
```
python3 data_filter.py datafiles/2000_data_concise.txt
python3 ACE_Solar_Wind_Data_Calculate.py datafiles/2000_data_concise_Filtered_Data.txt
python3 ACE_SolarWindForcePlot.py datafiles/2000_data_concise_Filtered_Data_calculated_data.txt datafiles/2000_time_seconds.txt
```
Syntax:
```
python3 data_filter.py [unfiltered data]
python3 ACE_Solar_Wind_Data_Calculate.py [filtered data]
python3 ACE_SolarWindForcePlot.py [filtered and calculated data] [time data]
```

For the comparison between the 2 datasets run:
```
python3 aceVlisa_betterFFT.py
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
