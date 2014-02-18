#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : Turk Site : http://rpy-italia.org/
# 
# Date : 26/05/2013
#

import os
import subprocess
import curses                   # curses e' l'interfaccia per l'acquisizione di pressioni di tasti nel menu

screen = curses.initscr()       # inizializza una nuova finestra per catturare la pressione dei tasti
curses.noecho() 
curses.cbreak()                 # Disattiva il buffering linea
curses.start_color()            # Consente di utilizzare i colori
screen.keypad(1)                # Acquisire l'input da tastiera


# Modificare questa sezione per utilizzare colori diversi per evidenziare le scelte
curses.init_pair(1,curses.COLOR_RED, curses.COLOR_WHITE)    # Imposta coppia di colori, testo Rosso con sfondo bianco (selezione)
h = curses.color_pair(1)                                    # h e' la colorazione di una opzione di menu evidenziato
n = curses.A_NORMAL                                         # n e' la colorazione di una opzione di menu non evidenziato

MENU = "menu"
COMMAND = "command"
FUNZIONE = "funzione"
menu_data = {'title': "MENU di gestione delle serie TVD", 'type': MENU, 'subtitle': "Selezionare un opzione e premere INVIO",
	    'options': [{'title': "Esegui ricerca delle serie", 'type':FUNZIONE, 'funzione': 'scansiona' },
    			{'title': "Da qui in giu non fanno niente", 'type':COMMAND, 'command': 'echo "non fanno niente!!"' },
    			{'title': "Visualizza LCD", 'type': FUNZIONE, 'funzione': 'visualizzalcd' },
 	    		{'title': "Operazioni sul Raspy", 'type': MENU, 'subtitle': "Selezionare un opzione",
    			'options': [{'title': "Reboot", 'type': COMMAND, 'command': 'echo "non fanno niente!!"' },
					{'title': "Spegni il Raspy", 'type': COMMAND, 'command': '' },
					{'title': "Backup della SD", 'type': COMMAND, 'command': '' },
					{'title': "Restore del Backup della SD", 'type': COMMAND, 'command': '' },]},
    			{'title': "Operazioni sul FILE Log", 'type': MENU, 'subtitle': "Selezionare un opzione",
			'options': [	{ 'title': "Visualizza il File LOG", 'type': FUNZIONE, 'funzione': 'log' },
					{ 'title': "Cancella il File LOG", 'type': COMMAND, 'command': '' },]},
            ]}

# Questa funzione inserisce l'ultima opzione giusta a seconda della paginata in cui ci si trova
def runmenu(menu, parent):
     # imposta l'ultima opzione a seconda del menu o sottomenu
    if parent is None:
        lastoption = "Esci (Ritorna al terminale)"
    else:
        lastoption = "Ritorna al menu: %s " % parent['title']

    optioncount = len(menu['options'])  # calcola il numero delle opzioni del menu
    pos = 0                             # evidenzia la posizione 0 (prima opzione) si puo cambiare
    oldpos = None                       # previene il refresh della finestra ogni volta
    x = None                            # controllo per uscire dal loop quando premuto INVIO
  
  # Loop fino alla pressione di INVIO
    while x != ord('c'):
        if pos != oldpos:
            oldpos = pos
            screen.clear()                                          # Cancella lo schermo alla pressione del tasto
            screen.border(0)	                                    # Disegna il bordo intorno alla finestra mettere # per toglierla
            screen.addstr(2,2, menu['title'], curses.A_STANDOUT)    # Titolo del menu
            screen.addstr(4,2, menu['subtitle'], curses.A_BOLD)     # Sottotitolo del menu

            # Scrive tutte le opzioni del menu ed evidenzia la 'pos'
            for index in range(optioncount):
                textstyle = n
                if pos == index:
                    textstyle = h
                screen.addstr(5+index,4, "%d - %s" % (index+1, menu['options'][index]['title']), textstyle)
        
            # Scrive l'ultima opzione
            textstyle = n
            if pos == optioncount:
                textstyle = h
      
            screen.addstr(5+optioncount,4, "%d - %s" % (optioncount+1, lastoption), textstyle)
            screen.refresh()
        
        x = screen.getch() # input della tastiera
        if x == ord('\n'):
            x = ord('c')
  
        if x >= ord('1') and x <= ord(str(optioncount+1)):
            pos = x - ord('0') - 1 # converte la pressione del tasto in un numero - 1
        elif x == 258: # tasto giu
            if pos < optioncount:
                pos += 1
            else: pos = 0
        elif x == 8: # tasto giu
            if pos < optioncount:
                pos += 1
            else: pos = 0
        elif x == 259: # tasto su
            if pos > 0:
                pos += -1
            else: pos = optioncount
        elif x == 259: # tasto su
            if pos > 0:
                pos += -1
            else: pos = optioncount
        elif x != ord('\n'):
             curses.flash()
  
    # ritorna "pos" in base alla selezione fatta
    return pos

# Questa funzione chiama scrive il sottomenu o esegue il comando o la funzione
def processmenu(menu, parent=None):
    optioncount = len(menu['options'])
    exitmenu = False
  
    while not exitmenu: #Loop fino a quando l'user non termina il programma
        getin = runmenu(menu, parent)
        if getin == optioncount:
            exitmenu = True
    
        elif menu['options'][getin]['type'] == COMMAND:
            os.system(menu['options'][getin]['command']) # esegue il comando
      
        elif menu['options'][getin]['type'] == MENU:
            processmenu(menu['options'][getin], menu) # visualizza il submenu
    
        elif menu['options'][getin]['type'] == FUNZIONE: # esegue le funzioni
            if menu['options'][getin]['funzione'] == "scansiona":
	        scansiona()
            elif menu['options'][getin]['funzione'] == "visualizzalcd":
	        visualizza_lcd()
            elif menu['options'][getin]['funzione'] == "log":
	        visualizza_log()
            elif menu['options'][getin]['funzione'] == "cancellalog":
	        cancella_log()

# Qui bisogna aggiungere le funzioni da richiamare
def scansiona():
    curses.endwin() # per evitare i problemi di visualizzazione si ritorna alla modalità normale del terminal
    os.system("clear")
    os.system("ls -l --color / | more")

    print ""
    raw_input("Premi INVIO per continuare") # attendo INVIO altrimenti torna immediatamente al menu
    os.system("clear") # pulisco il terminale prima di tornare al menu

def visualizza_lcd():
    curses.endwin()
    os.system("clear")

def visualizza_log():
    curses.endwin()
    os.system("clear")

# Programma principale
processmenu(menu_data)
curses.endwin() #IMPORTATNE!  Questo chiude il Menu e ritorna al Terminale riportando normale
