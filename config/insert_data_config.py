shop_profile_data_config = {
    'table_name' : 'pdata.shop_profile'
    ,'column_names' : ['name', 'score', 'comment_cnt', 'style']
    ,'conflict_columns' : ['name']
    ,'update_columns' : ['score', 'comment_cnt', 'style']
}

shop_feature_data_config = {
    'table_name' : 'pdata.shop_feature'
    ,'column_names' : ['name', 'feature']
    ,'conflict_columns' : ['name', 'feature']
    ,'update_columns' : None
}

shop_url_data_config = {
    'table_name' : 'pdata.shop_url'
    ,'column_names' : ['name', 'url']
    ,'conflict_columns' : ['name']
    ,'update_columns' : ['url']
}

shop_adr_data_config = {
    'table_name' : 'pdata.shop_adr'
    ,'column_names' : ['name', 'country', 'postalCode', 'address', 'latitude', 'longitude', 'telephone']
    ,'conflict_columns' : ['name']
    ,'update_columns' : ['country', 'postalCode', 'address', 'latitude', 'longitude', 'telephone']
}

shop_time_data_config = {
    'table_name' : 'pdata.shop_time'
    ,'column_names' : ['name', 'dayOfWeek', 'opens_time', 'closes_time']
    ,'conflict_columns' : ['name', 'dayOfWeek']
    ,'update_columns' : ['opens_time', 'closes_time']
}

shop_feature_detail_data_config = {
    'table_name' : 'pdata.shop_feature_detail'
    ,'column_names' : ['name', 'feature']
    ,'conflict_columns' : ['name', 'feature']
    ,'update_columns' : None
}

shop_product_detail_data_config = {
    'table_name' : 'pdata.shop_product_detail'
    ,'column_names' : ['name', 'product', 'price']
    ,'conflict_columns' : ['name', 'product']
    ,'update_columns' : ['price']
}