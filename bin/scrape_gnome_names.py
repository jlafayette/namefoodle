#!/usr/bin/env python

import json
import certifi

import click
import requests
from bs4 import BeautifulSoup


@click.command()
@click.argument("outfile", type=click.File('w'))
def scrape_gnome_names(outfile):
    url = "https://www.dndbeyond.com/characters/races/gnome"
    response = requests.get(url, verify=certifi.where())
    print(type(response))
    print(response)
    print(response.encoding)
    print(response.headers['content-type'])

    soup = BeautifulSoup(response.text, "html.parser")
    name_data = dict()

    container = soup.find("div", attrs={"class": "content-container"})
    paragraph_counter = 0
    name_items = list()
    for item in container.findChildren("p"):
        if paragraph_counter:
            print(paragraph_counter)
            name_items.append(item)
            paragraph_counter += 1
            if paragraph_counter > 4:  # there are 4 paragraphs of names
                break
        else:
            try:
                if "Gnomes love names" in item.text:
                    print("found it!")
                    paragraph_counter = 1
            except AttributeError:
                pass

    for item in name_items:
        section, comma_sep_list = item.text.split(": ")
        name_data[section] = comma_sep_list.split(", ")

    json.dump(name_data, outfile, indent=4, separators=(",", ": "), sort_keys=True)


if __name__ == '__main__':
    scrape_gnome_names()
