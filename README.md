# pycode

记录 Python 学习道路上自己编写的一些代码，小工具。

- bing_url.py : 爬取 bing 搜索结果中的链接
- brute_form.py : 暴力破解 wordpress 登录，使用 urllib 库，根据登录页输入框表单的字段名来破解，所以只需略加修改登录页及请求链接，可适用于其他的一般网站
- brute_form_request.py : 与上述功能相同，使用 requests 库，较为简单
- dir_bruster.py : 根据字典穷举网站路径，支持多线程
- download_img.py : 下载一篇百度贴吧的帖子中所有的图片，比如壁纸帖之类的
- download_http2.py: 下载 https://www.mzitu.com/zipai 中的图片，该站使用 HTTP2，这个脚本通过 hyper 使 requests 实现支持 HTTP2
- http_header_test.py : 获取返回的 HTTP 头，支持批量链接获取，便于比较
- socks_spider.py : 爬取[https://www.socks-proxy.net/](https://www.socks-proxy.net/)的 socks 代理地址
- ishadowx_spider.py : 爬取[https://global.ishadowx.net/](https://global.ishadowx.net/)的 socks 代理地址，以 shadowsocks 配置文件的格式输出
- cors_check.py: 检测 cors 漏洞
