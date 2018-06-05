## kcwiki_bot 使用说明

kcwiki_bot 是指一系列用于和zh.kcwiki.org交互的小工具（客户端），当前包括：
* voice_bot：用于舰娘语音的上传和生成语音相关wikicode

### voice_bot 使用说明
#### 配置文件 config.json
* login_config:
	* user_name: zh.kcwiki.moe 用户名
	* password: zh.kcwiki.moe 密码
* proxy: http代理（只支持http代理！）设置，不使用代理请删除该字段或用空字符串代替
* voice_config:
	* type: ''seasonal'' 表示季节性语音，''new_ship''表示追加新舰娘语音
    * new_ship_id: 在 type 为''seasonal''时，可以在此处添加id，用以区分季节性语音和新追加舰娘语音
	* seasonal_suffix: 季节性语音后缀
	* update_date: 更新日期，注意日期都用两位数字表示，比如''01''
* download_config:
    * include_id: 仅查看该列表中舰娘的语音是否有更新并下载
    * exclude_id: 查看舰娘语音是否有更新时，排除该列表中的舰娘
    * voice_id_range: 查找更新语音的范围，例如是否查看报时等
    * is_include_enemy": 是否查看深海舰队语音的更新

#### 使用方法

查看更新语音下载
``` shell
python voice_bot.py d
or python voice_bot.py download
```

修复更新语音并下载
``` shell
python voice_bot.py f
or python voice_bot.py fix
```

上传语音到zh.kcwiki.moe（必须已下载语音文件）
``` shell
python voice_bot.py u
or python voice_bot.py upload
```

生成wikicode
``` shell
python voice_bot.py g
or python voice_bot.py genwiki
```

查看使用帮助
```shell
python voice_bot.py h
or python voice_bot.py help
```

如果文件夹下有"subtitlesJp.json"和"subtitlesZh.json"，会自动将字幕合并到生成的wikicode中。