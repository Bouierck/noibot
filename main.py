import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
from lxml import html
import time
from discord.ext import tasks

#DATABASE LINKER
from Data.database_handler import DatabaseHandler

bot = commands.Bot(command_prefix="$", description="Bot de Agent Cog!")
             
#------------------------------------------------------------------ DATABASE HANDLER -------------------------------------------------------------------
database_handler = DatabaseHandler("database.db")

def register():
    print("---Register---")
    username = input("Username : ")
    password = input("Password :")

    database_handler.create_person(username, password)

def login():
    print("---Login---")
    username = input("Username : ")
    password = input("Password :")

    if database_handler.user_exists_with(username) and password == database_handler.password_for(username):
        menu_connected()
    else:
        print("not logged in")

def menu_not_connected():
    while True:
        login()
        return

def menu_connected():
    while True:
        menu_connected.connect = 1
        return




# ---------------------------------------------------------------------- BOT FUNCTION --------------------------------------------

@bot.event
async def on_ready():
    print("---------------------------------------------\n")
    print("--- Chargement du Bot ---\n")
    print("Apprentissage des verbes irréguliers............\n")
    print("Ajout de Coca dans le frigo............\n")
    print("--- Pret Pour Utilisation ---\n")
    #embed = discord.Embed()
    #embed.description = "This country is not supported, you can ask me to add it [here](https://www.pokebeach.com/2021/09/dunsparce-and-skate-park-from-fusion-arts)."
    #await ctx.send(embed=embed)

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='$pokehelp'))
    print("\n")
    news.lien = ""
    news.start()
    #menu_not_connected()
    menu_connected()

   


@tasks.loop(seconds = 30)
async def news():
    #print(lien)
    print('\n---- Recup dernier Event ----\n')
    page = requests.get('https://www.pokebeach.com/')
    tree = html.fromstring(page.content)
    #This will create a list of buyers:
    #buyers = tree.xpath('//div[@title="buyer-name"]/text()')
    #This will create a list of prices
    post = tree.xpath('//a[@rel="bookmark"]/text()')
    #link = tree.xpath('//a/@href')
    #print('Buyers: ', buyers)
    #print('Prices: ', post)
    #print('Link :', link)



    url = "https://www.pokebeach.com/"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    #print("The href links are :")

    #Recupere derniere news
    for link in soup.find_all('a'):
        s = link.get('href')
        if s is not None:
            if(s[26:30] == "2021"):
                news.lien = s
                #print(lien)
                break
    
    news.lienPred = database_handler.get_url_from_table()

    if(news.lien != news.lienPred):
        print("Lien Différent de Initial :",news.lien)
        news.lienPred = news.lien


        url = news.lien
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")

        #get title
        title = soup.find('h1').getText()
        print(title)

        #get Thumbnail
        for img_url in soup.find_all('a'):
            image = img_url.get('href')
            if image is not None:
                if(image[26:34] == 'news/202'):
                    image_url = image
                    print(image_url)
                    break
            #print(image)

        #'''
        #Send la news
        channel = bot.get_channel(567351510061547526)
        embedVar = discord.Embed(title=":loudspeaker:  News de Dernière Minute by Noibot :bangbang:  :star2: :100:", description=title, color=0x8700FF)
        embedVar.set_thumbnail(url=image_url)
        embedVar.add_field(name=":speech_left: Lien vers News :speech_balloon: ", value=news.lien, inline=False)
        embedVar.set_footer(text='By Agent Cog ',icon_url="https://static-cdn.jtvnw.net/jtv_user_pictures/e92327a1-9a99-405a-8ea8-681a013e2b55-profile_image-70x70.png")
        await channel.send(embed=embedVar)
        database_handler.modify_url(news.lien)

        #'''

    else:
        #Pas de news entre temps
        print("A jour")
 
'''
@bot.event
async def on_message(message):
    if message.content.startswith('$test'):
        await message.channel.send("I'm **Alive** no worries ! :innocent: ")

    await bot.process_commands(message)
    
    #if message.content.startswith('$event'):

    #if message.content.startswith('$achat'):

    #if message.content.startswith('$vente'):

    #if message.content.startswith('$shop'):

    #if message.content.startswith('$reservation'):
    
    #if message.content.startswitch('$op_deck')
'''



#async def stock_insert(message, nom_element: str, quantite: int, boutique: str, date: str):
#    print('hello')
#    await message.channel.send(nom_element)

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()  
async def hello(ctx):
    await ctx.send('hello!')
    

@bot.command()
async def test(ctx):
    await ctx.send("I'm **Alive** no worries ! :innocent: ")

@bot.command()
async def pokenews(message):
    await message.channel.send("Toutes les dernières **NEWS** se trouvent dans le salon : " + bot.get_channel(567351510061547526).mention + ':thumbsup: ')

@bot.command()
async def pokehelp(message):
    await message.channel.send('Hey ' + format(message.author.mention) + ", je suis là pour t'aider !")
    await message.channel.send("Je suis encore en apprentissage ! On m'ajoute des commandes au fur et à mesure tu vois ! :smile:")



    embedVar = discord.Embed(title="Liste des commandes à disposition", color=0x00FF32)
    embedVar.set_thumbnail(url="https://thumbs.gfycat.com/SomberFittingHornedtoad-size_restricted.gif")
    embedVar.add_field(name="Suis-je en vie ?", value="$test", inline=False)
    embedVar.add_field(name="Aide Commande du Bot", value="$pokehelp", inline=False)
    embedVar.add_field(name="Dernière News d'actualités", value="$pokenews", inline=False)
    embedVar.add_field(name="Items en Stock", value="$stock", inline=False)
    embedVar.set_footer(text='By Agent Cog ',icon_url="https://static-cdn.jtvnw.net/jtv_user_pictures/e92327a1-9a99-405a-8ea8-681a013e2b55-profile_image-70x70.png")
    await message.channel.send(embed=embedVar)


@bot.command()
@commands.has_role("Vendeur")
async def stock_insert(message, nom_element, quantite, boutique, date):
    if(not menu_connected.connect):
        await message.channel.send("Vous n'êtes pas Logged In")
        return
    else:
        database_handler.stock_increment(nom_element,quantite,boutique,date)
        await message.channel.send("Stock Mis à Jour !")
        print("OK")

@bot.command()
async def stock_view(message):
    if(not menu_connected.connect):
        await message.channel.send("Vous n'êtes pas Logged In")
        return
    else:
        result = database_handler.stock_show()
        print("OK")
        i = 0
        print(dict(result[0])["nom_element"])
        embedVar = discord.Embed(title=" :loudspeaker: **Liste des Stocks Disponible** :loudspeaker:", color=0x0D02FF)
        embedVar.set_thumbnail(url="https://stock.wikimini.org/w/images/2/2c/Pok%C3%A9mon.gif")
        while(i < len(result)):

            embedVar.add_field(name=" :mega: " + dict(result[i])["nom_element"], value="Quantité : " + str(dict(result[i])["quantite"]) + "\nBoutique : " + dict(result[i])["boutique"] + "\nDate : " + dict(result[i])["date"] + "\n*ID : " + str(dict(result[i])["id_stock"]) + "*", inline=False)
            i = i + 1
        embedVar.set_footer(text='By Agent Cog ',icon_url="https://static-cdn.jtvnw.net/jtv_user_pictures/e92327a1-9a99-405a-8ea8-681a013e2b55-profile_image-70x70.png")
        await message.channel.send(embed=embedVar)


@bot.command()
@commands.has_role("Vendeur")
async def stock_suppr(message, id_stock):
    if(not menu_connected.connect):
        await message.channel.send("Vous n'êtes pas Logged In")
        return
    else:
        database_handler.stock_delete(id_stock)
        await message.channel.send("L'article a bien été supprimé!\n")


@bot.command()
async def stock(message):
    embedVar = discord.Embed(title=" :gift: Liste des commandes pour les stocks :package: ", color=0x0D02FF)
    embedVar.set_thumbnail(url="https://stock.wikimini.org/w/images/2/2c/Pok%C3%A9mon.gif")
    embedVar.add_field(name="Voir la liste des **Stocks**", value=" :arrow_forward: $stock_view\n :speech_balloon: Permet de voir les articles en stock (ou bientôt disponible)", inline=False)
    embedVar.add_field(name="(**Vendeur**) Ajouter un nouvel article", value=" :arrow_forward:  $stock_insert NomArticle Quantité Boutique Date", inline=False)
    embedVar.add_field(name="(**Vendeur**) Supprimer un article", value=" :arrow_forward: $stock_suppr id\n :speech_balloon: l'id se trouve dans le tableau *$stock_view*", inline=False)
    embedVar.set_footer(text='By Agent Cog ',icon_url="https://static-cdn.jtvnw.net/jtv_user_pictures/e92327a1-9a99-405a-8ea8-681a013e2b55-profile_image-70x70.png")
    await message.channel.send(embed=embedVar)

@bot.command()
@commands.has_role("Admin")
async def Am_I_Admin(message):
    await message.channel.send("Vous êtes un **Administrateur** de ce serveur :sunglasses: !")

@bot.command()
@commands.has_role("Vendeur")
async def Am_I_Seller(message):
    await message.channel.send("Vous êtes un **Vendeur** de ce serveur :money_with_wings:  !")






'''
@bot.event
async def on_command_error(message, error):
    print(message.command.name + "was invoked incorrectly")
    print(error)
    if isinstance(error, commands.MissingRole):
        await message.channel.send("Vous ne pouvez pas effectué cette commande car vous n'avez pas le bon **rôle** sur ce serveur !")

'''



@bot.command()
async def reserver(message, id_stock: int, quantite: int):
    element_name = database_handler.get_name_from_id_stock(id_stock)
    if(database_handler.in_reserv(id_stock) == 1):
        if(database_handler.get_reserv(id_stock)==1):
            id_resa = database_handler.id_stock_to_id_resa(id_stock)
            database_handler.ajout_liste_reservation(message.author.id, id_resa, quantite)
            await message.channel.send("Vous avez reservé l'objet "+ element_name + "!")
        else:
            await message.channel.send("Une erreur est apparue ! :(")
    else:
        await message.channel.send("L'item " + element_name + " n'est plus en stock ! :(")


@bot.command()
@commands.has_role("Vendeur")
async def ajout_reservation(message, id_stock, quantite):
    if(database_handler.stock_exists(id_stock)==1):
        await message.channel.send("L'ID existe!")
        database_handler.reservation_increment(id_stock, quantite)
        await message.channel.send("Vous venez d'ajouter une possibilité de reservation!")
    else:
        await message.channel.send("L'ID donné n'est pas présent dans les stocks !")


@bot.command()
async def reservation_view(message):
    if(not menu_connected.connect):
        await message.channel.send("Vous n'êtes pas Logged In")
        return
    else:
        result = database_handler.reservation_show()
        print("OK")
        i = 0
        embedVar = discord.Embed(title=" :loudspeaker: **Liste des Réservations Disponible** :loudspeaker:", color=0x0D02FF)
        embedVar.set_thumbnail(url="https://stock.wikimini.org/w/images/2/2c/Pok%C3%A9mon.gif")
        while(i < len(result)):
            nom_element = database_handler.get_name_from_id_stock(dict(result[i])["id_stock"])
            embedVar.add_field(name=" :mega: " + nom_element, value="Quantité à Réserver : " + str(dict(result[i])["quantite_resa"]) + "\n*ID objet : " + str(dict(result[i])["id_stock"]) + "*" + "\n*ID résa : " + str(dict(result[i])["id_resa"]) + "*", inline=False)
            i = i + 1
        embedVar.set_footer(text='By Agent Cog ',icon_url="https://static-cdn.jtvnw.net/jtv_user_pictures/e92327a1-9a99-405a-8ea8-681a013e2b55-profile_image-70x70.png")
        await message.channel.send(embed=embedVar)



@bot.command()
async def test_name(message,id_stock):
    nom_element = database_handler.get_name_from_id_stock(id_stock)
    print(nom_element)

@bot.command()
async def liste_reservation_view(message):
    result = database_handler.liste_reservation_show()
    print("OK")
    i = 0
    embedVar = discord.Embed(title=" :star2:  **Reservations effectués :** :star2: ", color=0x0D02FF)
    embedVar.set_thumbnail(url="https://stock.wikimini.org/w/images/2/2c/Pok%C3%A9mon.gif")
    while(i < len(result)):
        #username = bot.get_user_info(dict(result[i])["user"])
        nom_element = database_handler.get_name_from_id_resa(dict(result[i])["id_resa"])
        embedVar.add_field(name=" :mega: " + nom_element, value="User : " + "<@" + str(dict(result[i])["user"]) + ">" + "\nQuantité : " + str(dict(result[i])["quantite"]), inline=False)
        i = i + 1
    embedVar.set_footer(text='By Agent Cog ',icon_url="https://static-cdn.jtvnw.net/jtv_user_pictures/e92327a1-9a99-405a-8ea8-681a013e2b55-profile_image-70x70.png")
    await message.channel.send(embed=embedVar)


# str(dict(result[i])["id_stock"]) + 



bot.run("ODg3NzQ0NjQ3ODY1MjAwNjQx.YUImoQ.WyXZ8sBn1-v4vUoA6SxAneT5usM");




#embed = discord.Embed()
#embed.description = "This country is not supported, you can ask me to add it [here](https://www.pokebeach.com/2021/09/dunsparce-and-skate-park-from-fusion-arts)."
#await ctx.send(embed=embed)





# DATABASE REGISTER / LOGIN

