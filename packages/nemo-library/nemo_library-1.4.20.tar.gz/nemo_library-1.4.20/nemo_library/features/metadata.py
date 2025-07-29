from collections import defaultdict
import copy
from dataclasses import fields, is_dataclass
import json
import logging
from pathlib import Path
import re
from typing import Type, TypeVar
from nemo_library.features.focus import focusMoveAttributeBefore
from nemo_library.features.nemo_persistence_api import (
    _deserializeMetaDataObject,
    createApplications,
    createAttributeGroups,
    createAttributeLinks,
    createDefinedColumns,
    createDiagrams,
    createMetrics,
    createPages,
    createReports,
    createRules,
    createSubProcesses,
    createTiles,
    deleteApplications,
    deleteAttributeGroups,
    deleteAttributeLinks,
    deleteDefinedColumns,
    deleteDiagrams,
    deleteMetrics,
    deletePages,
    deleteReports,
    deleteRules,
    deleteSubprocesses,
    deleteTiles,
    getApplications,
    getAttributeGroups,
    getAttributeLinks,
    getDefinedColumns,
    getDiagrams,
    getImportedColumns,
    getMetrics,
    getPages,
    getRules,
    getSubProcesses,
    getTiles,
)
from nemo_library.features.nemo_persistence_api import (
    getDependencyTree,
)
from nemo_library.features.nemo_persistence_api import (
    getReports,
)
from nemo_library.model.application import Application
from nemo_library.model.attribute_group import AttributeGroup
from nemo_library.model.attribute_link import AttributeLink
from nemo_library.model.defined_column import DefinedColumn
from nemo_library.model.dependency_tree import DependencyTree
from nemo_library.model.diagram import Diagram
from nemo_library.model.metric import Metric
from nemo_library.model.pages import Page
from nemo_library.model.report import Report
from nemo_library.model.rule import Rule
from nemo_library.model.tile import Tile
from nemo_library.model.subprocess import SubProcess
from nemo_library.utils.config import Config
from nemo_library.utils.utils import FilterType, FilterValue
import uuid

__all__ = ["MetaDataLoad", "MetaDataDelete", "MetaDataCreate"]

T = TypeVar("T")


def MetaDataLoad(
    config: Config,
    projectname: str,
    filter: str = "*",
    filter_type: FilterType = FilterType.STARTSWITH,
    filter_value: FilterValue = FilterValue.DISPLAYNAME,
) -> None:

    functions = {
        "applications": getApplications,
        "attributegroups": getAttributeGroups,
        "attributelinks": getAttributeLinks,
        "definedcolumns": getDefinedColumns,
        "diagrams": getDiagrams,
        "metrics": getMetrics,
        "pages": getPages,
        "reports": getReports,
        "rules": getRules,
        "tiles": getTiles,
        "subprocesses": getSubProcesses,
    }

    for name, func in functions.items():
        logging.info(f"load {name} from NEMO")
        data = func(
            config=config,
            projectname=projectname,
            filter=filter,
            filter_type=filter_type,
            filter_value=filter_value,
        )

        _export_data_to_json(config, name, data)


def MetaDataDelete(
    config: Config,
    projectname: str,
    filter: str = "*",
    filter_type: FilterType = FilterType.STARTSWITH,
    filter_value: FilterValue = FilterValue.DISPLAYNAME,
) -> None:

    get_functions = {
        "applications": getApplications,
        "attributegroups": getAttributeGroups,
        "attributelinks": getAttributeLinks,
        "definedcolumns": getDefinedColumns,
        "diagrams": getDiagrams,
        "metrics": getMetrics,
        "pages": getPages,
        "reports": getReports,
        "rules": getRules,
        "subprocesses": getSubProcesses,
        "tiles": getTiles,
    }

    delete_functions = {
        "subprocesses": deleteSubprocesses,
        "applications": deleteApplications,
        "pages": deletePages,
        "tiles": deleteTiles,
        "metrics": deleteMetrics,
        "definedcolumns": deleteDefinedColumns,
        "attributelinks": deleteAttributeLinks,
        "attributegroups": deleteAttributeGroups,
        "diagrams": deleteDiagrams,
        "reports": deleteReports,
        "rules": deleteRules,
    }

    for name, func in get_functions.items():
        logging.info(f"delete {name} from NEMO")
        data = func(
            config=config,
            projectname=projectname,
            filter=filter,
            filter_type=filter_type,
            filter_value=filter_value,
        )

        objects_to_delete = [obj.id for obj in data]

        delete_functions[name](config=config, **{name: objects_to_delete})


def MetaDataCreate(
    config: Config,
    projectname: str,
    filter: str = "*",
    filter_type: FilterType = FilterType.STARTSWITH,
    filter_value: FilterValue = FilterValue.DISPLAYNAME,
) -> None:

    # load data from model (JSON)
    logging.info(f"load model from JSON files in folder {config.get_metadata()}")
    applications_model = _load_data_from_json(
        config,
        "applications",
        Application,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    attributegroups_model = _load_data_from_json(
        config,
        "attributegroups",
        AttributeGroup,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    attributelinks_model = _load_data_from_json(
        config,
        "attributelinks",
        AttributeLink,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    definedcolumns_model = _load_data_from_json(
        config,
        "definedcolumns",
        DefinedColumn,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    diagrams_model = _load_data_from_json(
        config,
        "diagrams",
        Diagram,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    metrics_model = _load_data_from_json(
        config,
        "metrics",
        Metric,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    pages_model = _load_data_from_json(
        config,
        "pages",
        Page,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    reports_model = _load_data_from_json(
        config,
        "reports",
        Report,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    rules_model = _load_data_from_json(
        config,
        "rules",
        Rule,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    subprocesses_model = _load_data_from_json(
        config,
        "subprocesses",
        SubProcess,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    tiles_model = _load_data_from_json(
        config,
        "tiles",
        Tile,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )

    # load data from NEMO
    logging.info(f"load model from NEMO files from project {projectname}")
    applications_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getApplications,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    attributegroups_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getAttributeGroups,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    attributelinks_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getAttributeLinks,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    definedcolumns_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getDefinedColumns,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    diagrams_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getDiagrams,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    metrics_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getMetrics,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    pages_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getPages,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    reports_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getReports,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    tiles_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getTiles,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    rules_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getRules,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    subprocesses_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getSubProcesses,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )

    # reconcile data
    deletions: dict[str, list[T]] = {}
    updates: dict[str, list[T]] = {}
    creates: dict[str, list[T]] = {}

    logging.info(f"reconcile both models")
    for key, model_list, nemo_list in [
        ("applications", applications_model, applications_nemo),
        ("attributegroups", attributegroups_model, attributegroups_nemo),
        ("attributelinks", attributelinks_model, attributelinks_nemo),
        ("definedcolumns", definedcolumns_model, definedcolumns_nemo),
        ("diagrams", diagrams_model, diagrams_nemo),
        ("metrics", metrics_model, metrics_nemo),
        ("pages", pages_model, pages_nemo),
        ("reports", reports_model, reports_nemo),
        ("tiles", tiles_model, tiles_nemo),
        ("rules", rules_model, rules_nemo),
        ("subprocesses", subprocesses_model, subprocesses_nemo),
    ]:
        nemo_list_cleaned = copy.deepcopy(nemo_list)
        nemo_list_cleaned = _clean_fields(nemo_list_cleaned)

        deletions[key] = _find_deletions(model_list, nemo_list)
        updates[key] = _find_updates(model_list, nemo_list_cleaned)
        creates[key] = _find_new_objects(model_list, nemo_list)

    # Start with deletions
    logging.info(f"start deletions")
    delete_functions = {
        "applications": deleteApplications,
        "pages": deletePages,
        "tiles": deleteTiles,
        "metrics": deleteMetrics,
        "definedcolumns": deleteDefinedColumns,
        "attributegroups": deleteAttributeGroups,
        "attributelinks": deleteAttributeLinks,
        "diagrams": deleteDiagrams,
        "rules": deleteRules,
        "reports": deleteReports,
        "subprocesses": deleteSubprocesses,
    }

    for key, delete_function in delete_functions.items():
        if deletions[key]:
            objects_to_delete = [data_nemo.id for data_nemo in deletions[key]]
            delete_function(config=config, **{key: objects_to_delete})

    # Now do updates and creates in a reverse  order
    logging.info(f"start creates and updates")
    create_functions = {
        "attributegroups": createAttributeGroups,
        "reports": createReports,
        "rules": createRules,
        "diagrams": createDiagrams,
        "attributelinks": createAttributeLinks,
        "definedcolumns": createDefinedColumns,
        "metrics": createMetrics,
        "tiles": createTiles,
        "pages": createPages,
        "applications": createApplications,
        "subprocesses": createSubProcesses,
    }

    for key, create_function in create_functions.items():
        # create new objects first
        if creates[key]:
            create_function(
                config=config, projectname=projectname, **{key: creates[key]}
            )
        # now the changes
        if updates[key]:
            create_function(
                config=config, projectname=projectname, **{key: updates[key]}
            )


def MetaDataAutoResolveApplications(
    config: Config,
    projectname: str,
    filter: str = "*",
    filter_type: FilterType = FilterType.STARTSWITH,
    filter_value: FilterValue = FilterValue.DISPLAYNAME,
):
    """
    Build the attribute groups model by combining the models of applications, pages,
    diagrams, metrics, and defined columns.

    ASSUMPTION: model and NEMO are in sync (no deletions or updates)
    """

    logging.info(f"load model from JSON files in folder {config.get_metadata()}")
    attributegroups_model = (
        []
    )  # empty dictionary to hold the attribute groups to be created
    applications_model = _load_data_from_json(config, "applications", Application)
    pages_model = _load_data_from_json(config, "pages", Page)
    metrics_model = _load_data_from_json(config, "metrics", Metric)
    definedcolumns_model = _load_data_from_json(config, "definedcolumns", DefinedColumn)
    diagrams_model = _load_data_from_json(config, "diagrams", Diagram)
    attribute_groups_metrics = defaultdict(set)
    attributelinks_model = (
        []
    )  # empty dictionary to hold the attribute links to be created

    # build attribute groups tree first
    logging.info(f"build attribute groups tree")

    # start with root node
    root = AttributeGroup(
        internalName="optimate",
        displayName="Optimate",
        displayNameTranslations={"de": "Optimate", "en": "Optimate"},
        parentAttributeGroupInternalName=None,
        order="00",
    )
    attributegroups_model.append(root)

    # add a group for each application
    for app in applications_model:
        attributegroups_model.append(
            AttributeGroup(
                internalName=app.internalName,
                displayName=app.displayName,
                displayNameTranslations=app.displayNameTranslations,
                parentAttributeGroupInternalName="optimate",
            )
        )

        # add a group for each page
        for page in app.pages:

            page_ref = None
            for page_search in pages_model:
                if page_search.internalName == page.page:
                    page_ref = page_search
                    break
            if page_ref:
                attributegroups_model.append(
                    AttributeGroup(
                        internalName=page_ref.internalName,
                        displayName=page_ref.displayName,
                        displayNameTranslations=page_ref.displayNameTranslations,
                        parentAttributeGroupInternalName=app.internalName,
                    )
                )

                # add a group for each diagram
                for visual in page_ref.visuals:
                    if visual.type == "Diagram":
                        diagram_ref = None
                        for diagram_search in diagrams_model:
                            if diagram_search.internalName == visual.content:
                                diagram_ref = diagram_search
                                break
                        if diagram_ref:
                            attributegroups_model.append(
                                AttributeGroup(
                                    internalName=diagram_ref.internalName,
                                    displayName=diagram_ref.displayName,
                                    displayNameTranslations=diagram_ref.displayNameTranslations,
                                    parentAttributeGroupInternalName=page_ref.internalName,
                                )
                            )
                            for value in diagram_ref.values:
                                attribute_groups_metrics[diagram_ref.internalName].add(
                                    value.column
                                )
                    elif visual.type == "Metric":
                        attribute_groups_metrics[page_ref.internalName].add(
                            visual.content
                        )

    def assignOrder(parent: AttributeGroup):
        index = 0
        for attribute_group in attributegroups_model:
            if attribute_group.parentAttributeGroupInternalName == parent.internalName:
                attribute_group.order = f"{index:02}"
                index += 1
                assignOrder(attribute_group)

    assignOrder(root)
    attribute_groups_metrics = {k: list(v) for k, v in attribute_groups_metrics.items()}

    # move metrics to the right attribute group
    logging.info(f"move metrics to the right attribute group")
    for metric in metrics_model:
        # find metric in attribute groups
        attribute_group = None
        for key, value in attribute_groups_metrics.items():
            if metric.internalName in value:
                attribute_group = key
                break
        if attribute_group:
            metric.parentAttributeGroupInternalName = attribute_group

    # now we use the dependency tree to find the right attribute group for the defined and exported columns
    # load metrics from NEMO to get the id of them. This is needed to get the dependency tree
    logging.info(f"get dependency tree for metrics")
    metrics_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getMetrics,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    dependency_tree = {
        metric.internalName: _collect_node_objects(d)
        for metric in metrics_nemo
        if (d := getDependencyTree(config=config, id=metric.id)) is not None
    }
    importedcolumns_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getImportedColumns,
        filter="*",
        filter_type=filter_type,
        filter_value=filter_value,
    )

    # move defined columns to the right attribute group
    logging.info(f"move defined columns to the right attribute group")
    for metric_internal_name, values in dependency_tree.items():

        # find metric in model
        metric = None
        for metric_search in metrics_model:
            if metric_search.internalName == metric_internal_name:
                metric = metric_search
                break
        if not metric:
            logging.error(f"metric {metric_internal_name} not found in model")
            continue

        # move defined columns to the right attribute group
        for element in values:
            if element.nodeType == "DefinedColumn":
                # find defined column in model
                defined_column = None
                for defined_column_search in definedcolumns_model:
                    if defined_column_search.internalName == element.nodeInternalName:
                        defined_column = defined_column_search
                        break
                if not defined_column:
                    logging.error(
                        f"defined column {element.nodeInternalName} not found in model"
                    )
                    continue

                defined_column.parentAttributeGroupInternalName = (
                    metric.parentAttributeGroupInternalName
                )
            elif element.nodeType == "ExportedColumn":
                # find exported column in model
                imported_column = None
                for imported_column_search in importedcolumns_nemo:
                    if imported_column_search.internalName == element.nodeInternalName:
                        imported_column = imported_column_search
                        break
                if not imported_column:
                    logging.error(
                        f"exported column {element.nodeInternalName} not found in model"
                    )
                    continue
                attributelinks_model.append(
                    AttributeLink(
                        sourceAttributeId=imported_column.id,
                        parentAttributeGroupInternalName=metric.parentAttributeGroupInternalName,
                        displayNameTranslations={
                            "de": imported_column.displayNameTranslations.get("de", ""),
                            "en": imported_column.displayNameTranslations.get("en", ""),
                        },
                        displayName=imported_column.displayName,
                        internalName=f"{filter}_{imported_column.internalName}_{uuid.uuid4()}".replace(
                            "-", "_"
                        ),
                    )
                )
    # export the data to JSON finally
    export = {
        "attributegroups": attributegroups_model,
        "metrics": metrics_model,
        "definedcolumns": definedcolumns_model,
    }
    for name, data in export.items():
        _export_data_to_json(config, name, data)

    # it does not make sense to save the attribute links to JSON, because they
    # contain the id of the imported columns.
    # So we create them directly in NEMO

    # Remove duplicates from attributelinks_model
    unique_links = {}
    for link in attributelinks_model:
        key = (link.sourceAttributeId, link.parentAttributeGroupInternalName)
        if key not in unique_links:
            unique_links[key] = link
    attributelinks_model = list(unique_links.values())

    createAttributeLinks(
        config=config, projectname=projectname, attributelinks=attributelinks_model
    )


def _collect_node_objects(tree: DependencyTree) -> list[str]:
    elements = [tree]
    for dep in tree.dependencies:
        elements.extend(_collect_node_objects(dep))
    return elements


def _fetch_data_from_nemo(
    config: Config,
    projectname: str,
    func,
    filter: str = "*",
    filter_type: FilterType = FilterType.STARTSWITH,
    filter_value: FilterValue = FilterValue.DISPLAYNAME,
):
    return func(
        config=config,
        projectname=projectname,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )


def _load_data_from_json(
    config,
    file: str,
    cls: Type[T],
    filter: str = "*",
    filter_type: FilterType = FilterType.STARTSWITH,
    filter_value: FilterValue = FilterValue.DISPLAYNAME,
) -> list[T]:
    """
    Loads JSON data from a file and converts it into a list of DataClass instances,
    handling nested structures recursively.
    """
    path = Path(config.get_metadata()) / f"{file}.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    def match_filter(value: str, filter: str, filter_type: FilterType) -> bool:
        """Applies the given filter to the value."""
        if filter == "*":
            return True
        elif filter_type == FilterType.EQUAL:
            return value == filter
        elif filter_type == FilterType.STARTSWITH:
            return value.startswith(filter)
        elif filter_type == FilterType.ENDSWITH:
            return value.endswith(filter)
        elif filter_type == FilterType.CONTAINS:
            return filter in value
        elif filter_type == FilterType.REGEX:
            return re.search(filter, value) is not None
        return False

    # Apply filter to the data
    filtered_data = [
        item
        for item in data
        if match_filter(item.get(filter_value.value, ""), filter, filter_type)
    ]

    return [_deserializeMetaDataObject(item, cls) for item in filtered_data]


def _find_deletions(model_list: list[T], nemo_list: list[T]) -> list[T]:
    model_keys = {obj.internalName for obj in model_list}
    return [obj for obj in nemo_list if obj.internalName not in model_keys]


def _find_updates(model_list: list[T], nemo_list: list[T]) -> list[T]:
    updates = []
    nemo_dict = {getattr(obj, "internalName"): obj for obj in nemo_list}
    for model_obj in model_list:
        key = getattr(model_obj, "internalName")
        if key in nemo_dict:
            nemo_obj = nemo_dict[key]
            if is_dataclass(model_obj) and is_dataclass(nemo_obj):
                differences = {
                    attr.name: (
                        getattr(model_obj, attr.name),
                        getattr(nemo_obj, attr.name),
                    )
                    for attr in fields(model_obj)
                    if getattr(model_obj, attr.name) != getattr(nemo_obj, attr.name)
                }

            if differences:
                for attrname, (new_value, old_value) in differences.items():
                    logging.info(f"{attrname}: {old_value} --> {new_value}")
                updates.append(model_obj)

    return updates


def _find_new_objects(model_list: list[T], nemo_list: list[T]) -> list[T]:
    nemo_keys = {getattr(obj, "internalName") for obj in nemo_list}
    return [obj for obj in model_list if getattr(obj, "internalName") not in nemo_keys]


def _export_data_to_json(config: Config, file: str, data):
    data = _clean_fields(data)
    path = Path(config.get_metadata()) / f"{file}.json"
    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            [element.to_dict() for element in data], file, indent=4, ensure_ascii=True
        )


def _clean_fields(data):
    for element in data:
        element.id = ""
        element.tenant = ""
        element.projectId = ""
        element.tileSourceID = ""

        if isinstance(element, Diagram):
            for value in element.values:
                value.id = ""

        elif isinstance(element, Page):
            for visual in element.visuals:
                visual.id = ""

    return data
