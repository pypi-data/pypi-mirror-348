import argparse
import datetime
import json

from database_mysql_local.connector import Connector
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.LoggerLocal import Logger

SQL2CODE_COMPONENT_ID = 221
SQL2CODE_COMPONENT_NAME = "Sql2Code"
DEVELOPER_EMAIL = "roee.s@circ.zone"
sql2code_logger_code_object = {
    'component_id': SQL2CODE_COMPONENT_ID,
    'component_name': SQL2CODE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}

logger = Logger.create_logger(object=sql2code_logger_code_object)

# TODO Create .logger.json files such as https://github.com/circles-zone/logger-local-python-package/blob/dev/.logger.json.example from component_table

# TODO Implement generate_table_columns.py using Sql2Code (so we can delete generate_table_columns.py)


# TODO: to inherit from GenericCRUD - Low priority (Can cause circular dependency)
class SQL2Code:
    def __init__(self, default_schema_name: str, connection: Connector = None):
        self.schema_name = default_schema_name
        self.connection = connection or Connector.connect(schema_name=self.schema_name)
        self.cursor = self.connection.cursor()

    def read_table(self, table_name: str, columns_list: list[str] = None) -> dict:
        data_dict = {}
        i = 0
        logger.start(object={"table_name": table_name, "columns_list": columns_list})

        if columns_list is None:
            columns_list = ['*']
        column_str = ','.join(columns_list)
        schema_name = self.schema_name
        query = f"SELECT {column_str} FROM {schema_name}.{table_name}"
        logger.info(f"\nthis is query: {query}")
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        logger.info(f"\nthis is rows: {rows}")

        if columns_list == ['*']:
            columns_list = [desc[0] for desc in self.cursor.description()]
            logger.info("\nThis is columns_list name: "', '.join(column_name for column_name in columns_list))

        while (i < len(rows)):
            j = 0
            for col in columns_list:
                # logger.info(f"\n{col} -> {rows[i][j]}")
                if i == 0:
                    data_dict[col] = [rows[i][j]]
                else:
                    data_dict[col].append(rows[i][j])
                j += 1
            i += 1

        # logger.info(f"\nData dictionary: {data_dict}")
        logger.end(object={"return value": data_dict})

        return data_dict

    def create_code(self, language, format) -> str:
        # TODO use the Computer Languge enum we have/should have in Python SDK 
        if language == "Python" and format == "dictionary":
            res = "Python code as a dictionary"
        elif language == "TypeScript" and format == "dictionary":
            res = "TypeScript code as a dictionary"
        else:
            res = "Unsupported language or format combination"
        logger.info(f"Generated code: {res}")
        return res

    def switch_db(self, new_database: str) -> None:
        """Switches the database to the given database name."""
        logger.start(object={"default_schema_name": new_database})
        self.connection.set_schema(new_database)
        self.schema_name = new_database
        logger.end("Schema set successfully.")

    def set_schema(self, schema_name: str):
        """Sets the schema to the default schema."""
        logger.start()
        self.connection.set_schema(schema_name)
        self.schema_name = schema_name
        logger.end()

    def close(self) -> None:
        """Closes the connection to the database."""
        logger.start()
        self.connection.close()
        logger.end()


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)


# TODO: Do we really need this main function?
# TODO: add more formats
def main():
    parser = argparse.ArgumentParser(description="Generate code based on data in a database of Circles Ai")
    parser.add_argument("--schema", help="Database schema can be relationship_type", required=True)
    parser.add_argument("--table", help="Database table can be relationship_type_ml_table", required=True)
    parser.add_argument("--columns", help="Columns to select make sure they comma-separated")
    parser.add_argument("--language", help="Code created in Python or TypeScript", choices=["Python", "TypeScript"])
    parser.add_argument("--format", help="Code format as a dictionary)")
    parser.add_argument("--output_path", help="Output file path", default='')

    args = parser.parse_args()

    Sql2code = SQL2Code(default_schema_name=args.schema)
    logger.info("\n---------- Success to connect MySql Circles Ai Server ---------- \n")
    if args.columns is None:
        data = Sql2code.read_table(args.table)
    else:
        data = Sql2code.read_table(args.table, args.columns.split(',') if args.columns else None)

    if args.language == 'Python' and args.format == 'dictionary':
        # Write data to a .py file as a dictionary of dictionaries
        file_name = args.table.rsplit('_', 1)[0]
        logger.info(f"\nWriting to file_name: {file_name}")
        with open(f"{args.output_path}/{file_name}.py", 'w') as f:
            f.write("# Generated by SQL2Code (circles-zone/sql2code-local-python-packge/sql_to_code/src/sqltocode.py running from GHA .github/workflows using sql2code-command-line parameter and calling github-workflows/.github/workflows)\n\n")  # Add comment at the top
            f.write(f"{file_name} = {{\n")
            json.dump(data, f, cls=DateTimeEncoder, indent=2)
            logger.info(f"\nFinished writing to file: {args.output_path}/{file_name}.py")

    # Write data to a .py file as a class of classes
    # with open(f"{args.output_path}/{args.table}.py", 'w') as f:
    #     # Write the wrapper class definition to the file
    #     f.write(f"class {args.table.upper()}:\n")
    #     for i in range(len(data["table_name"])):
    #         # Write the class definition to the file, indented under the wrapper class
    #         f.write(f"    class {data['table_name'][i].upper()}:\n")
    #         for key, values in data.items():
    #             if key != "table_name":
    #                 # Write the field definition to the file, indented under the class
    #                 f.write(f"        {key.upper()} = {repr(values[i])}\n")
    #         # Write a newline to separate the classes
    #         f.write("\n")

    # TODO: Do we really need to generate code? What is the use case?
    if args.language is not None and args.format is not None:
        generated_code = Sql2code.create_code(args.language, args.format)
        logger.info(f"\nGenerated code:\n{generated_code}")

    logger.info(f"\nThe requested Table:\n{data}")


if __name__ == "__main__":
    main()
