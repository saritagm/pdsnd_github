import time
import pandas as pd
import numpy as np

# Constants for city data
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

# Constants for months and days
MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Ensures valid inputs are given for city, month, and day.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get valid city input
    city = ''
    while city not in CITY_DATA:
        city = input("Please choose a city from Chicago, New York City, or Washington: ").lower()
        if city not in CITY_DATA:
            print("Invalid input. Please try again.")

    # Get valid month input
    month = ''
    while month not in MONTHS:
        month = input(f"Please choose a month from {', '.join(MONTHS)}: ").lower()
        if month not in MONTHS:
            print("Invalid input. Please try again.")
    
    # Get valid day input
    day = ''
    while day not in DAYS:
        day = input(f"Please choose a day from {', '.join(DAYS)}: ").lower()
        if day not in DAYS:
            print("Invalid input. Please try again.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
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

    # Filter by month
    if month != 'all':
        df['Month'] = pd.to_datetime(df['Start Time']).dt.month
        month_index = MONTHS.index(month)
        df = df[df['Month'] == month_index]

    # Filter by day of week
    if day != 'all':
        df['Day of Week'] = pd.to_datetime(df['Start Time']).dt.day_name().str.lower()
        df = df[df['Day of Week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Most common month
    most_common_month = df['Month'].mode()[0] if 'Month' in df else None
    print(f"Most common month: {MONTHS[most_common_month]}")

    # Most common day of week
    most_common_day = df['Day of Week'].mode()[0] if 'Day of Week' in df else None
    print(f"Most common day: {most_common_day.capitalize()}")

    # Most common start hour
    df['Hour'] = pd.to_datetime(df['Start Time']).dt.hour
    most_common_hour = df['Hour'].mode()[0]
    print(f"Most common start hour: {most_common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print(f"Most common start station: {start_station}")

    # Most commonly used end station
    end_station = df['End Station'].mode()[0]
    print(f"Most common end station: {end_station}")

    # Most frequent combination of start and end station
    combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"Most frequent combination of start and end station: {combination[0]} to {combination[1]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time: {total_travel_time} seconds")

    # Average travel time
    average_travel_time = df['Trip Duration'].mean()
    print(f"Average travel time: {average_travel_time:.2f} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Counts of user types
    user_types = df['User Type'].value_counts()
    print(f"Counts of user types:\n{user_types}")

    # Counts of gender (if applicable)
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print(f"Counts of gender:\n{gender_counts}")
    
    # Earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print(f"Earliest year of birth: {earliest_birth_year}")
        print(f"Most recent year of birth: {most_recent_birth_year}")
        print(f"Most common year of birth: {most_common_birth_year}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
