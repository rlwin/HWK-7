#!/usr/bin/env python
# coding: utf-8

# # Homework 7, Part Two: A dataset about dogs.
# 
# Data from [a FOIL request to New York City](https://www.muckrock.com/foi/new-york-city-17/pet-licensing-data-for-new-york-city-23826/)

# ## Do your importing and your setup

# In[1]:


import pandas as pd
import numpy as np
import matplotlib as plt


# ## Read in the file `NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx` and look at the first five rows

# In[2]:


df_dogs=pd.read_excel('NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx', na_values=['Unknown', 'UNKNOWN'])
df_dogs.head(5)


# ## How many rows do you have in the data? What are the column types?
# 
# If there are more than 30,000 rows in your dataset, go back and only read in the first 30,000.
# 
# * *Tip: there's an option with `.read_csv` to only read in a certain number of rows*
df_dogs=pd.read_excel('NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx', na_values=['Unknown', 'UNKNOWN'], nrows=30000)

# In[3]:


df_dogs=pd.read_excel('NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx', nrows=30000, na_values=['Unknown', 'UNKNOWN'])


# In[4]:


df_dogs.shape


# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
# 
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”

# In[5]:


#Each row represents the license information of a dog in NYC
#Owner Zip Code refer to the zipcode that specific dog is licensed in
#Primary Breed gives the dog's primary breed


# # Your thoughts
# 
# Think of four questions you could ask this dataset. **Don't ask them**, just write them down in the cell below. Feel free to use either Markdown or Python comments.

# In[6]:


#Number of licensed dogs in each zipcode
#Popular breeds by zipcode
#most popular names by breed
#most popular age of licensed dogs in NYC


# # Looking at some dogs

# ## What are the most popular (primary) breeds of dogs? Graph the top 10.

# In[7]:


df_dogs['Primary Breed'].value_counts()


# ## "Unknown" is a terrible breed! Graph the top 10 breeds that are NOT Unknown
# 
# * *Tip: Maybe you want to go back to your `.read_csv` and use `na_values=`? Maybe not? Up to you!*

# In[8]:


df_dogs['Primary Breed'].value_counts()


# In[9]:


df_dogs['Primary Breed'].value_counts().head(10).plot(kind='bar')


# ## What are the most popular dog names?

# In[10]:


df_dogs['Animal Name'].value_counts()


# ## Do any dogs have your name? How many dogs are named "Max," and how many are named "Maxwell"?

# In[11]:


len(df_dogs[df_dogs["Animal Name"].str.contains("Max", na=False)])


# In[12]:


len(df_dogs[df_dogs["Animal Name"].str.contains("Maxwell", na=False)])


# ## What percentage of dogs are guard dogs?

# In[13]:


df_dogs.columns=df_dogs.columns.str.lower().str.replace(" ", "_")
df_dogs.columns
#I got annoyed at all my spelling errors at this point)


# In[14]:


df_dogs.guard_or_trained.value_counts(normalize=True)*100


# ## What are the actual numbers?

# In[15]:


df_dogs.guard_or_trained.value_counts()


# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
# 
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`. Think about missing data!

# In[16]:


df_dogs.guard_or_trained.value_counts().sum()


# In[17]:


df_dogs.guard_or_trained.isna().sum()


# ## Maybe fill in all of those empty "Guard or Trained" columns with "No"? Or as `NaN`? 
# 
# Can we make an assumption either way? Then check your result with another `.value_counts()`

# In[18]:


df_dogs.guard_or_trained.value_counts(dropna=False)
#wouldn't filling in with 'No' be false data? 


# ## What are the top dog breeds for guard dogs? 

# In[19]:


#df_dogs.groupby(by='guard_or_trained').primary_breed.value_counts().groupby(level=0).head(1)
df_dogs.groupby(by='guard_or_trained').primary_breed.value_counts().groupby(level=0, group_keys='false').nlargest(2)


# ## Create a new column called "year" that is the dog's year of birth
# 
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# In[20]:


df_dogs['year']=df_dogs['animal_birth'].apply(lambda birth: birth.year)
df_dogs


# ## Calculate a new column called “age” that shows approximately how old the dog is. How old are dogs on average?

# In[21]:


df_dogs['age']=2020-df_dogs.year
df_dogs


# In[22]:


df_dogs.age.mean().round(0)


# # Joining data together

# In[ ]:





# ## Which neighborhood does each dog live in?
# 
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# In[23]:


df_zips=pd.read_csv('zipcodes-neighborhoods.csv')
df_zips


# In[24]:


dogs_zips=df_dogs.merge(df_zips, left_on='owner_zip_code', right_on='zip', how='left')
dogs_zips


# In[25]:


dogs_zips.shape


# In[26]:


dogs_zips=dogs_zips.drop(columns=['zip'])
#dogs_zips=dogs_zips.pop('borough')
dogs_zips


# In[ ]:





# ## What is the most popular dog name in all parts of the Bronx? How about Brooklyn? The Upper East Side?
# 
# You'll want to do these separately, and filter for each.

# In[27]:


dogs_zips[dogs_zips.borough=='Bronx'].animal_name.value_counts().head(5)


# In[28]:


dogs_zips[dogs_zips.borough=='Brooklyn'].animal_name.value_counts().head(5)


# In[29]:


dogs_zips[dogs_zips.neighborhood=='Upper East Side'].animal_name.value_counts().head(5)


# ## What is the most common dog breed in each of the neighborhoods of NYC?
# 
# * *Tip: There are a few ways to do this, and some are awful (see the "top 5 breeds in each borough" question below).*

# In[71]:


pop_neighborhood=dogs_zips.groupby('neighborhood').primary_breed.value_counts().groupby(level=0).head(5)


# In[75]:


pd.set_option("display.max_rows", None)
pop_neighborhood


# ## What breed of dogs are the least likely to be spayed? Male or female?
# 
# * *Tip: This has a handful of interpretations, and some are easier than others. Feel free to skip it if you can't figure it out to your satisfaction.*

# In[31]:


#df_dogs[df_dogs.spayed_or_neut=='Yes'].groupby('animal_gender').plot(kind='bar')
df_dogs.groupby('animal_gender').head()


# In[32]:


df_dogs[df_dogs.spayed_or_neut=='Yes'].animal_gender.value_counts().groupby(level=0).head()


# ## Make a new column called `monochrome` that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# In[33]:


dogs_zips.animal_dominant_color=dogs_zips.animal_dominant_color.str.upper()
dogs_zips.animal_secondary_color=dogs_zips.animal_secondary_color.str.upper()
dogs_zips.animal_third_color=dogs_zips.animal_third_color.str.upper()


# In[126]:


#dogs_zips.loc[[],['animal_dominant_color', 'animal_secondary_color','animal_third_color']=='BLACK']

#HALP, I"M TUCK!




# ## How many dogs are in each borough? Plot it in a graph.

# In[35]:


dogs_zips.borough.value_counts().plot(kind='bar')


# ## Which borough has the highest number of dogs per-capita?
# 
# You’ll need to merge in `population_boro.csv`

# In[36]:


boro_pop=pd.read_csv('boro_population.csv')
boro_pop.head(5)


# In[37]:


dogs_zips_boros=dogs_zips.merge(boro_pop, left_on='borough', right_on='borough', how='left')
dogs_zips_boros.head(5)


# In[51]:


total_boro=dogs_zips.borough.value_counts()
#dogs_zips_boros[dogs_zips_boros.groupby('borough').population.value_counts()

total_pop=dogs_zips_boros.groupby(by='borough').population.sum()



# In[59]:


#pd.set_option('display.float_format', lambda x: '%.10f' % x)
pd.reset_option('display.float_format')
total_boro/total_pop*100


# ## Make a bar graph of the top 5 breeds in each borough.
# 
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.

# In[125]:


top_boro=dogs_zips.groupby('borough').primary_breed.value_counts().groupby(level=0).head(5)
#groupby(level=0).head(5).plot(kind='barh', figsize=[10,10])
top_boro.plot(x="borough", y="primary_breed", kind="bar")


# In[ ]:


#Could not figure out how to group my results into coloured columns to show
#Borough as x, value counts as y and grouped coloured columns as breeds

