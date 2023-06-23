from tools.create_table_tool import *
import os


main_path = os.getcwd()  # 程式所在的目錄路徑
sql_script_path = 'sql_script'
combine_path = os.path.join(main_path,sql_script_path)# 檔案所在的目錄路徑

shop_profile_create_table_sql = os.path.join(combine_path,'foodpanda_shop_profile_create_table.sql')
shop_feature_create_table_sql = os.path.join(combine_path,'foodpanda_shop_feature_create_table.sql')
shop_url_create_table_sql = os.path.join(combine_path,'foodpanda_shop_url_create_table.sql')
shop_adr_create_table_sql = os.path.join(combine_path,'foodpanda_shop_adr_create_table.sql')
shop_feature_detail_create_table_sql = os.path.join(combine_path,'foodpanda_shop_feature_detail_create_table.sql')
shop_product_detail_create_table_sql = os.path.join(combine_path,'foodpanda_shop_product_detail_create_table.sql')
shop_time_create_table_sql = os.path.join(combine_path,'foodpanda_shop_time_create_table.sql')

table_creator = TableCreator()
table_creator.create_table(shop_profile_create_table_sql)
table_creator.create_table(shop_feature_create_table_sql)
table_creator.create_table(shop_url_create_table_sql)
table_creator.create_table(shop_adr_create_table_sql)
table_creator.create_table(shop_feature_detail_create_table_sql)
table_creator.create_table(shop_product_detail_create_table_sql)
table_creator.create_table(shop_time_create_table_sql)