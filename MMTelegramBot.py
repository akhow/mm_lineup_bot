import requests

class MMTelegramBot:
    def __init__(self, token):
        self.token = token
        self.base = 1.45
        self.weights = []
        self.ourLineup = []
        self.theirLineup = []
    
    def setBase(self, weight):
        self.base = weight

    def generateLineup(self, ourLineupFile, theirLineupFile):
        f=open(ourLineupFile, 'r')
        next(f)
        ourLineup = []

        for x in f:
            weight = 0
            userinfo = x.split(",")
            userinfo[1] = int(userinfo[1])
            for l in self.weights:
                if userinfo[0] == l[0]:
                    weight = l[1]
            userinfo.append(userinfo[1]+weight)
            ourLineup.append(userinfo)

        while len(ourLineup) < 16:
            ourLineup.append(["LeagueBot",1000,1000])
        ourLineup.sort(key=lambda ourLineup: ourLineup[2])


        f.close()
        f=open(theirLineupFile, 'r')

        theirLineup = []

        for y in f:
            userinfo = y.split(",")
            userinfo[1] = int(userinfo[1])
            theirLineup.append(userinfo)

        while len(theirLineup) < 16:
            theirLineup.append(["LeagueBot",70])
        theirLineup.sort(key=lambda theirLineup: theirLineup[1])

        f.close()

        self.ourLineup = ourLineup
        self.theirLineup = theirLineup

        return ourLineup, theirLineup

    def generateLineupMessage(self, ourLineup, theirLineup):
        message = ""
        for z in range(16):
            message += ourLineup[15-z][0] + " vs " + theirLineup[15-z][0] + " [" + str(ourLineup[15-z][1]-theirLineup[15-z][1]) + "]\n"
        return message

    def saveLineups(self, ourLineup, theirLineup):
        f=open("matchups.csv",'w')
        f.write("TEAM,OFF,ADJ OFF\n")
        for z in range(16):
            f.write(ourLineup[15-z][0] + "," + str(ourLineup[15-z][1])+","+str(ourLineup[15-z][2])+"\n")
        f.close()

    def generateWeights(self, file):
        f=open(file, 'r')
        lineup = []
        next(f)

        for x in f:
            userinfo = x.split(",")
            userinfo[1] = int(userinfo[1])
            userinfo[2] = int(userinfo[2])
            userinfo[3] = float(userinfo[3])
            weight = [userinfo[0], round(1.45**(userinfo[3]/userinfo[2]), 2)]
            lineup.append(weight)

        f.close()
        lineup.sort(key=lambda lineup: lineup[1])
        lineup.reverse()

        self.weights = lineup

        return lineup
    
    def saveWeights(self, weights):
        f=open("weights.csv", 'w')
        for z in weights:
            f.write(z[0] + "," +str(z[1])+"\n")
        f.close()

    def loadWeights(self, file):
        g=open(file, 'r')
        weights = []
        for w in g:
            weight = w.split(",")
            weight[1] = float(weight[1])
            weights.append(weight)
        g.close()

        self.weights = weights

        return weights
    
    def generateWeightMessage(self, weights):
        message = "Here are this week's scales! Add them to your offensive overall to determine matchmaking.\n"
        for w in weights:
            message += w[0] + ": " + str(w[1])+"\n"
        return message
    
    def sendMessage(self, chat_id, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={chat_id}&text={message}"
        tel = requests.get(url).json()
        message_id = str(tel['result']['message_id'])
        print(message_id)

        url = f"https://api.telegram.org/bot{self.token}/pinChatMessage?chat_id={chat_id}&message_id={message_id}"
        print(requests.get(url).json())
    
    def deleteMessage(self, chat_id, message_id):
        url = f"https://api.telegram.org/bot{self.token}/deleteMessage?chat_id={chat_id}&message_id={message_id}"
        print(requests.get(url).json())

