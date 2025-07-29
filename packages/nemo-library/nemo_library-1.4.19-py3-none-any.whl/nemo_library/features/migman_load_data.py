from datetime import datetime
import json
import logging
import os
import re
import pandas as pd

from tabulate import tabulate

from nemo_library.features.migman_database import MigManDatabaseLoad
from nemo_library.features.nemo_persistence_api import (
    createImportedColumns,
    createReports,
    createRules,
    getImportedColumns,
    getProjectID,
)
from nemo_library.features.nemo_persistence_api import createProjects
from nemo_library.features.nemo_report_api import LoadReport
from nemo_library.model.imported_column import ImportedColumn
from nemo_library.model.migman import MigMan
from nemo_library.model.project import Project
from nemo_library.model.report import Report
from nemo_library.model.rule import Rule
from nemo_library.utils.config import Config
from nemo_library.features.fileingestion import ReUploadDataFrame
from nemo_library.utils.migmanutils import (
    get_mig_man_field,
    get_migman_fields,
    get_migman_mandatory_fields,
    get_migman_postfixes,
    get_migman_project_list,
    getProjectName,
    is_migman_project_existing,
)
from nemo_library.utils.utils import (
    get_internal_name,
    log_error,
)
from nemo_library.features.import_configuration import ImportConfigurations

__all__ = ["MigManLoadData"]


def MigManLoadData(config: Config) -> None:
    """
    Main function to load data for MigMan projects.

    This function retrieves the configuration, checks for the existence of projects in the database,
    and processes data files for each project and its associated postfixes. If the project or columns
    are not defined in NEMO, they are created. Data is then uploaded, and deficiency mining reports
    are updated.

    Args:
        config (Config): Configuration object containing MigMan settings.

    Raises:
        ValueError: If a project is not found in the database.
    """
    # get configuration
    local_project_directory = config.get_migman_local_project_directory()
    multi_projects = config.get_migman_multi_projects()
    projects = get_migman_project_list(config)

    database = MigManDatabaseLoad()
    for project in projects:

        # check for project in database
        if not is_migman_project_existing(database, project):
            raise ValueError(f"project '{project}' not found in database")

        # get list of postfixes
        postfixes = get_migman_postfixes(database, project)

        # init project
        multi_projects_list = (
            (multi_projects[project] if project in multi_projects else None)
            if multi_projects
            else None
        )
        if multi_projects_list:
            for addon in multi_projects_list:
                for postfix in postfixes:
                    _load_data(
                        config,
                        database,
                        local_project_directory,
                        project,
                        addon,
                        postfix,
                    )
        else:
            for postfix in postfixes:
                _load_data(
                    config, database, local_project_directory, project, None, postfix
                )


def _load_data(
    config: Config,
    database: list[MigMan],
    local_project_directory: str,
    project: str,
    addon: str,
    postfix: str,
) -> None:
    """
    Loads data for a specific project, addon, and postfix.

    This function checks for the existence of the data file, validates its contents,
    and uploads it to NEMO. It also creates missing columns and updates deficiency
    mining reports.

    Args:
        config (Config): Configuration object.
        database (list[MigMan]): List of MigMan database entries.
        local_project_directory (str): Path to the local project directory.
        project (str): Name of the project.
        addon (str): Addon name (optional).
        postfix (str): Postfix for the project.
    """
    # check for file first
    project_name = getProjectName(project, addon, postfix)
    file_name = os.path.join(
        local_project_directory,
        "srcdata",
        f"{project_name}.csv",
    )

    if os.path.exists(file_name):
        logging.info(
            f"File '{file_name}' for '{project}', addon '{addon}', postfix '{postfix}' found"
        )

        # does project exist? if not, create it
        new_project = False
        projectid = getProjectID(config, project_name)
        if not projectid:
            new_project = True
            logging.info(f"Project not found in NEMO. Create it...")
            createProjects(
                config=config,
                projects=[
                    Project(
                        displayName=project_name,
                        description=f"Data Model for Mig Man table '{project}'",
                    )
                ],
            )

        # check whether file is newer than uploaded data
        time_stamp_file = datetime.fromtimestamp(os.path.getmtime(file_name)).strftime(
            "%d.%m.%Y %H:%M:%S"
        )
        if not new_project:
            df = LoadReport(
                config=config,
                projectname=project_name,
                report_name="static information",
            )
            if df["TIMESTAMP_FILE"].iloc[0] == time_stamp_file:
                logging.info(
                    f"file and data in NEMO has the same time stamp ('{time_stamp_file}'). Ignore this file"
                )
                return

        # read the file now and check the fields that are filled in that file
        datadf = pd.read_csv(
            file_name,
            sep=";",
            dtype=str,
        )

        # drop all columns that are totally empty
        columns_to_drop = datadf.columns[datadf.isna().all()]
        datadf_cleaned = datadf.drop(columns=columns_to_drop)
        if not columns_to_drop.empty:
            logging.info(
                f"totally empty columns removed. Here is the list {json.dumps(columns_to_drop.to_list(),indent=2)}"
            )

        # reconcile migman columns with columns from import file
        columns_migman = get_migman_fields(database, project, postfix)
        for col in datadf_cleaned.columns:
            if not col in columns_migman:
                log_error(
                    f"file {file_name} contains column '{col}' that is not defined in MigMan Template"
                )

        # check mandatory fields
        mandatoryfields = get_migman_mandatory_fields(database, project, postfix)
        for field in mandatoryfields:
            if not field in datadf_cleaned.columns:
                raise ValueError(
                    f"file {file_name} is missing mandatory field '{field}'"
                )

        ics_nemo = getImportedColumns(config, project_name)
        ics_import_names = [ic.importName for ic in ics_nemo]

        new_columns = []
        for col in datadf_cleaned.columns:

            # column already defined in nemo? if not, create it
            if not col in ics_import_names:
                logging.info(
                    f"column '{col}' not found in project {project_name}. Create it."
                )

                col_migman = get_mig_man_field(
                    database, project, postfix, columns_migman.index(col) + 1
                )

                if not col_migman:
                    log_error(
                        f"could nof find record in migman database for project '{project}', postfix '{postfix}' and index {columns_migman.index(col) + 1}"
                    )

                # Convert JSON data to a list of tuples
                table_data = [
                    (key, value if value else "<None>")
                    for key, value in col_migman.to_dict().items()
                ]

                # Print the table
                description = tabulate(
                    table_data,
                    headers=["Field", "Value"],
                    tablefmt="plain",
                    maxcolwidths=[35, 30],
                )
                new_columns.append(
                    ImportedColumn(
                        displayName=col_migman.nemo_display_name,
                        importName=col_migman.nemo_import_name,
                        internalName=col_migman.nemo_internal_name,
                        description=description,
                        dataType="string",
                        order=f"{(columns_migman.index(col) + 1):03}",
                    )
                )

        if new_columns:
            createImportedColumns(
                config=config,
                projectname=project_name,
                importedcolumns=new_columns,
            )

        # now we have created all columns in NEMO. Upload data
        datadf_cleaned["timestamp_file"] = time_stamp_file
        ReUploadDataFrame(
            config=config,
            projectname=project_name,
            df=datadf_cleaned,
            update_project_settings=False,
            version=3,
            datasource_ids=[{"key": "datasource_id", "value": project_name}],
            import_configuration=ImportConfigurations(
                skip_first_rows=1,
                record_delimiter="\n",
                field_delimiter=";",
                optionally_enclosed_by='"',
                escape_character="\\",
            ),
        )

        _update_static_report(config=config, project_name=project_name)

        # if there are new columns, update all reports
        if new_columns:
            _update_deficiency_mining(
                config=config,
                project_name=project_name,
                postfix=postfix,
                columns_in_file=datadf_cleaned.columns,
                database=database,
            )
    else:
        logging.info(f"File {file_name} for project {project_name} not found")


def _update_static_report(
    config: Config,
    project_name: str,
) -> None:
    """
    Updates the static information report for a project.

    This report contains the latest timestamp of the uploaded file.

    Args:
        config (Config): Configuration object.
        project_name (str): Name of the project.
    """
    sql_query = """
SELECT  
    MAX(timestamp_file) AS timestamp_file
FROM 
    $schema.$table
WHERE
    not timestamp_file = 'timestamp_file'
"""
    createReports(
        config=config,
        projectname=project_name,
        reports=[
            Report(
                displayName="static information",
                querySyntax=sql_query,
                internalName="static_information",
                description="return static information",
            )
        ],
    )


def _update_deficiency_mining(
    config: Config,
    project_name: str,
    postfix: str,
    columns_in_file: list[str],
    database: list[MigMan],
) -> None:
    """
    Updates deficiency mining reports and rules for a project.

    This function generates column-specific and global deficiency mining reports
    based on the data file and MigMan database definitions.

    Args:
        config (Config): Configuration object.
        project_name (str): Name of the project.
        postfix (str): Postfix for the project.
        columns_in_file (list[str]): List of columns in the data file.
        database (list[MigMan]): List of MigMan database entries.
    """
    logging.info(
        f"Update deficiency mining reports and rules for project {project_name}"
    )

    # create column specific fragments
    frags_checked = []
    frags_msg = []
    joins = {}
    migman_fields = [
        x
        for x in database
        if x.project == project_name
        and x.postfix == postfix
        and x.nemo_import_name in columns_in_file
    ]
    for migman_field in migman_fields:

        frag_check = []
        frag_msg = []

        # data type specific checks
        match migman_field.desc_section_data_type.lower():
            case "character":
                # Parse format to get maximum length
                match = re.search(r"x\((\d+)\)", migman_field.desc_section_format)
                field_length = int(match.group(1)) if match else len(format)
                frag_check.append(
                    f"LENGTH({migman_field.nemo_internal_name}) > {field_length}"
                )
                frag_msg.append(
                    f"{migman_field.nemo_display_name} exceeds field length (max {field_length} digits)"
                )

            case "integer" | "decimal":
                # Parse format
                negative_numbers = "-" in migman_field.desc_section_format
                format = (
                    migman_field.desc_section_format.replace("-", "")
                    if negative_numbers
                    else migman_field.desc_section_format
                )

                if not negative_numbers:
                    frag_check.append(
                        f"LEFT(TRIM({migman_field.nemo_internal_name}), 1) = '-' OR RIGHT(TRIM({migman_field.nemo_internal_name}), 1) = '-'"
                    )
                    frag_msg.append(
                        f"{migman_field.nemo_display_name} must not be negative"
                    )

                # decimals?
                decimals = len(format.split(".")[1]) if "." in format else 0
                if decimals > 0:
                    format = format[: len(format) - decimals - 1]
                    frag_check.append(
                        f"""LOCATE(TO_VARCHAR(TRIM({migman_field.nemo_internal_name})), '.') > 0 AND 
            LENGTH(RIGHT(TO_VARCHAR(TRIM({migman_field.nemo_internal_name})), 
                        LENGTH(TO_VARCHAR(TRIM({migman_field.nemo_internal_name}))) - 
                        LOCATE(TO_VARCHAR(TRIM({migman_field.nemo_internal_name})), '.'))) > {decimals}"""
                    )
                    frag_msg.append(
                        f"{migman_field.nemo_display_name} has too many decimals ({decimals} allowed)"
                    )

                match = re.search(r"z\((\d+)\)", format)
                field_length = int(match.group(1)) if match else len(format)

                frag_check.append(
                    f"""LENGTH(
                    LEFT(
                        REPLACE(TO_VARCHAR(TRIM({migman_field.nemo_internal_name})), '-', ''), 
                        LOCATE('.', REPLACE(TO_VARCHAR(TRIM({migman_field.nemo_internal_name})), '-', '')) - 1
                    )
                ) > {field_length}"""
                )
                frag_msg.append(
                    f"{migman_field.nemo_display_name} has too many digits before the decimal point ({field_length} allowed)"
                )

                frag_check.append(
                    fr"NOT {migman_field.nemo_internal_name} LIKE_REGEXPR('^[-]?(?:[0-9]+|\d{1,3}(?:\.\d{3})+)(?:,\d+)?$')"
                )
                frag_msg.append(
                    f"{migman_field.nemo_display_name} is not a valid number"
                )

            case "date":
                frag_check.append(
                    f"NOT {migman_field.nemo_internal_name} LIKE_REGEXPR('^(\\d{{4}})-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$')"
                )
                frag_msg.append(f"{migman_field.nemo_display_name} is not a valid date")

        # special fields

        if "mail" in migman_field.nemo_internal_name:
            frag_check.append(
                f"NOT {migman_field.nemo_internal_name} LIKE_REGEXPR('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{{2,}}$')"
            )
            frag_msg.append(f"{migman_field.nemo_display_name} is not a valid email")

        # VAT_ID
        if "s_ustid_ustid" in migman_field.nemo_internal_name:
            joins[migman_field.nemo_internal_name] = {"CLASSIFICATION": "VAT_ID"}
            frag_check.append(
                f"(genius_{migman_field.nemo_internal_name}.STATUS IS NOT NULL AND genius_{migman_field.nemo_internal_name}.STATUS = 'check')"
            )
            frag_msg.append(
                f"genius analysis: ' || genius_{migman_field.nemo_internal_name}.STATUS_MESSAGE || '"
            )
        # URL
        elif "s_adresse_homepage" in migman_field.nemo_internal_name:
            joins[migman_field.nemo_internal_name] = {"CLASSIFICATION": "URL"}
            frag_check.append(
                f"(genius_{migman_field.nemo_internal_name}.STATUS IS NOT NULL AND genius_{migman_field.nemo_internal_name}.STATUS = 'check')"
            )
            frag_msg.append(
                f"genius analysis: ' || genius_{migman_field.nemo_internal_name}.STATUS_MESSAGE || '"
            )

        # now build deficiency mining report for this column (if there are checks)
        if frag_check:

            # save checks and messages for total report
            frags_checked.extend(frag_check)
            frags_msg.extend(frag_msg)
            sorted_columns = [
                f'{migman_field.nemo_internal_name} AS "{migman_field.nemo_display_name}"'
            ] + [
                f'{other_field.nemo_internal_name} AS "{other_field.nemo_display_name}"'
                for other_field in database
                if other_field.project == project_name
                and other_field.postfix == postfix
                and other_field.index != migman_field.index
                and other_field.nemo_import_name in columns_in_file
            ]

            # case statements for messages and dm report
            case_statement_specific = " ||\n\t".join(
                [
                    f"CASE\n\t\tWHEN {check}\n\t\tTHEN CHAR(10) || '{msg}'\n\t\tELSE ''\n\tEND"
                    for check, msg in zip(frag_check, frag_msg)
                ]
            )

            status_conditions = " OR ".join(frag_check)

            sql_statement = f"""SELECT
\tCASE 
\t\tWHEN {status_conditions} THEN 'check'
\tELSE 'ok'
\tEND AS STATUS
\t,LTRIM({case_statement_specific},CHAR(10)) AS DEFICIENCY_MININNG_MESSAGE
\t,{',\n\t'.join(sorted_columns)}
FROM
\t$schema.$table
"""
            if migman_field.nemo_internal_name in joins:
                sql_statement += f"""LEFT JOIN
\t$schema.SHARED_NAIGENT genius_{migman_field.nemo_internal_name}
ON  
\t    genius_{migman_field.nemo_internal_name}.CLASSIFICATION = '{joins[migman_field.nemo_internal_name]["CLASSIFICATION"]}'
\tAND genius_{migman_field.nemo_internal_name}.VALUE          = {migman_field.nemo_internal_name}
"""

            # create the report
            report_display_name = f"(DEFICIENCIES) {migman_field.index:03} {migman_field.nemo_display_name}"
            report_internal_name = get_internal_name(report_display_name)

            createReports(
                config=config,
                projectname=project_name,
                reports=[
                    Report(
                        displayName=report_display_name,
                        internalName=report_internal_name,
                        querySyntax=sql_statement,
                        description=f"Deficiency Mining Report for column '{migman_field.nemo_display_name}' in project '{project_name}'",
                    )
                ],
            )

            createRules(
                config=config,
                projectname=project_name,
                rules=[
                    Rule(
                        displayName=f"DM_{migman_field.index:03}: {migman_field.nemo_display_name}",
                        ruleSourceInternalName=report_internal_name,
                        ruleGroup="02 Columns",
                        description=f"Deficiency Mining Rule for column '{migman_field.nemo_display_name}' in project '{project_name}'",
                    )
                ],
            )

        logging.info(
            f"project: {project_name}, column: {migman_field.nemo_display_name}: {len(frag_check)} frags added"
        )

    # now setup global dm report and rule
    case_statement_specific, status_conditions = _create_dm_rule_global(
        config=config,
        project_name=project_name,
        postfix=postfix,
        columns_in_file=columns_in_file,
        database=database,
        frags_checked=frags_checked,
        frags_msg=frags_msg,
        sorted_columns=sorted_columns,
        joins=joins,
    )

    # create report for mig man
    _create_report_for_migman(
        config=config,
        project_name=project_name,
        postfix=postfix,
        columns_in_file=columns_in_file,
        database=database,
        case_statement_specific=case_statement_specific,
        status_conditions=status_conditions,
        joins=joins,
    )

    # create report for the customer containing all errors
    _create_report_for_customer(
        config=config,
        project_name=project_name,
        postfix=postfix,
        columns_in_file=columns_in_file,
        database=database,
        case_statement_specific=case_statement_specific,
        status_conditions=status_conditions,
        joins=joins,
    )

    logging.info(f"Project {project_name}: {len(frags_checked)} checks implemented...")
    return len(frags_checked)


def _create_dm_rule_global(
    config: Config,
    project_name: str,
    postfix: str,
    columns_in_file: list[str],
    database: list[MigMan],
    frags_checked: list[str],
    frags_msg: list[str],
    sorted_columns: list[str],
    joins: dict[str, dict[str, str]],
) -> (str, str):  # type: ignore
    """
    Creates a global deficiency mining rule and report for a project.

    Args:
        config (Config): Configuration object.
        project_name (str): Name of the project.
        postfix (str): Postfix for the project.
        columns_in_file (list[str]): List of columns in the data file.
        database (list[MigMan]): List of MigMan database entries.
        frags_checked (list[str]): List of condition fragments for checks.
        frags_msg (list[str]): List of messages corresponding to checks.
        sorted_columns (list[str]): List of sorted columns for the report.
        joins (dict[str, dict[str, str]]): Join conditions for the report.

    Returns:
        tuple: Case statement and status conditions for the global rule.
    """
    # case statements for messages and dm report
    case_statement_specific = " ||\n\t".join(
        [
            f"CASE\n\t\tWHEN {check}\n\t\tTHEN  CHAR(10) || '{msg}'\n\t\tELSE ''\n\tEND"
            for check, msg in zip(frags_checked, frags_msg)
        ]
    )

    status_conditions = " OR ".join(frags_checked)

    sql_statement = f"""WITH CTEDefMining AS (
    SELECT
        {',\n\t\t'.join([x.nemo_internal_name for x in database if x.project == project_name and x.postfix == postfix and x.nemo_display_name in columns_in_file])}
        ,LTRIM({case_statement_specific},CHAR(10)) AS DEFICIENCY_MININNG_MESSAGE
        ,CASE 
            WHEN {status_conditions} THEN 'check'
            ELSE 'ok'
        END AS STATUS
    FROM
        $schema.$table"""

    for join in joins:
        sql_statement += f"""
LEFT JOIN
\t$schema.SHARED_NAIGENT genius_{join}
ON  
\t    genius_{join}.CLASSIFICATION = '{joins[join]["CLASSIFICATION"]}'
\tAND genius_{join}.VALUE          = {join}"""

    sql_statement += f"""       
)
SELECT
      Status
    , DEFICIENCY_MININNG_MESSAGE
    , {',\n\t'.join(sorted_columns)}
FROM 
    CTEDefMining"""

    # create the report
    report_display_name = f"(DEFICIENCIES) GLOBAL"
    report_internal_name = get_internal_name(report_display_name)

    createReports(
        config=config,
        projectname=project_name,
        reports=[
            Report(
                displayName=report_display_name,
                internalName=report_internal_name,
                querySyntax=sql_statement,
                description=f"Deficiency Mining Report for  project '{project_name}'",
            )
        ],
    )

    createRules(
        config=config,
        projectname=project_name,
        rules=[
            Rule(
                displayName="Global",
                ruleSourceInternalName=report_internal_name,
                ruleGroup="01 Global",
                description=f"Deficiency Mining Rule for project '{project_name}'",
            )
        ],
    )

    return case_statement_specific, status_conditions


def _create_report_for_migman(
    config: Config,
    project_name: str,
    postfix: str,
    columns_in_file: list[str],
    database: list[MigMan],
    case_statement_specific: str,
    status_conditions: str,
    joins: dict[str, dict[str, str]],
) -> None:
    """
    Creates a report for MigMan containing valid data.

    Args:
        config (Config): Configuration object.
        project_name (str): Name of the project.
        postfix (str): Postfix for the project.
        columns_in_file (list[str]): List of columns in the data file.
        database (list[MigMan]): List of MigMan database entries.
        case_statement_specific (str): Case statement for deficiency messages.
        status_conditions (str): Conditions for status checks.
        joins (dict[str, dict[str, str]]): Join conditions for the report.
    """
    sql_statement = f"""WITH CTEDefMining AS (
    SELECT
        {',\n\t\t'.join([x.nemo_internal_name for x in database if x.project == project_name and x.postfix == postfix and x.nemo_display_name in columns_in_file])}
        ,LTRIM({case_statement_specific},CHAR(10)) AS DEFICIENCY_MININNG_MESSAGE
        ,CASE 
            WHEN {status_conditions} THEN 'check'
            ELSE 'ok'
        END AS STATUS
    FROM
        $schema.$table"""

    for join in joins:
        sql_statement += f"""
LEFT JOIN
\t$schema.SHARED_NAIGENT genius_{join}
ON  
\t    genius_{join}.CLASSIFICATION = '{joins[join]["CLASSIFICATION"]}'
\tAND genius_{join}.VALUE          = {join}"""

    sql_statement += f"""       
)
SELECT
    {',\n\t'.join([f"{x.nemo_internal_name} as \"{x.header_section_label}\"" for x in database if x.project == project_name and x.postfix == postfix and x.nemo_display_name in columns_in_file])}
FROM 
    CTEDefMining
WHERE
    STATUS = 'ok'
    """

    # create the report
    report_display_name = f"(MigMan) All records with no message"
    report_internal_name = get_internal_name(report_display_name)

    createReports(
        config=config,
        projectname=project_name,
        reports=[
            Report(
                displayName=report_display_name,
                internalName=report_internal_name,
                querySyntax=sql_statement,
                description=f"MigMan export with valid data for project '{project_name}'",
            )
        ],
    )


def _create_report_for_customer(
    config: Config,
    project_name: str,
    postfix: str,
    columns_in_file: list[str],
    database: list[MigMan],
    case_statement_specific: str,
    status_conditions: str,
    joins: dict[str, dict[str, str]],
) -> None:
    """
    Creates a report for customers containing invalid data.

    Args:
        config (Config): Configuration object.
        project_name (str): Name of the project.
        postfix (str): Postfix for the project.
        columns_in_file (list[str]): List of columns in the data file.
        database (list[MigMan]): List of MigMan database entries.
        case_statement_specific (str): Case statement for deficiency messages.
        status_conditions (str): Conditions for status checks.
        joins (dict[str, dict[str, str]]): Join conditions for the report.
    """
    sql_statement = f"""WITH CTEDefMining AS (
    SELECT
        {',\n\t\t'.join([x.nemo_internal_name for x in database if x.project == project_name and x.postfix == postfix and x.nemo_display_name in columns_in_file])}
        ,LTRIM({case_statement_specific},CHAR(10)) AS DEFICIENCY_MININNG_MESSAGE
        ,CASE 
            WHEN {status_conditions} THEN 'check'
            ELSE 'ok'
        END AS STATUS
    FROM
        $schema.$table"""

    for join in joins:
        sql_statement += f"""
LEFT JOIN
\t$schema.SHARED_NAIGENT genius_{join}
ON  
\t    genius_{join}.CLASSIFICATION = '{joins[join]["CLASSIFICATION"]}'
\tAND genius_{join}.VALUE          = {join}"""

    sql_statement += f"""       
)
SELECT
    DEFICIENCY_MININNG_MESSAGE,
    {',\n\t'.join([f"{x.nemo_internal_name} as \"{x.header_section_label}\"" for x in database if x.project == project_name and x.postfix == postfix and x.nemo_display_name in columns_in_file])}
FROM 
    CTEDefMining
WHERE
    STATUS <> 'ok'
"""

    # create the report
    report_display_name = f"(Customer) All records with message"
    report_internal_name = get_internal_name(report_display_name)

    createReports(
        config=config,
        projectname=project_name,
        reports=[
            Report(
                displayName=report_display_name,
                internalName=report_internal_name,
                querySyntax=sql_statement,
                description=f"export invalid data for project '{project_name}'",
            )
        ],
    )
