import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog as fd

def print_stats(modelnumber=str, lines=list):
    for l in lines:
        if float(l[0]) > float(modelnumber):
            break 
        elif l[0] == modelnumber:
            age = l[2]
            mass = l[4]
            Hecore = l[34]
            Ccore = l[35]
            Teff = 10**(float(l[39]))
            L = 10**(float(l[40]))
            R = 10**(float(l[41]))
            cntrrho = 10**(float(l[45]))
            cntrrho = np.format_float_scientific(cntrrho)
            cntrT = 10**(float(l[46]))
            cntrT = np.format_float_scientific(cntrT)
            return f'Parametry:\n Model: {modelnumber}\n Wiek: {age} yrs\n Masa: {mass} M_sun\n Jądro He: {Hecore} M_sun\n Jądro CO: {Ccore} M_sun\n T_eff: {Teff} K\n L: {L} L_sun\n R: {R} R_sun\n cntr_rho: {cntrrho} g/cm^3\n cntr_T: {cntrT} K'

def search_parameter(param,value,lines):
    val = float(value)
    if param == 'R':
        paramindex = 41
        log_flag = True
    elif param == 'Teff':
        paramindex = 39
        log_flag = True
    elif param == 'L':
        paramindex = 40
        log_flag = True
    elif param == 'cntrrho':
        paramindex = 45
        log_flag = True
    elif param == 'cntrT':
        paramindex = 46
        log_flag = True
    elif param == 'M' or param == 'Mass':
        paramindex = 4
        log_flag = False
    elif param == 'Age':
        paramindex = 2
        log_flag = False
    else:
        paramindex = None
        log_flag = False
    if log_flag == True:
        val = np.log10(val)
    if paramindex != None:
        differences = []
        for i in range(len(lines)):
            diff = np.abs(float(lines[i][paramindex]) - val)
            differences.append(diff)
        result_index = differences.index(min(differences))
        return result_index
    else:
        print('MESA histreader: search unsuccessful, setting default')
        return 0 

def die():
    print('MESA histreader: shutting down')
    root.destroy()

global openfile
global currenttext
global lines
global label

def make_label():
    global currenttext
    global label
    label = tk.Label(root,text=currenttext,anchor='w',justify='left')
    label.pack()

def file_call():
    global openfile
    global currenttext
    global lines
    openfile = fd.askopenfilename()
    with open(openfile,'r') as f:
        lines = f.readlines()
        lines = lines[6:] 
        for i in range(len(lines)):
            lines[i] = lines[i].split()
    currenttext = print_stats(modelnumber='1',lines=lines)
    make_label()

def label_redraw():
    global label
    label.destroy()
    make_label()

def change_current_model():
    global currenttext
    global lines
    global label
    Model_no = tk.simpledialog.askstring(title="Model number change",prompt="Input model number")
    #print(Model_no) #Debug
    if float(Model_no) % 5 != 0:
        print('MESA histread: Incorrect model number, setting default')
        Model_no = '1'
    currenttext = print_stats(modelnumber=Model_no,lines=lines)
    label_redraw()

def search_by_param():
    global currenttext
    global lines
    global label
    searchvar = tk.simpledialog.askstring(title="Search parameter",prompt="Input search variable (R, Teff, etc.)")
    searchval = tk.simpledialog.askstring(title="Search parameter",prompt="Input search variable value")
    index = search_parameter(searchvar,searchval,lines)
    Model_no = lines[index][0]
    currenttext = print_stats(modelnumber=Model_no,lines=lines)
    label_redraw()

def help_me():
    messagebox.showinfo(title='Info',message='Valid search paramterers:\n R, Teff, L, cntrrho, cntrT, M, Age')

root = tk.Tk()
root.geometry('600x450')
root.title('MESA histreader V2.0')
frm = ttk.Frame(root, padding=10)
menubar = tk.Menu(root)

filemenu = tk.Menu(menubar,tearoff=0)
filemenu.add_command(label="Open",command=file_call)
filemenu.add_command(label="Exit",command=die)
menubar.add_cascade(label="File", menu=filemenu)
filemenu2 = tk.Menu(menubar,tearoff=0)
filemenu2.add_command(label="Change model number",command=change_current_model)
filemenu2.add_command(label="Search by parameter",command=search_by_param)
filemenu2.add_command(label="Help",command=help_me)
menubar.add_cascade(label="Search", menu=filemenu2)
root.config(menu=menubar)

root.mainloop()