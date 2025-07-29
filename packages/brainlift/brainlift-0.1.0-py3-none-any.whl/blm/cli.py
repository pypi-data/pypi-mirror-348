#!/usr/bin/env python3
"""
BLM - BrainLift Manager (Serverless CLI)
A dedicated CLI for interacting with the BrainLift serverless backend
"""

import os
import sys
import argparse
import logging
from dotenv import load_dotenv

# Import from the package's client module
from blm.client import call_serverless_api, get_function_url, get_api_key

# Set up logging
logging.basicConfig(
    level=logging.WARNING,  # Default to WARNING level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('blm')

def load_env():
    """Load environment variables from .env file"""
    load_dotenv()
    logger.info("Loaded environment variables from .env")
    
    # Check if required environment variables are set
    function_url = get_function_url()
    api_key = get_api_key()
    
    if not function_url:
        logger.error("BRAINLIFT_FUNCTION_URL is not set in .env file")
        sys.exit(1)
    
    if not api_key:
        logger.error("BRAINLIFT_API_KEY is not set in .env file")
        sys.exit(1)
        
    logger.info(f"Using function URL: {function_url}")
    logger.info(f"Using API key: {api_key[:5]}...{api_key[-5:]}")

def import_content(args):
    """Import content from a markdown file"""
    try:
        # Read the markdown file
        with open(args.file, 'r') as f:
            content = f.read()
        
        # Use the serverless backend to import content
        params = {
            'product': args.product,
            'topic': args.topic or os.path.splitext(os.path.basename(args.file))[0],
            'content': content
        }
        
        logger.info(f"Importing content from {args.file} to product '{args.product}'")
        if args.topic:
            logger.info(f"Using specified topic: {args.topic}")
        else:
            logger.info(f"Using filename as topic: {params['topic']}")
            
        result = call_serverless_api('import', params)
        logger.info(f"Import result: {result}")
        
        if result.get('success', False):
            logger.info(f"Successfully imported content for {args.product}")
            logger.info(f"Created {len(result.get('files_created', []))} files")
            logger.info(f"Sections found: {', '.join(result.get('sections_found', []))}")
            logger.info(f"Vectors indexed: {result.get('vectors_indexed', 0)}")
        else:
            logger.error(f"Failed to import content: {result.get('error_message', 'Unknown error')}")
            return 1
            
        return 0
    except Exception as e:
        logger.error(f"Error importing content: {str(e)}")
        return 1

def search_content(args):
    """Search for content using semantic search"""
    try:
        params = {
            'query': args.query,
            'product': args.product,
            'topic': args.topic,
            'limit': args.limit
        }
        
        logger.info(f"Searching for: {args.query}")
        result = call_serverless_api('search', params)
        
        if result.get('results'):
            logger.info(f"Found {len(result['results'])} results:")
            for i, item in enumerate(result['results'], 1):
                print(f"\n{i}. {item.get('title', 'Untitled')} (Score: {item.get('score', 0):.2f})")
                print(f"   Path: {item.get('path', 'Unknown')}")
                print(f"   Content: {item.get('content', '')[:100]}...")
        else:
            logger.info("No results found")
            
        return 0
    except Exception as e:
        logger.error(f"Error searching content: {str(e)}")
        return 1

def get_content(args):
    """Get content by path"""
    try:
        # Build params with only required fields
        params = {
            'product': args.product,
            'topic': args.topic
        }
        
        # Add optional parameters if provided
        if args.section:
            params['section'] = args.section
        if args.item:
            params['item'] = args.item
        if hasattr(args, 'include_vector_info') and args.include_vector_info:
            params['include_vector_info'] = True
        
        # Construct path for logging
        path = f"{args.product}/{args.topic}"
        if args.section:
            path += f"/{args.section}"
            if args.item:
                path += f"/{args.item}"
        
        logger.info(f"Getting content for: {path}")
        result = call_serverless_api('get', params)
        
        if result.get('content'):
            # Format output based on user preference
            if hasattr(args, 'format') and args.format == 'json':
                # Return full JSON response
                import json
                print(json.dumps(result, indent=2))
            else:
                # Default: just print the content as markdown
                print(result['content'])
            
            logger.info("Content retrieved successfully")
        else:
            logger.error(f"Failed to get content: {result.get('error_message', 'Content not found')}")
            return 1
            
        return 0
    except Exception as e:
        logger.error(f"Error getting content: {str(e)}")
        return 1

def update_content(args):
    """Update existing content"""
    try:
        # Get content either from file or direct input
        content = None
        if args.file:
            with open(args.file, 'r') as f:
                content = f.read()
        elif args.content:
            content = args.content
        else:
            logger.error("No content provided. Use --file to specify a markdown file or --content to provide content directly.")
            return 1
        
        # Build params with only required fields
        params = {
            'product': args.product,
            'topic': args.topic,
            'content': content,
            'create_if_not_exists': True  # Add flag to create section if it doesn't exist
        }
        
        # Add optional parameters if provided
        if args.section:
            params['section'] = args.section
        if args.item:
            params['item'] = args.item
        
        # Construct path for logging
        path = f"{args.product}/{args.topic}"
        if args.section:
            path += f"/{args.section}"
            if args.item:
                path += f"/{args.item}"
        else:
            path += " (section will be determined by AI)"
        
        logger.info(f"Updating content for: {path}")
        result = call_serverless_api('update', params)
        
        if result.get('success', False):
            # If AI determined the section, show it in the log
            if not args.section and result.get('section'):
                logger.info(f"AI placed content in section: {result.get('section')}")
            logger.info("Content updated successfully")
        else:
            logger.error(f"Failed to update content: {result.get('error_message', 'Unknown error')}")
            return 1
            
        return 0
    except Exception as e:
        logger.error(f"Error updating content: {str(e)}")
        return 1

def delete_content(args):
    """Delete content"""
    try:
        params = {}
        if args.product:
            params['product'] = args.product
        if args.topic:
            params['topic'] = args.topic
        
        # Add optional parameters if provided
        if args.section:
            params['section'] = args.section
        if args.item:
            params['item'] = args.item
        
        logger.info(f"Deleting content with params: {params}")
        result = call_serverless_api('delete', params)
        
        # Result will already have been checked for success by call_serverless_api
        logger.info(f"Successfully deleted content")
        logger.info(f"Deleted {result.get('objects_deleted', 0)} objects")
        logger.info(f"Deleted {result.get('vectors_deleted', 0)} vectors")
        return 0
            
    except Exception as e:
        logger.error(f"Error deleting content: {str(e)}")
        return 1

def configure_serverless_backend(args):
    """Configure serverless backend with function URL and API key"""
    try:
        from brainlift.serverless.client import configure_serverless
        configure_serverless(args.function_url, args.api_key)
        logger.info(f"Successfully configured serverless backend with URL: {args.function_url}")
        return 0
    except Exception as e:
        logger.error(f"Error configuring serverless backend: {str(e)}")
        return 1

def generate_content(args):
    """Generate structured content from raw input"""
    try:
        params = {
            'product': args.product,
            'topic': args.topic,
            'content': args.content,
            'version': args.version
        }
        
        if args.file:
            with open(args.file, 'r') as f:
                params['content'] = f.read()
        
        logger.info(f"Generating structured content using template version {args.version}")
        result = call_serverless_api('generate', params)
        
        if result.get('success', False):
            logger.info(f"Successfully generated content")
            print(result.get('content', ''))
        else:
            logger.error(f"Failed to generate content: {result.get('error_message', 'Unknown error')}")
            return 1
            
        return 0
    except Exception as e:
        logger.error(f"Error generating content: {str(e)}")
        return 1

def list_content(args):
    """List products, topics, sections, and items"""
    try:
        # Build params with only optional fields
        params = {}
        
        # Add parameters if provided
        if args.product:
            params['product'] = args.product
        if args.topic:
            params['topic'] = args.topic
        if args.section:
            params['section'] = args.section
        
        # Determine what we're listing based on provided parameters
        if not args.product:
            logger.info("Listing all products")
        elif not args.topic:
            logger.info(f"Listing topics for product: {args.product}")
        elif not args.section:
            logger.info(f"Listing sections for topic: {args.product}/{args.topic}")
        else:
            logger.info(f"Listing items for section: {args.product}/{args.topic}/{args.section}")
        
        result = call_serverless_api('list', params)
        
        if result.get('success', False):
            level = result.get('level')
            
            if level == 'products':
                products = result.get('products', [])
                if products:
                    print("\nAvailable products:")
                    for product in products:
                        print(f"  - {product}")
                else:
                    print("No products found")
                    
            elif level == 'topics':
                topics = result.get('topics', [])
                if topics:
                    print(f"\nTopics for product '{result.get('product')}':")
                    for topic in topics:
                        print(f"  - {topic}")
                else:
                    print(f"No topics found for product '{result.get('product')}'") 
                    
            elif level == 'sections':
                sections = result.get('sections', [])
                items = result.get('items', {})
                
                if sections:
                    print(f"\nSections for topic '{result.get('product')}/{result.get('topic')}':")
                    for section in sections:
                        print(f"  - {section}")
                else:
                    print(f"No sections found for topic '{result.get('product')}/{result.get('topic')}'")
                
                if items:
                    print(f"\nItems by section:")
                    for section, section_items in items.items():
                        print(f"  {section}:")
                        for item in section_items:
                            print(f"    - {item}")
                            
            elif level == 'items':
                items = result.get('items', [])
                if items:
                    print(f"\nItems for section '{result.get('product')}/{result.get('topic')}/{result.get('section')}':")
                    for item in items:
                        print(f"  - {item}")
                else:
                    print(f"No items found for section '{result.get('product')}/{result.get('topic')}/{result.get('section')}'")
        else:
            logger.error(f"Failed to list content: {result.get('error_message', 'Unknown error')}")
            return 1
            
        return 0
    except Exception as e:
        logger.error(f"Error listing content: {str(e)}")
        return 1

def main():
    """Main entry point for the CLI"""
    # Create argument parser
    parser = argparse.ArgumentParser(description='BLM - BrainLift Manager (Serverless CLI)')
    
    # Add global verbose flag
    parser.add_argument('--verbose', choices=['INFO', 'DEBUG'], help='Set logging level for more detailed output')
    
    # Set logging level based on verbose flag
    args, remaining = parser.parse_known_args()
    if args.verbose:
        if args.verbose == 'INFO':
            logger.setLevel(logging.INFO)
        elif args.verbose == 'DEBUG':
            logger.setLevel(logging.DEBUG)
    
    # Reset parser for full command parsing
    parser = argparse.ArgumentParser(description='BLM - BrainLift Manager (Serverless CLI)')
    parser.add_argument('--verbose', choices=['INFO', 'DEBUG'], help='Set logging level for more detailed output')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Import command
    import_parser = subparsers.add_parser('import', help='Import content from file')
    import_parser.add_argument('file', help='Path to markdown file')
    import_parser.add_argument('--product', required=True, help='Product name')
    import_parser.add_argument('--topic', help='Topic name (defaults to filename)')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for content')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--product', help='Filter by product')
    search_parser.add_argument('--topic', help='Filter by topic')
    search_parser.add_argument('--limit', type=int, default=10, help='Maximum number of results')
    
    # Get command
    get_parser = subparsers.add_parser('get', help='Get content by path')
    get_parser.add_argument('--product', required=True, help='Product name')
    get_parser.add_argument('--topic', required=True, help='Topic name')
    get_parser.add_argument('--section', help='Section name (optional)')
    get_parser.add_argument('--item', help='Item name (optional)')
    get_parser.add_argument('--format', choices=['markdown', 'json'], default='markdown', help='Output format (default: markdown)')
    get_parser.add_argument('--include-vector-info', action='store_true', help='Include vector information in JSON output')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update content')
    update_parser.add_argument('--product', required=True, help='Product name')
    update_parser.add_argument('--topic', required=True, help='Topic name')
    update_parser.add_argument('--section', help='Section name (optional, will be determined by AI if not provided)')
    update_parser.add_argument('--item', help='Item name (optional)')
    update_content_group = update_parser.add_mutually_exclusive_group(required=True)
    update_content_group.add_argument('--file', help='Path to markdown file with new content')
    update_content_group.add_argument('--content', help='Direct content input as a string')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete content')
    delete_parser.add_argument('--product', help='Product name (optional, if not provided will delete all content)')
    delete_parser.add_argument('--topic', help='Topic name (optional, if not provided will delete all topics for the product)')
    delete_parser.add_argument('--section', help='Section name')
    delete_parser.add_argument('--item', help='Item name')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List products, topics, sections, and items')
    list_parser.add_argument('--product', help='Product name (optional)')
    list_parser.add_argument('--topic', help='Topic name (optional)')
    list_parser.add_argument('--section', help='Section name (optional)')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate structured content from raw input')
    generate_parser.add_argument('--product', required=True, help='Product name')
    generate_parser.add_argument('--topic', required=True, help='Topic name')
    generate_parser.add_argument('-v', '--version', default='v3', help='Template version to use (default: v3)')
    generate_content_group = generate_parser.add_mutually_exclusive_group(required=True)
    generate_content_group.add_argument('--file', help='Path to markdown file with raw content')
    generate_content_group.add_argument('--content', help='Direct content input as a string')
    
    # Configure serverless command
    configure_parser = subparsers.add_parser('configure-serverless', help='Configure serverless backend')
    configure_parser.add_argument('--function-url', required=True, help='Lambda function URL')
    configure_parser.add_argument('--api-key', required=True, help='API key for authentication')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Set logging level based on verbose flag
    if hasattr(args, 'verbose') and args.verbose:
        if args.verbose == 'INFO':
            logger.setLevel(logging.INFO)
        elif args.verbose == 'DEBUG':
            logger.setLevel(logging.DEBUG)
    
    # Load environment variables
    load_env()
    
    # Execute command
    if args.command == 'import':
        return import_content(args)
    elif args.command == 'search':
        return search_content(args)
    elif args.command == 'get':
        return get_content(args)
    elif args.command == 'update':
        return update_content(args)
    elif args.command == 'delete':
        return delete_content(args)
    elif args.command == 'list':
        return list_content(args)
    elif args.command == 'generate':
        return generate_content(args)
    elif args.command == 'configure-serverless':
        return configure_serverless_backend(args)
    else:
        parser.print_help()
        return 1

if __name__ == '__main__':
    sys.exit(main())
