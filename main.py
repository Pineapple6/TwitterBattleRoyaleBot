'''
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
'''
#-----------------------------------------------------------------------

# Rellenar esto con las claves de acceso ÚNICAS DE TU BOT
API_KEY = ''
API_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

SEED = None # Dejar en None para que sea totalmente aleatorio
DELAY = 500 # Tiempo (en segundos) entre cada tweet

#-----------------------------------------------------------------------

from random import choice, seed
from time import sleep 
import tweepy # Uso de la API de Twitter
from graphic import make_a_list

with open('custom/PEOPLE.txt', 'r') as f:
    names = f.readlines()
    names = [i.rstrip('\n') for i in names] # Crea una lista de los participantes manejable por Python a partir del documento de texto
    f.close()

with open('custom/PHRASES.txt', 'r') as f:
    phrases = f.readlines()
    phrases = [i.rstrip('\n') for i in phrases]# Lo mismo para las frases
    f.close()

# Se crea el objeto people, que contiene a todos los participantes junto a
# su estado (vivos o muertos) y su número de bajas
people = {}
for i in names:
    people[i] = {
        'live':True,
        'kills':0
    }

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)# Autentificación
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)# Acceso

api = tweepy.API(auth)# Si todo esto va bien, no debería haber ningún error a la hora de usar la API para publicar tweets.

if SEED != None: 
    seed(SEED)# Si la seed es una personalizada, el "elegidor aleatorio" se alimentará de esa seed.

def max_kills(dict):
    '''
    Devuelve el o los concursantes con mayor numero de bajas
    '''
    p_max = []# lista de jugadores con mas bajas
    maximum = 0
    for key in dict:
        if maximum < dict[key]['kills']:
            maximum = dict[key]['kills']
            p_max = [key]
        elif maximum == dict[key]['kills']:
            p_max.append(key)
    return p_max # Devuelve un array con el jugador con más bajas, o con los jugadores con mas bajas en caso de haber empate.

while True:
    message = '' # Mensaje que se enviará como tweet

    # Primero, se elige a una víctima y se elimina del grupo de participantes
    victim = choice(names)
    people[victim]['live'] = False # al no estar ya viva, su estado en el objeto 'people' es de muerta.
    names.remove(victim)

    # Tras ello, se elige a un atacante
    attacker = choice(names)
    people[attacker]['kills'] += 1 # Al ser este el asesino, su numero de bajas aumenta por uno. 

    # Se crea el mensaje que lo comunica...
    message += attacker + choice(phrases) + victim
    
    if len(names) == 1:# Si ya solo queda uno
        message += '\n{} ha ganado el Battle Royale'.format(names[0])# Esa persona gana (se comunica su victoria)
        
        # Junto a quién ha ganado el battle royale, se comunica también quienes son los que han tenido el
        # mayor número de bajas.
        if len(max_kills(people)) > 1:
            verb = 'han'
        else:
            verb = 'ha'
        message += '\n{0} {1} tenido el mayor numero de bajas, con un total de {2} asesinatos.'.format(' y '.join(max_kills(people)), verb, people[max_kills(people)[0]]['kills'])
        print(message)
        make_a_list(people, 'media/lasting.png')# Se hace una lista actualizada de los concursantes (ver graphics.py)
        sleep(5)# Se espera 5 segundos (tiempo de sobra para que la imagen se actualize)
        while True:
            try:
                api.update_with_media('media/lasting.png', status=message)# Se envía el nuevo tweet junto a la imagen de lista actualizada.
                break
            except:
                print('Error al enviar el tweet.')
                sleep(120)
        break # Se acaba el juego
    else:# Si, en cambio, queda suficiente gente para seguir jugando
        message += '\nQuedan {} participantes vivos'.format(len(names))# Se añade al mensaje el numero de participantes restantes
        print(message)
        make_a_list(people, 'media/lasting.png')# Se hace una lista actualizada de los concursantes (ver graphics.py)
        sleep(5)# Se espera 5 segundos (tiempo de sobra para que la imagen se actualize)
        while True:
            try:
                api.update_with_media('media/lasting.png', status=message)# Se envía el nuevo tweet junto a la imagen de lista actualizada.
                break
            except:
                print('Error al enviar el tweet')
                sleep(120)

    # Tras esto, se espera el tiempo establecido hasta el siguiente Tweet.
    sleep(DELAY)
