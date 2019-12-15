"""
DOL-system

"""

import numpy as np
import simpleaudio as sa

# audio sample rate
SAMPLE_RATE = 44100
# initial duration of a note (the duration of the note of the axiom)
INITIAL_NOTE_DURATION = 0.25
# duration accelaration ramp between generations (set to 1 if constant)
ACC_RAMP = 1.05

"""
class DOL(object):
    def __init__(self, letters, axiom, rules, derivations):
        self.letters=letters
        self.axiom=axiom
        self.rules=rules
        self.derivation=derivations
"""



def DOL(letras, axioma, reglas, derivaciones):
    """
    Return the DOL after d derivations

    Parameters
    ----------
    letters : tuple of char
        the letters of the dol
    axiom : string
        the axiom of the system 
    reglas : tuple list
        rewritre rules
    derivaciones : int
        the number of derivations (generations)

    Returns
    -------
    tuple string
        (evolution, last_state)    
        evolution is the aggregation of all states, from the axiom 
        until the last_state. 
        evolution append a '/' between each generation
    """

    evolucion=''
    estado=axioma # start form the axiom
    for pasada in range(0, derivaciones):                  
        new_estate=''
        for a in range(0,len(estado)):
            # apply rules simultaneously
            # first lookup position of the letter
            p=letras.index(estado[a])
            # apply rewrite rule of the letter
            new_estate+=reglas[p][1]
        estado=new_estate
        evolucion+=estado+'/'
        print(f"pasada {pasada} de {derivaciones}: {estado}")
        
    return(evolucion, estado)

def word_to_notes(letters, lsystem, mapping):
    """
    Take the word and create an array of notes

    Parameters
    ----------
    letters : tuple of char
        the letters of the dol
    lsystem : string
        string of letters 
    mapping : tuple list
        mapping betwwen the letters and the notes

    Returns
    -------
    16-bit np array
        the concatenation of the notes
    """
    duration = INITIAL_NOTE_DURATION
    song=[]
    # for each letter
    for l in lsystem:
        if l!='/': # change of generation
            # append the note
            # letters.index(l) is the position of letter l in the aray of lettes
            # thus, mapping[]
            letter_position = letters.index(l) # position of the letter
            letter_freq = mapping[letter_position][1] # frequency of the letter
            nt = note(letter_freq, duration)
            song.append(nt)
        else:
            # we accelerate the note duration of the next generation
            duration = duration / ACC_RAMP
    # create audio sequence
    audio = np.hstack(song)
    # normalize to 16-bit range
    audio *= 32767 / np.max(np.abs(audio))
    # convert to 16-bit data
    audio = audio.astype(np.int16)
    return(audio)

def tocala(audio):
    """
    Plays the audio
    
    Parameters
    ----------
    audio : np array of 16-bits
        the audio sequence 

    Returns
    -------
    None
    """    
    # start playback    
    play_obj = sa.play_buffer(
        audio_data = audio, 
        num_channels = 1, 
        bytes_per_sample = 2, 
        sample_rate = SAMPLE_RATE
        )

    # wait for playback to finish before exiting
    play_obj.wait_done()    



def note(frequency=440, duration=.25):
    """      
    Creates a note

    Parameters
    ----------
    frequency : int
        Freq in Hz
    duration : int
        duration in seconds

    Returns
    -------
    16-bit np array
        The the array with the note
    """    
    T = duration
    t = np.linspace(0, T, T * SAMPLE_RATE, False)

    # generate sine wave notes
    note = np.sin(frequency * t * 2 * np.pi)

    return(note)


# frequencies
A_freq = 440
Csh_freq = A_freq * 2 ** (4 / 12)
E_freq = A_freq * 2 ** (7 / 12)
D_freq = A_freq * 2 ** (10 / 12)


# Anabaena catenula
# a=a_r b=a_l c=b_r d=b_l
letters=('a','b','c','d')
axiom='b'
rules=( ('a', 'bc'), ('b', 'da'), ('c', 'a'), ('d', 'b') ) 
derivations=6
mapping = (
            ('a', A_freq),
            ('b', Csh_freq),
            ('c', E_freq),
            ('d', D_freq)
        )

# calculate the DOL-system
dol=DOL(
        letras=letters, 
        axioma=axiom, 
        reglas=rules, 
        derivaciones=derivations
    )

print(f"The L-system is {dol}")
# map letters to notes
audio=word_to_notes(    
    letters=letters,
    lsystem=dol[0],
    mapping= mapping
)
# play audio
tocala(audio)
