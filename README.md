# 概况

爬取安全客的安全知识版块和安全资讯版块的所有文章内容，进行分词预处理，并且存入mongodb中

# 网址分析

安全客：https://www.anquanke.com/

>安全知识：https://www.anquanke.com/knowledge  共345页  每页10篇  约3450篇

>安全资讯：https://www.anquanke.com/news     共279页  每页10篇   约2800篇

每页json：

>https://api.anquanke.com/data/v1/posts?size=10&page=2&category=knowledge

>https://api.anquanke.com/data/v1/posts?size=10&page=2&category=news

文章的url：https://www.anquanke.com/post/id/162589 （只需从源码中获取id号即可）

# 网页元素分析

安全知识的每页json：

https://api.anquanke.com/data/v1/posts?size=10&page=2&category=knowledge

>![帖子元素](https://github.com/leslie-lss/anquanke/blob/master/image.png)

对于每一篇文章，正文的定位为：

>Xpath：//div[@class='article-content']

# 数据存储结构

list表，存储每页json中的所有内容，包括了每篇文章的所有详细信息。

article表，每篇文章的具体内容：

>key | 意义
>-------- | --------
>_id | 文章id号，唯一，可确定url
>url | 文章的地址
>article | 文章正文内容

fenci表，对文本进行分词预处理的结果：

>key | 意义
>-------- | --------
>_id | 文章id号，唯一，可确定url
>url | 文章的地址
>article | 文章正文内容
>article_no_url | 过滤掉正文中的链接
>article_chi | 文章中的中文字符
>article_chi_final | 文章中的中文字符的分词结果
>article_eng | 文章中的英文字符
>article_eng_final | 文章中的英文字符的分词结果
