from datetime import time
from typing import List
import re


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
        tempsTotal (int): Temps total de production (en secondes simulées).
        etapesEffectue (List[str]): Etapes effectuées (par exemple, `["assemblage", "peinture"]`)

    Examples:
        >>> produit = Produit(1, "red", "fini", 18, ["assemblage", "peinture"])
        >>> print(produit)
        TOY-001-RED (Status: fini, Temps: 18s)
    """

    def __init__(
        self,
        numérosDeSérie: int,
        color: str,
        statut: str,
        tempsTotal: int,
        etapesEffectue: List[str],
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
        self.statut = statut
        self.tempsTotal = tempsTotal
        self.etapesEffectue = etapesEffectue

    def __str__(self) -> str:
        """Donne une représentation lisible d'un objet produit en affichant sont identifiant, sont status et le temps total de production.

        Returns:
            string: Représentation lisible du produit.

        Examples:
            >>> produit = Produit(1, "red", "fini", 18, ["assemblage", "peinture"])
            >>> print(produit)
            TOY-001-RED (Status: fini, Temps: 18s)
        """
        return f"{self.identifiant} (Status: {self.statut}, Temps: {self.tempsTotal}s)"

    def validationIdentifiant(self) -> bool:
        """Valide la forme de l'identifiant.

        Returns:
            bool: Valeur qui indique si l'identifiant est au bon format.

        Examples:
            >>> produit = Produit(1, "red", "fini", 18, ["assemblage", "peinture"])
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
            >>> produit = Produit(1, "red", "fini", 18, ["assemblage", "peinture"])
            >>> print(produit.getNumeroSerie())
            001
        """
        return re.search(r"TOY-(\d{3})-[A-Z]+", self.identifiant).group(1)
