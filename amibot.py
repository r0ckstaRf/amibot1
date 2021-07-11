
import amino
import time
from gtts import gTTS
import requests

client=amino.Client()

client.login(email="levkametov3@gmail.com",password="24112006")

print("logged in.....")

cid="165541630"
cidy=165541630

adm=[]
##admx=[http://aminoapps.com/p/226srq]

admx=["http://aminoapps.com/p/226srq","http://aminoapps.com/p/i347qjy"]

for i in admx:
	try:
		w=client.get_from_code(i).objectId
		adm.append(w)
	except:
		print("invalid admin links/format")
subclient=amino.SubClient(comId=cid,profile=client.profile)

WARNS = []
ANTI_SPAM = {}
JOIN_LEAVE_DETECTOR = {}

print("inside community")

def on_message(data):
    user_id = data.message.author.userId
    if user_id != client.userId:
        msg_type = data.message.type
        if msg_type != 0:
            media_type = data.message.mediaType
            content = data.message.content
            if content is not None and media_type == 0:
                sub_client.kick(chatId=data.message.chatId, userId=user_id, allowRejoin=False)
                print(f"{user_id} удален из чата за отправку системного сообщения")

@client.event("on_image_message")
@client.event("on_text_message")
def on_antispam(data):
    user_id = data.message.author.userId
    if user_id != client.userId:
        if ANTI_SPAM.get(user_id) is None:
            ANTI_SPAM[user_id] = int(time.time())
        elif int(time.time()) - ANTI_SPAM[user_id] <= 1.0:
            if WARNS.count(user_id) >= 4:
                sub_client.kick(userId=user_id, chatId=data.message.chatId, allowRejoin=False)
                print(f"{user_id} удален из чата за спам")
                for i in WARNS:
                    if i == user_id:
                        WARNS.remove(user_id)
            else:
                WARNS.append(user_id)
        elif int(time.time()) - ANTI_SPAM[user_id] > 1:
            ANTI_SPAM[user_id] = int(time.time())
            for i in WARNS:
                if i == user_id:
                    WARNS.remove(user_id)


@client.event("on_group_member_join")
def on_group_member_join(data):
	if data.comId==cidy:
		try:
			x=data.message.author.icon
			response=requests.get(f"{x}")
			file=open("sample.png","wb")
			file.write(response.content)
			file.close()
			img=open("sample.png","rb")
			subclient.send_message(chatId=data.message.chatId,message=f"""[c]Приветствую тебя в чате<${data.message.author.nickname}$>!\n[c] Напиши -help чтобы найти больше""",embedId=data.message.author.userId,embedTitle=data.message.author.nickname,embedLink=f"ndc://x{cid}/user-profile/{data.message.author.userId}",embedImage=img,mentionUserIds=[data.message.author.userId])
			print(f"\nwelcomed {data.message.author.nickname} to gc ")
		except Exception as e:
			print(e)
				
@client.event("on_group_member_leave")
def on_group_member_leave(data):
	if data.comId==cidy:
		try:
			subclient.send_message(chatId=data.message.chatId,message="""[c]Умер""")
			print(f"Someone left the gc")
		except Exception as e:
			print(e)

@client.event("on_avatar_chat_start")
def on_avatar_start_chat_start(data):
	if data.comId==cidy:
		if subclient.get_chat_thread(data.message.chatId).title!=None:
			try:
				subclient.send_message(chatId=data.message.chatId,message=f"Страшно вкусно и он абасрался <${data.message.author.nickname}$>",mentionUserIds=[data.message.author.userId])
				subclient.kick(userId=data.message.author.userId,chatId=data.message.chatId,allowRejoin=True)
				print(f"Someone spamed gc")
			except Exception as e:
				print(e)		

l=[]
@client.event("on_text_message")
def on_text_message(data):
	if data.comId==cidy:
		ex=data.message.content
		cd=ex.split(' ')
		x=cd[0]
		c=cd[1:]
		#print(c)
		adx=[]
		for w in cd:
			adx.append(w)
		print(adx)
		#m=data.message.messageType
		if ex:
			for i in adx:
				if len(i)<=50:
					if i[:23]=="http://aminoapps.com/p/" or i[:23]=="http://aminoapps.com/c/":
						fok=client.get_from_code(i)
						cidx=fok.path[1:fok.path.index("/")]
						if cidx!=cid:
							try:
								subclient.delete_message(chatId=data.message.chatId,messageId=data.message.messageId,asStaff=False)
								#subclient.kick(chatId=data.message.chatId,userId=data.message.author.userId,allowRejoin=True)
								s=subclient.get_chat_thread(data.message.chatId).title
								subclient.start_chat(userId=adm,message=f"ndc://x{cid}/user-profile/{data.message.author.userId} was advertisng in {s}")
								
								subclient.send_message(chatId=data.message.chatId,message="[c]Не рекламить здесь!!")
								print("spotted advertiser")
							except Exception as e:
								print(e)
			if x.lower()=="-info" and c==[]:
				try:
					subclient.send_message(chatId=data.message.chatId,message="[c]Привет я бот могу приветствовать и прощаться с людьми, когда они уходят")
					print(f"Info requested by {data.message.author.nickname}")
				except Exception as e:
					print(e)
			if x.lower()=="-global":
				try:
					for i in c:
						d=client.get_from_code(i).objectId
					subclient.send_message(chatId=data.message.chatId,message=f"""Глобальный айди :- 
ndc://g/user-profile/{d}""")
					print(f"Info requested by {data.message.author.nickname}")
				except Exception as e:
					print(e)
			if x.lower()=="-clear":
				if x.lower() not in l:
					try:
						for i in c:
							d=int(i)
						a=subclient.get_chat_messages(chatId=data.message.chatId,size=d)
						if d<=5:
							for i in a.messageId:
								subclient.delete_message(chatId=data.message.chatId,messageId=i,asStaff=True,reason="clear")
							subclient.send_message(chatId=data.message.chatId,message="[ci]Очищено")
							print(f"Info requested by {data.message.author.nickname}")
						else:
							subclient.send_message(chatId=data.message.chatId,message="[ci]Не могу очистить больше 5")
					except Exception as e:
						print(e)
				else:
					subclient.send_message(chatId=data.message.chatId,message="Команда clear заблокирована")
			if x.lower()=="-lock" and c==[]:
				try:
					subclient.send_message(chatId=data.message.chatId,message=f"Заблокированные команды: {l}")
					print(f"Info requested by {data.message.author.nickname}")
				except Exception as e:
					print(e)
			if x.lower()=="-alock":
				if data.message.author.userId in adm:
					try:
						for i in c:
							l.append(i)
							subclient.send_message(chatId=data.message.chatId,message=f"locked {i} command")
							print(l)
							print(f"Info requested by {data.message.author.nickname}")
					except Exception as e:
						print(e)
				else:
					try:
						subclient.send_message(chatId=data.message.chatId,message="Эту комманду могу использовать админы")
					except Exception as e:
						print(e)
			if x.lower()=="-rlock":
				if data.message.author.userId in adm:
					try:
						for i in c:
							l.remove(i)
							subclient.send_message(chatId=data.message.chatId,message=f"разблокирована {i} команда")
							print(l)
							print(f"Info requested by {data.message.author.nickname}")
					except Exception as e:
						print(e)
				else:
					try:
						subclient.send_message(chatId=data.message.chatId,message="Это команда доступна админам")
					except Exception as e:
						print(e)
						pass
			if x.lower()=="-join":
				if c==[]:
					try:
						subclient.send_message(chatId=data.message.chatId,message=f"{data.message.author.nickname}, ставь ссылку куда нужно присоединиться идиот!")
					except:
						pass
				else:
					try:
						for i in c:
							try:
								d=client.get_from_code(i).objectId
								subclient.join_chat(chatId=d)
								subclient.send_message(chatId=data.message.chatId,message="Присоединился !!")
							except Exception as e:
								print(e)
						print(f"Info requested by {data.message.author.nickname}")
					except Exception as e:
						print(e)
			if x.lower()=="-vc" and c==[]:
				try:
					subclient.invite_to_vc(userId=data.message.author.userId,chatId=data.message.chatId)
					print(f"invited {data.message.author.nickname} to vc")
				except Exception as e:
					print(e)
					subclient.send_message(chatId=data.message.chatId,message=f"[ic]У меня нет помощника/организатора <$@{data.message.author.nickname}$>")
			if x.lower()=="-inviteall" and c==[]:
				if x.lower() not in l:
					try:
						h=subclient.get_online_users(start=0,size=1000)
						for u in h.profile.userId:
							try:
								subclient.invite_to_vc(userId=u,chatId=data.message.chatId)
							except Exception as e:
								print(e)
								pass
						subclient.send_message(chatId=data.message.chatId,message=f"[ic]Приглашены все участники")
						print(f"invited {data.message.author.nickname} to vc")
					except Exception as e:
						print(e)
						subclient.send_message(chatId=data.message.chatId,message=f"[ic]У меня нет помощника/организатора, <$@{data.message.author.nickname}$>")
				else:
					try:
						subclient.send_message(chatId=data.message.chatId,message="Inviteall заблокирована")
					except:
						pass
			if x.lower() == "-prank" and c == []:
				try:
					subclient.delete_message(messageId=data.message.messageId, chatId=data.message.chatId, asStaff=True,
											 reason="clear")
					subclient.send_message(chatId=data.message.chatId,
										   message=f"Ты был обманут {data.message.author.nickname}",
										   messageType=109)
					print("deleted a message")
				except Exception as e:
					print(e)
			if x.lower()=="-start" and c==[]:
				if x.lower() not in l:
					try:
						client.start_vc(comId=cid,chatId=data.message.chatId,joinType=1)
						subclient.send_message(chatId=data.message.chatId,message=f"Голосовой чат начался")
						print(f"VC started")
					except Exception as e:
						print(e)
						try:
							subclient.send_message(chatId=data.message.chatId,message=f"[ic]У меня нет помощника/организатора, <${data.message.author.nickname}$>",mentionUserIds=[data.message.author.userId])
						except:
							pass
				else:
					try:
						subclient.send_message(chatId=data.message.chatId,message=f"Start команда заблокирована <${data.message.author.nickname}$> !!",mentionUserIds=[data.message.author.userId])
					except:
						pass
			if x.lower() == "-help" and c == []:
				try:
					subclient.send_message(chatId=data.message.chatId,message="""[cb]Комманды:-

-info                 
-join {chatlink}      -global {ссылка на участника}
-pm               -prank
-start               -vc
-heicmd           -inviteall
-lock                -clear
-alock,-rlock (только пери и моречка)""")
					print(f"Info requested by {data.message.author.nickname}")
				except Exception as e:
					print(e)
			if x.lower()=="-flirt" and c==[]:
				try:
					subclient.send_message(chatId=data.message.chatId,message="""[i]Каждый раз, когда я смотрю на тебя, мое сердце бьется быстрее, чем пуля""")
					print(f"Info requested by {data.message.author.nickname}")
				except Exception as e:
					print(e)
			if x.lower()=="-hugme" and c==[]:
				try:
					subclient.send_message(chatId=data.message.chatId,message="""[i]открывает руки для обьятий (づ｡◕‿‿◕｡)づ
[i]я здесь для тебя...""")
					print(f"Info requested by {data.message.author.nickname}")
				except Exception as e:
					print(e)
			if x.lower()=="-joke" and c==[]:
				try:
					subclient.send_message(chatId=data.message.chatId,message="""[i]Твоя жизнь""")
					print(f"Info requested by {data.message.author.nickname}")
				except Exception as e:
					print(e)
			if x.lower()=="-punchme" and c==[]:
				try:
					subclient.send_message(chatId=data.message.chatId,message="""[i]одевает свое боксерские перчатки и сильно бьет тебя по твоему лицу""")
					print(f"Info requested by {data.message.author.nickname}")
				except Exception as e:
					print(e)
			if x.lower()=="-cheerme" and c==[]:
				try:
					subclient.send_message(chatId=data.message.chatId,message="""[i]Я ответил многим участникам, но когда я отвечу вам, это сделает мой день лучше!""")
					print(f"Info requested by {data.message.author.nickname}")
				except Exception as e:
					print(e)
			if x.lower()=="-fuckmori" and c==[]:
				try:
					subclient.send_message(chatId=data.message.chatId,message="""[i]Поздравляю вы оттарабанили Моречку""")
					print(f"Info requested by {data.message.author.nickname}")
				except Exception as e:
					print(e)
			if x.lower()=="-fart" and c==[]:
				try:
					subclient.send_message(chatId=data.message.chatId,message="""[i]Пук пук я обосрался""")
					print(f"Info requested by {data.message.author.nickname}")
				except Exception as e:
					print(e)
			if x.lower()=="-twerk" and c==[]:
				try:
					subclient.send_message(chatId=data.message.chatId,message=f"""[i]Тверкает для <${data.message.author.nickname}$>..""")
					print(f"Info requested by {data.message.author.nickname}")
				except Exception as e:
					print(e)
			if x.lower()=="-fuckperry" and c==[]:
				try:
					subclient.send_message(chatId=data.message.chatId,message=f"""Вы выебали Пери!Умничьки,а теперь в шахту🌞""")
					print(f"Info requested by {data.message.author.nickname}")
				except Exception as e:
					print(e)
			if x.lower()=="-mansturbate" and c==[]:
				try:
					subclient.send_message(chatId=data.message.chatId,message=f"""[i]Мансутрует <${data.message.author.nickname}$>\n[i]Ну давай...Сенпай!""")
					print(f"Info requested by {data.message.author.nickname}")
				except Exception as e:
					print(e)
			if x.lower()=="-heicmd" and c==[]:
				try:
					subclient.send_message(chatId=data.message.chatId,message="""[b]Команды от моречки 🥰!!
-flirt
-punchme
-twerk
-cheerme
-hugme
-joke
-fart
-fuckmori
-mansturbate""")
					print(f"Info requested by {data.message.author.nickname}")
				except Exception as e:
					print(e)
			
def socketRoot():
	j=0
	while True:
		if j>=300:
			print("Updating socket.......")
			client.close()
			client.start()
			print("Socket updated")
			j=0
		j=j+1
		time.sleep(1)
socketRoot()

