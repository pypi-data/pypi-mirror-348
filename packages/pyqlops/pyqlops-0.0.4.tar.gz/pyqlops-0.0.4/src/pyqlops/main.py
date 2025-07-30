import db
import argparse
import glob
import subprocess
import json
import sys

from utils.helpers import merge

from dotenv import dotenv_values

parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(dest='command', help='subcommand help')

parser.add_argument('--config', help='configuration file')

parser.add_argument(
    '-l', '--list', action='store_true', help='list all sql files'
)
parser.add_argument('--schema', type=str, help='target schema')

parser.add_argument(
    '--forward-input',
    action='store_true',
    help='forward the json input on by including it with the output data',
)

parser.add_argument(
    '-',
    '--stdin',
    action='store_true',
    help='read from stdin',
)

# download proc
parser_dl = subparsers.add_parser('dl', help='download stored procedure')
parser_dl.add_argument(
    'proc_name', type=str, help='name of procedure to download'
)

# adhoc query
parser_query = subparsers.add_parser('query', help='create a query')

# save query
parser_save_query = subparsers.add_parser('save', help='save the procedure')
parser_save_query.add_argument(
    'path',
    help='the path to save the procedure to',
)

# store proc
parser_store_proc = subparsers.add_parser(
    'store', help='store the procedure in the database'
)
parser_store_proc.add_argument(
    'path',
    help='the path to the procedure to be stored',
)

# call stored procedure
parser_call = subparsers.add_parser(
    'call',
    help='call a stored procedure in the database that is defined with a JSON input parameter and a JSON output parameter',
)
parser_call.add_argument(
    '-t',
    '--temp',
    action='store_true',
    help='run temporary procedure rather than a stored one',
)
parser_call.add_argument('proc_name', type=str, help='name of jio procedure')
parser_call.add_argument(
    'json_input',
    type=json.loads,
    nargs='?',
    help='json input parameter to call stored procedure',
)

# temporary procedure
parser_run = subparsers.add_parser('run', help='run temporary procedure')
parser_run.add_argument(
    'proc_name',
    type=str,
    help='name of temporary procedure',
    nargs='?',
)
parser_run.add_argument(
    'json_input',
    type=json.loads,
    help='json input to be passed to temporary procedure',
    nargs='?',
)

# scaffold procs
parser_scaffold = subparsers.add_parser('scaffold', help='scaffold help')
parser_scaffold.add_argument(
    'new_proc', type=str, help='name of stored procedure being scaffolded'
)

args = parser.parse_args()
commands = vars(args)

forward_input = args.forward_input
if forward_input == None:
    forward_input = False

config_file = args.config
if config_file:
    config = dotenv_values(config_file)
    conn = db.connect(config)
    cursor = conn.cursor()

    workdir = config.get('WORKDIR')
    if workdir == None:
        workdir = os.getcwd()

    editor = config.get('EDITOR')
    if editor == None:
        editor = 'nano'

    schema = args.schema
    if schema == None:
        schema = config.get('SCHEMA')
    if schema == None:
        schema = 'dbo'

    from_stdin = None
    if args.stdin:
        from_stdin = json.loads(sys.stdin.read())

    if args.list:
        files = glob.glob('*.sql', recursive=True)
        for f in files:
            print(f)

    match args.command:
        case 'dl':
            db.dl_proc_def(cursor, schema, proc_name=args.proc_name)
        case 'query':
            db.create_query(cursor)
        case 'save':
            db.save_query(args.path)
        case 'store':
            db.store_proc(cursor, args.path, schema)
        case 'run':
            json_input = args.json_input
            proc_name = args.proc_name

            if json_input == None:
                try:
                    json_input = json.loads(proc_name)
                    proc_name = None
                except:
                    pass

            json_in = merge(from_stdin, json_input)

            if proc_name == '_':
                proc_name = None

            if proc_name == None:
                db.run_query(cursor, json_in)
            else:
                db.exec_temp_jio_proc(
                    cursor, proc_name, workdir, forward_input, json_in
                )

            # NOTE: Commit gets called here so changes are not rolled back
            conn.commit()
        case 'call':
            json_in = merge(from_stdin, args.json_input)
            if args.temp:
                db.exec_temp_jio_proc(
                    cursor, args.proc_name, workdir, forward_input, json_in
                )
            else:
                db.exec_jio_proc(
                    cursor, schema, args.proc_name, forward_input, json_in
                )
            # NOTE: Commit gets called here so changes are not rolled back
            conn.commit()
        case 'scaffold':
            db.scaffold_proc(editor, args.new_proc)
