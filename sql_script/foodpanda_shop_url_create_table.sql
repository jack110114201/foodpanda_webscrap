/************************************************************** 
*
*  PURPOSE    : 餐廳網址資訊
*  TABLE NAME : pdata.shop_url
*  AUTHOR     : 
*  DATE       : 
*  UPDATE BY  : 
*  UPDATE DATE: 
* 
**************************************************************/

drop table if exists pdata.shop_url;

CREATE TABLE if not exists pdata.shop_url (
  name varchar(50)
  ,url varchar(500)
  ,PRIMARY KEY (name)
);

comment on column pdata.shop_url.name is '餐廳名稱';
comment on column pdata.shop_url.url is '餐廳網址';