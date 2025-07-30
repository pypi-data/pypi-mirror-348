import xml.etree.ElementTree as ET
import os
import rdflib
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, OWL
from pyshacl import validate
import argparse
from .utils import recursiceCheck, built_in_types, create_formatted_label
import time
from datetime import datetime


class XSDtoRDF:    
    def __init__(self, abbreviations_file=None):
        """
        Initialize the XSDtoRDF class that combines SHACL and SKOS functionalities
        
        Args:
            abbreviations_file: Optional path to a file containing abbreviations (one per line)
        """
        # Load custom abbreviations if provided
        self.custom_abbreviations = None
        if abbreviations_file:
            from .utils import load_abbreviations_from_file
            self.custom_abbreviations = load_abbreviations_from_file(abbreviations_file)
            
        # Common namespaces
        self.era = rdflib.Namespace('http://data.europa.eu/949/')
        self.rdfSyntax = rdflib.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
        self.rdfsNS = rdflib.Namespace('http://www.w3.org/2000/01/rdf-schema#')
        self.xsdNS = rdflib.Namespace('http://www.w3.org/2001/XMLSchema#')
        self.xsdTargetNS = rdflib.Namespace('http://example.com/')
        self.NS = rdflib.Namespace('http://example.com/')
        self.owlNS = rdflib.Namespace('http://www.w3.org/2002/07/owl#')
        self.dctNS = rdflib.Namespace('http://purl.org/dc/terms/')
        self.cc = rdflib.Namespace('http://creativecommons.org/ns#')
        
        # SHACL specific namespaces
        self.shaclNS = rdflib.Namespace('http://www.w3.org/ns/shacl#')
        
        # SKOS specific namespaces
        self.skosNS = rdflib.Namespace('http://www.w3.org/2004/02/skos/core#')
        self.dctNS = rdflib.Namespace('http://purl.org/dc/terms/')
        self.ccNS = rdflib.Namespace('http://creativecommons.org/ns#')
        self.cc_license = URIRef("http://data.europa.eu/eli/dec_impl/2017/863/oj")
        
        # Common variables
        self.type_list = built_in_types()
        self.xsdNSdict = dict()
        self.processed_files = []
        self.xsd_file = None
        self.BASE_PATH = None
        self.root = None
        self.language = "en" #default language
        
        # SHACL specific variables
        self.SHACL = Graph()
        self.shapes = []
        self.extensionShapes = []
        self.enumerationShapes = []
        self.choiceShapes = []
        self.order_list = []
        self.backUp = None
        
        # SKOS specific variables
        self.SKOS = Graph()  # Graph for SKOS content
        self.concepts = []
        self.concept_schemes = {}  # Dictionary to track concept schemes and their concepts
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        
        # OWL specific variables
        self.OWL_Graph = Graph()

    def initialize_skos_graph(self):
        """Initialize a new RDF Graph with namespace bindings for SKOS"""
        graph = Graph()
        graph.bind('era', self.era)
        graph.bind('skos', self.skosNS)
        graph.bind('rdf', self.rdfSyntax)
        graph.bind('rdfs', self.rdfsNS)
        graph.bind('xsd', self.xsdNS)
        graph.bind('', self.NS)
        graph.bind('dct', self.dctNS)
        graph.bind('cc', self.ccNS)
        return graph

    def isSimpleComplex(self,xsd_element,xsd_type=None):
        """A function to determine whether the type of element is SimpleType or ComplexType"""
        if xsd_element == None:
            exception = f"Element {xsd_element} not found in the XSD file."
            raise ValueError(exception)
        if xsd_type == None:
            xsd_type = xsd_element.get("type")
        if xsd_type == None:
            for child in xsd_element.findall("./"):
                if "complexType" in child.tag:
                    if child.attrib.get("mixed") == "true":
                        return "mixed"
                    for sub_child in child:
                        if "simpleContent" in sub_child.tag:
                            return "simpleContent"
                    return 1
                elif "simpleType" in child.tag:
                    return 0
            return 0
        elif xsd_type.split(":")[-1] in self.type_list:
            return 0 #built-in type
        else:
            xsd_type = xsd_type.split(":")[-1]
            elements = self.root.findall(f".//*[@name='{xsd_type}']", self.xsdNSdict)
            # can't combine both conditions as xmltree doesn't support the full xpath syntax
            # sometimes, some elements are named after their type, we need to find the element that contains the type definition
            # that means we need to find the complexType or the simpleType element with that name
            child = next((e for e in elements if ("complexType" in e.tag or "simpleType" in e.tag)), None)
            if child is None:
                return 0
            if "complexType" in child.tag:
                if child.attrib.get("mixed") == "true":
                    return "mixed"
                for sub_child in child:
                    if "simpleContent" in sub_child.tag:
                        return "simpleContent"
                return 1
            elif "simpleType" in child.tag:
                return 0
            else:
                # Complex content
                return 1

    def find_parent(self, element, parent):
        """Find the parent element in the XML tree"""
        for child in parent:
            if child is element:
                return parent
            if len(child) > 0:
                result = self.find_parent(element, child)
                if result is not None:
                    return result
        return None

    def parse_language(self):
        """Parse the language from the XSD metadata."""
        if self.root is not None:
            language_element = self.root.find(".//{http://purl.org/dc/terms/}language")
            if language_element is not None and language_element.text:
                self.language = language_element.text.strip()

    def process_enumeration_for_skos(self, parent_element):
        """Process an element with enumeration values for SKOS concepts"""
        # Get the name of the type/element containing the enumeration
        name = parent_element.get("name")
        if not name:
            return None

        # Check for enumeration restrictions
        enums = parent_element.findall('.//xs:enumeration', namespaces={"xs": "http://www.w3.org/2001/XMLSchema"})
        if not enums:
            return None

        # Create a concept scheme for this enumeration type
        concept_scheme_uri = URIRef(self.NS + name + "Scheme")
        scheme_doc = None

        # Get documentation for the concept scheme
        annotation = parent_element.find("./{*}annotation")
        if annotation is not None:
            doc = annotation.find("./{*}documentation")
            if doc is not None and doc.text:
                scheme_doc = doc.text.strip()

        # Initialize or update dictionary for this concept scheme
        if name not in self.concept_schemes:
            self.concept_schemes[name] = {
                'uri': concept_scheme_uri,
                'doc': scheme_doc,
                'concepts': []
            }

        # Process each enumeration value as a SKOS concept
        concepts = []
        for enum in enums:
            value = enum.get("value")
            if value:
                concept_uri = URIRef(self.NS + name + "_" + value.replace(" ", "_"))
                concept_def = None

                # Process documentation for each enumeration value if available
                for annotation in enum.findall(".//{*}annotation"):
                    for doc in annotation.findall(".//{*}documentation"):
                        if doc.text:
                            concept_def = doc.text.strip()

                # Add concept to the concept scheme dictionary
                self.concept_schemes[name]['concepts'].append({
                    'uri': concept_uri,
                    'value': value,
                    'definition': Literal(concept_def, lang=self.language) if concept_def else None
                })

                # Keep track of created concepts
                self.concepts.append(concept_uri)
                concepts.append(concept_uri)

        return {
            'scheme_uri': concept_scheme_uri,
            'concepts': concepts
        }

    def transRestriction(self, tag, value, subject=None):
        """Process XSD restrictions and map them to SHACL constraints"""
        if subject == None:
            subject = self.shapes[-1]

        if "type" in tag or "restriction" in tag:
            if ((":" in value) and (value.split(":")[1] in self.type_list)):
                p = self.shaclNS.datatype
                o = self.xsdNS[value.split(":")[1]]
                self.SHACL.add((subject, p, o))
            elif value in self.type_list:
                p = self.shaclNS.datatype
                o = self.xsdNS[value]
                self.SHACL.add((subject, p, o))

        elif "default" in tag:
            p = self.shaclNS.defaultValue
            o = Literal(value)
            self.SHACL.add((subject, p, o))

        elif "fixed" in tag:
            p = self.shaclNS["in"]
            o = Literal(value)
            bn = BNode()
            self.SHACL.add((subject, p, bn))
            self.SHACL.add((bn, RDF.first, o))
            self.SHACL.add((bn, RDF.rest, RDF.nil))

        elif "pattern" in tag:
            p = self.shaclNS.pattern
            o = Literal(value)
            self.SHACL.add((subject, p, o))

        elif "maxExclusive" in tag:
            p = self.shaclNS.maxExclusive
            o = Literal(value)
            self.SHACL.add((subject, p, o))

        elif "minExclusive" in tag:
            p = self.shaclNS.minExclusive
            o = Literal(value)
            self.SHACL.add((subject, p, o))
  
        elif "maxInclusive" in tag:
            p = self.shaclNS.maxInclusive
            o = Literal(value)
            self.SHACL.add((subject, p, o))

        elif "minInclusive" in tag:
            p = self.shaclNS.minInclusive
            o = Literal(value)
            self.SHACL.add((subject, p, o))

        elif "length" in tag:        
            p = self.shaclNS.minLength
            o = Literal(int(value))
            self.SHACL.add((subject, p, o))
            p = self.shaclNS.maxLength
            o = rdflib.Literal(int(value))
            self.SHACL.add((subject, p, o))

        elif "minLength" in tag:        
            p = self.shaclNS.minLength
            o = Literal(int(value))
            self.SHACL.add((subject, p, o))

        elif "maxLength" in tag:        
            p = self.shaclNS.maxLength
            o = Literal(int(value))
            self.SHACL.add((subject, p, o))

    def transAnnotation(self, xsd_element, subject):
        """Process XSD annotations and map them to SHACL descriptions"""
        for child in xsd_element.findall("./"):
            tag = child.tag
            if "annotation" in tag:
                for sub_child in child.findall("./"):
                    tag = sub_child.tag
                    if "appinfo" in tag:
                        p = self.shaclNS.description
                        o = Literal(sub_child.text, lang=self.language)
                        self.SHACL.add((subject, p, o))
                    elif "documentation" in tag:
                        p = self.shaclNS.description
                        o = Literal(sub_child.text, lang=self.language)
                        self.SHACL.add((subject, p, o))

    def transEnumeration(self, xsd_element):
        """Process XSD enumerations for both SHACL and SKOS"""
        values = []
        subject = self.shapes[-1]
        parent_element = self.find_parent(xsd_element, self.root)

        if parent_element not in self.enumerationShapes:
            self.enumerationShapes.append(parent_element)
        else:
            return xsd_element

        # Process for SKOS concepts
        # Find first parent element with name
        parent_element_with_name = parent_element
        while parent_element_with_name is not None and parent_element_with_name.get("name") is None:
            parent_element_with_name = self.find_parent(parent_element_with_name, self.root)
        enum_skos = self.process_enumeration_for_skos(parent_element_with_name)
        
        # Process for SHACL constraints
        for e in parent_element.findall('.//xs:enumeration', namespaces={"xs": "http://www.w3.org/2001/XMLSchema"}):
            if e.get("value"):
                values.append(e.get("value"))

        if values == []:
            return xsd_element
        else:
            # If we have SKOS concepts for this enumeration, use them instead of literals
            if enum_skos:
                # Use sh:class and sh:nodeKind IRI to reference SKOS concepts in the constraints
                self.SHACL.add((subject, self.shaclNS.nodeKind, self.shaclNS.IRI))

                # Remove previous sh:datatype constraint if it exists
                self.SHACL.remove((subject, self.shaclNS.datatype, None))
                
                # Add SPARQL constraint to validate against the concept scheme
                sparql_bn = BNode()
                
                # Add the SPARQL constraint to the subject
                self.SHACL.add((subject, self.shaclNS.sparql, sparql_bn))
                self.SHACL.add((sparql_bn, RDF.type, self.shaclNS.SPARQLConstraint))
                self.SHACL.add((sparql_bn, self.shaclNS.message, Literal(f"The value must be a SKOS concept in the scheme {enum_skos['scheme_uri']}.", lang=self.language)))
                self.SHACL.add((sparql_bn, self.shaclNS.prefixes, Literal("skos:")))
                
                # Add the SPARQL select query
                sparql_query = f"""
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                    SELECT $this
                    WHERE {{
                        $this $PATH ?concept .
                        FILTER NOT EXISTS{{
                            ?concept skos:inScheme <{enum_skos['scheme_uri']}> .
                        }}
                    }}
                """
                self.SHACL.add((sparql_bn, self.shaclNS.select, Literal(sparql_query)))                
            else:
                # Traditional sh:in constraint with literal values
                current_BN = BNode()
                self.SHACL.add((subject, self.shaclNS["in"], current_BN))
                for index in range(len(values))[0:-1]:
                    self.SHACL.add((current_BN, RDF.first, Literal(values[index]))) 
                    next_BN = BNode()
                    self.SHACL.add((current_BN, RDF.rest, next_BN)) 
                    current_BN = next_BN

                self.SHACL.add((current_BN, RDF.first, Literal(values[-1]))) 
                self.SHACL.add((current_BN, RDF.rest, RDF.nil))
                
        return xsd_element    
    
    def transEleSimple(self, xsd_element):
        """A function to translate XSD element with simple type and attribute to SHACL property shape"""
        element_name = xsd_element.get("name")
        if element_name == None:
            return
        
        subject = self.NS[f'PropertyShape/{element_name}']

        if self.shapes != []:
            if "NodeShape" in str(self.shapes[-1]):
                pre_subject_path = self.shapes[-1].split("NodeShape/")[1]
            elif "PropertyShape" in str(self.shapes[-1]):
                pre_subject_path = self.shapes[-1].split("PropertyShape/")[1]
            else:
                subject = self.NS[f'PropertyShape/{pre_subject_path}/{element_name}']
            if subject not in self.choiceShapes:
                self.SHACL.add((self.shapes[-1], self.shaclNS.property, subject))
        
        self.transAnnotation(xsd_element, subject)
        self.shapes.append(subject)
        self.SHACL.add((subject, self.rdfSyntax['type'], self.shaclNS.PropertyShape))

        element_name_lowercase = element_name[0].lower() + element_name[1:] if element_name else ""
        self.SHACL.add((subject, self.shaclNS.path, self.xsdTargetNS[element_name_lowercase]))
        
        if "attribute" not in xsd_element.tag:
            element_min_occurs = Literal(int(xsd_element.get("minOccurs", "1")))
            self.SHACL.add((subject, self.shaclNS.minCount, element_min_occurs))
            element_max_occurs = xsd_element.get("maxOccurs", "1")
            if element_max_occurs != "unbounded" and (isinstance(element_max_occurs, int) or isinstance(element_max_occurs, str)):
                element_max_occurs = Literal(int(element_max_occurs))    
                self.SHACL.add((subject, self.shaclNS.maxCount, element_max_occurs))          

        elif xsd_element.get("use") == "required":
            self.SHACL.add((subject, self.shaclNS.minCount, Literal(1)))
            self.SHACL.add((subject, self.shaclNS.maxCount, Literal(1)))        
        elif xsd_element.get("use") == "optional":
            self.SHACL.add((subject, self.shaclNS.minCount, Literal(0)))
            self.SHACL.add((subject, self.shaclNS.maxCount, Literal(1)))
        elif xsd_element.get("use") == "prohibited":
            self.SHACL.add((subject, self.shaclNS.minCount, Literal(0)))
            self.SHACL.add((subject, self.shaclNS.maxCount, Literal(0)))
            
        # Format the element name for labels
        formatted_label = f"Type of {element_name[:-4]}" if element_name.endswith("Type") else create_formatted_label(element_name, self.custom_abbreviations)
        self.SHACL.add((subject, self.shaclNS.name, Literal(formatted_label, lang=self.language)))

        if self.order_list != []:
            self.SHACL.add((subject, self.shaclNS.order, Literal(self.order_list.pop())))

        for name in xsd_element.attrib:
            self.transRestriction(name, xsd_element.attrib[name])

        element_type = xsd_element.get("type") 
        # child type, built-in type or xsd simple type
        if element_type == None:
            return xsd_element
        elif (":" in element_type) or (element_type.split(":")[-1] in self.type_list): #TODO: check if this is a built-in type
            # already translated
            return xsd_element 
        else:
            next_node = self.root.find(f'.//{{http://www.w3.org/2001/XMLSchema}}simpleType[@name="{element_type}"]')
            # redirect current process to the next root (simple type)
            return next_node 
            
        return xsd_element

    def transEleComplex(self, xsd_element):
        """A function to translate XSD element with complex type to SHACL node shape"""
        element_name = xsd_element.get("name")
        subject = self.NS[f'NodeShape/{element_name}']
        ps_subject = self.NS[f'PropertyShape/{element_name}']

        if self.shapes != []:
            if "NodeShape" in str(self.shapes[-1]):
                pre_subject_path = self.shapes[-1].split("NodeShape/")[1]
            elif "PropertyShape" in str(self.shapes[-1]):
                pre_subject_path = self.shapes[-1].split("PropertyShape/")[1]
            subject = self.NS[f'NodeShape/{pre_subject_path}/{element_name}']
            ps_subject = self.NS[f'PropertyShape/{pre_subject_path}/{element_name}']
            if subject not in self.choiceShapes:
                self.SHACL.add((self.shapes[-1], self.shaclNS.node, subject))

        self.transAnnotation(xsd_element, subject)
        self.shapes.append(subject)
        self.SHACL.add((subject, self.rdfSyntax['type'], self.shaclNS.NodeShape))
        
        # Format the element name for labels
        formatted_label = f"Type of {element_name[:-4]}" if element_name.endswith("Type") else create_formatted_label(element_name, self.custom_abbreviations)
        self.SHACL.add((subject, self.shaclNS.name, Literal(formatted_label, lang=self.language)))
        
        # complex type does not have target, element can
        self.SHACL.add((subject, self.shaclNS.nodeKind, self.shaclNS.IRI))
        self.SHACL.add((subject, self.shaclNS.targetClass, self.xsdTargetNS[element_name]))
    
        for name in xsd_element.attrib:
            if "type" not in name:
                self.transRestriction(name, xsd_element.attrib[name], ps_subject)

        element_type = xsd_element.get("type")
        if element_type != None:
            self.SHACL.add((subject, self.shaclNS.node, self.NS[f'NodeShape/{element_type}'])) #Will be translated later

        return xsd_element

    def transEleComplexSimpleContent(self, xsd_element):
        """A function to translate XSD element with complex type simple Content to SHACL node shape"""
        element_name = xsd_element.get("name")
        subject = self.NS[f'NodeShape/{element_name}']
        ps_subject = self.NS[f'PropertyShape/{element_name}']

        if self.shapes != []:
            if "NodeShape" in str(self.shapes[-1]):
                pre_subject_path = self.shapes[-1].split("NodeShape/")[1]
            elif "PropertyShape" in str(self.shapes[-1]):
                pre_subject_path = self.shapes[-1].split("PropertyShape/")[1]
            subject = self.NS[f'NodeShape/{pre_subject_path}/{element_name}']
            ps_subject = self.NS[f'PropertyShape/{pre_subject_path}/{element_name}']
            if subject not in self.choiceShapes:
                self.SHACL.add((self.shapes[-1], self.shaclNS.node, subject))

        self.transAnnotation(xsd_element, subject)
        self.shapes.append(subject)
        self.SHACL.add((subject, self.rdfSyntax['type'], self.shaclNS.NodeShape))
        self.SHACL.add((subject, self.shaclNS.name, Literal(element_name, lang=self.language)))
        
        # complex type does not have target, element can
        self.SHACL.add((subject, self.shaclNS.nodeKind, self.shaclNS.IRI))
        self.SHACL.add((subject, self.shaclNS.targetClass, self.xsdTargetNS[element_name]))

        # Add one more property shape
        # BUG! The property shape should be added to the parent node
        # self.SHACL.add((subject, self.shaclNS.property, ps_subject))
        self.SHACL.add((ps_subject, self.rdfSyntax['type'], self.shaclNS.PropertyShape))
        self.SHACL.add((ps_subject, self.shaclNS['class'], self.xsdTargetNS[element_name]))
        self.SHACL.add((ps_subject, self.shaclNS.nodeKind, self.shaclNS.IRI))
        # Format the element name for labels
        formatted_label = f"Type of {element_name[:-4]}" if element_name.endswith("Type") else create_formatted_label(element_name, self.custom_abbreviations)
        self.SHACL.add((ps_subject, self.shaclNS.name, Literal(formatted_label, lang=self.language)))
        element_name_lowercase = element_name[0].lower() + element_name[1:] if element_name else ""
        self.SHACL.add((ps_subject, self.shaclNS.path, self.xsdTargetNS[element_name_lowercase]))
        element_min_occurs = Literal(int(xsd_element.get("minOccurs", "1")))
        self.SHACL.add((ps_subject, self.shaclNS.minCount, element_min_occurs))
        element_max_occurs = xsd_element.get("maxOccurs", "1")
        if element_max_occurs != "unbounded" and (isinstance(element_max_occurs, int) or isinstance(element_max_occurs, str)):
            element_max_occurs = Literal(int(element_max_occurs))    
            self.SHACL.add((ps_subject, self.shaclNS.maxCount, element_max_occurs))
    
        for name in xsd_element.attrib:
            if "type" not in name:
                self.transRestriction(name, xsd_element.attrib[name], ps_subject)
        element_type = xsd_element.get("type")
        if element_type == None:
            for i in xsd_element.findall(f".//{{http://www.w3.org/2001/XMLSchema}}complexType/{{http://www.w3.org/2001/XMLSchema}}simpleContent/{{http://www.w3.org/2001/XMLSchema}}extension"):
                type_name = i.get("base")
                if type_name.split(":")[-1] in self.type_list:
                    self.SHACL.add((ps_subject, self.shaclNS.datatype, self.xsdNS[type_name.split(":")[1]]))
                else:
                    extension_node = self.root.find(f".//*[@name='{type_name}']")
                    extension_node_type = self.isSimpleComplex(extension_node)
                    if extension_node_type == 0:
                        next_node = self.root.find(f'.//{{http://www.w3.org/2001/XMLSchema}}simpleType[@name="{type_name}"]')               
                        ps_type = self.NS[f'PropertyShape/{type_name}']
                        self.SHACL.add((subject, self.shaclNS.property, ps_type))

                        # redirect current process to the next root (simple type)         
                        return next_node 
                    elif extension_node_type == 1:
                        self.SHACL.add((ps_subject, self.shaclNS.node, self.NS[f'NodeShape/{type_name}']))
            return xsd_element
        else:
            self.SHACL.add((subject, self.shaclNS.node, self.NS[f'NodeShape/{element_type}'])) #Will be translated later

            for i in self.root.findall(f".//*[@name='{element_type}']/{{http://www.w3.org/2001/XMLSchema}}simpleContent/{{http://www.w3.org/2001/XMLSchema}}restriction"):
                type_name = i.get("base")
                if type_name.split(":")[-1] in self.type_list:
                    self.SHACL.add((ps_subject, self.shaclNS.datatype, self.xsdNS[type_name.split(":")[1]]))
            for i in self.root.findall(f".//*[@name='{element_type}']/{{http://www.w3.org/2001/XMLSchema}}simpleContent/{{http://www.w3.org/2001/XMLSchema}}extension"):
                type_name = i.get("base")
                if type_name.split(":")[-1] in self.type_list:
                    self.SHACL.add((ps_subject, self.shaclNS.datatype, self.xsdNS[type_name.split(":")[1]]))
                else:
                    extension_node = self.root.find(f".//*[@name='{type_name.split(':')[-1]}']")
                    extension_node_type = self.isSimpleComplex(extension_node)
                    if extension_node_type == 0:
                        next_node = extension_node
                        # redirect current process to the next root (simple type)
                        return next_node 
                    elif extension_node_type == 1:
                        self.SHACL.add((ps_subject, self.shaclNS.node, self.NS[f'NodeShape/{type_name}']))

            return xsd_element
        return xsd_element

    def transComplexType(self, xsd_element):
        """A function to translate XSD complex type to SHACL node shape""" 
        element_name = xsd_element.get("name")
        subject = self.NS[f'NodeShape/{element_name}']
        if self.shapes != []:
            if "NodeShape" in str(self.shapes[-1]):
                pre_subject_path = self.shapes[-1].split("NodeShape/")[1]
            elif "PropertyShape" in str(self.shapes[-1]):
                pre_subject_path = self.shapes[-1].split("PropertyShape/")[1]
            subject = self.NS[f'NodeShape/{pre_subject_path}/{element_name}']
            # To solve that it is the child node of any element
            if subject not in self.choiceShapes:
                self.SHACL.add((self.shapes[-1], self.shaclNS.node, subject))

        self.transAnnotation(xsd_element, subject)
        self.shapes.append(subject)
        self.SHACL.add((subject, self.rdfSyntax['type'], self.shaclNS.NodeShape))
        self.SHACL.add((subject, self.shaclNS.name, Literal(element_name, lang=self.language)))
        # complex type does not have target, element can

        for name in xsd_element.attrib:
            self.transRestriction(name, xsd_element.attrib[name])

        return xsd_element   

    def transGroup(self, xsd_element):
        """A function to translate XSD complex type to SHACL node shape""" 
        element_name = xsd_element.get("name")
        if element_name == None:
            element_name = xsd_element.get("id")
        subject = self.NS[f'NodeShape/{element_name}']
        self.shapes.append(subject)
        self.SHACL.add((subject, self.rdfSyntax['type'], self.shaclNS.NodeShape))
        self.SHACL.add((subject, self.shaclNS.name, Literal(element_name, lang=self.language)))
        # complex type does not have target, element can

        for name in xsd_element.attrib:
            self.transRestriction(name, xsd_element.attrib[name])

        return xsd_element    

    def transExtension(self, xsd_element):
        """A function to translate XSD extension"""
        element_name = xsd_element.get("base")
        # xsd_type = xsd_element.get("type")
        if element_name in self.extensionShapes:
            return xsd_element
        elif element_name.split(":")[-1] in self.type_list:
            if "PropertyShape" in str(self.shapes[-1]):
                self.SHACL.add((self.shapes[-1], self.shaclNS.datatype, self.xsdNS[element_name.split(":")[1]]))
            return xsd_element
        else:
            self.extensionShapes.append(element_name)
            sub_node = self.root.find(f'.//*[@name="{element_name.split(":")[-1]}"]', self.xsdNSdict)
            element_type = self.isSimpleComplex(sub_node, element_name.split(":")[-1])
            subject = self.shapes[-1]

            if element_type == 1:
                # complexType will be translated seperatly so we just need to add the node shape
                self.SHACL.add((subject, self.shaclNS.node, self.NS[f'NodeShape/{element_name}'])) 
                return xsd_element

        return xsd_element

    def transUnion(self, xsd_element):
        values = []
        subject = self.shapes[-1]

        if xsd_element.get("memberTypes") and len(xsd_element)==0:
            memberTypes = xsd_element.get("memberTypes").split(" ")

            current_BN = BNode()
            self.SHACL.add((subject, self.shaclNS["or"], current_BN))

            for index in range(len(memberTypes)):
                memberType = memberTypes[index]
                if (":" in memberType) and (memberType.split(":")[-1] in self.type_list):
                    shape_BN = BNode()
                    self.SHACL.add((current_BN, RDF.first, shape_BN)) 
                    self.SHACL.add((shape_BN, self.shaclNS.datatype, self.xsdNS[memberType.split(":")[1]])) 
                    next_BN = BNode()
                    if index == len(memberTypes)-1:
                        self.SHACL.add((current_BN, RDF.rest, RDF.nil)) 
                    else:   
                        self.SHACL.add((current_BN, RDF.rest, next_BN))
                    current_BN = next_BN
                else:
                    sub_node = self.root.find(f'.//*[@name="{memberType}"]', self.xsdNSdict)
                    element_type = self.isSimpleComplex(sub_node, memberType)
                    if element_type == 1:
                        self.SHACL.add((current_BN, RDF.first, self.NS[f'NodeShape/{memberType}'])) 
                        next_BN = BNode()
                        if index == len(memberTypes)-1:
                            self.SHACL.add((current_BN, RDF.rest, RDF.nil)) 
                        else:   
                            self.SHACL.add((current_BN, RDF.rest, next_BN))
                        current_BN = next_BN
                    elif element_type == 0:
                        sub_BN = BNode()
                        self.SHACL.add((current_BN, RDF.first, sub_BN))
                        self.shapes.append(sub_BN)
                        self.translate(sub_node)
                        self.shapes.pop()
                        next_BN = BNode()
                        if index == len(memberTypes)-1:
                            self.SHACL.add((current_BN, RDF.rest, RDF.nil)) 
                        else:   
                            self.SHACL.add((current_BN, RDF.rest, next_BN))
                        current_BN = next_BN
        elif xsd_element.get("memberTypes") and len(xsd_element)>0:
            memberTypes = xsd_element.get("memberTypes").split(" ")

            current_BN = BNode()
            self.SHACL.add((subject, self.shaclNS["or"], current_BN))

            for index in range(len(memberTypes)):
                memberType = memberTypes[index]
                if (":" in memberType) and (memberType.split(":")[-1] in self.type_list):
                    shape_BN = BNode()
                    self.SHACL.add((current_BN, RDF.first, shape_BN)) 
                    self.SHACL.add((shape_BN, self.shaclNS.datatype, self.xsdNS[memberType.split(":")[1]])) 
                    next_BN = BNode()
                    if index == len(memberTypes)-1:
                        self.SHACL.add((current_BN, RDF.rest, RDF.nil)) 
                    else:   
                        self.SHACL.add((current_BN, RDF.rest, next_BN))
                    current_BN = next_BN
                else:
                    sub_node = self.root.find(f'.//*[@name="{memberType}"]', self.xsdNSdict)
                    element_type = self.isSimpleComplex(sub_node, memberType)
                    if element_type == 1:
                        self.SHACL.add((current_BN, RDF.first, self.NS[f'NodeShape/{memberType}'])) 
                        next_BN = BNode()  
                        self.SHACL.add((current_BN, RDF.rest, next_BN))
                        current_BN = next_BN
                    elif element_type == 0:
                        sub_BN = BNode()
                        self.SHACL.add((current_BN, RDF.first, sub_BN))
                        self.shapes.append(sub_BN)
                        self.translate(sub_node)
                        self.shapes.pop()
                        next_BN = BNode()
                        self.SHACL.add((current_BN, RDF.rest, next_BN))
                        current_BN = next_BN         
            index = 0
            for sub_node in xsd_element:
                index += 1
                element_type = self.isSimpleComplex(sub_node)
                if element_type == 1:
                    self.SHACL.add((current_BN, RDF.first, self.NS[f'NodeShape/{memberType}'])) 
                    next_BN = BNode()
                    if index == len(memberTypes)-1:
                        self.SHACL.add((current_BN, RDF.rest, RDF.nil)) 
                    else:   
                        self.SHACL.add((current_BN, RDF.rest, next_BN))
                    current_BN = next_BN
                elif element_type == 0:
                    sub_BN = BNode()
                    self.SHACL.add((current_BN, RDF.first, sub_BN))
                    self.shapes.append(sub_BN)
                    self.translate(sub_node)
                    self.shapes.pop()
                    next_BN = BNode()
                    self.SHACL.add((current_BN, RDF.rest, next_BN))
                    current_BN = next_BN         
        else:
            current_BN = BNode()
            self.SHACL.add((subject, self.shaclNS["or"], current_BN))
            index = 0
            for sub_node in xsd_element:
                index += 1
                element_type = self.isSimpleComplex(sub_node)
                if element_type == 1:
                    self.SHACL.add((current_BN, RDF.first, self.NS[f'NodeShape/{memberType}'])) 
                    next_BN = BNode()
                    if index == len(memberTypes)-1:
                        self.SHACL.add((current_BN, RDF.rest, RDF.nil)) 
                    else:   
                        self.SHACL.add((current_BN, RDF.rest, next_BN))
                    current_BN = next_BN
                elif element_type == 0:
                    sub_BN = BNode()
                    self.SHACL.add((current_BN, RDF.first, sub_BN))
                    self.shapes.append(sub_BN)
                    self.translate(sub_node)
                    self.shapes.pop()
                    next_BN = BNode()
                    if index == len(xsd_element):
                        self.SHACL.add((current_BN, RDF.rest, RDF.nil)) 
                    else:   
                        self.SHACL.add((current_BN, RDF.rest, next_BN))
                    current_BN = next_BN         

    def transChoice(self, xsd_element):
        values = []
        subject = self.shapes[-1]
        if "NodeShape" in str(subject):
            pre_subject_path = subject.split("NodeShape/")[1]
        elif "PropertyShape" in str(subject):
            pre_subject_path = subject.split("PropertyShape/")[1]

        for child in xsd_element.findall("./"):
            tag = child.tag
            if "element" in tag:
                element_type = self.isSimpleComplex(child)
                if element_type == 0:
                    # values.append(self.NS[f'PropertyShape/{child.get("name")}'])
                    temp = self.NS[f'PropertyShape/{pre_subject_path}/{child.get("name")}']
                    values.append(temp)
                else:
                    # values.append(self.NS[f'NodeShape/{child.get("name")}'])
                    temp = self.NS[f'NodeShape/{pre_subject_path}/{child.get("name")}']
                    values.append(temp)
                self.choiceShapes.append(temp)
            elif "group" in tag:
                temp = child.get("ref")
                if temp == None:
                    temp = child.get("id")
                if temp == None:
                    temp = child.get("name")
                self.choiceShapes.append(temp)
                values.append(self.NS[f'NodeShape/{temp}'])

        values = [i for i in values if not i.endswith("None")]
        if values == []:
            return xsd_element
        else:
            current_BN = BNode()
            self.SHACL.add((subject, self.shaclNS["xone"], current_BN))
            for index in range(len(values))[0:-1]:
                self.SHACL.add((current_BN, RDF.first, URIRef(values[index]))) 
                next_BN = BNode()
                self.SHACL.add((current_BN, RDF.rest, next_BN)) 
                current_BN = next_BN

            self.SHACL.add((current_BN, RDF.first, URIRef(values[-1]))) 
            self.SHACL.add((current_BN, RDF.rest, RDF.nil)) 
            return xsd_element 

    def translate(self, current_node):
        """A function to iteratively translate XSD to SHACL and SKOS"""        
        
        for child in current_node.findall("*"):
            # Translate current node and associate this SHACL term/shape with its corresponding SHACL shape
            tag = child.tag
            next_node = child
            if ("element" in tag) or (("attribute" in tag) and ("attributeGroup" not in tag)):
                if child.get("ref"):
                    ref = child.get("ref")
                    if ":" in ref:
                        ref = ref.split(":")[-1]
                    ref_node = self.root.find(f".//*[@name='{ref}']")
                    if ref_node != None:
                        object = self.NS[f'PropertyShape/{ref}']
                        self.SHACL.add((self.shapes[-1], self.shaclNS.property, object))
                else:
                    element_type = self.isSimpleComplex(child)
                    if element_type == 0:
                        next_node = self.transEleSimple(child)
                    elif element_type == 1:
                        next_node = self.transEleComplex(child)
                    elif element_type == "simpleContent" or element_type == "mixed":
                        next_node = self.transEleComplexSimpleContent(child)
            elif ("simpleType" in tag) and (self.shapes == []):
                #self.transEleSimple(child)
                self.process_enumeration_for_skos(child)
                continue
            elif ("extension" in tag):
                next_node = self.transExtension(child)
            elif ("complexType" in tag) and (child.get("name")):
                next_node = self.transComplexType(child)
            elif ("attributeGroup" in tag):
                if child.get("ref"):
                    # next_node = self.root.find(f".//*[@name='{child.get('ref')}']")
                    self.SHACL.add((self.shapes[-1], self.shaclNS.node, self.NS[f'NodeShape/{child.get("ref")}']))
                else:
                    next_node = self.transComplexType(child)
            elif ("group" in tag):
                ref = child.get("ref")
                if ref:
                    if ref in self.choiceShapes:
                        pass
                    else:
                        self.SHACL.add((self.shapes[-1], self.shaclNS.node, self.NS[f'NodeShape/{ref}']))
                else:
                    next_node = self.transGroup(child)
            #combine with prev?
            elif ("simpleType" in tag):
                # self.transEleSimple(child)
                self.process_enumeration_for_skos(child)
            elif ("complexType" in tag): 
                pass
            elif ("restriction" in tag):
                value = child.get("base")
                self.transRestriction(tag, value)
            elif ("enumeration" in tag):
                self.transEnumeration(child)
            elif ("sequence" in tag):
                pass
            elif ("choice" in tag):
                self.transChoice(child)
            elif ("all" in tag):
                pass
            elif ("union" in tag):
                self.transUnion(child)
                continue
            elif ("appinfo" in tag) or ("documentation" in tag) or ("annotation" in tag):
                continue
            else:
                value = child.get("value")
                self.transRestriction(tag, value)
                
            # Translate next node
            self.translate(next_node)

            # Removed: or self.extension
            # an <xs:extension> is always inside another case that will return true below
            if (("element" in tag) and (child.get("name"))) or (("attribute" in tag) and ("attributeGroup" not in tag) and not child.get("ref")) or (("complexType" in tag) and (child.get("name"))) or (("attributeGroup" in tag) and (child.get("name"))) or (("group" in tag) and (child.get("name") or child.get("id"))):
                self.shapes.pop()
        
        if self.backUp != None:
            self.shapes.pop()
            temp = self.backUp
            self.backUp = None
            self.translate(temp)

    def parseXSD(self, ref_root, current_base_path=None):
        """Parse XSD to handle imports and includes, resolving relative paths correctly."""
        if current_base_path is None:
            current_base_path = self.BASE_PATH

        # Process xs:include
        for include_import_elem in ref_root.findall(".//xs:include", namespaces={"xs": "http://www.w3.org/2001/XMLSchema"}):
            self.root.remove(include_import_elem)
            included_imported_xsd_path = include_import_elem.get("schemaLocation")
            if included_imported_xsd_path and included_imported_xsd_path not in self.processed_files:
                try:
                    # Resolve path relative to the current base path
                    include_abs_path = os.path.join(current_base_path, included_imported_xsd_path)
                    next_ref_root = ET.parse(include_abs_path).getroot()
                    self.processed_files.append(included_imported_xsd_path)
                except Exception as e:
                    print("Error: parse include error file:", included_imported_xsd_path)
                    print("Complete exception follows below. Processing stopped")
                    raise e

                # The new base path for further includes/imports is the directory of the included file
                next_base_path = os.path.dirname(include_abs_path)
                for child in next_ref_root.findall("./"):
                    if ("import" not in child.tag) or ("include" not in child.tag):
                        self.root.append(child)
                self.parseXSD(next_ref_root, current_base_path=next_base_path)
        
        # Process xs:import
        for include_import_elem in ref_root.findall(".//xs:import", namespaces={"xs": "http://www.w3.org/2001/XMLSchema"}):
            self.root.remove(include_import_elem)
            included_imported_xsd_path = include_import_elem.get("schemaLocation")
            if included_imported_xsd_path and included_imported_xsd_path not in self.processed_files:
                try:
                    import_abs_path = os.path.join(current_base_path, included_imported_xsd_path)
                    next_ref_root = ET.parse(import_abs_path).getroot()
                    self.processed_files.append(included_imported_xsd_path)
                except Exception as e:
                    print("Parse error import file:", included_imported_xsd_path)
                    self.processed_files.append(included_imported_xsd_path)
                    continue

                next_base_path = os.path.dirname(import_abs_path)
                for child in next_ref_root.findall("./"):
                    if ("import" not in child.tag) or ("include" not in child.tag):
                        self.root.append(child)
                self.parseXSD(next_ref_root, current_base_path=next_base_path)

    def writeShapeToFile(self, file_name):
        """Write SHACL shapes to file"""
        for prefix in self.xsdNSdict:
            self.SHACL.bind(prefix, self.xsdNSdict[prefix])
        self.SHACL.bind("ex", self.NS)

        self.SHACL.bind('era', 'http://data.europa.eu/949/')
        self.SHACL.bind('sh', 'http://www.w3.org/ns/shacl#', False)
        self.SHACL.bind('skos', 'http://www.w3.org/2004/02/skos/core#')

        self.SHACL.serialize(destination=file_name, format='turtle')

    def writeSkosToFile(self, output_dir):
        """Save each concept scheme to a separate file."""
        if not self.concept_schemes:
            print("No concept schemes found to save.")
            return
            
        # Create output directory if it doesn't exist
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
            
        base_filename = os.path.basename(self.xsd_file)
        
        # Save each concept scheme to a separate file
        for name, scheme_data in self.concept_schemes.items():
            # Create a new graph for this concept scheme
            graph = self.initialize_skos_graph()
            # Add the concept scheme first
            scheme_uri = scheme_data['uri']
            
            # Create formatted label for the concept scheme
            formatted_name = create_formatted_label(name, self.custom_abbreviations)
            conceptscheme_label = "Concept Scheme for " + (f"type of {formatted_name[:-5].lower()}" if name.endswith("Type") else formatted_name)
            
            graph.add((scheme_uri, RDF.type, self.skosNS.ConceptScheme))
            graph.add((scheme_uri, self.rdfsNS.label, Literal(conceptscheme_label, lang=self.language)))
            
            # Add Dublin Core metadata
            graph.add((scheme_uri, self.dctNS.title, Literal(conceptscheme_label, lang=self.language)))
            graph.add((scheme_uri, self.dctNS.issued, Literal(self.current_date, datatype=self.xsdNS.date)))
            graph.add((scheme_uri, self.dctNS.modified, Literal(self.current_date, datatype=self.xsdNS.date)))
            
            # Add Creative Commons license
            graph.add((scheme_uri, self.ccNS.license, self.cc_license))
            
            # Add documentation if available
            if scheme_data['doc']:
                graph.add((scheme_uri, self.skosNS.definition, Literal(scheme_data['doc'], lang=self.language)))
            
            # Add all concepts for this scheme
            for concept in scheme_data['concepts']:
                # Create formatted label for the concept
                formatted_value = create_formatted_label(concept['value'], self.custom_abbreviations)
                
                graph.add((concept['uri'], RDF.type, self.skosNS.Concept))
                graph.add((concept['uri'], self.skosNS.notation, Literal(formatted_value, datatype=self.xsdNS.token)))
                graph.add((concept['uri'], self.skosNS.inScheme, scheme_uri))
                graph.add((concept['uri'], self.skosNS.topConceptOf, scheme_uri))
                
                if concept['definition']:
                    graph.add((concept['uri'], self.skosNS.prefLabel, Literal(concept['definition'], lang=self.language)))
                else:
                    graph.add((concept['uri'], self.skosNS.prefLabel, Literal(formatted_value, lang=self.language)))

            # Save the graph to a file
            file_path = os.path.join(output_dir, f"{base_filename}.skos.{name}.ttl")
            graph.serialize(destination=file_path, format="turtle")
            print(f"Saved concept scheme '{name}' to {file_path}")

    def initialize_owl_ontology(self):
        """Initialize the OWL ontology with namespace bindings and ontology declaration"""
        # Add namespace bindings
        self.OWL_Graph.bind('era', self.era)
        self.OWL_Graph.bind('owl', self.owlNS)
        self.OWL_Graph.bind('rdf', self.rdfSyntax)
        self.OWL_Graph.bind('rdfs', self.rdfsNS)
        self.OWL_Graph.bind('xsd', self.xsdNS)
        self.OWL_Graph.bind('dct', self.dctNS)
        self.OWL_Graph.bind('cc', self.ccNS)
        self.OWL_Graph.bind('', self.NS)
        
        # Create ontology declaration
        ontology_uri = URIRef(self.NS)
        self.OWL_Graph.add((ontology_uri, RDF.type, OWL.Ontology))
        
        # Add ontology label based on the XSD file name
        xsd_name = os.path.splitext(os.path.basename(self.xsd_file))[0]
        formatted_name = create_formatted_label(xsd_name,self.custom_abbreviations)
        self.OWL_Graph.add((ontology_uri, self.rdfsNS.label, Literal(f"Ontology generated from {formatted_name} XSD", lang="en")))
        
        # Extract all Dublin Core terms from the XSD annotation
        dcterms = self.extract_dcterms_from_annotation()
        
        # Add all extracted dcterms to the ontology
        # If specific terms are not found, use default values
        
        # Set default values for common dcterms if they don't exist in the extracted data
        defaults = {
            'description': f"Ontology generated from {formatted_name} XSD",
            'title': f"Ontology generated from {formatted_name} XSD",
            'created': self.current_date,
            'modified': self.current_date,
            'issued': self.current_date
        }
        
        # Add all dcterms from the annotation element
        for term, value in dcterms.items():
            if isinstance(value, list):
                # Add each value separately for repeated terms
                for val in value:
                    # Try to detect if the value should be a literal with language tag
                    if term in ['title', 'description', 'abstract', 'subject', 'creator', 'publisher', 'contributor', 'rights']:
                        self.OWL_Graph.add((ontology_uri, getattr(self.dctNS, term), Literal(val, lang=self.language)))
                    else:
                        # For dates and other non-language tagged terms
                        self.OWL_Graph.add((ontology_uri, getattr(self.dctNS, term), Literal(val)))
            else:
                # Add single value
                if term in ['title', 'description', 'abstract', 'subject', 'creator', 'publisher', 'contributor', 'rights']:
                    self.OWL_Graph.add((ontology_uri, getattr(self.dctNS, term), Literal(value, lang=self.language)))
                else:
                    # For dates and other non-language tagged terms
                    self.OWL_Graph.add((ontology_uri, getattr(self.dctNS, term), Literal(value)))
        
        # Add default values for missing common dcterms
        for term, default_value in defaults.items():
            if term not in dcterms:
                if term in ['title', 'description']:
                    self.OWL_Graph.add((ontology_uri, getattr(self.dctNS, term), Literal(default_value, lang=self.language)))
                else:
                    self.OWL_Graph.add((ontology_uri, getattr(self.dctNS, term), Literal(default_value)))
    
    def extract_dcterms_from_annotation(self):
        """Extract Dublin Core terms from the XSD schema's first annotation element"""
        dcterms_dict = {}
        
        if self.root is not None:
            # Find the first annotation element in the schema
            annotation = self.root.find(".//{http://www.w3.org/2001/XMLSchema}annotation")
            if annotation is not None:
                # Look for any elements that are dcterms
                for element in annotation.findall(".//*"):
                    # Check if element namespace is Dublin Core terms
                    if element.tag.startswith("{http://purl.org/dc/terms/}"):
                        # Extract term name from namespace URI
                        term = element.tag.split('}')[1]
                        if element.text and element.text.strip():
                            # Store the term and its value
                            # If the term already exists in the dictionary, make it a list or append to existing list
                            if term in dcterms_dict:
                                if isinstance(dcterms_dict[term], list):
                                    dcterms_dict[term].append(element.text.strip())
                                else:
                                    # Convert single value to list with both values
                                    dcterms_dict[term] = [dcterms_dict[term], element.text.strip()]
                            else:
                                # Store single value
                                dcterms_dict[term] = element.text.strip()
        
        return dcterms_dict

    def generate_owl_graph(self):
        """Generate OWL graph from SHACL shapes"""
        
        owl_classes = self.SHACL.query("""
            prefix owl: <http://www.w3.org/2002/07/owl#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix sh: <http://www.w3.org/ns/shacl#>

            construct {
            ?classIRI a owl:Class;
                rdfs:label ?classLabel;
                rdfs:comment ?classComment.
            }
            where {
            ?nodeshape a sh:NodeShape;
                sh:targetClass ?classIRI;
                sh:name ?classLabel.
                OPTIONAL{?nodeshape sh:description ?classComment . } 
            }"""
        )
        
        # Add the results of the OWL class query to the OWL graph
        for s, p, o in owl_classes:
            self.OWL_Graph.add((s, p, o))

        owl_dataproperties = self.SHACL.query("""
            prefix owl: <http://www.w3.org/2002/07/owl#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix sh: <http://www.w3.org/ns/shacl#>

            construct {
                ?propertyIRI a owl:DatatypeProperty;
                    rdfs:label ?propertyLabel;
                    rdfs:comment ?propertyComment.
                                                
                    # We'll create the domain/range relationships separately to handle properly
            }
            where {
                ?datatypeProperty a sh:PropertyShape;
                    sh:path ?propertyIRI;
                    sh:datatype ?datatype.

                    OPTIONAL{?datatypeProperty sh:name ?propertyLabel;}
                    OPTIONAL{?datatypeProperty sh:description ?propertyComment;}
            }   
            """)

        # Add the results of the OWL data property query to the OWL graph
        for s, p, o in owl_dataproperties:
            self.OWL_Graph.add((s, p, o))

        # Add functional properties
        owl_functional_properties = self.SHACL.query("""
            prefix owl: <http://www.w3.org/2002/07/owl#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix sh: <http://www.w3.org/ns/shacl#>

            construct {
                ?propertyIRI a owl:FunctionalProperty.
            }
            where {
                ?datatypeProperty a sh:PropertyShape;
                    sh:path ?propertyIRI;
                    sh:maxCount 1;
                .
            }   
        """)

        # Add the results of the OWL functional properties query to the OWL graph
        for s, p, o in owl_functional_properties:
            self.OWL_Graph.add((s, p, o))

        # Create additional query for object properties
        owl_objectproperties = self.SHACL.query("""
            prefix owl: <http://www.w3.org/2002/07/owl#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix sh: <http://www.w3.org/ns/shacl#>

            construct {
                ?propertyIRI a owl:ObjectProperty;
                    rdfs:label ?propertyLabel;
                    rdfs:comment ?propertyComment.
                
                # We'll create the domain/range relationships separately to handle properly
            }
            where {
                ?objectProperty a sh:PropertyShape;
                    sh:path ?propertyIRI;    
                    sh:nodeKind ?propertyNodekind.

                    OPTIONAL{?objectProperty sh:name ?propertyLabel;}
                    OPTIONAL{?objectProperty sh:description ?propertyComment;}
                    
                    FILTER(?propertyNodekind = sh:IRI)
            }
        """)

        # Add the basic object property triples from the query
        for s, p, o in owl_objectproperties:
            self.OWL_Graph.add((s, p, o))

        # Now handle domain and range separately to properly create owl:unionOf when needed
        domain_query = self.SHACL.query("""
            prefix owl: <http://www.w3.org/2002/07/owl#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix sh: <http://www.w3.org/ns/shacl#>

            select ?propertyIRI ?domainClass
            where {
                ?nodeshape a sh:NodeShape;
                    sh:targetClass ?domainClass;
                    sh:property ?propertyShapeIri .

                ?propertyShapeIri a sh:PropertyShape;
                    sh:path ?propertyIRI.
            }
            GROUP BY ?propertyIRI ?domainClass
        """)

        # Group domains by property
        domains_by_property = {}
        for row in domain_query:
            property_iri = row.propertyIRI
            class_iri = row.domainClass
            
            if property_iri not in domains_by_property:
                domains_by_property[property_iri] = []
            domains_by_property[property_iri].append(class_iri)

        # Create domain relationships with owl:unionOf when needed
        for property_iri, classes in domains_by_property.items():
            if len(classes) == 1:
                # Single domain
                self.OWL_Graph.add((property_iri, self.rdfsNS.domain, classes[0]))
            else:
                # Multiple domains need owl:unionOf
                union_node = BNode()
                self.OWL_Graph.add((property_iri, self.rdfsNS.domain, union_node))
                self.OWL_Graph.add((union_node, RDF.type, OWL.Class))
                self.OWL_Graph.add((union_node, OWL.unionOf, self.create_rdf_list(classes)))

        # Handle ranges similarly
        range_query = self.SHACL.query("""
            prefix owl: <http://www.w3.org/2002/07/owl#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix sh: <http://www.w3.org/ns/shacl#>
            prefix skos: <http://www.w3.org/2004/02/skos/core#>

            select ?propertyIRI ?rangeClass
            where {
                {
                    ?objectProperty a sh:PropertyShape;
                        sh:path ?propertyIRI;    
                        sh:nodeKind sh:IRI.
                                            
                    {
                        ?objectProperty sh:class ?rangeClass.
                    } 
                    UNION {
                        ?objectProperty sh:sparql ?propertySparql.
                        ?propertySparql sh:select ?query.
                        FILTER(CONTAINS(?query, "skos:inScheme"))
                        BIND(skos:Concept AS ?rangeClass)
                    }
                }  
                UNION {
                    ?datatypeProperty a sh:PropertyShape;
                        sh:path ?propertyIRI;    
                        sh:datatype ?rangeClass.        
                }
            }
            GROUP BY ?propertyIRI ?rangeClass
        """)

        # Group ranges by property
        ranges_by_property = {}
        for row in range_query:
            property_iri = row.propertyIRI
            class_iri = row.rangeClass
            
            if property_iri not in ranges_by_property:
                ranges_by_property[property_iri] = []
            ranges_by_property[property_iri].append(class_iri)

        # Create range relationships with owl:unionOf when needed
        for property_iri, classes in ranges_by_property.items():
            if len(classes) == 1:
                # Single range
                self.OWL_Graph.add((property_iri, self.rdfsNS.range, classes[0]))
            else:
                # Multiple classes need owl:unionOf
                union_node = BNode()
                self.OWL_Graph.add((property_iri, self.rdfsNS.range, union_node))
                self.OWL_Graph.add((union_node, RDF.type, OWL.Class))
                self.OWL_Graph.add((union_node, OWL.unionOf, self.create_rdf_list(classes)))

    def create_rdf_list(self, items):
        """
        Create an RDF list from a list of items.
        """
        if not items:
            return RDF.nil
        
        head = BNode()
        self.OWL_Graph.add((head, RDF.first, items[0]))
        
        if len(items) == 1:
            self.OWL_Graph.add((head, RDF.rest, RDF.nil))
        else:
            tail = self.create_rdf_list(items[1:])
            self.OWL_Graph.add((head, RDF.rest, tail))
        
        return head
    
    def writeOWLToFile(self, file_name):       
        # Save OWL ontology to file
        self.OWL_Graph.serialize(destination=file_name, format='turtle')
        print(f"Saved OWL ontology in {file_name}!")

    def evaluate_file(self, xsd_file, output_dir=None):
        """
        Parse the given XSD file and generate both SHACL shapes and SKOS concepts
        
        Args:
            xsd_file: Path to the XSD file to be converted
            output_dir: Directory to save the generated files (optional)
        """
        self.xsd_file = xsd_file
        self.BASE_PATH = os.path.dirname(xsd_file)
        self.xsdTree = ET.parse(xsd_file)
        self.root = self.xsdTree.getroot()

        recursiceCheck(self.root)

        self.xsdNSdict = dict([node for (_, node) in ET.iterparse(xsd_file, events=['start-ns'])])

        self.parse_language()
        print(f"Using language tag: {self.language}")

        # Parse XSD to handle imports and includes
        print("#########Start parsing XSD file")
        self.parseXSD(self.root)

        # Extract namespaces from the XSD
        xmlns = self.root.get('xmlns')
        if xmlns:
            # Normalize namespace by removing trailing / (if present) and then adding it back
            normalized_ns = xmlns.rstrip('/') + '/'
            self.NS = Namespace(normalized_ns)
            
        # Extract the target namespace
        for key in self.root.attrib:
            if key == "targetNamespace":
                # Normalize namespace by removing trailing / (if present) and then adding it back
                normalized_ns = self.root.attrib[key].rstrip('/') + '/'
                self.xsdTargetNS = Namespace(normalized_ns)
                if not xmlns:  # Only update NS if xmlns was not found
                    self.NS = Namespace(normalized_ns)  

        print("#########Start translating XSD to RDF (SHACL + SKOS)")
        start = time.time()
        self.translate(self.root)
        end = time.time()
        print(f"RDF conversion completed in {end - start:.2f} seconds")

        print("#########Start validating SHACL shapes syntax")
        shaclValidation = Graph()
        shaclValidation.parse("https://www.w3.org/ns/shacl-shacl")
        
        if len(self.SHACL) < 10000:
            r = validate(self.SHACL, shacl_graph=shaclValidation)
            if not r[0]:
                print(r[2])
            else:
                print("Well formed SHACL shapes!")
        else:
            print("Skip SHACL shape syntax check using pyshacl due to the size of SHACL shapes is too large!")

        print("#########Start creating OWL graph")
        self.initialize_owl_ontology()
        self.generate_owl_graph()

        # Determine output directory
        if output_dir is None:
            output_dir = self.BASE_PATH
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        # Compose output file paths
        base_filename = os.path.basename(xsd_file)
        shacl_file = os.path.join(output_dir, base_filename + ".shape.ttl")
        owl_file = os.path.join(output_dir, base_filename + ".owl.ttl")

        print("#########Start writing SHACL shapes to file")
        self.writeShapeToFile(shacl_file)
        print(f"Saved SHACL shapes in {shacl_file}!")
        
        print("#########Start writing SKOS concepts to files")
        self.writeSkosToFile(output_dir)
        
        print("#########Start writing OWL to file")
        self.writeOWLToFile(owl_file)

        return {
            'shacl': self.SHACL,
            'concept_schemes': self.concept_schemes
        }
