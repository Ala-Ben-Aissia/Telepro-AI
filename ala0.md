```
République Tunisienne
```

---

Ministère de l’Enseignement Supérieur et de la Recherche Scientifique

---

Université de Monastir

---

Institut Supérieur d’Informatique et de Mathématiques de Monasti

---

Département informatique\*\*

# Projet Fin d’Année

###### Spécialité :

###### Sciences Informatiques

###### Elaboré Par :

###### MALEK BOUBAKER

**MAJDI BOUBAKER**

**IMEN CHATTI**

**RIMA BOUWAZRA**

**MAYARA BOUWAZRA**

**AYOUB CHOUCHANE**

**SADOK BEN SALEM**

## Gestion des Clubs en ligne

```
Soutenu le 2 7 - 02 - 2024 devant le jury composé de :
Docteur Bouzidi Aljia
Année universitaire : 202 3 – 2024
```

## Table des matières

Chapitre I : Etude préalable

1.contexte de Travail

- 1.1 Cadre du Projet
- 1.2 Présentation de l'Organisme (ISIMM)
- 1.3 Idée de Projet

2 .Etude de l’Existant

- 2.1 Solutions Existantes

```
▪ 2.1.1 IHEC Carthage
```

```
▪ 2.1.2 Faculté des Sciences de Monastir
```

```
▪ 2.1.3 Institut Supérieur de Biotechnologie de Monastir
```

- 2.2 Critiques de l’Existant

3 Solution Retenue

- 3.1 Description de la Solution
- 3.2 Architecture Technique
- 3.3 Design de l’Interface Utilisateur

4 Méthodologie du Travail

- 4.1 Méthode 2TUP: Two Tracks Unified
- 4.2 Gestion de Projet

5 Conclusion

Chapitre II : Analyse & spécification des besoins

1. Identification des acteurs

2.Modèle Informationnel de Contexte

- 2.1 Diagramme de Contexte

  3.Capture des Besoins

- 3.1 Besoins Fonctionnels
- 3.2 Besoins Non Fonctionnels

4. Spécification des Besoins

- 4.1 Diagramme de cas d’Utilisation Global
- 4.2 Diagrammes de cas d’utilisation détaillés

```
▪ 4.2.1 Diagramme de cas d’utilisation détaillé de l’acteur ”internaute”
```

```
▪ 4.2.2 Diagramme de cas d’utilisation détaillé de l’acteur”responsable de club”
```

- 4.3 Diagrammes de séquence acteur-système

```
▪ 4.3.1 Diagramme de séquence “demander de rejoindre cub”
```

```
▪ 4.3.2 Diagramme de séquence “responsable club”
```

5 Choix techniques

- 5.1 Bibliothèque React
- 5.2 Framework Laravel

Chapitre III : Conception

1.Architecture Applicative

- 1.1 Architecture Physique : Architecture 3 - tiers
- 1.2 Architecture Logique : MVC
- 1.3 Architecture de l’Application

2. Conception de base de données

- 2.1. MCD
- 2.2. MLD

3. Conception Logicielle

- 3.1. Vue Statique: Diagramme de Classe d’Analyse
- 3.2. Vue Dynamique: Diagramme de séquence

  4.Conception Graphique

- 4.1. Maquettage

```
4.1.1. Interface d’information
```

```
4.1.2. Interface de choix entre s’inscrire et se connecter
```

```
4.1.3 Interface de présentation des clubs et des responsables des clubs
```

5. Conclusion

## Table des figures

### Figure 1 : “Espace de clubs étudiants à l’IHEC”

**Figure 2 :** “ Suivi espace de clubs étudiants à l’IHEC”

**Figure 3 :** “Espace de clubs étudiants à la faculté des sciences de Monastir”

**Figure 4 :** “ Espace de clubs étudiants à l’ISBM ”

##### Figure 5 : “Diagramme de Méthode 2TUP ”

**Figure 6** : “ Diagramme de contexte”

###### Figure 7 : “ Diagramme de cas d’utilisation global”

**Figure 8 :** “Diagramme de cas d’utilisation détaillé “Internaute” ”

**Figure 9 :** “Diagramme de cas d’utilisation détaillé “Responsable du Club” ”

###### Figure 10 : “Diagramme de Séquence “demande de rejoindre Club” ”

**Figure 1 1 :** “Diagramme de Séquence “Responsable du Club” ”

**Figure 1 2 :** “ Diagramme de comparaison entre les Frameworks JS”

**Figure 1 3 :** “Comparaison Entre les Frameworks PHP”

**Figure 1 4 :** “Architecture 3-tiers”

**Figure 1 5 :** “ L’architecture du Modèle MVC ”

**Figure 1 6 :** “ Modèle Conceptuel des Données”

**Figure 1 7 :** “ Diagramme de classe”

**Figure 1 8 :** “Diagramme de classe de conception”

###### Figure 1 9 : “Diagramme de séquence”

**Figure 20 :** “Interface de plus d’information”

Figure 2 1 : “Interface de choix entre se connecter et s’inscrire”

**Figure 22 :** “Interface d’inscription”

**Figure 23 :** “Interface de connexion”

**Figure 24 :** “Interface des clubs et responsables”

## Liste des tableaux

**Tableau 1 : Tableau comparatif entre les solutions existantes**

**Tableau 2 : Description textuelle : Cas d’utilisation : Demander de joindre club**

**Tableau 3 : Description textuelle : Cas d’utilisation : gérer évènement**

**Tableau 4 : Tableau comparatif entre les solutions existantes**

## Liste des abréviations

ISIMM **:** Institue Supérieur de l’Informatique et de Mathématique Monastir

IHEC **:** Institue de Hautes Études Commerciales

C : Critère

Js : JavaScript

ReactJS **:** React JavaScript

MYSQL :

MY : the name of co-founder Michael Widenius's daughter

SQL: Structured Query Language

2Tup : Two Tracks Unified

UML : Langage de Modélisation Unifié

WCAG : Règles pour l’Accessibilité des Contenus Web

API : Interface de Programmation d’Information

DOM : Document Object Model

MVC : Modèle – Vue – Contrôleur

BD : Base de Donnée

CSRF : Cross-Site Request Forgery

PHP : Hypertext Preprocessor

MCD : Modèle Conceptuel de Donnée

MLD : Modèle Logique de Donnée

E/A : Entité Association

HTTPS : Protocole de Transfert Hypertexte Sécurisé

IEEE : The Institute of Electrical and Electronics Engineers

CPU : Cyber Processing Unit

CRI : Club Robotique Isimm

## INTRODUCTION GENERALE

```
L'épanouissement académique ne se limite pas aux seules salles de classe. Il s'étend
```

également aux activités extra-scolaires, qui jouent un rôle crucial dans le développement

personnel et professionnel des étudiants. Dans cette optique, l'Institut Supérieur

d'Informatique et de Mathématiques de Monastir(ISIMM) reconnaît l'importance des clubs

étudiants comme catalyseurs de la vie universitaire, offrant un espace pour l'exploration, la

collaboration et la croissance.

```
Afin de valoriser et de faciliter l'engagement des étudiants dans ces clubs, nous avons
```

entrepris le développement d'une plateforme de gestion des clubs étudiants, destinée à

rationaliser les processus administratifs, à promouvoir la participation des étudiants et à

renforcer la communauté étudiante au sein de l'institut.

```
Le présent rapport présente les différentes étapes de la réalisation de notre projet qui
```

s’étale sur quatre chapitres. Au niveau du premier chapitre « Étude préalable », nous

présenterons le cadre général et l'idée émergente du projet puis les solutions existantes et la

méthodologie de travail. Dans le deuxième chapitre « Analyse et spécification des besoins »,

nous mettrons l’accent sur les spécifications des besoins fonctionnels, non fonctionnels et les

besoins techniques. Nous procéderons au cours du troisième chapitre à la « Conception »,

nous allons détailler la conception de la base de données, ainsi que les couches logicielles de

notre application. Nous aborderons aussi la conception des interfaces utilisateurs. Il illustre

aussi les différentes interfaces de notre système. Et pour finir, nous clôturerons notre rapport

par une conclusion générale.

###### CHAPITRE I : Etude préalable

INTRODUCTION :

###### Au cours de ce chapitre, nous allons présenter notre projet en

###### étudiant son cadre général et la problématique qui a mené l'organisme

###### d'accueil à réaliser cette application. Ensuite nous allons procéder à

###### l’étude de l’existant avec leurs critiques et nous introduirons les solutions

###### proposées. Par la suite, nous allons aborder une étude sur les différentes

###### méthodologies de travail existantes afin de dégager celle la plus

#### adéquate à notre projet.

###### 1.Contexte de travail :

Dans cette partie, nous allons présenter le cadre général du projet et ses objectifs.

**1.1 Cadre du Projet :**

```
Objectif du Projet : Mettre en place une plateforme centralisée de gestion des clubs à
l'ISIMM pour faciliter la communication, la coordination et la visibilité des activités des
différents clubs.
```

```
Portée du Projet : La plateforme couvrira la gestion des événements, des membres,
des ressources, et la communication interne des clubs.
```

**1.2 Présentation de l'Organisme (ISIMM) :**

```
Nom de l'Institut : ISIMM - Institut Supérieur d'Informatique et de Mathématique de
Monastir.
```

```
Mission et Vision : Former des professionnels compétents dans le domaine de
l'informatique, mathématiques, EEA(Electronique,Electrotechnique et Automatique) et
TIC(Technologies de l’Information et de Communication) tout en encourageant la
participation étudiante à travers des clubs et des activités parascolaires.
```

Structure organisationnelle :

```
La structure administrative:
```

```
Département d'Informatique
Département de Mathématiques
Département d'Électronique
```

**1.3 Idée de Projet :**

```
Description du Projet : La plateforme permettra aux différents clubs de l'ISIMM de
gérer efficacement leurs membres, d'organiser des événements, de partager des
ressources, et de favoriser la collaboration entre les clubs.
```

```
Bénéfices attendus : Amélioration de la coordination entre les clubs, accès facile aux
```

###### informations et ressources, et renforcement de la vie étudiante.

###### 2. Étude de l'existant :

L'étude de l'existant consiste à auditer les solutions existantes pour s’inspirer et pour

raffiner de plus l’idée émergente.

2.1 Solutions Existantes :

```
2.1.1.IHEC Carthage :
```

```
Figure 1: “espace de clubs étudiants à l’I HEC
```

```
Figure 2: “ suivi espace de clubs étudiants à l’IHEC”
```

L'Institut des Hautes Études Commerciales (IHEC) Carthage est une institution d'enseignement
supérieur située à Carthage, en Tunisie. Il est réputé pour ses programmes en économie,
gestion, et commerce.

```
Méthodes Actuelles de Gestion des Clubs :
```

Documents Papier : Les clubs peuvent utiliser des documents papier pour tenir des registres
des membres, des budgets, et des activités planifiées.

E-mails et réunions physiques : La communication entre les membres des clubs peut se faire
via des échanges d'e-mails et des réunions physiques régulières pour discuter des activités et
des projets en cours.

Affichage sur le Campus : Les clubs peuvent utiliser des affiches et des panneaux d'affichage
sur le campus pour promouvoir leurs événements et recruter de nouveaux membres.

**2.1.2.Faculté des Sciences de Monastir :**

```
Figure 3: “espace de clubs étudiants à la faculté des sciences de Monastir”
```

La Faculté des Sciences de Monastir est l'une des institutions universitaires de référence
en Tunisie dans le domaine des sciences naturelles et appliquées. Elle propose des
programmes d'études dans des disciplines telles que la biologie, la physique, la chimie et les
mathématiques.

```
Méthodes Actuelles de Gestion des Clubs :
```

Documents Papier et Registres : Les clubs peuvent maintenir des documents papier et des
registres pour enregistrer les activités des membres, les budgets, et les décisions prises lors
des réunions.

Réunions en Personne : Les réunions en personne sont souvent utilisées pour discuter des
activités planifiées, des projets en cours, et des préoccupations des membres.

Groupes de Discussion en Ligne : Certains clubs peuvent utiliser des groupes de discussion en
ligne via des plateformes telles que WhatsApp ou Facebook pour faciliter la communication et
la coordination entre les membres.

**2.1.3.Institut Supérieur de Biotechnologie de Monastir :**

```
Figure 4: “espace de clubs étudiants à l’ISBM ”
```

```
L'Institut Supérieur de Biotechnologie de Monastir est une institution spécialisée dans le
domaine des biotechnologies, de la biologie moléculaire, et de la biochimie. Il offre des
programmes de formation et de recherche avancés dans ces domaines
```

```
Méthodes Actuelles de Gestion des Clubs :
```

```
Documents Papier et Fichiers Partagés : Les clubs peuvent utiliser des documents papier et
des fichiers partagés pour enregistrer les informations sur les membres, les budgets, et les
événements planifiés.
```

```
Réunions et Assemblées Générales : Les réunions et les assemblées générales sont
organisées régulièrement pour discuter des activités du club, prendre des décisions
importantes, et élire des responsables.
```

```
Utilisation de Messagerie Instantanée : Les membres des clubs peuvent utiliser des
applications de messagerie instantanée comme WhatsApp ou Telegram pour communiquer
rapidement et efficacement sur les projets en cours et les événements à venir.
```

2.2 Critiques de l'Existant :

Nous pouvons classer les résultats de l'analyse des applications web existantes
mentionnées précédemment, comme l’illustre le tableau 1, selon huit critères (Cx) pris en
considération dans le processus d'évaluation de ses applications :

o **C1 : Temps de réponse :** Le temps qui s'écoule entre l'application d'un stimulus et la
réaction volontaire consécutive.

o **C2 : Structure :** L'organisation et la structure d'une application sont les deux éléments
principaux qui définissent son architecture. En effet, ce sont tous les éléments qui vont
permettre de faire fonctionner l'application et surtout c'est comment ils vont permettre de le
faire.

o **C3 : Mise à jour :** Une mise à jour est un programme destiné à apporter une correction à
un programme existant, régulièrement, les mises à jour de son système sont destinées à
améliorer l’expérience de l’utilisateur.

o **C4 : Gestion de profil :** Préserver la simplicité lors de la gestion d'un profil utilisateur ou
modèle d'utilisateur est un ensemble de données et métadonnées fonctionne d'un ou
plusieurs utilisateurs qui influence le comportement d'un dispositif informatique.

o **C5 : Message :** La messagerie c'est un système qui permet à deux ou plusieurs personnes
de discuter virtuellement via un logiciel adéquat.

###### o C6 : Notification : La notification est la formalité par laquelle on tient officiellement une

###### personne, informée du contenu d'un acte à laquelle elle n'a pas été partie.

###### o

o **C7 : participation en ligne :** Passer les demandes de participer aux événements en ligne
sans se déplacer.

o **C8: Paiement en ligne :** Payer les factures en ligne et immédiatement.

###### Les existants

#### Critères

```
IHEC
Carthage
```

```
Faculté des
Sciences de
Monastir
```

```
Institut Supérieur de
Biotechnologie de
Monastir
```

##### C1 : Temps de

##### réponse

##### C2 : Structure

##### C3 : Mise à jour

##### C4 : Gestion de

##### profil

##### C5 : Message

##### C6 : Notification

##### C7 : participation en

##### ligne

##### C8: Paiement en

##### ligne

```
Tableau 1 : Tableau comparatif entre les solutions existantes
```

###### 3. solution retenue :

**3.1 Description de la Solution**

```
Fonctionnalités clés : Gestion des membres, planification d'événements, partage de
ressources, forum de discussion entre clubs.
```

```
Innovations : Intégration d'un système de suivi des participations, notifications en temps réel,
interface intuitive.
```

**3.2 Architecture Technique :**

##### Technologies Utilisées :

```
Pour le développement de la plateforme de gestion des clubs étudiants, nous avons utilisé
les technologies suivantes :
Langages de Programmation : Nous avons utilisé JavaScript pour le développement front-
end de l'interface utilisateur avec ReactJS comme framework principal. Pour le développement
back-end, nous avons utilisé PHP avec le framework Laravel.
```

```
Framework de Développement : ReactJS a été choisi pour sa capacité à créer des
interfaces utilisateur interactives et dynamiques de manière efficace. Il offre une structure
modulaire et facilite la gestion de l'état des composants.
```

```
Base de données : Nous avons utilisé MySQL comme système de gestion de base de
données pour stocker les informations relatives aux clubs, aux membres, aux événements, etc.
MySQL s'intègre bien avec Laravel pour assurer une interaction fluide entre l'application et la
base de données.
```

**Sécurité :**

```
En ce qui concerne la sécurité des données des clubs et des membres, nous avons mis en
place les protocoles suivants :
```

```
Chiffrement des Données : Toutes les données sensibles sont cryptées lors de leur
transmission sur le réseau et lors de leur stockage dans la base de données. Nous utilisons
des protocoles de chiffrement standard tels que HTTPS pour assurer la confidentialité des
informations.
```

```
Gestion des Identifiants : Nous utilisons des techniques de hachage sécurisé pour stocker
les mots de passe des utilisateurs dans la base de données, tant du côté front-end avec
ReactJS que du côté back-end avec Laravel.
```

**Contrôle d'Accès :** Nous avons mis en place un système de contrôle d'accès basé sur les
rôles pour limiter l'accès aux différentes fonctionnalités de l'application en fonction des
privilèges des utilisateurs, avec une gestion efficace de l'état des composants dans ReactJS.

**Audit et Surveillance :** Nous effectuons régulièrement des audits de sécurité pour identifier
et corriger les vulnérabilités potentielles de l'application, en tenant compte des aspects front-
end et back-end de l'application.

**3.3 Design de l'Interface Utilisateur :**

###### Convivialité : Interface conviviale avec une navigation facile.

**Carte Graphique :** Utilisation des couleurs et du logo de l'ISIMM pour une identité visuelle cohérente.

###### 4. MÉthodologie du travail :

Avant de réaliser chaque projet, il est nécessaire de choisir une méthodologie de travail afin
d’aboutir à un logiciel fiable, adaptable et efficace. Et pour pouvoir choisir la méthodologie la
plus adéquate nous avons procédé à une comparaison entre la méthode 2Tup

**4.1 Méthode 2TUP: Two Tracks Unified:**

La méthode 2 Tracks Unified est un processus de développement logiciel qui met en œuvre
la méthode du processus unifié (c'est-à-dire construit sur UML, itératif, centré sur l'architecture
et conduit par les cas d'utilisation).
Le 2TUP propose un cycle de développement en Y, qui dissocie les aspects techniques des
aspects fonctionnels. Il commence par une étude préliminaire qui consiste essentiellement à
identifier les acteurs qui vont interagir avec le système à construire, les messages

qu'échangent les acteurs et le système, à produire le cahier de charges et à modéliser le
contexte.

```
Le processus s'articule ensuite autour de trois phases essentielles :
```

```
Une branche fonctionnelle : elle capitalise la connaissance du métier de l’entreprise. Cette
branche capture des besoins fonctionnels, ce qui produit un modèle focalisé sur le métier des
utilisateurs finaux.
```

```
Une branche technique : capitalise un savoir-faire technique et/ou des contraintes
techniques. Les techniques développées pour le système sont indépendamment des fonctions
```

###### à réaliser.

```
Une phase de réalisation : elle consiste à réunir les deux branches, permettant de mener une
conception applicative et enfin la livraison d'une solution adaptée aux besoins
```

```
Figure 5 : “Diagramme de Méthode 2TUP”
```

**4.2 Gestion de Projet :**

##### Équipe Projet :

###### les membres de l'équipe :

MALEK BOUBAKER

MAJDI BOUBAKER

IMEN CHATTI

RIMA BOUWAZRA

MAYARA BOUWAZRA

AYOUB CHOUCHANE

SADOK BEN SALEM

```
Les responsables des clubs impliqués:
```

**The Code Bey : Yassine Bouajila**

**IEEE : Louay Jaber**

**CPU : Rayen lahmar**

**CRI : Bachir Gara**

**Englistics : Omar Hassan**

**Outils de Gestion :**

```
Dans le cadre de l'amélioration de la gestion des activités au sein de nos clubs étudiants,
nous avons adopté une approche combinée faisant appel à Trello pour la gestion des
tâches et à des réunions régulières pour la communication et la coordination.
```

###### 5 .Conclusion :

```
En guise de conclusion, dans ce chapitre nous avons mis notre projet dans
son cadre général. Ensuite, nous avons étudié les solutions existantes et
proposé notre propre solution. Enfin, nous avons clôturé la méthodologie de
développement que nous avons adoptée. Dans le chapitre suivant nous allons
spécifier les différents besoins auxquels doit répondre notre application.
```

### CHAPITRE II : Analyse et spécifications des besoins

INTRODUCTION :

L’étape d’analyse et spécification des besoins est une étape indispensable pour
comprendre les fonctionnalités que le système doit fournir. Dans ce chapitre nous présenterons
les fonctionnalités fournies et les acteurs concernés par notre système. Nous allons exprimer les
besoins fonctionnels et non fonctionnels sous forme de diagrammes de cas d’utilisation et des

###### diagrammes de séquence.

###### 1.Identification des acteurs:

```
Un acteur est une entité externe qui définit le rôle joué par un utilisateur,
humain ou non humain, qui interagit avec un système interactif. Notre système
comporte les acteurs suivants :
```

**Étudiants :**

```
Les étudiants sont les utilisateurs finaux de la plateforme de gestion des clubs. Ils
utilisent l'application pour explorer les clubs disponibles, s'inscrire à des clubs qui les
intéressent, participer aux événements organisés par les clubs et interagir avec d'autres
membres.
```

**Responsables des Clubs :**

```
Les responsables des clubs sont les étudiants ou membres du personnel qui dirigent et
gèrent les clubs étudiants. Ils utilisent l'application pour créer et gérer le profil de leur
club, publier des informations sur les activités et les événements du club, gérer les
membres du club et communiquer avec eux.
```

**Administrateurs :**

```
Les administrateurs sont les membres de l'équipe de gestion de la plateforme. Leur rôle
est de superviser et de gérer l'ensemble du système, y compris la gestion des
utilisateurs, la modération du contenu, la résolution des problèmes techniques et la
mise en place de nouvelles fonctionnalités. Ils ont un accès étendu à l'application et
peuvent intervenir en cas de besoin.
```

**Internautes :**

```
Les internautes sont les visiteurs occasionnels de la plateforme qui ne sont pas
nécessairement des étudiants de l'institut. Ils peuvent accéder à certaines parties de
l'application, telles que les informations générales sur les clubs et les événements
publics, mais n'ont pas accès à toutes les fonctionnalités réservées aux utilisateurs
enregistrés.
```

###### 2.Modèle informationnel de contexte:

2.1.Diagramme de contexte:

**Figure 6 : “Diagramme de contexte”**

###### 3.Capture des besoins:

```
Dans cette partie, nous allons analyser les différents besoins fonctionnels et non
fonctionnels que notre système cherche à satisfaire.
```

3.1.Besoins fonctionnels:

```
Les besoins fonctionnels d'une application web de gestion des clubs dans une institution
comme l'ISIMM peuvent être variés, couvrant différentes fonctionnalités nécessaires pour une
gestion efficace des activités des clubs.
Voici une liste de besoins fonctionnels potentiels :
```

Gestion des Membres :

```
Enregistrement des membres : Permet aux étudiants de s'inscrire en tant que
membres d'un club en remplissant un Formulaire d'inscription avec des champs pour les
informations personnelles et le choix du club.
```

```
Profil utilisateur pour chaque membre avec des informations personnelles et
d'adhésion: Chaque membre dispose d'un profil personnel dont il dispose des
informations personnelles, des activités récentes, des clubs auxquels le membre est
inscrit.
```

```
Attribution de rôles et de responsabilités au sein des clubs : Permet aux
responsables de clubs d'attribuer des rôles et des responsabilités aux membres.
```

Gestion des Événements :

```
Création, modification et suppression d'événements : Les responsables de clubs
peuvent créer, modifier et supprimer des événements en remplissant un Formulaire de
création/modification avec des champs pour le titre, la date, l'heure, la description, et la
localisation de l'événement.
```

```
Calendrier des événements:Offre une vue d'ensemble des événements planifiés avec
des fonctionnalités de filtrage par club, date, et type d'événement.et de recherche.
```

Inscription des membres aux événements : Les membres peuvent s'inscrire à des
événements d'où on trouve un bouton d'inscription sur la page de l'événement, avec
confirmation et annulation.
Communication Interne :

```
Forum de discussion pour chaque club : Chaque club dispose d'un espace de
discussion interne.
```

```
Système de messagerie interne entre les membres : Les membres peuvent
s'envoyer des messages privés d'où on trouve une boîte de réception,notifications de
nouveaux messages.
```

```
Notifications en temps réel pour les annonces importantes : Les membres
reçoivent des notifications instantanées pour les annonces importantes.
```

Gestion des Ressources :

```
Partage de documents : Les membres peuvent partager des documents,
présentations et autres ressources liés aux activités du club entre les membres.
```

```
Section dédiée aux documents administratifs des clubs : Espace pour les
documents officiels du club avec un accès restreint aux responsables de clubs pour la
gestion des documents administratifs.
```

```
Galerie de médias pour les photos et vidéos des événements : Stocke et partage
des photos et vidéos des événements et pour cela on trouve une Interface pour
téléverser, visualiser et commenter des médias.
```

Suivi des Présences et Participations :

```
Enregistrement électronique de la participation des membres aux réunions et aux
événements : Les responsables de clubs peuvent enregistrer la participation des
membres aux réunions et aux événements en utilisant une interface pour enregistrer la
présence des membres avec des options de justification pour les absences.
```

Gestion des Projets :

```
Suivi des projets en cours : Permet aux clubs de suivre l'avancement de leurs projets
pour cela on utilise une liste des projets en cours avec des détails sur l'état
d’avancement.
```

```
Attribution de tâches et suivi de leur avancement : Les responsables de clubs
peuvent attribuer des tâches aux membres en utilisant une interface pour créer,
attribuer et suivre les tâches liées aux projets.
```

```
Stockage des documents liés aux projets : Espace dédié pour stocker les documents
liés aux projets.
```

Personnalisation des Profils :

```
Possibilité pour les membres de personnaliser leurs profils : Ajout d'informations
supplémentaires, de compétences, et de centres d'intérêt.
```

```
Affichage public des profils des membres : Permet aux membres de rendre
publiques certaines parties de leur profil pour favoriser la collaboration.
```

Statistiques et Rapports :

```
Rapports sur les activités des clubs, la participation des membres et les
événements organisés : Statistiques sur le nombre d'événements organisés, la
participation des membres, etc.
```

```
Statistiques pour évaluer l'engagement des membres : Mesure l'engagement des
membres dans les activités du club en le présentant par des graphiques et statistiques
sur la participation individuelle et collective.
```

```
Suivi financier des dépenses : Permet de suivre les dépenses liées aux activités des
clubs.
```

Administration et Gestion des Accès :

```
Attribution de droits d'accès spécifiques aux responsables de clubs et aux
administrateurs : Attribution de rôles avec des droits spécifiques pour différentes
parties de l'application.
```

```
Gestion des comptes utilisateurs : offrir la possibilité de créer de compte utilisateurs,
modification des Informations du compte, réinitialisation de mot de passe et
désactivation de compte.
```

```
Système de Votes et Sondages :
```

```
Possibilité de créer des sondages : permet aux responsables de clubs de créer des
sondages pour recueillir l'avis des membres.
```

```
Système de votes pour les décisions importantes au sein des clubs : Les membres
peuvent voter pour des décisions importantes au sein des clubs en utilisant une
interface de vote en implémentant une comptabilisation des résultats.
```

```
Intégration avec le Site de l'Institut :
```

```
Intégration de la plateforme dans le site web de l'institut : La plateforme est
accessible directement depuis le site web de l'institut en s’appuyant sur un lien direct vers
la plateforme depuis le site.
```

3.2.Besoins non fonctionnels:

```
Les besoins non fonctionnels sont des exigences qui définissent les caractéristiques
globales du système plutôt que ses fonctionnalités spécifiques. Voici quelques exemples de
besoins non fonctionnels pertinents pour une application web de gestion des clubs dans
une institution comme l'ISIMM
```

```
Performances :
```

```
Temps de Réponse : L'application doit offrir des temps de réponse rapides pour
assurer une expérience utilisateur fluide.
```

```
Évolutivité : La plateforme doit être capable de s'adapter à l'augmentation du
nombre d'utilisateurs et de données au fil du temps.
```

```
Sécurité :
```

```
Protection des Données : Assurer la confidentialité des informations personnelles
des membres et des données sensibles.
```

```
Authentification et Autorisation : Mettre en place des mécanismes robustes
d'authentification et d'autorisation pour protéger les zones sensibles de l'application.
```

```
Fiabilité :
```

```
Disponibilité : Garantir une disponibilité élevée de la plateforme, minimisant les
temps d'indisponibilité prévus.
```

```
Sauvegardes Régulières : Mettre en place des procédures de sauvegarde
régulières pour prévenir la perte de données.
```

```
Maintenabilité :
```

```
Modularité : Conception modulaire de l'application pour faciliter les mises à jour et
les extensions.
```

```
Documentation : Fournir une documentation exhaustive pour le code source et
l'utilisation de l'application.
```

Compatibilité :

```
Navigateurs : Assurer la compatibilité avec les principaux navigateurs web
(Chrome, Firefox, Safari, Edge).
```

```
Appareils : Garantir une expérience utilisateur cohérente sur différents types
d'appareils (ordinateurs de bureau, tablettes, smartphones).
```

Convivialité et Accessibilité :

```
Interface Utilisateur Intuitive : Concevoir une interface utilisateur conviviale et
intuitive pour faciliter la navigation.
```

```
Accessibilité : Assurer l'accessibilité de l'application conformément aux normes
WCAG pour les personnes en situation de handicap.
```

Performances du Système :

```
Optimisation : Optimiser les performances du système pour garantir une utilisation
fluide même dans des conditions de charge élevée.
```

Interopérabilité :

```
Intégrations : Assurer l'interopérabilité avec d'autres systèmes utilisés dans
l'institution si nécessaire.
```

Conformité aux Normes :

```
Conformité Légale : Respecter les normes et réglementations légales relatives à la
gestion des données et de la confidentialité.
```

Évolutivité :

```
Évolutivité Technique : Concevoir l'application de manière à pouvoir ajouter de
nouvelles fonctionnalités et s'adapter aux évolutions futures.
```

Esthétique et Design :

```
Carte Graphique : Respecter la charte graphique de l'institution pour une identité
visuelle cohérente.
```

Support et Formation :

```
Support Utilisateur : Mettre en place un système de support utilisateur efficace.
```

```
Formation : Fournir des sessions de formation pour les administrateurs et les
utilisateurs clés.
```

```
En intégrant ces besoins non fonctionnels dans la conception de l'application,
vous pouvez vous assurer que celle-ci répondra aux attentes en termes de
performances, sécurité, fiabilité et convivialité.
```

###### 4.Spécification des besoins:

```
Cette phase consiste à comprendre le contexte du système. Il s'agit de déterminer les
fonctionnalités et les acteurs les plus pertinents, de préciser les risques les plus critiques et
d'identifier les cas d'utilisation initiaux.
```

**4.1.Diagramme de cas d’utilisation global:**

```
Figure 7 : “ Diagramme de cas d’utilisation global”
```

**4.2.Diagrammes de cas d’utilisation détaillés:**

```
4.2.1.Diagramme de cas d’utilisation détaillé de l’acteur “internaute”:
```

```
La figure 8 illustre les fonctionnalités à fournir à l’acteur « internaute » après
l’authentification. Un « internaute » peut consulter les informations publiques sur les
clubs et les événements, s’inscrire aux événements publics organisés par les clubs,
soumettre une demande d'adhésion à un club spécifique. Aussi, il a la possibilité de
communiquer avec le responsable de club via un système de chat.
```

**Figure 8 : “Diagramme de cas d’utilisation détaillé “Internaute” ”**

**Description textuelle : Cas d’utilisation : Demander de rejoindre club :**

###### Description : Le responsable du club demande d’ajouter

###### ou modifier ou annuler un événement

###### Acteur : Internaute

###### Evénement

###### déclencheur :

###### L’internaute souhaite rejoindre un club et

###### soumet sa demande via la plateforme de

###### gestion des clubs.

###### Scénario principal : 1 - L’internaute se connecte au plateforme de

###### gestion des clubs.

###### 2 - L’internaute le club auquel il souhaite

###### adhérer

###### 3 - L’internaute sélectionne le club souhaité et

###### choisi l’option « demander de rejoindre club »

###### 4 - Le système affiche un formulaire de

###### demande à remplir , comprenant des champs

###### pour les informations pertinentes telles que le

###### nom, l'adresse e-mail, le programme

###### d'études, etc. Cet écran est inclus dans ce cas

###### d'utilisation et est traité dans le scénario

###### d'inclusion "Remplir formulaire".

**Tableau 2 : Description textuelle : Cas d’utilisation : Demander de joindre club**

###### 5 - L'étudiant remplit le formulaire avec ses

###### informations et soumet sa demande.

###### Scénario

###### d’inclusion :Remplir

###### formulaire

###### 1 - Le système affiche un formulaire de

###### demande à remplir lorsque l'étudiant

###### sélectionne l'option "Demander de

###### Rejoindre Club".

###### 2 - L'internaute saisit les informations

###### requises dans les champs du formulaire

###### et les soumet.

###### 3 - Le système traite les informations

###### soumises et enregistre la demande dans

###### la base de données du système.

###### Scenario

###### d’extension :Faire

###### un interview :

###### 1 - Après avoir reçu la demande de

###### l’internaute, le responsable du club peut

###### choisir d'étendre le processus en

###### invitant l'étudiant à un entretien pour

###### discuter de sa demande.

###### 2 - Le responsable du club contacte

###### l'internaute pour fixer un rendez-vous

###### pour l'interview.

###### 3 - L'interview est mené pour évaluer

###### l'adéquation de l’internaute avec le club

###### et discuter de son engagement

###### potentiel.

###### Précondition : Le club est répertorié dans la plateforme

###### Post condition : L'internaute a soumis sa demande pour

###### rejoindre le club, qui sera examinée par le

###### responsable du club.

**4.2.2.Diagramme de cas d’utilisation détaillé de l’acteur “responsable club”:**

```
La figure 9 illustre les fonctionnalités à fournir à l’acteur « responsable
club » après l’authentification. Un « responsable club » peut publier des
événements et des activités planifiés par son club sur la plateforme, communiquer
avec les membres de son club via un système de messagerie intégré et il a aussi la
possibilité de réserver des salles ou des matériels nécessaires pour les activités et
événements organisés par son club.
```

**Figure 9 : “Diagramme de cas d’utilisation détaillé “Responsable d** e **Club” ”**

**Description textuelle : Cas d’utilisation : gérer évènement :**

###### Description : Le responsable du club demande d’ajouter

###### ou modifier ou annuler un événement

###### Acteur : Responsable du club

###### Evénement

###### déclencheur :

###### Le responsable du club souhaite créer,

###### modifier ou supprimer un événement

###### organisé par son club.

###### Scénario principal : 1 - Le responsable du club accède à la

###### fonctionnalité de gestion des événements

###### dans le tableau de bord du club.

###### 2 - Le système affiche une liste des

###### événements actuels du club, ainsi que des

###### options pour créer un nouvel événement ou

###### modifier ou supprimer des événements

###### existants.

###### 3 - Le responsable du club sélectionne l'option

###### correspondant à l'action qu'il souhaite

###### effectuer : créer, modifier ou supprimer un

###### événement.

###### 4 - Si le responsable choisit de créer un nouvel

###### événement :

###### . Le système affiche un formulaire permettant

###### de saisir les détails de l'événement, tels que le

###### titre, la date, l'heure, le lieu, la description,

###### etc.

###### . Le responsable du club remplit le formulaire

###### avec les informations nécessaires et soumet la

###### demande de création de l'événement.

###### .Le système enregistre l'événement dans la

###### base de données du club.

###### 5 - Si le responsable choisit de modifier un

###### événement existant :

###### .Le système affiche les détails de l'événement

###### sélectionné, ainsi qu'un formulaire pré-rempli

###### avec ces informations.

###### . Le responsable du club met à jour les

###### champs nécessaires dans le formulaire et

###### soumet les modifications.

###### .Le système met à jour les informations de

###### l'événement dans la base de données du club.

###### 6 - Si le responsable choisit de supprimer un

###### événement :

###### . Le système demande une confirmation avant

###### de procéder à la suppression.

###### .Après confirmation, le système supprime

###### l'événement de la base de données du club.

**Tableau 3 : Description textuelle : Cas d’utilisation : gérer évènement**

4.3.Diagrammes de séquence acteur-système:

Les diagrammes de séquences permettent de montrer les interactions des éléments du
système entre eux et avec les acteurs.

```
4.3.1.Diagramme de séquence “demander de rejoindre club”:
```

```
Figure 10 : “Diagramme de Séquence “demande de rejoindre Club” ”
```

###### Précondition : Le responsable du club doit être connecté à la

###### plateforme de gestion des clubs et avoir accès

###### au tableau de bord administratif du club

###### Le responsable du club doit disposer des

###### autorisations nécessaires pour gérer les

###### événements du club. Cela peut inclure des

###### privilèges spécifiques définis par les

###### administrateurs de la plateforme.

###### Post condition : Les événements du club sont gérés avec

###### succès, avec les mises à jour nécessaires

###### apportées à la base de données du club.

###### Contrainte : Le Responsable doit être inscrit au

###### plateforme.

```
4.3.2.Diagramme de séquence “responsable club”:
```

**Figure 11 : “Diagramme de Séquence “Responsable d** e **Club” ”**

###### 5.Choix teChniques:

```
Pour le côté front-end nous allons utiliser la bibliothèque React JS et le framework Laravel
pour le côté back-end.
```

5.1. Bibliothèque React:

```
ReactJS est considéré comme une bibliothèque plutôt que comme un framework. C’est une
bibliothèque JavaScript open source développée par Facebook depuis 2013. Le but
principal de cette bibliothèque est de faciliter la création d'application web monopage, via la
création de composants réutilisables et dépendants d’état. Nous avons opté pour la
bibliothèque React JS pour les raisons suivantes :
```

- La Flexibilité : Avec React, la création d’applications est simplifiée grâce à son API qui
  permet une utilisation facile des composants et à l’utilisation d’un DOM virtuel.
- Performance : React a été conçue pour offrir des performances élevées grâce à la mise
  en œuvre d’un DOM virtuel ce qui rend les applications complexes extrêmement rapides.

```
La figure ci dessous présente un diagramme qui compare l’utilisation des frameworks JS
les plus utilisés
```

```
Figure 12 : “ Diagramme de comparaison entre les Frameworks JS”
```

5.2. Framework Laravel :

```
Laravel est un framework web PHP open-source gratuit, créé par Taylor Otwell depuis
2011 et destiné au développement d'applications web suivant le modèle architectural
modèle – vue – contrôleur (MVC). Nous avons opté pour la framework Laravel pour les
raisons suivantes :
```

- Sécurité : Laravel est l’un des frameworks les plus robustes et sécurisés. Parmi les
  mesures de sécurité qu’il offre : cryptage des mots de passe lors de l'enregistrement dans
  la BD, protection contre les injections SQL et protection contre les attaques de type CSRF
  (Cross-site request forgery).
- Performances améliorées : Laravel supporte divers outils pour fournir une excellente
  performance aux applications web tels que Memcached et Redis, systèmes de cache
  performant permettant de stocker pour un temps limité des données sur la mémoire vive,
  ce qui permet de renvoyer directement une donnée à l’utilisateur sans avoir besoin
  d'accéder à la base de données.

```
La figure ci dessous présente une comparaison entre les frameworks PHP les plus utilisées
```

**Figure 13 : “Comparaison Entre les Frameworks PHP”**

###### Conclusion:

Dans ce chapitre, nous avons identifié les acteurs, les besoins fonctionnels et non-
fonctionnels de notre système à l’aide de diagrammes de cas d’utilisation et de séquence
acteur système. Aussi nous avons présenté le choix technique des frameworks à utiliser.
Le troisième chapitre sera consacré à la conception de notre application.

###### CHAPITRE III : Conception

INTRODUCTION :

```
Dans ce chapitre nous allons entamer une partie importante du développement de
l’application qui constitue un pont entre la spécification et la réalisation. Nous commencerons par la
présentation de l'architecture générale de notre application, ensuite la conception générale puis la
conception détaillée comprenant les vues statiques via les diagrammes de classes. Enfin nous
clôturerons ce chapitre par quelques fonctionnalités de l'application à l'aide des maquettes.
```

###### 1.Architecture applicative:

Après avoir fait le choix de la méthodologie 2TUP, la démarche de conception sera en
adéquation avec l'architecture de l'application Avant de développer notre application, il est
indispensable de choisir un modèle de conception (pattern design). Parmi les patrons les plus
connus, nous mentionnons l’architecture 3-tiers et le patron Modèle-Vue-Contrôleur (MVC).

1.1.Architecture physique:Architecture 3-tiers

```
Ce modèle d’architecture, décrit par la figure 13, se décompose en trois niveaux logiques
bien distincts qui ont chacune un rôle bien défini :
```

- La couche de présentation correspond à l’interface utilisateur. Son rôle est d’afficher les
  données et de permettre à l’utilisateur final d’interagir avec ces dernières.
- La couche métier est en charge d’appliquer et de respecter les règles métiers (ou actes
  de gestion). Avec ce modèle d’architecture, la logique applicative et la sécurité sont
  implémentées dans cette couche.
- **La couche d’accès aux données** , quant à elle, assure la persistance des données qui
  doivent être conservées.

**Figure 14 : “Architecture 3-tiers”**

1.2.Architecture logique: MVC

L'architecture Modèle/Vue/Contrôleur (MVC) est une façon d'organiser une interface
graphique d'un programme. Elle consiste à distinguer trois entités distinctes qui sont, le
modèle, la vue et le contrôleur ayant chacun un rôle précis dans l'interface.

La figure 1 5 décrit l’architecture MVC. Dans l'architecture MVC, les rôles des trois entités
sont les suivants :

- Le modèle : il gère les données de site, son rôle est de récupérer les informations dans
  la base de données, de les organiser et de les assembler pour qu'elles puissent ensuite
  être traitées par le contrôleur
- La vue : elle représente l’interface utilisateur, sa première tâche est d'afficher les
  données qu'elle a récupérées auprès du modèle. Sa seconde tâche est de recevoir toutes
  les actions de l'utilisateur. Ses différents événements sont envoyés au contrôleur.
- Le contrôleur : cette partie est chargée de la synchronisation du modèle et de la vue.
  C'est en quelque sorte l'intermédiaire entre le modèle et la vue : le contrôleur demande au
  modèle les données, les analyser, prendre des décisions et finalement les déléguer à la
  vue.

```
Figure 15 : “ L’architecture du Modèle MVC ”
```

**1.3.Architecture de l’application:**

En utilisant une architecture 3-tiers, l'application est organisée de manière modulaire
et évolutive, ce qui permet une séparation claire des responsabilités entre les différentes
couches et une meilleure maintenabilité du code.où le front-end est composé d'une
template et le back-end est formé de routing, controlling et model :

```
Tier Front-End (Présentation) :
```

```
Le tier front-end est responsable de l'interface utilisateur de l'application, c'est-à-
dire ce que les utilisateurs voient et avec quoi ils interagissent. Dans ce cas, le
front-end de l'application est composé d'une template préconstruite,
probablement une combinaison de HTML, CSS et JavaScript, qui fournit une
structure de base pour l'interface utilisateur. Cette template peut inclure des
éléments tels que des pages, des formulaires, des boutons, etc., qui sont stylisés
et organisés pour offrir une expérience utilisateur cohérente et attrayante.
```

```
Tier Back-End (Logique Métier) :
```

```
Le tier back-end est responsable de la logique métier de l'application, y compris
le traitement des requêtes des utilisateurs, la manipulation des données et la
gestion des opérations de base de données. Dans ce cas, le back-end de
l'application est structuré selon une approche MVC (Modèle-Vue-Contrôleur) :
```

```
Modèle (Model) : Le modèle représente la structure des données de l'application.
Il est responsable de la gestion des interactions avec la base de données et de la
manipulation des données. Les modèles peuvent inclure des classes ou des
fonctions qui définissent la structure des données et fournissent des méthodes
pour effectuer des opérations CRUD (Create, Read, Update, Delete) sur les
données.
```

```
Vue (View) : Bien que la template front-end fournisse une partie de la vue, le
back-end peut également générer des vues dynamiques en utilisant des modèles
de rendu côté serveur. Ces vues peuvent être rendues à la volée en fonction des
données récupérées du modèle et des actions de l'utilisateur.
```

```
Contrôleur (Controller) : Le contrôleur agit comme un intermédiaire entre les
vues et les modèles. Il est responsable de la gestion des requêtes HTTP, de la
coordination des interactions entre les vues et les modèles, et de l'exécution de la
logique métier de l'application. Les contrôleurs utilisent les routes définies pour
acheminer les requêtes vers les actions appropriées et retourner les réponses
correspondantes.
```

```
Tier Base de Données (Persistance des Données) :
```

```
Le tier base de données est responsable de la persistance des données de
l'application. Dans ce cas, une base de données relationnelle telle que MySQL est
utilisée pour stocker les informations sur les clubs, les membres, les
événements, etc. La base de données est gérée par le modèle du back-end, qui
effectue les opérations de lecture et d'écriture des données en fonction des
besoins de l'application.
```

###### 2.Conception de base de données:

La conception d'une base de données est l'organisation des données selon un modèle. Elle
aide à déterminer comment les données doivent être stockées et comment elles sont liées. Donc,
Nous commençons par présenter le modèle conceptuel de données (MCD) et par la suite le
modèle Logique de données (MLD).

2.1.MCD:

Un MCD décrit les différentes entités ainsi que les relations qui existent entre elles.
La figure 16 illustre le modèle conceptuel de notre base de données. Le tableau ci-dessous
donne les détails de description de chaque entité.

**Figure 16 : “ Modèle Conceptuel des Données”**

**Tableau 4 : Tableau comparatif entre les solutions existantes**

2.2.MLD:

Un modèle MCD peut être organisé selon différents modèles logiques de données. Dans
notre projet, nous avons opté pour le modèle relationnel qui répond bien à nos besoins non
fonctionnels. En appliquant les règles de transformations du modèle E/A vers un modèle
relationnel, nous obtenons le schéma relationnel suivant:

Administrateur (Admin_ID , nom , prénom, email) ;

Responsable du club (respon_ID , nom_club,Role,Num_tel ) ;

Club ( Club_ID , nom_Club, Date_fond , Nb_membre );

##### Entités Description Attributs et types

###### Administrateur Elle contient toutes les

```
informations de
l’administrateur
```

- Admin_id : Number
- Nom : string
- Prenom : string
- Email : string

###### Responsable du

###### club

```
Elle hérite la classe «
Etudiant » et contient les
attributs
supplémentaires relatives
aux responsable du club.
```

- Respon_id : number
- Num_tel : Number
- Role : string
- nom_club :string

###### Evènement Elle contient^ toutes^ les

```
informations des
Evènements.
```

- Event_id :number
- Event_name : string
- Event_date :Date
- Event_place : string
- Facture : float

###### Club^

```
Elle contient toutes les
informations des clubs
```

- Club_id : Number
- Nom :String
- Date_fond :Date
- nb_membre

###### Internaute Elle hérite la classe «

```
Etudiant » et contient les
attributs
supplémentaires relatives
à l’internaute.
```

- inter_id :number

###### Etudiant^

```
Elle Contient toutes les
informations des étudiants
```

- Etud_id :Number
- Nom :string
- prenom :string
- email :string
- psswd :string

###### Salle Elle contient toutes les

```
informations des salles
```

- Num_salle :Number
- Nom_salle : string

###### Activité Elle hérite la classe «

```
Evènement » et contient
les attributs
supplémentaires relatives
aux activités.
```

- Nom_activ : string
- Couts :float

Evenement (Event_ID , Event_name , event_Date , Event_place , Nom_activité );

Etudiant ( Etud_ID , Nom , prénom ,Email , password ) ;

Internaute (Inter_ID ) ;

Diriger (#Club_ID , #Respon_ID);

Adhérer (#Event_ID , #Etud_ID);

Gèrer (#Respon_ID , #Event_ID);

Participer (#Club_ID,#Etud_ID);

Reserver (#Num_salle , # Event_ID);

###### 3.Conception logicielle:

Dans La conception logicielle détaillée nous allons donner une vue statique avec le diagramme de
classe et une vue dynamique avec le diagramme de séquence

3.1.Vue statique: **Diagramme de classe d’analyse** :

**Figure 17 : “ Diagramme de Classe”**

**Diagramme de classe de conception:**

**Figure 18 : “Diagramme de classe de conception”**

**3.2.Vue dynamique: diagramme de séquence**

Dans cette partie nous présentons le déroulement des traitements et des interactions entre

les différentes couches via des diagrammes de séquence.

Figure 1 9 **: “Diagramme de séquence ”**

###### 4.Conception graphique:

4.1.Maquettage:

Le maquettage est une étape indispensable, il permet de donner une idée sur le site et sur
les différentes interfaces sous forme de schéma. Dans ce qui suit, nous allons illustrer
quelques maquettes de notre application :

**4.1.1. Interface d'Information :**

```
Cette interface vise à fournir des informations essentielles sur l'institut, telles que
l'adresse, l'adresse e-mail et le numéro de téléphone.
```

**Figure 20 : “interface de plus d’information ”**

**4.1.2.Interface de Choix entre s'inscrire et se connecter :**

Cette interface permet aux utilisateurs de choisir entre se connecter à un compte existant ou
de s’inscrire.

**Figure 21 : “interface de choix entre se connecter et s’inscrire ”**

D’où cette interface nous ramène à l’interface de l’inscription ou bien celle de
connexion :

**Figure 22 : “interface d’inscription”**

**Figure 23 : “interface de connexion”**

**4.1.3. Interface de Présentation des clubs et des Responsables des Clubs :**

Cette interface permet aux utilisateurs de découvrir les clubs, les responsables et
leurs informations.

**Figure 24 : “interface des clubs et responsables”**

###### 5.Conclusion :

Dans ce chapitre, nous avons détaillé les principales étapes de la conception de notre
projet.

En effet, nous avons commencé par présenter l’architecture générale de notre
application. Ensuite, nous avons détaillé la conception de la base de données via le modèle
conceptuel de données et le modèle relationnel. Puis nous sommes passés à la conception
logicielle en donnant le diagramme de classe qui détaille la vue statique et des diagrammes
de séquence qui détaillent la vue dynamique de notre système. Enfin nous avons présenté
la conception graphique des interfaces utilisateur en donnant les différents liens de
navigation entre elles.

###### Conclusion générale :

La création de la plateforme de gestion des clubs étudiants à l'ISIMM marque le début d'une
nouvelle ère d'engagement étudiant, de collaboration et d'épanouissement au sein de notre
communauté universitaire. Tout au long de ce projet, nous avons travaillé avec détermination pour
développer une solution innovante et pratique qui répond aux besoins diversifiés de nos étudiants,
de nos responsables de clubs et de nos administrateurs.

En rassemblant les membres de notre communauté à travers une plateforme numérique unifiée,
nous aspirons à renforcer les liens sociaux, à encourager la créativité et l'initiative, et à favoriser
un environnement d'apprentissage dynamique et inclusif. La plateforme offre un espace où
chacun peut exprimer ses intérêts, partager ses idées et contribuer à la richesse et à la diversité
de la vie universitaire.

À mesure que nous avançons dans l'implémentation et le déploiement de cette plateforme, nous
restons déterminés à garantir son accessibilité, sa convivialité et sa pertinence pour l'ensemble de
notre communauté. Nous sommes convaincus que cette initiative aura un impact positif durable
sur la qualité de vie étudiante, sur l'engagement académique et sur le développement personnel
de nos membres.

En conclusion, la plateforme de gestion des clubs étudiants incarne notre engagement envers
l'excellence, l'innovation et l'épanouissement des étudiants à l'Institut ISIMM. Nous sommes
impatients de voir cette initiative prendre vie et de continuer à travailler ensemble pour créer un
environnement universitaire dynamique et inspirant pour tous.
