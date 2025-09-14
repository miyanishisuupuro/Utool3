async def handle_message(message):
    if message.author.bot:
        return
    print(f"📨 Message from {message.author}: {message.content}")
