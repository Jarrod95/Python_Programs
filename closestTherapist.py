import pandas as pd
import googlemaps
from datetime import date, timedelta

api_key = ''
gmaps = googlemaps.Client(key=api_key)
today = date.today()

#Find most recent file
extension = r'C:\Users\info\OneDrive\1. M2M Administration\EXPORTED FROM SOFTWARE\Therapist Data\Maps_Export_'

#Extract most recent therapist data up to 10 days ago
i = 0
while i < 10:
    dt = date.today() - timedelta(i)
    df = pd.read_csv(fr'{extension}{dt.strftime("%d-%m-%Y")}.csv', skiprows=1, skipfooter=3, engine='python')
    if len(df) > 1:
        break
    i += 1
    if i == 10:
        print("Checked 10 days worth of data -- please extract more recent data")

#Drop everyone expired or unavail
df = df.dropna(subset=['Insurance Expiry Date', 'First Aid Expiry', 'Police Check Expiry', 'Membership Expiry'])
df = df[~df['Client Type'].str.match('Expired')]
df = df[~df['Client Type'].str.match('Unavailable')]
#Change Mobile column to international number
df['Mobile'] = df['Mobile'].str.replace('04', '+614', 1)
df['Mobile'] = df['Mobile'].str.replace(' ', '')
print('input state')
state = input()

print('Please input an address')
dest = input()
#drop rows that don't match the state of new client
match = df[df['State-'].str.match(state)].reset_index(drop=True)
match['Address'] = match['Street'] + ', ' + match['Suburb'] + ', ' + \
                   match['State-'] + ', ' + match['Postcode'].astype(str)

# Compare distances
dist = []
dur = []
for i in match['Address']:
    result = gmaps.distance_matrix(i, dest, mode='driving')
    duration = result['rows'][0]['elements'][0]['duration']['text']
    distance = result['rows'][0]['elements'][0]['distance']['text']
    print(duration + ' (' + distance + ')')
    dist.append(distance)
    dur.append(duration)
match['distance'] = dist
match['duration'] = dur
#Convert format to mins
match['Minutes'] = pd.eval(match['duration'].replace(['hours?', 'mins', 'min'], ['*60+', '', ''], regex=True)).astype(int)
match = match.sort_values(by=['Minutes']).reset_index(drop=True)
print(match[['First Name-', 'duration', 'distance', 'Minutes']])
best_fit = match.nsmallest(4, 'Minutes')
print('--------------------------')
print('Here are the four closest therapists:\n\n')
print(best_fit[['First Name-', 'duration', 'distance', 'Minutes']])
