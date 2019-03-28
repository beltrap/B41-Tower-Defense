class Debug(object):
    def log(modele):
        # Sert � afficher si la partie est en cours (si la valeur existe)
        if hasattr(modele, "partieEnCours"):
            print("===[Partie en cours]===============================================")
            print(modele.partieEnCours)
            print()
            
        # Sert � afficher si la partie est en pause (si la valeur existe)
        if hasattr(modele, "pause"):
            print("===[Partie en pause]===============================================")
            print(modele.pause)
            print()
        
        # Sert � afficher les point du sentier (s'il existe) dans la console
        if hasattr(modele, "sentier"):
            print("===[Chemin du Sentier]=============================================")
            for point in modele.sentier.chemin:
                print(point)
            print()
            
        # Sert � afficher la position du portail (s'il existe) dans la console
        if hasattr(modele, "portail"):
            print("===[Position du Portail]===========================================")
            print("(", modele.portail.x, ",",  modele.portail.y, ")")
            print()