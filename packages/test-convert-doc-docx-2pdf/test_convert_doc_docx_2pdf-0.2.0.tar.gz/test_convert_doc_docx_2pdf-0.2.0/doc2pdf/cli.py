import argparse
import sys
from pathlib import Path
from .converter import DocConverter

def main():
    parser = argparse.ArgumentParser(
        description="Convert Microsoft Word documents (.doc, .docx) to PDF format"
    )
    
    # Input arguments
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-f', '--file', help="Path to a Word document (.doc, .docx)")
    input_group.add_argument('-d', '--directory', help="Directory containing Word documents")
    
    # Output arguments
    parser.add_argument('-o', '--output', help="Output PDF file or directory")
    
    # Additional options
    parser.add_argument('-r', '--recursive', action='store_true', 
                        help="Search for Word documents recursively (only with --directory)")
    parser.add_argument('--use-docx2pdf', action='store_true',
                        help="Force using docx2pdf instead of LibreOffice")
    
    args = parser.parse_args()
    
    # Initialize converter
    converter = DocConverter(use_libreoffice=not args.use_docx2pdf)
    
    try:
        if args.file:
            # Convert a single file
            input_path = Path(args.file)
            output_path = args.output if args.output else None
            
            pdf_path = converter.convert(input_path, output_path)
            print(f"Converted: {input_path} -> {pdf_path}")
            
        elif args.directory:
            # Convert all files in directory
            input_dir = Path(args.directory)
            output_dir = Path(args.output) if args.output else None
            
            pdf_files = converter.batch_convert(input_dir, output_dir, args.recursive)
            print(f"Converted {len(pdf_files)} files")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
        
    sys.exit(0)