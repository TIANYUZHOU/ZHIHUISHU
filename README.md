# ZHIHUISHU-智慧树

智慧树互动分自动获取。

## 介绍

目前仅支持回答问题，不支持提问。

### 运行环境

```python
python 3.7.6
requests==2.28.1
selenium==3.141.0
```

### 使用教程

#### 准备

##### 浏览器

本项目需要使用到`Chrome`浏览器，请提前安装。

##### 文本转写接口

本项目需要用到文本转写，所以需要到**讯飞开放平台**申请一个**文本转写**的接口（新用户免费试用`100w`字，`90`天）。

- 申请地址：[https://www.xfyun.cn/services/text_rewrite](https://www.xfyun.cn/services/text_rewrite)

- 申请成功后，按照教程创建应用即可获得`APPID`、`APISecret`、`APIKey`

##### 问答页面链接

登录智慧树，进入问答页面可获得链接如：`https://qah5.zhihuishu.com/qa.html#/web/home/xxxx?role=2&recruitId=xxxx`

##### 配置文件

配置文件模板位于`config/example/config.ini`，在使用前需要完成配置文件的配置。

#### 开始使用

##### 使用 `autoqa.exe`

- 如果使用`autoqa.exe`文件，你需要：
  
  - 在与 `autoqa.exe` 同级的目录中，创建`config/config.ini`根据模板，写好配置文件。

  - 在与 `autoqa.exe` 同级的目录中，创建`webdriver/`将与自己的浏览器版本对应的`chromedriver.exe`放入。

  - 双击运行。

##### 使用源代码脚本

- 如果使用源代码脚本，你需要：

  - 安装依赖 `pip install -r requirements.txt`

  - 在与 `autoqa.py` 同级的目录中，创建`config/config.ini`根据模板，写好配置文件。

  - 在与 `autoqa.py` 同级的目录中，创建`webdriver/`将与自己的浏览器版本对应的`chromedriver.exe`放入。

  - 执行脚本。

#### 关于`chromedriver`

- 这个程序用来调用浏览器内核完成模拟操作，在自动化测试中用得比较多。
- 下载地址：[https://registry.npmmirror.com/binary.html?path=chromedriver/](https://registry.npmmirror.com/binary.html?path=chromedriver/)
- 如果不知道怎么安装，请自行`Bing or Google`

### 注意

- 本程序仅供学习交流使用，切勿用于真实课程学习中。
