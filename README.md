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
    //	源数据库相关配置
     "from":{
         "host" : "127.0.0.1",
         "user" : "root",
         "passwd" : "123456",
         "db" : "minigame_stat",
         "charset" : "utf8"
     },
    //	新数据库配置
     "to":{
         "host" : "192.168.2.225",
         "user" : "root",
         "passwd" : "houyi123456",
         "db" : "minigame_stat",
         "charset" : "utf8"
     },
    // 每个表最大复制行数 若为0则为全量复制
     "max_lines" : "200"
}

```

##	运行

```shell
$ python MysqlSyn.py
```

##	其他

* 程序并未设置liveing标识,发生错误将会在同级目录上生成文件`log.log`
* 需先创建新数据库，并确保新数据库为空，且编码规则与源数据库一致



