A common question our customer have is how to append to an existing RDD or DataFrame. Luckily doing so is easy with the union method.

```java
val firstDF = spark.range(3).toDF("myCol")
val newRow = Seq(20)
val appended = firstDF.union(newRow.toDF())
display(appended)
```

```python
firstDF = spark.range(3).toDF("myCol")
newRow = spark.createDataFrame([[20]])
appended = firstDF.union(newRow)
display(appended)
```
