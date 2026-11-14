- It is difficult to select variables that could indicate change. 
- The challenge is about creating a tool that can 
  - select variables measured by Earth science missions or produced by Earch science models
  -  visualize how they change over time, and determine what is changing
  -  where it is changing
  -  how much it is changing
  -  and if these changes are what scientists call "Significant"!
-  From the video, when there is a significant sulfer spead on a wide area, they call that a significant cooling trend. 
-  One example they provided was the wildfires happens in Canada, and affects the air quality in USA. They used a metric called **Aerosol Optical Depth (AOD)** - a variable that indicates how much the transmission of light is reduced by the presence of substances in the air, like particales that compose smoke. 
-  Then they made a time-series of AOD using data from the Moderate Resolution Imaging Spectroradiometer (MODIS) on the Aqua satellite. 
- This instrument began observing the Earth in 2002
- The time-series will average the value of AOD over the entire state of Wisconsin for every month since the observation began. 
- To determine if it was significant or not, they used something called p-value of the time-series. 
  - If the p-value is less than 0.05, the time-series meets the standard for significance - it is a significant trend. 
  - If the p-value is more than 0.05, then it does not meet the standard. However, it does not also mean that it is not a trend, because sometimes to be a trend, it just need to be longer time-series. 

## Steps to follow to be an Earth Science data Trend Detective with NASA data
- Our app should be able to do the following:
  - Decide on the data variables for analysis. 
  - Choose a region for the analysis. (It can be the entrie world).
  - Select the time-period for the time-series. 
  - Select the time-series and examine it. Does it appear to have a trend. 
  - Analyze the trend for significance. 
- We also need to understand what does trend mean, what is a time-series, how can we measure p-values, and how can we decide the significance. 
  - Trend means changes that moves in particular direction over time. 


### Notes:
- NASA has a lot of data, we can work on one particular type:
  - rainfall
  - soil moisture
  - or we can work on different kinds of data. 
- Choosing the data can be more complicated than doing the analysis. 
- NASA datasets can have datapoints with different time periods (e.g. every hour, every 3 hours, etc...), it is easier to determine the trends over time for data points that are weekly or monthly. 
- We can use instruments like:
  - Moderate resolution imaging spectroradiometer (MODIS)
  - Ozone monitoring instrument (OMI)
  - Atmospheric infrared sounder (AIRS)
  - Global Preciotion measurement (GPM)
- There are some data sites that offer tools to generate time-series, and statistical analysis packages providing basic significance testing. 
- Try to select the daily or monthly data, it is a best fit. 
- Consider looking for publicly available tools for plotting hydrological data offered by outside organisations like Consortium of Universities for advancement science. 

### Challenges:
1. There is a wide variety of variables that can be studied. 
2. There can be a changes in a particular variable in one particular region moving in one direction, and in another region moving in the opposite direction for the same variable. 
3. There are two important parts to this problem:
   1. Finding variables that are trending, from simple ones like temp, and rainfall to more complex like evaporation and streamflow
   2. Analyzing the trends in particular regions of the land, ocean, or even levels of the atmosphere. 
    
## Objectives
- Successful solution can be:
  1. Identify Earth science variabes of interest that can be investigated for potential trends. 
    - NASA and other space agencies already offer some variables, we can select from them. 
  2. Acquire the data variables for a particular region, because most trends will not be global. 
  3. Generate and visualize a time series for the variable and region of interest over a long enough period of time to allow statistical analysis. 
  4. Finally, perform statistical analysis of that time series, indicating the rate of the change over time, and test the trend's significance using methods such as t-test, Mann-Kendall test, or confidence intervals. 
- A submission that does both visualization and analysis meets the full scope of the challenge. 
  
## Nice to have
- Basic knowledge of scientific terminology and statistical analysis. 
- Providing a short definition to each used variable is a plus => We should include it. 

## How to win and present it well
- We should be able to respond to the short series questions about what or where they woul