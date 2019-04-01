# -*- coding:utf-8 -*-
from tkinter import *
import random
import helper
import debug
from _overlapped import NULL

class Portail():
    def __init__(self, parent):
        self.parent = parent
        self.pointsDeVie = 1000
        # Retire le dernier point du sentier pour représenter la position du portail
        self.x, self.y = parent.sentier.chemin.pop()
    
    # Réduit les points de vie du portail s'il est endommagé
    def endommager(self, dommages):
        self.pointsDeVie -= dommages

class Sentier():
    def __init__(self, parent):
        self.parent = parent
        self.chemin = []
        self.minPctCouverture = 25
        self.maxPctCouverture = 30
        
        # Détermination du point de départ
        # Lecôté de départ représente le haut(0), la droite(1), le bas(2) et la gauche(3)
        coteDepart = random.randrange(4)
        
        # Haut
        if coteDepart == 0:
            x = random.randrange(self.parent.largeur)
            y = 0
        # Droite
        elif coteDepart == 1:
            x = self.parent.largeur - 1
            y = random.randrange(self.parent.hauteur)
        # Bas
        elif coteDepart == 2:
            x = random.randrange(self.parent.largeur)
            y = self.parent.hauteur - 1
        # Gauche
        else:
            x = 0
            y = random.randrange(self.parent.hauteur)
        
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
            couvertureMin = self.parent.largeur * self.parent.hauteur * self.minPctCouverture / 100
            couvertureMax = self.parent.largeur * self.parent.hauteur * self.maxPctCouverture / 100
            
            if len(self.chemin) >= couvertureMin and len(self.chemin) <= couvertureMax and not cheminRejete:
                cheminAccepte = True

class TowerDefense():
    def __init__(self, parent):
        self.parent = parent
        self.largeur = 20
        self.hauteur = 20
        self.sentier = None
        self.portail = None
        self.partieEnCours = False
        
    def creerPartie(self):
        self.sentier = Sentier(self)
        self.portail = Portail(self)
        
        # Afficher le debug
        debug.Debug.log(self)

class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.modele = self.parent.modele
        self.root = Tk()
        self.echelleDeGrosseur = 29
        self.largeur = 800
        self.hauteur = 600
        self.titreDuJeu = "Tower Defense"
        self.largeurSideBar = 200
    
    def afficheMenuInit(self):
        if self.parent.modele.partieEnCours:
            self.frameJeu.pack_forget()
        
        # Titre de la fenêtre
        self.root.title(self.titreDuJeu)
        self.root.configure(bg = "#222222")
        
        # Détermine la résolution de la fenêtre
        geometry = "%dx%d" % (self.largeur, self.hauteur)
        self.root.geometry(geometry)
        
        # Création du frame qui va contenir le menu
        self.frameMenu = Frame(self.root,
                               bg = "#F0F0F0",
                               highlightthickness = 0)
        self.frameMenu.pack(side = TOP, expand = True)
        
        # Création du titre
        self.labTitre = Label(self.frameMenu,
                              font = ("Agency FB", 40),
                              bg = "#F0F0F0",
                              fg = "#222222",
                              text = self.titreDuJeu)
        self.labTitre.pack(fill = X,
                           padx = 40,
                           pady = 20)
        
        # Création des boutons
        self.menuBtn = []
        menuBtnTxtOuCmd = [("Continuer", self.parent.jouerCoup),
                           ("Nouvelle partie", self.parent.debutPartie),
                           ("Quitter", self.parent.quitter)]
        
        for txtOuCmd in menuBtnTxtOuCmd:
            # Si la partie est en cours, afficher l'option de continuer la partie
            if txtOuCmd[0] == "Continuer" and not self.modele.partieEnCours:
                continue
            
            btn = Button(self.frameMenu,
                         font = ("Agency FB", 20),
                         bg = "#292929",
                         fg = "#FFFFFF",
                         activebackground = "#FFFFFF",
                         activeforeground = "#292929",
                         text = txtOuCmd[0],
                         command = txtOuCmd[1])
            btn.pack(fill = X,
                     padx = 7,
                     pady = 7)
            
            self.menuBtn.append(btn)
        
        self.labCredit = Label(self.root,
                              font = ("Arial", 7),
                              bg = "#222222",
                              fg = "#CBCBCB",
                              text = "Développé par: Jessica Khau, Maxime Denis et Paul Beltran\nDans le cadre du cour de B41 Gestion de projet - Technique et méthodologie au CVM")
        self.labCredit.pack(side = BOTTOM)
    
    def afficheNiveau(self):
        self.frameMenu.pack_forget()
        self.labCredit.pack_forget()
        
        self.frameJeu = Frame(self.root,
                              bg = "#222222",
                              highlightthickness = 0)
        self.frameJeu.pack(side = TOP,
                           expand = True)
        
        self.canvasJeu = Canvas(self.frameJeu,
                                highlightthickness = 0,
                                width = self.largeur - 19 - self.largeurSideBar,
                                height = self.hauteur - 19,
                                bg = "#006600")
        self.canvasJeu.pack(side = LEFT,
                            padx = 10)
        
        lineColor = "#222222"
        
        for i in range(self.modele.largeur + 1):
            self.canvasJeu.create_line(i * self.echelleDeGrosseur,
                                       0,
                                       i * self.echelleDeGrosseur,
                                       self.largeur - self.largeurSideBar,
                                       fill = lineColor)

        for i in range(self.modele.hauteur + 1):
            self.canvasJeu.create_line(0,
                                       i * self.echelleDeGrosseur,
                                       self.hauteur,
                                       i * self.echelleDeGrosseur,
                                       fill = lineColor)
        
        for point in self.modele.sentier.chemin:
            self.canvasJeu.create_rectangle(point[0] * self.echelleDeGrosseur + 1,
                                            point[1] * self.echelleDeGrosseur + 1,
                                            point[0] * self.echelleDeGrosseur + self.echelleDeGrosseur,
                                            point[1] * self.echelleDeGrosseur + self.echelleDeGrosseur,
                                            fill = "#994C00", width = 0)
        
        self.canvasJeu.create_rectangle(self.modele.portail.x * self.echelleDeGrosseur + 1,
                                        self.modele.portail.y * self.echelleDeGrosseur + 1,
                                        self.modele.portail.x * self.echelleDeGrosseur + self.echelleDeGrosseur,
                                        self.modele.portail.y * self.echelleDeGrosseur + self.echelleDeGrosseur,
                                        fill = "#6600CC", width = 0)
        
        self.frameSideBar = Frame(self.frameJeu,
                                  bg = "#222222",
                                  highlightthickness = 0,
                                  width = self.largeurSideBar,
                                  height = self.hauteur - 10)
        self.frameSideBar.pack(side = LEFT)
        
        self.frameBtnMenu = Frame(self.frameSideBar,
                                  bg = "#F0F0F0",
                                  highlightthickness = 0,
                                  width = 200)
        self.frameBtnMenu.pack(side = TOP,
                               fill = X,
                               padx = 10,
                               pady = 10)
        
        self.btnMenuPrincipal = Button(self.frameBtnMenu,
                                       font = ("Agency FB", 17),
                                       bg = "#292929",
                                       fg = "#FFFFFF",
                                       activebackground = "#FFFFFF",
                                       activeforeground = "#292929",
                                       text = "Menu principal",
                                       command = None)
        self.btnMenuPrincipal.pack(side = TOP,
                                   fill = X,
                                   padx = 7,
                                   pady = 7)
        
        self.labScore = Label(self.frameBtnMenu,
                              anchor = W,
                              font = ("Agency FB", 17),
                              bg = "#F0F0F0",
                              fg = "#222222",
                              text = "Score: 0")
        self.labScore.pack(side = TOP,
                           fill = X,
                           padx = 5,
                           pady = 5)
        
        self.labRessources = Label(self.frameBtnMenu,
                                   anchor = W,
                                   font = ("Agency FB", 17),
                                   bg = "#F0F0F0",
                                   fg = "#222222",
                                   text = "Ressources: 0")
        self.labRessources.pack(side = TOP,
                                fill = X,
                                padx = 5,
                                pady = 5)
        
    def afficheFinDeJeu(self):
        pass

class Controleur():
    def __init__(self):
        self.modele = TowerDefense(self)
        self.vue = Vue(self)
        
        # Afficher le menu initial
        self.vue.afficheMenuInit()
        
        # Commencer le mainloop de tkinter
        self.vue.root.mainloop()
    
    def debutPartie(self):
        self.modele.creerPartie()
        self.jouerCoup()
    
    def jouerCoup(self):
        self.vue.afficheNiveau()
    
    def retourMenu(self):
        pass
    
    def quitter(self):
        pass

if __name__ == '__main__':
    controleur = Controleur()