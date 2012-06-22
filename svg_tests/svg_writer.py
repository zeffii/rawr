"""TEST 01: Injecting a .template with the appropriate junk"""

output_filename = "output.svg"

# data to inject -------------------------------------
def get_gdata():
  return_val = """\
  <g
     inkscape:label="Layer 1"
     inkscape:groupmode="layer"
     id="layer1">
    <path
       style="fill:none;stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
       d="M 402.85714,175.21933 137.14286,706.6479"
       id="path2985"
       inkscape:connector-curvature="0" />
    <path
       style="fill:none;stroke:#000000;stroke-width:6;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;opacity:1;stroke-miterlimit:4;stroke-dasharray:none"
       d="m 594.28571,526.6479 -300,234.28571"
       id="path2987"
       inkscape:connector-curvature="0" />
    <path
       style="fill:none;stroke:#000000;stroke-width:3;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;stroke-miterlimit:4;stroke-dasharray:none"
       d="M 520,895.21933 142.85714,849.50504"
       id="path2989"
       inkscape:connector-curvature="0" />
    <path
       style="fill:none;stroke:#000000;stroke-width:35;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;stroke-miterlimit:4;stroke-dasharray:none"
       d="M 129.29953,339.19449 76.771593,468.49401"
       id="path3759"
       inkscape:path-effect="#path-effect3761"
       inkscape:original-d="M 129.29953,339.19449 76.771593,468.49401"
       inkscape:connector-curvature="0" />
  </g>"""
  return return_val.split('\n')

value_dict = {
        "file_name": ["\"%s\"" % output_filename],
        "width": ["width=\"744.09448819\""],
        "height": ["height=\"1052.3622047\""],
        "gdata": get_gdata()
        }


## print utility
def coolprint(input):
  print("\033[32;1m%s\033[0m" % input)
  

# cache the template
def get_template_content(template_name):
  template_file = open(template_name)
  template_content = [line for line in template_file]
  template_file.close()
  return template_content


# check for injection token
def line_has_injectable(line, value_dict):
  for key in value_dict.keys():
    if "{{"+key+"}}" in line:
      return True, key
  return None, None


# inject into the template, write as new file
def write_to_file(output_file, line, key):
  coolprint("Injecting {{%s}}" % key)
  for thing in value_dict[key]:
    line_to_write = line.replace("{{"+key+"}}", thing)
    output_file.write(line_to_write)


# delegation function
def inject(template_name, **value_dict):
  template_content = get_template_content(template_name)

  output_file = open(output_filename, 'w')
  for line in template_content:
    injectable, key = line_has_injectable(line, value_dict)
    if injectable:
      write_to_file(output_file, line, key)
    else:
      output_file.write(line)

  output_file.close()



inject(template_name="example.template", **value_dict)


