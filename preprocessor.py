import streamlit as st
import pandas as pd
import numpy as numpy
import matplotlib.pyplot as pyplot
import seaborn as sns
import re

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

def preprocess(data):

    # Pattern for WhatsApp date-time
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    
    # Split messages and extract dates
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Create DataFrame
    df = pd.DataFrame({
        'user_message': messages,
        'message_date': dates
    })

    # Clean date column
    df['message_date'] = df['message_date'].str.strip()
    df['message_date'] = df['message_date'].str.replace(' -', '', regex=False)

    # Convert to datetime
    df['message_date'] = pd.to_datetime(
        df['message_date'],
        format='%m/%d/%y, %H:%M',
        errors='coerce'
    )

    # Rename column
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Extract users and messages
    users = []
    msgs = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)

        if entry[1:]:  # user exists
            users.append(entry[1])
            msgs.append(entry[2])
        else:
            users.append('group_notification')
            msgs.append(entry[0])

    df['user'] = users
    df['message'] = msgs

    # Drop original column
    df.drop(columns=['user_message'], inplace=True)

    # Feature engineering
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day_name'] = df['date'].dt.day_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['period'] = df['hour'].apply(lambda x: f"{x:02d}-{(x+1)%24:02d}")
    df['minute'] = df['date'].dt.minute

    return df



