import os

from extensions import extensions_list
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash


def add_extensions_to_navigation_bar(extensions_list):
    with open('templates/base.html', 'w') as f:
        with open('templates/base_original.html', 'r') as fo:
            original_content = fo.read()
            f.seek(0, 0)
            f.write(original_content)

    with open('templates/base.html', 'r+') as f:
        contents = f.readlines()
        for i, extension in enumerate(extensions_list):
            name = extension.extension_name
            content = """
            <li>
                  <a href="/extension/""" + name + """"class="nav-link text-white">
                    <svg class="bi me-2" width="16" height="16"><use xlink:href="#speedometer2"></use></svg>
                    """ + name + """
                  </a>
                </li>
            """
            contents.insert(32 + i, content)
        f.seek(0, 0)
        f.writelines(contents)


def build_extension_html(extension):
    with open('templates/extension_' + extension.extension_name + '.html', 'w') as f:
        contents = ["""{% extends "base.html" %}\n{%block body%}\n<link rel="stylesheet" href="../static/style/extension.css">\n<script type="text/javascript" src="../static/script/extension.js"></script>\n<div class="tab">"""]
        for tab in extension.tabs:
            name = "".join(tab.tab_name.split(' '))
            content = """\n<button class="tablinks" onclick="openTab(event,'""" + name + """')">""" + name + """</button>"""
            contents.append(content)
        contents.append('</div>')
        for tab in extension.tabs:
            name = "".join(tab.tab_name.split(' '))
            action = tab.route
            tab_content = ("""\n<div id="{0}" class="tabcontent">"""+
                           """\n<form id="{0}Form" target="{0}Frame"  action="{1}" method="POST">"""+
                           """\n<input type="text" name="extension" value="True" />"""+
                           """\n</form>"""+

                           """<iframe name="{0}Frame" src="#" width="1200" height="650">
               Your browser does not support inline frames.
            </iframe>
            
            <script>
             $(document).ready(function(){{
             var {0}form= document.getElementById("{0}Form");
             {0}form.style.display = "none";
             {0}form.submit();
            }});
            </script>
            </div>""").format(name, action)
            contents.append(tab_content)
        contents.append('{%endblock%}')
        f.writelines(contents)


def build_extensions_html(extensions_list):
    for file in os.listdir('templates'):
        if file.startswith('extension_'):
            os.remove(os.path.join('templates', file))
    for extension in extensions_list:
        build_extension_html(extension)


add_extensions_to_navigation_bar(extensions_list)
build_extensions_html(extensions_list)
