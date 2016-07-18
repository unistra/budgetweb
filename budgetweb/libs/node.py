from budgetweb.models import *


class Node:
    def __init__(self, n, s, level, visibility):
        self.id = n
        self.title = s
        self.level = level
        self.visibility = visibility
        self.children = []

    def getMarginLeft(self):
        return self.level * 10

    def addChild(self, Node):
        self.children.append(Node)

    def getChild(self):
        return self.children

    def __str(self):
        return self.id + " " + self.title + "(" + \
               self.level + ")" + self.children


def generateTree(request):
    # On commence par la liste des programmes de financements.
    ETAB = Node('ETAB', "ETAB", 1, 1)
    listeCF = Node('TOP', "TOP", 0, 1)
    listeCF.addChild(ETAB)
    return listeCF


# Ajouter une exception si jamais pas de période ouverte
def getCurrentYear():
    return PeriodeBudget.objects.filter(is_active=True).first().annee
