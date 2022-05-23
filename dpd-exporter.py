#!/usr/bin/env python3
# coding: utf-8

import json
import typer
import zipfile
from datetime import datetime
from timeis import timeis, yellow, green, line

from generate_html_and_json import generate_html_and_json
from helpers import copy_goldendict, get_resource_paths


app = typer.Typer()

RSC = get_resource_paths()

@app.command()
def run_generate_html_and_json(generate_roots: bool = True):
    generate_html_and_json(generate_roots)

@app.command()
def run_generate_goldendict(move_to_dest: bool = True):
    """Generate a Stardict-format .zip for GoldenDict."""

    rsc = get_resource_paths()

    # importing Simsapa here so other commands don't have to load it and its numerous dependencies
    from simsapa.app.stardict import export_words_as_stardict_zip, ifo_from_opts, DictEntry

    print(f"{timeis()} {yellow}generate goldendict")
    print(f"{timeis()} {line}")

    print(f"{timeis()} {green}reading json")
    with open(rsc['gd_json_path'], "r") as f:
        gd_data_read = json.load(f)

    print(f"{timeis()} {green}parsing json")
    def item_to_word(x):
        return DictEntry(
            word=x["word"],
            definition_html=x["definition_html"],
            definition_plain=x["definition_plain"],
            synonyms=x["synonyms"],
        )

    words = list(map(item_to_word, gd_data_read))

    ifo = ifo_from_opts(
        {
            "bookname": "Digital Pāḷi Dictionary",
            "author": "Bodhirasa",
            "description": "Digital Pāḷi Dictionary",
            "website": "https://digitalpalidictionary.github.io",
        }
    )

    print(f"{timeis()} {green}writing goldendict")
    export_words_as_stardict_zip(words, ifo, rsc['output_stardict_zip_path'], rsc['icon_path'])

    zipfilepath = rsc['output_stardict_zip_path']
    with zipfile.ZipFile(zipfilepath, 'a') as zipf:
        source_path = rsc['icon_bmp_path']
        destination = 'dpd/android.bmp'
        zipf.write(source_path, destination)

    if move_to_dest:
        copy_goldendict(rsc['output_stardict_zip_path'], rsc['output_share_dir'])
    

def main():
    # Process cli with typer.
    app()

if __name__ == "__main__":
    main()
