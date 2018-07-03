
# Leo Spark Notes

## Note
* Case class used in spark should not be defined within a function (normally the main function) otherwise the program could rise "Malformed class name" or "class could not converted to bean" exception! [e.g](https://stackoverflow.com/questions/37959985/spark-udaf-java-lang-internalerror-malformed-class-name)
* In scala the priority of operator -> is higher than operator +, so that value expression of a map should be wrapped with parentheses: e.g. k->(v+1) is OK while k->v+1 reports compile errors.
* In Spark dataframe.map use `row.getAs[java.lang.Double]("abc")` instead of `row.getAs[Double]("abc")` when the column "abc" might have null values. java.lang.Double is the Java Double class that is nullable, while Double is default to be the scala Double class that is not nullable.

## Tutorial
* [Spark SQL, DataFrames and Datasets Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
* How-to: Translate from MapReduce to Apache Spark [part1](https://blog.cloudera.com/blog/2014/09/how-to-translate-from-mapreduce-to-apache-spark/)[part2](http://blog.cloudera.com/blog/2015/04/how-to-translate-from-mapreduce-to-apache-spark-part-2/)
* Scala [Mutable and Immutable Collections](https://www.scala-lang.org/docu/files/collections-api/collections_1.html)
* [Dependency Management with Spark](http://theckang.com/2016/dependency-management-with-spark/)
* [Understanding your Apache Spark Application Through Visualization](https://databricks.com/blog/2015/06/22/understanding-your-spark-application-through-visualization.html)|[Monitoring Spark Applications](https://www.cloudera.com/documentation/enterprise/5-9-x/topics/operation_spark_applications.html)
* [Improving Spark Performance With Partitioning](https://dev.sortable.com/spark-repartition/)

## Q&A
* [Spark iteration time increasing exponentially when using join](https://stackoverflow.com/questions/31659404/spark-iteration-time-increasing-exponentially-when-using-join)
* [How to define and use a User-Defined Aggregate Function in Spark SQL?](https://stackoverflow.com/questions/32100973/how-to-define-and-use-a-user-defined-aggregate-function-in-spark-sql?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa)
* [Multi-Column Key and Value – Reduce a Tuple in Spark](http://dmtolpeko.com/2015/02/12/multi-column-key-and-value-reduce-a-tuple-in-spark/)
* [Apply a custom Spark Aggregator on multiple columns (Spark 2.0)](https://stackoverflow.com/questions/33899977/how-to-define-a-custom-aggregation-function-to-sum-a-column-of-vectors?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa)
