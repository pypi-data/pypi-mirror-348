from CharmCord.globeHandler import get_globals

async def messageAuthor(ids, context):
    bots = get_globals()[1]

    try:
        args = ids.split(";")
        channel = await bots.fetch_channel(args[0])
        mes = int(args[1])
        message = await channel.fetch_message(mes)
        return message.author
    except:
        raise SyntaxError("Not a message args")
