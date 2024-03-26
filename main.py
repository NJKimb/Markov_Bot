import os
import markovify
import discord
import random

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)


def create_model():
    with open("logs.txt", "r", encoding='utf8') as logs:
        text = logs.read()
    model = markovify.NewlineText(text)
    model = model.compile()
    return model


def generate(model):
    generated_message = model.make_sentence()
    return generated_message


model = create_model()


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    num = random.randrange(1, 25)
    if num == 23:
        generated_message = generate(model)
        await message.channel.send(generated_message)


client.run(os.environ['TOKEN'])