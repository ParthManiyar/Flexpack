testcase = int(input())
while(testcase>0):
    #print(testcase)
    no_of_tweets = int(input())
    usernames = {}
    for i in range(0,no_of_tweets):
        s = input()
        [username, tweet] = s.split(" ")
        if(usernames.get(username)):
            usernames[username] = usernames[username] + 1 
        else:
            usernames[username] = 1 
            
    max = 0
    for user in usernames:
        if(max<usernames[user]):
            max = usernames[user]

    for user in sorted(usernames):
        if(max==usernames[user]):
            print(user + " "+ str(usernames[user]))
        
    testcase = testcase-1