
# Énoncé du projet Python : Simulation d'une usine de fabrication de jouets (avec explications internes)

---

## Introduction

Dans le cadre de votre cours de programmation Python, vous devez développer un projet simulant une usine de fabrication de jouets (par exemple, des voitures miniatures). L'objectif est de créer un programme qui modélise une chaîne de production où les jouets passent par différentes étapes (stations) avant d'être finalisés. Vous devrez gérer des goulets d'étranglement, des erreurs de production (produits défectueux), et des pannes imprévues des stations, tout en produisant un rapport final pour analyser les performances.

Cet énoncé est conçu pour expliquer non seulement ce qu'il faut faire, mais aussi **comment le faire**, en détaillant le fonctionnement interne des mécanismes du code, les choix d'implémentation, et les concepts Python utilisés. Vous devrez écrire le code vous-même, mais les explications fournies ici vous guideront pour comprendre les rouages internes et prendre des décisions éclairées.

---

## Objectifs pédagogiques

À la fin de ce projet, vous serez capable de :
1. Structurer un programme complexe en utilisant la **programmation orientée objet (POO)**, avec des classes bien définies et des responsabilités claires.
2. Implémenter et utiliser des structures de données comme les **files d'attente (queue)** et les **piles (stack)**, en comprenant leur fonctionnement interne (FIFO vs LIFO).
3. Exploiter des outils de la bibliothèque standard Python, notamment **`itertools`** (pour générer des séquences), **`logging`** (pour tracer les événements), et les fonctions fonctionnelles (**`map`**, **`filter`**, **`reduce`**).
4. Utiliser des **expressions régulières (regex)** pour valider et analyser des données, en comprenant comment les motifs fonctionnent.
5. Implémenter une **récursivité** simple pour gérer des processus répétitifs, en comprenant la pile d'appels.
6. Simuler des événements aléatoires (par exemple, pannes, défauts) et comprendre comment les intégrer dans une simulation.

---

## Contexte du projet

Vous devez simuler une usine qui fabrique des jouets. Chaque jouet passe par les étapes suivantes, dans l'ordre :
1. **Assemblage** : Les pièces du jouet sont assemblées.
2. **Peinture** : Le jouet est peint.
3. **Contrôle qualité** : Le jouet est inspecté pour détecter d'éventuels défauts.
4. **Emballage** : Les jouets validés sont emballés et prêts à être expédiés.

Chaque étape est représentée par une **station** qui peut traiter un produit à la fois. Les stations ont des temps de traitement variables, ce qui peut créer des goulets d'étranglement (par exemple, si la peinture est plus lente que l'assemblage, une file d'attente se forme). De plus, certaines stations peuvent tomber en panne de manière aléatoire, bloquant temporairement le traitement. Enfin, certains jouets peuvent être détectés comme défectueux au contrôle qualité et devront être retraités.

---

## Structure générale du programme

Votre programme sera structuré autour de plusieurs classes principales, chacune avec des responsabilités spécifiques. Voici un aperçu des classes et de leur rôle, avec des explications détaillées sur leur fonctionnement interne dans les sections suivantes :
- **Classe `Produit`** : Représente un jouet fabriqué, avec un identifiant unique, un statut, un temps total de production, et un suivi des étapes effectuées.
- **Classe `Station`** : Représente une étape de production, avec une file d'attente pour gérer les produits en attente, un temps de traitement variable, et la possibilité de tomber en panne.
- **Classe `PileDefauts`** : Gère une pile de produits défectueux, avec un mécanisme pour les renvoyer à une étape précédente.
- **Classe `Usine`** : Orchestre toute la simulation, en gérant les stations, la pile des défauts, et les produits finis, et produit un rapport final.

Chaque section ci-dessous explique en détail comment implémenter ces classes, avec un focus sur les mécanismes internes et les concepts utilisés.

---

## Description détaillée du projet 

### 1. Scénario

Vous devez simuler une usine qui fabrique des jouets. Chaque jouet passe par les étapes suivantes, dans l'ordre :
1. **Assemblage** : Temps de traitement moyen de 2 secondes (variable entre 1 et 3 secondes).
2. **Peinture** : Temps de traitement moyen de 3 secondes (variable entre 1.5 et 4.5 secondes, plus lent que l'assemblage, donc susceptible de créer une file d'attente).
3. **Contrôle qualité** : Temps de traitement moyen de 1 seconde (variable entre 0.5 et 1.5 secondes). Probabilité de 20 % qu'un jouet soit défectueux.
4. **Emballage** : Temps de traitement moyen de 1 seconde (variable entre 0.5 et 1.5 secondes).

### 2. Fonctionnalités attendues

Votre programme doit inclure les fonctionnalités suivantes, avec des explications détaillées sur leur fonctionnement interne et leur implémentation.

#### 2.1. Gestion des produits

**Objectif** : Représenter chaque jouet comme un objet avec des données et des comportements.

**Fonctionnement interne** :
- Chaque produit est un objet avec un identifiant unique sous la forme `"TOY-XXX-COLOR"`, où `XXX` est un numéro de série (par exemple, 001, 002) et `COLOR` est une couleur (par exemple, RED, BLUE, GREEN).
- L'identifiant est généré automatiquement lors de la création du produit, en combinant un numéro de série (incrémenté automatiquement) et une couleur choisie aléatoirement.
- Le produit a un statut (`"en cours"`, `"fini"`, ou `"rejeté"`) qui est mis à jour au fil de la simulation.
- Le produit garde une trace de son temps total de production (en secondes simulées) et des étapes effectuées (par exemple, `["assemblage", "peinture"]`).

**Implémentation** :
- Créez une classe `Produit` avec un constructeur (`__init__`) qui prend un numéro de série et une couleur, et initialise l'identifiant, le statut, le temps total, et la liste des étapes effectuées.
- Ajoutez une méthode `__str__` pour faciliter l'affichage du produit (par exemple, `"TOY-001-RED (Status: en cours, Temps: 5.2s)"`).
- Ajoutez une méthode pour valider l'identifiant avec une regex (par exemple, `r"TOY-\d{3}-[A-Z]+"`) pour s'assurer que le format est correct.
- Ajoutez une méthode pour extraire le numéro de série avec une regex (par exemple, `r"TOY-(\d{3})-[A-Z]+"`, en utilisant `re.search` et `match.group(1)`).

**Exemple de mécanisme interne** : Quand un produit est créé, son identifiant est généré avec un formatage de chaîne (par exemple, `f"TOY-{numero_serie:03d}-{couleur.upper()}"`), où `:03d` garantit que le numéro de série a toujours 3 chiffres (par exemple, `001` au lieu de `1`). La validation avec regex utilise `re.match` pour vérifier que l'identifiant correspond au motif attendu, et retourne `True` ou `False`.

---

#### 2.2. Simulation du flux de production

**Objectif** : Simuler le passage des produits à travers les stations, avec des files d'attente et des temps de traitement variables.

**Fonctionnement interne** :
- Chaque station a une file d'attente (queue) pour stocker les produits en attente, implémentée avec `collections.deque`.
- Chaque station a un temps de traitement moyen (par exemple, 2 secondes pour l'assemblage), mais ce temps varie aléatoirement (par exemple, entre 50 % et 150 % du temps moyen, calculé avec `random.uniform`).
- Les produits passent d'une station à la suivante dans l'ordre, sauf en cas de défaut ou de panne.
- La simulation est gérée par une boucle principale qui vérifie l'état de toutes les files d'attente et de la pile des défauts, et continue tant qu'il reste des produits à traiter.

**Implémentation** :
- Créez une classe `Station` avec un constructeur qui prend un nom (par exemple, `"assemblage"`) et un temps de traitement moyen.
- Ajoutez un attribut `file_attente` initialisé avec `collections.deque()` pour stocker les produits en attente.
- Ajoutez une méthode `ajouter_produit` qui ajoute un produit à la fin de la file d'attente avec `file_attente.append(produit)` et enregistre un message dans les logs.
- Ajoutez une méthode `traiter_produit` qui :
  - Vérifie si la file d'attente est vide (sinon retourne `None`).
  - Retire le produit en tête de la file avec `file_attente.popleft()`.
  - Calcule un temps de traitement aléatoire (par exemple, `random.uniform(temps_moyen * 0.5, temps_moyen * 1.5)`).
  - Simule un délai avec `time.sleep(temps / 10)` (pour accélérer la simulation).
  - Met à jour le produit (incrémente son temps total, ajoute l'étape à `etapes_effectuees`).
  - Retourne le produit traité.
- Créez une classe `Usine` avec un dictionnaire de stations (par exemple, `{"assemblage": Station("assemblage", 2), ...}`) et une méthode pour simuler le flux.

**Exemple de mécanisme interne** : Quand un produit termine l'assemblage, il est retiré de la file d'attente de l'assemblage et ajouté à la file d'attente de la peinture. Si la peinture est plus lente, sa file d'attente se remplira progressivement, simulant un goulet d'étranglement. La boucle principale de la simulation vérifie chaque station à tour de rôle, traite un produit si possible, et le passe à la station suivante.

---

#### 2.3. Gestion des défauts

**Objectif** : Gérer les produits défectueux détectés au contrôle qualité, en les renvoyant à une étape précédente pour correction.

**Fonctionnement interne** :
- Au contrôle qualité, un produit a une probabilité de 20 % d'être défectueux, déterminée avec `random.random() < 0.2`.
- Les produits défectueux sont empilés dans une pile (stack) pour être traités dans l'ordre inverse (LIFO).
- Chaque produit défectueux a un nombre de tentatives de correction, qui est incrémenté à chaque renvoi. S'il dépasse une limite (par exemple, 3), le produit est marqué comme `"rejeté"`.
- Un produit défectueux est renvoyé à une étape précédente (par exemple, assemblage ou peinture, choisi aléatoirement avec `random.choice`).

**Implémentation** :
- Créez une classe `PileDefauts` avec un attribut `pile` initialisé comme une liste vide.
- Ajoutez une méthode `ajouter_defaut` qui ajoute un produit à la pile avec `pile.append(produit)` et enregistre un message dans les logs.
- Ajoutez une méthode `traiter_defaut` qui :
  - Vérifie si la pile est vide (sinon retourne `None`).
  - Retire le produit au sommet de la pile avec `pile.pop()`.
  - Incrémente le nombre de tentatives du produit.
  - Si le nombre de tentatives dépasse la limite, marque le produit comme `"rejeté"` et enregistre un message `ERROR` dans les logs.
  - Sinon, renvoie le produit à une étape précédente (par exemple, assemblage ou peinture) en l'ajoutant à la file d'attente de la station correspondante.
- Dans la classe `Usine`, intégrez la gestion des défauts dans la simulation, en vérifiant après le contrôle qualité si un produit est défectueux.

**Exemple de mécanisme interne** : Quand un produit est détecté comme défectueux, il est ajouté à la pile des défauts. La boucle principale de la simulation vérifie régulièrement la pile et traite le produit au sommet en le renvoyant à une étape précédente. Si un produit échoue 3 fois, il est marqué comme `"rejeté"` et ajouté à la liste des produits finis (pour être inclus dans les statistiques finales).

---

#### 2.4. Simulation de pannes

**Objectif** : Simuler des pannes aléatoires des stations, qui bloquent temporairement le traitement et augmentent les files d'attente.

**Fonctionnement interne** :
- Chaque station a une probabilité de panne (par exemple, 5 %, déterminée avec `random.random() < 0.05`) à chaque tentative de traitement.
- Quand une panne se produit, la station est bloquée pendant une durée aléatoire (par exemple, entre 5 et 10 secondes, déterminée avec `random.uniform`).
- Pendant une panne, aucun produit n'est traité, et la file d'attente de la station continue de se remplir.
- La panne est gérée par un compteur de temps restant, qui est décrémenté à chaque tour de la simulation. Quand il atteint 0, la panne est résolue.

**Implémentation** :
- Dans la classe `Station`, ajoutez des attributs pour gérer les pannes : `en_panne` (booléen), `temps_restant_panne` (temps restant en secondes simulées), `proba_panne` (probabilité de panne), `duree_panne_min` et `duree_panne_max` (durées de panne).
- Ajoutez une méthode `verifier_panne` qui :
  - Si la station est déjà en panne, décrémente `temps_restant_panne`. Si `temps_restant_panne <= 0`, met `en_panne` à `False` et enregistre un message dans les logs.
  - Si la station n'est pas en panne, tire un nombre aléatoire avec `random.random()`. Si ce nombre est inférieur à `proba_panne`, met `en_panne` à `True`, choisit une durée aléatoire avec `random.uniform(duree_panne_min, duree_panne_max)`, et enregistre un message dans les logs.
- Modifiez la méthode `traiter_produit` pour appeler `verifier_panne` avant de traiter un produit, et retourner `None` si la station est en panne.

**Exemple de mécanisme interne** : Quand la station de peinture tombe en panne, elle cesse de traiter les produits, et sa file d'attente commence à se remplir. La boucle principale de la simulation continue de vérifier l'état de la panne à chaque tour, et quand la panne est résolue, la station reprend le traitement normal.

---

#### 2.5. Enregistrement des événements

**Objectif** : Enregistrer tous les événements importants dans un fichier de logs pour suivre le déroulement de la simulation.

**Fonctionnement interne** :
- Le module `logging` est configuré pour écrire dans un fichier `usine.log` avec un format qui inclut un horodatage, un niveau de sévérité, et un message.
- Les niveaux de sévérité utilisés sont `INFO` (informations générales, comme le traitement d'un produit), `WARNING` (avertissements, comme une panne ou un défaut), et `ERROR` (erreurs graves, comme le rejet d'un produit).
- Chaque appel à `logging.info`, `logging.warning`, ou `logging.error` ajoute une ligne au fichier de logs.

**Implémentation** :
- Configurez le logging au début du programme avec `logging.basicConfig`, en spécifiant le fichier de sortie (`filename='usine.log'`), le niveau minimum (`level=logging.INFO`), et le format des messages (`format='%(asctime)s - %(levelname)s - %(message)s'`).
- Ajoutez des appels à `logging` dans toutes les méthodes pertinentes, par exemple :
  - `logging.info` dans `Station.ajouter_produit` pour indiquer qu'un produit a été ajouté à la file d'attente.
  - `logging.info` dans `Station.traiter_produit` pour indiquer qu'un produit a été traité.
  - `logging.warning` dans `PileDefauts.ajouter_defaut` pour indiquer qu'un produit est défectueux.
  - `logging.error` dans `PileDefauts.traiter_defaut` pour indiquer qu'un produit a été rejeté.
  - `logging.warning` dans `Station.verifier_panne` pour indiquer qu'une panne a commencé ou s'est terminée.

**Exemple de mécanisme interne** : Quand un produit termine l'étape d'assemblage, un message comme `"2025-03-11 14:32:15,125 - INFO - Produit TOY-001-RED a terminé l'étape d'assemblage en 1.82s"` est ajouté au fichier `usine.log`. Ces messages permettent de retracer tout le déroulement de la simulation, y compris les pannes et les défauts.

---

#### 2.6. Analyse des données

**Objectif** : Produire un rapport final qui analyse les performances de l'usine à la fin de la simulation.

**Fonctionnement interne** :
- À la fin de la simulation, tous les produits (finis ou rejetés) sont stockés dans une liste (par exemple, `produits_finis` dans `Usine`).
- Les fonctions `map`, `filter`, et `reduce` sont utilisées pour extraire et analyser les données de cette liste.
- Les résultats sont affichés dans la console sous forme de statistiques claires.

**Implémentation** :
- Dans la classe `Usine`, ajoutez une méthode `generer_rapport` qui :
  - Calcule le nombre total de jouets produits (longueur de `produits_finis`).
  - Calcule le pourcentage de jouets défectueux (nombre de produits avec `tentatives > 0` divisé par le total, multiplié par 100, en utilisant `filter`).
  - Calcule le temps moyen de production (somme des `temps_total` de tous les produits divisée par le total, en utilisant `reduce`).
  - Calcule le nombre de jouets rejetés (nombre de produits avec `status == "rejeté"`, en utilisant `filter`).
  - Extrait la liste des numéros de série (en utilisant `map` pour appeler la méthode `extraire_numero_serie` de chaque produit).
- Affichez ces résultats dans la console avec des messages clairs (par exemple, `print(f"Nombre total de jouets produits : {total_produits}")`).

**Exemple de mécanisme interne** : Pour calculer le pourcentage de jouets défectueux, vous utiliserez `filter(lambda p: p.tentatives > 0, produits_finis)` pour obtenir une liste des produits défectueux, puis diviserez sa longueur par la longueur totale de `produits_finis`. Pour calculer le temps moyen, vous utiliserez `reduce(lambda x, y: x + y.temps_total, produits_finis, 0)` pour obtenir la somme des temps, puis diviserez par le nombre total de produits.

---

### 3. Contraintes 

**Objectif** : Définir les contraintes pour garantir un code de qualité et respectueux des consignes.

**Fonctionnement interne** :
- Les contraintes garantissent que le programme est modulaire, lisible, et conforme aux attentes pédagogiques.
- Elles limitent l'utilisation de bibliothèques externes pour se concentrer sur la bibliothèque standard Python, ce qui est important pour apprendre les bases.

**Implémentation** :
- Votre programme doit être **modulaire**, avec des classes et des fonctions bien définies. Par exemple, la gestion des pannes doit être encapsulée dans la classe `Station`, et non dispersée dans `Usine`.
- Vous devez **commenter votre code** pour expliquer les parties importantes, notamment l'utilisation des concepts demandés (par exemple, un commentaire expliquant pourquoi `collections.deque` est utilisé pour la file d'attente).
- Vous ne devez pas utiliser de bibliothèques externes autres que celles de la bibliothèque standard Python (`collections`, `itertools`, `logging`, `re`, `random`, `time`, etc.).
- Les temps de traitement et les pannes doivent être simulés avec des délais réalistes, mais accélérés pour le test. Par exemple, un temps de traitement de 2 secondes est simulé en 0.2 seconde avec `time.sleep(temps / 10)` pour ne pas rendre la simulation trop lente.

**Exemple de mécanisme interne** : La modularité est assurée en séparant les responsabilités : la classe `Produit` gère les données du produit, la classe `Station` gère le traitement et les pannes, la classe `PileDefauts` gère les défauts, et la classe `Usine` orchestre tout. Les commentaires expliquent des choix comme l'utilisation de `collections.deque` pour les files d'attente, qui est plus efficace qu'une liste standard pour les opérations `popleft`.

---

### 4. Livrables 

**Objectif** : Définir ce qui doit être rendu pour évaluer le projet.

**Fonctionnement interne** :
- Les livrables permettent de vérifier que le programme fonctionne correctement et produit les résultats attendus.
- Le fichier de logs et le rapport final sont essentiels pour analyser le déroulement de la simulation et les performances.

**Implémentation** :
- Vous devez rendre les éléments suivants :
  1. Le **code source complet** sous forme d'un fichier Python (`usine.py`) ou d'un notebook Jupyter (`usine.ipynb`). Ce fichier doit inclure toutes les classes et fonctions nécessaires, avec des commentaires.
  2. Un **fichier de logs** généré (`usine.log`), contenant tous les événements enregistrés pendant la simulation. Ce fichier est généré automatiquement par le module `logging`.
  3. Un **rapport final** affiché dans la console, contenant les analyses demandées (nombre de jouets produits, pourcentage de défauts, temps moyen, etc.). Ce rapport est généré par la méthode `generer_rapport` de la classe `Usine`.

**Exemple de mécanisme interne** : Le fichier `usine.log` est créé par la configuration initiale du logging et mis à jour à chaque appel à `logging.info`, `logging.warning`, ou `logging.error`. Le rapport final est généré en appelant `generer_rapport`, qui utilise `map`, `filter`, et `reduce` pour analyser les données de `produits_finis`.

---


### 6. Conseils pour la réalisation

**Objectif** : Fournir des conseils pratiques pour aider à implémenter le projet, avec un focus sur les mécanismes internes.

**Fonctionnement interne** :
- La planification et le test progressif sont essentiels pour gérer la complexité du projet.
- La modularité et les logs aident à déboguer et à maintenir le code.

**Implémentation** :
- **Planification** :
  - Commencez par définir les classes principales (`Produit`, `Station`, `PileDefauts`, `Usine`) et leurs responsabilités. Par exemple, `Produit` gère les données du produit, `Station` gère le traitement et les pannes, `PileDefauts` gère les défauts, et `Usine` orchestre tout.
  - Décomposez le projet en étapes : gestion des produits, simulation du flux, gestion des défauts, simulation des pannes, analyse des données.
  - Exemple de mécanisme interne : La classe `Usine` utilise un dictionnaire pour stocker les stations, ce qui permet d'accéder facilement à chaque station par son nom (par exemple, `stations["assemblage"]`). Cela facilite l'ajout de produits aux files d'attente et le passage des produits d'une station à la suivante.

- **Test progressif** :
  - Testez chaque classe individuellement avant d'intégrer toutes les fonctionnalités. Par exemple, testez la validation des identifiants avec regex dans `Produit` avant d'implémenter la simulation complète.
  - Exemple de mécanisme interne : Pour tester `Produit`, créez une instance avec un identifiant comme `"TOY-001-RED"` et vérifiez que la méthode de validation retourne `True`, et que la méthode d'extraction retourne `1` comme numéro de série.

- **Utilisation des logs** :
  - Les logs sont essentiels pour déboguer et comprendre le déroulement de la simulation. Assurez-vous d'enregistrer suffisamment d'informations pour pouvoir retracer les événements, comme les ajouts aux files d'attente, les traitements, les pannes, et les défauts.
  - Exemple de mécanisme interne : Les logs sont écrits dans un fichier `usine.log` grâce à la configuration initiale du logging. Chaque appel à `logging.info` ou `logging.warning` ajoute une ligne avec un horodatage, ce qui permet de suivre l'ordre des événements et de détecter les problèmes (par exemple, une file d'attente qui se remplit trop vite à cause d'une panne).

- **Modularité** :
  - Gardez votre code modulaire en séparant les responsabilités. Par exemple, la gestion des pannes doit être encapsulée dans la classe `Station`, et non dans la classe `Usine`. Cela facilite les modifications et les tests.
  - Exemple de mécanisme interne : La méthode `verifier_panne` de `Station` gère tout l'état de la panne (vérification, décrémentation du temps restant, résolution), ce qui permet à la classe `Usine` de simplement appeler `traiter_produit` sans se soucier des détails des pannes.
