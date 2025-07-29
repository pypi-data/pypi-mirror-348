import os
import json
import requests
import logging
import configparser
from pathlib import Path

logger = logging.getLogger(__name__)

CONFIG_DIR = Path.home() / '.brain-lift'
CONFIG_FILE = CONFIG_DIR / 'config'

def load_config():
    """Load configuration from config file"""
    config = configparser.ConfigParser()
    
    if CONFIG_FILE.exists():
        config.read(CONFIG_FILE)
    
    # Ensure sections exist
    if 'serverless' not in config:
        config['serverless'] = {}
    
    return config

def save_config(config):
    """Save configuration to config file"""
    CONFIG_DIR.mkdir(exist_ok=True)
    
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)

def get_api_key():
    """Get API key from config file or environment variable"""
    # Check environment variable first
    api_key = os.environ.get('BRAINLIFT_API_KEY')
    if api_key:
        return api_key
        
    # Check config file
    config = load_config()
    if 'serverless' in config and 'api_key' in config['serverless']:
        return config['serverless']['api_key']
            
    return None

def get_function_url():
    """Get function URL from config file or environment variable"""
    # Check environment variable first
    function_url = os.environ.get('BRAINLIFT_FUNCTION_URL')
    if function_url:
        return function_url
        
    # Check config file
    config = load_config()
    if 'serverless' in config and 'function_url' in config['serverless']:
        return config['serverless']['function_url']
            
    return None

def configure_serverless(function_url, api_key):
    """Configure serverless backend"""
    config = load_config()
    
    config['serverless']['function_url'] = function_url
    config['serverless']['api_key'] = api_key
    
    save_config(config)
    logger.info(f"Serverless backend configured: {function_url}")
    return True

def is_serverless_enabled():
    """Check if serverless backend is enabled"""
    config = load_config()
    return config.getboolean('serverless', 'enabled', fallback=False)

def enable_serverless(enabled=True):
    """Enable or disable serverless backend"""
    config = load_config()
    config['serverless']['enabled'] = str(enabled).lower()
    save_config(config)
    logger.info(f"Serverless backend {'enabled' if enabled else 'disabled'}")
    return True

def call_serverless_api(operation, params, use_path_based=True):
    """Call the BrainLift Lambda function URL with API key authentication
    
    Args:
        operation (str): The operation to perform (e.g., 'search', 'get', 'import')
        params (dict): Parameters for the operation
        use_path_based (bool): Whether to use the new path-based endpoints (default: True)
    """
    api_key = get_api_key()
    if not api_key:
        raise ValueError("API key not found. Set BRAINLIFT_API_KEY environment variable or run 'blm configure'")
    
    function_url = get_function_url()
    if not function_url:
        raise ValueError("Function URL not found. Set BRAINLIFT_FUNCTION_URL environment variable or run 'blm configure'")
    
    headers = {
        'Content-Type': 'application/json',
        'x-api-auth': api_key
    }
    logger.info(f"Using API key: {api_key}")
    logger.info(f"Headers being sent: {headers}")
    
    # Use path-based endpoints if enabled
    if use_path_based:
        # Map operations to HTTP methods and paths
        operation_map = {
            'ping': {'method': 'get', 'path': '/ping', 'use_params': False},
            'get_info': {'method': 'get', 'path': '/info', 'use_params': False},
            'search': {'method': 'post', 'path': '/search', 'use_params': True},
            'get': {'method': 'post', 'path': '/get', 'use_params': True},
            'import': {'method': 'post', 'path': '/import', 'use_params': True},
            'update': {'method': 'post', 'path': '/update', 'use_params': True},
            'delete': {'method': 'post', 'path': '/delete', 'use_params': True},
            'list': {'method': 'get', 'path': '/list', 'use_params': True},
            'generate': {'method': 'post', 'path': '/generate', 'use_params': True},
            # Legacy operations fall back to operation-based
            'store_content': {'method': 'post', 'path': '/', 'legacy': True},
            'retrieve_content': {'method': 'post', 'path': '/', 'legacy': True}
        }
        
        if operation not in operation_map:
            raise ValueError(f"Unsupported operation: {operation}")
        
        op_info = operation_map[operation]
        
        # Fall back to legacy mode for unsupported operations
        if op_info.get('legacy', False):
            return call_serverless_api(operation, params, use_path_based=False)
        
        # Build the URL
        url = function_url.rstrip('/') + op_info['path']
        method = op_info['method']
        
        # Prepare the request
        if method == 'get' and op_info['use_params']:
            # For GET requests, use query parameters
            response = requests.get(url, headers=headers, params=params)
        elif method == 'get':
            # For GET requests without params
            response = requests.get(url, headers=headers)
        else:
            # For POST requests
            payload = {'params': params} if op_info['use_params'] else {}
            response = requests.post(url, headers=headers, json=payload)
    else:
        # Legacy operation-based approach
        payload = {
            'operation': operation,
            'params': params
        }
        response = requests.post(function_url, headers=headers, json=payload)
    
    try:
        logger.info(f"Calling serverless API: {operation}")
        logger.info(f"Request URL: {response.request.url}")
        logger.info(f"Request method: {response.request.method}")
        logger.info(f"Request headers: {response.request.headers}")
        logger.info(f"Request body: {response.request.body}")
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response headers: {response.headers}")
        try:
            logger.info(f"Response body: {response.text}")
        except:
            logger.info("Could not log response body")
        
        if response.status_code != 200:
            raise Exception(f"API call failed with status {response.status_code}: {response.text}")
        
        result = response.json()
        if isinstance(result, dict) and 'body' in result:
            # Handle Lambda function URL response format
            try:
                body = json.loads(result['body'])
                if 'error' in body:
                    raise Exception(body['error'])
                return body
            except json.JSONDecodeError:
                return result['body']
        
        if 'error' in result:
            raise Exception(result['error'])
        return result
    except json.JSONDecodeError:
        raise Exception(f"Invalid JSON response: {response.text}")
    except requests.RequestException as e:
        logger.error(f"Error calling serverless API: {str(e)}")
        raise Exception(f"Failed to connect to serverless API: {str(e)}")
