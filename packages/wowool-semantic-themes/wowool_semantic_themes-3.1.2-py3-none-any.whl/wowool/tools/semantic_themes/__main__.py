#!/usr/bin/python3
import sys
from wowool.native.core import PipeLine
from wowool.semantic_themes import Themes
from wowool.semantic_themes.app_id import APP_ID, APP_ID_TOPIC_IDENTIFIER
from pathlib import Path
from wowool.io.console import console
from wowool.utility.diagnostics import print_diagnostics
import json
from wowool.utility.default_arguments import make_document_collection


def parse_arguments(argv):
    """
    This is the EyeOnText topic identification tool.

    If you want to make your own topic model, please run first the toc tool

    Example: topics -f ~/corpus/english -l english
    """
    from wowool.tools.semantic_themes.argument_parser import ArgumentParser

    parser = ArgumentParser()
    args = parser.parse_args(argv)
    return args


def _print_extract(document):
    print("-" * 80, file=sys.stderr)
    document_id = document.id
    print("docid:", document.id, file=sys.stderr)
    if Path(document_id).exists():
        with open(document_id) as fh:
            data = fh.read(1000)
            sys.stderr.write(data)
            if len(data) >= 1000:
                sys.stderr.write("...")
    else:
        print(document.text, file=sys.stderr)
    print("-" * 80, file=sys.stderr)


def print_categories(categories, debug=True):
    console.print("[h1]Semantic-Themes:[/h1]")
    for item in categories:
        category = item["name"]
        del item["name"]
        console.print(
            f""" '{category}' : <default>{item["relevancy"]}<default>""", end=""
        )
        del item["relevancy"]
        if debug:
            console.print(f""": {item['debug']}""", end="")
        console.print("")


def print_topics(topics):
    console.print("[h1]Topics:[/h1]")
    for topic in topics:
        console.print(f""" '{topic["name"]}': {topic['relevancy']}""")


def expand_pipeline(pipeline_str):
    from wowool.config import config as wowool_config

    if wowool_config.get_language(pipeline_str):
        return f"""{pipeline_str},semantic-theme,topics.app"""
    else:
        return pipeline_str


def main(sys_args=None): # noqa
    """
    Command line tool for the entity mapper
    """
    if sys_args is None:
        kwargs = dict(parse_arguments(sys.argv[1:])._get_kwargs())
    else:
        kwargs = dict(parse_arguments(sys_args)._get_kwargs())

    debug = True if "debug" in kwargs and kwargs["debug"] else False
    json_format = kwargs["json"]

    theme_config = {}
    if kwargs["config"]:
        with open(kwargs["config"]) as fh:
            theme_config = json.load(fh)

    pipeline_str = expand_pipeline(kwargs["pipeline"])
    if debug:
        print(f"pipeline: {pipeline_str}", file=sys.stderr)

    if debug:
        theme_config["debug_info"] = debug

    pipeline = PipeLine(pipeline_str)
    theme_app = Themes(
        **theme_config,
        threshold=kwargs["threshold"],
        count=kwargs["count"],
    )

    collection = make_document_collection(**kwargs)
    for doc in collection:
        if debug:
            _print_extract(doc)
        doc = pipeline(doc)
        doc = theme_app(doc)
        if not kwargs["raw_print"]:
            print_diagnostics(doc, console, file=sys.stderr)

        themes = doc.results(APP_ID)
        if themes:
            topics = doc.results(APP_ID_TOPIC_IDENTIFIER)
            if not json_format:
                if topics:
                    print_topics(topics)
                print_categories(themes, debug)
            else:
                json_result = {"themes": themes}
                if topics:
                    json_result["topics"] = topics
                if kwargs["raw_print"]:
                    print(json.dumps(json_result))
                else:
                    console.print_json(json_result)

        else:
            console.print("[red]No themes have been found.[/red]", file=sys.stderr)


if __name__ == "__main__":
    main()
