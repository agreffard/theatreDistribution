#!/usr/bin/env python
import sys
import os

characters = {}
# partners = {}
scenes = {}

header = []

actorsList = {
    'Aurel': 'H',
    'Auriane': 'F',
    'Cannelle': 'F',
    'Clara': 'F',
    'Leonie': 'F',
    'Manu': 'H',
    'Stephane': 'H',
    'Pascal': 'H',
}

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

def getSceneByName(name):
    # print("getSceneByName " + name)
    global scenes
    if name in scenes:
        return scenes[name]
    scene = Scene(name)
    scenes[name] = scene
    return scene

def getSceneName(index):
    # print("getSceneName " + str(index) + " - " + str(len(header)))
    # print(str(header))
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
            print(characterData)
            print("Line {}: {}".format(cnt, line.strip()))
            addLine(characterData)
            cnt += 1
            line = f.readline()


def printPartners():
    print ("################################### PARTENAIRES DE JEU ###################################")
    for k, v in characters.items():
        print(k + " : " + str(v.partners))

def main():
    buildData()
    # ok ici on a tous nos partenaires de jeu
    printPartners()



if __name__ == "__main__":
    main()
