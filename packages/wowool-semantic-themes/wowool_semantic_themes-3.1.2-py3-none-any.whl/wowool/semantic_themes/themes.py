#!/usr/bin/python3
# ex :  python3 -m wowool.themes -f ~/dev/csv2_test/net.csv

import json
from collections import defaultdict
from wowool.document.analysis.document import AnalysisDocument
from wowool.annotation import Token, Concept, Sentence
from dataclasses import dataclass, field
from typing import Any, Optional
import logging
from wowool.semantic_themes.app_id import APP_ID
from wowool.diagnostic import Diagnostics, Diagnostic, DiagnosticType


logger = logging.getLogger(__name__)

URI = "uri"


APP_ID_TOPIC_IDENTIFIER = "wowool_topics"


class Theme:

    ID = APP_ID

    def __init__(self):
        self.relevancy = 0
        self.normalized_relevancy = 0
        self.uris = set()
        self.words = set()
        self.count = 0

    def __iter__(self):
        yield from {
            "relevancy": f"{self.normalized_relevancy:.0f}",
            "debug": {
                "count": self.count,
                "words": list(self.words),
                "uris": list(self.uris),
            },
        }.items()

    def dict(self, debug_info):
        if not debug_info:
            return {
                "relevancy": int(f"{self.normalized_relevancy:.0f}"),
            }
        else:
            return {
                "relevancy": int(f"{self.normalized_relevancy:.0f}"),
                "debug": {
                    "count": self.count,
                    "words": list(self.words),
                    "uris": list(self.uris),
                },
            }

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()


uri_of_interest = set(["Theme", "Event"])


class FilterUriOfInterset:
    def __call__(self, concept):
        return concept.uri in uri_of_interest


def filter_uri_of_interest(concept):
    return concept.uri in uri_of_interest


@dataclass
class DocumentMemento:

    nrof_sentence: int
    percentage: float = 0.2
    sentence_relevancy: float = 1.0
    sentence_idx: int = 0
    already_added_short_descriptions: Any = field(init=False)
    topics: Any = field(init=False)
    total_relevancy: float = 1.0
    # topic_to_relevancy : Dict[str,float] = field(default_factory=dict)

    def __post_init__(self):
        self.already_added_short_descriptions = set()
        self.topics = {}

    def next(self):
        if self.sentence_idx >= (self.nrof_sentence * self.percentage) and self.sentence_idx < (
            self.nrof_sentence * (1 - self.percentage)
        ):  # noqa
            self.sentence_relevancy = 0.5
        else:
            self.sentence_relevancy = 1.0
        self.sentence_idx += 1


def _outer(input_list, percent):
    retval = input_list[: int(len(input_list) * percent)]
    retval += input_list[0 - int(len(input_list) * percent) :]
    return retval


def _normalize_relevancy(results, dm):
    max_theme_relevancy = 0
    for k, _theme in results.items():
        max_theme_relevancy = max(max_theme_relevancy, _theme.relevancy)

    for k, _theme in results.items():
        _theme.normalized_relevancy = (_theme.relevancy * 100) / max_theme_relevancy


def _exclude_concept_with_description(concept, uri_desc):
    if "exclude" in uri_desc:
        excluders = uri_desc["exclude"]
        for key, value in excluders.items():
            if key in concept.attributes and concept.attributes[key][0] in value:
                logger.debug(f"""exclude filter: {concept.uri}:{concept.literal} is in {key}:{value}""")
                return True
    return False


class Themes:
    """
    The object used to collect the themes information.

    :param config: the configuration object.
    :type dict: str

    .. literalinclude:: english_themes_call.py
        :caption: topic_init.py

    """

    ID = APP_ID

    DEFAULT_CONFIG = {
        "collect": {
            "Company": {"short_descriptions": False, URI: False, "exclude": {"sector": ["media"]}},
            "Event": {"short_descriptions": False},
        },
        "attributes": ["sector", "theme"],
    }

    debug = False

    def __init__(
        self,
        count: Optional[int] = 5,
        threshold: Optional[int] = 0,
        collect: Optional[dict] = None,
        attributes: Optional[list] = None,
        debug_info: Optional[bool] = False,
        mapping: Optional[dict] = None,
    ):
        self.debug_info = debug_info
        self.count = count
        self.threshold = threshold
        self.mapping = mapping

        if collect is not None:
            self.collect_desc = collect
        else:
            self.collect_desc = Themes.DEFAULT_CONFIG["collect"]

        if attributes is not None:
            self.attribute_to_collect = attributes
        else:
            self.attribute_to_collect = Themes.DEFAULT_CONFIG["attributes"]

        # assert len(self.attribute_to_collect), "You need to specify the attributes to collect in your json config file"

    def _exclude_concept(self, concept):
        return _exclude_concept_with_description(concept, self.collect_desc[concept.uri])

    def _rename_theme_attribute(self, key):
        if self.mapping is None:
            return key
        if key in self.mapping:
            return self.mapping[key]

    def _add_attribute_theme(self, themes_to_add, concept, key):
        if key in concept.attributes:
            for themes in concept.attributes[key]:
                for theme in [theme.strip().lower() for theme in themes.split("|")]:
                    thn = self._rename_theme_attribute(theme)
                    if thn:
                        themes_to_add.add(thn)

    def _collect(self, concept: Concept, dm):  # noqa
        # print(concept, concept.literal)
        themes_to_add = set()
        # add the default key if any.
        # for att keys like "theme", "sector" collect the values.
        for key in self.attribute_to_collect:
            self._add_attribute_theme(themes_to_add, concept, key)

        # add the keys for the given concepts or the uri it self
        if concept.uri in self.collect_desc:
            uri_desc = self.collect_desc[concept.uri]
            if URI in uri_desc:
                if uri_desc[URI]:
                    if self._exclude_concept(concept):
                        return
                    themes_to_add.add(concept.canonical)
            # "collect": { "Person": { "short_descriptions": true, URI: false, "attributes": [ "position" ] },
            if "attributes" in uri_desc:
                requested_attributes = uri_desc["attributes"]
                for key in requested_attributes:
                    self._add_attribute_theme(themes_to_add, concept, key)

        lwr_literal = concept.literal.lower()
        for theme in themes_to_add:
            _theme = self._categories[theme]
            _theme.count += 1
            _theme.relevancy += dm.sentence_relevancy

            # add extra relevancy in case we find it in the topic collection.
            if dm.topic_to_relevancy:
                if lwr_literal in dm.topic_to_relevancy:
                    logger.debug(f"add topic relevancy: {lwr_literal=} r:{dm.topic_to_relevancy[lwr_literal]}")
                    _theme.relevancy += dm.topic_to_relevancy[lwr_literal]

            dm.total_relevancy += _theme.relevancy
            # for debugging purpose we keep track of the uri with the stem.
            _theme.uris.add(f"{concept.uri}:{concept.stem}")
            _theme.words.add(f"{concept.stem}".lower())
            logger.debug(f"add {theme} {concept.uri},{concept.literal} {dm.sentence_relevancy} , {_theme}")

    def _requires_short_description_info(self, uri, dm) -> bool:
        value = (
            True
            if uri in self.collect_desc
            and "short_descriptions" in self.collect_desc[uri]
            and self.collect_desc[uri]["short_descriptions"] is True
            else False
        )
        return value

    def process(
        self,
        sentences: list[Sentence],
        topics: None | list = None,
        document_id: str = "none",
        diagnostics: Diagnostics | None = None,
    ) -> list:
        self._categories = defaultdict(Theme)
        dm = DocumentMemento(len(sentences))

        dm.topics = topics
        if dm.topics:
            dm.topic_to_relevancy = {item["name"]: item["relevancy"] / 100 for item in dm.topics}
            logger.debug(f"topics: {dm.topic_to_relevancy}")
        else:
            dm.topic_to_relevancy = {}
            if diagnostics:
                diagnostics.add(
                    Diagnostic(document_id, f"{self.ID}: Could not use topics for better results add 'topics.app'", DiagnosticType.Warning)
                )

        # sentences = [s for s in document.analysis]
        for sentence in sentences:
            dm.next()
            sentence_tokens = 0
            for token in Token.iter(sentence):
                sentence_tokens += 1

            for concept in Concept.iter(sentence):
                self._collect(concept, dm)

            for concept in Concept.iter(sentence):
                logger.debug(f"{concept.uri}, {concept.literal}")

        _normalize_relevancy(self._categories, dm)
        sorted_categories = sorted(self._categories.items(), key=lambda x: (x[1].relevancy, x[0]), reverse=True)
        sorted_categories = [
            {"name": theme[0], **theme[1].dict(self.debug_info)}
            for theme in sorted_categories
            if theme[1].normalized_relevancy >= self.threshold
        ][: self.count]

        return sorted_categories

    def __call__(self, document: AnalysisDocument) -> AnalysisDocument:  # noqa
        """
        Callable object to perform the semantic theme calculation.
        """
        if not isinstance(document, AnalysisDocument) or document.analysis is None:
            raise ValueError("The document.analysis not filled in yet. You need to run the required language and domains")
        diagnostics = Diagnostics()
        try:

            topics = document.results(APP_ID_TOPIC_IDENTIFIER) if document.has_results(APP_ID_TOPIC_IDENTIFIER) else None
            sorted_categories = self.process(document.analysis.sentences, topics, document_id=document.id, diagnostics=diagnostics)
            if len(sorted_categories) == 0:
                if document.metadata and "concepts" in document.metadata:
                    if "Theme" not in document.metadata["concepts"]:
                        diagnostics.add(
                            Diagnostic(
                                document.id,
                                f"{self.ID} : No 'Theme' concept found. Try adding the 'semantic-theme' Domain to your pipeline ",
                                DiagnosticType.Warning,
                            )
                        )

            document.add_results(self.ID, sorted_categories)

        except Exception as ex:
            diagnostics.add(Diagnostic(document.id, f"{self.ID} : {ex}", DiagnosticType.Critical))

        if diagnostics:
            document.add_diagnostics(self.ID, diagnostics)

        return document
