from distutils.dir_util import copy_tree
import json
import os
import pathlib
import sys
from jinja2 import Environment, FileSystemLoader, select_autoescape

def static(output_dir):
    input_dir = os.getcwd()
    input_dir = pathlib.Path(input_dir)
    static_dir = input_dir/'static'
    if not static_dir.exists():
        return
    
    copy_tree(str(static_dir), str(output_dir))


def directory():
    input_dir = os.getcwd()
    input_dir = pathlib.Path(input_dir)
    output_dir = input_dir/'html'
    output_dir = pathlib.Path(output_dir)
    i = 0

    try:
        output_dir.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        print('Directory already exists')
        sys.exit(1)

    static(output_dir)
    return output_dir


def parse_json():
    input_dir = os.getcwd()
    input_dir = pathlib.Path(input_dir)
    template_dir = input_dir/'templates'
    i = 0

    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template_list, context_list = ([] for i in range(2))

    with open(input_dir/'config.json', encoding='utf-8') as file:
        json_data = json.load(file)
        for data in json_data:
            template_list.append(data['template'])
            context_list.append(data['context'])
    return template_list, context_list, env


def setup():
    output_dir = directory()
    template_list, context_list, env = parse_json()

    for template, context in zip(template_list, context_list):
        jinja_template = env.get_template(template)
        html_template = jinja_template.render(context)
        output_path = output_dir/'index.html'

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(html_template)


def driver():
    setup()

# 
def main():
    driver()


if __name__ == "__main__":
    main()