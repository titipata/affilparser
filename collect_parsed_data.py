from lxml import etree
from itertools import chain
from unidecode import unidecode

def list_xml_path(path_dir):
    """
    List full xml path under given directory
    Parameters
    ----------
    path_dir: str, path to directory that contains xml or nxml file
    Returns
    -------
    path_list: list, list of xml or nxml file from given path
    """
    fullpath = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(path_dir)) for f in fn]
    path_list = [folder for folder in fullpath if os.path.splitext(folder)[-1] in ('.nxml', '.xml')]
    return path_list

def read_xml(path):
    """
    Parse tree from given XML path
    """
    try:
        tree = etree.parse(path)
    except:
        try:
            tree = etree.fromstring(path)
        except Exception as e:
            print("Error: it was not able to read a path, a file-like object, or a string as an XML")
            raise
    return tree

def get_parsed_affiliation(path, tag='addr-line'):
    aff_list = []
    tree = etree.parse(path)
    for aff in tree.xpath('//aff'):
        tree_string = etree.tostring(aff)
        tags = [e.tag for e in aff.getchildren()]
        if tag in tags:
            aff_list.append(tree_string)
    return aff_list

def get_affil_tuple(affiliation_string):
    affil_text = []
    affil_tree = etree.fromstring(affiliation_string)
    tags = [e.tag for e in affil_tree.getchildren()]
    if 'country' in tags:
        for e in affil_tree.iterchildren():
            if e.tag != 'sup' and e.tag != 'label' and e.text is not None and 'country' in tags:
                affil_text.append((e.tag, e.text))
        return affil_text
    else:
        return None


if __name__ == '__main__':
    paths = list_xml_path('/pubmed_oa/') # give path to Pubmed OA
    paths_rdd = spark.sparkContext.parallelize(paths, numSlices=1000)
    affiliation_strings = paths_rdd.flatMap(lambda x: get_parsed_affiliation(x, tag='addr-line')).filter(lambda x: x is not None).collect()
    affiliation_country = [get_affil_tuple(affiliation_string) for affiliation_string in affiliation_strings] # tuple with country
    affiliation_country = [a for a in affiliation_country if a is not None]
