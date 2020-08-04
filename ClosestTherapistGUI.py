# Program to make a simple  
# login screen    
import tkinter as tk
from tkinter import ttk
import pandas as pd
import googlemaps
import time
import testMessage
from secrets import api_key

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
checkbutton3 = tk.IntVar()
checkbutton4 = tk.IntVar()
checkbutton5 = tk.IntVar()

#insert progress bar
def bar():
    progress['value'] = 20
    treev.update_idletasks()
    time.sleep(1)

    progress['value'] = 40
    treev.update_idletasks() 
    time.sleep(1) 
  
    progress['value'] = 50
    treev.update_idletasks() 
    time.sleep(1) 
  
    progress['value'] = 60
    treev.update_idletasks() 
    time.sleep(1) 
  
    progress['value'] = 80
    treev.update_idletasks() 
    time.sleep(1) 
    progress['value'] = 100   
# defining a function that will 
# get the name and password and  
# print them on the screen 
def submit():
    global name, dest, female_only, male_only, state, address, inital, weekly, monthly
    bar()
    name=name_var.get() 
    dest=passw_var.get()
    female_only = checkbutton1.get()
    male_only = checkbutton2.get()
    initial = checkbutton3.get()
    weekly = checkbutton4.get()
    monthly = checkbutton5.get()
    
    # Retrieve state from address
    address = dest.split(' ')
    states = ['NSW', 'QLD', 'WA', 'VIC', 'TAS', 'SA', 'NT', 'ACT']
    state = [s for s in address if any(xs in s for xs in states)][0]
    name_var.set("") 
    passw_var.set("")
    find_contractor()
def message():
    global message
    message = f"Hi {cont['values'][0]}, we have a new client {name} in {address[-3].strip(',')} \
looking for FN appts. She is avail Mon - AM, Tues - PM, Wed - AM. Pls respond with avail. Thanks - M2M"
    testMessage()
    for item in treev.selection():
        item_text = treev.item(item, "text")
        print(item_text)
def find_contractor():
    global match, best_fit
    # Get contractor data 
    df = pd.read_csv(r'C:\Users\info\Downloads\therapists.csv', skiprows=1, skipfooter=3, engine='python')

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
    match = match.sort_values(by=['Minutes'])
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
# creating a label for frequency 
freq_label = tk.Label(root, 
                       text = 'Frequency', 
                       font = ('calibre',10,'bold')).place(x=30, y=150)
#Frequency Buttons
Button3 = tk.Checkbutton(root, text = 'I', variable =checkbutton3,
                      onvalue=1, offvalue=0, height=2,width=10).place(x=120, y=140)
Button4 = tk.Checkbutton(root, text = 'W', variable =checkbutton4,
                      onvalue=1, offvalue=0, height=2,width=10).place(x=180, y=140)
Button4 = tk.Checkbutton(root, text = 'M', variable =checkbutton5,
                      onvalue=1, offvalue=0, height=2,width=10).place(x=260, y=140)
   
# creating a button using the widget  
# Button that will call the submit function  
sub_btn=tk.Button(root,text = 'Submit', 
                  command = submit).place(x=200,y=170)
message_btn=tk.Button(root,text = 'Message', 
                  command = message).place(x=200,y=450)

#Creating check buttons
Button1 = tk.Checkbutton(root, text = 'Female Only', variable =checkbutton1,
                      onvalue=1, offvalue=0, height=2,width=10).place(x=150, y=110)
Button2 = tk.Checkbutton(root, text = 'Male Only', variable =checkbutton2,
                      onvalue=1, offvalue=0, height=2,width=10).place(x=250, y=110)
#Create TreeView
treev = ttk.Treeview(root, selectmode='extended')
treev.place(x=30, y=210)
verscrlbar = ttk.Scrollbar(root, orient='vertical', command=treev.yview)
verscrlbar.pack(side='right', fill='x')
treev.configure(xscrollcommand = verscrlbar.set)
treev['columns'] = ('1','2','3', '4', '5')
treev['show'] = 'headings'
progress = ttk.Progressbar(root, orient = "horizontal", 
              length = 100, mode = 'determinate') 
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

def insert_data():
    i = 0
    for x in match.index:
        treev.insert('', 'end', text='item '+str(i),
                     values=(match['First Name-'][x], match['Client Type'][x], match['duration'][x], \
                             match['distance'][x], match['Minutes'][x]))
        i = i+1
        treev.bind('<Button-1>', OnSelect)
def OnSelect(event):
    global curItem, cont, number
    curItem = treev.focus()
    print(treev.item(curItem))
    cont = treev.item(curItem)
    number = match[match['First Name-'].str.contains(cont['values'][0])]['Mobile'].values[0]
    print("you clicked on", treev.selection())

  
progress.pack(pady = 500) 
  
    
root.mainloop() 
