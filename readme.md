# Graphical python toll for database management

This tool for DB management simulates a MySQL-like structure, with tables beeing loaded into RAM for queries to be processed.

## Setup

For graphical interface library installation run:

Package Manager:
```terminal
sudo apt install python3-tk
```

Pip command:
```terminal
pip install tk
```

## How to use it

Simply run:

```terminal
python3 main.py
```

on your terminal, and a load screen will pop up. Choose the desired folder with _.csv_ files in it, and then click **Load**.

All .csv files will be loaded into memory as tables, and you can start to write your queries.

### Query syntax

The syntax is simpler than the MySQL one. It's separator is a **blank space**.

To write correctly simply **put a blank space between all words and sybols** and then **put a ; in the end**. Any other syntax will cause problems. Press ENTER to run.

**Query example**

```terminal
select id birth_date first_name from employees where first_name = John and id > 50397 order by birth_date ;
```

### Join syntax

To include _join_ in the application, some traits have to be considered in query syntax. Firstly, the query must be ordered with _join_ before **where** and **order by** parameters. After that, they only apply to the inner table, failing if you consider the outer one for the conditions. The query will accept the terms **on** or **using**  for _join_.

It also accepts an implicit form of _join_, where the join parameter is not written, but instead, two tables are declared in **from** parameter and their attributes are compared in the **where** parameter.

**Explicit join example**

```terminal
select departments.dept_name dept_manager.dept_no from departments join dept_manager on departments.dept_no = dept_manager.dept_no where emp_no > 111000 order by dept_no ;
```

**Implicit join example**

```terminal
select departments.dept_name dept_manager.dept_no from departments dept_manager where departments.dept_no = dept_manager.dept_no and emp_no > 111000 order by dept_no ;
```