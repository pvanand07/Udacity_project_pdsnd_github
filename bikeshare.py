# *\US-Bikeshare-EDA-Python\bikeshare_2.py
#
# PROGRAMMER: Anand Siva P V
# DATE CREATED: 03-04-2023
# REVISED DATE: 01-05-2023
# PURPOSE: Explore US Bikeshare data and display the data in a user-friendly manner. 
# Imports python modules

import time
import pandas as pd
import numpy as np
from IPython.display import display
import warnings
# Ignore warnings
warnings.filterwarnings("ignore")


##-------------------------------------------------------------------------------------------------#
##   1.1 GET USER INPUT                                                                            #
##-------------------------------------------------------------------------------------------------#

def get_filters():
    '''
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    '''
    # Print a welcome message to the user
    print("Hello! Let's explore some US bikeshare data!")

    # Get a list of available cities from the CITY_DATA dictionary
    cities = list(CITY_DATA.keys())

    # Ask the user to input a city name to filter by
    city = input(f"Enter city name to filter by {cities}").lower()

    # Keep asking for city input until a valid city name is entered
    while city not in cities:
        city = input(f"Try again, Enter city name to filter by {cities}").lower()

    # Define a list of available months to filter by
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

    # Ask the user to input a month name to filter by
    month = input(f"Enter month name to filter by {months}").lower()

    # Keep asking for month input until a valid month name is entered
    while month not in months:
        month = input(f"Enter month name to filter by {months}").lower()

    # Define a list of available days of the week to filter by
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    # Ask the user to input a day of the week to filter by
    day = input(f"Enter day name to filter by {days}").lower()

    # Keep asking for day input until a valid day name is entered
    while day not in days:
        day = input(f"Try again, Enter day name to filter by {days}").lower()

    print('-'*45)
    return city, month, day


##-------------------------------------------------------------------------------------------------#
##   1.2  LOAD AND FILTER  DATA                                                                    #                                                                                                                                                               
##-------------------------------------------------------------------------------------------------#

def load_data(city, month, day):
    # provide postion arguments in the function definition to load data for the specified city, month and day

    '''
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    
    '''
    # Load data from the specified city
    df = pd.read_csv(CITY_DATA[city])

    # Convert the "Start Time" column to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract the month, day of week, and hour from the "Start Time" column
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # Filter the data by the specified month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        df = df[df['month'] == (months.index(month)+1)]

    # Filter the data by the specified day of week
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    # prompt if the user wants to see 5 lines of raw data, display if the answer is 'yes',
    prompt=input('Wold you like to see the first 5 rows of raw data? (yes/no)').lower()
    if prompt=='yes':
        print(df.iloc[:5,:].T)

        # Continue iterating these prompts until the user says 'no' or there is no more raw data to display.
        for i in range(5, len(df), 5):
            prompt=input('Wold you like to see the next 5 rows of raw data? (yes/no)').lower()
            if prompt=='yes':
                print(df.iloc[i:i+5,:].T)
            else:
                break
    
    print('-' * 40)
    return df


##-------------------------------------------------------------------------------------------------#
##   1.3  DISPLAY STATISTICS ON OCCATION OF TRAVEL                                                 #
##-------------------------------------------------------------------------------------------------#

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    idx_max_month = df['month'].value_counts().idxmax()
    max_month = ['all', 'january', 'february', 'march', 'april', 'may', 'june'][idx_max_month]
    print(f"The most common month is {max_month}")

    # display the most common day of week
    max_weekday = df['day_of_week'].value_counts().idxmax()
    print(f"The most common day of week is {max_weekday}")

    # display the most common start hour
    max_hour = df['hour'].value_counts().idxmax()
    print(f"The most common start hour is {max_hour}:00")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


##-------------------------------------------------------------------------------------------------#
##   1.4  DISPLAY STATISTICS ON MOST POPULAR STATIONS AND TRIPS                                    #
##-------------------------------------------------------------------------------------------------#

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trips...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].value_counts().idxmax()
    print(f"The most common start station is {start_station}")

    # display most commonly used end station
    end_station = df['End Station'].value_counts().idxmax()
    print(f"The most common end station is {end_station}")

    # display most frequent combination of start station and end station trip
    start_end_station = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"The most frequent combination of start station and end station trip is {start_end_station}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


##-------------------------------------------------------------------------------------------------#
##   1.5   DISPLAY STATISTICS ON TRIP DURATION                                                     #                                                                           
##-------------------------------------------------------------------------------------------------#

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"The total travel time is {total_travel_time} seconds")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"The mean travel time is {mean_travel_time} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


##-------------------------------------------------------------------------------------------------#
##   1.6  DISPLAY STATISTICS ON USER DEMOGRAPHICS                                                  #                                                                                                                                                
##-------------------------------------------------------------------------------------------------#

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = df['User Type'].value_counts()
    user_count = df['User Type'].value_counts()
    print(user_count,'\n')

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print(gender_count,'\n')

    # Check if 'Birth Year' column exists in the dataframe
    if 'Birth Year' in df.columns:
        
        # Calculate the earliest, most recent, and most common year of birth
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode())

        print(f"The earliest birth year is    {earliest_birth_year}")
        print(f"The most recent birth year is {most_recent_birth_year}")
        print(f"The most common birth year is {most_common_birth_year}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


##-------------------------------------------------------------------------------------------------#
##   1.7  DISPLAY STATISTICS USING BIVARIATE ANALYSIS                                              #                                                                                                                                                      
##-------------------------------------------------------------------------------------------------#

def eda(df):
    """ Displays statistics using bivariate analysis. """

    # Start the timer
    start_time = time.time()

    # Check if 'Gender' column exists in the dataframe
    if 'Gender' in df.columns:
        
        # Filter Null values in 'Gender' column
        df_2 = df.dropna(subset = ['Gender'])
        
        # Calcuate the median trip duration for different genders
        median_trip_duration_gender = df_2.groupby(['Gender'])['Trip Duration'].median()
        print(f"The median trip duration for different genders is:\n{median_trip_duration_gender}\n")

    # Calculate the median trip duration for different user types
    median_trip_duration_user = df.groupby(['User Type'])['Trip Duration'].median()
    print(f"The median trip duration for different user types is:\n{median_trip_duration_user}\n")

    # Calculate the median trip duration for different age groups
    if 'Birth Year' in df.columns:
        
        # Filter Null values in 'Birth Year' column
        df = df.dropna(subset =['Birth Year'])
                
        # Calculate the age group for each user
        df['Age'] = df['Start Time'].dt.year - df['Birth Year']
        df['Age_group'] = pd.cut(df['Age'], 9)

        # Calculate the median trip duration for different age groups
        median_trip_duration_age = df.groupby(['Age_group'])['Trip Duration'].median().fillna('Nill')
        print(f"The median trip duration for different age groups is:\n{median_trip_duration_age}\n")

        # Calculate the correlation between trip duration and age
        correlation = df['Trip Duration'].corr(df['Age'])
        print(f"The correlation between trip duration and age is: {correlation}\n")

    # Print the total time taken
    print(f"This took {time.time() - start_time} seconds.")
    print('-' * 40)


##-------------------------------------------------------------------------------------------------#
##   2.0 MAIN FUNCTION                                                                             #                                                                                                                                                      
##-------------------------------------------------------------------------------------------------#
    
def main():
    """ Main function that runs the bikeshare data analysis program.  """

    # Runs the program until the user wants to quit
    while True:
        # Get the user's input and filters the dataframe
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        # check if dataframe is empty
        if df.empty:
            print('No data found for the specified filters')
            main()

        # Get statistics on the time of travel
        time_stats(df)
        
        # Get statistics of stations used by the customer
        station_stats(df)
        
        # Get statistics on the trip duration
        trip_duration_stats(df)
        
        # Get statistics of the users
        user_stats(df)
        
        # Perform bivariate analysis
        eda(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

# Dictionary to hold the filenames
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Executes the main function
if __name__ == "__main__":
	main()

##-------------------------------------------------------------------------------------------------#
##                            *--* *--* END OF BIKESHARE.PY *--* *--*                                 #                                                                                                                                                     
##-------------------------------------------------------------------------------------------------#

