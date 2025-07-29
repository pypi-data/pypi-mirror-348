#!/usr/bin/python3
import sys
import json
from wowool.topic_identifier import TopicIdentifier
from wowool.native.core import Pipeline, Engine
from wowool.io.console import console
from os import pathsep
from wowool.utility.default_arguments import make_document_collection


def parse_arguments(argv):
    """
    This is the EyeOnText topic identification tool.

    If you want to make your own topic model, please run first the toc tool

    Example: topic_identifier -f ~/corpus/english -l english
    """
    from .argument_parser import ArgumentParser

    parser = ArgumentParser()
    args = parser.parse_args(argv)
    return args


def main(sys_args=None):
    """
    Command line tool for the entity mapper
    """
    if sys_args == None:
        args = parse_arguments(sys.argv[1:])
    else:
        args = parse_arguments(sys_args)

    json_format = args.json

    stripped = None
    if args.cleanup:
        stripped = lambda s: "".join(i for i in s if 31 < ord(i) < 127 or ord(i) == 0xD or ord(i) == 0xA)

    if args.lxware:
        engine = Engine(lxware=args.lxware)
        paths = args.lxware.split(pathsep)
    else:
        from wowool.native.core.engine import default_engine

        engine = default_engine()
        paths = engine.lxware

    pipeline = Pipeline(args.pipeline, engine=engine, paths=paths)

    topic_identifier = TopicIdentifier(
        language=pipeline.language,
        count=args.count,
        threshold=args.threshold,
        topic_model=args.topic_model,
        engine=engine,
    )
    collection = make_document_collection(text=args.input, file=args.file)

    if args.verbose:
        print(f"Building model for:{len(collection)} documents ...")
    # first add al documents to the topic model
    for ip in collection:
        if args.verbose:
            print(f"adding {ip.id}")
        doc = pipeline(ip)
        topic_identifier.add(doc)

    topic_identifier.build()

    for ip in collection:
        print(f"process: {ip.id}", file=sys.stderr)
        doc = topic_identifier(ip)
        topics = doc.results(TopicIdentifier.ID)
        if topics:
            if json_format:
                if args.raw_print:
                    print(json.dumps(topics))
                else:
                    console.print(topics)
            else:
                for topic in topics:
                    console.print(f""" - {topic["name"]}: {topic["relevancy"]}""")
        else:
            print("No topics found")


if __name__ == "__main__":
    main()
