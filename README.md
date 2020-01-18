MysqlSyn
 ===========================

##	功能

从源数据库复制结构和数据到新数据库，可通过配置选择复制单表最大条目或全表复制。

## 环境

`python3x` 建议使用`Python3.8`

安装方式

```
请自行百度，推荐安装pip
```

`pymysql` 模块

安装方式

```shell
pip install PyMySQL
```

##	配置说明

`config.json`必须与 `MysqlSyn.py`在同一目录下

```json
{
    //	源数据库配置
     "from":{
         "host" : "rm-bp11j7ex56770w4h40o.mysql.rds.aliyuncs.com",
         "user" : "rsync_test",
         "passwd" : "rsync_test@2020",
         "db" : "minigame_stat",
         "charset" : "utf8"
     },
    //	 新数据库配置
     "to":{
         "host" : "127.0.0.1",
         "user" : "root",
         "passwd" : "houyi123456",
         "db" : "minigame_stat",
         "charset" : "utf8"
     },
    //	默认最大条目  0为全量
     "default_max_lines" : 0,
	// 单页条目，不用修改
     "page_size" : 5000,
    //	自定义 包含在以下字典中的表迁移数据量按此配置
     "custom" : {
         //	即wx_user_action_record表最大迁移10000条
        "wx_user_action_record" : 10000,
        "wx_consumer_report" : 10000,
        "wx_scene_record_appid" : 10000,
        "wx_user_device_info" : 10000,
        "wx_user_info" : 10000,
        "wx_user_access" : 10000,
        "wx_app_event" : 10000,
        "wx_channel_record_appid" : 10000,
        "wx_report_data" : 10000,
        "wx_adv_real_click" : 10000,
        "wx_adv_click_record" : 10000,
        "wx_app_custom_event_record" : 10000,
        "wx_channel_record" : 10000,
        "wx_ip" : 10000,
        "region" : 10000,
        "wx_app_custom_event_stat_appid" : 10000,
        "wx_scene_link_stat_appid" : 10000,
        "wx_adv_click_stat" : 10000
     }
}

```

##	运行

```shell
$ python MysqlSyn.py
```

##	其他

* 程序并未设置liveing标识,发生错误将会在同级目录上生成文件`log.log`
* 需先创建新数据库，并确保新数据库为空，且编码规则与源数据库一致
