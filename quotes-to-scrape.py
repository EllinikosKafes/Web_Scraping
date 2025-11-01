import requests
from bs4 import BeautifulSoup

class QuotePageLocators:
    """
    This is the css locator for each tag.
    Using select with beautiful soup we are gonna grab all of our div tags (quotes)
    """
    QUOTE = 'div.quote'


class QuoteLocators:
    """
    These are the locators for our specific div tags.
    Each div tag is a quote with its elements.
    These are the locators we're gonna use to select_one with bs4
    """
    AUTHOR ='small.author' 
    CONTENT = 'span.text'
    TAGS = 'div.tags a.tag'


class QuoteParser:
    """
    Given one specific quote div , find out the data about the quote using our QuoteLocators.
    (quote content, quote author, quote tags)
    """
    def __init__(self,parent):          #Parent = one div tag (beautiful soup tag)
        self.parent = parent

    def __repr__(self):
        return f"<Quote {self.content} by {self.author}>"

    @property
    def content(self):
        locator = QuoteLocators.CONTENT
        return self.parent.select_one(locator).string
    
    @property
    def author(self):
        locator = QuoteLocators.AUTHOR
        return self.parent.select_one(locator).string
    
    @property
    def tags(self):
        locator = QuoteLocators.TAGS
        return [e.string for e in self.parent.select(locator)]
    

class QuotesPage:
    
    def __init__(self,page):                            #page= our page content (html code)
        self.soup = BeautifulSoup(page,'html.parser')

    @property
    def quote(self):
        locator = QuotePageLocators.QUOTE
        quote_tags = self.soup.select(locator)          #selecting all of the div tags
        return [QuoteParser(e) for e in quote_tags]     #returns a list of QuoteParser objects



link = 'https://quotes.toscrape.com/'

page_content = requests.get(link).content
page = QuotesPage(page_content)

for quote in page.quote:                #each quote is a QuoteParser object with property methods like author,content,tags
    print(quote.tags)