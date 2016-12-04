import random
import math
import csv
import matplotlib.pyplot as plt

#random.seed(57)


scoreA = 0
scoreB = 0

plotPointsNormal = []
def game(ra, rb):
    global scoreA
    global scoreB

    plotPointsNormal.append(scoreA + scoreB)

    prob = ra / (ra + rb)

    if (scoreA >= 11 or scoreB >= 11) and math.fabs(scoreA - scoreB) >= 2:
        result = (scoreA, scoreB)
        scoreA = scoreB = 0
        return result

    if random.random() < prob:
        scoreA += 1
    else:
        scoreB += 1

    return game(ra, rb)

def winProbability(ra, rb, n):
    winsA = 0

    for i in range(n):
        result = game(ra, rb)
        winsA += result[0] > result[1]

    return winsA / n

def readList():
    with open('test.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        return [(int(row[0]), int(row[1])) for row in reader]

def makePlot(probList):
    probabilities = [row[0] / (row[0] + row[1]) for row in probList]
    skill = [row[0] / row[1] for row in probList]

    plt.plot(skill, probabilities, 'ro')

    plt.axis([0, 4, 0, 1])
    plt.xlabel('ra / rb')
    plt.ylabel('Probability for A to win')
    plt.show()

# Even though for one specific game the chance of A winning does not change,
# repeated games the overall probability increases
def simulateUntilProbability(ra, rb, desiredProb):
    i = 1 # Start with 1 game
    prob = ra / (ra + rb) # Calculate base probability of A winning

    # As long as the probability of a winning "i" games is lower than the desired probability
    # increase count of games played
    while 1 - prob ** i < desiredProb:
        i += 1

    return i
#print(simulateUntilProbability(60, 40, 0.9))

plotPointsEnglish = []
playUntilDecision = 0
def englishGame(ra, rb, isA = True, nRallies = 0):
    global scoreA
    global scoreB
    global playUntilDecision
    global plotPointsEnglish

    plotPointsEnglish.append(scoreA + scoreB)

    prob = ra / (ra + rb)
    prob = prob if isA else 1 - prob

    # we neglect who hits 8 first for the sake simplicity because either way playUntilDecision is random
    if playUntilDecision == 0 and scoreA == 8 and scoreB == 8:
        playUntilDecision = random.randint(9, 10)

    # we play fixed until 9 if we haven't hit 8-8
    playUntil = 9 if playUntilDecision == 0 else playUntilDecision

    if (scoreA >= playUntil or scoreB >= playUntil):
        result = (scoreA, scoreB)
        scoreA = scoreB = playUntilDecision = 0
        return result

    if random.random() < prob:
        if isA:
            scoreA += 1
        else:
            scoreB += 1
    else:
        isA = not isA

    return englishGame(ra, rb, isA, nRallies + 1)

def makeTimePlot(ra, rb):
    # Assumptions:
    # Due to the fact that in PARS scoring, every score is exactly one rally, and in
    # English scoring one score can involve many rallies, the assumption is made that
    # an English game will take an increasingly long time the closer the skill is between players as
    # there is more chance that one point has multiple rallies.
    # Theoretically in a simulation if one player has an significantly higher skill than another,
    # an English game would be faster than a PARS game as it is to 9 points not 11.
    game(ra, rb)
    englishGame(ra, rb)

    plt.plot(plotPointsNormal)
    plt.plot(plotPointsEnglish)

    plt.xlabel('Game Time')
    plt.ylabel('Combined Score')
    plt.title('Player A: {}, Player B: {}'.format(ra, rb))
    plt.show()
makePlot(readList())
