# python -m pytest main.py --html=log.html

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class IMDbSearchPage:
    def __init__(self, driver):
        self.driver = driver
        self.search_box = (By.ID, 'suggestion-search')
        self.search_button = (By.ID, 'suggestion-search-button')
        self.filter_dropdown = (By.ID, 'SearchFilter')
        self.genre_dropdown = (By.ID, 'genres')
        self.sort_by_dropdown = (By.ID, 'sort')
        self.rating_range_min = (By.NAME, 'user_rating_min')
        self.rating_range_max = (By.NAME, 'user_rating_max')

    def enter_search_text(self, text):
        self.driver.find_element(*self.search_box).send_keys(text)

    def click_search_button(self):
        self.driver.find_element(*self.search_button).click()

    def select_filter(self, filter_option):
        filter_dropdown = self.driver.find_element(*self.filter_dropdown)
        filter_dropdown.click()
        filter_dropdown.find_element(By.XPATH, f"//option[text()='{filter_option}']").click()

    def select_genre(self, genre_option):
        genre_dropdown = self.driver.find_element(*self.genre_dropdown)
        genre_dropdown.click()
        genre_dropdown.find_element(By.XPATH, f"//option[text()='{genre_option}']").click()

    def select_sort_by(self, sort_option):
        sort_by_dropdown = self.driver.find_element(*self.sort_by_dropdown)
        sort_by_dropdown.click()
        sort_by_dropdown.find_element(By.XPATH, f"//option[text()='{sort_option}']").click()

    def enter_rating_range(self, min_rating, max_rating):
        self.driver.find_element(*self.rating_range_min).send_keys(min_rating)
        self.driver.find_element(*self.rating_range_max).send_keys(max_rating)

@pytest.fixture
def setup():
    # Initialize the webdriver
    driver = webdriver.Chrome()
    driver.get("https://www.imdb.com/search/name/")
    
    # Set up an implicit wait
    driver.implicitly_wait(10)

    yield driver

    # Clean up after the test
    driver.quit()

def test_imdb_search(setup):
    # Create an instance of the IMDbSearchPage
    imdb_search_page = IMDbSearchPage(setup)

    # Perform the search with the specified criteria
    imdb_search_page.enter_search_text("Tom Hanks")
    imdb_search_page.select_filter("Titles")
    imdb_search_page.select_genre("Drama")
    imdb_search_page.select_sort_by("Popularity")
    imdb_search_page.enter_rating_range("7", "10")
    imdb_search_page.click_search_button()

    # Use Explicit Wait for the search results to load
    wait = WebDriverWait(setup, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'lister-list')))

    # Additional Assertions or Actions can be added based on the test requirements

if __name__ == "__main__":
    pytest.main()
