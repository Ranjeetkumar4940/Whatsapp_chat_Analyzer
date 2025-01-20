import re
import pandas as pd


def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'User-Message': messages, 'Date': dates})
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y, %H:%M - ')

    users = []
    messages = []
    for message in df['User-Message']:
        entry = re.split(r'(.*?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Group Notification')
            messages.append(entry[0])

    df['Users'] = users
    df['Messages'] = messages

    df.drop(columns=['User-Message'], inplace=True)
    df['Year'] = df['Date'].dt.year
    df['month_num'] = df['Date'].dt.month
    df['only_date'] = df['Date'].dt.date
    df['day_name'] = df['Date'].dt.day_name()
    df['Month'] = df['Date'].dt.month_name()
    df['Day'] = df['Date'].dt.day
    df['hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df


