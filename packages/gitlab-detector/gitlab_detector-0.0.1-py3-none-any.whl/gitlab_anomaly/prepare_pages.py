"""
Main orchestrator module for generating the HTML report.
Imports and uses functionality from page_generator modules to create the report.
"""

import sys
import os
import logging
from jinja2 import Environment, FileSystemLoader

from page_generator.data_loader import _read_data, load_environment_variables
from page_generator.css_generator import generate_css
from page_generator.js_view_logic import generate_view_logic
from page_generator.js_rendering import generate_rendering
from page_generator.js_event_listeners import generate_event_listeners

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def _generate_javascript():
    """Generates the complete JavaScript by combining all components."""
    logger.debug("Generating complete JavaScript...")
    js_parts = [
        "'use strict';",  # Enable strict mode for the entire script
        generate_view_logic(),  # Core view switching and UI logic
        generate_rendering(),   # UI rendering functions
        generate_event_listeners(),  # Event handling
        "initializeReport();"   # Trigger the initialization process
    ]
    js_content = "\n\n".join(js_parts)
    logger.debug("Complete JavaScript content generated.")
    return js_content

def update_index_html(output_dir='public', data_filename='data.json'):
    """
    Reads anomaly data, generates CSS, JS, and HTML using granular functions and Jinja2 templates,
    and writes index.html.

    Args:
        output_dir (str): The directory to save the output files.
        data_filename (str): The name of the data file within the output directory.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Ensured output directory exists: {output_dir}")
    except OSError as e:
        logger.critical(f"Could not create output directory {output_dir}: {e}", exc_info=True)
        return  # Stop if we can't create the directory

    # Load environment variables (if needed)
    env_vars = load_environment_variables()
    logger.debug("Environment variables loaded")

    html_filepath = os.path.join(output_dir, 'index.html')
    logger.info(f"Preparing to generate HTML report at: {html_filepath}")

    # Set up Jinja2 environment
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # Get the templates
    base_template = env.get_template('base.html')
    content_template = env.get_template('content.html')
    
    # Generate CSS and JavaScript content
    css_content = generate_css()
    javascript_content = _generate_javascript()
    
    # Render the content template
    content_html = content_template.render()
    
    # Render the base template with the generated content
    html_content = base_template.render(
        css=css_content,
        javascript=javascript_content,
        content=content_html
    )

    try:
        logger.info(f"Writing HTML to {html_filepath}...")
        with open(html_filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logger.info(f"Successfully updated {html_filepath}")
    except IOError as e:
        logger.error(f"Error writing {html_filepath}: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"An unexpected error occurred during HTML generation/writing: {e}", exc_info=True)

def main():
    """Main entry point for generating the report."""
    logger.info("Starting report generation process...")
    update_index_html()
    logger.info("Report generation process finished.")

if __name__ == "__main__":
    main()
