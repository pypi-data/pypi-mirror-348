import pytest

from nemo_library import NemoLibrary
from datetime import datetime

from nemo_library.utils.utils import FilterType, FilterValue
from tests.testutils import getNL

META_PROJECT_NAME = "Business Processes"


def test_create():
    nl = getNL()
    nl.MetaDataCreate(
        projectname=META_PROJECT_NAME,
        filter="(C)",
        filter_type=FilterType.STARTSWITH,
        filter_value=FilterValue.DISPLAYNAME,
    )


def test_load():
    nl = getNL()
    nl.MetaDataLoad(
        projectname=META_PROJECT_NAME,
        filter="(C)",
        filter_type=FilterType.STARTSWITH,
        filter_value=FilterValue.DISPLAYNAME,
    )


def test_delete():
    nl = getNL()
    nl.MetaDataDelete(
        projectname=META_PROJECT_NAME,
        filter="(C)",
        filter_type=FilterType.STARTSWITH,
        filter_value=FilterValue.DISPLAYNAME,
    )
