import undetected_chromedriver as uc
import csv
import json
import random
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from urllib import error as urlliberror
from confluent_kafka import Producer
import time
import datetime
import os
import sys
import errno
import http.client


class FoodpandaScraper_product_detail:
    def __init__(self):
        self.cnt = 0
        self.delay_choices = [5, 6, 7]  #延遲的秒數
        self.path = os.path.dirname(os.path.abspath('__file__'))  # 檔案所在的目錄路徑
        # 設定要連線到 Kafka 集群的相關設定
        self.props = {
                      'bootstrap.servers': 'localhost:9092',
                      'error_cb': self.error_cb
                     }
        self.producer = Producer(self.props)
    
    def find_lastest_url_file(self):
        prefix = "shop_url"  # 檔案名稱前綴
        # 列出目錄下所有以指定前綴開頭的檔案
        files = [f for f in os.listdir(self.path) if f.startswith(prefix)]
        # 將檔案按照最後修改時間排序，並取最後一個即為最新創建的檔案
        latest_url_file_path = sorted(files, key=lambda x: os.path.getmtime(os.path.join(self.path, x)), reverse=True)[0]
        print("最新創建的檔案是:", latest_url_file_path)
        return latest_url_file_path
    # 用來接收從 Consumer instance 發出的 error 訊息
    def error_cb(err):
        sys.stderr.write(f'Error: {err}')

    def kafka_producer(self,key_name,data):
        # 指定想要訂閱訊息的 topic 名稱
        topicName = 'test'
        try:
            print('Start sending messages ...')
            time_start = int(round(time.time() * 1000))
            # Convert data to JSON string
            scrap_data_json = json.dumps(data)

            # Send the message to Kafka
            self.producer.produce(topicName, key=key_name, value=scrap_data_json)
            self.producer.poll(0) # 呼叫 poll 來讓 client 程式去檢查內部的 Buffer, 並觸發 callback
            cnt = 1
            print(f'Sent {cnt} message')
            time_spend = int(round(time.time() * 1000)) - time_start
            print(f'Sent        : {cnt} messages to Kafka')
            print(f'Total spent : {time_spend} milliseconds')
        except BufferError as e:
            sys.stderr.write(
                             f'Local producer queue is full ({len(self.producer)} messages awaiting delivery): try again'
            )
        except Exception as e:
            sys.stderr.write(str(e))
        self.producer.flush(10)
        print('Message sending completed!')

    def foodpanda_product_detail(self, createtime):
        latest_url_file_path = self.find_lastest_url_file()

        with open(latest_url_file_path, "r") as ref_url:
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
                scrap_data = {
                           'name': '',
                           'createtime' : '',
                           'data_adr': '',
                           'data_time' : [],
                           'data_feature_detail' : [],
                           'data_product_detail' : []
                          }
                try:
                    json_script = soup.find("script",{'data-testid': 'restaurant-seo-schema'})
                    json_text = json_script.string
                    shop_data = json.loads(json_text)

                    # 填入producer資訊
                    scrap_data['name'] = shop_data['name']
                    scrap_data['createtime'] = createtime

                    # data_adr資訊
                    data_adr = {
                                'name' : shop_data['name'],
                                'country' : shop_data['address']['addressCountry'],
                                'postalCode' : shop_data['address']['postalCode'],
                                'address' : shop_data['address']['streetAddress'].split(')')[1],
                                'latitude' : shop_data['areaServed']['geoMidpoint']['latitude'],
                                'longitude' : shop_data['areaServed']['geoMidpoint']['longitude'],
                                'telephone' : shop_data['telephone']
                                }
                    scrap_data['data_adr'] = data_adr

                    # data_time資訊      
                    for time_detail in shop_data['openingHoursSpecification']:
                        # 分成平日、假日
                        for k in time_detail['dayOfWeek']:
                            data_time = {
                                'name' : shop_data['name']
                                ,'dayOfWeek' : k
                                ,'opens_time' : time_detail['opens']
                                ,'closes_time' : time_detail['closes']
                            }
                            scrap_data['data_time'].append(data_time)

                    # data_feature_detail資訊 
                    for feature in shop_data['servesCuisine']:
                        data_feature_detail = {
                                               'name': shop_data['name'],
                                               'feature': feature
                                              }
                        scrap_data['data_feature_detail'].append(data_feature_detail)
                    
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
                                data_product_detail = {
                                                       'name' : shop_data['name'],
                                                       'product' : product,
                                                       'price' : price,
                                                      }
                                scrap_data['data_product_detail'].append(data_product_detail)
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
                    # Kafka 傳送producer資料
                    self.kafka_producer(shop_data['name'],scrap_data)
                    time.sleep(10)
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