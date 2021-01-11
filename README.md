# Chintubot
### Prefix - $

### Type "$help" to get the list of commands.

**Be sure to run `pip install -r requirements.txt` to install all the required packages.**


**You will need the following API keys and tokens:**
	- Discord Bot Token (as "TOKEN" in a .env)
	- Reddit API Client ID (as "CLIENT_ID" in a .env)
	- Reddit API Client Secret (as "SECRET" in a .env)
	- Rapid API key (as "RAPID_API_KEY")
	- Perspective API key (in **line12** of **main.py**. Read the Note below.)


**Note on Getting the Perspective API key:** You will need the access to Perspective API by Google. You can ask for access here: https://forms.gle/Pdj5KitPgoYHV9do7 . They usually take 30-40 minutes analyzing your responses and granting you with the link to enable the API in your Google Console. Before going further, make sure you have a project created in Google Console. After creating a project and enabling the API, you will need to generate the API key from the projects credentials page. Add your API key in **line 12** of **main.py** for the API to work and remove the commented function call on **line 77** of **main.py**. 


**Note on Developing without the Perspective API:** If you want to develop the bot without getting the Perspective API, just leave **line 12** in **main.py** as it is and never remove the comment on **line 77** of **main.py**.
