### Note
* When there is null value in a column it needs to be treated alone: null!='abc' does not return true.
* Only the 'abc' row is inserted as the second row is with different partition value:
```sql
insert overwrite table tab1 partition(p_20181001) select * from (
  select 20181001 as ds, 'abc' as name  from one_row_tab union all
  select 20181002 as ds, 'def' as name from one_row_tab
) a;
```
* A versatile approach to deal with skew join by using _with_ and _mapjoin_. Suppose we have two tables - _tab_x_, _tab_y_ and for some _yid_ in _tab_x_ there are millions of records and normal join would lead to the skew join problem. We can then use this approach:
```sql
tab_x: xid, yid
tab_y: yid, name

insert overwrite into table tab_z partition($ds$) 
with yid_nr as (
  select yid, count(1) as nr from tab_x group by yid
), tab_y_nr as (
  select a.*, b.nr from tab_y a join yid_nr on a.yid=yid_nr.yid
)
select /*+mapjoin(c)*/
   a.xid, a.yid, coalesce(b.name, c.name) as name
from tab_x a 
left outer join (
  select * from tab_y_nr where nr<=100000
) b on a.yid=b.yid
left outer join (
  select * from tab_y_nr where nr>100000
) c on a.yid=c.yid;
 ```
 * Window function _count_ should be used without the order by clause otherwise it would result in different count result for a same partition. e.g. Correct: count(1) over (partition city), Wrong: count(1) over (partition city order by 1).

### Tutorial
* [LanguageManual UDF](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+UDF)

