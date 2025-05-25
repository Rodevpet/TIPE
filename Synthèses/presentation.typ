#import "@preview/polylux:0.4.0":*
#import "@preview/sns-polylux-template:0.1.0" as sns-theme: *
#import "@local/Macros:0.1.2":*
#show: thmrules.with(qed-symbol: $square$)
  //Pour afficher en dispaly everytime
#show math.equation.where(block: false): it => math.display(it)
#set quote(block: true)
#set text(lang: "fr")
#show: sns-theme.with(
  aspect-ratio    : "4-3",
  title           : text(size: 50pt)[Optimisation du traitement du signal sonore sous forme numérique],
  subtitle        : text(size: 20pt)[Où comment utiliser la transformée de Fourier pour créer un identifiant unique et reconnaître efficacement une musique],
  event           : [],
  short-title     : "TIPE 2025",
  short-event     : "",
  logo-2          : (""),
  logo-1          : (""),
  authors         : (
    {
      set text(top-edge: 0pt, bottom-edge: 0pt)
      grid(gutter: 2em, columns: (1fr, 1.2fr),
        align(right,[PETIT Robin]),
        align(left,[#link("MPI")])
      )
    },
  )
)
#title-slide()

#toc-slide()

#new-section-slide("Introduction")


#slide(
  title: "Les exigences croissantes"
)[
/* Notes
Tout d'abord je me suis interressé à la manière dont l'information pouvait transiter,
Grâce au Sniffer Proxyman, lorsque j'ai lancé une recherche de musique, j'ai pu intercepté les données qui transitait.
*/
#place(figure(
  image("Images/Exigence Croissantes Step 0.svg")
),left+horizon)
]

#slide(
  title: "Les exigences croissantes"
)[
/*Notes
En premier, j'ai pu constater que seul un fichier de 1,21kB était envoyé.
*/
#place(figure(
  image("Images/Exigence Croissantes Step 1.svg")
),left+horizon)
]
#slide(
  title:"Les exigences croissantes"
)[
/*Notes
Shazam semble alors prendre 120 ms à traité l'information.
*/
#place(figure(
    image("Images/Exigence Croissantes Step 2.svg")
  ),left+horizon)
]
#slide(
  title:"Les exigences croissantes"
)[
/*Notes
Puis renvoie l'information, comme le titre de la musique.
*/
#place(figure(
  image("Images/Exigence Croissantes Step 3.svg")
),left+horizon)
]
#slide(
  title:"Les exigences croissantes"
)[
/*Notes
Sachant que Shazam possède une base de donné répertoriant 40 millions de musique en 2016
*/
#place(figure(
  image("Images/Exigence Croissantes Step 4.svg")
),left+horizon)
]
#new-section-slide("Problématique")
#slide(
  title:"Problématique"
)[
  Comment identifier un morceau de musique complet de manière unique et efficace à partir d'un échantillon de celle-ci ?
]
#slide(
  title:"Modélisation du problème"
)[
/*Notes
Numériquement, le signal est discret, grâce à un outil d'acquisition on peut récupérer les données sous cette forme, avec $k$ étant analogue au temps et représentant la k-ème donné acquise.
x[k] revient à l'amplitude de la k-ème donné.
Enfin $T$ est la période d'acquisition, i.e. la période entre deux données acquises par l'appareil de mesure.
*/
  #place(figure(
  image("Images/Modelisation Probleme.svg")
),left+horizon)
  #place(left, dx:400pt, dy: -180pt)[
    - $k$ : $k$-ème donnée acquise numériquement\ depuis le début de l'acquisition.
    - $x[k]$ : Amplitude correspondante à la \ $k$-ème donné.
    - $T$ : Période d'acquisition
  ]
]
#new-section-slide("1ère Approche - La Fast Fourier Transform")
#slide(
  title:"L'algorithme de Cooley-Tukey",
  subtitle: "Principales caractéristiques"
)[]

#slide(
  title:"L'algorithme de Cooley-Tukey",
  subtitle: "Principales caractéristiques"
)[
  - Récursif
]
#slide(
  title:"L'algorithme de Cooley-Tukey",
  subtitle: "Principales caractéristiques"
)[
  - Récursif
  - Basé sur le paradigme "diviser pour régner"
]
#slide(
  title:"L'algorithme de Cooley-Tukey",
  subtitle: "Principales caractéristiques"
)[
  - Récursif
  - Basé sur le paradigme "diviser pour régner"
  - Complexité temporel en $O(N log(N))$ avec $N$ le nombre de point acquis.
]
#slide(
  title:"L'algorithme de Cooley-Tukey",
  subtitle: "Principales caractéristiques"
)[
  - Récursif
  - Basé sur le paradigme "diviser pour régner"
  - Complexité temporel en $O(N log(N))$ avec $N$ le nombre de point acquis.
  - *Entrée* : Un signal sous forme de décomposition de fourrier.
]
#slide(
  title:"L'algorithme de Cooley-Tukey",
  subtitle: "Principales caractéristiques"
)[
  - Récursif
  - Basé sur le paradigme "diviser pour régner"
  - Complexité temporel en $O(N log(N))$ avec $N$ le nombre de point acquis.
  - *Entrée* : Un signal sous forme de décomposition de fourrier.
  - *Sortie* : La liste des coefficients de fourrier.
]
#slide(
  title:"L'algorithme de Cooley-Tukey",
  subtitle: "Principe"
)[
Soit :
  - $N$ le nombre de points acquis.
  - $x : [|0,N-1|] -> RR$ l'application qui pour tout point $k in [|0,N-1|]$ acquis associe sont amplitude $x[k]$.
  - $X : cases(delim:#none,n mapsto X[n]=display(sum^(N-1)_(k=0)x[k]e^(-2pi i (k n)/N)),[|0,N-1|] -> RR)$ où $X[n]$ est appelé "coefficient de Fourier".
]
#slide(
  title:"L'algorithme de Cooley-Tukey",
  subtitle: "Principe"
)[
/*On décompose alors la somme entre les nombres paires et impaires*/
$ X[n] &= sum^(floor(N/2-1))_(m=0)x[2m] e^(-2pi i (2 m n)/N)+ sum^(floor(N/2-1)) x[2m+1] e^(-2 pi i ((2m+1)n)/N)\
&= underbrace(sum^(floor(N/2-1))_(m=0)x[2m] e^(-2pi i (m n)/N/2),E[n]_(N/2))+e^(-2 pi i n/N) underbrace(sum^(floor(N/2-1)) x[2m+1] e^(-2 pi i (m n)/N/2),O[n]_(N/2))\
&=E[n]_(N/2)+e^(-(2 pi i)/N)O[n]_(N/2) $

On en déduit que $cases(X[n]=E[n]_(N/2)+e^((-2 pi i n)/N)O[n]_(N/2), X[n+N/2]=E[n]_(N/2)- e^((-2pi i n)/N) O[n]_(N/2))$
]

#slide(
  title:"L'algorithme de Cooley-Tukey",
  subtitle: "Pseudo-Code"
)[
/*Notes
x : Il s’agit de la séquence d’entrée, c’est-à-dire le signal dont on veut calculer la FFT. Ce paramètre est généralement un tableau de nombres complexes ou réels représentant les valeurs du signal.
N : C’est la longueur de la FFT à calculer, ou le nombre de points dans la séquence d’entrée. Cette valeur doit être une puissance de deux pour l’algorithme de Cooley-Tukey (comme 2, 4, 8, 16, etc.).
s : Ce paramètre représente l’intervalle de saut entre les indices du tableau d’entrée x. Ce saut est utilisé pour accéder aux éléments en divisant récursivement la séquence en sous-séquences de plus en plus petites (pairs et impairs). Au début de la récursion, s est initialisé à 1 (ce qui signifie qu’on prend chaque élément de la séquence), puis il augmente en doublant à chaque étape de la récurs

T[0:N:2] : on prend seulement les éléments aux indices paires.
T[1:N:2] : on prend seulement les éléments aux indices impaires.

%%%

*/
#pseudocode-list(line-gap: 0.3em)[
  + *Fonction* FFT ($X$)
    + *Soit* $N<-$Taille $X$
    + *Si* $N=1$ *alors*
      + *renvoyer* $X[0]$
    + *Fin Si*
    + partie_paire $<-$ FFT($X[0":"N":"2]$)
    + partie_impaire $<-$ FFT($X[1":"N":"2]$)
    + *Pour* $k$ *de* $0$ *à* $N\/2$ :
      + t$<- e^(-2 i pi k/N) times$ partie_impaire[k]
      + $X [k] <-$ partie_paire$[k]+t$
      + $X [k+N\/2] <-$ partie_paire$[k]-t$
    + *Fin Pour*
    + *renvoyer* $X$
]
#place(left, dx:400pt, dy: -350pt)[
  Initialement, $X=[x[k]*e^(2 pi i k/N)]_(k in [|0,N|])$
  ]

]

#new-section-slide("Les limites de la FFT")
#slide(
  title:"Les performance de Shazam",
)[

]
#slide(
  title:"Les performance de Shazam",
)[
/*Notes
Il faut en moyenne 4 seconde à Shazam pour reconnaître un son.
*/
- Reconnaissance $approx 4 unit("s")$
]
#slide(
  title:"Les performance de Shazam",
)[
/*Notes
Si on estime la fréquence d'échantillonage à 44000 Hz
*/
- Reconnaissance $approx 4 unit("s")$
- Fréquence d'échantillonage $= 44 000 unit("Hz")$
]
#slide(
  title:"Les performance de Shazam",
)[
/*Notes
Alors on tombe sur un nombre de point de 176400 pour 4 seconde
*/
- Reconnaissance $approx 4 unit("s")$
- Fréquence d'échantillonage $= 44 000 unit("Hz")$
- Nombre de point : $N=176400$
]
#slide(
  title:"Le résultat d'une simple FFT",
  subtitle:"Les échantillons"
)[
/*Notes
Réalisation d'un premier teste avec ces deux échantillons sur 4 seconde
*/
#place(center+horizon,dx:150pt,dy:-70pt)[
  #figure(
  image("Images/Album Animals.png",width: 25%),
)
]
#place(center+horizon,dx:-150pt,dy: -63pt)[
  #figure(
  image("Images/Album Titanium.png",width: 25%)
)
]
#place(center+horizon,dx:-150pt,dy:50pt)[
  $approx 4 #unit("s")$\
  $176400$ points
]
#place(center+horizon,dx:150pt,dy:50pt)[
  $approx 4 #unit("s")$\
  $176400$ points
]
]
#slide(
  title:"Le résultat d'une simple FFT",
  subtitle:"Le Résultat"
)[
  #place(center+horizon)[
  #figure(
  image("Images/Garrix vs Guetta Spectres.png")
)
]
]

#new-section-slide("2ème Approche - La STFT")
#slide(
  title:"La STFT",
  subtitle:"Définition"
)[
//Definition 1. Algorithme permettant de représenter le spectre de fourrier d'un signal numérique en fonction du Temps
Algorithme permettant de représenter le spectre de fourrier d'un signal numérique en fonction du Temps
]

#slide(
  title:"Application",
  subtitle:"L'échantillon"
)[
/*Notes
Réalisation d'un premier teste avec ces deux échantillons sur 4 seconde
*/
#place(center+horizon)[
  #figure(
  image("Images/Album Voila.png",width: 25%),
)
]
]
#slide(
  title:"Application",
  subtitle:"Résultats"
)[
#figure(
  image("Images/STFT.png"),
)
]

#new-section-slide("Les limites de la STFT")
#slide(
  title:"Les limites",
  subtitle:"La taille de la clé"
)[
- Problème 1 : La taille de la clé
]
#slide(
  title:"La STFT",
  subtitle:"Définition"
)[
- Problème 1 : La taille de la clé\
#image("Images/Fichier_Icone.svg",width: 5%)
#place(left,dy: 30pt,dx:40pt)[
  : $approx 2$ Mo pour 4 secondes
]
]
#slide(
  title:"La STFT",
  subtitle:"Définition"
)[
- Problème 1 : La taille de la clé\
#image("Images/Fichier_Icone.svg",width: 5%)
#place(left,dy: -55pt,dx:40pt)[
  : $approx 2$ Mo pour 4 secondes
]
#image("Images/Note.png",width: 3%)
#place(left,dy: -25pt,dx:40pt)[
  : $approx 3 #unit("min") 30 #unit("s")$
]
]
#slide(
  title:"La STFT",
  subtitle:"Définition"
)[
- Problème 1 : La taille de la clé\
#image("Images/Fichier_Icone.svg",width: 5%)
#place(left,dy: -55pt,dx:40pt)[
  : $approx 2$ Mo pour 4 secondes
]
#image("Images/Note.png",width: 3%)
#place(left,dy: -50pt,dx:40pt)[
  : $approx 3 #unit("min") 30 #unit("s")$
]
#image("Images/Database.svg",width: 3%)
#place(left,dy: -30pt,dx:40pt)[
  : $approx 20 #unit("M")$ de son.
]
]
#slide(
  title:"La STFT",
  subtitle:"Problème"
)[
- La taille de la clé\
#image("Images/Fichier_Icone.svg",width: 5%)
#place(left,dy: -55pt,dx:40pt)[
  : $approx 2$ Mo pour 4 secondes
]
#image("Images/Note.png",width: 3%)
#place(left,dy: -50pt,dx:40pt)[
  : $approx 3 #unit("min") 30 #unit("s")$
]
#image("Images/Database.svg",width: 3%)
#place(left,dy: -55pt,dx:40pt)[
  : $approx 20 #unit("M")$ de son.
]
Résultat : 206 565 To de donné à parcourir.
]
#new-section-slide("L'algorithme Shazam")
#slide(
  title:"Principe",
  subtitle:"L'échantillon utilisé"
)[
/*Notes
On utilisera voilà pour l'exemple d'utilisation
*/
#place(center+horizon)[
  #figure(
  image("Images/Album Voila.png",width: 25%),
)
]
]
#slide(
  title:"1ère étape : La FFT",
  subtitle:"Simple FFT"
)[
  /*Notes
On reprend la FFT qu'on avait avant
  */
  #place(center+horizon)[
    #image("Images/Simple FFT.svg",width: 70%)
  ]
]
#slide(
  title:"1ère étape : La FFT",
  subtitle:"Sélection des n extremum FFT"
)[
  /*Notes
On reprend la FFT qu'on avait avant
  */
  #place(center+horizon)[
    #image("Images/Extremum FFT.svg",width: 70%)
  ]
]
#slide(
  title:"1ère étape : La FFT",
  subtitle:"Application du principe à la STFT"
)[
  /*Notes
On applique alors le principe à la STFT
  */
#figure(
  image("Images/STFT.png"),
)
]
#slide(
  title:"1ère étape : La FFT",
  subtitle:"Application du principe à la STFT"
)[
  /*Notes
On applique alors le principe à la STFT en prenant les 15 pics
  */
#figure(
  image("Images/Constellation.svg",width: 80%),
)
Voir l'annexe pour le code de génération de la constellation.
]
#slide(
  title:"2ème étape : Le Hashage",
  subtitle:"Fonction de Hashage combinatoire"
)[
  /*Notes
On reprend la FFT qu'on avait avant
  */
A faire
]
#slide(
  title:"3ème étape : Constitution des bases de données",
  subtitle:""
)[
  /*Notes
On construit 2 tables
  */
#place(center+horizon)[
#table(
  columns: (auto, auto),
  align: horizon+center,
  table.header(
    [#image("Images/Database.svg") *Index Musique*], [#image("Images/Database.svg") *Hashes*],
  ),[
    #table(
      columns: (auto,auto),
      align: horizon+center,
      table.header(
        [*ID musique*],[*Titre musique*]
      ),
    [1],[Voilà],[2],[Animals - Martin Garrix],[$dots.v$],[$dots.v$])
  ],[
  #table(
      columns: (auto,auto),
      align: horizon+center,
      table.header(
        [*ID musique*],[*Tableau de tuple (temps,hashe)*]
      ),
    [1],[[(0,28923),...,($N_1$,98467)]],[2],[(0,976643),...,($N_2$,098348)],[$dots.v$],[$dots.v$])
  ]
)
]
]
#slide(
  title:"4ème étape : Reconaissance",
  subtitle:"Résumé"
)[
  /*
  Notes
  Résumé de ce qu'on a fait jusque là
  */
1. STFT
2. Constellation
3. Hashage
\
\
#place(center)[
  On souhaite maintenant comparer les données acquises avec la base de donnée.
]
]
#slide(
  title:"4ème étape : Reconaissance",
  subtitle:"Comparaison de l'Échantillon"
)[
  #place(center,dy:-230pt)[
    #image("Images/Correlation Step 1.svg",width: 40%)
  ]
]
#slide(
  title:"4ème étape : Reconaissance",
  subtitle:"Comparaison de l'Échantillon"
)[
  #place(center,dy:-230pt)[
    #image("Images/Correlation Step 1.svg",width: 40%)
    #image("Images/Correlation Step 2.svg",width: 110%)
  ]
]
#slide(
  title:"4ème étape : Reconaissance",
  subtitle:"Comparaison de l'Échantillon"
)[
  #place(center,dy:-230pt)[
    #image("Images/Correlation Step 1.svg",width: 40%)
    #image("Images/Correlation Step 2.svg",width: 110%)
    #image("Images/Correlation Step 3.svg",width: 110%)
  ]
]
#slide(
  title:"4ème étape : Reconaissance",
  subtitle:"Compilation des résultats"
)[
  #place(horizon,dx:50pt)[
    #image("Images/Correlation Step 4.svg")
  ]
]
#slide(
  title:"4ème étape : Reconaissance",
  subtitle:"Compilation des résultats"
)[
  #place(horizon,dx:50pt)[
    #image("Images/Correlation Step 4.svg")
  ]
  #place(horizon+right,dx:-50pt)[
    #image("Images/Correlation Step 5.svg")
  ]
]
#slide(
  title:"5ème étape : Reconaissance",
  subtitle:"Tri"
)[
  #place(left+horizon)[
    #image("Images/Tri Step 1.svg")
  ]
]
#slide(
  title:"5ème étape : Reconaissance",
  subtitle:"Tri"
)[
    #place(left+horizon)[
    #image("Images/Tri Step 2.svg")
  ]
]
#slide(
  title:"5ème étape : Reconaissance",
  subtitle:"Conclusion"
)[
    #place(center+horizon)[
    #image("Images/Podium.png")
  ]
]
#focus-slide(new-sec: none)[
  FIN
]

#new-section-slide("Annexe")
#slide(
  title:"La fonction de hashage en détail"
)[
```py
def create_hashes(constellation, song_id=None):
    hashes = {}
    freq_max = 23_000
    n_bits_freq = 10
    for idx, (time, freq) in enumerate(constellation):
        for next_time, next_freq in constellation[idx : idx + 60]:
            diff = next_time - time
            if diff <= 1 or diff > 10:
                continue
            freq_binned = freq / freq_max * (2 ** n_bits_freq)
            other_freq_binned = next_freq / freq_max * (2 ** n_bits_freq)
            hash = int(freq_binned) | (int(other_freq_binned) << 10) | (int(diff) << 20)
            hashes[hash] = (time, song_id)
    return hashes,occurrence_hash
}
```
]
#slide(
  title:"La fonction de hashage en détail"
)[
#place(center+horizon)[
  #image("Images/Collisions.svg",width: 100%)
]
]
#slide(
  title:"Génération de la constellation en détail"
)[
  ```py
def cree_constellation(audio, Fs):
    # Paramètres
    Fenetre = 0.5 #en seconde
    #fréquence d'échantillonage : on utilise celui du CD
    freq_ech = 44100 #Hz
    Nbre_point = int(Fenetre * freq_ech)
    Nbre_point += Nbre_point % 2
    # Nombre de pic voulu, plus la fenêtre est grande plus le nombre de pics peut être élevé.
    Nbre_pics = 4

    # Complète le son pour obtenir des multiple de Nbre_point
    amount_to_pad = Nbre_point - audio.size % Nbre_point

    #Nouveau son tel qu'il est divisible par Nbre_point
    son_complete = np.pad(audio, (0, amount_to_pad))

    # On procède à une transformé de fourrier sur le son complété
    frequences, temps, stft = signal.stft(
        son_complete, Fs, nperseg=Nbre_point, nfft=Nbre_point, return_onesided=True
    )

    # Initialisation de la constellation
    constellation = []

    for temps_id, fen in enumerate(stft.T):
        # Le spectre est complexe par défaut.
        # Nous voulons seulement son module.
        spectre = abs(fen)
        # find_peaks retourne les pics et leurs caractéristique, ici la distance entre 2 pics doit être de 2000 points.
        pics, props = signal.find_peaks(spectre, prominence=0, distance=2000)
        # Nous souhaitons uniquement les pics les plus proéminent.
        # Avec un maximum de 4 pics par tranche.
        Nbre_pics_1 = min(Nbre_pics, len(pics))
        largest_peaks = np.argpartition(props["prominences"], -Nbre_pics_1)[-Nbre_pics_1:]
        for pic in pics[largest_peaks]:
            frequence = frequences[pic]
            constellation.append([temps_id, frequence])

    return constellation
  ```<Annexe-Constellation>
  
]