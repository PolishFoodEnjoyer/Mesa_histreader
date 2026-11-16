import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog as fd

global openfile
global currenttext
global lines
global label
global headers

def print_stats(modelnumber=str, lines=list, headers=list):
    for l in lines:
        if float(l[0]) > float(modelnumber):
            break 
        elif l[0] == modelnumber:
            age = l[headers.index('star_age')]
            mass = l[headers.index('star_mass')]
            Hecore = l[headers.index('he_core_mass')]
            Ccore = l[headers.index('co_core_mass')]
            Teff = 10**(float(l[headers.index('log_Teff')]))
            L = 10**(float(l[headers.index('log_L')]))
            R = 10**(float(l[headers.index('log_R')]))
            cntrrho = 10**(float(l[headers.index('log_cntr_Rho')]))
            cntrrho = np.format_float_scientific(cntrrho)
            cntrT = 10**(float(l[headers.index('log_cntr_T')]))
            cntrT = np.format_float_scientific(cntrT)
            return f'Parametry:\n Model: {modelnumber}\n Wiek: {age} yrs\n Masa: {mass} M_sun\n Jądro He: {Hecore} M_sun\n Jądro CO: {Ccore} M_sun\n T_eff: {Teff} K\n L: {L} L_sun\n R: {R} R_sun\n cntr_rho: {cntrrho} g/cm^3\n cntr_T: {cntrT} K'

def search_parameter(param,value,lines,headers):
    val = float(value)
    if param == 'R':
        paramindex = headers.index('log_R')
        log_flag = True
    elif param == 'Teff':
        paramindex = headers.index('log_Teff')
        log_flag = True
    elif param == 'L':
        paramindex = headers.index('log_L')
        log_flag = True
    elif param == 'cntrrho':
        paramindex = headers.index('log_cntr_Rho')
        log_flag = True
    elif param == 'cntrT':
        paramindex = headers.index('log_cntr_T')
        log_flag = True
    elif param == 'M' or param == 'Mass':
        paramindex = headers.index('star_mass')
        log_flag = False
    elif param == 'Age':
        paramindex = headers.index('star_age')
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

def make_label():
    global currenttext
    global label
    label = tk.Label(root,text=currenttext,anchor='w',justify='left')
    label.pack()

def file_call():
    global openfile
    global currenttext
    global lines
    global headers
    openfile = fd.askopenfilename()
    with open(openfile,'r') as f:
        lines = f.readlines()
        headerline = lines[5]
        headers = headerline.split()
        lines = lines[6:] 
        for i in range(len(lines)):
            lines[i] = lines[i].split()
    currenttext = print_stats(modelnumber='1',lines=lines,headers=headers)
    make_label()

def label_redraw():
    global label
    label.destroy()
    make_label()

def change_current_model():
    global currenttext
    global lines
    global label
    global headers
    Model_no = tk.simpledialog.askstring(title="Model number change",prompt="Input model number")
    #print(Model_no) #Debug
    if float(Model_no) % 5 != 0:
        print('MESA histread: Incorrect model number, setting default')
        Model_no = '1'
    currenttext = print_stats(modelnumber=Model_no,lines=lines,headers=headers)
    label_redraw()

def search_by_param():
    global currenttext
    global lines
    global label
    global headers
    searchvar = tk.simpledialog.askstring(title="Search parameter",prompt="Input search variable (R, Teff, etc.)")
    searchval = tk.simpledialog.askstring(title="Search parameter",prompt="Input search variable value")
    index = search_parameter(searchvar,searchval,lines,headers)
    Model_no = lines[index][0]
    currenttext = print_stats(modelnumber=Model_no,lines=lines,headers=headers)
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
