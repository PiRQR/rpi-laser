#!/usr/bin/env python3                          
import signal                   
import sys
import json
import time
import os 

absolute_path = os.path.dirname(__file__)
sequ_file_path = os.path.join(absolute_path, "sequences", "sequences.json")
    
# déclaration des GPIO
BUTTON_GPIO1 =  3
BUTTON_GPIO2 =  4
LED_GPIO =      17
OUT_GPIO2 =      17
OUT_GPIO3 =      17
OUT_GPIO4 =      17
    
# mappage gpio out du json avec gpio du code
gpio_map = {"gpio1":LED_GPIO, "gpio2":OUT_GPIO2, "gpio3":OUT_GPIO3, "gpio4":OUT_GPIO4}

# déclaration variables
sequence =          0
liste_sequences =   {}
nb_sequences =      0
toggle =            0
threads_term_nb = len(gpio_map) # pour savoir lorsque touts les threads sont terminés

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def set_all_gpio(val: bool):
    '''
        mettre toutes les gpio au même état, val=True ou val=False
    '''
    for gpio in gpio_map:
        GPIO.output(gpio_map[gpio], val)    

def button_callback(btn_nb):
    '''
        callback appelée lors de l'appuie sur le btn 1
    '''
    global sequence
    global nb_sequences
    
    if btn_nb==1: # si btn 1 appuyé
        if(sequence < nb_sequences):
            sequence += 1
        else:
            sequence = 1
        print(f"séquence changée: {sequence}")
        
    elif btn_nb==2: # si btn 2 appuyé
        toggle != toggle
        #sequence = 0
        print(f"arrêt !")

def sequence_gpio(sequ: list, gpio: int):
    index = 0
    ret = False
    global threads_term_nb
    taille_sequ = len(sequ)
    
    if taille_sequ%2:
        print("error: la sequence n'est pas valide")
    else:
        while(index<taille_sequ):
            if toggle:
                GPIO.output(gpio, sequ[index])
                index+=1
                time.sleep(sequ[index])
                index+=1
            else:
                GPIO.output(gpio, False)
        ret = True
    
    threads_term_nb+1 # un thread est terminé, on incrémente
    return ret

def exec_sequences(gpio_list: list):
    '''
        gpio_list: (liste des gpio contenant les sequences (ex: "gpio1":[0,0]))
    '''
    index = 0
    for gpio in gpio_map:
        threading.Thread(target=sequence_gpio, args=(gpio_list.get(gpio), gpio_map[gpio])).start()
        
if __name__ == '__main__':
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    # define bouton 1 input
    GPIO.setup(BUTTON_GPIO1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # define bouton 2 input
    GPIO.setup(BUTTON_GPIO2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # define des gpio du gpio map en out
    for gpio_out in gpio_map:
        GPIO.setup(gpio_out, GPIO.OUT)
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
        if threads_term_nb==len(gpio_map):
            threads_term_nb=0 # on remet à zéro le cpt de threads terminés
            exec_sequences(gpiolist)
        if not toggle:
            set_all_gpio(False) # mettre toutes les gpio à zéro
    
    signal.pause()    
        
    
    
    
    