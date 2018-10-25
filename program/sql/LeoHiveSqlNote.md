### Note
* When there is null value in a column it needs to be treated alone: null!='abc' does not return true.
* Only the 'abc' row is inserted as the second row is with different partition value:
```sql
insert overwrite table tab1 partition(p_20181001) select * from (
  select 20181001 as ds, 'abc' as name  from one_row_tab union all
  select 20181002 as ds, 'def' as name from one_row_tab
) a;
```

### Tutorial
* [LanguageManual UDF](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+UDF)

