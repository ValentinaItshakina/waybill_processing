from datetime import date
import os

def process_file(input_path: str, option: str, filename) -> str:
    if option == 'type1':
        return process_file_Teleon(input_path, filename)
    elif option == 'type2':
        return process_file_Invoce(input_path, filename)
    else:
        raise ValueError("Неверная опция")

def process_file_Teleon(input_path: str, filename) -> str:
    # Создаём имя выходного файла
    output_path = input_path.rsplit('\\', 1)[0] +'\\'+ str(filename) + '_rez.txt'
    
    # Открываем файлы
    with open(input_path, encoding='utf-8') as F, open(output_path, "w") as R:
        f = F.readlines()
        i = 0
        k = 0
        rez = {}

        for l in range(len(f)):   # убираем вводную инфу
            if 'Description' in f[l]:
                f = f[l+1:]
                break

        l = 0
        while l < len(f):  # чистим от концов страниц
            if 'Teleon' in f[l]:
                k = l+1
                while k < len(f) and not 'Description' in f[k]:
                    k += 1
                del f[l:k+1]
                l = l-2
                k = l
            if 'LENTIS LU-313' in f[l]:
                k = l+1
                while k < len(f) and not 'Teleon' in f[k]:
                    k += 1
                del f[l:k]
                l = l-2
            if f[l] == '\n':
                del f[l]
                l -= 1
            l += 1

        sequence_number = 0
        k = 0
        while k < len(f):
            while k < len(f) and f[k].split()[0] == str(sequence_number + 1):
                sequence_number = int(f[k].split()[0])
                ind = f[k].split()[1]
                nam = ' '.join(f[k].split()[2:])
                nam = nam[:nam.rfind('D')+4].strip()
                con = int(nam[nam.rfind(' ')+1:])
                nam = nam[:nam.rfind(' ')]
                power = nam[nam.rfind(' '):].strip()
                nam = nam[:nam.rfind(' ')].strip()
                s = ind + ';' + nam + '; POWER ' + power
                rez[s] = rez.get(s, [])
                k += 1
                
                if k < len(f):
                    country = f[k].split()[-1]
                    while k < len(f) and 'Use by' not in f[k]:
                        k += 1
                    
                    for j in range(con):
                        if k < len(f):
                            st = f[k].split(',')[0].strip() + ';' + date.today().strftime("%Y-%m") + ';' + f[k].split(',')[1].split()[-1] + ';' + country
                            rez[s].append(st)
                            k += 1
            
            if k < len(f) and 'Total EUR' in f[k]:
                sequence_number = 0
            k += 1

        for i in rez:
            for j in rez[i]:
                R.write(i + ';' + j + '\n')
    
    return output_path

def process_file_Invoce(input_path: str, filename) -> str:
    # Создаём имя выходного файла
    output_path = input_path.rsplit('\\', 1)[0] +'\\'+ str(filename) + '_rez.txt'
    
    # Открываем файлы
    with open(input_path, encoding='utf-8') as F, open(output_path, "w") as R:
        f = F.readlines()
        i = 0
        k = 0
        rez = {}
        for l in range(len(f)):   #убираем вводную инфу
            if 'Pos' in f[l]:
                f = f[l:]
                break

        l = len(f)-1
        while l >0:  #чистим от концов страниц
            if 'Shipping Agent Code' in f[l]:
                k = l+1
                while not 'Continued' in f[l]:
                    l-=1
                del f[l:k+1]
                l = min(k, len(f)-1)
            if 'INVOICE' in f[l]:
                k = l+1
                while not 'Continued' in f[l]:
                    l-=1
                del f[l:k]
                l = min(k, len(f)-1)
            
            if f[l]=='\n':
                del f[l]
            # if l == 1476:
            #     r = f[l]
            l-=1
            #print(f)

        k =0
        for i in range(len(f)):
            print(i, f[i])

        while k < len(f):
            if 'Pos' in f[k]:# для удобства вырезаю
                k+=1
                ind = f[k].split()[1]
                nam= ' '.join(f[k].split()[2:])
                nam= nam[:nam.find('Pieces')-1]
                con = int(nam[nam.rfind(' ')+1:])
                nam = nam[:nam.rfind(' ')]+' '
                k+=1
                while not ('POWER' in nam and 'D' in nam and nam.find('POWER') < nam.rfind('D')):
                    nam+=f[k].strip()+' '
                    k+=1
                power = nam[nam.find('POWER'):].strip()
                nam = nam[:nam.find('POWER')].strip()
                s = ind + ';' + nam + ';' + power
                rez[s] = rez.get(s, [])
            if 'Serial Nr.' in f[k]:
                k+=1
                while con > 0:
                    if 'Continued' in f[k]:
                        r = f[k]
                    st = ';'.join(f[k].split()[:2])+ ';' + ';'.join(f[k].split()[3:])
                    rez[s].append(st)
                    k+=1
                    con-=1
                k-=1
            print(k, f[k])
            k+=1
            # if k >2237:
            


        for i in rez:
            for j in rez[i]:
                # print(i+';'+j)
                R.write(i+';'+j+'\n')


        return output_path

process_file_Invoce("D:\\Users\\valen\\Downloads\\Telegram Desktop\\Invoice - IN00170925-1.txt", "Invoice - IN00170925-1")