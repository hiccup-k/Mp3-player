from pygame import mixer
from tkinter import *
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

current_volume= float(0.5)

#Main Screen
master=Tk()
master.title("Music Player")
master.geometry('500x449')

#intialize mixer
mixer.init()

#Global Pause Variable
global paused
paused=False 

#Functions


def play_time():
    current_time=mixer.music.get_pos()/1000


    convert_current_time=time.strftime('%M:%S',time.gmtime(current_time))
    

    #get song length with mutagen
    song_playing=song_box.curselection()
    current_song=song_box.get(song_playing)
    current_song=f"C:/Users/LENOVO/Desktop/Music Player/MUSIC/{current_song}.mp3"
    song_mut=MP3(current_song)
    global song_length
    song_length=song_mut.info.length
    converted_song_length=time.strftime('%M:%S',time.gmtime(song_length))
     
    current_time+=1 

    if int(slider.get())==int(song_length):
        status_bar.config(text=f'Timey Elapsed: {converted_song_length}  of  {converted_song_length} ')

    elif paused:
        pass
    #moving slider according to song position
    elif(slider.get()==int(current_time)):
        #slider hasn't moved
        slider_pos=int(song_length)
        slider.config(to=slider_pos,value=int(current_time))

    else:
        #slider has moved
        slider_pos=int(song_length)
        slider.config(to=slider_pos,value=int(slider.get()))
        
        convert_current_time=time.strftime('%M:%S',time.gmtime(int(slider.get())))
        #output time to status bar
        status_bar.config(text=f'Time Elapsed: {convert_current_time}  of  {converted_song_length} ')
        
        next_time=int(slider.get())+1
        slider.config(value=next_time)

    #update time
    status_bar.after(1000,play_time)

def add_song():
    current_songs=filedialog.askopenfilenames(initialdir="C:/Users/LENOVO/Desktop/Music Player/MUSIC",title= "Please select the song",filetype=(("mp3 files","*.mp3"),))
    #Loop through song list for adding many list
    for current_song in current_songs:
        #strip out the directory info and extension from the name
        current_song=current_song.replace("C:/Users/LENOVO/Desktop/Music Player/MUSIC/","")
        current_song=current_song.replace(".mp3","")
        #insert song in the list
        song_box.insert(END,current_song)
    

    #Add song to listbox
    song_box.insert(END,current_song)

def play():
    current_song=song_box.get(ACTIVE)
    current_song=f"C:/Users/LENOVO/Desktop/Music Player/MUSIC/{current_song}.mp3"
    mixer.music.load(current_song)
    mixer.music.play(loops=0)
    mixer.music.set_volume(current_volume)
    volume_bar.config(fg="black",text="volume:"+str(current_volume)) 
    
    #call play_time function for song time
    play_time()

    #update slider TO position
    #song_pos=int(song_length)
    #slider.config(to=song_pos,value=0)
    
def pause(is_paused):
    global paused
    paused=is_paused
    if paused:
        #unpaused
        mixer.music.unpause()
        paused=False
    else:
        #pause
        mixer.music.pause()
        paused=True
        
def stop():
    #reset slider
    status_bar.config(text='')
    slider.config(value=0)
    #stop music
    mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    #clearing status bar 
    status_bar.config(text='')

def reduce_vol():
    global current_volume
    if current_volume<=0:
            volume_bar.config(fg="blue",text="Volume: Muted")
            return
    current_volume=current_volume - float(0.1)
    current_volume=round(current_volume,1)
    mixer.music.set_volume(current_volume)
    volume_bar.config(fg="red",text="Volume:"+ str(current_volume)) 

def inc_vol():
    global current_volume
    if current_volume>=1:
            volume_bar.config(fg="blue",text="Volume: Max")
            return
    current_volume=current_volume + float(0.1)
    current_volume=round(current_volume,1)
    mixer.music.set_volume(current_volume)
    volume_bar.config(fg="green",text="Volume:"+str(current_volume))

def forward():
    status_bar.config(text='')
    slider.config(value=0)
    next_one=song_box.curselection()
    next_one=next_one[0]+1
    current_song=song_box.get(next_one)
    current_song=f"C:/Users/LENOVO/Desktop/Music Player/MUSIC/{current_song}.mp3"
    mixer.music.load(current_song)
    mixer.music.play(loops=0)
    #clear active bar
    song_box.selection_clear(0,END)
    #activate next song bar
    song_box.activate(next_one)
    #set now active bar 
    song_box.selection_set(next_one,last=None)

def backward():
    status_bar.config(text='')
    slider.config(value=0)
    next_one=song_box.curselection()
    next_one=next_one[0]-1
    current_song=song_box.get(next_one)
    current_song=f"C:/Users/LENOVO/Desktop/Music Player/MUSIC/{current_song}.mp3"
    mixer.music.load(current_song)
    mixer.music.play(loops=0)
    #clear active bar
    song_box.selection_clear(0,END)
    #activate prev song bar
    song_box.activate(next_one)
    #set now active bar 
    song_box.selection_set(next_one,last=None)

def delete_song():
    stop()
    song_box.delete(ANCHOR)
    mixer.music.stop()

def delete_all_song():
    stop()
    song_box.delete(0,END)
    mixer.music.stop

def slide(x):
   #slider_label.config(text=f'{int(slider.get())} of {int(song_length)}')
    current_song=song_box.get(ACTIVE)
    current_song=f"C:/Users/LENOVO/Desktop/Music Player/MUSIC/{current_song}.mp3"
    mixer.music.load(current_song)
    mixer.music.play(loops=0,start=int(slider.get()))






#Playlist box
song_box=Listbox(master,bg="dodger blue",fg="midnight blue",width=60,selectbackground="blue",selectforeground="black")
song_box.grid(pady=20,row=1)

#Button images
select_button_img=PhotoImage(file='png\mp3.png')
pause_button_img=PhotoImage(file='png\pause.png')
play_button_img=PhotoImage(file='png\play.png')
volume_inc_button_img=PhotoImage(file='png\inc.png')
volume_red_button_img=PhotoImage(file='png\dec.png')
forward_button_img=PhotoImage(file='png\move_forward.png')
backward_button_img=PhotoImage(file='png\move_backward.png')
stop_button_img=PhotoImage(file='png\stop.png')

#Buttons frame
control_frame=Frame(master)
control_frame.grid()

#Buttons
select_button=Button(control_frame,image=select_button_img,borderwidth=0,command=add_song)
pause_button=Button(control_frame,image=pause_button_img,borderwidth=0,command=lambda:pause(paused))
play_button=Button(control_frame,image=play_button_img,borderwidth=0,command=play)
volume_inc_button=Button(control_frame,image=volume_inc_button_img,borderwidth=0,command=inc_vol)
volume_red_button=Button(control_frame,image=volume_red_button_img,borderwidth=0,command=reduce_vol )
forward_button=Button(control_frame,image=forward_button_img,borderwidth=0,command=forward) 
backward_button=Button(control_frame,image=backward_button_img ,borderwidth=0,command=backward)
stop_button=Button(control_frame,image=stop_button_img,borderwidth=0,command=stop)


select_button.grid(row=2,column=2,padx=10)
volume_inc_button.grid(row=2,column=1,padx=10)
volume_red_button.grid(row=2,column=3,padx=10)
pause_button.grid(row=3,column=1,padx=10)
play_button.grid(row=3,column=2,padx=10)
forward_button.grid(row=3,column=4,padx=10)
backward_button.grid(row=3,column=0,padx=10)
stop_button.grid(row=3,column=3,padx=10)

#Create Menu
my_menu=Menu(master)
master.config(menu=my_menu)


#create Delete song Menu
remove_song_menu=Menu(my_menu)
my_menu.add_cascade(label="Remove Songs",menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist",command=delete_song)
remove_song_menu.add_command(label="Delete All Song From Playlist",command=delete_all_song)

#status Bar
status_bar=Label(master,text="",bd=1,relief=GROOVE,anchor=E,width=70)
status_bar.grid(row=8,ipady=5)
volume_bar=Label(master,text="",bd=1,relief=GROOVE,anchor=E,width=70)
volume_bar.grid(row=7,)

#Create slider for song duration
slider=ttk.Scale(master,from_=0 ,to=100,orient=HORIZONTAL,value=0,command=slide,length=360)
slider.grid(row=6,pady=20)

#Create slider label
slider_label=Label(master,text="0")
slider_label.grid()
 
master.mainloop()
