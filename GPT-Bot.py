import discord
from discord.ext import commands
import requests
import json
import openai
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def generate_response(prompt, engine):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }

    data = {
        'prompt': f'{prompt}',
        'max_tokens': 1000,
        'n': 1,
        'stop': None,
        'temperature': 0,
    }

    gpt_api_url = f'https://api.openai.com/v1/engines/{engine}/completions'
    response = requests.post(gpt_api_url, headers=headers, json=data)
    result = json.loads(response.text)
    return result['choices'][0]['text'].strip()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='ask')
async def ask(ctx, *, question):
    prompt = f'Q: {question}\nA:'
    response = generate_response(prompt, 'text-davinci-003')
    answer = response.replace(prompt, '').strip()
    await ctx.send(answer)

bot.run(BOT_TOKEN)