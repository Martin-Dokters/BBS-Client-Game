import socket   
import random    

#Vergabe von Host/Adresse und Port
bbs_host = 'localhost'
bbs_port = random.randint(0,65535)


#Starten des BBS-Clients
def bbs_server(bbs_host,bbs_port):                                      #
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)    #Erstellung eines Socket-Objekts
    server_socket.bind((bbs_host,bbs_port))                             #Das Socket-Objekt bekommt eine Adresse und einen Port
    server_socket.listen(1)                                             #Limitiert die Anzahl an Leuten die sich verbinden koennen

    print(f"Server listining on {bbs_host}:{bbs_port}")                 #Die Adresse und Port wird ausgegeben 


    while True:                                                 #
        client_socket, client_address = server_socket.accept()  #Wartet das sich jemand Verbindet 
        print(f"Connection from {client_address}")              #und gibt die Adresse vom Nutzer aus

        def start(client_socket):                               #
            clear_command = b"\x1b[2J\x1b[H"                    #Erstellung einer Escape-Sequence
            client_socket.send(clear_command)                   #Sowie das ausfueren der Escape-Sequence

            Anzeige =   [                                                               #Deklarierung des Textes im Start Menue
                            "Wilkommen bei meinem 100 Stunden BBS-Client Projekt",      #
                            "",                                                         #
                            "",                                                         #           
                            "1: Spiel Spielen",                                         #
                            "2: Credits",                                               #
                            "3: Exit"                                                   #
                        ]                                                               #
            
            for i in range(len(Anzeige)):                                   #gibt alle Elemente von Anzeige aus
                client_socket.send(Anzeige[i].encode('utf-8') + b'\r\n')    #

            try:                                        
                while True:                             

                    data = client_socket.recv(1024)     #Empfaengt die Inputs vom Nutzer 
                    response = data.decode('utf-8')     #und uebertraegt diese in utf-8

                    if response == "1":              

                        def game(cs):              
                           
                            BLUE = "\033[94m"       #Deklarierung der einzelnen Farben 
                            GREEN = "\033[92m"      #
                            WHITE = "\033[97m"      #
                            RED = "\033[91m"        #
                            YELLOW = "\033[93m"     #

                            X = GREEN + "-" + WHITE     #Deklarierung der einzelnen Elementen, in Kombination mit der jeweiligen Farbe
                            P = BLUE + "|" + WHITE      #
                            W = "X"                     #
                            G = YELLOW + "!" + WHITE    #
                            E = RED + "A" + WHITE       #
                            L = " "

                            mapcounter = 1

                            def read_txt_file(file_path):                   #
                                global client_socket                        #
                                try:                                        #
                                    map1 = [""]                             #
                                    with open(file_path) as f:              #Versucht eine .txt Datei zu lesen
                                        map1 = [row.split() for row in f]   #traegt die daten in ein 2D-Array (map1) ein
                                finally:                                    #
                                    if map1[0] == "":                       #sollte nichts gelesen worden sein, wird das menue wieder angezeigt
                                        start(cs)                           #
                                                                            
                                    return map1                             
                               
                            
                            def nextmap(mapcounter):                                #
                                map1 = []                                           #
                                file_path = 'Maps/'+ str(mapcounter) + 'map.txt'    #Erstellung von file-path aus der kombination des mapcounters und 'map.txt'
                                map1 = read_txt_file(file_path)                     #map1 = Daten aus der Datei
                                map2 = map1                                         #map2 = map1, damit map2 genauso gross ist
                                                                             
                                for row in range(len(map1)):                #schleife die durch das 2D-Array map1 geht
                                    for column in range(len(map1[row])):    #
                                        if map1[row][column] == "X":        #conventiert text aus map1 in die Variablen der Elementen (Zeile:54-59)
                                            map2[row][column] = X           #
                                        if map1[row][column] == "P":        #
                                            map2[row][column] = P           #
                                        if map1[row][column] == "W":        #
                                            map2[row][column] = W           #
                                        if map1[row][column] == "G":        #
                                            map2[row][column] = G           #
                                        if map1[row][column] == "L":        #
                                            map2[row][column] = L           #
                                        if map1[row][column] == "E":        #
                                            map2[row][column] = E           #
                                                                            
                                return map2                                 
                            
                            map2 = nextmap(mapcounter)  #map2 = die map von dem mapcounter

                            def Enemy_movement(map2,mc):    #
                                px,py = poscheck(map2)      #px,py = Position des Spielers
                                Ex = []                     #Gegner x koordinaten
                                Ey = []                     #Gegner y koordinaten
                                
                                
                                for row in range(len(map2)):                #Geht durch jede Reihe und Spalte von map2
                                    for column in range(len(map2[row])):    #
                                        if map2[row][column] == E:          #Traegt die koordinaten von allen Gegnern (E) ein
                                            x,y = column,row                #

                                            Ex.append(x)                    #x und y werden in den Arrays Ex und Ey eingegeben
                                            Ey.append(y)                    #
                                
                                
                                for i in range(len(Ex)):    
                                    movement = False        
                                    
                                    Ex1 = 0
                                    Ey1 = 0
                                    
                                    
                
                                    if Ey[i] > py and movement == False:                        #Es wird Gegner y koordinate mit Spieler y koordinate verglichen. movement muss False sein
                                        Ey1 = Ey[i] - 1                                         #naechste y koordinate vom Gegner wird eingetragen
                                        if map2[Ey1][Ex[i]] != W and map2[Ey1][Ex[i]] != E:     #sollte da keine Wand (W) oder Gegner (E) sein:
                                            map2[Ey[i]][Ex[i]] = X                              #wird auf der Aktuellen Position Boden (X) eingetragen
                                            map2[Ey1][Ex[i]] = E                                #und auf der naechsten Position ein Gegner (E) Eingetragen   
                                            movement = True                                     #movement wird auf True gestellt, damit der Gegner nur in eine richtung geht
                                    
                                    if Ex[i] > px and movement == False:                        #Es wird Gegner x koordinate mit Spieler x koordinate verglichen. movement muss False sein
                                        Ex1 = Ex[i] - 1                                         #naechste x koordinate vom Gegner wird eingetragen
                                        if map2[Ey[i]][Ex1] != W and map2[Ey[i]][Ex1] != E:     #siehe oben
                                            map2[Ey[i]][Ex[i]] = X                              #
                                            map2[Ey[i]][Ex1] = E                                #
                                            movement = True                                     #
                                    
                                    if Ey[i] < py and movement == False:                        #Es wird Gegner y koordinate mit Spieler y koordinate verglichen. movement muss False sein
                                        Ey1 = Ey[i] + 1                                         #naechste y koordinate vom Gegner wird eingetragen
                                        if map2[Ey1][Ex[i]] != W and map2[Ey1][Ex[i]] != E:     #siehe oben
                                            map2[Ey[i]][Ex[i]] = X                              #
                                            map2[Ey1][Ex[i]] = E                                #
                                            movement = True                                     #
                                        
                                    if Ex[i] < px and movement == False:                        #Es wird Gegner x koordinate mit Spieler x koordinate verglichen. movement muss False sein
                                        Ex1 = Ex[i] + 1                                         #naechste x koordinate vom Gegner wird eingetragen
                                        if map2[Ey[i]][Ex1] != W and map2[Ey[i]][Ex1] != E:     #siehe oben
                                            map2[Ey[i]][Ex[i]] = X                              #
                                            map2[Ey[i]][Ex1] = E                                #
                                            movement = True                                     #
                                
                                            
                                
                                    if px == Ex1 and py == Ey[i] or px == Ex[i] and py == Ey1:  #Sollte die neue Position mit der des Spieler uebereinstimmen:
                                        map2 = nextmap(mc)                                      #wird map2 nochmal zurueckgesetzt
                                
                                return map2
                                
                            def poscheck(map2):                             #       
                                for row in range(len(map2)):                #Schleife geht durch map2
                                    for column in range(len(map2[row])):    #
                                        if map2[row][column] == P:          #wenn row, column ein Spieler (P) sein
                                            return column, row              #werden die koordinaten Column (x) und row (y) ausgegeben


                            def up(map2,mc):                        #Bewegung nach oben
                                x,y = poscheck(map2)                #x,y koordinaten werden ausgegeben
                                y1 = y - 1                          #naechste y koordinate wird eingetragen
                                if map2[y1][x] == X:                #sollte auf der naechsten koordinate Boden (X) sein:
                                    map2[y][x] = X                  #aktuelle position vom Spieler (P) wird as Boden (X) eingetragen
                                    map2[y1][x] = P                 #neue position wird als Spieler (P) eingetragen
                                map2 = Enemy_movement(map2,mc)      #Gegner sollen sich bewegen und auf der map2 eingetragen werden
                                

                                if map2[y1][x] == G:        #Sollte die Spieler Koordinate mit der koordinate des Zieles (Z) uebereinstimmen:
                                    mc = mc + 1             #wird der mapcounter (mc) um 1 erhoeht
                                    map2 = nextmap(mc)      #map2 wird auf die naechste map aktualisiert
                                return map2,mc              #

                            def down(map2,mc):                      #Siehe Zeile:166-172
                                x,y = poscheck(map2)                #
                                y1 = y + 1                          #
                                if map2[y1][x] == X:                #
                                    map2[y][x] = X                  #
                                    map2[y1][x] = P                 #
                                map2 = Enemy_movement(map2,mc)      #


                                if map2[y1][x] == G:        #Siehe Zeile:175-178
                                    mc = mc + 1             #
                                    map2 = nextmap(mc)      #
                                return map2,mc              #

                            def left(map2,mc):                      #Siehe Zeile:166-172
                                x,y = poscheck(map2)                #
                                x1 = x - 1                          #
                                if map2[y][x1] == X:                #
                                    map2[y][x] = X                  #
                                    map2[y][x1] = P                 #
                                map2 = Enemy_movement(map2,mc)      #
                                
                                if map2[y][x1] == G:        #Siehe Zeile:175-178
                                    mc = mc + 1             #
                                    map2 = nextmap(mc)      #
                                return map2,mc              #

                            def right(map2,mc):                     #Siehe Zeile:166-172
                                x,y = poscheck(map2)                #
                                x1 = x + 1                          #
                                if map2[y][x1] == X:                #
                                    map2[y][x] = X                  #
                                    map2[y][x1] = P                 #
                                map2 = Enemy_movement(map2,mc)      #
                                
                                

                                if map2[y][x1] == G:        #Siehe Zeile:175-178
                                    mc = mc + 1             #
                                    map2 = nextmap(mc)      #
                                return map2,mc              #

                            def update(map2,cs,kc,mc):              #
                                clear_command = b"\x1b[2J\x1b[H"    #Erstellung einer Escape-Sequence
                                cs.sendall(clear_command)           #Sowie das ausfueren der Escape-Sequence
                           
                                for row in map2:                                                                #Schleife geht durch map2
                                    map3 = ' '.join(map(str, row))                                              #map3 bekommt alle Elemente von row (map2) und traegt diese als ein string ein
                                    cs.send(map3.encode('utf-8') + b'\r\n')                                     #Alle Zeilen von map3 werden nach und nach ausgegeben
                                cs.send("bewegungen: ".encode('utf-8') + str(kc).encode('utf-8')+ b'\r\n')      #Danach werden die Anzahl von Bewegungen, wie auch bei welchem Level man ist angezeigt
                                cs.send("Level: ".encode('utf-8') + str(mc).encode('utf-8')+ b'\r\n')           #

                            kcounter = 0    #Anzahl von Key inputs                        

                            update(map2,cs,kcounter,mapcounter)     #Spiel wird geupdated
                            update(map2,cs,kcounter,mapcounter)     #Zwei mal, um alle Farben richtig Darzustellen

                            while True:                             #
                                keyinput = cs.recv(1024)            #Empfaengt die Inputs vom Nutzer 
                                key = keyinput.decode('utf-8')      #und uebertraegt diese in utf-8
                                
                                if key == "w":                                  #Wenn die taste w gedrueckt wird:
                                    kcounter = kcounter + 1                     #wird der kcounter hochgezaehlt
                                    map2,mapcounter = up(map2,mapcounter)       #die Funktion up() wird aufgerufen
                                    update(map2,cs,kcounter,mapcounter)         #das spiel wird aktualisiert
                                    
                                if key == "s":                                  #Wenn die taste s gedrueckt wird:  
                                    kcounter = kcounter + 1                     #siehe oben       
                                    map2,mapcounter = down(map2,mapcounter)     #die Funktion down() wird aufgerufen
                                    update(map2,cs,kcounter,mapcounter)         #

                                if key == "a":                                  #Wenn die taste a gedrueckt wird:
                                    kcounter = kcounter + 1                     #siehe oben  
                                    map2,mapcounter = left(map2,mapcounter)     #die Funktion left() wird aufgerufen
                                    update(map2,cs,kcounter,mapcounter)         #

                                if key == "d":                                  #Wenn die taste d gedrueckt wird:
                                    kcounter = kcounter + 1                     #siehe oben  
                                    map2,mapcounter = right(map2,mapcounter)    #die Funktion right() wird aufgerufen
                                    update(map2,cs,kcounter,mapcounter)         #           

                                if key == '\x1b':   #Wenn die Escape taste gedrueckt wird:
                                    start(cs)       #wird das Menue angezeigt
                                    
                    
                        game(client_socket)


                    def credits(cs):                                            #
                        Credits = "Erstellt von Martin Dokters"                 #Elemente die Angezeigt werden sollen werden deklariert
                        back = "druecke ESC um zurueck zu gehen"                #

                        clear_command = b"\x1b[2J\x1b[H"                        #Erstellung einer Escape-Sequence
                        client_socket.send(clear_command)                       #Sowie das ausfueren der Escape-Sequence

                        client_socket.send(Credits.encode('utf-8') + b'\r\n')   #Zeigt die Elemente Credits und back an 
                        client_socket.send(back.encode('utf-8') + b'\r\n')      #

                        while True:                             #
                            data = client_socket.recv(1024)     #empfaengt Inputs vom Nutzer
                            key = data.decode('utf-8')          #uebertraegt diese zu utf-8

                            if key == '\x1b':                   #wenn die Taste Escape gedrueckt wird
                                start(cs)                       #wird das Menue wieder angezeigt
                            

                    if response == "2":             #Wenn Taste 2 gedrueckt wird werden die Credits gestartet
                        credits(client_socket)      #

                        
                    if response == "3":             #Wenn Taste 3 gedrueckt wird die Verbindung geschlossen
                        client_socket.close()       #
        


            finally:                                                    #
                print(f"Connection with {client_address} closed.")      #gibt aus welcher Nutzer die Verbindung schliesst
                client_socket.close()                                   #Verbindung wird geschlossen
 
        start(client_socket)

bbs_server(bbs_host,bbs_port)