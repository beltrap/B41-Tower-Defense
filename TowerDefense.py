# -*- coding:utf-8 -*-
from tkinter import *
import random
import helper
from _overlapped import NULL

class Portail():
    def __init__(self, parent):
        self.parent = parent
        self.pointsDeVie = 1000
        # Retire le dernier point du sentier pour représenter la position du portail
        position = parent.sentier.chemin.pop()
        self.x = position[0]
        self.y = position[1]
    
    # Réduit les points de vie du portail s'il est endommagé
    def endommager(self, dommages):
        self.pointsDeVie -= dommages

class Sentier():
    def __init__(self, parent):
        self.parent = parent
        self.chemin = []
        self.minPctCouverture = 20
        self.maxPctCouverture = 25
        
        # Détermination du point de départ
        # Lecôté de départ représente le haut(0), la droite(1), le bas(2) et la gauche(3)
        coteDepart = random.randrange(4)
        
        # Haut
        if coteDepart == 0:
            x = random.randrange(parent.largeur)
            y = 0
        # Droite
        elif coteDepart == 1:
            x = parent.largeur - 1
            y = random.randrange(parent.hauteur)
        # Bas
        elif coteDepart == 2:
            x = random.randrange(parent.largeur)
            y = parent.hauteur - 1
        # Gauche
        else:
            x = 0
            y = random.randrange(parent.hauteur)
        
        depart = (x, y)
        
        # Génération et acceptation du terrain
        # Acceptation selon le pourcentage de points qui forment le chemin
        cheminAccepte = False
        
        while not cheminAccepte:
            
            # Réinitialise le chemin et on intègre le point de départ comme premier point
            self.chemin.clear()
            self.chemin.append(depart)
            dernierPoint = self.chemin[-1]
            
            # Génération du chemin de façon aléatoire
            generation = True
            cheminRejete = False
            
            while generation and not cheminRejete:
                
                # Détermination de la direction du prochain point
                directionValide = False
                
                while not directionValide and not cheminRejete:
                    
                    # La direction est représentée par le haut(0), la droite(1), le bas(2) et la gauche(3)
                    direction = random.randrange(4)
                    
                    # Haut
                    if direction == 0:
                        x = dernierPoint[0]
                        y = dernierPoint[1] - 1
                    # Droite
                    elif direction == 1:
                        x = dernierPoint[0] + 1
                        y = dernierPoint[1]
                    # Bas
                    elif direction == 2:
                        x = dernierPoint[0]
                        y = dernierPoint[1] + 1
                    # Gauche
                    else:
                        x = dernierPoint[0] - 1
                        y = dernierPoint[1]
                    
                    # Si le point n'existe pas déjà dans le chemin, l'ajouter à la liste
                    if (x, y) not in self.chemin:
                        self.chemin.append((x, y))
                        dernierPoint = self.chemin[-1]
                        directionValide = True
                    
                    # Si tout le chemin ne peut plus aller nulle part (pris dans une spirale), on le rejet
                    if (dernierPoint[0] + 1, dernierPoint[1]) in self.chemin and (dernierPoint[0] - 1, dernierPoint[1]) in self.chemin and (dernierPoint[0], dernierPoint[1] + 1) in self.chemin and (dernierPoint[0], dernierPoint[1] - 1) in self.chemin:
                        cheminRejete = True
                
                # Vérifie si le chemin va en dehors du terrain
                # Si oui, on retire le dernier point et la génération est terminée
                if dernierPoint[0] < 0 or dernierPoint[0] > parent.largeur - 1 or dernierPoint[1] < 0 or dernierPoint[1] > parent.hauteur - 1:
                    self.chemin.remove(dernierPoint)
                    generation = False
            
            # Vérification pour savoir si le chemin est trop long ou trop court selon les pourcentages minimales et maximales
            couvertureMin = parent.largeur * parent.hauteur * self.minPctCouverture / 100
            couvertureMax = parent.largeur * parent.hauteur * self.maxPctCouverture / 100
            
            if len(self.chemin) >= couvertureMin and len(self.chemin) <= couvertureMax and not cheminRejete:
                cheminAccepte = True

class TowerDefense():
    def __init__(self, parent):
        self.parent = parent
        self.largeur = 30
        self.hauteur = 20
        self.sentier = Sentier(self)
        self.portail = Portail(self)

class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.modele = self.parent.modele
        self.root = Tk()
        self.echelleDeGrosseur = 20
        self.largeur = 800
        self.hauteur = 600
        
    # ===[Debugging]=====================================================
    
    def debugging(self):
        # Sert à afficher les point du sentier (s'il existe) dans la console
        if self.modele.sentier is not NULL:
            print("===[Chemin du Sentier]=============================================")
            for point in self.modele.sentier.chemin:
                print(point)
            
        # Sert à afficher la position du portail (s'il existe) dans la console
        if self.modele.portail is not NULL:
            print("===[Position du Portail]===========================================")
            print("(", self.modele.portail.x, ",",  self.modele.portail.y, ")")
    
    # ===================================================================

class Controleur():
    def __init__(self):
        self.modele = TowerDefense(self)
        self.vue = Vue(self)
        
        # Debug
        self.vue.debugging()

if __name__ == '__main__':
    controleur = Controleur()