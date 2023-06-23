/************************************************************** 
*
*  PURPOSE    : 店家基本資訊
*  TABLE NAME : pdata.shop_profile
*  AUTHOR     : 
*  DATE       : 
*  UPDATE BY  : 
*  UPDATE DATE: 
* 
**************************************************************/

drop table if exists pdata.shop_profile;

CREATE TABLE if not exists pdata.shop_profile (
  name varchar(50)
  ,score float
  ,comment_cnt int
  ,style varchar(50)
  ,PRIMARY KEY (name)
);

comment on column pdata.shop_profile.name is '餐廳名稱';
comment on column pdata.shop_profile.score is '評論分數';
comment on column pdata.shop_profile.comment_cnt is '評論次數';
comment on column pdata.shop_profile.style is '餐廳風格/特徵';