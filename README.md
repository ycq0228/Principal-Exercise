##  Principal-Exercise
### Step 1: An overview of the project. The goal of my project to clean up the original dataset, perform data analysis on the cleaned dataset and generate some insights from the data. There are several components: 
#### a) Load the data and create an output of a cleaned data set. This process includes several steps: 1) Identify the data type, data shape, economic meaning of each column and row and replace the original column name with name that has better description after researching the credit bureau website. 2) Identify the missing data, outliers and anomalies that need special treatment. I have a set of rules to take care of the missing values, and delete the columns with more than 15% of missing values. 3) Identify the relationship between each column and row and perform some data exploratory analysis. 4) Prepare the data for modeling process, including remove the columns that have duplicated information and highly correlated columns. 
#### b) List the assumptions used to clean the data and summarize any anomalies that may have been noticed. After the first step, I performed additional data analysis to reorganize the data for the next step. Assumptions I made are mainly for interpolating the missing values, I.e., mean/median or regression analysis to interpolate those values assuming same trend/distribution for that column. 
#### c) Create a brief overview of the data using any preferred python visualization package. I mainly use matplotlib/seaborn and plotly package for visualization combing the FIPS code and geojson to create Choropleth Maps. 

### Step 2 : Instructions on how to run the script and generate outputs. 
##### Import the required python packages and run the entire script. 

### Step 3 : Any additional details or assumptions about the project you would like us to know.
#### Some columns are highly correlated, i.e., employment (total labor force and female labor force), although the data looks clean, they should be taken care of before modeling process due to multicollinearity. The current data is static not time series, which cannot provide changes over time for more insights. Such panel data is good to identify correlation but there is not ground truth (target variable in the dataset) which could use to identify the market trend. 

### If I have more time and know what specific product to work on , I will drill down the relevant columns (features) to the target output, and perform detailed feature engineering to prepare for the modeling process (either supervised or unsupervised modeling). 

## Thank you! :) 
