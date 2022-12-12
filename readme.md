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

### Query sintax

The sintax is simpler than the MySQL one. It's separator is a **blank space**.

To write correctly simply **put a blank space between all words and sybols** and then **put a ; in the end**. Any other syntax will cause problems. Press ENTER to run.

**Query example**

```terminal
select id birth_date first_name from employees where first_name = John and id > 50397 order by birth_date ;
```

### Join sintax

To include join ?attribute? in the application some traits have to be added in query sintax, firstly the query must place join before **where** and **order by** parameters, after that the parameters only applies to the outer table failing if you consider the inner one for the conditions.

**Query example**

```terminal
select departments.dept_name dept_manager.dept_no from departments join dept_manager on dept_manager.dept_no = departments.dept_no where emp_no > 111000 order by dept_name ;
```