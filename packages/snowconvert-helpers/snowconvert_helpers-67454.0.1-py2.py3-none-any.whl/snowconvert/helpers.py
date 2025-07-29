# <copyright file="helpers.py" company="Snowflake Inc">
#     Copyright (c) 2019-2025 Snowflake Inc. All rights reserved.
# </copyright>

import atexit
import csv
import datetime
import inspect
import logging
import logging.config
import re
import sys
import subprocess
import snowflake.connector
import traceback
from functools import singledispatch
from os import access, getenv, R_OK, makedirs, path, stat, system
from deprecated import deprecated
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

snow_debug_colors = getenv("SNOW_DEBUG_COLOR", "").strip().upper()
snow_logging_enabled = getenv("SNOW_LOGGING", False)

if snow_debug_colors:
    import termcolor

def colored(text, color="blue"):
    """Prints colored text from the specified color.

        text
            The text to be printed
        color="blue"
            The color to print

    """
    if (snow_debug_colors == "YES" or snow_debug_colors == "ON" or snow_debug_colors == "TRUE"):
        return termcolor.colored(text, color)
    return text

# constants
COMPANY_NAME = "snowflake"

# global status values
_max_error_level = -1
max_errors = -1
current_error_count = 0
activity_count = 0
error_code = 0
error_level = 0
warning_code = 0
system_return_code = 0
quit_application_already_called = False

# severities dictionary
_severities_dictionary = dict()
_default_error_level = 8

# last executed sql statement
_previous_executed_sql = ""

has_passed_variables = False
passed_variables = {}

def configure_log(configuration_path=None):
    """Configures the logging that will be performed for any data related execution on the snowflake connection.
        The log file is named 'snowflake_python_connector.log' by default.

        configuration_path
            The configuration path of the file that contains all the settings desired for the logging.
    """
    if configuration_path: 
        logging.config.fileConfig(configuration_path)
    else :
        logging.basicConfig(
            filename= 'snowflake_python_connector.log',
            level=logging.DEBUG,
            format="{asctime} {levelname:<8} {message}",
            style="{",
            filemode='w')


def log(*msg, level=logging.INFO, writter=None):
    """ Prints a message to the console (standard output) or to the log file, depending on if logging is enabled.

        msg
            The message to print or log.
    """
    if snow_logging_enabled :
        finalmsg = [re.sub(r'\033\[\d*m','', str(item)) for item in msg]
        if level == logging.ERROR :
            logging.error(*finalmsg)
        elif level == logging.DEBUG:
            logging.debug(*finalmsg)
        elif level == logging.WARNING:
            logging.warning(*finalmsg)
        else:
            logging.info(*finalmsg)
    else :
        print(*msg, file=writter)

def get_from_vars_or_args_or_environment(arg_pos, variable_name, vars, args):
    """Gets the argument from the position specified or gets the value from the table vars or gets the environment variable name passed.

        arg_pos
            The argument position to be used from the arguments parameter.
        variable_name
            The name of the variable to be obtained.
        vars
            The hash with the variables names and values.
        args
            The arguments array parameter.
    """
    if (arg_pos < len(args)):
        return args[arg_pos]
    var_value = vars.get(variable_name, None)
    if (var_value is not None):
        return var_value
    env_value = getenv(variable_name)
    return env_value

def get_argkey(astr):
    """Gets the argument key value from the passed string.

    It must start with the string '--param-'
        astr
            The argument string to be used
            The string should have a value similar to --param-column=32 and
            the returned string will be 'column'
    """
    if astr.startswith('--param-'):
        astr = astr[8:astr.index('=')]
    return astr

def get_argvalue(astr):
    """Gets the argument value from the passed string.
    It must start with the string '--param-'

        astr
            The argument string to be used
            The string should have a value similar to --param-column=32 and
            the returned string will be '32'
    
    """
    if astr.startswith('--param-'):
        astr = astr[astr.index('=')+1:]
    return astr

def read_param_args(args):
    """Reads the parameter arguments from the passed array.

        args
            The arguments to be used
    """
    script_args = [item for item  in args if item.startswith("--param-")]
    dictionary = {}
    if len(script_args) > 0:
        dictionary = { get_argkey(x) : get_argvalue(x) for x in args}
        if len(dictionary) != 0:
            has_passed_variables = True
            log("Using variables")
            print_table(dictionary)
    return dictionary

def print_table(dictionary):
    """
    Prints the dictionary without exposing user and password values
    """
    length = len(dictionary)
    i = 0
    terminator = ', '
    msg = "{"
    for key,value in dictionary.items():
        if ("PASSWORD" in key or "USER" in key):
            value = "*" * 12
        i += 1
        if (i == length) :
            terminator = ''
        msg += f"'{key}':'{value}'"+terminator
    msg += "}"
    log(msg)

def expandvars(path, params, skip_escaped=False):
    """Expand environment variables of form $var and ${var}.
       If parameter 'skip_escaped' is True, all escaped variable references
       (i.e. preceded by backslashes) are skipped.
       Unknown variables are set to 'default'. If 'default' is None,
       they are left unchanged.
    """
    def replace_var(m):
        varname = m.group(3) or m.group(2)
        passvalue = params.get(varname, None)
        return getenv(varname, m.group(0) if passvalue is None else passvalue)
    reVar = (r'(?<!\)' if skip_escaped else '') + r'(\$|\&)(\w+|\{([^}]*)\})'
    return re.sub(reVar, replace_var, path)

def expands_using_params(statement, params):
    """Expands the statement passed with the parameters.

        statement
            The sql statement to be used
        params
            The parameters of the sql statement
    """
    def replace_var(m):
        varname = m.group(1)
        passvalue = params.get(varname, None)
        if (passvalue is None):
            return m.group(0)
        else:
            return str(passvalue)
    reVar = r'\{([^}]*)\}'
    return re.sub(reVar, replace_var, statement) 

def expandvar(str):
    """Expands the variable from the string passed.

        str
            The string to be expanded with the variables.
    """
    return expandvars(str, passed_variables)

opened_connections = []

def load_private_key(path, password):
    with open(path, "rb") as key_file:
        private_key_path = serialization.load_pem_private_key(
            key_file.read(),
            password=password.encode() if password else None,
            backend=default_backend()
        )
    return private_key_path

def log_on(user=None, password=None, account=None, database=None, warehouse=None, role=None, login_timeout=10, authenticator=None, token=None, private_key_path=None, private_key_password=None):
    """Logs on the snowflake database with the credentials, database, warehouse,
        role, login_timeout and authenticator passed parameters.

        user
            The user of the database
        password
            The password of the user of the database
        database
            The database to be connected
        warehouse
            The warehouse of the database to be connected
        role
            The role to be connected
        login_timeout
            The maximum timeout before giving error if the connection is taking too
            long to connect
        authenticator
            The authenticator supported value to use like SNOWFLAKE, EXTERNALBROWSER,
            SNOWFLAKE_JWT or OAUTH
        token
            The OAUTH or JWT token
        private_key_path
            The private_key_path path
        private_key_password
            The password for the private key file if applicable, if not leave it empty
    """
    global error_code
    global opened_connections
    log(f"arguments: {sys.argv}")
    # exclude arguments passed inline to the script
    args = [item for item in sys.argv if not item.startswith("--param-")]
    if (user is None):
        user = get_from_vars_or_args_or_environment(1, "SNOW_USER", passed_variables, args)
    if (password is None):
        password = get_from_vars_or_args_or_environment(2, "SNOW_PASSWORD", passed_variables, args)
    if (account is None):
        account = get_from_vars_or_args_or_environment(3, "SNOW_ACCOUNT", passed_variables, args)
    if (database is None):
        database = get_from_vars_or_args_or_environment(4, "SNOW_DATABASE", passed_variables, args)
    if (warehouse is None):
        warehouse = get_from_vars_or_args_or_environment(5, "SNOW_WAREHOUSE", passed_variables, args)
    if (role is None):
        role = get_from_vars_or_args_or_environment(6, "SNOW_ROLE", passed_variables, args)
    if (authenticator is None):
        authenticator = get_from_vars_or_args_or_environment(7, "SNOW_AUTHENTICATOR", passed_variables, args)
    if (token is None):
        token = get_from_vars_or_args_or_environment(8, "SNOW_TOKEN", passed_variables, args)
    if (private_key_path is None):
        private_key_path = get_from_vars_or_args_or_environment(9, "PRIVATE_KEY_PATH", passed_variables, args)
    if (private_key_password is None):
        private_key_password = get_from_vars_or_args_or_environment(10, "PRIVATE_KEY_PASSWORD", passed_variables, args)
    query_tag = passed_variables.get("SNOW_QUERYTAG", None)
    if (query_tag is None):
        query_tag = getenv("SNOW_QUERYTAG", None)
    if query_tag is None:
        frm = inspect.stack()[1]
        query_tag = path.basename(frm.filename)
    c = None

    try:
        p = {
                'user'          : user,
                'password'      : password,
                'account'       : account,
                'database'      : database,
                'warehouse'     : warehouse,
                'application'   : COMPANY_NAME,
                'role'          : role,
                'login_timeout' : login_timeout,
                'token'         : token,
                'session_parameters' : {
                    'QUERY_TAG': query_tag
                }
            }

        if authenticator :
            p ["authenticator"] = authenticator

        if private_key_path:
            p_key = load_private_key(private_key_path, private_key_password)
            p['private_key'] = p_key.private_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption())
            
        c = snowflake.connector.connect(**p)
    except Exception as e:
        log(f"{colored('*** Failure: logon failed :', 'red')} { str(e) }", level = logging.ERROR, writter = sys.stderr)
        error_code = 333
        quit_application(error_code)
    if c:
        opened_connections.append(c)
        error_code = 0
    return c

def at_exit_helpers():
    """Executes at the exit of the execution of the script
    """
    log("Script done >>>>>>>>>>>>>>>>>>>>")
    for c in opened_connections:
        if not c.is_closed():
            c.close()
    quit_application()

def exception_hook(exctype, value, traceback):
    """Executes when there is an exception.

        exctype
            The type of the exception
        value
            The value of the exception
        traceback
            The call stack when the exception was produced
    """
    traceback_formatted = traceback.format_exception(exctype, value, traceback)
    traceback_string = colored("*** Failure: " + "".join(traceback_formatted), 'red')
    log(traceback_string, level = logging.ERROR, writter = sys.stderr)
    quit_application(1)

def using(*argv, rows_to_read=1):
    using_dicts = []
    Import.using(using_dicts, *argv, rows_to_read=rows_to_read)
    return using_dicts

def import_file(filename, separator=' '):
    """Imports the passed filename with the optional separator.

        filename
            The file name path to be imported
        separator=' '
            The optional separator.
    """
    return Import.file(filename, separator)

def import_reset():
    return Import.reset()

def exec(sql_string, using=None, con=None):
    """Executes a sql string using the last connection, optionally it uses arguments or an specific connection.

        sql_string
            The definition of the sql
        using=None
            The optional parameter that can be used in the sql passed
        con=None
            The connection to be used, if None is passed it will use the last
            connection performed

        Examples:
            exec("SELECT * FROM USER")

            exec("SELECT * FROM SALE", con)

            exec("SELECT * FROM CUSTOMER WHERE CUSTOMERID= %S", customer)
    """
    global opened_connections
    global activity_count
    global current_error_count
    global _max_error_level
    global error_level
    global error_code
    global _previous_executed_sql
    if (con is None):
        # get last connection
        con = opened_connections[-1]

    cur = con.cursor()
    try:
        error_code = 0
        log(f"{colored('Executing: ')} { colored(sql_string, 'cyan') }")
        if ("$" in sql_string or "&" in sql_string):
            log ("Expanding variables in SQL statement")
            sql_string = expandvars(sql_string, passed_variables)
            log (f"{colored('Expanded string: ')} {colored(sql_string, 'green')}")
        if (using is not None):
                #we need to change variables from {var} to %(format)
                sql_string = re.sub(r'\{([^}]*)\}', r'%(\1)s', sql_string)
                sql_string = re.sub(r':(\w+)', r'%(\1)s', sql_string)
                log(f"using parameters {using}")
        if isinstance(using, (list, tuple)) and isinstance(using[0], (list, tuple, dict)):
            cur.executemany(sql_string, seqparams=using)
        else:
            cur.execute(sql_string, params=using)
        activity_count = cur.rowcount
        if activity_count and activity_count >= 1:
            _print_result_set(cur)
        else:
            if (Export.expandedfilename is not None):
                _print_result_set(cur)
    except snowflake.connector.errors.ProgrammingError as e:
        current_error_count = current_error_count + 1
        _handle_syntax_error(e, sql_string)
    except: # catch *all* exceptions
        current_error_count = current_error_count + 1
        e = sys.exc_info()
        msg = colored("*** Failure running statement", 'red')
        log(msg, level= logging.ERROR, writter = sys.stderr)
        log(e, level = logging.ERROR, writter = sys.stderr)
    finally:
        _previous_executed_sql = sql_string
        cur.close()
        if _max_error_level >= 0 and _max_error_level <= error_level:
            log(colored(f'*** Failure: reached max error level {error_level}', 'red'), level = logging.ERROR)
            quit_application(1)
        elif max_errors > 0 and current_error_count >= max_errors:
            log(colored(f'*** Failure: reached max number of errors  {max_errors}', 'red'), level = logging.ERROR)
            quit_application(1)

def repeat_previous_sql_statement(con=None, n=1):
    """Repeats the previous executed sql statement(s).

        con=None
            Connection if specified. If it is not passed it will use the last
            connection performed
        n=1
            The number of previous statements to be executed again
    """
    if _previous_executed_sql == "":
        if n == 0:
            n = 1
        for rep in xrange(n):
            exec(_previous_executed_sql, con)
    else:
        log("Warning: No previous SQL request.", level = logging.WARNING)

def _print_result_set(cur):
    if (Export.expandedfilename is None):
        # if there is not export file set then print to console
        log("Printing Result Set:")
        log(','.join([col[0] for col in cur.description]))
        for row in cur:
            log(','.join([str(val) for val in row]))
        log("")
    else:
        log(f">>>>>> Exporting to {Export.expandedfilename}")
        reportdir = path.dirname(Export.expandedfilename)
        makedirs(reportdir, exist_ok=True)
        with open(Export.expandedfilename, 'a') as f:
            for row in cur:
                allarenone = all(v is None for v in row)
                if (allarenone):
                    log("Row is 'None' it will not be exported")
                else:
                    rowval = Export.separator.join([str(val) for val in row])
                    print(rowval, file=f)

def _handle_syntax_error(e, sql_string):
    if "syntax error" in e.msg:
        regex = r"syntax error line (\d+) at position (\d+)"
        matches = re.finditer(regex, e.msg, re.MULTILINE)
        error_fragment = "SYNTAX ERROR:\n"
        sql_lines = sql_string.splitlines()
        last_line = -1       
        for matchNum, match in enumerate(matches, start=1):
                line = int(match.groups()[0])-1
                column = int(match.groups()[1])
                if line != last_line:
                    error_line = sql_lines[line]
                    error_line = f"{error_line[:column]} {colored(error_line[column:], 'red')}"
                    error_fragment = error_fragment + f"{line:0>2d},{column:0>2d}:{error_line}\n"
                last_line = line
        log(error_fragment, level = logging.ERROR)
    _handle_sql_error(e)

def _handle_sql_error(e):
    global error_code, error_level
    error_code = e.errno
    if error_code not in _severities_dictionary or _severities_dictionary[error_code] != 0:
        msg = colored(f"*** Failure {str(e)}", 'red')
        log(msg, level = logging.ERROR, writter = sys.stderr)
        if error_code in _severities_dictionary:
            error_level = max(error_level, _severities_dictionary[error_code])
        else:
            error_level = max(error_level, _default_error_level)

@singledispatch
def set_error_level(arg, severity_value):
    f"Invoked set_error_level with arg={arg}, severity_value={severity_value}"

@set_error_level.register(int)
def _(arg, severity_value):
    _severities_dictionary[arg] = severity_value

@set_error_level.register(list)
def _(arg, severity_value):
    for code in arg:
        _severities_dictionary[code] = severity_value

def set_default_error_level(severity_value):
    global _default_error_level
    _default_error_level = severity_value

def set_max_error_level(severity_value):
    global _max_error_level
    _max_error_level = severity_value

def os(args):
    global system_return_code
    system_return_code = system(args)

def readrun(line, skip=0):
    """Reads the given filename lines and optionally skips some lines at
    the beginning of the file.

        line
            The filename to be read
        skip=0
            The lines to be skipped
    """
    expandedpath = path.expandvars(line)
    if path.isfile(expandedpath):
        return open(expandedpath).readlines()[skip:]
    else:
        return []

def exec_file(filename, con=None):
    """Reads the content of a file and executes the sql statements contained 
    with the specified connection

        filename
            The filename to be read and executed
        con=None
            The connection to be used, if None is passed it will use the last
            connection performed
    """
    expandedpath = path.expandvars(filename)
    if path.isfile(expandedpath):
        with open(expandedpath, 'r') as f:
            contents = f.read()
            statements = contents.split(";")
            for statement in statements:
                exec(statement, con=con)
    else:
        log(colored("*** Error: File does not exist", 'red'), level = logging.ERROR, writter = sys.stderr)

def remark(arg):
    """Prints the argument.

        arg
            The argument to be printed
    """
    log(arg)

def get_error_position():
    """Gets the error position from the file using the
    information of the stack of the produced error.
    """
    stack = inspect.stack()
    important_frames = []
    for i in range(len(stack)):
        current_stack = stack[i]
        if current_stack.filename.endswith(__name__ + ".py"):
            # we skip the first one because is the frame for this function
            # now we take this element and the next max 5 ones
            next_frames = i + 5 if i + 5 < len(stack) else len(stack)
            important_frames.extend(stack[i+1:next_frames])
    stack_trace = "Error at:\n"
    for frame in important_frames:
        stack_trace = stack_trace + f"{frame.filename}:{frame.lineno} function: {frame.function} \n"
    return stack_trace

def quit_application(code=None):
    """Quits the application and optionally returns the passed code.

        code=None
            The code to be returned after it quits
    """
    global quit_application_already_called
    if quit_application_already_called:
        return
    quit_application_already_called = True
    code = code or error_level
    if code != 0:
        log(colored(f"Exit code: {code}", 'red'), level = logging.ERROR, writter = sys.stderr)
        stack_trace = get_error_position()
        log(colored(stack_trace, 'red'), level = logging.ERROR, writter = sys.stderr)
        sys.exit(code)
    else:
        log(colored(f"Exit code: {code}", 'red'), level = logging.INFO, writter = sys.stdout)

def import_file_to_temptable(filename, temp_table_name, column_definition, insert_values='*', file_delimiter=',', skip_header=1, con=None):
    """Imports the file passed to a temporary table.
    It will use a public stage named as the temporary table with the prefix
    Stage_.
    At the end of the loading to the temporary table it will delete the stage
    that was used in the process.
        filename
            The name of the file to be read
        temp_table_name
            The name of the temporary table
        column_definition
            The definition of all the fields that will have the temporary table
        insert_values
            The insert values and conditions 
        field_delimiter
            The field delimiter
        skip_header
            The number of rows to skip
        con
            The connection to be used        
    """
    temp_table_name = expandvar(temp_table_name)
    filename = expandvar(filename)
    exec(f"CREATE TRANSIENT TABLE {temp_table_name} ({column_definition})", con=con)
    BeginLoading.import_file_to_table(temp_table_name, column_definition, filename, "", [], field_delimiter=file_delimiter, skip_header=skip_header, con=con)
    exec(f"CREATE OR REPLACE TRANSIENT TABLE {temp_table_name} AS SELECT {insert_values} FROM {temp_table_name}", con=con)

def drop_transient_table(temp_table_name, con=None):
    """Drops the transient table with the specified name.
        temp_table_name
            The name of the temporary table
        con=None
            The connection to be used, if None is passed it will use the last
            connection performed    
    """
    global opened_connections
    if (con is None):
        # get last connection
        con = opened_connections[-1]

    exec(f"""DROP TABLE {temp_table_name}""", con)

def file_exists_and_readable(filename):
    return access(path.expandvars(filename), R_OK)

def exec_os(command):
    """Executes a command in the operative system.
    """
    log(f"executing os command: {command}")
    return subprocess.getoutput(command)

def fast_load(target_schema, filepath, stagename, target_table_name, con=None):
    """Executes the fast load with the passed parameters target_schema, filepath, stagename and target_table_name.
        target_schema
            The name of the schema to be used in the fast load
        filepath
            The file name path to be loaded in the table
        target_table_name
            The name of the table that will have the data loaded
        con=None
            The connection to be used, if None is passed it will use the last
            connection performed
    """
    global opened_connections
    if (con is None):
        # get last connection
        con = opened_connections[-1]   ## expand any environment var
    target_schema = expandvar(target_schema)
    filepath = expandvar(filepath)
    filename = path.basename(filepath)
    stagename = expandvar(stagename)
    target_table_name = expandvar(target_table_name)
    exec(f""" USE SCHEMA {target_schema} """, con)
    log(f"Putting file {filepath} into {stagename}...")
    exec(f"PUT file://{filepath} @{stagename} OVERWRITE = TRUE", con)
    log(f"Done put file...ErrorCode {error_code}")
    log(">>>Copying into...")
    exec(f"""
    COPY INTO {target_schema}.{target_table_name}
    FROM @{stagename}/{filename}
    FILE_FORMAT=(TYPE=CSV SKIP_HEADER=1)
    ON_ERROR=CONTINUE""", con)
    log(f"<<<Done copying. ErrorCode {error_code}")
    log(f">>>Creating temp table CTE_{target_table_name}")
    sql = f"CREATE TABLE {target_schema}.CTE_{target_table_name}  AS SELECT DISTINCT * FROM {target_schema}.{target_table_name}"
    exec(sql, con)
    log(f"<<<Done creating temp table. ErrorCode {error_code}")
    log(f">>>Droping old {target_table_name}")
    sql = f"DROP TABLE {target_schema}.{target_table_name}"
    exec(sql, con)
    log(f"<<<Done droping old table. ErrorCode {error_code}")
    log(f">>>Renaming old CTE_{target_table_name}")
    sql = f"ALTER TABLE {target_schema}.CTE_{target_table_name} RENAME TO {target_schema}.{target_table_name}"
    exec(sql, con)
    log(f"<<<Done droping old table. ErrorCode {error_code}")

atexit.register(at_exit_helpers)

def exception_hook(exctype, value, tback):
    log(colored(f"*** Failure: {value}", 'red'), level = logging.ERROR, writter = sys.stderr)
    traceback_formatted = traceback.format_exception(exctype, value, tback)
    traceback_string = "".join(traceback_formatted)
    log(traceback_string, level = logging.ERROR, writter = sys.stderr)
    quit_application(1)

sys.excepthook = exception_hook
   
class Import:
    expandedfilename = None
    separator=' '
    reader = None
    no_more_rows = False
    read_obj = None

    @staticmethod
    def file(file, separator=' '):
        Import.separator = separator
        Import.expandedfilename = path.expandvars(file)
        Import.reader = None
        if (not Import.read_obj is None):
            Import.read_obj.close()
        Import.read_obj = None
        Import.no_more_rows = False

    @staticmethod
    def using(globals, *argv, rows_to_read=1):
        print (argv)
        try:
            variables_li = [] 
            types_li = []
            i = 0
            while i < len(argv):
                elem = argv[i]
                if (i % 2 == 0): 
                    variables_li.append(elem) 
                else: 
                    types_li.append(elem)
                i += 1
            i = 0
            # init the global variables for the using clause
            rowDict = {}
            while i < len(variables_li):
                initvalue = None
                if (types_li[i].startswith("DECIMAL")):
                    initvalue = 0
                else:
                    if (types_li[i].startswith("DATE")):
                        initvalue = datetime.date.min
                    else:
                         if (types_li[i].startswith("TIMESTAMP")):
                            initvalue = datetime.datetime.min
                rowDict[variables_li[i]] = initvalue
                i += 1
            globals.append(rowDict)
            # open file in read mode
            if (Import.expandedfilename is not None):
                if (Import.reader is None):
                    read_obj = open(Import.expandedfilename, 'r')
                    log(f">>>>>>>>> Importing from {Import.expandedfilename}")
                    if (stat(Import.expandedfilename).st_size == 0):
                        log("Import file is empty")
                        return
                    else:
                        # pass the file object to reader() to get the reader object
                        Import.reader = csv.reader(read_obj, delimiter=Import.separator)
                # read next row
                log("Reading rows")
                log('READER', Import.reader)
                log('VAR_LI', variables_li)
                # reset globals list
                globals.clear()             
                rowNum = 0
                # row variable is a list that represents a row in csv
                for row in Import.reader:
                    if rowNum == rows_to_read:
                        break
                    rowDict = {}
                    columnNum = 0
                    log('ROW', row)
                    while columnNum < len(variables_li):
                        rowDict[variables_li[columnNum]] = row[columnNum]
                        columnNum += 1
                    globals.append(rowDict)
                    rowNum += 1
        except StopIteration:
            Import.no_more_rows = True
            log ("No more rows")
        except Exception as e:
            log (f"*** Failure importing {e}")
        log("Done importing")
    def reset():
            Import.expandedfilename = None
            Import.separator = ' '

class Export:
    expandedfilename = None
    separator = ' '
    _record_mode = False
    _separator_width = 2
    _side_titles = False
    _title_dashes = False
    _title_dashes_with = 0
    _width = 80
    _null = '?'

    @staticmethod
    def defaults():
        Export.reset()

    @staticmethod
    def null(value = None):
        if value is not None:
            Export._null = value
        return Export._null

    @staticmethod
    def record_mode(value = None):
        if value is not None:
            Export._record_mode = value
        return Export._record_mode

    @staticmethod
    def report(file, separator=' '):
        Export.separator = separator
        Export.expandedfilename = path.expandvars(file)

    @staticmethod
    def reset():
        Export.expandedfilename = None
        Export.record_mode(False)
        Export.title_dashes(False, 0)
        Export.side_titles(False)
        Export.separator_string(' ')
        Export.separator_width(2)
        Export.width(80)
        Export.null('?')

    @staticmethod
    def separator_string(value = None):
        if (value is not None):
            Export.separator = value
        return Export.separator

    @staticmethod
    def separator_width(value = None):
        if (value is not None):
            Export._separator_width = value
        return Export._separator_width

    @staticmethod
    def side_titles(value = None):
        if value is not None:
            Export._side_titles = value
        return Export._side_titles

    @staticmethod
    def title_dashes(value = None, withValue = None):
        if value is not None:
            Export._title_dashes = value
        if withValue is not None:
            Export.title_dashes_with(withValue)
        return Export._title_dashes
    
    @staticmethod
    def title_dashes_with(value = None):
        if value is not None:
            Export._title_dashes_with = value
        return Export._title_dashes_with

    @staticmethod
    def width(value = None):
        if value is not None:
            Export._width = value
        return Export._width

class BeginLoading:

    @staticmethod
    def import_file_to_table(target_schema_table, define_columns, define_file, begin_loading_columns, begin_loading_values, field_delimiter = ",", skip_header=0, input_data_place_holder=None, con=None):
        """Imports the file passed to a temporary table.
        It will use a public stage named as the temporary table with the prefix
        Stage_.
        At the end of the loading to the temporary table it will delete the stage
        that was used in the process.
            target_schema_table
                the target schema (optional) and table name
            define_file
                The name of the file to be read
            define_columns
                The definition of all the columns for the temporary table
            begin_loading_columns
                The column names to insert. Dictates the order in which values are inserted
            begin_loading_values
                The list of raw insert values to convert
            field_delimiter
                The field delimiter
            skip_header
                The number of rows to skip
            input_data_place_holder
                The location of the file in a supported cloud provider. Set parameter when the file is not stored locally
            con
                The connection to be used
        """

        global opened_connections
        if (con is None):
            # get last connection
            con = opened_connections[-1]

        is_local_file = input_data_place_holder is None
        if is_local_file:
            stage_name = BeginLoading._get_stage_name(target_schema_table)
            exec(f"CREATE OR REPLACE TEMPORARY STAGE {stage_name} FILE_FORMAT=(TYPE=CSV)", con=con)
            stage_name = f"@{stage_name}"
            exec(f"PUT file://{define_file} {stage_name} OVERWRITE=TRUE", con=con)
        else:
            stage_name = input_data_place_holder

        fileFormat = f"FIELD_DELIMITER = '{field_delimiter}'" if field_delimiter not in ['', 'UNFORMATTED'] else "FIELD_DELIMITER = ' ' FIELD_OPTIONALLY_ENCLOSED_BY = 'NONE'"
        unordered_actual_values = [] 
        if define_columns != "" and field_delimiter == '':
            unordered_actual_values = BeginLoading._get_substrings(define_columns)

        copy_into = f""
        if define_columns != "" and begin_loading_values != []:            
            column_names = BeginLoading._get_column_names(define_columns)
            if field_delimiter != '':
                unordered_actual_values = [f"${index + 1}" for index in range(0, len(column_names))]           
            select_values = BeginLoading._get_select_values(column_names, begin_loading_values, unordered_actual_values)
            copy_into = f"COPY INTO {target_schema_table} {begin_loading_columns} FROM (SELECT {select_values} FROM {stage_name})  FILE_FORMAT=(TYPE=CSV SKIP_HEADER={skip_header} {fileFormat}) ON_ERROR=CONTINUE"
        else:
            select_values = ', '.join(unordered_actual_values) if unordered_actual_values != [] else '*'
            copy_into = f"COPY INTO {target_schema_table} FROM (SELECT {select_values} FROM {stage_name})  FILE_FORMAT=(TYPE=CSV SKIP_HEADER={skip_header} {fileFormat}) ON_ERROR=CONTINUE"

        exec(copy_into, con=con)        

        exec(f"""CREATE TABLE IF NOT EXISTS {target_schema_table}_ERROR (
        "DATE" TIMESTAMP,
        CATEGORY CHAR(5000),
        ERROR CHAR(5000),
        LINE CHAR(5000),
        "CHARACTER" CHAR(5000),
        COLUMN_NAME CHAR(5000),
        REJECTED_RECORD CHAR(5000))
        """)
        exec(f"""EXECUTE IMMEDIATE $$
            BEGIN    
                INSERT INTO {target_schema_table}_ERROR 
                SELECT CURRENT_TIMESTAMP,"CATEGORY", "ERROR", "LINE", "CHARACTER", "COLUMN_NAME", "REJECTED_RECORD"  
                FROM TABLE(VALIDATE({target_schema_table}, JOB_ID => '_last'));
            END;
        $$;
        """)

        if is_local_file:
            exec(f"DROP STAGE {stage_name[1:]}", con=con)

        exec(f"""CREATE TABLE {target_schema_table}_CTE AS SELECT DISTINCT * FROM {target_schema_table}""", con=con)
        exec(f"""DROP TABLE {target_schema_table}""", con=con)
        exec(f"""ALTER TABLE {target_schema_table}_CTE RENAME TO {target_schema_table}""", con=con)

    @staticmethod
    def _get_substrings(define_columns):
        """Gets a list of substring functions such as 'SUBSTRING($1, position, length)' based on a column definition.
            define_columns
                The definition of all the fields that will have the temporary table
        """
        unordered_actual_values = []
        RE_COLUMN = re.compile(".+\(?.+\((\d+).*\)\)?", re.IGNORECASE)
        columns = re.split(r"\s*(?<=\)),", define_columns.replace("\n",""))
        position = 1
        for i in range(0,len(columns)):
            parts = list(RE_COLUMN.match(columns[i]).groups())
            length = int(parts[0])
            unordered_actual_values += [f"SUBSTRING($1, {position}, {length})"]
            position = position + length
        return unordered_actual_values

    @staticmethod
    def _get_column_names(define_columns):
        """Gets a list of column names based on a column definition.
            define_columns
                The definition of all the fields that will have the temporary table
        """
        return re.findall(r'([\w\d]+)\s+\(.*?\)', define_columns.upper())

    @staticmethod
    def _get_select_values(column_names, begin_loading_values, unordered_actual_values):
        """Gets an ordered string of the actual values to be inserted in the loading process.
            column_names
                The list of column names
            begin_loading_values
                The list of raw insert values to convert
            unordered_actual_values
                The list of the unordered insert values
        """
        pattern = r":(\w+)"
        return re.sub(pattern, lambda match: unordered_actual_values[column_names.index(match.group(0).strip(':').upper())], ', '.join(map(str, begin_loading_values)))

    @staticmethod
    def _get_stage_name(target_schema_table):
        schema_table_list = target_schema_table.split('.')

        if len(schema_table_list) == 2:
            return f"{schema_table_list[0]}.Stage_{schema_table_list[1]}"
        
        return f"Stage_{target_schema_table}"

class Parameters:
    passed_variables = {}

## Loading extra parameters from command line
passed_variables = read_param_args(sys.argv[1:])
