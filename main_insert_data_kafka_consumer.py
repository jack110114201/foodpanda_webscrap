import sys
import json
import os
import datetime
from confluent_kafka import Consumer, KafkaException, KafkaError
from tools.insert_data_tool import *
from config.insert_data_config import *



class KafkaConsumer:
    def __init__(self):
        # 用來接收從 Consumer instance 發出的 error 訊息
        self.error_cb = self.error_callback
        # 當發生 commit 時被呼叫
        self.commit_cb = self.commit_callback
        # 設定要連線到 Kafka 集群的相關設定
        self.props = {
            'bootstrap.servers': 'localhost:9092',         # Kafka 集群在那裡? (置換成要連接的 Kafka 集群)
            'group.id': 'foodpanda_data',                  # ConsumerGroup 的名稱
            'auto.offset.reset': 'earliest',               # 是否從這個 ConsumerGroup 尚未讀取的 partition/offset 開始讀
            'enable.auto.commit': True,                    # 是否啟動自動 commit
            'auto.commit.interval.ms': 5000,               # 自動 commit 的 interval
            'on_commit': self.commit_cb,                   # 設定接收 commit 訊息的 callback 函數
            'error_cb': self.error_cb                       # 設定接收 error 訊息的 callback 函數
        }
        self.consumer = Consumer(self.props)
        self.path = os.path.dirname(os.path.abspath('__file__'))  # 檔案所在的目錄路徑
        self.createdate = datetime.datetime.now().strftime('%Y%m%d')

    def error_callback(self, err):
        sys.stderr.write(f'Error: {err}')

    def commit_callback(self, err, partitions):
        if err:
            print(f'Failed to commit offsets: {err}: {partitions}')
        else:
            for p in partitions:
                print(f'Committed offsets for: {p.topic}-{p.partition} [offset={p.offset}]')

    # 轉換 msg_key 或 msg_value 成為 utf-8 的字串
    def try_decode_utf8(self, data):
        return data.decode('utf-8') if data else None

    def write_data_log(self, path, data):
        with open(path, 'a',encoding='utf-8') as data_writer:
            data_writer.write(data + '\n')

    def process_records(self, records):
        data_inserter = DataInserter()
        for record in records:
            if not record:
                continue

            # 檢查是否有錯誤
            if record.error() and record.error().code() != KafkaError._PARTITION_EOF:
                raise KafkaException(record.error())
            else:
                # ** 在這裡進行商業邏輯與訊息處理 **

                # 取出相關的 metadata
                topic = record.topic()
                partition = record.partition()
                offset = record.offset()

                # 取出 msg_key 與 msg_value
                msg_key = self.try_decode_utf8(record.key())
                msg_value = self.try_decode_utf8(record.value())
                
                # 把kafka相關資訊彙整進爬蟲下來的資料，作為一筆log
                data = json.loads(msg_value)
                data['topic'] = topic
                data['partition'] = partition
                data['offset'] = offset
                data['msg_key'] = msg_key
                data['data_recvdatetime'] = datetime.datetime.now().strftime('%Y-%m-%d- %H:%M:%S')

                # 秀出 metadata
                data_str = json.dumps(data,ensure_ascii=False)
                print(data_str)
                lag_path = os.path.join(self.path, f'kafka_consumer_data/consumer_log_{self.createdate}.json')
                log = self.write_data_log(lag_path, data_str)    
                # 處理data_adr資料
                data_adr = data['data_adr']
                data_inserter.insert_consumer_data(shop_adr_data_config['table_name'],
                                                   data_adr,
                                                   shop_adr_data_config['column_names'],
                                                   shop_adr_data_config['conflict_columns'],
                                                   shop_adr_data_config['update_columns'])    
                # 處理data_time資料
                data_time = data['data_time']
                for shop_week_time in data_time:
                    data_inserter.insert_consumer_data(shop_time_data_config['table_name'],
                                                       shop_week_time,
                                                       shop_time_data_config['column_names'],
                                                       shop_time_data_config['conflict_columns'],
                                                       shop_time_data_config['update_columns'])   
                # 處理data_feature_detail資料
                data_feature_detail = data['data_feature_detail']
                for shop_feature in data_feature_detail:
                    data_inserter.insert_consumer_data(shop_feature_detail_data_config['table_name'],
                                                       shop_feature,
                                                       shop_feature_detail_data_config['column_names'],
                                                       shop_feature_detail_data_config['conflict_columns'],
                                                       shop_feature_detail_data_config['update_columns'])    
                # 處理data_product_detail資料
                data_product_detail = data['data_product_detail']
                for shop_product in data_product_detail:
                    data_inserter.insert_consumer_data(shop_product_detail_data_config['table_name'],
                                                       shop_product,
                                                       shop_product_detail_data_config['column_names'],
                                                       shop_product_detail_data_config['conflict_columns'],
                                                       shop_product_detail_data_config['update_columns'])

    def consume_messages(self):
        # 指定想要訂閱訊息的 topic 名稱
        topicName = 'test'

        # 讓 Consumer 向 Kafka 集群訂閱指定的 topic
        self.consumer.subscribe([topicName])

        try:
            # 持續的拉取 Kafka 有進來的訊息
            while True:
                # 請求 Kafka 把新的訊息吐出來
                records = self.consumer.consume(num_messages=500, timeout=1.0)  # 批次讀取

                if not records:
                    continue

                self.process_records(records)

        except KeyboardInterrupt as e:
            sys.stderr.write('Aborted by user\n')

        except Exception as e:
            sys.stderr.write(str(e))

        finally:
            # 關掉 Consumer 實例的連線
            self.consumer.close()


if __name__ == '__main__':
    consumer = KafkaConsumer()
    consumer.consume_messages()
                

