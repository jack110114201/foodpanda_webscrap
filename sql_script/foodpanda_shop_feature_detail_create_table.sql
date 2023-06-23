/************************************************************** 
*
*  PURPOSE    : 餐廳多項風格/特徵
*  TABLE NAME : pdata.shop_feature_detail
*  AUTHOR     : 
*  DATE       : 
*  UPDATE BY  : 
*  UPDATE DATE: 
* 
**************************************************************/

drop table if exists pdata.shop_feature_detail;

CREATE TABLE if not exists pdata.shop_feature_detail (
  name varchar(50)
  ,feature varchar(50)
  ,PRIMARY KEY (name,feature)
);

comment on column pdata.shop_feature_detail.name is '餐廳名稱';
comment on column pdata.shop_feature_detail.feature is '餐廳風格/特徵';