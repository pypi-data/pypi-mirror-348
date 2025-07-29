import asyncio
from CharmCord.globeHandler import get_globals
from CharmCord.CharmErrorHandling import CharmCordErrors


async def waitMessage(args, context):
    """
    Ex. $waitMessage[ChannelID;User;timeout;timeoutErrMsg;return]
    """
    bots = get_globals()[1]
    split = args.split(";")
    if len(split) < 3:
        raise SyntaxError("args, User, or timeout not provided to $waitMessage")
    try:
        channel_id = split[0]
        user = split[1]
        timeout = int(split[2])
        return_data = timeout

        def check(msg):
            if int(channel_id) == msg.channel.id:
                if user == "everyone":
                    return True
                elif int(user) == msg.author.id:
                    return True
                else:
                    return False

        error = None
        if len(split[3]) > 1:
            error = split[3]
        if error is None:
            try:
                message = await bots.wait_for("message", timeout=timeout, check=check)
                return message.content
            except asyncio.TimeoutError:
                return
        else:
            try:
                message = await bots.wait_for("message", timeout=timeout, check=check)
                return message.content
            except asyncio.TimeoutError:
                return await context.channel.send(error)
    except ValueError:
        CharmCordErrors(f"args Error in {context.command.name}")
        return
