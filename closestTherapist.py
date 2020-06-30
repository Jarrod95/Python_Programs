import pandas as pd
import googlemaps

api_key = ''
gmaps = googlemaps.Client(key=api_key)

df = pd.read_csv(r'C:\Users\info\Downloads\therapists.csv', skiprows=1, skipfooter=3)

#Drop everyone expired or unavail
df = df.dropna(subset=['Insurance Expiry Date', 'First Aid Expiry Date', 'Police Check Expiry', 'Membership Expiry'])
df = df[~df['Client Type'].str.match('Expired')]
df = df[~df['Client Type'].str.match('Unavailable')]
#Change Mobile column to international number
df['Mobile'] = df['Mobile'].str.replace('04', '+614', 1)
df['Mobile'] = df['Mobile'].str.replace(' ', '')

print('Please input a State')
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
match['Minutes'] = pd.eval(match['duration'].replace(['hours?', 'mins', 'min'], ['*60+', '', ''], regex=True))
print(match[['First Name-', 'duration', 'distance', 'Minutes']])
best_fit = match.nsmallest(4, 'Minutes')
print('--------------------------')
print('Here are the four closest therapists:\n\n')
print(best_fit[['First Name-', 'duration', 'distance', 'Minutes']])
