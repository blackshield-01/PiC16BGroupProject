import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# convert duration to numerical format in minutes
def clean_duration(duration):
    durations = []
    for dur in duration:
        dur_split = dur.split()
        hours = int(dur_split[0].split("h")[0]) if "h" in dur_split[0] else 0
        minutes = int(dur_split[1].split("m")[0]) if "m" in dur_split[1] else 0
        total_minutes = hours * 60 + minutes
        durations.append(total_minutes)
    return durations

# convert it to numerical
def clean_stops(stops):
    if stops == 'nonstop':
        return 0
    elif stops == '1 stop':
        return 1
    elif stops == '2 stops':
        return 2
    elif stops == '3 stops':
        return 3
    else:
        return np.nan

#split the date to day of week (0=Sunday,1=Monday, etc.) and month
def clean_date(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['DayOfWeek'] = (df['Date'].dt.dayofweek + 1) % 7
    df['Month'] = df['Date'].dt.month
    return df

#remove uncessary space and punctuation
def clean_company_name(df):
    # Remove leading and trailing whitespace
    df['Company Name'] = df['Company Name'].str.strip()
    # Remove punctuation
    df['Company Name'] = df['Company Name'].str.replace('[^\w\s]', '')
    # Remove extra whitespace within the company name
    df['Company Name'] = df['Company Name'].str.replace('\s+', ' ')
    return df

#convert date and company name into numerical representations

def preprocess(df):
    df = clean_company_name(df)  # Clean company names first
    le = LabelEncoder()
    df['Date'] = le.fit_transform(df['Date'])
    df['Company Name'] = le.fit_transform(df['Company Name'])
    return df

def clean_destination(df):
    le = LabelEncoder()
    df['Destination'] = le.fit_transform(df['Destination'])
    return df