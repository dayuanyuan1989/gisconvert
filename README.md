# 百度坐标系转WGS84坐标系

实现使用python，根据 [这个哥们的代码改造而来](https://blog.csdn.net/VIP_CR/article/details/126967565?csdn_share_tail=%7B%22type%22%3A%22blog%22%2C%22rType%22%3A%22article%22%2C%22rId%22%3A%22126967565%22%2C%22source%22%3A%22unlogin%22%7D)，这哥们使用的是C#，我用Python使用起来轻量化些

# 使用说明

1. 准备输入文件 data/{filename}.txt

```vim
经度值1,维度值1
经度值2,维度值2
...
```

2. 执行 python convert.py

3. 输出 output/{filename}.txt

# 使用更高精度的gcj02-wgs84的方法

[gcj02_To_Wgs84_exact](https://www.cnblogs.com/wanghuanl/p/15927619.html)
