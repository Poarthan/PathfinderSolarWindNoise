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
