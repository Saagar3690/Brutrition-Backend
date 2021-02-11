# Brutrition-Backend
This is the backend for the Brutrition API, which serves webscraped nutrition data from UCLA's dining hall menus.

### To Set Up
  * `git pull`
  * `npm ci`
  * `pip install requirements.txt`
  * Make sure you have the `.env` file configured with the necessary environment variables
  
### To start
  * local server: `node server.js`
  * alternatively (better suited for development): `npx nodemon server.js` 
  * webscraping: `python scrape.py`
  * populating database: `python sendRequests.py`
