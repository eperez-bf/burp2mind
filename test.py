#!/usr/bin/env python3
import os
import sys

def build_tree(root, uri_list):
    tree = {}
    for uri in uri_list:
        if uri.startswith(root):
            path, _, query = uri[len(root):].partition("?")
            parts = path.strip("/").split("/")
            current = tree
            for part in parts:
                if part not in current:
                    current[part] = {}
                current = current[part]
            if query:
                query_params = query.split("&")
                if len(query_params) == 1:
                    key, value = query_params[0].split("=")
                    current[key] = {"value": value}
                else:
                    current["query"] = {}
                    for param in query_params:
                        key, value = param.split("=")
                        current["query"][key] = {"value": value}
    return tree

def traverse_tree(node, level=0):
    result = []
    if isinstance(node, str):
        result.append(node)
    elif isinstance(node, dict):
        for name, child in node.items():
            prefix = "  " * level
            if level == 0:
                prefix += "- "
            else:
                prefix += "+ "
            if "value" in child:
                result.append(prefix + name + "=" + child["value"])
            elif "query" in child:
                result.append(prefix + name)
                result.extend(traverse_tree(child["query"], level+1))
            else:
                result.append(prefix + name)
                result.extend(traverse_tree(child, level+1))
    return result

def save_to_file(root, lines, filename):
    with open(filename, "w") as f:
        f.write("# " + root + "\n")
        for line in lines:
            f.write(line + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python markdown.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, "r") as f:
        uri_list = [line.strip() for line in f]

    root = uri_list[0]
    tree = build_tree(root, uri_list)
    output = traverse_tree(tree)
    save_to_file(root, output, output_file)
