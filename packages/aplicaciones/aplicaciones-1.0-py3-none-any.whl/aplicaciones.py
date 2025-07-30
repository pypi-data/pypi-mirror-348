#######################
# Curso Python Nivel II
# Autor: Ernesto Castro
# Fecha: 03/24/2025
# Version: 1.0
########################


#El programa muestra un menu al usuario para abrir cualquiera de las aplicaciones: Notepad, Calculadora, Word, Excel, Paint.


import subprocess

'''
Opciones del programa aplicaciones .py
El usuario escoge la aplicacion que desea abrir usando alguna de estas opciones:
n -> abrir Notepad
c -> abrir Calculadora
w -> abrir Word
e -> abrir excel
p -> abrir Paint
s - > salit
'''

comando = 'x'
while comando != 's':
    comando = input("\nCual aplicacion desea iniciar? \n" \
            "Notepad -> [n]\n" \
            "Calculadora ->[c]\n" \
            "Word ->[w]\n" \
            "Excel ->[e], " \
            "Paint ->[p]\n" \
            "Salir ->[s]\n" \
            "Opcion:  ")

   
    if comando == 'n':  
       subprocess.Popen(['notepad.exe'])
    
    elif comando == 'c': 
       subprocess.Popen(['calc.exe'])

    elif comando == 'w':  
       subprocess.Popen(['C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\WINWORD.EXE'])

    elif comando == 'e':  
       subprocess.Popen(['C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\EXCEL.EXE'])

    elif comando == 'p':  
       subprocess.Popen(['mspaint.exe'])

