from typing import List, Dict, Deque
import re
from collections import deque
import logging
import random
import time

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="usine.log",
    filemode="w",  # Écriture (remplace le fichier existant)
)


# Gestion des produits
class Produit:
    """Classe qui représente un produit qui est un jouet.
    - Chaque produit est un objet avec un identifiant unique sous la forme `"TOY-XXX-COLOR"`, où `XXX` est un numéro de série (par exemple, 001, 002) et `COLOR` est une couleur (par exemple, RED, BLUE, GREEN).
    - L'identifiant est généré automatiquement lors de la création du produit, en combinant un numéro de série (incrémenté automatiquement) et une couleur choisie aléatoirement.
    - Le produit a un statut (`"en cours"`, `"fini"`, ou `"rejeté"`) qui est mis à jour au fil de la simulation.
    - Le produit garde une trace de son temps total de production (en secondes simulées) et des étapes effectuées (par exemple, `["assemblage", "peinture"]`).

    Attributes:
        identifiant (str): Identifiant unique sous la forme `"TOY-XXX-COLOR"`, où `XXX` est un numéro de série (par exemple, 001, 002) et `COLOR` est une couleur (par exemple, RED, BLUE, GREEN).
        statut (str): Un statut (`"en cours"`, `"fini"`, ou `"rejeté"`) qui est mis à jour au fil de la simulation.
        tempsTotal (float): Temps total de production (en secondes simulées).
        etapesEffectue (List[str]): Etapes effectuées (par exemple, `["assemblage", "peinture"]`)

    Examples:
        >>> produit = Produit(1, "red")
        >>> print(produit)
        TOY-001-RED (Status: en cours, Temps: 0s)
    """

    def __init__(
        self,
        numérosDeSérie: int,
        color: str,
    ):
        """Initialise un nouveau produit.

        Args :
            numérosDeSérie (int): Un numéro qui va être convertie en 3 chiffres (example: 1 -> 001).
            color (str): La couleur du produit.
            statut (str): Un statut (`"en cours"`, `"fini"`, ou `"rejeté"`) qui est mis à jour au fil de la simulation.
            tempsTotal (int): Temps total de production (en secondes simulées).
            etapesEffectue (List[str]): Etapes effectuées (par exemple, `["assemblage", "peinture"]`)
        """
        self.identifiant = f"TOY-{numérosDeSérie:03d}-{color.upper()}"
        self.statut = "en cours"
        self.tempsTotal = 0
        self.etapesEffectue = []

    def __str__(self) -> str:
        """Donne une représentation lisible d'un objet produit en affichant sont identifiant, sont status et le temps total de production.

        Returns:
            string: Représentation lisible du produit.

        Examples:
            >>> produit = Produit(1, "red")
            >>> print(produit)
            TOY-001-RED (Status: en cours, Temps: 0s)
        """
        return f"{self.identifiant} (Status: {self.statut}, Temps: {self.tempsTotal}s)"

    def validationIdentifiant(self) -> bool:
        """Valide la forme de l'identifiant.

        Returns:
            bool: Valeur qui indique si l'identifiant est au bon format.

        Examples:
            >>> produit = Produit(1, "red")
            >>> print(produit.validationIdentifiant())
            True

            >>> produit = Produit(1, "1", "fini", 18, ["assemblage", "peinture"])
            >>> print(produit.validationIdentifiant())
            False
        """
        return bool(re.match(r"TOY-\d{3}-[A-Z]+", self.identifiant))

    def getNumeroSerie(self) -> str:
        """Permet de récupérer le numéros de série à partir de l'identifiant.

        Returns:
            str: Le numéros de série de l'objet.

        Examples:
            >>> produit = Produit(1, "red")
            >>> print(produit.getNumeroSerie())
            001
        """
        return re.search(r"TOY-(\d{3})-[A-Z]+", self.identifiant).group(1)


produit = Produit(1, "red")
print(produit)


# Simulation du flux de production
class Station:
    def __init__(self, nom: str, temps_moyen: float):
        self.nom = nom
        self.temps_moyen = temps_moyen
        self.file_attente = deque()

    def ajouter_produit(self, produit: Produit) -> None:
        self.file_attente.append(produit)
        logging.info(
            f"Le produit {produit} à bien été ajouter à la fin de la file d'attente."
        )

    def traiter_produit(self) -> Produit:
        if len(self.file_attente) == 0:
            return None
        else:
            produit = self.file_attente.popleft()
            temps_traitement = random.uniform(
                self.temps_moyen * 0.5, self.temps_moyen * 1.5
            )
            time.sleep(temps_traitement / 10)
            produit.tempsTotal += temps_traitement
            produit.etapesEffectue.append(self.nom)
            return produit


station = Station("assemblage", 18.5)
station.ajouter_produit(produit)
print(station.traiter_produit())


class Usine:
    def __init__(self):
        self.stations = {
            "assemblage": Station("assemblage", 2),
            "peinture": Station("peinture", 3),
            "contrôle qualité": Station("contrôle qualité", 1),
            "emballage": Station("emballage", 1),
        }

    def simuler_flux(self) -> None:
        etapes = ["assemblage", "peinture", "contrôle qualité", "emballage"]
        while any(station.file_attente for station in self.stations.values()):
            for i, etape in enumerate(etapes):
                produit_traite = self.stations[etape].traiter_produit()
                if produit_traite == None:
                    continue
                elif etape == "emballage":
                    print("Tous les étapes sont terminé pour ce produit")
                else:
                    self.stations[etape[i + 1]].ajouter_produit(produit_traite)
