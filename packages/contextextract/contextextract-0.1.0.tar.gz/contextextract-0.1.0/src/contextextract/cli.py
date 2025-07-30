import os
import json
import argparse
from contextextract import ContextExtractor


def main():
    """
    Command-line interface for the ContextExtract package.
    """
    parser = argparse.ArgumentParser(
        description="Extract key-value pairs from URLs, PDFs, or text using Groq API."
    )
    
    # Setup subcommands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # URL processing subcommand
    url_parser = subparsers.add_parser("url", help="Extract from a URL")
    url_parser.add_argument("url", help="URL to extract data from")
    url_parser.add_argument("-o", "--output", help="Output JSON file path")
    
    # PDF processing subcommand
    pdf_parser = subparsers.add_parser("pdf", help="Extract from a PDF file")
    pdf_parser.add_argument("pdf_path", help="Path to the PDF file")
    pdf_parser.add_argument("-o", "--output", help="Output JSON file path")
    
    # Text processing subcommand
    text_parser = subparsers.add_parser("text", help="Extract from text")
    text_parser.add_argument("text", help="Input text or file path containing text")
    text_parser.add_argument("--is-file", action="store_true", help="Treat input as a file path")
    text_parser.add_argument("-o", "--output", help="Output JSON file path")
    
    # Common options
    parser.add_argument("-k", "--api-key", help="Groq API key")
    parser.add_argument("-m", "--model", default="llama3-70b-8192", help="Groq model to use")
    parser.add_argument("-p", "--pretty", action="store_true", default=True, 
                        help="Output pretty-printed JSON")
    
    args = parser.parse_args()
    
    # Exit if no command provided
    if not args.command:
        parser.print_help()
        return
    
    # Get API key
    api_key = args.api_key or os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Error: Groq API key is required. Use --api-key or set GROQ_API_KEY environment variable.")
        return
    
    # Initialize extractor
    extractor = ContextExtractor(api_key=api_key)
    
    # Setup parameters
    params = {
        "model": args.model
    }
    
    # Process based on command
    try:
        if args.command == "url":
            result = extractor.extract_from_url(args.url, params)
            output_file = args.output or f"url_extract_{args.url.split('//')[-1].split('/')[0]}.json"
        
        elif args.command == "pdf":
            result = extractor.extract_from_pdf(args.pdf_path, params)
            output_file = args.output or f"pdf_extract_{os.path.basename(args.pdf_path).split('.')[0]}.json"
        
        elif args.command == "text":
            if args.is_file:
                with open(args.text, 'r', encoding='utf-8') as f:
                    text_content = f.read()
            else:
                text_content = args.text
            
            result = extractor.extract_from_text(text_content, params)
            output_file = args.output or "text_extract.json"
        
        # Save the result
        extractor.save_to_json(result, output_file, pretty=args.pretty)
        print(f"Extraction complete. Results saved to {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
