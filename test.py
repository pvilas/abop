"""
DOL-system
Es el modelo más sencillo. Deterministic and context-free. Existe un conjunto de letras  {𝑎,𝑏}  que forman unas palabras words. Cada letra tiene asociada una regla de reescritura. Por ejemplo:
𝑎→𝑎𝑏 
𝑏→𝑎 

Se parte de un axioma, p.e.  𝑏  y, en cada derivación, se va reescribiendo simultáneamente toda la palabra según las reglas de reescritura.

𝑏→𝑎→𝑎𝑏→𝑎𝑏𝑎→𝑎𝑏𝑎𝑎𝑏→𝑎𝑏𝑎𝑏𝑎𝑏𝑎 

Por ejemplo, el desarrollo filamentoso de Anabaena catenula es, siendo  𝑙  y  𝑟  la polaridad, es decir las posiciones en donde las células hijas de tipo  𝑎  o  𝑏  serán producidas. El desarrollo está descrito por el siguiente L-system:

𝜔:𝑎𝑟𝑝1:𝑎𝑟→𝑎𝑙𝑏𝑟𝑝2:𝑎𝑙→𝑏𝑙𝑎𝑟𝑝3:𝑏𝑟→𝑎𝑟𝑝4:𝑏𝑙→𝑎𝑙 

Empezando por la primera célula, el axioma  𝑎𝑟 , produce:

𝑎𝑟→𝑎𝑙𝑏𝑟→𝑏𝑙𝑎𝑟𝑎𝑟→...

"""

import numpy as np
import simpleaudio as sa

def DOL(letras, axioma, reglas, derivaciones, pasada=0):
    """devuelve el L-system de tipo DOL después de d derivaciones"""

    # fin de la recursión
    if pasada==derivaciones:
        print(f'retornando {axioma}')
        return(axioma)
  
    print(f"pasada {pasada} de {derivaciones}")
    estado_inicial=axioma # partimos del axioma
    estado_final='' # el estado final está inicialmente vacío
    for a in range(0,len(estado_inicial)):
        # aplicamos las reglas de reescritura a todos los miembros 
        # del conjunto simultáneamente
        # primero buscamos posición de la letra en la lista
        p=letras.index(estado_inicial[a])
        # añadimos la reescritura de la letra
        estado_final+=reglas[p][1]

    print(f"estado {estado_final}")
    pasada+=1
    # recursión, pasamos estado_final como axioma
    DOL(letras, estado_final, reglas, derivaciones, pasada)


def tocala2():

    # calculate note frequencies
    A_freq = 440
    Csh_freq = A_freq * 2 ** (4 / 12)
    E_freq = A_freq * 2 ** (7 / 12)

    # get timesteps for each sample, T is note duration in seconds
    sample_rate = 44100
    T = 0.25
    t = np.linspace(0, T, T * sample_rate, False)

    # generate sine wave notes
    A_note = np.sin(A_freq * t * 2 * np.pi)
    Csh_note = np.sin(Csh_freq * t * 2 * np.pi)
    E_note = np.sin(E_freq * t * 2 * np.pi)

    # concatenate notes
    audio = np.hstack((A_note, Csh_note, E_note))
    # normalize to 16-bit range
    audio *= 32767 / np.max(np.abs(audio))
    # convert to 16-bit data
    audio = audio.astype(np.int16)

    # start playback
    play_obj = sa.play_buffer(audio, 1, 2, sample_rate)

    # wait for playback to finish before exiting
    play_obj.wait_done()    



def tocala():
    frequency = 440  # Our played note will be 440 Hz
    fs = 44100  # 44100 samples per second
    seconds = 3  # Note duration of 3 seconds

    # Generate array with seconds*sample_rate steps, ranging between 0 and seconds
    t = np.linspace(0, seconds, seconds * fs, False)

    # Generate a 440 Hz sine wave
    note = np.sin(frequency * t * 2 * np.pi )

    # Ensure that highest value is in 16-bit range
    audio = note * (2**15 - 1) / np.max(np.abs(note))
    # Convert to 16-bit data
    audio = audio.astype(np.int16)

    # Start playback
    play_obj = sa.play_buffer(audio, 1, 2, fs)

    # Wait for playback to finish before exiting
    play_obj.wait_done()




print(f"El resultado es",
    DOL(
        letras=('a','b'), 
        axioma='b', 
        reglas=( ('a', 'ab'), ('b', 'a') ), 
        derivaciones=5
    )
)

tocala2()