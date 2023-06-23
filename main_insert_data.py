from tools.insert_data_tool import *
from config.insert_data_config import *
import os


main_path = os.getcwd()  # 程式所在的目錄路徑
data_path = 'data'
combine_path = os.path.join(main_path,data_path)# 檔案所在的目錄路徑


# shop_profile
shop_profile_prefix = "shop_profile"  # 檔案名稱前綴
shop_profile_files = [f for f in os.listdir(combine_path) if f.startswith(shop_profile_prefix)]
# 將檔案按照最後修改時間排序，並取最後一個即為最新創建的shop_profile_file檔案
shop_profile_file = sorted(shop_profile_files, key=lambda x: os.path.getmtime(os.path.join(combine_path, x)), reverse=True)[0]
shop_profile_data_path = os.path.join(combine_path,shop_profile_file)
print("最新創建的shop_profile檔案是:", shop_profile_data_path)

# shop_feature
shop_feature_prefix = "shop_feature"
shop_feature_files = [f for f in os.listdir(combine_path) if f.startswith(shop_feature_prefix)]
shop_feature_file = sorted(shop_feature_files, key=lambda x: os.path.getmtime(os.path.join(combine_path, x)), reverse=True)[0]
shop_feature_data_path = os.path.join(combine_path,shop_feature_file)
print("最新創建的shop_feature檔案是:", shop_feature_data_path)

# shop_url
shop_url_prefix = "shop_url"
shop_url_files = [f for f in os.listdir(combine_path) if f.startswith(shop_url_prefix)]
shop_url_file = sorted(shop_url_files, key=lambda x: os.path.getmtime(os.path.join(combine_path, x)), reverse=True)[0]
shop_url_data_path = os.path.join(combine_path,shop_url_file)
print("最新創建的shop_url檔案是:", shop_url_data_path)

# shop_adr
shop_adr_prefix = "shop_adr"
shop_adr_files = [f for f in os.listdir(combine_path) if f.startswith(shop_adr_prefix)]
shop_adr_file = sorted(shop_adr_files, key=lambda x: os.path.getmtime(os.path.join(combine_path, x)), reverse=True)[0]
shop_adr_data_path = os.path.join(combine_path,shop_adr_file)
print("最新創建的shop_adr檔案是:", shop_adr_data_path)

# shop_time
shop_time_prefix = "shop_time"
shop_time_files = [f for f in os.listdir(combine_path) if f.startswith(shop_time_prefix)]
shop_time_file = sorted(shop_time_files, key=lambda x: os.path.getmtime(os.path.join(combine_path, x)), reverse=True)[0]
shop_time_data_path = os.path.join(combine_path,shop_time_file)
print("最新創建的shop_time檔案是:", shop_time_data_path)

# shop_feature_detail
shop_feature_detail_prefix = "shop_feature_detail"
shop_feature_detail_files = [f for f in os.listdir(combine_path) if f.startswith(shop_feature_detail_prefix)]
shop_feature_detail_file = sorted(shop_feature_detail_files, key=lambda x: os.path.getmtime(os.path.join(combine_path, x)), reverse=True)[0]
shop_feature_detail_data_path = os.path.join(combine_path,shop_feature_detail_file)
print("最新創建的shop_feature_detail檔案是:", shop_feature_detail_data_path)

# shop_product_detail
shop_product_detail_prefix = "shop_product_detail"
shop_product_detail_files = [f for f in os.listdir(combine_path) if f.startswith(shop_product_detail_prefix)]
shop_product_detail_file = sorted(shop_product_detail_files, key=lambda x: os.path.getmtime(os.path.join(combine_path, x)), reverse=True)[0]
shop_product_detail_data_path = os.path.join(combine_path,shop_product_detail_file)
print("最新創建的shop_product_detail檔案是:", shop_product_detail_data_path)



data_inserter = DataInserter()
data_inserter.insert_data(shop_profile_data_config['table_name']
                          ,shop_profile_data_path
                          ,shop_profile_data_config['column_names']
                          ,shop_profile_data_config['conflict_columns']
                          ,shop_profile_data_config['update_columns'])

data_inserter.insert_data(shop_feature_data_config['table_name']
                          ,shop_feature_data_path
                          ,shop_feature_data_config['column_names']
                          ,shop_feature_data_config['conflict_columns']
                          ,shop_feature_data_config['update_columns'])

data_inserter.insert_data(shop_url_data_config['table_name']
                          ,shop_url_data_path
                          ,shop_url_data_config['column_names']
                          ,shop_url_data_config['conflict_columns']
                          ,shop_url_data_config['update_columns'])

data_inserter.insert_data(shop_adr_data_config['table_name']
                          ,shop_adr_data_path
                          ,shop_adr_data_config['column_names']
                          ,shop_adr_data_config['conflict_columns']
                          ,shop_adr_data_config['update_columns'])

data_inserter.insert_data(shop_time_data_config['table_name']
                          ,shop_time_data_path
                          ,shop_time_data_config['column_names']
                          ,shop_time_data_config['conflict_columns']
                          ,shop_time_data_config['update_columns'])

data_inserter.insert_data(shop_feature_detail_data_config['table_name']
                          ,shop_feature_detail_data_path
                          ,shop_feature_detail_data_config['column_names']
                          ,shop_feature_detail_data_config['conflict_columns']
                          ,shop_feature_detail_data_config['update_columns'])

data_inserter.insert_data(shop_product_detail_data_config['table_name']
                          ,shop_product_detail_data_path
                          ,shop_product_detail_data_config['column_names']
                          ,shop_product_detail_data_config['conflict_columns']
                          ,shop_product_detail_data_config['update_columns'])