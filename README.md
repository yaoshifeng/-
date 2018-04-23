# 爬取网页 python3.6
爬取11个类型的小说各40篇（可以自己修改）

4月14号——spider_2.0.py
学习了HTML的对应的标签
初学爬虫的第一个demo，只是单纯通过正则表达式查找并取得对应的字符串，技术含量有点低....

4月16号——spider_2.1.py
在上一次知道爬取的流程后对2.0进行改良，通过结合Beautifulsoup库查找对应的内容，查找更准确

4月19号——把之前看的CDSN博客里的mzitu反扒取功能添加
(感谢我室友刘哥，和伟哥的技术帮助，谢新哥伟哥，哈哈)
getip.py——http://www.xicidaili.com/wt/ 代理服务器可用列表，每次选取其中几页开始选定可用的
国内代理的匿名服务器进行对应网页访问

download.py——利用getip得到的代理服务器ip，重对request函数进行后改良，添加代理功能

update 4月20号 —— upload spider 3.0 ——即日起更新用英语，显得高大尚，hhhhhhh

1.select lots of crawling code encapsulated as a class in paqu.py file to make main code cleaner

2.add paqu.py encapsulated code as a Spider() class

3.add Novel_Type ENUM and Novel_Info ENUM to make code more understanding

4.add multithreading to crawl the www.quanshuwang.com

5.add save_pic function

     can save all novel pictures in the path
  
     every novel has its own folder to save pictures(now just save pictures...)
  
6.get information return a list, is easy to add the connect mysql function

※A Dangerious Bug——crawd 1,2,3,4,6 page, novels with repetition ,maybe novel_url has some issues.

4月22号——预计将提取的数据存储到mysql中 并设计mysql库

April 23rd

I'm sorry to late for update the file

Because there are some issues in my own computer.

I ghost my computer, all my work environment applications are lost... Let me cry in 5 seconds.

Now I finish my own first beyond one thousand lines project.

Let me say what I update:

First:Add error handling

     In spider3.0, all the function has no error handling. 
     
     And make me carry because of adding the mysql function. 
     
     Always said something wrong with the project and can't write in mysql. 
     
     So I add lots of error handling, and the paqu.py beyond 400 lines, Brilliant! 
     
     Finally I find it's a proxy server problem! What the ***

Second:A big problem

     In spider3.0, I just show the novel the latest novel content, 
     
     All right it's my question,
     
     So I crawl the whole novel.

Third: My pride——Saving all novel information in Mysql

if you want to run and see:

1.Mysql, Please setup The authority application, I setup a piracy and always said 99 errors 
when I use multithreading to crawl.

2.Configure the mysql information:  

       host 	= "localhost"

       port 	= 3306

       user 	= "root"

       passwd 	= ""

       db   	= "novel_information_list"

       charset 	= "utf8"(dot write "utf-8", this error I find 3 hours...)

※Well, you can configure anything you like, don't forget to revise the paqu.py code

3.Create table

     |——eleven chapter_(type_num)_list tables.for Example: chapter_1_list

     `——one novel_information_list table.

novel_informtaion_list:

    novel_id  (type = char, len=8, Not NULL, PRIMARY, Default 10000) 

    type      (type = shortint, len=2)

    novel_name(type = varchar, len 64)

    serialize (type = tinyint, len 1)

    author    (type = varchar, len=60)

    summary   (type = varchar, len=255)(I forget to code it, Forgive it)

chapter_(type_num)_list:

     novel_id          (type = int, len = 11(whatever it's ok to enough), NOT ULL, PRIMARY)

     novel_name        (type = varchar, len = 50)

     novel_chapter_name(type = varchar, len = 50)

     chapter_content   (type = longtext)
            
Finally:  

     OK, I admit it's not a good project:
     
     Two questions confuse me a lot. 
     
     First, I don't know the reason Why page 1,2,3,4 always crawl repeat... And 6,7,8,9,10,11 is good.
     
     Second, I don't know the reason Why crawl about a half it will stop to write in Mysql, 
     
     It's no way insert too many in list. And I just create one threading.lock, 
     
     it's impossible to rob resources. 
     
     If I can handle it, I'll resive it soon, or PLEASE HELP ME. Thank you!
            
        
        
       
