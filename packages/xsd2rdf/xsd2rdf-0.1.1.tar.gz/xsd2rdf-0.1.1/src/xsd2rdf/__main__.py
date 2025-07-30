import argparse
import os
import sys
from .XSDtoRDF import XSDtoRDF


def define_args():
    parser = argparse.ArgumentParser(description='Convert XSD to RDF formats (SHACL, OWL, SKOS)')

    parser.add_argument("--XSD_FILE", "-x", type=str, required=True, 
                        help="XSD file to be converted into RDF")
    parser.add_argument("--OUTPUT_DIR", "-o", type=str, 
                        help="Output directory for generated files (default: same as XSD file)")
    parser.add_argument("--ABBREVIATIONS_FILE", "-a", type=str, 
                        help="File containing custom abbreviations, one per line")
    return parser.parse_args()

def main():
    args = define_args()
    
    if args.XSD_FILE:
        xsd_file = args.XSD_FILE
        output_dir = args.OUTPUT_DIR
        abbreviations_file = args.ABBREVIATIONS_FILE

        if not os.path.isfile(xsd_file):
            print(f"Error: XSD file {xsd_file} not found")
            sys.exit(1)
            
        if abbreviations_file and not os.path.exists(abbreviations_file):
            print(f"Warning: Abbreviations file {abbreviations_file} not found. Using default abbreviations.")
            abbreviations_file = None
            

        # If output directory is not provided, use the directory of the XSD file
        if not output_dir:
            output_dir = os.path.dirname(os.path.abspath(xsd_file))
            # If the dirname is empty (running in same dir as file), use current directory
            if not output_dir:
                output_dir = os.getcwd()

        # Create output directory if it doesn't exist
        if output_dir and not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        print(f"Converting {xsd_file} to SHACL, SKOS and OWL...")
        
        converter = XSDtoRDF(abbreviations_file)
        result = converter.evaluate_file(xsd_file, output_dir)
        
        print(f"All conversions completed successfully! Output files saved in: {output_dir}")

    else:
        # If no command is provided, show help
        define_args()
        print("Please specify a command. Use --help for more information.")
        sys.exit(1)

if __name__ == "__main__":
    main()
