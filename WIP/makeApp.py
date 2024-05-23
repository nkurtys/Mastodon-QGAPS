#Variable Funktions to deal with Mastodon.py

import mastodon
from mastodon import Mastodon
from datetime import datetime
from bs4 import BeautifulSoup


#Function to create a Mastodon App to access Mastodon API via Mastodon.py
'''
Arguments:
    name: name of the App you want to create as a string
    client_string: a list carrying the client_id and client_secret 
    created by Mastodon.create_app() function 
    (Default:False)
Returns:
    clients_id and client_secret in a list
Attention: 
    With every call without client_id and client_secret, they get newly generated. 
    To avoid this it is adviced to only call this function once and save the client_id and client_secret in a comment. From then on 
    use client_id and client_secret to call the function again if needed.
#medibubble.org
#mstdn.social
#medibubble
#sciencemastodon.com
#mstdn.science
'''
def makeApp(instance, client_string=False, content=False):
    if client_string == False:
        client_string = Mastodon.create_app("qgaps", api_base_url=instance[0])
        print('App registration completed on ' + instance)
        
    #Authentication on chosen instance
    App = Mastodon(client_id = client_string[0], 
                    client_secret = client_string[1], 
                    api_base_url = instance)
    print('App authenticated!')


#grab weekly activity of instance
    activity = App.instance_activity()
    print('          week        statuses', 'logins', 'registrations')
    for dic in activity:
        print(dic["week"], dic["statuses"], dic["logins"], dic["registrations"])

#grab toots including hashtag
    print('------------------------------------------------------')
    qfever = App.timeline_hashtag("qfever")
    influenza = App.timeline_hashtag("Influenza", limit=1000)
    corona = App.timeline_hashtag("Corona", limit = 1000)
    print('Toots found on ' + instance + ' including #QFever: ' + str(len(qfever)))
    print('Toots found on ' + instance + ' including #Influenza: ' + str(len(influenza)))
    print('Toots found on ' + instance + ' including #Corona: ' + str(len(corona)))
    print('                                                      ')
    print('------------------------------------------------------')
    print('------------------------------------------------------')
    print('                                                      ')

# Print content of 4 most recent toots if 'content == TRUE'
    if content == True :
        print('Content of the 4 most recent toots on ' + instance + ' mentioning #QFever: ')
        for toot in range(4):
            print('\n')
            html = qfever[toot]["uri"]
            #soup = BeautifulSoup(html, features="html.parser")
            #print(soup.get_text())
            print(html)
        print('                                                      ')
        print('------------------------------------------------------')
        print('------------------------------------------------------')
        print('                                                      ')
        # print('Content of the 4 most recent toots on ' + instance + ' mentioning #Influenza: ')
        # for toot in range(4):
        #     print('\n')
        #     date = influenza[toot]["created_at"]
        #     print(date)
        #     html = influenza[toot]["content"]
        #     soup = BeautifulSoup(html, features="html.parser")
        #     print(soup.get_text())
        
        # print('                                                      ')
        # print('------------------------------------------------------')
        # print('------------------------------------------------------')
        # print('                                                      ')
        # print('Content of the 4 most recent toots on ' + instance + ' mentioning #Corona: ')
        # for toot in range(4):
        #     print('\n')
        #     html = corona[toot]["content"]
        #     soup = BeautifulSoup(html, features="html.parser")
        #     print(soup.get_text())
    
    return client_string
    
def getEntries(instance, client_string):

    #Authentication on chosen instance
    App = Mastodon(client_id = client_string[0], 
                    client_secret = client_string[1], 
                    api_base_url = instance
                    #,ratelimit_method="throw"
                    )
    print('App authenticated')
    
    # Define initial parameters
    limit = 40  # Number of statuses per page
    max_id = None  # Start from the beginning
    min_id = ( int( datetime(2024,5,7,23,59).timestamp() ) << 16 ) * 1000
    lent = 0
    run = 0
    # Fetch timeline statuses page by page
    while True:
        # Fetch a page of statuses
        #statuses = App.timeline_hashtag("covid", limit=limit, max_id=max_id, min_id=min_id)
        statuses = App.timeline_public(limit=limit, max_id=max_id, min_id=min_id)

        # Process each status
        for status in statuses:
            # Process the status as needed
            print(lent)
            lent = lent + 1
            print(status['created_at'])
            

        # Check if there are more pages
        if len(statuses) < 1:
            break  # No more pages

        # Set max_id for the next page
        #max_id = statuses[-1]['id']
        min_id = statuses[0]['id']

        ratelimit = App.ratelimit_remaining
        print(ratelimit)
        if ratelimit == 1:
            run = run + 1
            print("-----------------Run End: " + str(run) + "-----------------------------------")

    

#b=makeApp('mastodon.social')
#print(b) #('dg_42Iu19vFSxFGWAwY5P9J8APY3yt-GrGoe-NE0y4o', 'KqIjPKRl5yWlJb04I7jtv84Tt3IMLVvNNv7FiJmdN-s')

getEntries('https://mastodon.social', ('dg_42Iu19vFSxFGWAwY5P9J8APY3yt-GrGoe-NE0y4o', 'KqIjPKRl5yWlJb04I7jtv84Tt3IMLVvNNv7FiJmdN-s'))

#makeApp('https://mastodon.social', ('dg_42Iu19vFSxFGWAwY5P9J8APY3yt-GrGoe-NE0y4o', 'KqIjPKRl5yWlJb04I7jtv84Tt3IMLVvNNv7FiJmdN-s'), True)
#makeApp('https://mstdn.social', ('tQ7DUJO5A5rVCryCvt5-jUbb1VpYDoSNP4XU5hyFzSw', 'bKDG0wbmv7xMhKX-KuuIa_qc_luwfDzkCLqgL63wlmc'), True)

