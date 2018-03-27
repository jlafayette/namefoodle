import json
import urllib.request

import click
from bs4 import BeautifulSoup


@click.command()
@click.argument("outfile", type=click.File('w'))
def scrape_harry_potter_spells(outfile):
    quote_page = "http://harrypotter.wikia.com/wiki/List_of_spells"
    with urllib.request.urlopen(quote_page) as response:
        html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    spells = list()

    # find all the pages
    pages = soup.findAll("div", attrs={"class": "tabbertab"})
    for page in pages:
        items = page.findChildren(recursive=False)[0].findChildren(recursive=False)
        print("items: {}".format(len(items)))
        spell = dict()
        for item in items:
            headline = item.find("span", attrs={"class": "mw-headline"})
            if headline is not None:
                # save previous spell
                if spell:
                    spells.append(spell)
                spell = dict()

                # start new spell
                spell['name'] = headline.text
                continue

            for dd in item.findAll("dd"):
                if "Pronunciation:" in dd.text:
                    spell["pronunciation"] = dd.text[len("Pronunciation:"):].strip()
                    break

    json.dump(spells, outfile, indent=4, separators=(",", ": "), sort_keys=True)


if __name__ == '__main__':
    scrape_harry_potter_spells()
