# Représentation procédurale d’une grammaire EBNF en Python
## Description
Ce projet vise à implémenter une représentation procédurale d’une grammaire EBNF (Extended Backus–Naur Form) en utilisant le langage Python.
L’objectif principal est de modéliser les règles de production grammaticales sous forme de structures procédurales afin de faciliter leur définition, leur compréhension et leur manipulation.

Ce travail s’inscrit dans un contexte pédagogique lié à l’étude des langages formels et des techniques de modélisation syntaxique.

## Objectifs
- Représenter les symboles terminaux et non-terminaux d’une grammaire EBNF
- Implémenter les opérateurs fondamentaux de l’EBNF (séquence, alternative, option, répétition)
- Proposer une approche procédurale simple et lisible

## Rappels sur la grammaire EBNF
L’EBNF (Extended Backus–Naur Form) est une extension de la notation BNF permettant de décrire la syntaxe des langages formels à l’aide des constructions suivantes :
- Sequence : A B
- Alternative : A|B
- Option : [A]
- Répétition : {A}
- Groupement : (A)

## Approche adoptée
L'application récupère une règle EBNF entrée par l'utilisateur, lit cette règle et produit un tableau de tokens définis préalablement. Grâce à ce tableau de tokens, elle construit un arbre syntaxique abstrait puis génère finalement la procédure représentative.

## Prérequis
- Python 3.9 ou supérieur
Aucune bibliothèque extérieure n'est requise.

## Exécution
Pour exécuter le code:
```bash
python -u main.py
```

## Auteurs
[EL HAFFARI Soumia](https://github.com/Soumiaelhaffari25) \
[SOULEY Kossi Adelphe](https://github.com/adelphe1109)
