import re
import pandas as pd

def parse_whatsapp_chat(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    chat_data = []
    date_time_pattern = r'\[\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}:\d{2} [APap][mM]\]'
    message_pattern = re.compile(rf'({date_time_pattern}) (.*?): (.*)')

    for line in lines:
        if line.strip():  # Check for empty lines
            match = message_pattern.match(line)
            if match:
                date_time, sender, message = match.groups()
                # Remove the brackets around date_time
                date_time = date_time[1:-1]
                chat_data.append([date_time, sender, message])
            else:
                # Append message to the previous entry if it's a multi-line message
                if chat_data:  # Ensure there's at least one previous message
                    chat_data[-1][-1] += f'\n{line.strip()}'

    # Convert to DataFrame
    df = pd.DataFrame(chat_data, columns=['DateTime', 'User', 'Message'])
    df['DateTime'] = pd.to_datetime(df['DateTime'], format='%m/%d/%y, %I:%M:%S %p')
    users = []
    messages = []
    for message in df['Message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['Message'], inplace=True)
    df.drop(columns=['user'], inplace=True)

    # Extract multiple columns from the Date Column

    df['only_date'] = df['DateTime'].dt.date
    df['year'] = df['DateTime'].dt.year
    df['month_num'] = df['DateTime'].dt.month
    df['month'] = df['DateTime'].dt.month_name()
    df['day'] = df['DateTime'].dt.day
    df['day_name'] = df['DateTime'].dt.day_name()
    df['hour'] = df['DateTime'].dt.hour
    df['minute'] = df['DateTime'].dt.minute

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
    
