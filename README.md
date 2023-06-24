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
# 四、基本_主要程式說明:
序號|程式名稱|功能敘述
|:---|:----|:----|
1|main_foodpanda_scrapper_profile.py|1.收集餐廳資訊(餐廳基本資訊,餐廳url網址資訊,餐廳特徵資訊)<br>2.將收集到的資訊儲存成csv，放置/data目錄
2|main_foodpanda_scrapper_detail_vr_csv.py|1.讀取餐廳url網址資訊csv檔<br>2.依據檔案中的url網址爬取餐廳資訊(餐廳地址資訊,餐廳營業時間,餐廳完整特徵資訊,餐廳餐點資訊)<br>3.將收集到的資訊儲存成csv，放置/data目錄
3|main_create_table.py|1.依據/script目錄下的.sql，在postgres db建立7張table
4|main_insert_data.py|1.依據/data目錄下的csv，導入postgres db table
# 五、基本主要程式開發流程、遇到的問題&解決措施:
1. 流程:
   * 透過undected-selenium的方式進入Foodpanda 地點位於台北市的頁面: https://www.foodpanda.com.tw/en/city/taipei-city
   * 在搜尋餐廳資訊前，需要定義好地區範圍。實作是輸入”信義區忠孝東路”
   * 進入選擇餐廳的網頁，開始爬取需要的資訊
   * 將爬取到的資訊儲存至csv檔案
     - 餐廳基本資訊
     - 餐廳url網址資訊
     - 餐廳特徵資訊
   * 讀取餐廳url網址資訊的csv檔案，使用儲存的url資訊，另透過undetected-chromedriver的方式，進入餐廳的點餐頁面進行爬取資訊
   * 將爬取到的資訊儲存至csv檔案
     - 餐廳地址資訊
     - 餐廳營業時間
     - 餐廳完整特徵資訊
     - 餐廳餐點資訊
   * 爬取的資訊都存成csv檔案後，再把資訊導入Postgres db
     - pdata.shop_profile
     - pdata.shop_url
     - pdata.shop_feature
     - pdata.shop_adr
     - pdata.shop_time
     - pdata.shop_feature_detail
     - pdata.shop_product_detail
2. 遇到的問題&解決措施:
   * 餐廳的網頁屬於動態生成的頁面，最一開始透過指令直接移動到頁面最底部，預期會觸動動態生成的機制，但不會觸動:
     - 措施: 透過window.scrollBy的方式，慢慢滑動頁面
   * 透過window.scrollBy的方式，有時候頁面還沒加載完成，就繼續滑動頁面，導致頁面又跑到頁面的最底部:
     - 措施: 除了延遲向下滑動頁面外，也有做向上滑動頁面的動作
   * 餐廳數量很多，不知道要爬到何年何月:
     - 措施: 訂定停止點，當爬到目前尚不接受點餐(Closed for now)的資訊，就停止爬取資訊
   * 原本是透過chromedriver的方式去爬取資訊，但在進行爬取點餐頁面資訊時，高機率遇到機器人機制的情況。曾嘗試延遲爬取資訊的間隔時間、停留在頁面上久一點、進入餐廳點餐頁面前，先進入其他的網頁..等方式，皆無法解決:
     - 措施: 改使用undtected-chromedriver的方式
   * 改使用undtected-chromedriver的方式，偶爾還是會遇到下列情況，尚待改善:
     - 連續啟動爬蟲程式，還是可能會遇到機器人機制，但手動通過驗證後，程式可繼續執行
     - 有遇過完全無法連進Foodpanda網站，或者雖然出現機器人機制，但不給我手動驗證的情況
   * undtected-chromedriver需要使用的chrome版本與local版本不一致，更新chrome版本方式:
     - sudo apt-get update
     - sudo apt-get --only-upgrade install google-chrome-stable
# 六、進階_主要程式說明:
- 替換基本主要程式序號2、4

序號|程式名稱|功能敘述
|:---|:----|:----|
1|main_foodpanda_scrapper_detail_vr_kafka_producer.py|1.讀取餐廳url網址資訊csv檔<br>2.依據檔案中的url網址爬取餐廳資訊(餐廳地址資訊,餐廳營業時間,餐廳完整特徵資訊,餐廳餐點資訊)<br>3.將收集到的資訊儲存成json格式的資料，並透過kafka producer寫至topic: test中
2|main_insert_data_kafka_consumer.py|1.透過kafka consumer將接收到的資訊，寫至/kafka_consumer_data/consumer_log_yyyymmdd.json<br>2.寫完log資訊後，再將資訊導入postgres db table
# 七、進階主要程式開發過程:
1. 過程:
   * 手動建立Kafka topic
   * 將基礎目標程式(main_foodpanda_scrapper_detail_vr_csv.py)調整成將爬取的資訊傳送至kafka producer的版本
   * 將基礎目標程式(main_insert_data.py)調整成透過kafka consumer接收資訊，取代讀取csv檔的版本
     - 僅規劃接收餐廳地址資訊,餐廳營業時間,餐廳完整特徵資訊,餐廳餐點資訊
# 八、未來優化事項:
1. 檢視儲存在db的資料後，發現爬取到的資料有待清洗的空間，例如文字前後有空格、有些資訊沒爬取完整等
2. 目前是透過url檔案進行餐廳商品的資料爬取，如果過程中程式中斷，重新啟動程式，會必須從第1筆url開始執行。應可調整成功爬取資料後，將該筆url移除，後續執行程式，就可從新的資料開始爬取。
3. 目前都是透過手動執行程式的方式，後續嘗試透過AirFlow進行排程執行。



 
