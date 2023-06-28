#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import missingno as msno
import matplotlib.pyplot as plt 
import seaborn as sns
import sys
import os
import statsmodels.api as sm
import math
import plotly.express as px #graphing
import plotly.graph_objects as go #graphing
from plotly.subplots import make_subplots #graphing
from datetime import datetime, timedelta


# In[2]:


#!pip install missingno


# In[3]:


path = "/Users/ycq/Downloads/Principal/"
df =pd.read_csv(path + "/Quant Exercise.csv")


# ### Exploratory Data Analysis 

# In[4]:


df.head(), df.info(), df.shape


# In[18]:


df.describe(), df.columns, df.isnull().sum()


# In[19]:


df.dtypes


# ##### Sourced from credit bureau data
#  
# The column header names do not provide a good description of the data. I located the columns that I wanted to use and created a dictionary with the key value pairs for the column header names which can be seen below.
# 
# I also added a FIPS county code column to the dataset for each county in Pennsylvania. FIPS is a five-digit Federal Information Processing Standards code which uniquely identifies counties in the United States. We can use FIPS along with geojson to create Choropleth Maps. 

# In[12]:


# Dictionary of all renamed columns
# All of the renamed columns are ESTIMATES from the U.S. Census Bureau
# Columns not renamed include: Percent (PE), Margin of Error (M), Percent Margin of Error (PM)

dict = {# Employment Status
        # Population 16 years and over
        "DP03_0001E" : "total_population", # Total Population elgible for work
        "DP03_0002E" : "labor_force",
        "DP03_0003E" : "civ_labor_force",
        "DP03_0004E" : "total_employed",
        "DP03_0005E" : "total_unemployed",
        "DP03_0006E" : "armed_forces",
        "DP03_0007E" : "not_in_labor_force",
    

        # Females 16 years and over
        "DP03_0010E" : "total_population_female", # Total Population elgible for work
        "DP03_0011E" : "labor_force_female",
        "DP03_0012E" : "civ_labor_force_female",
        "DP03_0013E" : "civ_labor_force_female_employed",
    

        # Households with children
        "DP03_0014E" : "household_children_under_6", # Own children of the householder under 6 years
        # All parents in family in labor force
        "DP03_0015E" : "parents_work_children_under_6", # Own children of the householder under 6 years
        "DP03_0016E" : "household_children_6to17", # Own children of the householder 6 to 17 years
        # All parents in family in labor force
        "DP03_0017E" : "parents_work_children_6to17", # Own children of the householder 6 to 17 years
    

        # Commuting to work
        "DP03_0018E" : "total_workers_commute",
        "DP03_0019E" : "solo_vehicle_commute", # Car, truck, or van -- drove alone
        "DP03_0020E" : "carpool_commute", # Car, truck, or van -- carpooled
        "DP03_0021E" : "public_transportation_commute", # Public transportation (excluding taxicab)
        "DP03_0022E" : "walked_commute",
        "DP03_0023E" : "other_means_commute",
        "DP03_0024E" : "worked_from_home",
        "DP03_0025E" : "mean_commute_time_minutes",
    

        # Occupation
        "DP03_0027E" : "manage_business_sci_art", # Management, business, science, and arts occupations
        "DP03_0028E" : "service_occupations",
        "DP03_0029E" : "sales_and_office_occupations",
        # Natural resources, construction, and maintenance occupations
        "DP03_0030E" : "nr_construction_and_maintenance",
        # Production, transportation, and material moving occupations
        "DP03_0031E" : "production_transportation_mm",
    

        # Industry
        "DP03_0033E" : "ag_forest_fish_hunt_mine", # Agriculture, forestry, fishing and hunting, and mining
        "DP03_0034E" : "construction",
        "DP03_0035E" : "manufacturing",
        "DP03_0036E" : "wholesale_trade",
        "DP03_0037E" : "retail_trade",
        "DP03_0038E" : "transportation_warehousing_utilities",
        "DP03_0039E" : "information",
        "DP03_0040E" : "firerl", # Finance, insurance, real estate, rental and leasing
        # Professional, scientific, and management, and administrative and waste management services
        "DP03_0041E" : "psmawms",
        # Educational services, and health care and social assistance
        "DP03_0042E" : "education_health_care_social",
        # Arts, entertainment, and recreation, and accommodation and food services
        "DP03_0043E" : "art_entertainment_accommodation",
        "DP03_0044E" : "other_services", # Other services, except public administration
        "DP03_0045E" : "public_administration",
    

        # Class of worker
        "DP03_0047E" : "private_wage_and_salary_worker",
        "DP03_0048E" : "government_worker",
        "DP03_0049E" : "self_employed_worker", # Self-employed in own not incorporated business workers
        "DP03_0050E" : "unpaid_family_worker",
    

        # Income and benefits (in 2020 inflation-adjusted dollars)
        # Total households
        "DP03_0051E" : "total_households",
        "DP03_0052E" : "household_less_than_10k",
        "DP03_0053E" : "household_10k_to_15k", # $10,000 to $14,999
        "DP03_0054E" : "household_15k_to_25k", # $15,000 to $24,999
        "DP03_0055E" : "household_25k_to_35k", # $25,000 to $34,999
        "DP03_0056E" : "household_35k_to_50k", # $35,000 to $49,999
        "DP03_0057E" : "household_50k_to_75k", # $50,000 to $74,999
        "DP03_0058E" : "household_75k_to_100k", # $75,000 to $99,999
        "DP03_0059E" : "household_100k_to_150k", # $100,000 to $149,999
        "DP03_0060E" : "household_150k_to_200k", # $150,000 to $199,999
        'DP03_0061E' : "household_200k_plus", # $200,000 or more
        "DP03_0062E" : "household_median_income", # dollars
        "DP03_0063E" : "household_mean_income", # dollars

    
        # Families
        "DP03_0075E" : "total_families",
        "DP03_0076E" : "family_less_than_10k",
        "DP03_0077E" : "family_10k_to_15k", # $10,000 to $14,999
        "DP03_0078E" : "family_15k_to_25k", # $15,000 to $24,999
        "DP03_0079E" : "family_25k_to_35k", # $25,000 to $34,999
        "DP03_0080E" : "family_35k_to_50k", # $35,000 to $49,999
        "DP03_0081E" : "family_50k_to_75k", # $50,000 to $74,999
        "DP03_0082E" : "family_75k_to_100k", # $75,000 to $99,999
        "DP03_0083E" : "family_100k_to_150k", # $100,000 to $149,999
        "DP03_0084E" : "family_150k_to_200k", # $150,000 to $199,999
        "DP03_0085E" : "family_200k_plus", # $200,000 or more
        "DP03_0086E" : "family_median_income", # dollars
        "DP03_0087E" : "family_mean_income", # dollars
        "DP03_0088E" : "per_capita_income",

    
        # Nonfamily Households
        "DP03_0089E" : "total_nonfamily_households",
        "DP03_0090E" : "nonfamily_median_income", # dollars
        "DP03_0091E" : "nonfamily_mean_income", # dollars
    
    
        # Median Earnings
        "DP03_0092E" : "median_earnings_for_workers", # dollars
        "DP03_0093E" : "median_earnings_male_fulltime", # dollars
        "DP03_0094E" : "median_earnings_female_fulltime", # dollars

    
        # Health Insurance Coverage
        "DP03_0095E" : "total_civ_population", # Total Civilian Noninstitutionalized Population
        "DP03_0096E" : "civ_health_insurance_coverage", # Population
        "DP03_0097E" : "civ_private_health_insurance", # Population
        "DP03_0098E" : "civ_public_health_insurance", # Population
        "DP03_0099E" : "civ_no_health_insurance"} # Population

df.rename(columns = dict, inplace = True)


# In[13]:


df = df.dropna(axis=1, how="all")


# In[14]:


df.head()


# In[15]:


df.tail(), df.county.nunique


# In[16]:


df0 = df[df["county"] == "Pennsylvania"]
df = df[df["county"] != "Pennsylvania"]


# In[17]:


print(df.county.unique())


# #### Above is most of the data cleaning process, with labeling, missing value treatment, data formatting. 

# ### Data Visulization - a brief overview of the data 

# In[29]:


plt.rcParams["figure.figsize"] = (12, 8)


# In[30]:


# Importing county data for Plotly Choropleth Maps
from urllib.request import urlopen
import json
with urlopen("https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json") as response:
    counties = json.load(response)


# In[31]:


#Pennsylvania Household Income and Benefits 

plt.style.use('seaborn-dark')
plot = df0[["county", "household_less_than_10k", "household_10k_to_15k", "household_15k_to_25k",
                      "household_25k_to_35k", "household_35k_to_50k", "household_50k_to_75k",
                      "household_75k_to_100k", "household_100k_to_150k", "household_150k_to_200k",
                      "household_200k_plus"]].plot(x = "county", kind = "bar", cmap = "Spectral")

plt.grid(axis = 'y', alpha = 0.3)
plot.set_xticklabels(plot.get_xticklabels(), rotation = 360, fontsize = 20)
plt.title("Distribution of Pennsylvania Total Household Income", fontsize = 25)
plt.legend(bbox_to_anchor = (1.02, 1), loc = 2, borderaxespad = 0, fontsize = 15)


# In[35]:


# Percentage of Households with less than $50,000 income 

df["household_less_than_50k"] = df["household_less_than_10k"] + df["household_10k_to_15k"] + df["household_15k_to_25k"] + df["household_25k_to_35k"] + df["household_35k_to_50k"]

df["household_less_than_50k_percentage"] = (df["household_less_than_50k"]/df["total_households"]) * 100

fig = px.choropleth_mapbox(df, geojson = counties, locations = "fips", 
                           color = "household_less_than_50k_percentage",
                           color_continuous_scale = "Reds",
                           mapbox_style = "carto-darkmatter",
                           zoom = 6.25, center = {"lat": 41, "lon": -77.65},
                           hover_name = "county",
                           labels = {"household_less_than_50k_percentage": "% Household < $50,000 💰"}
                          )
                                     
fig.update_layout(margin = {"r": 0,"t": 0,"l": 0,"b": 0})
fig.update_layout(template = "plotly_white")
fig.show()


# In[36]:


# Percentage of Households with more than $100,000 income 

df["household_100k_plus"] = df["household_100k_to_150k"] + df["household_150k_to_200k"] + df["household_200k_plus"]

df["household_100k_plus_percentage"] = (df["household_100k_plus"]/df["total_households"]) * 100

fig = px.choropleth_mapbox(df, geojson = counties, locations = "fips", 
                           color = "household_100k_plus_percentage",
                           color_continuous_scale = "Greens",
                           mapbox_style = "carto-darkmatter",
                           zoom = 6.25, center = {"lat": 41, "lon": -78},
                           hover_name = "county",
                           labels = {"household_100k_plus_percentage": "% Household > $100,000 💰"}
                          )
                                     
fig.update_layout(margin = {"r": 0,"t": 0,"l": 0,"b": 0})
fig.update_layout(template = "plotly_white")
fig.show()


# #### Pennsylvania Employment Analysis
# 
# 

# In[40]:


# Total Employment Rate

df["employment_rate"] = (df["total_employed"]/df["labor_force"]) * 100

fig = px.choropleth_mapbox(df, geojson = counties, locations = "fips", 
                           color = "employment_rate",
                           color_continuous_scale = "RdBu_r",
                           range_color = (91.5, 97.5),
                           mapbox_style = "carto-darkmatter",
                           zoom = 6.25, center = {"lat": 41, "lon": -77.65},
                           hover_name = "county",
                           hover_data = ["total_employed", "total_unemployed"],
                           labels = {"employment_rate": "Employment Rate",
                                     "total_employed": "Total Employed",
                                     "total_unemployed": "Total Unemployed"}
                          )

fig.update_layout(margin = {"r": 0,"t": 0,"l": 0,"b": 0})
fig.update_layout(template = "plotly_dark")
fig.show()


# In[41]:


# Employment Rate Percentage by County¶


df["labor_force_male"] = df["labor_force"] - df["labor_force_female"]
df["total_male_employed"] = df["total_employed"] - df["civ_labor_force_female_employed"]
df["employment_rate_male"] = (df["total_male_employed"]/df["labor_force_male"]) * 100
df["employment_rate_female"] = (df["civ_labor_force_female_employed"]/df["civ_labor_force_female"]) * 100


plt.style.use("Solarize_Light2")

x1 = df.employment_rate_male
x2 = df.employment_rate_female
x3 = df.employment_rate
y = df.county

plt.figure(figsize = (6, 14), dpi = 80)
plt.scatter(x1, y, color = "#0000FF", edgecolors = "#000000", s = 50, alpha = 0.75, label = "Male Employment Rate %")
plt.scatter(x2, y, color = "#FF00FF", edgecolors = "#000000", s = 50, alpha = 0.75, label = "Female Employment Rate %")
plt.plot(x3, y, color = "#000000", alpha = 0.5, linestyle = "dashed", label = "Total Employment Rate %")
plt.grid(color = "#d3d3d3", linestyle = '-', linewidth = 0.75)
plt.title("Employment Rate % by County")
plt.xlabel("Employment Rate Percentage")
plt.ylabel("")
plt.legend(loc = 2)
plt.show()


# In[ ]:





# #### Pennsylvania Median Earnings by County 
# 

# In[42]:


#Pennsylvania Median Earnings by County 


plt.style.use("Solarize_Light2")

x1 = df.median_earnings_for_workers
x2 = df.median_earnings_male_fulltime
x3 = df.median_earnings_female_fulltime
y = df.county

plt.figure(figsize = (8, 14), dpi = 80)
plt.scatter(x1, y, color = "#000000", alpha = 1, s = 12, label = "All Workers")
plt.plot(x1, y, color = "#000000", alpha = 0.75)
plt.scatter(x2, y, color = "#0000FF", edgecolors = "#000000", label = "Male Full Time")
plt.plot(x2, y, color = "#0000FF", alpha = 0.75, linestyle = "--")
plt.scatter(x3, y, color = "#FF00FF", edgecolors = "#000000", label = "Female Full Time")
plt.plot(x3, y, color = "#FF00FF", alpha = 0.75, linestyle = "--")
plt.grid(color = "#d3d3d3", linestyle = '-', linewidth = 2)
plt.title("Pennsylvania Median Earnings by County")
plt.xlabel("Median Earnings (dollars)")
plt.ylabel("")
plt.legend(loc = 1)
plt.show()


# In[43]:


#Pennsylvania Per Capita Income by County


plt.style.use("seaborn-dark")

x = df.per_capita_income
y = df.county

plt.figure(figsize = (8, 14), dpi = 80)
plt.scatter(x, y, color = "#00DB16", alpha = 1, s = 100, edgecolors = "#d3d3d3", label = "Per Capita Income (USD)")
plt.plot(x, y, color = "#00DB16", linestyle = "dotted")
plt.grid(color = "#d3d3d3", linestyle = '-', linewidth = 0.25)
plt.title("Pennsylvania Per Capita Income by County")
plt.xlabel("Per Capita Income (dollars)")
plt.ylabel("")
plt.legend(loc = 1)
plt.show()


# #### How People in Pennsylvania Commute to Work

# In[44]:


# Percentage Worked From Home 


df["worked_from_home_percentage"] = (df["worked_from_home"]/df["total_workers_commute"]) * 100

fig = px.choropleth_mapbox(df, geojson = counties, locations = "fips", 
                           color = "worked_from_home_percentage",
                           color_continuous_scale = "Viridis",
                           mapbox_style = "carto-darkmatter",
                           zoom = 6.25, center = {"lat": 41, "lon": -77.65},
                           hover_name = "county",
                           labels = {"worked_from_home_percentage": "% Working From Home"}
                          )

fig.update_layout(margin = {"r": 0,"t": 0,"l": 0,"b": 0})
fig.update_layout(template = "plotly_dark")
fig.show()


# #### Pennsylvania Health Insurance Coverage Analysis

# In[45]:


#civ_health_insurance_coverage_percentage

df["civ_health_insurance_coverage_percentage"] = (df["civ_health_insurance_coverage"]/df["total_civ_population"]) * 100

fig = px.choropleth_mapbox(df, geojson = counties, locations = "fips", 
                           color = "civ_health_insurance_coverage_percentage",
                           color_continuous_scale = "Picnic",
                           mapbox_style = "carto-darkmatter",
                           zoom = 6.25, center = {"lat": 41, "lon": -77.65},
                           hover_name = "county",
                           labels = {"civ_health_insurance_coverage_percentage": "Percentage w/ Health Insurance 🏥"}
                          )
                                     
fig.update_layout(margin = {"r": 0,"t": 0,"l": 0,"b": 0})
fig.update_layout(template = "plotly_dark")
fig.show()


# In[ ]:





# In[ ]:





# In[46]:


#!pip install geopandas==0.8.1
#!pip install pyshp==1.2.10
#!pip install shapely==1.6.3


# In[76]:





# In[48]:


#import plotly.figure_factory as ff
#fig = ff.create_choropleth(fips=df.fips, 
#                           scope=['PA'],
#                          values=df.total_population, 
#                           title='PA total population by County', 
#                           legend_title='')
#fig.layout.template = None
#fig.show()


# In[85]:


#import plotly.figure_factory as ff

#values = range(len(df.fips))

#fig = ff.create_choropleth(fips=df.fips, values=values)
#fig.layout.template = None
#fig.show()


# In[ ]:





# In[ ]:





# In[ ]:




