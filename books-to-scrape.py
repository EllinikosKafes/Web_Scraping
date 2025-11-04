import requests
import re
from bs4 import BeautifulSoup

class  AllBooksPageLocators:
    """
    This is the css locator for each tag.
    Using select with beautiful soup we are gonna grab all of our div tags (quotes)
    """
    BOOK_LIST = 'div.page_inner section li.col-xs-6.col-sm-4'


class BookLocators:
    """
    These are the locators for our specific div tags.
    Each div tag is a quote with its elements.
    These are the locators we're gonna use to select_one with bs4
    """
    STAR_RATING ='article.product_pod p.star-rating' 
    TITLE = 'article.product_pod h3 a'
    LINK = 'article.product_pod h3 a'
    PRICE = 'div.product_price p.price_color'


class BookParser:
    """
    Given one specific quote div , find out the data about the quote using our QuoteLocators.
    (quote content, quote author, quote tags)
    """
    RATINGS = {
        "One":1,
        "Two":2,
        "Three":3,
        "Four":4,
        "Five":5
    }

    def __init__(self,parent):          #Parent = one div tag (beautiful soup object)
        self.parent = parent

    def __repr__(self):
        return f"<Title: {self.title}| Price: £{self.price}| Rating: {self.stars} Stars>"

    @property
    def price(self):
        locator = BookLocators.PRICE
        expression = "£([0-9]+\.[0-9]+)"
        item_price = self.parent.select_one(locator).string
        matcher = re.search(expression,item_price)
        return float(matcher.group(1))
    
    @property
    def stars(self):
        locator = BookLocators.STAR_RATING
        rating_string = self.parent.select_one(locator).attrs.get("class")[1]
        return BookParser.RATINGS.get(rating_string)
    
    @property
    def title(self):
        locator = BookLocators.TITLE
        return self.parent.select_one(locator).attrs.get("title")
    

class BooksPage:
    
    def __init__(self,page):                            #page= our page content (html code)
        self.soup = BeautifulSoup(page,'html.parser')

    @property
    def book(self):
        locator = AllBooksPageLocators.BOOK_LIST
        book_tags = self.soup.select(locator)          #selecting all of the li.col-xs... tags
        return [BookParser(e) for e in book_tags]     #returns a list of QuoteParser objects


def print_best_books(books):
    best_books = filter(lambda x:x.stars==5 ,books)
    for book in best_books:
        print(book)

def print_cheapest_books(books):
    best_books = sorted(books,key = lambda x:x.price)[:10]
    for book in best_books:
        print(book)

def get_next_book(books):
    print(next(books_generator))



USER_CHOICE = """
- 'b' to look at 5-star books
- 'c' to look at the cheapest books
- 'n' to get the next available book on the catalogue
- 'q' to exit

Enter your choice: """

user_choices = {
    'b': print_best_books,
    'c': print_cheapest_books,
    'n': get_next_book
}

link = 'https://books.toscrape.com/'

page_content = requests.get(link).content
page = BooksPage(page_content)

books_generator = (x for x in page.book)

user_input = input(USER_CHOICE).lower()
while user_input  !='q':
    if user_input in ('b','c','n'):
        user_choices[user_input](page.book)
    else:
        print("Please enter something valid")

    user_input = input(USER_CHOICE).lower()