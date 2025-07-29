import os
import sys
import subprocess
from pathlib import Path

class DocConverter:
    """Converts Microsoft Word documents (.doc, .docx) to PDF format."""
    
    def __init__(self, use_libreoffice=True):
        """
        Initialize the converter with the preferred conversion method.
        
        Args:
            use_libreoffice (bool): Whether to use LibreOffice for conversion
                                  (falls back to python-docx2pdf if False or if LibreOffice fails)
        """
        self.use_libreoffice = use_libreoffice
        
    def _check_libreoffice(self):
        """Check if LibreOffice is available on the system."""
        try:
            if sys.platform == "win32":
                # Check for soffice.exe on Windows
                subprocess.run(["where", "soffice.exe"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                # Check for soffice on Linux/Mac
                subprocess.run(["which", "soffice"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def _convert_with_libreoffice(self, input_path, output_path=None):
        """
        Convert document using LibreOffice.
        
        Args:
            input_path (str): Path to input document
            output_path (str, optional): Path for output PDF file
        
        Returns:
            str: Path to the created PDF file
        """
        input_path = Path(input_path).resolve()
        
        if output_path is None:
            output_path = input_path.with_suffix('.pdf')
        else:
            output_path = Path(output_path).resolve()
            
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Prepare the command
        if sys.platform == "win32":
            cmd = ["soffice.exe"]
        else:
            cmd = ["soffice"]
            
        cmd.extend([
            "--headless",
            "--convert-to", "pdf",
            "--outdir", str(output_path.parent),
            str(input_path)
        ])
        
        # Run the conversion
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # LibreOffice uses the same filename with .pdf extension
            auto_output = input_path.with_suffix('.pdf')
            
            # If output_path is different from auto_output, rename the file
            if str(auto_output) != str(output_path) and auto_output.exists():
                auto_output.rename(output_path)
                
            return str(output_path)
        except subprocess.SubprocessError as e:
            raise RuntimeError(f"LibreOffice conversion failed: {e}")
    
    def _convert_with_docx2pdf(self, input_path, output_path=None):
        """
        Convert document using docx2pdf package.
        
        Args:
            input_path (str): Path to input document
            output_path (str, optional): Path for output PDF file
        
        Returns:
            str: Path to the created PDF file
        """
        try:
            from docx2pdf import convert
            
            input_path = Path(input_path).resolve()
            
            if output_path is None:
                output_path = input_path.with_suffix('.pdf')
            else:
                output_path = Path(output_path).resolve()
                
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Perform the conversion
            convert(str(input_path), str(output_path))
            
            return str(output_path)
        except ImportError:
            raise RuntimeError("docx2pdf package is not installed. Please install it with 'pip install docx2pdf'")
    
    def convert(self, input_path, output_path=None):
        """
        Convert a Word document to PDF.
        
        Args:
            input_path (str): Path to the Word document
            output_path (str, optional): Path for the output PDF file
                                       (if not provided, will use the same name with .pdf extension)
        
        Returns:
            str: Path to the created PDF file
            
        Raises:
            FileNotFoundError: If the input file doesn't exist
            ValueError: If the input file is not a .doc or .docx file
            RuntimeError: If conversion fails
        """
        input_path = Path(input_path)
        
        # Check if input file exists
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Check if input file is a Word document
        if input_path.suffix.lower() not in ['.doc', '.docx']:
            raise ValueError(f"Input file must be a .doc or .docx file, got: {input_path.suffix}")
        
        # Try with LibreOffice if requested and available
        if self.use_libreoffice and self._check_libreoffice():
            try:
                return self._convert_with_libreoffice(input_path, output_path)
            except RuntimeError:
                print("LibreOffice conversion failed, falling back to docx2pdf")
        
        # Otherwise use docx2pdf
        return self._convert_with_docx2pdf(input_path, output_path)
    
    def batch_convert(self, input_dir, output_dir=None, recursive=False):
        """
        Convert all Word documents in a directory.
        
        Args:
            input_dir (str): Directory containing Word documents
            output_dir (str, optional): Directory for output PDF files
                                      (if not provided, PDFs will be created in the same directory)
            recursive (bool): Whether to search for files recursively
            
        Returns:
            list: Paths to all created PDF files
            
        Raises:
            FileNotFoundError: If the input directory doesn't exist
        """
        input_dir = Path(input_dir)
        
        # Check if input directory exists
        if not input_dir.exists() or not input_dir.is_dir():
            raise FileNotFoundError(f"Input directory not found: {input_dir}")
        
        # Prepare output directory
        if output_dir is not None:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
        
        # Find all Word documents
        if recursive:
            doc_files = list(input_dir.glob('**/*.doc')) + list(input_dir.glob('**/*.docx'))
        else:
            doc_files = list(input_dir.glob('*.doc')) + list(input_dir.glob('*.docx'))
        
        # Convert each document
        pdf_files = []
        for doc_file in doc_files:
            # Calculate relative path from input_dir
            rel_path = doc_file.relative_to(input_dir)
            
            if output_dir is not None:
                # Create output file path with the same relative path but in output_dir
                output_file = output_dir / rel_path.with_suffix('.pdf')
                # Ensure parent directories exist
                output_file.parent.mkdir(parents=True, exist_ok=True)
            else:
                output_file = doc_file.with_suffix('.pdf')
                
            try:
                pdf_path = self.convert(doc_file, output_file)
                pdf_files.append(pdf_path)
                print(f"Converted: {doc_file} -> {pdf_path}")
            except Exception as e:
                print(f"Failed to convert {doc_file}: {e}")
                
        return pdf_files