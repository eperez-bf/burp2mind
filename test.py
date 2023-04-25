#!/usr/bin/env python3
import os

def build_tree(root, uri_list):
    tree = {}
    for uri in uri_list:
        if uri.startswith(root):
            path = uri[len(root):].lstrip("/")
            parts = path.split("/")
            current = tree
            for part in parts:
                if part not in current:
                    current[part] = {}
                current = current[part]
    return tree

def traverse_tree(node, level=0):
    result = []
    for name, child in node.items():
        result.append(("    " * level) + name)
        result.extend(traverse_tree(child, level+1))
    return result

def save_to_file(lines, filename):
    with open(filename, "w") as f:
        for line in lines:
            f.write(line + "\n")

if __name__ == "__main__":
    with open("sitelist.raw", "r") as f:
        uri_list = [line.strip() for line in f]
    root = uri_list[0]
    tree = build_tree(root, uri_list)
    tree_lines = traverse_tree(tree)
    save_to_file(tree_lines, "sitelist.textbundle")
    save_to_file(tree_lines, "sitelist.md")
    save_to_file(tree_lines, "sitelist.opml")
