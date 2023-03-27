import matplotlib.pyplot as plt
import numpy as np

# 读取data目录里path11.txt里的数据
points = np.loadtxt("data/path21.txt", delimiter=",")

# 将经度转换为x轴坐标，将纬度转换为y轴坐标
x = [point[0] for point in points]
y = [point[1] for point in points]

for i in range(len(points)):
    plt.text(points[i][0]+0.0002,points[i][1],f"{i}", fontsize=10, color='g')

# 绘制线条
plt.plot(x, y, color='black', linewidth=2, linestyle='--', marker='o')


# 绘制起始坐标点
plt.scatter(points[0][0], points[0][1], s=100, c='r', marker='x')

# 绘制起始坐标点
plt.scatter(points[1][0], points[1][1], s=100, c='pink', marker='x')

# # 绘制坐标点
# plt.scatter(121.9240479220495, 30.891977296792966, s=60, c='g', marker='o')

# # 绘制计算后的点
# plt.scatter(121.9259254944243, 30.8927478501053, s=60, c='yellow', marker='o')

# 设置图像标题和坐标轴标签
plt.title('Line Plot of Points')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# 显示图像
plt.show()