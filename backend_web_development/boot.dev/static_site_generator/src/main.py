import os, shutil
from pathlib import Path
from markdown_blocks import markdown_to_html_node


def main():
    copy_from_static()
    generate_pages_recursive("content", "template.html", "public")


def extract_title(markdown):
    for i in markdown.split("\n"):
        i = i.strip()
        if i != "" and i != " ":
            if i[0] == "#" and i[1] == " ":
                return i[2:]
    raise Exception("h1 header needed")


def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)


def copy_from_static():
    delete_from_destination("public")
    os.mkdir("public")
    recurse_to_copy_r("static", "public")


def recurse_to_copy_r(source, destination):
    for i in os.listdir(source):
        path = os.path.join(source, i)
        if os.path.isfile(path):
            shutil.copy(path, destination)
        else:
            new_path = os.path.join(destination, i)
            os.mkdir(new_path)
            recurse_to_copy_r(path, new_path)


def delete_from_destination(destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)


if __name__ == "__main__":
    main()
