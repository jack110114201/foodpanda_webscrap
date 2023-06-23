/************************************************************** 
*
*  PURPOSE    : 店家營業資訊
*  TABLE NAME : pdata.shop_time
*  AUTHOR     : 
*  DATE       : 
*  UPDATE BY  : 
*  UPDATE DATE: 
* 
**************************************************************/

drop table if exists pdata.shop_time;

CREATE TABLE if not exists pdata.shop_time (
  name varchar(50)
  ,dayOfWeek varchar(50)
  ,opens_time varchar(50)
  ,closes_time varchar(100)
  ,PRIMARY KEY (name,dayOfWeek)
);

comment on column pdata.shop_time.name is '餐廳名稱';
comment on column pdata.shop_time.dayOfWeek is '週期';
comment on column pdata.shop_time.opens_time is '餐廳開始營業時間';
comment on column pdata.shop_time.closes_time is '餐廳結束營業時間';