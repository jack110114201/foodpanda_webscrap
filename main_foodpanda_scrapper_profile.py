import random
import csv
import os
import undetected_chromedriver as uc
#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import datetime


class FoodpandaScraper_profile:
    def __init__(self):
        self.total_info = None

        self.data_profile = {
            'name': '',
            'score': '',
            'comment_cnt': '',
            'style': ''
        }

        self.data_url = {
            'name': '',
            'url': ''
        }

        self.data_feature = {
            'name': '',
            'feature': ''
        }

    def scrape_foodpanda(self, url,area):
        # undetected_chromedriver
        options = uc.ChromeOptions()
        #options.headless=True
        #options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        browser = uc.Chrome(options=options)

        # webdriver
        #chrome_options = Options()
        #chrome_options.add_argument('--no-sandbox')
        #chrome_options.add_argument('--disable-dev-shm-usage')
        #browser = webdriver.Chrome(executable_path='../DAY18/chromedriver', chrome_options=chrome_options)

        #url = "https://www.foodpanda.com.tw/en/city/taipei-city"
        browser.get(url)

        # Enter the area
        #area = "信義區忠孝東路"
        browser.find_element(By.ID, "delivery-information-postal-index").send_keys(area)

        # Click search
        browser.find_element(By.XPATH, '//*[@id="seo-city-page-root"]/div/div[2]/div[2]/div[2]/div[1]/div/div/div[2]/button').click()

        time.sleep(10)
        SCROLL_PAUSE_TIME = 5
        SCROLL_PAUSE_TIME_1 = 5

        last_height = ''
        while True:
            delay_choices = [5, 6, 7, 8, 9]
            delay = random.choice(delay_choices)
            time.sleep(delay)
            browser.execute_script("window.scrollBy(0, 1000);")
            time.sleep(delay)
            browser.execute_script("window.scrollBy(0, 600);")
            time.sleep(delay)
            browser.execute_script("window.scrollBy(0, -500);")
            my_current_url = browser.current_url
            print(my_current_url)
            print(browser.execute_script("return document.body.scrollHeight"))
            try:
                browser.find_element(By.XPATH, '//*[@id="seo-city-page-root"]/div/div[3]/div[1]/section[2]/span')
                print('Closed for now')
                break
            except:
                print('網頁更新中...')

        html_source = browser.page_source
        browser.quit()
        soup = BeautifulSoup(html_source, "html.parser")
        self.total_info = soup.find_all("section", class_="vendor-list-section")
        return self.total_info

    def foodpanda_profile(self, createtime):
        script_dir = os.path.dirname(os.path.abspath('__file__'))
        shop_profile_path = os.path.join(script_dir,f'data/shop_profile_{createtime}.csv')
        shop_url_path = os.path.join(script_dir,f'data/shop_url_{createtime}.csv')
        shop_feature_path = os.path.join(script_dir,f'data/shop_feature_{createtime}.csv')
        
        with open(shop_profile_path, 'w', newline='', encoding="utf8") as shop_profile_file, \
             open(shop_url_path, 'w', newline='', encoding="utf8") as shop_url_file, \
             open(shop_feature_path, 'w', newline='', encoding="utf8") as shop_feature_file:
            shop_profile_writer = csv.DictWriter(shop_profile_file, fieldnames=[*self.data_profile.keys()], delimiter=",")
            shop_url_writer = csv.DictWriter(shop_url_file, fieldnames=[*self.data_url.keys()], delimiter=",")
            shop_feature_writer = csv.DictWriter(shop_feature_file, fieldnames=[*self.data_feature.keys()], delimiter=",")

            shop_profile_writer.writeheader()
            shop_url_writer.writeheader()
            shop_feature_writer.writeheader()

            # 正在營業的店
            open_info = self.total_info[0]

            for x in open_info.find_all("li", class_="vendor-tile-wrapper"):
                # 店名
                name = x.find("a", class_="name fn").text
                #print(name)
                self.data_profile["name"] = name
                self.data_url['name'] = name

                # 評價分數
                try:
                    score = x.find("span", class_="rating--label-primary cl-rating-tag-text f-label-small-font-size fw-label-small-font-weight lh-label-small-line-height").text.split('/')[0]
                    #print(score)
                    self.data_profile["score"] = score
                except:
                    #print('0')
                    self.data_profile["score"] = '0'

                # 評論數
                try:
                    comment_cnt = x.find("span", class_="rating--label-secondary cl-neutral-secondary f-label-small-secondary-font-size fw-label-small-secondary-font-weight lh-label-small-secondary-line-height").text \
                        .replace('(', '') \
                        .replace(')', '') \
                        .replace('+', '')
                    #print(comment_cnt)
                    self.data_profile["comment_cnt"] = comment_cnt
                except:
                    #print('0')
                    self.data_profile["comment_cnt"] = '0'

                # 店家類型
                try:
                    tag = x.find("li", class_="vendor-characteristic").text
                    #print(tag)
                    self.data_profile["style"] = tag
                except:
                    #print('None')
                    self.data_profile["style"] = 'None'

                # 網址
                url = 'https://www.foodpanda.com.tw/' + x.find("a", class_="name fn").get('href')
                #print(url)
                self.data_url["url"] = url

                # 特徵、優惠
                try:
                    features = x.find_all("span", class_="box-flex fd-row ai-center")
                    # 定位的到，但回傳是空list
                    if len(features) == 0:
                        #print('None')
                        self.data_feature["name"] = name
                        self.data_feature["feature"] = 'None'
                        shop_feature_writer.writerow(self.data_feature)
                    else:
                        for j in features:
                            feature = j.text
                            if feature == 'Featured':
                                pass
                            else:
                                #print(feature)
                                self.data_feature["name"] = name
                                self.data_feature["feature"] = feature
                                shop_feature_writer.writerow(self.data_feature)
                except:
                    #print('None')
                    self.data_feature["name"] = name
                    self.data_feature["feature"] = 'None'
                    shop_feature_writer.writerow(self.data_feature)

                shop_profile_writer.writerow(self.data_profile)
                shop_url_writer.writerow(self.data_url)
                #print('--------------------------------------------------------------------------------------------------')
            # 尚未營業的店
            #close_info = total_info[1]
        print('Finish!')
if __name__ == '__main__':
    FoodpandaScraper = FoodpandaScraper_profile()
    url = "https://www.foodpanda.com.tw/en/city/taipei-city"
    area = "信義區忠孝東路"
    FoodpandaScraper.scrape_foodpanda(url,area)
    createtime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    FoodpandaScraper.foodpanda_profile(createtime)

























