#!/usr/bin/env python
# Based on: https://github.com/antonio-ramadas/aoc-to-markdown

import os
import re

import requests
from bs4 import BeautifulSoup
from slugify import slugify


def get_dir_with_digits(root_dir: str) -> list[str]:
    return [dir for dir in os.listdir(root_dir) if dir.isdigit()]


def html_tags_to_markdown(tag, is_first_article):
    children = tag.find_all(recursive=False)

    if tag.name != "code":
        for child in children:
            html_tags_to_markdown(child, is_first_article)

    if tag.name == "h2":
        style = "#" if is_first_article else "##"
        tag.insert_before(f"{style} ")
        tag.insert_after("\n\n")
        tag.unwrap()
    elif tag.name == "p":
        tag.insert_after("\n")
        tag.unwrap()
    elif tag.name == "em":
        style = "**" if tag.has_attr("class") and tag["class"] == "star" else "*"
        tag.insert_before(style)
        tag.insert_after(style)
        tag.unwrap()
    elif tag.name == "a":
        tag.insert_before("[")
        tag.insert_after(f']({tag["href"]})')
        tag.unwrap()
    elif tag.name == "span":
        tag.insert_before("*")
        tag.insert_after("*")
        tag.unwrap()
    elif tag.name == "ul":
        tag.unwrap()
    elif tag.name == "li":
        tag.insert_before(" - ")
        tag.insert_after("\n")
        tag.unwrap()
    elif tag.name == "code":
        if "\n" in tag.text:
            tag.insert_before("```\n")
            tag.insert_after("\n```")
        else:
            tag.insert_before("`")
            tag.insert_after("`")
        tag.unwrap()
    elif tag.name == "pre":
        tag.insert_before("")
        tag.insert_after("\n")
        tag.unwrap()
    elif tag.name == "article":
        pass
    else:
        raise ValueError(f"Missing condition for tag: {tag.name}")


def get_readme(year: str, day: str) -> str:
    url = f"https://adventofcode.com/{year}/day/{day}"
    response = requests.get(url, cookies={"session": os.getenv("AOC_SESSION")})
    if response.status_code != 200:
        raise ValueError(
            f"Querying the url {url} resulted in status code {response.status_code} with the following " f"text: {response.text}")

    soup = BeautifulSoup(response.text, features="html.parser")
    articles = soup.body.main.find_all("article", recursive=False)
    content = ""

    for i, article in enumerate(articles):
        html_tags_to_markdown(article, i == 0)
        content += "".join([tag.string for tag in article.contents if tag.string])

    return content


def get_input(year: str, day: str) -> str:
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    response = requests.get(url, cookies={"session": os.getenv("AOC_SESSION")})
    if response.status_code != 200:
        raise ValueError(
            f"Querying the url {url} resulted in status code {response.status_code} with the following " f"text: {response.text}")
    return response.text


def file_conains_part_two(readme_path: str):
    with open(readme_path) as f:
        lines = f.readlines()
        r = any(line.find("--- Part Two ---") >= 0 for line in lines)
        return r


TEMPLATE = """
from aoclib import *

def get_data(filename: str) -> list[str]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()
    return lines
    
def q1(filename:str) -> int:
    data = get_data(filename)
    
    return 0
    
def q2(filename: str) -> int:
    data = get_data(filename)
    
    return 0
    
def test_q1():
    assert q1("test.txt") == 0

def test_q2():
    assert q2("test.txt") == 0

"""


def sync_dir(root_dir: str):
    for year in get_dir_with_digits(root_dir):
        for day in get_dir_with_digits(os.path.join(root_dir, year)):
            readme_path = os.path.join(root_dir, year, day, "README.md")
            if not os.path.exists(readme_path) or not file_conains_part_two(readme_path):
                print(f"Downloading README for {year}/{day}")
                readme = get_readme(year, day)
                with open(readme_path, "w") as f:
                    f.write(readme)

                title = re.search(r": (.+) ---", readme.splitlines()[0])[1]
                test_name_path = os.path.join(root_dir, year, day, f"{slugify(title, separator='_')}_test.py")
                if not os.path.exists(test_name_path):
                    with open(test_name_path, "w") as f:
                        f.write(f"# {title} - https://adventofcode.com/{year}/day/{day}\n")
                        f.write(TEMPLATE)

            data_path = os.path.join(root_dir, year, day, "data.txt")
            if not os.path.exists(data_path):
                print(f"Downloading DATA for {year}/{day}")
                with open(data_path, "w") as f:
                    f.write(get_input(year, day))


if __name__ == "__main__":
    sync_dir(".")
