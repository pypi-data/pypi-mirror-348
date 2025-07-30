from collections.abc import Sequence
import json
import pyodbc
import sys
import subprocess
import os

from utils import paths


def connect(config):

    SERVER = config['SERVER']
    DATABASE = config['DATABASE']
    USERNAME = config['USERNAME']
    PASSWORD = config['PASSWORD']
    DRIVER = config['DRIVER']

    connectionString = f'DRIVER={{{DRIVER}}};SERVER={
        SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

    conn = pyodbc.connect(connectionString)

    return conn


def print_sql_output(cursor: pyodbc.Cursor, isjson: bool):
    try:
        results = []
        if cursor.description:
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                l = []
                for val in list(row):
                    val_type = str(type(val))
                    match val_type:
                        case "<class 'datetime.datetime'>":
                            iso_datetime = (
                                val.isoformat('T', 'milliseconds') + 'Z'
                            )
                            l.append(iso_datetime)
                        case _:
                            l.append(val)
                r = dict(zip(columns, l))
                results.append(r)
        if isjson:
            print(json.dumps(results))
        else:
            print(results)
    except Exception as error:
        print('an error occurred', error)


def create_query(cursor: pyodbc.Cursor):
    cwd = os.getcwd()
    query_dir = '/tmp/syqlops'
    file_path = f'{query_dir}/QUERY_EDIT.sql'

    proc_name = 'QUERY'
    os.makedirs(query_dir, exist_ok=True)
    proc_def = f"""\
CREATE PROC #{proc_name}
    @jsonIn NVARCHAR(MAX),
    @jsonOut NVARCHAR(MAX) OUTPUT
AS
BEGIN
SET NOCOUNT ON;
-- READ JSON INPUT:
-- ----------------------------------------------------------------------
-- DECLARE @arg1 int = JSON_VALUE(@jsonIn, 'strict $.arg1')
-- DECLARE @arg2 int = isnull(JSON_VALUE(@jsonIn, '$.arg2'), 1)
--
SELECT @jsonOut = (
-- YOUR CODE HERE...
'[]'
)
END
"""
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write(proc_def)
    subprocess.run(['nvim', file_path])


def run_query(cursor: pyodbc.Cursor, json_input):
    cwd = os.getcwd()
    query_dir = f'/tmp/syqlops'
    file_path = f'{query_dir}/QUERY_EDIT.sql'

    with open(file_path, 'r') as file:
        temp_proc_def = file.read()
        cursor.execute(temp_proc_def)

    proc_name = 'QUERY'

    sql = f"""\
    SET NOCOUNT ON;
    DECLARE @out nvarchar(max);
    EXEC #{proc_name} @jsonIn = ?, @jsonOut = @out OUTPUT;
    SELECT JSON_QUERY(@out) AS the_output
    """
    params = (json.dumps(json_input),)
    cursor.execute(sql, params)
    printFirstField(cursor, None)


def save_query(save_path: str):
    cwd = os.getcwd()
    dir_path = paths.parent_dirs(save_path)
    proc_name = paths.last_segment(save_path)

    save_path = f'{cwd}/{save_path}.sql'
    if len(dir_path):
        os.makedirs(f'{cwd}/{dir_path}', exist_ok=True)

    query_dir = f'/tmp/syqlops'
    file_path = f'{query_dir}/QUERY_EDIT.sql'

    create_proc = f'CREATE PROC #{paths.file_name(proc_name)}'

    with open(file_path, 'r') as file:
        proc_def = file.read()
        lines = proc_def.split('\n')
        if len(lines) > 1:
            proc_def = create_proc + '\n'
            proc_def += '\n'.join(lines[1::])

    with open(save_path, 'w') as file:
        file.write(proc_def)
    subprocess.run(['nvim', save_path])


def store_proc(cursor: pyodbc.Cursor, proc_path: str, schema: str):
    cwd = os.getcwd()
    file_path = f"{cwd}/{paths.path_without_ext(proc_path) + '.sql'}"
    proc_name = paths.file_name(file_path)

    create_proc = f'CREATE PROC [{schema}].[{proc_name}]'

    with open(file_path, 'r') as file:
        proc_def = file.read()
        lines = proc_def.split('\n')
        if len(lines) > 1:
            proc_def = create_proc + '\n'
            proc_def += '\n'.join(lines[1::])
        print(proc_def)
        # cursor.execute(proc_def)


def build_call_str(procname: str, param_count: int):
    final = f'CALL {procname}'
    params = ''
    if param_count > 0:
        params = '('

    for _ in range(0, param_count - 1):
        params += '?,'

    if param_count > 0:
        final += ' ' + params + '?)'

    return '{' + final + '}'


def exec_jio_proc(
    cursor: pyodbc.Cursor,
    schema: str,
    procname: str,
    forward_input: bool,
    json_input,
):
    sql = f"""\
    SET NOCOUNT ON;
    DECLARE @out nvarchar(max);
    EXEC [{schema}].[{procname}] @jsonIn = ?, @jsonOut = @out OUTPUT;
    SELECT JSON_QUERY(@out) AS the_output
    """
    params = (json.dumps(json_input),)
    cursor.execute(sql, params)
    if forward_input:
        printFirstField(cursor, json_input)
    else:
        printFirstField(cursor, None)


def exec_temp_jio_proc(
    cursor: pyodbc.Cursor, path: str, workdir: str, forward_input: bool, json_input
):
    files = paths.paths_with_filename(path, workdir)
    if len(files) < 1:
        print(
            f'Could not find "{
                path}.sql" inside the current directory. Are you sure you are in the right directory?',
            file=sys.stderr,
        )
        print(f'- proc_name: {path}', file=sys.stderr)
        print(f'- current working directory: {os.getcwd()}', file=sys.stderr)
        print(f'- workdir: {workdir}', file=sys.stderr)

        # Print a plain json object to stdout
        print('{}')
        return

    file_path = f"{paths.path_without_ext(files[0]) + '.sql'}"
    proc_name = paths.file_name(file_path)

    with open(file_path, 'r') as file:
        temp_proc_def = file.read()
        cursor.execute(temp_proc_def)

    # Execute temp procedure
    sql = f"""\
    SET NOCOUNT ON;
    DECLARE @out nvarchar(max);
    EXEC #{proc_name} @jsonIn = ?, @jsonOut = @out OUTPUT;
    SELECT JSON_QUERY(@out) AS the_output
    """
    params = (json.dumps(json_input),)
    cursor.execute(sql, params)
    if forward_input:
        printFirstField(cursor, json_input)
    else:
        printFirstField(cursor, None)


def printFirstField(cursor: pyodbc.Cursor, input_data):
    first_field = extract_first_field(cursor, input_data)
    print(first_field)


def extract_first_field(cursor: pyodbc.Cursor, include_data):
    row = cursor.fetchone()
    first_field = None
    if row != None:
        first_field, *_ = list(row)

    if first_field == None:
        first_field = '{}'

    if include_data != None:
        first_field = json.loads(first_field)
        first_field.update(include_data)
        return json.dumps(first_field)

    return first_field


def get_proc_def(cursor: pyodbc.Cursor, schema: str, proc_name: str) -> str:
    sql = f"""\
    SELECT OBJECT_DEFINITION (OBJECT_ID(N'[{schema}].[{proc_name}]')) as 'procDef';
    """
    cursor.execute(sql)
    proc_def = extract_first_field(cursor, None)
    if isinstance(proc_def, str) == False:
        return ''

    return proc_def


def dl_proc_def(cursor: pyodbc.Cursor, schema: str, proc_name: str):
    proc_def = get_proc_def(cursor, schema, proc_name)
    print(proc_def, file=sys.stdout)

    file_path = f'/tmp/syqlops/dl-proc/{proc_name}.sql'

    os.makedirs('/tmp/syqlops/dl-proc/{schema}', exist_ok=True)
    if proc_def:
        with open(file_path, 'w') as file:
            file.write(proc_def)

    proc_paths = paths.paths_with_filename(proc_name)
    if len(proc_paths) > 0:
        subprocess.run(['nvim', '-d', file_path, proc_paths[0]])


def scaffold_proc(editor: str, proc_name_and_path: str):
    cwd = os.getcwd()
    dir_path = paths.parent_dirs(proc_name_and_path)
    proc_name = paths.last_segment(proc_name_and_path)

    file_path = f'{cwd}/{proc_name_and_path}.sql'
    print(dir_path)
    print(file_path)
    if len(dir_path):
        os.makedirs(f'{cwd}/{dir_path}', exist_ok=True)

    with open(file_path, 'w') as file:
        proc_def = f"""\
CREATE PROC #{proc_name}
    @jsonIn NVARCHAR(MAX),
    @jsonOut NVARCHAR(MAX) OUTPUT
AS
BEGIN
SET NOCOUNT ON;
-- READ JSON INPUT:
-- ----------------------------------------------------------------------
-- DECLARE @arg1 int = JSON_VALUE(@jsonIn, 'strict $.arg1')
-- DECLARE @arg2 int = isnull(JSON_VALUE(@jsonIn, '$.arg2'), 1)
--
-- YOUR CODE HERE...
SELECT @jsonOut = '[]'
END
"""
        file.write(proc_def)
    subprocess.run([editor, file_path])


def list_schemas(cursor: pyodbc.Cursor):
    sql = f"""\
    SELECT
        sch.name, (select count(*) from sys.procedures where OBJECT_SCHEMA_NAME(OBJECT_ID) = sch.name)
    FROM sys.schemas sch
    ORDER BY name asc
    """
    cursor.execute(sql)
    print_sql_output(cursor, isjson=True)


def list_procs(cursor: pyodbc.Cursor, schema: str):
    sql = f"""\
      SELECT
        name as 'procName'
        --OBJECT_DEFINITION(OBJECT_ID) as 'sourceCode'
      FROM sys.procedures
      WHERE OBJECT_SCHEMA_NAME(OBJECT_ID) = '{schema}'
      ORDER BY name asc
    """
    cursor.execute(sql)
    print_sql_output(cursor, isjson=True)
