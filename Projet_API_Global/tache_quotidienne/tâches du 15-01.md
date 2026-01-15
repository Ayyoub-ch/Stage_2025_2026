But : Trouver des Apis corrects

Essayer d'extraire les données de l'API Festivals de France





Je n'ai pas trop réussi à trouver des API Sports mais grâce à JP j'ai pu trouver quelque chose d'exploitable

Pour l'API Festival j'ai trouver quelque chose et je l'ai extrait, j'ai pris les champs avantageux, vérifiés les cas complexes

comme les années non conformes ou les codes postaux multiples




Pour le Football ou le sport en général, je dois voir ce site là pour récolter les données efficacement: 
https://www.football-data.org/documentation/quickstart
https://www.thesportsdb.com/documentation#search_v1 (lui bof bof)


PARTIE FESTIVAL : (FAITE)

données intéressantes:

* nom\_du\_festival
* region\_principale\_de\_deroulement
* departement\_principal\_de\_deroulement
* commune\_principale\_de\_deroulement
* code\_postal\_de\_la\_commune\_principale\_de\_deroulement
* numero\_de\_voie
* type\_de\_voie\_rue\_avenue\_boulevard\_etc
* nom\_de\_la\_voie
* adresse\_postale
* complement\_d\_adresse\_facultatif
* site\_internet\_du\_festival
* annee\_de\_creation\_du\_festival
* discipline\_dominante
* sous\_categorie\_spectacle\_vivant
* sous\_categorie\_musique
* sous\_categorie\_musique\_cnm
* sous\_categorie\_cinema\_et\_audiovisuel
* sous\_categorie\_arts\_visuels\_et\_arts\_numeriques
* sous\_categorie\_livre\_et\_litterature
* periode\_principale\_de\_deroulement\_du\_festival
* identifiant
* geocodage\_xy







cas aberrants:



"annee\_de\_creation\_du\_festival": "2012 a eu lieu le premier Coup de théâtre",

"annee\_de\_creation\_du\_festival": "01/01/2016 00:00",







