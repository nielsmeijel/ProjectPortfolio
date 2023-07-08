
## Recipe Scraper 👨‍🍳

This is a simple web scraper that scrapes recipes from the website [Epicuious](https://www.epicurious.com/). It is written in Python and uses the [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) library to parse the HTML. The main function does not take any arguments as inputs and it returns a list of dictionaries. Each dictionary contains the following keys: "primarykey", "Title","Author","ContributorLink", "PublishDate","Serves","Ingredients","Methods". The return can easily be parsed to json or csv files accordingly. 

The script scrapes the home pages newest recipes: "Our Newest Recipes" at the bottom of the page, it access those 5 new recipe and scrapes the recipe page for the information. The script does not scrape the entire website. The html structure of the website was manually inspected for the relvant information. 

### Usage 

The script can easily be used in an ETL process. The script can be scheduled to run daily and the output can be stored in a database.
Personally i parsed the output to json files and stored them in a folder locally once per two weeks using a chronjob.

### Limitations
- The script is dependent on the css and html structure of the website. If the website changes the script will not work.
- The script only scrapes epicurious.com. 


