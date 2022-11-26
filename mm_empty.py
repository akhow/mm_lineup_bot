import MMTelegramBot

TOKEN = "" # place your token here
chat_id = "" #place the chat id you want the message to be sent to here

mm = MMTelegramBot.MMTelegramBot(TOKEN)

mm.generateLineup("ourLineup.csv", "theirLineup.csv")
mm.saveLineups(mm.ourLineup, mm.theirLineup)
msg = mm.generateLineupMessage(mm.ourLineup, mm.theirLineup)
mm.sendMessage(chat_id, msg)