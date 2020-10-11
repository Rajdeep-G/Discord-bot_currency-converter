# Importing the packages
import discord
import requests

# Fetching the data from the api
res=requests.get('https://api.exchangeratesapi.io/latest') 
data=res.json()['rates']

# Function to calculate the converted amount
def convert(value,src,to):
    return((value/data[src] )*(data[to]))

# Driving code
client=discord.Client()

@client.event
async def on_message(message):
    message.content=message.content.lower()
    if message.author==client.user:
        return
    # Help command Initialisation
    if message.content.startswith("%help"):
        help_str='''```
Usage
Command-%convert <amount> <from(optional)> <to(optional)>
Desc: To conv a given amt to any cuurency(deafult from- USD, default to-INR) ```'''
        await message.channel.send(help_str)
    if message.content.startswith("%convert"):
        l=message.content[9::]
        c = 0
        c_from=''
        c_to=''
        value=0
        converted_amount = 0
        # Actual working code
        try:
            for i in range(len(l)):
                if l[i] == ' ':
                    c += 1
            if len(l) == 0:
                print("wrong input")
            else:
                # case-1 if only amount is given (No From and to is given) || Hence converts from USD to INR
                if c == 0:
                    value = float(l)
                    c_to = "INR"
                    c_from="USD"
                    converted_amount = convert(value, "USD", "INR")
                # Case-2 If source is given only. It takes default to as "INR"
                elif c == 1:
                    i = l.find(' ')
                    value = float(l[:i])
                    j = l.find(' ', i)
                    c_from = l[j + 1:]
                    c_from = c_from.upper()
                    c_to = "INR"
                    converted_amount = convert(value, c_from, c_to)
                # Both are provided ny user . 
                elif c == 2:
                    i = l.find(' ')
                    value = float(l[:i])
                    j = l.find(' ', i + 1)
                    c_from = l[i + 1:j]
                    c_from = c_from.upper()
                    c_to = l[j + 1:].upper()
                    converted_amount = convert(value, c_from, c_to)
                converted_amount=round(converted_amount,2)
                # print(c_from)
                # await message.channel.send(converted_amount)
                display_data='```'+(str(value))+" "+c_from+" = "+(str(converted_amount))+" "+c_to+'```'

                await message.channel.send(display_data)
        except:
            await message.channel.send("```Please ensure correct input```")

# API TOKEN. Replace the string with your token.
client.run('your api token') 