from flask import Blueprint
from extensions import extensions

def modify_base_html(extensions):
    with open('templates/base.html', 'w') as f:
        with open('templates/base_original.html', 'r') as fo:
            original_content = fo.read()
            f.seek(0, 0)
            f.write(original_content)

    with open('templates/base.html', 'r+') as f:
        contents = f.readlines()
        for i, extension in enumerate(extensions):
            content = """
            <li>
                  <a href="{{route_weather}}" class="nav-link text-white">
                    <svg class="bi me-2" width="16" height="16"><use xlink:href="#speedometer2"></use></svg>
                    """ + extension.extension_name + """
                  </a>
                </li>
            """
            contents.insert(32+i, content)
        f.seek(0, 0)
        f.writelines(contents)

extensions_blueprint = Blueprint('extensions', __name__)

for extension in extensions:
    @extensions.route('/'+extension.extension_name)
    def extension_route():
        pass
