from wowool.diagnostic import Diagnostics
from wowool.analysis_formatter.app_id import APP_ID
from wowool.document.analysis.document import AnalysisDocument
from wowool.annotation import Concept
from wowool.string import canonicalize
import logging
from typing import Dict
from wowool.utility.apps.decorators import (
    exceptions_to_diagnostics,
    requires_analysis,
)
from wowool.native.core.analysis import get_byte_offset

logger = logging.getLogger(__name__)


def get_begin_offset(concept: Concept, document: AnalysisDocument):
    return concept.begin_offset


def get_end_offset(concept: Concept, document: AnalysisDocument):
    return concept.end_offset


def get_begin_byte_offset(concept: Concept, document: AnalysisDocument):
    return get_byte_offset(document.analysis, concept.begin_offset)


def get_end_byte_offset(concept: Concept, document: AnalysisDocument):
    return get_byte_offset(document.analysis, concept.end_offset)


def get_uri(concept: Concept, document: AnalysisDocument):
    return concept.uri


def get_literal(concept: Concept, document: AnalysisDocument):
    return concept.literal


def get_stem(concept: Concept, document: AnalysisDocument):
    return concept.stem


def get_attributes(concept: Concept, document: AnalysisDocument):
    return concept.attributes


def get_canonical(concept: Concept, document: AnalysisDocument):
    return concept.canonical


available_functions = {
    "begin_offset": get_begin_offset,
    "end_offset": get_end_offset,
    "begin_byte_offset": get_begin_byte_offset,
    "end_byte_offset": get_end_byte_offset,
    "uri": get_uri,
    "literal": get_literal,
    "stem": get_stem,
    "canonical": get_canonical,
    "attributes": get_attributes,
}


def convert_formatter(formatter):
    table = []
    for key, name in formatter.items():
        if name in available_functions:
            table.append([key, available_functions[name]])
        else:
            raise RuntimeError(f"Unknown Formatter name: [{name}]")
    return table


class AnalysisFormatter:
    ID = APP_ID
    docs = """# Analysys Formatter
The application is used to define a custom format for the results of a document analysis.

## Configuration
    
    - formatter (object[string:string]) – A dictionary describing the custom format of the analysis. The first string is the name of the key in your custom result object. The second is one of the strings from the pre-defined set of keywords for the available data

### Pre-defined Keywords

The following keywords can be used within the custom format:

    **uri**: URI of the concept
    **canonical**: canonical for of the concept if any otherwise it will return the literal
    **literal**: literal representation of the concept
    **stem**: stem representation of the concept
    **attributes**: attributes attach to the concept
    **begin_offset**: begin offset in the text
    **end_offset**: end offset in the text
    **begin_byte_offset**: begin byte offset in the utf-8 input
    **end_byte_offset**: end byte offset in the utf-8 input

## Example
```json
{"formatter": {"uri":"uri","bo":"begin_offset","s":"stem"}}
```

"""

    def __init__(self, formatter: Dict[str, str] = {}):
        self.format = convert_formatter(formatter)

    @exceptions_to_diagnostics
    @requires_analysis
    def __call__(
        self, document: AnalysisDocument, diagnostics: Diagnostics
    ) -> AnalysisDocument:
        """
        :param document:  The document we want to format the concepts from.
        :type document: AnalysisDocument

        :returns: The custom formatted result.
        """

        results = []

        for concept in document.concepts():
            out = {}
            for key, function in self.format:
                out[key] = function(concept, document)
            results.append(out)

        document.add_results(self.ID, results)
        return document
