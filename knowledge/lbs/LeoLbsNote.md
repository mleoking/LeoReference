
# 地理编码
## 经纬度后面的小数的位数对于精度影响有多少？

在纬度相等的情况下：

经度每隔0.00001度，距离相差约1米；
经度每隔0.0001度，距离相差约10米；
经度每隔0.001度，距离相差约100米；
经度每隔0.01度，距离相差约1000米；
经度每隔0.1度，距离相差约10000米。

在经度相等的情况下：

纬度每隔0.00001度，距离相差约1.1米；
纬度每隔0.0001度，距离相差约11米；
纬度每隔0.001度，距离相差约111米；
纬度每隔0.01度，距离相差约1113米；
纬度每隔0.1度，距离相差约11132米。

但是上诉的答案是否是正确的呢？我们先来了解下地球的一些基本信息：

地球的赤道半径 = 6378.1 公里
地球的极半径 = 6356.8 公里
Latitude的范围是：-90 到 +90
Longitude的范围：-180 到 +180
地球参考球体的周长：40075016.68米

## 如何求出地球两点距离呢？

```java
private const double EARTH_RADIUS = 6378.137;
private static double rad(double d)
{
   return d * Math.PI / 180.0;
}
public static double GetDistance(double lat1, double lng1, double lat2, double lng2)
{
   double radLat1 = rad(lat1);
   double radLat2 = rad(lat2);
   double a = radLat1 - radLat2;
   double b = rad(lng1) - rad(lng2);
   double s = 2 * Math.Asin(Math.Sqrt(Math.Pow(Math.Sin(a/2),2) +
    Math.Cos(radLat1)*Math.Cos(radLat2)*Math.Pow(Math.Sin(b/2),2)));
   s = s * EARTH_RADIUS;
   s = Math.Round(s * 10000) / 10000;
   return s;
}
