# BrainLift CLI

A command-line interface for the BrainLift knowledge management system. This CLI tool allows you to interact with the BrainLift serverless backend to manage, search, and generate structured knowledge content.

## Installation

```bash
# Install from source
pip install -e .
```

### Environment Setup

Create a `.env` file in your home directory at `~/.brain-lift/.env` with the following variables:

```bash
BRAINLIFT_FUNCTION_URL=your_lambda_function_url
BRAINLIFT_API_KEY=your_api_key
```

Alternatively, you can use the `configure-serverless` command to set these values:

```bash
blm configure-serverless --function-url https://your-lambda-function-url.lambda-url.region.on.aws/ --api-key your-api-key
```

## Commands

### List Content

```bash
# List all products
blm list

# List topics in a product
blm list --product <product>

# List sections in a topic
blm list --product <product> --topic <topic>
```

### Search Content

```bash
# Search for content
blm search "your search query"

# Search within a specific product
blm search "your search query" --product <product>

# Limit search results
blm search "your search query" --limit 5
```

### Get Content

```bash
# Get content by path
blm get --product <product> --topic <topic>

# Get specific section
blm get --product <product> --topic <topic> --section <section>
```

### Import Content

```bash
# Import content from a markdown file
blm import <file.md> --product <product> --topic <topic>
```

### Update Content

```bash
# Update content
blm update --product <product> --topic <topic> --file <file.md>
```

### Delete Content

```bash
# Delete content
blm delete --product <product> --topic <topic>
```

### Generate Content

```bash
# Generate structured content from raw input
blm generate --product <product> --topic <topic> --file <file.md>

# Specify template version
blm generate --product <product> --topic <topic> --file <file.md> -v v3
```

### Content Generation Guidelines

When using the `generate` command, the system follows these principles:

1. **Factual Accuracy**: The system prioritizes factual accuracy over filling every template section. All content must be derived from the source material.

2. **DOK Structure**:
   - **DOK1 and DOK2**: Function as context packs containing factual information and foundational knowledge directly from the source material.
   - **DOK3 and DOK4**: Higher-level insights are only included when they can be genuinely derived from the content, not invented.

3. **Experts Section**: Only includes people or sources that are explicitly mentioned in the original content. If no experts are explicitly mentioned, this section should remain empty or be omitted.

4. **Purpose Section**: Clearly defines what the content is about - the core objective or focus of the material.

5. **Template Flexibility**: The template structure respects what's actually in the content rather than forcing information into categories where it doesn't exist in the source material.

## Verbose Mode

Add the `--verbose` flag to get more detailed output:

```bash
blm --verbose INFO list
blm --verbose DEBUG generate --product <product> --topic <topic> --file <file.md>
```

## Development

This CLI is a thin wrapper around the BrainLift serverless backend. It handles:

1. Command-line argument parsing
2. File I/O for content import/export
3. API calls to the serverless backend
4. Formatting and displaying results

All business logic, content processing, and storage operations are handled by the serverless backend.
