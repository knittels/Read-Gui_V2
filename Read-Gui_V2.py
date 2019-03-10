import tkinter
import time
import _thread

#------------------------------------

def eingabe():
    # Modul zur Eingabe der Messparameter
    # Wie lange und mit welchem Intervall soll die Messung laufen

    Dauer = eingabe_1.get()
    Dauer = float(Dauer)
    Dauer = int(Dauer)
    Intervall = eingabe_2.get()
    Intervall = float(Intervall)
    Intervall = int(Intervall)
    Datafile = eingabe_3.get()
    Datafile = Datafile + ".csv"
    Dauer_sec = Dauer * 3600
    Intervall_sec = Intervall * 60
    return Dauer_sec, Intervall_sec, Datafile

# -----------------------------------------

def read_mw(threadName, Dauer, delay, File):
    global Tges
    import sys, urllib.request
    import time

    # Datum bestimmen
    Datum = time.strftime("%a, %d %b %Y")

    # Datum und Kopf zum Start ind csv-Datei schreiben
    #d = oeffnen(DF, "w")
    #d.write(Datum + ";" + "Temperatur" + ";" + "rel.Feuchte" + "\n")
    #d.close()

    ausgabe_1.config(fg="blue")
    ausgabe_1["text"] = "Messung läuft"

    # Verbindung zum Sensor...
    try:
        u = urllib.request.urlopen("http://sensor1:8080")
    except:
        print("Fehler: Sensor nicht online")
        sys.exit(0)
    # ... und in eine Liste einlesen
    li = u.readlines()
    # ... und wieder schließen
    u.close()

    # Ausgabe der Werte
    for Wert in li:
        # Poistion von Temp- und Feuchtewerte finden
        Wert_str = str(Wert).replace(".", ",")
        Pos1 = Wert_str.find("temp")
        # print (Pos1)
        Pos2 = Wert_str.find("rel")
        # print (Pos2)
        Zeit = (time.strftime("%H:%M:%S"))
        Temp = Wert_str[Pos1 + 6:Pos1 + 11]
        Feuchte = Wert_str[Pos2 + 5:Pos2 + 8]
        # und Ausgabe am Bilschirm
        print("Zeit: ", Zeit, "Temperatur: ", Temp, "°C", "Luftfeuchte:", Feuchte, "% rel.")
        Nachricht = "Zeit: " + Zeit + "   Temperatur: " + Temp + " °C" + "   Luftfeuchte: " + Feuchte + " % rel."
        # und Ausgabe als CSV-Datei
        # Zugriff auf Ausgabe-Datei
        d = oeffnen(DF, "a")
        # schreiben in Datei als csv
        d.write(Zeit + ";" + Temp + ";" + Feuchte + "\n")
        # und schließen
        d.close()
    # Ausgabe der Messwerte im Fenster vorbereiten
    # anhängig vom Wert -> verschiedene Farben
    #ausgabe_uhr.after(1000)
    ausgabe_uhr.config(fg="blue")
    ausgabe_uhr["text"] = Zeit + " Uhr"
    if int(Temp[0:3]) < 20:
        ausgabe_temp.config(fg="blue")
    else:
        if int(Temp[0:3]) > 25:
            ausgabe_temp.config(fg="red")
        else:
            ausgabe_temp.config(fg="green")
    ausgabe_temp["text"] = Temp + " °C"
    if int(Feuchte) < 35:
        ausgabe_feuchte.config(fg="red")
    else:
        ausgabe_feuchte.config(fg="green")
    ausgabe_feuchte["text"] = Feuchte + " % rel."
    # abgeöaufene Zeit aufsummieren
    Tges = Tges + delay
    time.sleep(delay)
    print (Tges)
    # Messung so lange wiederholen bis die Zeit abgelaufen ist
    if Tges < Ds:
        messung()

# ----------------------------------------

def start():
    global Ds, Is, DF, Tges
    # Wenn bereits eine Messung läuft, kann keine neue gestartet werden
    try:
        if Tges > 0:
            ausgabe_1.config(fg="red")
            ausgabe_1["text"] = "Messung läuft bereits"
            return
     # Wenn keine Messung läuft, wird eine gestartet
    except:
        Tges = 0
        (Ds, Is, DF) = eingabe()
        kopf_schreiben()
        messung ()

#------------------------------------------

def oeffnen(Datei,Modus):
    # Modul zum öffnen der Datei
    try:
        d = open(Datei, Modus)
    except:
        print("Datei nicht gefunden")
        sys.exit(0)
    return (d)
#-----------------------------------------

def kopf_schreiben():
    # Datum bestimmen
    Datum = time.strftime("%a, %d %b %Y")

    # Datum und Kopf zum Start ind csv-Datei schreiben
    d = oeffnen(DF, "w")
    d.write(Datum + ";" + "Temperatur" + ";" + "rel.Feuchte" + "\n")
    d.close()

#-----------------------------------------

def messung():
    _thread.start_new_thread(read_mw, ("thread_1", Ds, Is, DF))

#----------------------------------------

def stop():
    fenster.destroy()

#----------------------------------------

def main():
    while True:
        fenster.update_idletasks()
        fenster.update()





# Fenster

fenster = tkinter.Tk()
fenster.title("Sensor auslesen")

intext_1 = tkinter.Label (fenster, text = "Messdauer:")
intext_1.grid(row=0, column=0, pady=10)

intext_2 = tkinter.Label (fenster, text = "Intervall:")
intext_2.grid(row=1, column=0, padx=20, pady=10)

intext_3 = tkinter.Label(fenster, text = "Fileame:")
intext_3.grid(row=2, column=0, padx=20, pady=10)

eingabe_1 = tkinter.Entry(fenster)
eingabe_1.grid(row=0, column=1, padx=10, pady=10)

eingabe_2 = tkinter.Entry(fenster)
eingabe_2.grid(row=1, column=1, padx=10, pady=10)

eingabe_3 = tkinter.Entry(fenster)
eingabe_3.grid(row=2, column=1, padx=10, pady=10)

los = tkinter.Button(fenster, text = "Start", command= start)
los.grid(row=3, column=0, padx=50, pady=20 )



ausgabe = tkinter.Label(fenster, text = "aktuelle Messwerte:")
ausgabe.grid(row=4, column=1, padx=10, pady=10)

ausgabe_1 = tkinter.Label(fenster, text = " ")
ausgabe_1.grid(row=4, padx=10, pady=10)

ausgabe_u = tkinter.Label(fenster, text = "Uhrzeit:")
ausgabe_u.grid(row=5, column=0, padx=10, pady=5)

ausgabe_uhr = tkinter.Label(fenster, text = "0")
ausgabe_uhr.grid(row=5, column=1, padx=10, pady=5)

ausgabe_t = tkinter.Label(fenster, text = "Temperatur:")
ausgabe_t.grid(row=6, column=0, padx=10, pady=5)

ausgabe_temp = tkinter.Label(fenster, text = "0")
ausgabe_temp.grid(row=6, column=1, padx=10, pady=5)

ausgabe_f = tkinter.Label(fenster, text = "Luftfeuchtigkeit:")
ausgabe_f.grid(row=7, column=0, padx=10, pady=5)

ausgabe_feuchte = tkinter.Label(fenster, text = "0")
ausgabe_feuchte.grid(row=7, column=1, padx=10, pady=5)


ende = tkinter.Button(fenster, text = "Beenden", command= stop)
ende.grid(row=3, column=1, padx=50, pady=20 )

fenster.mainloop()


