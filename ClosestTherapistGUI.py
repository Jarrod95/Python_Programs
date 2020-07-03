# Program to make a simple  
# login screen    
import tkinter as tk
from tkinter import ttk
import pandas as pd
import googlemaps

api_key = 'AIzaSyAbRYyx5buQlljdbL0iMG9IlAQ4aboAX6M'
gmaps = googlemaps.Client(key=api_key)
   
root=tk.Tk() 
  
# setting the windows size 
root.geometry("500x500")
root.title('Closest contractors')
label = tk.Label(root, text="Locate closest therapist", font=("Arial",20)).place(x=250, y =25, anchor='center')  
# declaring string variable 
# for storing name and password 
name_var=tk.StringVar() 
passw_var=tk.StringVar() 
checkbutton1 = tk.IntVar()
checkbutton2 = tk.IntVar()
   
# defining a function that will 
# get the name and password and  
# print them on the screen 
def submit():
    global name, dest, female_only, male_only, state
    name=name_var.get() 
    dest=passw_var.get()
    female_only = checkbutton1.get()
    male_only = checkbutton2.get()

    # Retrieve state from address
    address = dest.split(' ')
    states = ['NSW', 'QLD', 'WA', 'VIC', 'TAS', 'SA', 'NT', 'ACT']
    state = test2 = [s for s in address if any(xs in s for xs in states)][0]
##    print("The name is : " + name) 
##    print("The address is : " + dest)
##    print("The state is: " + state)
##    print("Female Only: ", female_only == 1)
##    print("Male Only: ",  male_only == 1)
    #Print results to text box??
##    w = tk.Text(root, height=1, borderwidth=0)
##    w.insert(1.0, state)
##    w.place(x=200,y=220)
    name_var.set("") 
    passw_var.set("")
    find_contractor()
def find_contractor():
    global match, best_fit
    # Get contractor data 
    df = pd.read_csv(r'C:\Users\info\Downloads\therapists.csv', skiprows=1, skipfooter=3)

    #Drop everyone expired or unavail
    df = df.dropna(subset=['Insurance Expiry Date', 'First Aid Expiry Date', 'Police Check Expiry', 'Membership Expiry'])
    df = df[~df['Client Type'].str.match('Expired')]
    df = df[~df['Client Type'].str.match('Unavailable')]
    #Change Mobile column to international number
    df['Mobile'] = df['Mobile'].str.replace('04', '+614', 1)
    df['Mobile'] = df['Mobile'].str.replace(' ', '')
    match = df[df['State-'].str.match(state)].reset_index(drop=True)
    #Drop therapists that do not match gender pref
    if female_only == 1:
        match = match[match['Gender'] == 'Female']
    elif male_only == 1:
        match = match[match['Gender'] == 'Male']
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
    match['Minutes'] = pd.eval(match['duration'].replace(['hours?', 'mins', 'min','Minutes'], ['*60+', '', '', ''], regex=True)).astype(int)
    match.sort_values(by=['Minutes'])
    print(match[['First Name-', 'duration', 'distance', 'Minutes']])
    best_fit = match.nsmallest(4, 'Minutes')
    print('--------------------------')
    print('Here are the four closest therapists:\n\n')
    print(best_fit[['First Name-', 'duration', 'distance', 'Minutes']])
    insert_data()

# name using widget Label 
name_label = tk.Label(root, text = 'First Name', 
                      font=('calibre', 
                            10, 'bold')).place(x=30, y=50)
   
# creating a entry for input 
# name using widget Entry 
name_entry = tk.Entry(root, 
                      textvariable = name_var,
                      font=('calibre',10,'normal')).place(x=150, y=50) 
   
# creating a label for password 
passw_label = tk.Label(root, 
                       text = 'Address', 
                       font = ('calibre',10,'bold')).place(x=30, y=90) 
   
# creating a entry for password 
passw_entry=tk.Entry(root, width=45,
                     textvariable = passw_var, 
                     font = ('calibre',10,'normal')).place(x=150, y=90) 
   
# creating a button using the widget  
# Button that will call the submit function  
sub_btn=tk.Button(root,text = 'Submit', 
                  command = submit).place(x=200,y=170)

#Creating check buttons
Button1 = tk.Checkbutton(root, text = 'Female Only', variable =checkbutton1,
                      onvalue=1, offvalue=0, height=2,width=10).place(x=150, y=110)
Button2 = tk.Checkbutton(root, text = 'Male Only', variable =checkbutton2,
                      onvalue=1, offvalue=0, height=2,width=10).place(x=250, y=110)
#Create TreeView
treev = ttk.Treeview(root, selectmode='browse')
treev.place(x=30, y=210)
verscrlbar = ttk.Scrollbar(root, orient='vertical', command=treev.yview)
verscrlbar.pack(side='right', fill='x')
treev.configure(xscrollcommand = verscrlbar.set)
treev['columns'] = ('1','2','3', '4', '5')
treev['show'] = 'headings'
#Add columns
treev.column('1', width=90, anchor='c')
treev.column('2', width=90, anchor='se')
treev.column('3', width=90, anchor='se')
treev.column('4', width=90, anchor='se')
treev.column('5', width=90, anchor='se')

treev.heading('1', text = 'Name')
treev.heading('2', text= 'Status')
treev.heading('3', text = 'Duration')
treev.heading('4', text = 'Distance')
treev.heading('5', text = 'Minutes')

#insert values
##treev.insert("", 'end', text ="L1",  
##             values =("Nidhi", "F", "25")) 
##treev.insert("", 'end', text ="L2", 
##             values =("Nisha", "F", "23"))
def insert_data():
    i = 0
    for x in match.index:
        treev.insert('', 'end', text='item '+str(i),
                     values=(match['First Name-'][x], match['Client Type'][x], match['duration'][x], \
                             match['distance'][x], match['Minutes'][x]))
        i = i+1

   
root.mainloop() 
