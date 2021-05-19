from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import time
from random import randint

def random_time_wait(base):
    
    value = randint(0, 5)
    
    time.sleep(base + value)

class AutoMercado():
    
    def __init__(self, driver):
        
        self.driver = driver
        
        self.cars_data = []
        
        self.next_page = True 
        
    def go_next_page(self):
        
        try:
            
            pagination = self.driver.find_element_by_class_name('ui-search-pagination')
        
            self.driver.execute_script("arguments[0].scrollIntoView();", pagination)
        
            next_button = pagination.find_element_by_class_name('andes-pagination__button--next')
        
            next_button.click()
        
        except:
            
            self.next_page = False
    
    def get_cars(self):
        
        section = driver.find_element_by_class_name('ui-search-results')

        rows = section.find_elements_by_tag_name('ol')
        
        self.cars = []
        
        for row in rows:
            
            cars_in_row = row.find_elements_by_class_name('ui-search-result__content')
            
            for car in cars_in_row:
                
                self.cars.append(car)
    
    def go_to_car(self, car):
        
        car_url = car.get_attribute('href')
        
        self.driver.execute_script("window.open('');")

        self.driver.switch_to.window(driver.window_handles[1])
        
        self.driver.get(car_url)
        
    def return_menu(self):
        
        self.driver.close()
        
        self.driver.switch_to.window(self.driver.window_handles[0])
        
    def get_car_data(self):
        
        car_page = BeautifulSoup(self.driver.page_source, 'html.parser')

        car_name = car_page.find('h1', class_='ui-pdp-title').text
        
        price_tag = car_page.find('span', class_='price-tag')

        currency , price = price_tag.find_all('span')

        currency = currency.text
        price = price.text

        car_data_sheet = car_page.find('table', class_='andes-table')
        
        car_data_rows = car_data_sheet.find_all('tr')
        
        x = {}
        
        x['Nombre'] = car_name
        x['Moneda'] = currency
        x['Precio'] = price
        
        for row in car_data_rows:
            
            char_name = row.find('th').text
            char = row.find('td').span.text
            
            x[char_name] = char
            
            
        self.cars_data.append(x)
        
if __name__ == '__main__':

    driver = webdriver.Chrome('./chromedriver')
    
    links_txt = open("./links.txt", "r")
    links = links_txt.readlines()
    
    web_mercado = AutoMercado(driver)
    
    for link in links:
        
        try:
            driver.get(link)
        except:
            continue
            
        web_mercado.next_page = True
        
        random_time_wait(3)
        
        while web_mercado.next_page:
            
            web_mercado.get_cars()
        
            for car in web_mercado.cars:
                
                web_mercado.go_to_car(car)
                
                random_time_wait(5)
                
                try:
                    web_mercado.get_car_data() #NOT EVERY CAR HAS A DATA SHEET
                except:
                    pass
                
                random_time_wait(1)
                
                web_mercado.return_menu()
                
                random_time_wait(1)
            
            web_mercado.go_next_page()
    
    driver.close()
    
    df = pd.DataFrame.from_dict(web_mercado.cars_data)
    
    df.to_excel('cars_data.xlsx')