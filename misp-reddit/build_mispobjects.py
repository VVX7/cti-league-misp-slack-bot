import json
import sys
import glob

from os import walk

#arguments misp-objects directory misp_objects.py file

def build_objects_list(objects_dir):
    objects_dir_list = glob.glob(f'{objects_dir}/*/definition.json')
    return objects_dir_list

def determine_class_names(objects_dir):
    dirs = []
    for (dirpath, dirnames, filenames) in walk(objects_dir):
        dirs.extend(dirnames)
        break

    classes = []
    for dir in dirs:
        class_name = dir.title()
        class_name = class_name.replace('-', '')
        classes.append({'dir' : dir, 'class_name' : class_name})
    return classes

def map_definition_to_class(objects_dir):
    definition_map = []
    definition_files = build_objects_list(objects_dir)
    classes = determine_class_names(objects_dir)

    for definition_file in definition_files:
        for class in classes:
            if class['dir'] in definition_file:
                rec = {'definition_file' : definition_file, 'class_name' : class['class_name']}
                definition_map.append(rec)
    return definition_map


def load_definition(definition_file):
    f = open(definition_file)
    definition = json.load(f)
    f.close()
    return definition

def create_misp_objects_file(objects_file):
    f=open(objects_file, 'w')
    f.write('from pymisp.tools.abstracgneerator import AbstractMISPObjectGenerator\n\n')
    return f

def write_class_definition(f, class_name, misp_object_name, definition):
    f.write(f'class {class_name}(AbstractMISPObjectGenerator):\n')
    f.write('\tdef __init__(self, parameters: dict, strict: bool = True, standalone: bool = True, **kwargs):\n')
    f.write(f'\t\tsuper(RedditAccount, self).__init__({misp_object_name}, strict=strict, standalone=standalone, **kwargs)\n')
    f.write('\t\tself._parameters = parameters\n\t\tself.generate_attributes()\n\n')



def main(argv):
    if len(argv) < 2:
        printf('Usage build_mispobjects.py <misp-objects directory> <misp_objects.py file>')
    objects_dir=argv[0]
    objects_file = argv[1]
