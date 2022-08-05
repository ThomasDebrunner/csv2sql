# CSV2SQL

Simple python tool to create SQL `INSERT` statements from CSV files.

## Usage  

`python csv2sql.py <csv_file> -t <table_name>`

### Arguments

* `csv_file`: The CSV file to be read  
* `-t` or `--table`: The name of the destination SQL table.  
* `-d` or `--delimiter`: (Optional) The delimiter used in the CSV, `,` by default.
* `-o` or `--output`: (Optional) The output of the SQL statement, `stdout` by default.  
* `-e` or `--encoding`: (Optional) The Encoding when reading and writing file, `utf-8` by default.  

### CSV file format  

The first line of the CSV file is the header of the table. You can optionally to add a symbol ` : ` and a type name after each field name as a type signature to mark the data type. The available type signature is:  

* `TextNotNull` :  The data will be surrounded by `'` to represent the string type. The empty item will be replaced by `''`.  
* `Text` : Similar with `TextNotNull` but the empty item will be replaced by `NULL`.  
* Other type signature such as `Number`, `Bool`, etc : The data will be directly what it is except emtpy item will be replaced by `NULL`.

If there's no type signature for one field, it would be `TextNotNull`. See the format of the file `example.csv` and the result below.  

![sql_result](./result.jpg)  
