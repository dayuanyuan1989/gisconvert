import json
import math
import os

# 功能说明
# 百度坐标系，转化成wgs84

# ref: https://blog.csdn.net/VIP_CR/article/details/126967565?csdn_share_tail=%7B%22type%22%3A%22blog%22%2C%22rType%22%3A%22article%22%2C%22rId%22%3A%22126967565%22%2C%22source%22%3A%22unlogin%22%7D
# 这哥们的是c#写，我简单改造成python

x_pi = math.pi * 3000.0 / 180.0
a = 6378245.0  # // 长半轴
ee = 0.00669342162296594323  # // 扁率


class GPSPoint:
    def __init__(self, lng=0, lat=0):
        self.lng = lng
        self.lat = lat


# 百度转84
def bd09towgs84(bd: GPSPoint) -> GPSPoint:
    hx = bd09togcj02(bd)
    wgs84 = gcj02towgs84(hx)
    return wgs84


# 百度转火星
def bd09togcj02(Bd: GPSPoint) -> GPSPoint:
    x = Bd.lng - 0.0065
    y = Bd.lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - .000003 * math.cos(x * x_pi)
    hx = GPSPoint()
    hx.lng = z * math.cos(theta)
    hx.lat = z * math.sin(theta)
    return hx


# //火星转84
def gcj02towgs84(hx: GPSPoint) -> GPSPoint:
    dlat = transformlat(hx.lng - 105.0, hx.lat - 35.0)
    dlng = transformlng(hx.lng - 105.0, hx.lat - 35.0)
    radlat = hx.lat / 180.0 * math.pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * math.pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * math.pi)
    wgs84 = GPSPoint()
    mglat = hx.lat + dlat
    mglng = hx.lng + dlng
    wgs84.lat = hx.lat * 2 - mglat
    wgs84.lng = hx.lng * 2 - mglng
    return wgs84


# /*辅助函数*/
# //转换lat
def transformlat(lng: float, lat: float) -> float:
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * \
        lat + 0.1 * lng * lat + 0.2 * math.sqrt(abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * math.pi) + 20.0 *
            math.sin(2.0 * lng * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * math.pi) + 40.0 *
            math.sin(lat / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * math.pi) + 320 *
            math.sin(lat * math.pi / 30.0)) * 2.0 / 3.0
    return ret


# /*辅助函数*/
# //转换lng
def transformlng(lng: float, lat: float) -> float:
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
        0.1 * lng * lat + 0.1 * math.sqrt(abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * math.pi) + 20.0 *
            math.sin(2.0 * lng * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * math.pi) + 40.0 *
            math.sin(lng / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * math.pi) + 300.0 *
            math.sin(lng / 30.0 * math.pi)) * 2.0 / 3.0
    return ret


def make_data(input: str, output: str):
    wgs84List = []
    with open(input) as f:
        lines = f.readlines()
        baiduList = []

        for l in lines:
            ss = l.strip().split(",")
            if len(ss) != 2:
                continue
            lng = float(ss[0])
            lat = float(ss[1])
            baiduList.append((lng, lat))
            # wgs84
            wgs = bd09towgs84(GPSPoint(lng, lat))
            wgs84List.append((wgs.lng, wgs.lat))

    with open(output, mode="w+") as f:
        for item in wgs84List:
            obj = {"longitude": item[0], "latitude": item[1]}
            f.write("- " + json.dumps(obj)+"\n")

            # f.write(f"- latitude: {item[1]}\n")
            # f.write(f"  longitude: {item[0]}\n")

            # f.write(f"{{{item[0]},{item[1]}}},\n")


if __name__ == "__main__":

    # 遍历data目录下的所有.txt的文件
    for file in os.listdir("./data"):
        if file.endswith(".txt"):
            make_data("./data/" + file, "./output/" + file)

    print("Done")
