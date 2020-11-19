import threading
import time
import pythonFiles.shared_things as shared_things
import json
# Our thread class
class MinTimer (threading.Thread):

    def __init__(self, x, oldEpoch):
        self.__x = x
        self.__oldEpoch = oldEpoch
        threading.Thread.__init__(self)

    def run (self):
        while(self.__x > 0 and (self.__oldEpoch == shared_things.oldEpoch or self.__oldEpoch =="lobbyTimer") and shared_things.inChampionSelect == True):
            #print("Thread >0 self.__epoch == shared_things.epoch")
            timeLeft = {"time":self.__x}
            fileName = "timer"
            if(self.__oldEpoch =="lobbyTimer"):
                fileName = "lobbyTimer"
            filePathNameWithExt = "./jsonFiles/"+fileName + ".json"
            with open(filePathNameWithExt, "w") as fp:
                json.dump(timeLeft, fp)
            self._update()
            time.sleep(1)
        timeLeft = {"time":self.__x}
        fileName = "timer"
        if(self.__oldEpoch =="lobbyTimer"):
            #print("OLD EPOCH LOBBY TIMER")
            self.__x = 400
            if(shared_things.inChampionSelect == False):
                self.__x = 400
                #print("OLD EPOCH LOBBY TIMER")
            fileName = "lobbyTimer"
        filePathNameWithExt = "./jsonFiles/"+fileName + ".json"
        timeLeft = {"time":self.__x}
        with open(filePathNameWithExt, "w") as fp:
            json.dump(timeLeft, fp)
        print("STOPPING THREAD")
        return

    def _update(self):
        print("Coundown Timer: ",str(self.__x))
        self.__x = self.__x-1
    def setXAs(self):
        self.__x = 0
        return
