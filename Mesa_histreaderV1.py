import numpy as np

def main():
    infile = input('Podaj ścieżkę do history.data (lub wciśnij RETURN jeśli jesteś w katalogu LOGS)\n')
    if infile == '':
        try:
            infile = 'history.data'
        except:
            print('Nie znaleziono pliku history.data')
            return
    with open(infile,'r') as f:
        lines = f.readlines()
        lines = lines[6:]
        for i in range(len(lines)):
            lines[i] = lines[i].split()
        model = input('Podaj numer modelu:\n')
        if model == '':
            model = '1'
        elif float(model) % 5 != 0:
            print('Nr modelu musi być podzielny przez 5!')
            return
        print_stats(model,lines)
    search = input('Wyszukać po wartości parametru? Y/N\n')
    if search == 'Y':
        parameter = input('Podaj parametr do wyszukania (np. R, Teff)\n')
        value = input('Podaj wartość do wyszukania\n')
        index = search_parameter(parameter,value,lines)
        modelnumber = lines[index][0]
        print_stats(modelnumber,lines)
    else:
        return

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
            print(f'Parametry:\n Model: {modelnumber}\n Wiek: {age} yrs\n Masa: {mass} M_sun\n Jądro He: {Hecore} M_sun\n Jądro CO: {Ccore} M_sun\n T_eff: {Teff} K\n L: {L} L_sun\n R: {R} R_sun\n cntr_rho: {cntrrho} g/cm^3\n cntr_T: {cntrT} K\n')

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
        log_flag = 2
    else:
        paramindex = None
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
        print('Nie znaleziono paramteru\n')
        return

main()