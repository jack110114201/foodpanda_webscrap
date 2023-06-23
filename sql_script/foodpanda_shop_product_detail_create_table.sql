/************************************************************** 
*
*  PURPOSE    : 店家餐點資訊
*  TABLE NAME : pdata.shop_product_detail
*  AUTHOR     : 
*  DATE       : 
*  UPDATE BY  : 
*  UPDATE DATE: 
* 
**************************************************************/

drop table if exists pdata.shop_product_detail;

CREATE TABLE if not exists pdata.shop_product_detail (
  name varchar(50)
  ,product varchar(100)
  ,price int
  ,PRIMARY KEY (name,product)
);

comment on column pdata.shop_product_detail.name is '餐廳名稱';
comment on column pdata.shop_product_detail.product is '餐點項目';
comment on column pdata.shop_product_detail.price is '餐點價格';