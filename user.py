class user:
    def __init__(self,name,username,password,curr_ip,curr_port):
        self.name=name
        self.username=username      #name appended wih roll no. so username will be unique for every user
        self.password=password
        self.curr_ip=curr_ip
        self.curr_port=curr_port
        self.groupList=[]            #list of group names this user is part of
        # self.isOnline=False          #boolean to denote user is online or not

    #Function to return user's ip and port
    def getIpPort(self):
        return self.curr_ip,self.curr_port

    #function receives username,password and dictionary of users: {'username':'password'}
    #returns 1: userid password matches, 0 if userid matches but wrong password, -1 if user doesn't exist
    def signIn(self,username,password,userDict):
        foundFlag=0
        for user in userDict:
            if user==username:
                foundFlag=1
                if userDict[user]==password:
                    
                    #isOnline=True
                    print("User logged in successfully!")
                    return 1
                else:
                    print("UserId and Password doesn't match")
                    return 0
        if foundFlag==0:
            print("Account doesn't exist. Please sign up first")
            return -1
    
    # #Function to log user out of chat application
    # def signOut(self):
    #     isOnline=False

    #Function to display all groups the user is a part of
    def showGroups(self):
        if groupList==[]:
            sys.stderr.write("User is not part of any group yet.")
        else:
            for group in groupList:
                print(group)

    #Function to create group
    def createGroup(self,groupName,allGroups):
        if groupName in allGroups:
            sys.stderr.write("Group already exists.")
            if groupName in groupList:
                sys.stderr.write("And you are already part of it")
            else:
                ans= input("Do you want to join this group? [Y/N]")
                if ans=="Y":
                    joinGroup(groupName,allGroups)
                else:
                    return
        groupList.append(groupName)
        allGroups[groupName]=self.username
        return allGroups
    
    #Function to join group
    def joinGroup(self,groupName,allGroups):
        if groupName not in allGroups:
            sys.stderr.write("Group doesn't exist. Creating group:"+groupName)
            createGroup(groupName,allGroups)
        else:
            allGroups[groupName].append(self.username)
    
    #def broadcast a msg/file to a group
    def broadcastToGroup(self,messageObj, groupName):
        pass

    #def send msg/file to single user
    def sendToUser(self,messageObj, username):
        pass
