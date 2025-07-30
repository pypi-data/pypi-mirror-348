# ipydfconfig

ipydfconfig is an IPython extension to simplify per-cell dataframe display configuration.

## Quickstart

1. `pip install ipydfconfig`
2. In a notebook or IPython session,
   ```python
   %load_ext ipydfconfig
   ```
3. For any cell in which you wish to temporarily configure a dataframe output, for polars,
   ```python
   %%plconfig nr=20
   df
   ```
   or for pandas,
   ```python
   %%pdconfig nc=50 strlen=200
   df
   ```

## Motivation

In IPython and more commonly, Jupyter notebooks using the IPython kernel, 
if you wish to display a specific dataframe with more rows or columns than the default, you generally have two imperfect solutions:

### Imperfect Solution 1: Modify the global configuration

```python
pl.Config.set_tbl_rows(20)
df
```

```python
pd.set_option('display.max_rows', 20)
df
```

The downside to this solution is that these options persist for the entire session unless you execute
code to reset them, meaning they are not constrained to a particular cell.

### Imperfect Solution 2: Use a context manager with display

```python
with pl.Config(tbl_rows=20):
    display(df)
```

```python
with pd.option_context('display.max_rows', 20):
    display(df)
```

While this solution ensures the changes are only for the specified block of code, the edits signficantly alter
the structure of the code, and IPython no longer considers `df` as the "output" of the cell.

### Configuration Option Confusion

Finally, if you use multiple dataframe modules, the differences between configuration options
can require consulting documentation and/or lengthy parameter names (e.g. `display.max_rows` in pandas vs. `tbl_rows` in polars).

## ipydfconfig

ipydfconfig simplifies this process by introducing cell magics that configure a cell according to the specified
options that only apply to that single cell. In addition, users can use universal shortcuts that will be translated
to whichever dataframe library is being used. Finally, the `%%dfconfig` cell magic will apply to outputs from any
configured dataframe module; if an option is specific to one module, it will be ignored for the others.

There are three cell magics:

* `%%plconfig`: polars
* `%%pdconfig`: pandas
* `%%dfconfig`: universal

In addition to all specified option names from each library 
([polars docs](https://docs.pola.rs/api/python/stable/reference/config.html), 
[pandas docs](https://pandas.pydata.org/docs/reference/api/pandas.set_option.html)),
ipydfconfig provides the following shortcuts that are translated to the equivalent option names:

* `nr`: number of rows to display
* `rows`: number of rows to display
* `nc`: number of columns to display
* `cols`: number of columns to display
* `strlen`: maximum number of characters to show per string
* `listlen`: maximum number of items to show in a list/sequence

### Examples

##### polars
 ```python
 %%plconfig nr=20
 df
 ```

##### pandas
 ```python
 %%pdconfig nc=50 strlen=200
 df
 ```

##### universal
```%%dfconfig nr=30 nc=50
df1 = pd.read_parquet('data.parquet')
display(df1)
df2 = pl.read_parquet('data.parquet')
display(df2)
```
