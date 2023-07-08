import requests
from bs4 import BeautifulSoup
import hashlib

def links_to_newest_recipes(soup):
    linkstorecipes = []
    navnumpages = soup.find_all('div', class_="recipe")
    for div in navnumpages:
        recipelink = div.find('a')['href']
        linkstorecipes.append(recipelink)
    return linkstorecipes


def scrape_recipe_content(recipeurl):
    response = requests.get(recipeurl)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        header = soup.head.title.text
        header = header.replace(" Recipe | Epicurious", "")

        authors = soup.find('a', class_="BaseWrap-sc-gjQpdd BaseText-ewhhUZ BaseLink-eNWuiM BylineLink-gEnFiw iUEiRd dPcDNa hcRjeq eErqIx byline__name-link button")
        contributorLink = authors['href']
        authors = authors.text

        publishDate = soup.find('time', class_="SplitScreenContentHeaderPublishDate-bMGEVk jZRIyI")['datetime']
        
        try:
            serves = soup.find('p', class_="BaseWrap-sc-gjQpdd BaseText-ewhhUZ Yield-eyQhTA iUEiRd gQBfcy DyTuB")
            serves = serves.text
        except: 
            serves = "N/A"


        ingredients = soup.find_all('div', class_="Wrapper-dxnTBC jIWNsq")[0]
        ingredients = ingredients.find_all('div', class_="BaseWrap-sc-gjQpdd BaseText-ewhhUZ Description-cSrMCf iUEiRd ioVvSX fsKnGI")
        ingredients = [ingredient.text for ingredient in ingredients]
        ingredientsDict = {index:ingredient for index, ingredient in enumerate(ingredients)}


        methods = soup.find_all('div', class_="InstructionsWrapper-hZXqPx RmryN")[0]
        methods = methods.find_all('p')
        methods = [method.text for method in methods]
        methodsDict = {index:method for index, method in enumerate(methods)}

        

        returnRecipeDict = {
            "primarykey": hashlib.md5(header.encode()).hexdigest(),
            "Title": header,
            "Author": authors,
            "ContributorLink": contributorLink,
            "PublishDate": publishDate,
            "Serves": serves,
            "Ingredients": ingredientsDict,
            "Methods": methodsDict,
        }
    else:
        print("Error: ", response.status_code)
    
    return returnRecipeDict






def main():

    baseurl = "https://www.epicurious.com"
    response = requests.get(baseurl)
    print(response.status_code)

    soup = BeautifulSoup(response.content, 'html.parser')

    newestRecipes = []
    for link in links_to_newest_recipes(soup):
        
        newestRecipes.append(scrape_recipe_content(baseurl + link))
    print(newestRecipes)
    return newestRecipes


if __name__ == "__main__":
    main()