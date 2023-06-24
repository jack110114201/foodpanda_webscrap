# 一、專題摘要
1. 專題主題 : Foodpanda網站爬蟲
2. 基本目標 :
   *  獲得餐廳販售的品項名稱、價格…等資訊
   *  爬取的資訊寫入csv檔，再導入postgres db
3. 進階目標:
   * 串接Kakfa，爬取的資訊寫至producer，再透過consumer將資料導入postgres db
# 二、基本目標流程圖:
![link](https://github.com/jack110114201/foodpanda_webscrap/blob/6afd0d1cb0afbc36e153665e94657c638801ec73/upload_image/%E5%9F%BA%E6%9C%AC%E7%9B%AE%E6%A8%99_%E6%B5%81%E7%A8%8B%E5%9C%96.jpg)
# 三、進階目標流程圖:
![link](https://github.com/jack110114201/foodpanda_webscrap/blob/4a53e28adb6391cb77f92fd8b05007179fed9655/upload_image/%E9%80%B2%E9%9A%8E%E7%9B%AE%E6%A8%99_%E6%B5%81%E7%A8%8B%E5%9C%96.drawio.png)
# 四、基本_主要程式說明
序號|程式名稱|功能敘述
|:---:|:----:|:----|
1|main_foodpanda_scrapper_profile.py|1.收集餐廳資訊(餐廳基本資訊,餐廳url網址資訊,餐廳特徵資訊)<br>2.將收集到的資訊儲存成csv，放置/data目錄
2|main_foodpanda_scrapper_detail_vr_csv.py|1.讀取餐廳url網址資訊csv檔<br>2.依據檔案中的url網址爬取餐廳資訊(餐廳地址資訊,餐廳營業時間,餐廳完整特徵資訊,餐廳餐點資訊)<br>3.將收集到的資訊儲存成csv，放置/data目錄
3|main_create_table.py|1.依據/script目錄下的.sql，在postgres db建立7張table
4|main_insert_data.py|1.依據/data目錄下的csv，導入postgres db table
# 五、進階_主要程式說明
- 替換基本主要程式序號2、4

序號|程式名稱|功能敘述
|:---:|:----:|:----|
1|main_foodpanda_scrapper_detail_vr_kafka_producer.py|1.讀取餐廳url網址資訊csv檔<br>2.依據檔案中的url網址爬取餐廳資訊(餐廳地址資訊,餐廳營業時間,餐廳完整特徵資訊,餐廳餐點資訊)<br>3.將收集到的資訊儲存成json格式的資料，並透過kafka producer寫至topic: test中
2|main_insert_data_kafka_consumer.py|1.透過kafka consumer將接收到的資訊，寫至/kafka_consumer_data/consumer_log_yyyymmdd.json<br>2.寫完log資訊後，再將資訊導入postgres db table



 
