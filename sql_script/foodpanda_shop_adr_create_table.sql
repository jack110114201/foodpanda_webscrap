/************************************************************** 
*
*  PURPOSE    : 店家地址資訊
*  TABLE NAME : pdata.shop_adr
*  AUTHOR     : 
*  DATE       : 
*  UPDATE BY  : 
*  UPDATE DATE: 
* 
**************************************************************/

drop table if exists pdata.shop_adr;

CREATE TABLE if not exists pdata.shop_adr (
  name varchar(50)
  ,country varchar(50)
  ,postalCode int
  ,address varchar(100)
  ,latitude varchar(100)
  ,longitude varchar(100)
  ,telephone varchar(100)
  ,PRIMARY KEY (name)
);

comment on column pdata.shop_adr.name is '餐廳名稱';
comment on column pdata.shop_adr.country is '餐廳所在國家';
comment on column pdata.shop_adr.postalCode is '餐廳郵遞區號';
comment on column pdata.shop_adr.address is '餐廳地址';
comment on column pdata.shop_adr.latitude is '餐廳所在緯度';
comment on column pdata.shop_adr.longitude is '餐廳所在經度';
comment on column pdata.shop_adr.telephone is '餐廳電話';