#!/usr/bin/env python
# Based on: https://github.com/antonio-ramadas/aoc-to-markdown

import os

import requests
from bs4 import BeautifulSoup


def get_dir_with_digits(root_dir: str) -> list[str]:
    return [dir for dir in os.listdir(root_dir) if dir.isdigit()]


def html_tags_to_markdown(tag, is_first_article):
    children = tag.find_all(recursive=False)

    if tag.name != 'code':
        for child in children:
            html_tags_to_markdown(child, is_first_article)

    if tag.name == 'h2':
        style = '#' if is_first_article else '##'
        tag.insert_before(f'{style} ')
        tag.insert_after('\n\n')
        tag.unwrap()
    elif tag.name == 'p':
        tag.insert_after('\n')
        tag.unwrap()
    elif tag.name == 'em':
        style = '**' if tag.has_attr('class') and tag['class'] == 'star' else '*'
        tag.insert_before(style)
        tag.insert_after(style)
        tag.unwrap()
    elif tag.name == 'a':
        tag.insert_before('[')
        tag.insert_after(f']({tag["href"]})')
        tag.unwrap()
    elif tag.name == 'span':
        tag.insert_before('*')
        tag.insert_after('*')
        tag.unwrap()
    elif tag.name == 'ul':
        tag.unwrap()
    elif tag.name == 'li':
        tag.insert_before(' - ')
        tag.insert_after('\n')
        tag.unwrap()
    elif tag.name == 'code':
        if '\n' in tag.text:
            tag.insert_before('```\n')
            tag.insert_after('\n```')
        else:
            tag.insert_before('`')
            tag.insert_after('`')
        tag.unwrap()
    elif tag.name == 'pre':
        tag.insert_before('')
        tag.insert_after('\n')
        tag.unwrap()
    elif tag.name == 'article':
        pass
    else:
        raise ValueError(f'Missing condition for tag: {tag.name}')


def get_readme(year: int, day: int) -> str:
    url = f"https://adventofcode.com/{year}/day/{day}"
    response = requests.get(url, cookies={'session': os.getenv("AOC_SESSION")})
    if response.status_code != 200:
        raise ValueError(f"Querying the url {url} resulted in status code {response.status_code} with the following "
                         f"text: {response.text}")

    soup = BeautifulSoup(response.text, features="html.parser")
    articles = soup.body.main.findAll('article', recursive=False)
    content = ''

    for i, article in enumerate(articles):
        html_tags_to_markdown(article, i == 0)
        content += ''.join([tag.string for tag in article.contents])

    return content


def sync_dir(root_dir: str):
    for year in get_dir_with_digits(root_dir):
        for day in get_dir_with_digits(os.path.join(root_dir, year)):
            readme_path = os.path.join(root_dir, year, day, "README.md")
            if os.path.exists(readme_path):
                print(f"Skip {year}/{day} - README.md already exists")
                continue
            print(f"Downloading README for {year}/{day}")
            readme = get_readme(year, day)
            with open(readme_path, "w") as f:
                f.write(readme)


if __name__ == "__main__":
    sync_dir(".")
