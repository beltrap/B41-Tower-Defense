class Debug(object):
    def log(modele):
        # Sert à afficher si la partie est en cours (si la valeur existe)
        if hasattr(modele, "partieEnCours"):
            print("===[Partie en cours]===============================================")
            print(modele.partieEnCours)
            print()
            
        # Sert à afficher si la partie est en pause (si la valeur existe)
        if hasattr(modele, "pause"):
            print("===[Partie en pause]===============================================")
            print(modele.pause)
            print()
        
        # Sert à afficher les point du sentier (s'il existe) dans la console
        if hasattr(modele, "sentier"):
            print("===[Chemin du Sentier]=============================================")
            for point in modele.sentier.chemin:
                print(point)
            print()
            
        # Sert à afficher la position du portail (s'il existe) dans la console
        if hasattr(modele, "portail"):
            print("===[Position du Portail]===========================================")
            print("(", modele.portail.x, ",",  modele.portail.y, ")")
            print()