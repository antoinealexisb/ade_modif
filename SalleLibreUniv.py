#SalleLibreUniv.py

'''On s’intéresse aux horaires des salles de cours.
Ce programme permet d'afficher les créneaux d'occupation des salles de cours de la faculté des sciences de Lens.
Il n'affiche que les horaires du jour. (la version avec les jours futur est sur le bot)

Fonctions:
 - home()
 - ajouteSalle(tmpDeb, tmpFin, tmpSalle)
 - afficheSalles()
 - triHoraire()
 - affichageSalle(nomsalle)
 - menu()
 - main()
'''
__author__ = 'Antoine-Alexis Bourdon <antoine-alexis_bourdon@ens.univ-artois.fr>'
__date__= '07/01/2020'


#Importation des librairies.
import datetime
import urllib3

#Variable global = c'est le mal ;)
salle = []
date = "datetime.datetime.now().strftime("%Y-%m-%d")

def home():
    '''
    Cette partie télécharge le fichier ADE du jour.(fichier au format .ics .Format de données pour les échanges de données de calendrier)
    Arguments:
        None.
    Retour:
        :--bool (si l'opération c'est bien passée ou non)
    '''
    global date
    global salle
    salle = []
    print("Téléchargement de la base ADE pour le semestre pair, année 2019 (jour : "+date+")")
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://ade-consult.univ-artois.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=8005&projectId=1&calType=ical&firstDate='+date+'&lastDate='+date+'&data=02427bf08a4e3905df54e3828781966417a0456235d61df4705fb52a51c95d7ffb650adbf17b96d5d97cc32ac608bd134bd92253eb85eb8cc5b140158eb150a876ea41bc176608f34b0dc0eb3d0541420d219a8a2811502431d44fcc2bedcd5766fe1467ca6773eda8418747eceeea208fc8eaca54c53c509dc2134dcd161ba64a660cb94c969a7630feed39799f89a9f0f26b2783481751a1bc422e85df36640812d1b6fab9bafa2230f703ec4296da,1')
    if r.status != 200:
        print("Erreur : Echec téléchargement base ADE !")
        return False
    print("\tTéléchargement effectué")

    baseADE = r.data.decode('utf-8').replace("\r","")
    tmpsalle = ""
    tmpDeb=""
    tmpFin=""
    tmp=""
    tailleLo=len("LOCATION:")
    taillestart=len("DTSTART:")
    tailleEnd=len("DTEND:")

    for i in range(len(baseADE)-taillestart):
        if "DTSTART:" == baseADE[i:i+taillestart]:
            i+=taillestart

            #recupere l'heure de commencement du cours
            while baseADE[i] != '\n':
                tmp+=baseADE[i]
                i+=1
            tmpDeb=str(int(tmp[9:11])+1).zfill(2)+"h"+tmp[11:13]

            tmp=""
            i+=tailleEnd+1

            #recupere l'heure de fin du cours
            while baseADE[i] != '\n':
                tmp+=baseADE[i]
                i+=1
            tmpFin=str(int(tmp[9:11])+1).zfill(2)+"h"+tmp[11:13]

            #salle
            while "LOCATION:" != baseADE[i:i+tailleLo]:
                i+=1 
            i+=tailleLo
            while baseADE[i] != '\n':
                tmpsalle+=baseADE[i]
                i+=1

            ajouteSalle(tmpDeb, tmpFin, tmpsalle)
            tmpDeb=""
            tmpFin=""
            tmp=""
            tmpsalle=""
    triHoraire()
    return True

def ajouteSalle(tmpDeb, tmpFin, tmpSalle):
    '''
    Fonction qui ajoute au tableau salle(global), le numéro de salle, l'heure de début et de fin.
    Arguments:
        tmpDeb : --str heure de début du cours dans la salle
        tmpFin : --str heure de fin du cours dans la salle
        tmpSalle : --str nom de salle (G310, S25, ...)
    Retour:
        True : --bool.
    '''
    for i in range(len(salle)):
        if salle[i][0] == tmpSalle:
            salle[i][1].append(tmpDeb+" - "+tmpFin)
            return True
    salle.append([tmpSalle,[tmpDeb+" - "+tmpFin]])
    return True

def afficheSalles():
    '''Fonction qui affiche toutes les salles occupées, avec les horaires d'occupation.
    Arguments:
        None.
    Retour:
        None.
    '''
    for i in range(len(salle)):
        print(salle[i][0],":")
        for j in range(len(salle[i][1])):
            print("\t",salle[i][1][j])
        print()

def triHoraire():
    '''Fonction qui trie les horaires en fonction des salles du tableau salle(global).
    Arguments:
        None.
    Retour:
        None.
    '''
    for i in range(len(salle)):
        salle[i][1].sort()


def affichageSalle(nomsalle):
    '''Fonction qui affiche la salle donnée en argument, si celle-ci existe.
    Arguments:
        -nomsalle : --str (nom de la salle)
    Retour:
        --bool (retourne si la salle existe ou non)
    '''
    for i in range(len(salle)):
        if salle[i][0] == nomsalle:
            print(salle[i][0],":")
            for j in range(len(salle[i][1])):
                print("\t",salle[i][1][j])
            return True
    return False

def menu():
    '''
    Fonction qui affiche un petit demandant le nom de la salle.
    Arguments:
        None.
    Retour:
        None.
    '''
    print("\n\nNom de la salle (ex: G310, S25) : ", end="")
    nomsalle = input()
    print("\n\n")
    if nomsalle == "all":
        afficheSalles()
        return True
    if not affichageSalle(nomsalle):
        print("Erreur : La salle n'est pas dans le fichier !")
        return False
    return True

def main():
    '''Fonction principale, qui n'est pas rangée XD.
    '''
    global date
    print("\t##################################################")
    print("\t## Affiche les créneaux d'occupation des salles ##")
    print("\t##################################################")
    print("\n\n")
    if not home():
        print("Pas de connexion : Erreur")
        return False
    else:
        continuer = 1
        while continuer==1:
            menu()
            continuer = input("\n\n\t Voulez-vous continuer \n\t  0 - non\n\t  1 - oui\n\t : ")
            if continuer != "0":
                continuer = 1
                if date != datetime.datetime.now().strftime("%Y-%m-%d"):
                    print("\n\n\t #### Mise à jour du fichier suite à un changement du jour courant !!\n")
                    date=datetime.datetime.now().strftime("%Y-%m-%d")
                    if not home():
                        print("Impossible de copier la base ADE\n Erreur de connexion")
                        return False
            else:
                continuer = 0
        return True

if __name__ == "__main__":
    main()
