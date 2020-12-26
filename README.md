# 简述

本项目包含了一系列财务数据的处理工具。

* cmbcred.py: 招行信用卡账单
* cmbdebit.py: 招行银行卡账单
* spdbcred.py: 浦发信用卡账单
* wechat_enhance.py: 微信花销增强工具
* cancel_enhance.py: 消除账内退款记录
* jd: 京东消费分析工具
  * jd-order.json: web scraper脚本，抓订单。
  * jd-type.json: web scraper脚本，抓订单对应的分类。
  * jd.py: 结合上两项数据，出整合报表。后续可以直接计算分类花销。

# 格式

项目中的工具，遵循一个特定格式。月份，日期，卡号（最后四位），金额，描述。所有工具的输入和输出一致，因此可以协同产生一份最终数据，简单加上表头后用pandas进行分析。
