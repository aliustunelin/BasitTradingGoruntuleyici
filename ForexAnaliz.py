# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 00:45:45 2020

@author: alius
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np





window=tk.Tk()
window.geometry("1080x640")
window.title("degisik hareketler")


#ana şemadaki 3'lü panel ve window bölümleri
pw=ttk.Panedwindow(window, orient=tk.HORIZONTAL)
pw.pack(fill=tk.BOTH, expand=True)

w2=ttk.Panedwindow(pw, orient=tk.VERTICAL)

frame1=ttk.Frame(pw, width=360, height=640,relief=tk.SUNKEN)
frame2=ttk.Frame(pw, width=720, height=400,relief=tk.SUNKEN)
frame3=ttk.Frame(pw, width=720, height=200,relief=tk.SUNKEN)

w2.add(frame2)
w2.add(frame3)
#iç içe ifadelerde birşey eklerken onu add ile ilk katmandakilere ekleriz
pw.add(w2)  #normalde grid vs ile window'a direk gömersin ama add lazım java mantığı
pw.add(frame1)



#frame1'deki major minor menüsü
treeview=ttk.Treeview(frame1)
treeview.grid(row=0, column=1, padx=25, pady=25)
treeview.insert("","0","Major",text="Major")
treeview.insert("Major","1","EURO/USD",text="EURO/USD")
treeview.insert("","2","Minor",text="Minor")
treeview.insert("Minor","3","EURO/GBR",text="EURO/GBR")



item = ""

def callback(event):
    global item
    item = treeview.identify("item", event.x,event.y)
    #print(item)
        
treeview.bind("<Double-1>", callback)

def readNews(item): #textbox'da txt'den okuduğumuz yalan haberlerş bascaz
    if item=="EURO/USD":
        news=pd.read_csv("SahteHaberUsd.txt")
        
    elif item=="EURO/GBR":
        news=pd.read_csv("SahteHaberGbr.txt")        
    
    textBox.insert(tk.INSERT, news)        
    

def openTrade():
    print("Open Trading")
    global data, future, line ,data_close_array, canvas, future_array, ax1, line2, canvas2, ax2,line3, canvas3, ax3, line4, canvas4, ax4
    if item != "":
        print("Secilen parite: ",item)
        
        if item=="EURO/USD":
            open_button.config(state="disable")
            start_button.config(state="normal")
            
            #bilgiler csv'den okunacak onlarda burada
            data=pd.read_csv("EuroUsa.csv") 
               #sadece kapanış değerlerini baastırsak şuan yeterli 
            future=data[-1000:]
            data=data[:len(data)-1000]
            data_close_array=data.close1.values
            future_array=list(future.close1.values)                           
    
            #iki plot olcak line plot
            fig1=plt.Figure(figsize=(5,4),dpi=100)
            ax1=fig1.add_subplot(111) #eksen 1.satır1.sutun1taneplot
            line,=ax1.plot(range(len(data)),data.close1,color="blue")
            canvas=FigureCanvasTkAgg(fig1,master=tab1) #oluşşturulan figur bir canvas'a eklenmeli
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)  
            
            #öteki plot scatter
            fig2=plt.Figure(figsize=(5,4),dpi=100)
            ax2=fig2.add_subplot(111) #ikinci eksen
            line2=ax2.scatter(range(len(data)),data.close1,s=1, alpha=0.5, color="blue")
            canvas2=FigureCanvasTkAgg(fig2, master=tab2) #master tab1,2 meselesi hangi tab altına ekrana basacağız ??
            canvas2.draw()
            canvas2.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH, expand=1) #tüm bu top ve both tikenterdan geliyor
            
            
            #şuanlık sahte olan haberleri okuma
            readNews(item)
            
        elif item== "EURO/GBR":
            #print(item+" nasii")    
            open_button.config(state="disabled") #seim yapılnca open butonu gitsin start butonu on olsun
            start_button.config(state="normal")
            
            #verileri okuom            
            data=pd.read_csv("EuroGbr.csv")
            
            #verilerin sadece sonuçları lazım onları alıyorum
            future=data[-1000:]
            data=data[:len(data)-1000]
            data_close_array=data.close1.values
            future_array=list(future.close1.values)
            
            #lin plot
            fig3=plt.Figure(figsize=(5,4), dpi=100)
            ax3=fig3.add_subplot(111)
            line3,=ax3.plot(range(len(data)),data.close1, color="blue")
            canvas3=FigureCanvasTkAgg(fig3, master=tab1)    
            canvas3.draw()
            canvas3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            
            #scatter plot
            fig4=plt.Figure(figsize=(5,4), dpi=100)
            ax4=fig4.add_subplot(111)
            line4=ax4.scatter(range(len(data)), data.close1, s=1, alpha=0.5, color="blue")
            canvas4=FigureCanvasTkAgg(fig4, master=tab2) #tab1 line tab2 scatter menüsü
            canvas4.draw()
            canvas4.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            #sahte haber gbr okuma
            readNews(item)
            
        else: #hic birsey secmezse
            messagebox.showinfo(title="Nabion La", message="La gardas 2 defa tikla birinin ustune")
    else: #tee en başta item girmez ise
        messagebox.showinfo(title="Nabion La", message="La gardas 2 defa tikla birinin ustune")
        
            
    
    
#frame1'deki buton
open_button=tk.Button(frame1, text="Open Trading",command=openTrade)
open_button.grid(row=2,column=1,padx=5, pady=5)




#frame3'de yazıları haberleri basacak text 

textBox=tk.Text(frame3, width=70, height=10, wrap="word")
textBox.grid(row=0, column=0, padx=25, pady=35)
scroll=tk.Scrollbar(frame3, orient=tk.VERTICAL, command=textBox.yview)#yview hazır fonk
scroll.grid(row=0, column=1, sticky=tk.N + tk.S, pady=10) #sticky yapıştırır N S vs yönler
textBox.config(yscrollcommand=scroll.set)


#trade grafikleri frame2'de bunda tabview var

tabs=ttk.Notebook(frame2,width=540, height=300)
tabs.place(x=25, y=25)


tab1=ttk.Frame(tabs,width=50, height=50)
tab2=ttk.Frame(tabs)

tabs.add(tab1,text="line")
tabs.add(tab2,text="scatter", compound=tk.LEFT)

method=tk.StringVar()
tk.Radiobutton(frame2,text="m1: ",value="m1",variable=method).place(x=580, y=100)
tk.Radiobutton(frame2,text="m2: ",value="m2",variable=method).place(x=580, y=125)

label_frame=tk.LabelFrame(frame2, text="Sonuc" , width=100, height=150)
label_frame.place(x=580, y=25)
tk.Label(label_frame,text="Satin Al: ",bd=3).grid(row=0,column=0)
tk.Label(label_frame,text="SatiVerGitsin: ",bd=3).grid(row=1,column=0)


buy_value=tk.Label(label_frame, text="1", bd=3)
buy_value.grid(row=0, column=1)
sell_value=tk.Label(label_frame, text="0", bd=3)
sell_value.grid(row=1, column=1)


def moving_average(a,n=50):
    ret=np.cumsum(a,dtype=float)
    ret[n:]=ret[n:]-ret[:-n]
    return ret[n-1:]/n    
    
def update():
    global data_close_array, ax1, ax2, ax3, ax4
    spread=0.0003
    buy_value.config(text= str((data_close_array[-1]-spread).round(5)))
    sell_value.config(text= str((data_close_array[-1]+spread).round(5)))
    
    window.after(500,update) #ekranı yenile, yenileyincede yeni değerler satın alma ve satma kısımlarında önüne geliyor
    data_close_array=np.append(data_close_array, future_array.pop(0)) #future array-en sondaki elemanlar-dekileri data close'e atıyoruz ve ekranda sürekli güncellenen bir yapı oluyor
    
    
    if method.get() == "m1":
        if item=="EURO/USD":
            #line pllot güncelleme
            ax1.set_xlim(0, len(data_close_array)+10)
            line.set_ydata(data_close_array)
            line.set_xdata(range(len(data_close_array)))
            
            #scateer plot güncellem
            ax2.set_xlim(0, len(data_close_array)+10)
            ax2.scatter(range(len(data_close_array)),data_close_array,s=1,slpha=0.5, color="blue")
            
            
            #moving avarege güncellemesi
            n=50
            mid_rolling=moving_average(data_close_array,n)
            ax1.plot(range(n-1,len(data_close_array)),mid_rolling,linestyle="--", color="red")
            ax2.plot(range(n-1,len(data_close_array)),mid_rolling,linestyle="--", color="red")
            
            canvas.draw()
            canvas2.draw()
            
            
            
def oylesine():
   pass #kullanılmayacak bir fonksiyon yada daha hazırlamadığın fonk içine pass döndür

 
    
   
   
def startTrading():
    print("start Trading")
    window.after(0,update) #window güncellencek 0 anında yani tıklayınca hemen update'e git
    
    
    
start_button=tk.Button(frame2, text="Start Trading",command=startTrading)
start_button.place(x=580,y=150)
start_button.config(state="disabled")





window.mainloop()