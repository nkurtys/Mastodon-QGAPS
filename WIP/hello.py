import requests as rq
import mastodon
from mastodon import Mastodon
import json

'''
m = Mastodon(access_token="_t2HmVBWVXiRpp08Guo9fhIlI_R1onhuR9Ys0MPDkWk", api_base_url="mastodon.social")

activity = m.instance_activity()
print(activity[0].keys())
for dic in activity:
    print(dic["week"], dic["statuses"], dic["logins"], dic["registrations"])
'''

'''
#App registration mastodon.social - only needed once
AppInfo = Mastodon.create_app("QGAPS", api_base_url="mastodon.social")
print(AppInfo)
#('FHZLsdZArV02VmQtTqst7ejmh03ous-m_Sfd0JQ7vrY', 'JeYPRuKyk3Z7MHUNpsl0CWWiog7-BBB1uWPdf7nVGOs')
'''
'''
#App registration mstdn.social - only needed once
AppInfo = Mastodon.create_app("QGAPS", api_base_url="mstdn.social")
print(AppInfo)
#('tQ7DUJO5A5rVCryCvt5-jUbb1VpYDoSNP4XU5hyFzSw', 'bKDG0wbmv7xMhKX-KuuIa_qc_luwfDzkCLqgL63wlmc')
'''
'''
#App registration medibubble.org - only needed once
AppInfo = Mastodon.create_app("QGAPS", api_base_url="medibubble.org")
print(AppInfo)
#('THaFWhTyGIY5aTiQFu5LrClZrPc1bub5IF97ZnKH7d0', 'eSjzvu-xOWHprIHM69-aTzHQNpihFilCzgsT8KOp6dA')
'''

'''
#App registration sciencemastodon.com - only needed once
AppInfo = Mastodon.create_app("QGAPS", api_base_url="sciencemastodon.com")
print(AppInfo)
#('ViAJCbtjCBRkv7hV3iiGxfbF0RGGGYwYcfd5ZmB8Dxw', 'OYXwh-BrC4AiPbHjZ8xTz9yk7FNnML320U7LROY6xK0')
'''
'''
#App registration biologists.social - only needed once
AppInfo = Mastodon.create_app("QGAPS", api_base_url="biologists.social")
print(AppInfo)
#('Bc_wwLAGRJ4MqGFH8DbM2u5ezBQxiinbI9BpipCwzOM', '0yrgCLaQEEQyRxi0_69WsBO31D_TQvDdJzGMvOecHpY')
'''

'''
#App registration mstdn.science - only needed once
AppInfo = Mastodon.create_app("QGAPS", api_base_url="mstdn.science")
print(AppInfo)
#('7lik8ACZhPN252re_JMNoNR_CinrqHkNwRDI0pTojzg', 'TdHtOaUSh_13FgWcfyvxNda8yZ6In6CuFCLe0LDGrmA')
'''
# m = Mastodon(access_token="_t2HmVBWVXiRpp08Guo9fhIlI_R1onhuR9Ys0MPDkWk", api_base_url="mastodon.social")
# res = m.search('qfever')
# print(res[0]['content'])
#Authentication mastodon.social
App = Mastodon(client_id = 'FHZLsdZArV02VmQtTqst7ejmh03ous-m_Sfd0JQ7vrY', 
                  client_secret = 'JeYPRuKyk3Z7MHUNpsl0CWWiog7-BBB1uWPdf7nVGOs', 
                  api_base_url = "mastodon.social")



    

#Authentication mastdn.social
mstdnApp = Mastodon(client_id = 'tQ7DUJO5A5rVCryCvt5-jUbb1VpYDoSNP4XU5hyFzSw', 
                  client_secret = 'bKDG0wbmv7xMhKX-KuuIa_qc_luwfDzkCLqgL63wlmc', 
                  api_base_url = "mstdn.social")

#Authentication medibubble.org
bubbleApp = Mastodon(client_id = 'THaFWhTyGIY5aTiQFu5LrClZrPc1bub5IF97ZnKH7d0', 
                  client_secret = 'eSjzvu-xOWHprIHM69-aTzHQNpihFilCzgsT8KOp6dA', 
                  api_base_url = "medibubble.org")

#Authentication sciencemastodon.com
scienceApp = Mastodon(client_id = 'ViAJCbtjCBRkv7hV3iiGxfbF0RGGGYwYcfd5ZmB8Dxw', 
                  client_secret = 'OYXwh-BrC4AiPbHjZ8xTz9yk7FNnML320U7LROY6xK0', 
                  api_base_url = "sciencemastodon.com")

#Authentication biologists.social
bioApp = Mastodon(client_id = 'Bc_wwLAGRJ4MqGFH8DbM2u5ezBQxiinbI9BpipCwzOM', 
                  client_secret = '0yrgCLaQEEQyRxi0_69WsBO31D_TQvDdJzGMvOecHpY', 
                  api_base_url = "biologists.social")

#Authentication mstdn.social
mscienceApp = Mastodon(client_id = '7lik8ACZhPN252re_JMNoNR_CinrqHkNwRDI0pTojzg', 
                  client_secret = 'TdHtOaUSh_13FgWcfyvxNda8yZ6In6CuFCLe0LDGrmA', 
                  api_base_url = "mstdn.science")

activity = App.instance_activity()
print(activity[0].keys())
for dic in activity:
    print(dic["week"], dic["statuses"], dic["logins"], dic["registrations"])

activity = mstdnApp.instance_activity()
print(activity[0].keys())
for dic in activity:
    print(dic["week"], dic["statuses"], dic["logins"], dic["registrations"])

activity = bubbleApp.instance_activity()
print(activity[0].keys())
for dic in activity:
    print(dic["week"], dic["statuses"], dic["logins"], dic["registrations"])

activity = scienceApp.instance_activity()
print(activity[0].keys())
for dic in activity:
    print(dic["week"], dic["statuses"], dic["logins"], dic["registrations"])

activity = bioApp.instance_activity()
print(activity[0].keys())
for dic in activity:
    print(dic["week"], dic["statuses"], dic["logins"], dic["registrations"])

'''
activity = mscienceApp.instance_activity()
print(activity[0].keys())
for dic in activity:
    print(dic["week"], dic["statuses"], dic["logins"], dic["registrations"])
'''
#medibubble.org
#mstdn.social
#medibubble
#sciencemastodon.com
#mstdn.science

response = App.timeline_hashtag("qfever")
print(len(response))
print(response[0]["id"])


mstdn = mstdnApp.timeline_hashtag("qfever")
print(len(mstdn))
bubble = mstdnApp.timeline_hashtag("qfever")
print(len(bubble))
science = scienceApp.timeline_hashtag("qfever")
print(len(science))
bio = bioApp.timeline_hashtag("qfever")
print(len(bio))
ms = mscienceApp.timeline_hashtag("qfever")
print(len(ms))

#print(bio[0]["uri"])

#print(response[0]["content"])
print(response[0].keys())
