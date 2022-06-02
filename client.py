# -*- coding: utf-8-*-
from Imgood.linepy import *
from Imgood.akad import *
from Imgood.linepy.style import *
from justgood import imjustgood
from time import sleep
from gtts import gTTS
from datetime import datetime
from bs4 import BeautifulSoup
from threading import Thread, active_count
import os,traceback,sys,json,time,ast,requests,re,random,pytz
from Liff.ttypes import LiffChatContext, LiffContext, LiffSquareChatContext, LiffNoneContext, LiffViewRequest
"""
          **  JUSTGOOD MINI SELFBOT  ** 

        BOT TYPE      -  MINI SELFBOT
        DEVELOPER     -  IMJUSTGOOD.COM/TEAM
        SOURCE LIB    -  PYPI/LINEPY
        MEDIA API     -  PYPI/JUSTGOOD
"""
login = json.loads(open('Data/token.json','r').read())
setting = json.loads(open('Data/settings.json','r').read())
cctv = json.loads(open('Data/cctv.json','r').read())
if login["token"] == "":
    client = LINE(login["email"],login["password"])
else:client = LINE(idOrAuthToken=login["token"])

flex = Autobots()
clPoll = OEPoll(client)
starting = time.time()
mid = client.profile.mid
media = imjustgood(setting["apikey"])
host = "https://{}".format(setting["main"])
oburl = client.server.LINE_OBJECT_URL
protectMax = setting["proMax"]
protectStaff = setting["proStaff"]
read = {
    "addwhitelist":False,
    "delwhitelist":False, 
    "addblacklist":False,
    "delblacklist":False,
    "dual":False,
    "dual2":False,
    "pp":False,
    "gpict":{},
    "cctv":{},
    "imgurl":{},
    "wmessage":{},
    "lmessage": ""
}

"""
                    ** LINE OPERATION FUNCTION ** 

"""
def Oup(op):
       if op.type in [19,133]:
           if op.param3 not in mid:
               if op.param1 in protectStaff:
                   th = Thread(target=prostaff(op,))
                   th.start()
                   th.join()
               elif op.param1 in protectMax:
                   th =Thread(target=promax(op,))
                   th.start()
                   th.join()
           else:kekick(op)       

       if op.type in [13,124]:
           if op.param1 in protectMax:
               th = Thread(target=proinvite(op,))
               th.start()
               th.join()

       if op.type == 55 :
           try:
             target = [ax.mid for ax in client.getGroup(op.param1).members]
             if op.param1 in read["cctv"]:
                if op.param2 in target:
                    if op.param2 not in read["cctv"][op.param1]:
                        user = ["Monyet lu","hai homo sapien","homo sapiens apa kabar?","piye mbakmu ayu ra?"]
                        data = random.choice(user)
                        text = "• @!  {}".format(data)       
                        client.sendMention(op.param1,text,[op.param2])
                        read["cctv"][op.param1][op.param2] = True
             if op.param1 in cctv['readPoint']:
                 timezone = pytz.timezone("Asia/Jakarta")
                 timing = datetime.now(tz=timezone)
                 timer = timing.strftime('%H.%M')
                 if op.param2 in cctv['readPoint'][op.param1]:pass
                 else:
                   cctv['readPoint'][op.param1][op.param2] = True
                   cctv['readMember'][op.param1][op.param2] = "Time: {}".format(timer)
                   with open('Data/cctv.json', 'w') as fp:
                      json.dump(cctv, fp, sort_keys=True, indent=4)
           except:pass

       if op.type in [17,130]:
           if op.param1 in setting["welcome"]:
              if op.param2 not in setting["blacklist"]:
                  jangan = client.getGroup(op.param1)
                  if op.param1 in read["wmessage"]: 
                     text = "Hi @! \nWelcome to " + jangan.name + "\n" + read["wmessage"][op.param1]
                     client.sendMention(op.param1,text,[op.param2])
                     client.sendPage(op.param1)
                  else:
                     text = "Hi @! \nWelcome to " + jangan.name 
                     client.sendMention(op.param1,text,[op.param2])
                     client.sendPage(op.param1)


       if op.type in [15,128]:
          if setting["leave"] == True:
              if op.param2 not in setting["blacklist"]:
                  jangan = client.getGroup(op.param1)
                  if read["lmessage"] !="":
                      mess = read["lmessage"] + " @! "
                      client.sendMention(op.param1,mess,[op.param2])
                  else:
                      mess = "Good bye @! "
                      client.sendMention(op.param1,mess,[op.param2])


       if op.type == 5 :
           if setting["adders"] == True:
               if op.param1 not in setting["blacklist"]:
                   if setting["addmsg"] == "":client.sendMention(op.param1,"Hi @! \nThank u for add me :)",[op.param1])
                   else:
                      text = "Hi @! \n" + setting["addmsg"]
                      client.sendMention(op.param1,text,[op.param1])


       if op.type in [13,17,55,124,130]:
          if op.param2 in setting["blacklist"]:
              try:client.kickoutFromGroup(op.param1,[op.param2])
              except:pass


       if op.type in [32,126]:
           if op.param1 in protectMax:
               if op.param2 not in setting["whitelist"]:
                  setting["blacklist"].append(op.param2)
                  with open('Data/settings.json', 'w') as fp:
                    json.dump(setting, fp, sort_keys=True, indent=4)
                  try:
                     client.kickoutFromGroup(op.param1,[op.param2])                     
                     client.findAndAddContactsByMid(op.param3)
                     client.inviteIntoGroup(op.param1,[op.param3])
                  except:pass                   

       if op.type in [11,122]:
           if op.param1 in protectMax and op.param3 == "4":
               if op.param2 not in setting["whitelist"]:
                   setting["blacklist"].append(op.param2)
                   with open('Data/settings.json', 'w') as fp:
                      json.dump(setting, fp, sort_keys=True, indent=4)
                   hoax = client.getGroup(op.param1)
                   if hoax.preventedJoinByTicket == False:
                      abc = client.getGroup(op.param1)
                      abc.preventedJoinByTicket = True
                      client.updateGroup(abc)
                      try:client.kickoutFromGroup(op.param1,[op.param2])
                      except:pass
               else:
                  hoax = client.getGroup(op.param1)
                  if hoax.preventedJoinByTicket == False:
                     abc = client.getGroup(op.param1)
                     abc.preventedJoinByTicket = True
                     client.updateGroup(abc)                  
      
       if op.type == 11:
           if op.param1 in protectMax and op.param3 == "1":
               if op.param2 not in setting["whitelist"]:
                   setting["blacklist"].append(op.param2)
                   with open('Data/settings.json', 'w') as fp:
                      json.dump(setting, fp, sort_keys=True, indent=4)
                   hoax = client.getGroup(op.param1).name
                   if hoax not in setting["gname"][op.param1]:
                      abc = client.getGroup(op.param1)
                      abc.name = setting["gname"][op.param1]
                      client.updateGroup(abc)
                      try:client.kickoutFromGroup(op.param1,[op.param2])
                      except:pass
               else:
                  abc = client.getGroup(op.param1).name                     
                  setting["gname"][op.param1] = abc
                  with open('Data/settings.json', 'w') as fp:
                     json.dump(setting, fp, sort_keys=True, indent=4)

       if op.type == 25:
            try:
                msg = op.message
                txt = msg.text
                if msg.toType in [0,2]:
                   to = msg.to
                   ids = msg.id
                   msg.to = msg.to
                   if msg.contentType == 0:
                      if None == txt:
                          return
                      cmd = txt.lower()
                      rname = setting["rname"].lower() + " "
                      link = txt[txt.find(":")+2:]
                      search = txt[txt.find(":")+2:].lower()
                      if cmd== ".help" or cmd== rname + "help":
                          if cmd.startswith('.'):label = cmd.replace('.','')
                          else:label = cmd.replace(rname,"")
                          menu = "       Media             Stealing\n       Utility              Listing\n       Settings         Protection\n       Groupset       Customing\n       ───────────\n       Use 「 • 」for prefix."
                          client.help(msg.to,label,menu)

                      if cmd== ".me" or cmd== rname + "me":
                          client.me(msg.to)

                      if cmd in [".speed","sp","speed",".sp"] or cmd== rname + "speed":                      
                          rend = time.time()
                          client.getProfile() 
                          yosh = time.time() - rend
                          client.sendMention(msg.to, "「   @!   」\nTime: %.4f"%(yosh),[mid])

                      if cmd in ["rname",".rname","mykey",".mykey"] or cmd== rname + "rname":
                          client.sendMessage(msg.to,setting["rname"].title())

                      if cmd== ".kickall" or cmd== rname + "kickall" or cmd == setting["keykick"].lower():
                         if msg.toType == 2:
                            hoax = client.getGroup(msg.to)
                            client.sendMessage(msg.to,"Goodbye Bitch ~")
                            for ax in hoax.members:
                               if ax.mid not in setting["whitelist"]:
                                  client.kickoutFromGroup(msg.to,[ax.mid])
                            client.sendMessage(msg.to,"Rubish has been cleared")

                      if cmd== ".unsend" or cmd== rname + ".unsend":       
                         client.sendMessage(msg.to,"「   Usage 」\n.unsend num")
                      if cmd.startswith(".unsend ") or cmd.startswith(rname + "unsend "):
                         msgid = cmd.split("unsend ")[1]                        
                         if msgid.isdigit():
                            mess = client.getRecentMessagesV2(msg.to,999)                     
                            mes = []
                            for x in mess:
                                if x._from == mid:    
                                   mes.append(x.id)                            
                                   if len(mes) == int(msgid):break                       
                            for b in mes:
                                try:client.unsendMessage(b)
                                except:pass
                         else:client.sendMessage(msg.to,"「   Usage 」\n.unsend num")

                      if cmd== ".runtime" or cmd== rname + "runtime":
                         high = time.time() - starting
                         voltage =  "Selfbot has been running for:\n"+runtime(high)
                         client.sendMessage(msg.to,f"{voltage}")

                      if cmd== ".reboot":
                          client.sendMessage(msg.to,"restarting..")
                          restart()

                      if cmd== ".allowliff":
                         try:
                            liff()
                            client.sendFlexText(msg.to,"Flex enabled.")
                         except:client.sendReplyMessage(ids,to,"Click and allow url to enable flex\nline://app/1602876096-e9QWgjyo")

                      if cmd== ".tagall":
                         group = client.getGroup(msg.to)
                         midMembers = [contact.mid for contact in group.members]
                         midSelect = len(midMembers)//20
                         for mentionMembers in range(midSelect+1):
                             ret_ = "• MENTIONALL\n• IMJUSTGOOD\n• MINI SELFBOT\n"
                             no = 0;dataMid = [];
                             for dataMention in group.members[mentionMembers*20 : (mentionMembers+1)*20]:
                                 dataMid.append(dataMention.mid)
                                 ret_ += "\n{}. @!\n".format(str(no))
                                 no = (no+1)
                             ret_ += "\n\n「 Total {} Members 」".format(str(len(dataMid)))
                             client.sendMention(msg.to, ret_, dataMid)

                      if cmd.startswith(".kick ") or cmd.startswith(rname + "kick "):
                          if 'MENTION' in msg.contentMetadata.keys()!= None:
                              names = re.findall(r'@(\w+)', cmd)
                              mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                              mentionees = mention['MENTIONEES']
                              Mmbers = [a.mid for a in client.getGroup(msg.to).members]
                              hole = []
                              for mention in mentionees:
                                  if mention["M"] not in hole:
                                     if mention['M'] not in Mmbers:
                                        hole.append(mention["M"])
                              for mmq in hole:
                                  try:client.kickoutFromGroup(msg.to, [mmq])
                                  except:client.sendMessage(msg.to, "Gagal son.")

                      if cmd.startswith(".invite ") or cmd.startswith(rname + "invite "):
                          if 'MENTION' in msg.contentMetadata.keys()!= None:
                              names = re.findall(r'@(\w+)', cmd)
                              mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                              mentionees = mention['MENTIONEES']
                              Mmbers = [a.mid for a in client.getGroup(msg.to).members]
                              hole = [];
                              for mention in mentionees:
                                  if mention["M"] not in hole:
                                     if mention['M'] not in Mmbers:
                                        hole.append(mention["M"])
                              for mmq in hole:
                                  try:
                                      client.findAndAddContactsByMid(mmq)
                                      client.inviteIntoGroup(msg.to, [mmq])
                                  except:client.sendMessage(msg.to, "Gagal son.")

                      if cmd.startswith(".locate") or cmd.startswith(rname + "locate"):
                          cmdx = cmd.split(' @')[0]
                          if cmd.startswith('.'):label = cmdx.replace('.','')
                          else:label = cmdx.replace(rname,"")
                          gruplist = client.getGroupIdsJoined()
                          kontak = client.getGroups(gruplist)
                          if 'MENTION' in msg.contentMetadata.keys()!= None:
                              names = re.findall(r'@(\w+)', cmd)
                              mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                              mentionees = mention['MENTIONEES']
                              no = 1; detect = [];menu= "Groups Joined:\n\n"
                              for mention in mentionees:
                                  profile = client.getContact(mention['M'])
                                  for xx in range(len(kontak)):
                                     located = [x.mid for x in kontak[xx].members]
                                     if mention['M'] in located:
                                        detect.append(kontak[xx].id)
                                        menu += " {}. {} ({})\n".format(no,kontak[xx].name,len(located))
                                        no = (no+1)
                              if detect == []:client.sendMessage(msg.to,"Nothing found.")
                              else:
                                 menu += "\n\nTotal: {} Groups.".format(len(detect))
                                 data ={"type":"bubble","size":"kilo","body":{"type":"box","layout":"vertical","backgroundColor": "#000000","contents":[{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","contents":[{"type":"image","url":"{}{}".format(oburl,profile.pictureStatus),"aspectRatio":"1:1","aspectMode":"cover"}],"cornerRadius":"100px"}],"alignItems":"center","paddingTop":"50px"},{"type":"box","layout":"vertical","contents":[{"type":"text","text":"{}".format(profile.displayName),"color":"#FFC300","weight":"bold","align":"center"},{"type":"text","text":"Tetaplah mesum","color":"#FFC300cc","align":"center","size":"xxs"}],"paddingAll":"10px"},{"type":"box","layout":"vertical","contents":[{"type":"text","text":label.upper(),"color":"#FFC300","weight":"bold","size":"xxs"}],"position":"absolute","borderWidth":"1px","borderColor":"#ffffffcc","paddingStart":"8px","paddingEnd":"8px","paddingTop":"5px","paddingBottom":"5px","offsetTop":"10px","offsetStart":"10px","cornerRadius":"20px"},{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","contents":[{"type":"text","text":menu,"color":"#FFC300","size":"xs","wrap":True}],"paddingAll":"20px","backgroundColor":"#111111"}],"paddingAll":"20px","paddingTop":"5px"}],"paddingAll":"0px"},"styles":{"body":{"backgroundColor":"#161e2b"}}}
                                 client.sendFlex(msg.to,data)

                      if cmd.startswith(".broadcast: ") or cmd.startswith(rname + "broadcast: "):
                         bc = cmd.split("broadcast: ")[1]
                         groups = client.getGroupIdsJoined()
                         allGc = client.getGroups(groups)
                         youBc = "「   Broadcast Message   」".format(host,len(allGc),bc)
                         for x in range(len(allGc)):
                             client.sendMention(allGc[x].id, youBc,[mid])                           
                         client.sendReplyMessage(id,to,"Success Broadcasted on {} groups.".format(len(allGc)))
while True:
    try:
        ops = clPoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                clPoll.setRevision(op.revision)
                t1 = Thread(target=Oup(op,))
                t1.start()
                t1.join()
    except Exception as error:
        client.log("「   ERROR 」\n{}".format(str(error)))
        traceback.print_tb(error.__traceback__)
