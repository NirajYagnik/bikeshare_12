import time
import pandas as pd #importing NumPy,time and pandas packages
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
def get_item(input_print,error_print,enterable_list,get_value): 
    """function to reduce the iterations and conditional statement"""
    while (True):
        ret = input(input_print);
        ret = get_value(ret)
        if ret.title() in enterable_list:#if the input exists in the list, then the input is returned or else the iteration continues
            return ret
            break
        else:
            print(error_print);
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #callback
    city = get_item('Would you like to analyse the data of Chicago, New York City or Washington \n',
                    'Error!Please input the correct city name.',
                    ['Chicago', 'New York City', 'Washington'],
                    lambda x: str.title(x))
    choice1=get_item('Enter Month,Day,Both or None \n',
                     'Error!Enter valid input',
                     ['Month','Day','Both','None'],lambda x: str.lower(x))
    if choice1 in 'both':#if choice entered is both, both day and month is taken as input for data filter
        month=get_item('Enter the month, January, Febrauary, March, April, May, June \n',
                       'Error!Please input the correct month name',
                       ['January','February','March','April','May','June'],lambda x: str.title(x))
        day=get_item('Enter the day of the week: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday,Sunday\n',
                     'Error!Please input the correct day of the week',
                     ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],lambda ax: str.title(ax))      
    elif choice1 in 'month':#if choice entered is month, month is taken as input for filtering
        month=get_item('Enter the month, January, Febrauary, March, April, May, June \n',
                       'Error!Please input the correct month name',
                       ['January','February','March','April','May','June'],lambda x: str.title(x))
        day="all"
    elif choice1 in 'day':#if choice entered is day, day is taken as input for filtering
        month="all"
        day=get_item('Enter the day of the week: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday,Sunday\n',
                     'Error!Please input the correct day of the week',
                     ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],lambda ax: str.title(ax)) 
    elif choice1 in 'none': #if choice is none, both month and day are given default value "all"
        month="all"
        day="all"
        
    
    print('-'*40)
    return city.lower(),month.lower(),day.lower(),choice1.lower()
def load_data(city, month, day): #code from the "Practice Problem #3" in the project section of "Introduction to Python" (Approved for use as it states," you'll implement the load_data() function, which you can use directly in your project.")
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city]) 

    df['Start Time'] = pd.to_datetime(df['Start Time'])#Converting Start Time values to datetime values
    df['month'] = df['Start Time'].dt.month # extract month and day of week from Start Time to create new columns
    df['day_of_week'] = df['Start Time'].dt.weekday_name 

    
    if month != 'all':#month filtering
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    
    if day != 'all': #filter by days of week if user decides to filter by date/both
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df
def time_stats(df,choice1):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if choice1 in 'both':#if the data is filtered by both day of the week and month then the most common day and month is not computed
        popular_hour = df['Start Time'].dt.hour.mode()[0]
        print('Most Frequent Start Hour:', popular_hour,'Hrs')
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    else:
        months1=['January','February','March','April','May','June']
        mon_index=df['Start Time'].dt.month.mode()[0] #using mode() to get the most common month
        print('Most Common Month is -',months1[mon_index-1])

    # display the most common day of week
        weeks1=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        day_common=df['Start Time'].dt.weekday_name.mode()[0]
        print('Most Common Week-',day_common)
    # display the most common start hour
        popular_hour = df['Start Time'].dt.hour.mode()[0]
        print('Most Frequent Start Hour:', popular_hour,'Hrs')
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start=df['Start Station'].mode()[0]# most common start station using mode() 
    counts1=(df['Start Station']==pop_start).sum()# count of the the particular function using sum()
    print('The most popular start station is ',pop_start)
    print('Counts :',counts1)
    
     # display most commonly used end station
    pop_end=df['End Station'].mode()[0]#most common end station using mode()
    print('The most popular end Station is ' , pop_end)
    print('Counts:',(df['End Station']==pop_end).sum())

    # display most frequent combination of start station and end station trip
    df['combined'] = df['Start Station'].map(str) +"->" + df['End Station']# concatenate two columns of the dataframe into one column for convenient analysis
    #got the syntax for concatenating the columns from stackoverflow.com 
    pop_trip=df['combined'].mode()[0]
    print('Most frequent trip is ', pop_trip)
    print('Counts:',(df['combined']==pop_trip).sum())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_time=df['Trip Duration'].sum()
    print('Total travel time is ',total_time, 's')# display total travel time
    average_time=df['Trip Duration'].mean()
    print('average Tavel time is', average_time, 's')

    # display mean travel time


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types=df['User Type'].value_counts()
    print('User Types are:')
    print(user_types)
    
    if city in 'washington':#Data about gender is not provide for Washington
        print('No data provided about gender for this city')
    else:
        genders1=df['Gender'].value_counts()# Display counts of gender
        print(genders1)

    if city in 'washington':#data regarding birth date is not provided for Washington
        print('No data provied about Birth Year for this city')
    else:# Display earliest, most recent, and most common year of birth
        early_date=df['Birth Year'].min()
        recent_date=df['Birth Year'].max()
        common_date=df['Birth Year'].mode()[0]
        print('Earliest birth year is :',int(early_date))
        print('Most recent birth year is :',int(recent_date))
        print('Most common year is :',int(common_date), ', Counts', (df['Birth Year']==common_date).sum())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    """ Main function that calls all the sub functions sequentially"""
    while True:
        city, month, day,choice1 = get_filters()
        df = load_data(city, month, day)
        time_stats(df,choice1)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':# breaks if the input is pno
            break

if __name__ == "__main__":
    main()






