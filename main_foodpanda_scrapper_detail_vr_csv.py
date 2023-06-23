import undetected_chromedriver as uc
import csv
import json
import random
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from urllib import error as urlliberror
import time
import datetime
import os
import errno
import http.client


class FoodpandaScraper_product_detail:
    def __init__(self):
        self.data_adr = {
            'name' : '',
            'country' : '',
            'postalCode' : '',
            'address' : '',
            'latitude' : '',
            'longitude' : '',
            'telephone' : ''  
            }
        self.data_time = {
            'name' : '',
            'dayOfWeek' : '',
            'opens_time' : '',
            'closes_time' : ''
            }
        self.data_feature_detail = {
            'name': '',
            'feature': ''
        }
        self.data_product_detail = {
            'name' : '',
            'product' : '',
            'price' : '',
            }
        self.cnt = 0
        self.delay_choices = [5, 6, 7]  #延遲的秒數
        self.path = os.path.dirname(os.path.abspath('__file__'))  # 檔案所在的目錄路徑

    def find_lastest_url_file(self):
        prefix = "shop_url"  # 檔案名稱前綴
        # 列出目錄下所有以指定前綴開頭的檔案
        files = [f for f in os.listdir(self.path) if f.startswith(prefix)]
        # 將檔案按照最後修改時間排序，並取最後一個即為最新創建的檔案
        latest_url_file_path = sorted(files, key=lambda x: os.path.getmtime(os.path.join(self.path, x)), reverse=True)[0]
        print("最新創建的檔案是:", latest_url_file_path)
        return latest_url_file_path
    
    def foodpanda_product_detail(self, createtime):
        latest_url_file_path = self.find_lastest_url_file()
        shop_adr_path = os.path.join(self.path, f'data/shop_adr_{createtime}.csv')
        shop_time_path = os.path.join(self.path, f'data/shop_time_{createtime}.csv')
        shop_feature_detail_path = os.path.join(self.path, f'data/shop_feature_detail_{createtime}.csv')
        shop_product_detail_path = os.path.join(self.path, f'data/shop_product_detail_{createtime}.csv')

        with open(latest_url_file_path, "r") as ref_url,\
             open(shop_adr_path,'w',newline='', encoding="utf8") as shop_adr_file,\
             open(shop_time_path,'w',newline='', encoding="utf8") as shop_time_file,\
             open(shop_feature_detail_path,'w',newline='', encoding="utf8") as shop_feature_detail_file,\
             open(shop_product_detail_path,'w',newline='', encoding="utf8") as shop_product_detail_file:
            shop_adr_writer = csv.DictWriter(shop_adr_file, fieldnames=[*self.data_adr.keys()], delimiter=",")
            shop_time_writer = csv.DictWriter(shop_time_file, fieldnames=[*self.data_time.keys()], delimiter=",")
            shop_feature_detail_writer = csv.DictWriter(shop_feature_detail_file, fieldnames=[*self.data_feature_detail.keys()], delimiter=",")
            shop_product_detail_writer = csv.DictWriter(shop_product_detail_file, fieldnames=[*self.data_product_detail.keys()], delimiter=",")

            shop_adr_writer.writeheader()
            shop_time_writer.writeheader()
            shop_feature_detail_writer.writeheader()
            shop_product_detail_writer.writeheader()

            # 讀取url file中的data
            reader = csv.reader(ref_url)
            header = next(reader)  # 讀取標題行,忽略header資料
            for row in reader:
                print(row[0],':',row[1])
                
                # 進入爬蟲階段
                options = uc.ChromeOptions()
                #options.headless=True  
                #options.add_argument('--headless=new')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                browser = uc.Chrome(options=options)
                browser.get(row[1])
                time.sleep(random.choice(self.delay_choices))
                ActionChains(browser).move_by_offset(20, 20).click().perform() # 鼠標左鍵點擊， 200爲x座標， 100爲y座標
                time.sleep(random.choice(self.delay_choices))
                # 滑動頁面
                for i in range(3):
                    browser.execute_script('window.scrollBy(0, {x});'.format(x = random.uniform(1500, 2500))) #隨機選取拉動幅度
                    time.sleep(random.choice(self.delay_choices))
                # 取得html資料
                html_source = browser.page_source
                soup = BeautifulSoup(html_source, "html.parser")
                try:
                    json_script = soup.find("script",{'data-testid': 'restaurant-seo-schema'})
                    json_text = json_script.string
                    shop_data = json.loads(json_text)

                    # data_adr資訊
                    self.data_adr['name'] = shop_data['name']
                    self.data_adr['country'] = shop_data['address']['addressCountry']
                    self.data_adr['postalCode'] = shop_data['address']['postalCode']
                    self.data_adr['address'] = shop_data['address']['streetAddress'].split(')')[1]
                    self.data_adr['latitude'] = shop_data['areaServed']['geoMidpoint']['latitude']
                    self.data_adr['longitude'] = shop_data['areaServed']['geoMidpoint']['longitude']
                    self.data_adr['telephone'] = shop_data['telephone']
                    shop_adr_writer.writerow(self.data_adr)
        
                    # data_time資訊      
                    for time_detail in shop_data['openingHoursSpecification']:
                        for k in time_detail['dayOfWeek']:
                            self.data_time['name'] = shop_data['name']
                            self.data_time['dayOfWeek'] = k
                            self.data_time['opens_time'] = time_detail['opens']
                            self.data_time['closes_time'] = time_detail['closes']
                            shop_time_writer.writerow(self.data_time)
                    
                    # data_feature_detail資訊 
                    for feature in shop_data['servesCuisine']:
                        self.data_feature_detail['name'] = shop_data['name']
                        self.data_feature_detail['feature'] = feature 
                        shop_feature_detail_writer.writerow(self.data_feature_detail)
                
                    #data_product_detail資訊
                    products = soup.find_all("li",class_ = 'box-flex dish-card bg-white jc-space-between p-relative sm:pl-zero md:pl-md lg:pl-md pl-sm sm:pr-zero md:pr-md lg:pr-md pr-sm sm:pt-zero md:pt-md lg:pt-md pt-sm sm:pb-sm md:pb-md lg:pb-md pb-sm br-xxs bs-1')
          
                    for i in products:
                        product_all = i.find("button")['aria-label'].split(',')
                        product = product_all[0]
                        price = product_all[1].split('-')[0].strip().replace('$','')
                        try:
                            if int(price) == 0:
                                pass
                            else:
                                self.data_product_detail['name'] = shop_data['name']
                                self.data_product_detail['product'] = product
                                self.data_product_detail['price'] = price
                                shop_product_detail_writer.writerow(self.data_product_detail)
                        except:
                            pass
                    browser.quit() #https://blog.csdn.net/yangfengjueqi/article/details/84338167
                    #解決辦法: https://github.com/SeleniumHQ/selenium/issues/8612
                    #conn = http.client.HTTPConnection(browser.service.service_url.split("//")[1])
                    #conn.request("GET", "/shutdown")
                    #conn.close()
                    #del browser
                    self.cnt += 1
                    print(self.cnt)
                    time.sleep(20)
                # https://blog.csdn.net/qq_37163925/article/details/115277342
                except urlliberror as e:
                    if e.errno != errno.ECONNRESET:
                        exit_code = 1
                        print(f"執行{row[0]}過程發生錯誤")
                        exit(exit_code)
                        raise
                    else:
                        print(f"執行{row[0]}過程發生ECONNRESET")
                        pass        
                except:
                    exit_code = 1
                    print(f"執行{row[0]}過程發生錯誤")
                    exit(exit_code)  
if __name__ == '__main__':
    createtime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    FoodpandaScraper = FoodpandaScraper_product_detail()
    FoodpandaScraper.foodpanda_product_detail(createtime)