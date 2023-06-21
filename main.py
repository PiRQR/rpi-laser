#!/usr/bin/env python3                          
import signal                   
import sys
import json
import time
import os 
import RPi.GPIO as GPIO

absolute_path = os.path.dirname(__file__)
sequ_file_path = os.path.join(absolute_path, "sequences", "sequences.json")
        


# déclaration des GPIO
BUTTON_GPIO1 = 3
BUTTON_GPIO2 = 4
LED_GPIO = 17

# déclaration variables
sequence = 0
liste_sequences = {}
nb_sequences = 0

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def led(etat):
    if etat:
        GPIO.output(LED_GPIO, True)
    else:
        GPIO.output(LED_GPIO, False)
    

def button_callback(btn_nb):
    '''
        callback appelée lors de l'appuie sur le btn 1
    '''
    global sequence
    global nb_sequences
    
    if btn_nb==1:
        if(sequence < nb_sequences):
            sequence += 1
        else:
            sequence = 1
        print(f"séquence changée: {sequence}")
    else:
        sequence = 0
        print(f"arrêt !")

def exec_sequence(sequ):
    index = 0
    taille_sequ = len(sequ)
    if taille_sequ%2:
        print("error: la sequence n'est pas valide")
        return False
    while(index<taille_sequ):
        led(sequ[index])
        index+=1
        time.sleep(sequ[index])
        index+=1
    return True

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    # define bouton 1 input
    GPIO.setup(BUTTON_GPIO1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # define bouton 2 input
    GPIO.setup(BUTTON_GPIO2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # define led
    GPIO.setup(LED_GPIO, GPIO.OUT)
    # déclaration de l'interruption sur la gpio des boutons
    GPIO.add_event_detect(BUTTON_GPIO1, GPIO.FALLING, callback=lambda x: button_callback(1), bouncetime=200)
    GPIO.add_event_detect(BUTTON_GPIO2, GPIO.FALLING, callback=lambda x: button_callback(2), bouncetime=200)
    # CTRL+C => sortir du code
    signal.signal(signal.SIGINT, signal_handler)
    
    with open(sequ_file_path, 'r') as f:
        liste_sequences = json.load(f).get("sequences")
    nb_sequences = len(liste_sequences)
    print(f"nombre de sequences detectées: {nb_sequences}")
    # boucle principale
    while(1):
        for sequ in liste_sequences:
            if sequence==int(sequ):
                exec_sequence(liste_sequences[sequ])
    
    signal.pause()    
        
    
    
    
    