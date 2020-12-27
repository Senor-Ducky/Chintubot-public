import discord
from discord.ext import commands
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

languages = {'Afrikaans':'af','Albanian':'sq','Amharic':'am','Arabic':'ar','Armenian':'hy','Azerbaijani':'az','Basque':'eu','Belarusian':'be','Bengali':'bn','Bosnian':'bs','Bulgarian':'bg','Catalan':'ca','Cebuano':'ceb','Chinese':'zh-CN','Corsican':'co','Croatian':'hr','Czech':'cs','Danish':'da','Dutch':'nl','English':'en','Esperanto':'eo','Estonian':'et','Finnish':'fi','French':'fr','Frisian':'fy','Galician':
'gl','Georgian':'ka','German':'de','Greek':'el','Gujarati':'gu','Haitian':'ht','Hausa':'ha','Hawaiian':'haw','Hebrew':'he','Hindi':'hi','Hmong':'hmn','Hungarian':'hu','Icelandic':'is','Igbo':'ig','Indonesian':'id','Irish':'ga','Italian':'it','Japanese':'ja','Javanese':'jw','Kannada':'kn','Kazakh':'kk','Khmer':'km','Korean':'ko','Kurdish':'ku','Kyrgyz':'ky','Lao':'lo','Latin':'la','Latvian':'lv','Lithuanian':'lt','Luxembourgish':'lb','Macedonian':'mk','Malagasy':'mg','Malay':'ms','Malayalam':'ml','Maltese':'mt','Maori':'mi','Marathi':'mr','Mongolian':'mn','Myanmar':'my','Nepali':'ne','Norwegian':'no','Nyanja':'ny','Pashto':'ps','Persian':'fa','Polish':'pl','Portuguese':'pt','Punjabi':'pa','Romanian':'ro','Russian':'ru','Samoan':'sm','Scots':'gd','Serbian':'sr','Sesotho':'st','Shona':'sn','Sindhi':'sd','Sinhala':'si','Slovak':'sk','Slovenian':'sl','Somali':'so','Spanish':'es','Sundanese':'su','Swahili':'sw','Swedish':'sv','Tagalog':'tl','Tajik':'tg','Tamil':'ta','Telugu':'te','Thai':'th','Turkish':'tr','Ukrainian':'uk','Urdu':'ur','Uzbek':'uz','Vietnamese':'vi','Welsh':'cy','Xhosa':'xh','Yiddish':'yi','Yoruba':'yo','Zulu':'zu'}

url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

headers = {
    'content-type': "application/x-www-form-urlencoded",
    'accept-encoding': "application/gzip",
    'x-rapidapi-key': os.getenv("RAPID_API_KEY"),
    'x-rapidapi-host': "google-translate1.p.rapidapi.com"
    }

class Translate(commands.Cog):

	def __init__(self, bot):
		self.bot = bot


	@commands.command()
	async def translate(self, ctx,to, *, word):
		try:
			#gotta get super pythonic
			result_language = languages[to.capitalize()]
			payload = f"q={word}&source=en&target={result_language}"
			response = requests.request("POST", url, data=payload, headers=headers)
			language = list(languages.keys())[list(languages.values()).index(result_language)]
			em = discord.Embed(title = f"Translating '{word}' to {language}")
			em.add_field(name="Translated Text", value=json.loads(response.text)['data']['translations'][0]['translatedText'])
			await ctx.send(embed=em)
		except:
			await ctx.send('Language not supported.')

def setup(bot):
	bot.add_cog(Translate(bot))