from os import walk,getcwd,makedirs,name
from os.path import normcase,splitext,join,split,basename,isdir
from pygame import mixer_music,mixer,error
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import  askyesno, showerror, showinfo
from time import sleep
from json import load,dump,JSONDecodeError
from threading import Thread
from mutagen.mp3 import MP3
from pyttsx3 import speak
# from PIL import Image,ImageTk
class music_player():
    def __init__(self):
        self.play_list=[]
        self.file_dir=[]
        self.file_name_dir={}
        self.udplay_list={}
        # print(type(self.udplay_list),"udplay_list")
        self.exited=False
        self.name=None
        self.playing=False
        self.paused=False
        self.audio_format=[".mp3",".MP3",".wav",".3gp",".aa",".aax",".avi",".ogg"]
        # loadd=Image.open(join(getcwd(),"img/play.png"))
        # self.play_img=ImageTk.PhotoImage(loadd)
        self.root=Tk()
        self.speak_=BooleanVar()
        self.root.title("Music Player")
        # self.root.iconbitmap("/home/cooldood/Desktop/tkicon.ico")
        self.root.geometry("250x300")
        self.list_window=Frame(self.root)
        menu=Menu(self.root)
        self.root.config(menu=menu)
        self.root.bind("<Control-O>",self.open_folder)
        self.root.bind("<Alt-leftarrow>",self.previous)
        self.root.bind("<Alt-rightarrow>",self.next)
        self.root.bind("<space>",self.play)
        File=Menu(menu)
        File.add_command(label="Add Folder ctrl+shift+o",command=self.open_folder)
        File.add_command(label="Close Floder",command=self.close_floder)
        playlist_menu=Menu(menu)
        playlist_menu.add_command(label="CreatePlaylist",command=self.creat_playlist)
        self.list_menu=Menu(menu)

        playlist_menu.add_cascade(label="PLay Playlist",menu=self.list_menu)
        menu.add_cascade(label="File",menu=File)
        menu.add_cascade(label="Playlist",menu=playlist_menu)
        self.list_window.pack(side=TOP)
        self.title_label=Label(self.root)
        self.title_label.pack()  
        self.progresslabel=Label(self.root)
        self.progresslabel.pack()      
        self.button_window=Frame(self.root)
        self.button_window.pack(side=BOTTOM)
        self.list=Listbox(self.list_window,width=30)
        self.list.grid(row=0,column=0)
        repeat=True
        self.list.bind("<Button-1>",self.play2)
        # self.list.bind("<Key-o>",lambda : self.play(repeat=True))
        self.get_data()
        if self.volume == None:
            self.volume=25
        if self.udplay_list==None or type(self.udplay_list) ==list:
            self.udplay_list={}
        for pllist in self.udplay_list:
            self.list_menu.add_command(label=pllist,command=lambda :self.play_play_list(pllist))
        

        
        self.image4=PhotoImage(file=join(getcwd(),"img/previous.png"))
        # startfile(join(getcwd(),"img/previous.png"))
        self.previous_button=Button(self.button_window,command=self.previous,image=self.image4)
        self.previous_button.grid(row=0,column=1)
        self.image2=PhotoImage(file=join(getcwd(),"img/play.png"))
        self.button=Button(self.button_window,command=self.play,image=self.image2)
        self.button.grid(row=0,column=2)
        self.volume_scale=Scale(self.button_window,orient='vertical',variable=self.volume,from_=100,to=0)
        self.volume_scale.grid(row=0,column=5)
        self.image3=PhotoImage(file=join(getcwd(),"img/next.png"))
        self.next_button=Button(self.button_window,command=self.next,image=self.image3)
        self.next_button.grid(row=0,column=3)
        self.check_button=Checkbutton(self.button_window,text="Say name",variable=self.speak_,onvalue=True,offvalue=False)
        self.check_button.deselect()
        self.check_button.grid(row=0,column=0)
        self.volume_scale.bind('<ButtonRelease>',self.set_volume)
        self.volume_scale.set(self.volume)
        if not self.last_played ==None:
            self.play(selected=self.last_played) 
        self.root.mainloop()
        self.exited=True
        self.dump_data()
        try:
            mixer_music.stop()
        except error:
            pass
        showinfo("Exit??","Closing The Player")
            
            
               
    def open_folder(self,event=None,a=None,list_=None):
        file_name_list=[]
        if list_==None:
            list=self.list
        else:
            list=list_
            # self.play_list=[]
        if a==None:
            a=askdirectory(initialdir="/")
            self.file_dir.append(a)
        for Directory_path,_,file_name in walk(a):
            file_name_list.append([Directory_path,file_name])
            pass
        for dir_n,file_list in file_name_list:
            for name in file_list:
                _,exe=splitext(name)
                if exe in self.audio_format:

                    list.insert(END,name)
                    self.file_name_dir[name]=normcase(dir_n)
                    self.play_list.append(name)
            list.select_anchor(len(self.play_list))
            #print(self.list.size(),"size")
    def play(self,event=None,selected=None,repeat=False):
        
        if selected is None:
            index=self.list.curselection()
            name=self.play_list[index[0]]
            file=join(self.file_name_dir[name],name)
            self.list.selection_set(index)

        else:
        
            file=selected
            _,name=split(file)
            index=self.play_list.index(name)
            self.list.see(index)
            self.list.selection_set(index)

        mixer.init()
        if self.playing:
            self.image=PhotoImage(file=join(getcwd(),"img/play.png"))
            self.button.config(image=self.image)
            mixer_music.pause()
            mixer_music.set_volume(self.volume)
            q=mixer_music.get_pos()
            #print(q//1000)
            self.paused=True
            self.playing=False
            # return None

        
        else:
            if len(file)>4:
                self.image=PhotoImage(file=join(getcwd(),"img/pause.png"))
                self.button.config(image=self.image)
               
                try:
                    if not self.paused or self.name != name:
                        if self.speak_.get():
                            speak(f"Playing {name}")
                        mixer_music.load(file)
                        mixer_music.set_volume(self.volume)
                        mixer_music.play() 
                        if self.first_played !=None:
                            mixer_music.set_pos(self.pos)
                            # self.pos=0
                            #print("positions updated",mixer_music.get_pos())
                            self.first_played=None
                        mixer_music.play()
                        self.last_played=file
                        self.thread=Thread(target=self.check_end_position)
                        self.thread.start()
                        
                        self.name=name
                        self.title_label["text"]=name
                    else:
                        
                        mixer_music.unpause()
                        mixer_music.set_volume(self.volume)
                    self.playing=True
                    # return None
                except Exception as e:
                    Label(self.root,text=e).pack()
        if repeat:
            self.play()
    def get_data(self):
        try:
            if name =="nt":
                file=join(getcwd(),"Data\\music_player.json")
            else:
                file=join(getcwd(),"Data/music_player.json")
            with open(normcase(file),"r") as f:
                self.json_data=load(f)
                self.file_dir=self.json_data["path"]
                self.last_played=self.json_data["last_played"]
                self.first_played=self.last_played
                self.pos=self.json_data["pos"]
                self.volume=self.json_data["volume"]
                self.udplay_list=self.json_data["play_list"]
                for file in self.file_dir:
                    self.open_folder(a=file)
        except Exception as e:
            # if e is FileNotFoundError:
            if isdir(join(getcwd(),"Data")):
                makedirs(join(getcwd(),"Data"))
            if name =="nt":
                file=join(getcwd(),"Data\\music_player.json")
            else:
                file=join(getcwd(),"Data/music_player.json")
            with open(normcase(file),"w") as f:
                f.write(r'{"path":[],"last_played":null,"pos":null,"volume":null,"play_list":{}}')
            self.get_data()
            # elif JSONDecodeError:

    def set_volume(self,event):
        self.volume=self.volume_scale.get()
        mixer_music.set_volume(self.volume)
        self.volume_scale.bell()
    def dump_data(self):
        try:
            if name =="nt":
                file=join(getcwd(),"Data\\music_player.json")
            else:
                file=join(getcwd(),"Data/music_player.json")
            with open(normcase(file),"w") as f:
                self.json_data["path"]=self.file_dir
                
                self.json_data["last_played"]=self.last_played
                self.json_data["pos"]=self.pos
                self.json_data["volume"]=self.volume
                self.json_data["play_list"]=self.udplay_list
                dump(self.json_data,f,indent=4,sort_keys=1)
        except FileNotFoundError:
                makedirs(join(getcwd(),"Data"))
                if name =="nt":
                    file=join(getcwd(),"Data\\music_player.json")
                else:
                    file=join(getcwd(),"Data/music_player.json")
                with open(normcase(file),"w") as f:
                    f.write(r'{"path":[],"last_played":null,"pos":null,"volume":null,"play_list":{}}')
            
                with open(normcase(file),"w") as f:
                    self.json_data["path"]=self.file_dir
                    self.json_data["last_played"]=self.last_played
                    self.json_data["pos"]=self.pos
                    self.json_data["volume"]=self.volume
                    self.json_data["play_list"]=self.udplay_list
                    dump(self.json_data,f,indent=4,sort_keys=1) 
    def next(self,event=None):
    
        self.a=self.list.curselection()
        self.list.select_clear(self.a[0])
        if self.a[0]+1==self.list.size():
            self.list.selection_set(0)
            # self.list.selection_set(0)
            self.list.see(self.a[0]+1)
            #print("Changed to 0 in try")    
        else:
            self.list.selection_set(self.a[0]+1)
            self.list.see(self.a[0]+1)
            #print("tried Next")
        
        self.play(repeat=True)
        # self.list.
    def previous(self,event=None):
        self.a=self.list.curselection()
        #print(self.a)
        self.list.select_clear(self.a[0])
        if self.a[0]==0:
            self.list.selection_set(self.list.size()-1)
            # self.list.selection_set(0)
            self.list.see(self.list.size()-1)
            # #print("Changed to 0 in try")    
        else:
            self.list.selection_set(self.a[0]-1)
            self.list.see(self.a[0]-1)
            # #print("tried Next")
        
        self.play(repeat=True)

    def check_end_position(self):
        audio=MP3(self.last_played)
        end=audio.info.length
        self.end_time=round(end/60,3)
        #print(self.end_time)
        try:
            while not self.exited:
                self.pos=mixer_music.get_pos()
                end_time=round(round(round(self.pos/1000,2)//60,2)+round(round(self.pos/1000,2)%60,2)/100,3)
                if end_time==self.end_time or mixer_music.get_busy()==0:
                    self.next()
                elif type(end_time) == float or type(end_time) == int:
                    self.progresslabel["text"] = f"{end_time}/{self.end_time}"
            return True
        except Exception as e:
            #print(e)
            return False    
     
    def close_floder(self):
        self.close_window=Tk()
        self.radio_value=IntVar()
        for vlue,file in enumerate(self.file_dir):
            self.radio_button=Radiobutton(self.close_window,variable=self.radio_value,value=vlue,text=file).pack(anchor=W)
        # self.radio_button.deselect()
        Button(self.close_window,text="Remove",command=self.remove_folder).pack()
        pass
    def remove_folder(self):
        #print("removing")
        self.file_dir.pop(self.radio_value.get())
        self.list.delete(0,END)
        for file in self.file_dir:
            self.open_folder(a=file)
        self.close_window.destroy()
        # self.close_folder()
    def play2(self,event=None):
        self.play()
        self.play()
    def creat_playlist(self):
        def add():
            a=self.play_list_list.curselection()
            play_name=self.play_list_name.get()
            if self.udplay_list.__contains__(play_name):
                a=askyesno("PLaylit",f"The Play list {play_name} Already exist ")
                if a:
                    self.udplay_list[play_name]=None
                else:
                    return None
            udlist=[]
            for index in a:
                    
                # index=self.list.curselection()
                name=self.play_list[index]
                file=join(self.file_name_dir[name],name)
                # self.list.selection_set(index)
                udlist.append(file)
        
            self.udplay_list[play_name]=udlist
            self.list_menu.add_command(label=play_name,command=lambda :self.play_play_list(play_name))
            showinfo("Created Playlist",f"Successfully Created Playlist {play_name}")
            self.play_list_window.destroy()
                
            pass

        def continuee():
            self.play_list_list=Listbox(self.play_list_window,width=30,selectmode=MULTIPLE)
            self.play_list_list.pack()
            Label(self.play_list_window,text="Select the Songs to add to the playlist").pack()
            
            for file in self.file_dir:
                self.open_folder(a=file,list_=self.play_list_list)
            Button(self.play_list_window,text="Add to playlist",command=add).pack()
        
        self.play_list_window=Tk()
        Label(self.play_list_window,text="Enter Playlist name").pack()
        self.play_list_name=Entry(self.play_list_window)
        self.play_list_name.pack()
        Button(self.play_list_window,text="Continue",command=continuee).pack()
        
    def play_play_list(self,key_):
        list_=self.udplay_list[key_]
        self.list.delete(0,END)
        del self.play_list
        del self.file_name_dir
        self.play_list=[]
        self.file_name_dir={}
        for name in list_:
            dir_name,bname=split(name)
            self.list.insert(END,bname)
            self.file_name_dir[bname]=normcase(dir_name)
            self.play_list.append(bname)

        
        pass

music_player()



