# abop
Experiments on L-systems and sounds. Based on the Algorithmic Beauty of Plants.

## Introducción
Estaba leyendo el fantástico libro, 

> Przemyslaw Prusinkiewicz y Aristid Lindenmayer. **The Algorithmic Beauty of Plants**. Electronic Edition 2004 Przemyslaw Prusinkiewicz.

y viendo cómo se podía representar el crecimiento de sistemas biológicos mediante una cuantas reglas lógicas me pregunté cómo sería *oir* el crecimiento de dichos sistemas. Es decir, mapear las letras del L-system a sonidos para oir su crecimiento. El enfoque tradicional ha sido, como es normal, gráfico, ya que se han utilizado los L-systems para modelizar el crecimiento de las ramas de los vegetales. 

Como era de esperar, muchos han *sonificado* estos sistemas de formas muy originales para crar arte.

Vaya por delante que no tengo ni idea de música y que estas son mis pruebas preliminares. Cuando tenga tiempo, me leeré el artículo que acompaña a la librería [music](https://pypi.org/project/music/) que parece muy interesante y que explica cómo generar notas. De momento, las *notas* son senoides a frecuencias determinadas.

En cuanto a la implementación (hecha en un par de horas) tampoco es que me haya matado para sacar los algoritmos más eficientes. De hecho, el crecimiento se guarda en un simple string que se va ampliando. He primado la claridad a la eficiencia.


## DOL-system

Es el modelo de L-system más sencillo. Es determinístico y sin contexto. Existe un conjunto de letras $\{a, b\}$ que forman unas palabras *words*.

Cada letra tiene asociada una **regla de reescritura**. Por ejemplo:
$$
a \to ab \\
b \to a
$$

Se parte de un axioma, p.e. $b$ y, en cada derivación o generación, se va reescribiendo **simultáneamente** toda la palabra según las reglas de reescritura.

$$b \to a \to ab  \to aba  \to abaab  \to abababa$$

Por ejemplo, el desarrollo filamentoso de la cianobacteria [Anabaena catenula](https://es.wikipedia.org/wiki/Anabaena) se rige por un conjunto de cuatro reglas. $l$ y $r$ se refieren la polaridad, es decir las posiciones en donde las células hijas de tipo $a$ o $b$ serán producidas. El desarrollo del organismo está descrito por el siguiente L-system:

$$ \begin{matrix}
\omega: a_r \\
p_1: a_r \to a_l b_r \\
p_2: a_l \to b_l a_r \\
p_3: b_r \to a_r \\
p_4: b_l \to a_l
\end{matrix}$$

Empezando por la primera célula, el axioma $a_r$, produce:

$$a_r \to a_l b_r \to b_l a_r a_r \to ...$$

Si mapeamos $\{a_r, a_l, b_r, b_l\}$ a $\{a, b, c, d\}$, la evolución sería:

$$a/da/bbc/dadaa/bbcbbcbc/dadaadadaadaa/bbcbbcbcbbcbbcbcbbcbc/...$$

Ver el vídeo de la sonificación de [Raven Kwok](http://ravenkwok.com/1b5f1/) de este tema.

## Implementación

A la espera de crear una clase para empaquetar todos los componentes, el flujo sería el siguiente:

### Definir las frecuencias de las notas
A_freq = 440
Csh_freq = A_freq * 2 ** (4 / 12)
E_freq = A_freq * 2 ** (7 / 12)
D_freq = A_freq * 2 ** (10 / 12)


### Definir el DOL

Las letras del sistema (a=a_r b=a_l c=b_r d=b_l)

```
letters=('a','b','c','d') 
```

El axioma es el núcleo desde donde se inicia el crecimiento

```
axiom='b'
```

Las reglas de reescritura 
```
rules=( ('a', 'bc'), ('b', 'da'), ('c', 'a'), ('d', 'b') ) 
```
El número de generaciones que deseamos crear
```
derivations=6
```
El mapeo de letras en frecuencias
```
mapping = (
            ('a', A_freq),
            ('b', Csh_freq),
            ('c', E_freq),
            ('d', D_freq)
        )
````

### Calcular el DOL
```
dol=DOL(
        letras=letters, 
        axioma=axiom, 
        reglas=rules, 
        derivaciones=derivations
    )
print(f"The L-system is {dol}")
````

### Mapear las letras en notas
```
audio=word_to_notes(    
    letters=letters,
    lsystem=dol[0],
    mapping= mapping
)
````

### Oir el resultado
```
tocala(audio)
```

### Modificar paràmetros de reproducción
Si el resultado no nos convence, podemos modificar la duración de las notas en función de la generación. La idea es que el sonido de las generaciones más jóvenes (cadenas más largas) tenga notas más cortas para representar que son más *jovenes*. Esto lo hacemos con dos constantes. ```INITIAL_NOTE_DURATION``` controla la duración de las notas de la primera generación y ```ACC_RAMP``` controla la aceleración entre generaciones.

```
# initial duration of a note (the duration of the note of the axiom)
INITIAL_NOTE_DURATION = 0.25
# duration accelaration ramp between generations (set to 1 if constant)
ACC_RAMP = 1.05
```

Lo divertido es ir modificando todos estos parámetros, sobre todo las reglas, y *oir* cómo evoluciona el *organismo*.

## Bibliografía

Wikipedia ([es](https://es.wikipedia.org/wiki/Sistema-L), [en](https://en.wikipedia.org/wiki/L-system)) tiene un montón de información sobre el tema y fantásticos links.
