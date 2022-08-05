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


### License 

3-clause BSD

```
Copyright 2015-2022 Thomas Debrunner

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
