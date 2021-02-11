from recipe_scrapers import scrape_me

def scrape_url(url):
    """ function that scrapes recipe data"""
    try:
        scraper = scrape_me(url, wild_mode=True)
        print(f'{scraper.title()}')
        print(f'cooking time: {scraper.total_time()}')
        print(f'number of servings {scraper.yields()[:2]}')
        print('\nRECIPE\n')
        for i in scraper.ingredients(): print(i)
        print('\nINSTRUCTIONS\n')
        print(scraper.instructions())
        print(f'\nimage: {scraper.image()}')
        print(f'\nsource: {scraper.host()}')
        #print(scraper.links())
        print('\nNUTRIENTS\n')
        for k,v in scraper.nutrients().items(): print(f'{k}:{v}')  # if available
        print(f'\nauthor: {scraper.author()}')
        print(f'\ncanonical_url: {scraper.canonical_url()}')
        print(f'\nlanguage: {scraper.language()}')
        print(f'\nreviews: {scraper.reviews()}')
        print(f'\nsite_name: {scraper.site_name()}')

        


    except:
        print(f'no information retrieved from {url}')
    return 0


#scrape_url('https://www.bbc.co.uk/food/recipes/slow_cooker_minestrone_24914')
scrape_url('https://www.bbc.co.uk/food/recipes/edamame_and_tofu_97832')

