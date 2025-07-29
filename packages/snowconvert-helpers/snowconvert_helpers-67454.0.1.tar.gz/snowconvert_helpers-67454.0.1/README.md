## SnowConvert Helpers

SnowConvert Helpers is a set of classes with functions designed to facilitate the conversion of Teradata script files to
Python files that Snowflake can interpret. Snowflake SnowConvert for Teradata can take in any Teradata SQL or
scripts (BTEQ, FastLoad, MultiLoad and TPump) and convert them to functionally equivalent Snowflake SQL,
JavaScript embedded in Snowflake SQL, and Python. Any output Python code from SnowConvert will call functions from these
helper classes to complete the conversion and create a functionally equivalent output in Snowflake.

The [Snowflake Connector for Python](https://pypi.org/project/snowflake-connector-python/) will also be called in order 
to connect to your Snowflake account, and run the output python code created by SnowConvert.

For more information, visit the following webpages:

> [Snowflake SnowConvert for Teradata Documentation](https://docs.snowconvert.com/snowconvert/for-teradata/introduction)

> [User Guide for snowconvert-helpers](https://docs.snowconvert.com/snowconvert-limited-access/-MUuBuIkrrZbtDaKcru_/for-teradata/translation-reference/scripts-translation-reference)

## Release Notes
* v2.0.23 (Sep 5th, 2023)
  > * _Add error logging functionality for import_file_to_temptable, the errors are stored on a table with the name temp_table_name + \_ERROR._

* v2.0.22 (Aug 18th, 2023)
  > * _Setting Snowflake Inc proprietary information._

* v2.0.21 (July 17, 2023)
  > * _Adding support for the REPEAT statement._

* v2.0.20 (July 11, 2023)
  > * _Adding support for the USING REQUEST MODIFIER statement._

* v2.0.17 (June 16, 2023)
  > * _Adding support for MLOAD layout conditions when calling the import_file_to_temptable() method._

* v2.0.16 (May 17, 2023)
  > * _Adding support for FastLoad BEGIN LOADING through the class BeginLoading._

* v2.0.15 (March 17, 2023)
  > * _Removing max_error default value of 1 to avoid exit on error._
  > * _Adding max_errorlevel to exit when the resulting errorlevel is greater or equal to the value set._
  
* v2.0.14 (August 24, 2022)
  > * _Adding support for authentication via token in log_on function_
  > * _Adding support for token in parameter as --param-SNOW_TOKEN=VALUE_
  
* v2.0.13 (December 1, 2021)
  > * _Adding support for authenticator value used directly in log_on function_
  > * _Adding support for authenticator in parameter as --param-SNOW_AUTHENTICATOR=VALUE_
  > * _Adding support for authenticator as the seventh positional argument passed to the python in the system command line arguments_

* v2.0.12 (October 20, 2021)
  > * _Fix for positional parameter in configure_log function_

* v2.0.11 (October 19, 2021)
  > * _Adding support for authenticator in snowconvert-helpers_

* v2.0.10 (October 18, 2021)
  > * _Removing innecesary print_

* v2.0.9 (October 18, 2021)
  > * _Fix for SNOW_DEBUG_COLOR usage when logging is disabled_

* v2.0.8 (October 15, 2021)
  > * _Adding posiblity to configure python logging for snowconvert-helpers_

* v2.0.7 (September 9, 2021)
  > * _Updating User Guide documentation for snowconvert-helpers_

* v2.0.6 (July 23, 2021)
  > * _Adding a new set of static functions to class Export: defaults, null, record_mode, separator_string, separator_width, side_titles, title_dashes_with, and width_
  > * _Removing Deprecated to the functions of class Export_
  > * _Adding new exec_file function to class helpers_

* v2.0.5 (June 21, 2021)
  > * _Enabling the use of command line parameters SNOW_USER, SNOW_PASSWORD, SNOW_ACCOUNT, SNOW_DATABASE, SNOW_WAREHOUSE, SNOW_ROLE and SNOW_QUERYTAG when passed like --param-VARNAME=VALUE to logon_

* v2.0.4 (June 17, 2021)
  > * _Setting the application name to Mobilize.net when the connection is executed overriding the default PythonConnector_

* v2.0.3 (June 16, 2021)
  > * _Added @staticmethod tag to static methods with @deprecated tag_

* v2.0.2 (May 25, 2021)
  > * _Update snowconvert-helpers internal documentation_
  > * _Adding Deprecated requirement from >=1.2.12 to <2.0.0_
  > * _Marking several functions as deprecated_

* v2.0.1 (May 12, 2021)
  > * _Update snowconvert-helpers user guide link_

* v2.0.0 _(Breaking changes)_ (May 07, 2021)
  > * _Update snowflake-connector-python requirement from >=2.3.6 to >=2.4.3_
  > * _Renaming module name from snowconvert_helpers to snowconvert_
  > * _Renaming regular uses from snowconvert_helpers to snowconvert.helpers_
  > * _Renaming execute_sql_statement to exec_
  > * _Cleaning imports in \_\_init\_\_.py_
  > * _The functions exec, drop_transient_table, fast_load, import_file_to_temptable and repeat_previous_sql_statement will now have the con parameter optional, when not passed it will be used the last connection_

* v1.10.1(Feb 23, 2021)
  > * _Renaming module name from snowconverthelpers to snowconvert_helpers_

* v1.10.0(Feb 12, 2021)
  > * _Adding imports in \_\_init\_\_.py_
  > * _Adding more information web links in documentation package_

* v1.9.10(Jan 29, 2021)
  > * _Handling errors_
  > * _Logging fixes_
  > * _Use of Snow_Role environment variable for the role_
  > * _Use of Snow_QueryTag envirnoment variable for the querytag_
  > * _Added project description/documentation_
  > * _Added License_
  > * _Added Classifiers_
  > * _Modify outputs to use the pip package_

* v1.9.7(Jan 18, 2021)
  > * _Supporting correct replacing of variables like $var or $(var) in sql execution_