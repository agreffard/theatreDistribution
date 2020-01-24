#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import random

characters = {}
scenes = {}

header = []

actors = ['Acteur 1', 'Acteur 2', 'Acteur 3', 'Acteur 4'] # Aurel, Manu, Stephane, Pascal
actresses = ['Actrice 1', 'Actrice 2', 'Actrice 3', 'Actrice 4'] # Auriane, Cannelle, Clara, Leonie

distributions = []

class Character:
    def __init__(self, name, gender, lines):
        self.name = name
        self.gender = gender
        self.lines = lines
        self.partners = []

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

class Scene:
    def __init__(self, name):
        self.name = name
        self.characters = []

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

class Actor:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

class Distribution:
    def __init__(self):
        self.actorByCharacter = {}
        self.charactersByActor = {}
        self.incompatibilities = {}

    # def __eq__(self, other):
    #     for k, v in self.actorByCharacter.items():
    #         if self.actorByCharacter[k] != other.actorByCharacter[k]:
    #             return False
    #     return True

def getDistribByActor(name):
    global scenes
    if name in scenes:
        return scenes[name]
    scene = Scene(name)
    scenes[name] = scene
    return scene

def getSceneByName(name):
    global scenes
    if name in scenes:
        return scenes[name]
    scene = Scene(name)
    scenes[name] = scene
    return scene

def getSceneName(index):
    return header[index]

def getSceneByIndex(index):
    return getSceneByName(getSceneName(index))

def addLine(characterData):
    global characters
    global scenes
    character = Character(characterData[0], characterData[1], characterData[2])
    characters[character.name] = character
    for i, val in enumerate(characterData):
        if i > 2 and val != '':
            scene = getSceneByIndex(i)
            scene.characters.append(character)
            for otherScene in scenes.values():
                if scene != otherScene and character in otherScene.characters:
                    for otherCharacter in otherScene.characters:
                        if character != otherCharacter:
                            if (otherCharacter not in character.partners):
                                character.partners.append(otherCharacter)
                            if (character not in otherCharacter.partners):
                                otherCharacter.partners.append(character)

def buildData():
    global header
    with open('repliques.txt') as f:
        header = f.readline().split('\t')
        cnt = 0
        # print("Header {}: {}".format(cnt, header.strip()))
        cnt += 1
        line = f.readline()
        while line:
            characterData = line.split('\t')
            # print(characterData)
            # print("Line {}: {}".format(cnt, line.strip()))
            addLine(characterData)
            cnt += 1
            line = f.readline()


def printPartners():
    return
    print ("################################### PARTENAIRES DE JEU ###################################")
    for k, v in characters.items():
        print(k + " : " + str(v.partners))
    print ("##########################################################################################")

def getRandomAvailableActor(character, distribution):
    availabilities = []
    if character.gender == 'F':
        availabilities = actresses
    elif character.gender == 'H':
        availabilities = actors
    else:
        availabilities = actors + actresses

    availabilities = [a for a in availabilities if a not in distribution.incompatibilities or character not in distribution.incompatibilities[a]]
    print ("availabilities" + str(availabilities))

    if len(availabilities) == 0:
        return None
    selectedActor = random.choice(availabilities)
    return selectedActor


def addCharacterToActor(actor, character, distribution):
    distribution.actorByCharacter[character.name] = actor
    if actor not in distribution.charactersByActor:
        distribution.charactersByActor[actor] = []
    distribution.charactersByActor[actor].append(character)

    if actor not in distribution.incompatibilities:
        distribution.incompatibilities[actor] = []
    for partner in character.partners:
        if partner not in distribution.incompatibilities[actor]:
            distribution.incompatibilities[actor].append(partner)

def newDistrib():
    distribution = Distribution()
    for character in characters.values():
        selectedActor = getRandomAvailableActor(character, distribution)
        if selectedActor is None:
            return None
        addCharacterToActor(selectedActor, character, distribution)
        # print(character.name + " ::: " + str(selectedActor))
    return distribution

def removeDistributionDuplicates():
    global distributions
    distributions = [distribution for i in distribution]

def calculateSumLines(characters):
    return sum([int(character.lines) for character in characters])

def diffLines(lines):
    diff = ((lines / 197.25) -1.0) * 100.0
    perct = "{:.1f}%".format(diff)
    if (diff > 0):
        return "+" + perct
    return perct

def calculateLinesInDistribution(distribution):
    return {
        actorName: {
            'lines': calculateSumLines(characters),
            'diff': diffLines(calculateSumLines(characters)),
            'characters': characters
            # 'offset': offsetLines(calculateSumLines(characters)),
        }
        for actorName, characters in distribution.charactersByActor.items()
    }

def nbActorsInDistribution(distribution):
    return len(distribution.charactersByActor.keys())

def offsetLines(distribution):
    lines = [l['lines'] for l in calculateLinesInDistribution(distribution).values()]
    # print(str(lines))
    return max(lines) - min(lines)

def diffDistribution(distribution):
    lines = [l['lines'] for l in calculateLinesInDistribution(distribution).values()]
    return diffLines(lines)

def main():
    global distributions
    buildData()
    # ok ici on a tous nos partenaires de jeu
    printPartners()
    # on genere des distrib aleatoires
    it = 1000
    for i in range(1000):
        print(str(i)+"/"+str(it))
        distribution = newDistrib()
        if distribution is not None and distribution not in distributions:
            distributions.append(distribution)
    # on verifie si les repartitions sont homogenes
    
    for d in distributions:
        offset = offsetLines(d)
        if nbActorsInDistribution(d) == 8 and offset < 140:
            result = ["{}: {} ({} repliques, {}).".format(actorName, info['characters'], info['lines'], info['diff']) for actorName, info in calculateLinesInDistribution(d).items()]
            print("Ecart: {}. Resultat = {}\n".format(str(offset), str(result)))
            # print("LINES OFFSET::: " + str(offset))






if __name__ == "__main__":
    main()
