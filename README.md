# spider-practice

 
<h2>2018.9.28 11：48</h2>
今日抓出了不能正常解析的元凶，requests库请求之返回了部分js的内容，导致解析失败，换用urllib.
同时，数据库部分也有问题，由于主键id不能自动更新导致插入数据库失败。
明日优化细节。