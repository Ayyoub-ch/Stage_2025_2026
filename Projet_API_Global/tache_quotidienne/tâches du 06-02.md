Nouvel essai afin de comprendre pourquoi je n'arrive pas à avoir toutes les données dans chaque case + les séances divisées en deux colonnes : DEBUT\_SEANCE et FIN\_SEANCE





Réussis:

-Faire en sorte que les séances soient séparées et le tableau indemne (Cinema Now uniquement) 12h30

-Faire en sorte que le Cinema soit complété (Liste déroulante ajoutée + Séances formatées en deux colonnes

-Faire en sorte que les noms des colonnes soient renommées



A faire:

-Faire en sorte que la date puisse changer (mettre min et max)







EXPLICATIONS du programme

1 ) Fonction safe\_parse\_seances



**def safe\_parse\_seances(x):**



*Elle prend x en paramètre et son but est de convertir x en liste Python de manière surement, si elle ne peut pas elle renvoie une liste vide*





<b>   if pd.isna(x) or x == '':</b>

<b>       return \[]</b>





*Si on a une chaine vide ou qu'on détecte un None alors on renvoie une liste vide, l'objectif est d'éviter une erreur ou une exception*





    **if isinstance(x, list):**

        **return x**



*Ici on vérifie que le type de x est une liste, si c'est le cas alors on renvoie simplement x*



*Cela est vérifier afin que si cela est le cas alors on évite des erreurs ou bien un parsing en trop*









<b>    try:</b>

<b>        parsed = json.loads(x)</b>





*Autrement on parse le json grâce à json.loads(x)*



Ce qui donnerait:

'\[{"a":1}]' → \[{"a":1}]



Cela peut lever des erreur si le JSON est invalide ou bien si le type de x n'est pas une string



* JSONDecodeError si le JSON est invalide



* TypeError si x n’est pas une string







        **if isinstance(parsed, list):**

            **return parsed**

        **else:**

            **return \[]**





*Si le type du résultat est une liste alors on le renvoie autrement on retourne une liste vide* 

*Parce que json.loads(x) peut retourner une dictionnaire ou bien un nombre ou tout autre type possible à l'intérieur du JSON*







<b>Gestion des Erreurs</b>



<b>    except (json.JSONDecodeError, TypeError):</b>

<b>        return \[]</b>



*S'il y a une erreur alors on retourne une liste vide*







2 ) Bloc Streamlit



&nbsp;   if st.session\_state.api\_data is not None:

*Si les données sont présentes alors on affichera le résultat*







&nbsp;       films = st.session\_state.api\_data

*on place les données qui sont sous forme de dictionnaire json* 

*les données contiennent probablement une clé SEANCES*





&nbsp;       display\_data(

&nbsp;           films,

&nbsp;           st.session\_state.api\_filename

&nbsp;       )

*Affichage simple des données avec un bouton de téléchargement*





&nbsp;       df = pd.DataFrame(\[films])

*Création d'un dataframe* 

*films étant un dictionnaire on le met dans une liste, ce dataframe n'est qu'une seule ligne*

*chaque clé deviendra une colonne*







        **df\['SEANCES'] = df\['SEANCES'].apply(safe\_parse\_seances)**

*On applique la fonction safe\_parse\_seances aux cellules de SEANCES issues du DataFrame, même s'il y a une faille*





<b>        df = df.explode('SEANCES')</b>

*On explose chaque élément de la liste afin qu'on a une liste*

*Exemple: un film ayant 5 séances -> 5 lignes* 

*Autrement si la liste est vide, on conserve la ligne mais dans SEANCES il y aura NaN*





<b>        df\['SEANCES'] = df\['SEANCES'].apply(lambda x: x if isinstance(x, dict) else {})</b>



*Ici on force chaque cellule à être soit un dictionnaire valide soit vide*

*Cela évite les erreurs ou crash*





<b>        seances\_details = df\['SEANCES'].apply(pd.Series)</b>

*On extrait les champs dans SEANCES pour que chaque dictionnaire devient plusieurs colonnes* 

*Exemple:* 

*{"DEBUT": "18:00", "FIN": "20:00"}*

*➡️ Colonnes DEBUT, FIN*

*Si c'est un dictionnaire vide alors on aura une colonne vide avec comme valeur NaN*





<b>        df\_final = pd.concat(</b>

<b>            \[df.drop(columns=\['SEANCES']), seances\_details],</b>

<b>            axis=1</b>

<b>        ).fillna('')</b>

*Finalement on supprime la colonne SEANCES et on fusionne avec les détails juste au dessus* 

*autrement ce qui est avec NaN on remplace par des guillemets*

*On obtient un tableau plat prêt à l'affichage*





        ***st.subheader("Films avec séances détaillées")***

        ***st.dataframe(df\_final, use\_container\_width=True)***



*On ajoute un titre secondaire  et on affiche le tableau (largeur adaptative)*









