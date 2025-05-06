# OpenAI Image Generator

A command-line tool that uses OpenAI's DALL-E models to generate images based on text prompts.

## Features

- Support for both DALL-E 2 and DALL-E 3 models
- Multiple image size options based on the selected model
- Generate multiple images at once
- Images automatically saved to a local directory
- Simple interactive command-line interface

## Requirements

- Python 3.6+
- tkinter (Python's standard GUI package)
- OpenAI API key

## Setup

### Quick Setup

Run the setup script to quickly set up the project:

```bash
./setup.sh
```

### Manual Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/carmandale/image-gen.git
   cd image-gen
   ```

2. Ensure tkinter is installed:
   ```bash
   # On Ubuntu/Debian
   sudo apt-get install python3-tk
   
   # On Fedora
   sudo dnf install python3-tkinter
   
   # On macOS (using Homebrew)
   brew install python-tk
   
   # On Windows
   # tkinter is included with standard Python installations
   ```

3. Create a virtual environment:
   ```bash
   # Using Python's venv
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
   # Or using uv
   uv venv
   source .venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   # Using pip
   pip install -r requirements.txt
   
   # Or using uv
   uv pip install -r requirements.txt
   ```

5. Create a `.env` file in the project root with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
   
   You can copy the provided `.env.example` file:
   ```bash
   cp .env.example .env
   # Then edit .env to add your API key
   ```

## Usage

Run the script:

```bash
python openai_image_generator.py
```

Follow the interactive prompts:

1. Select a model (DALL-E 2 or DALL-E 3)
2. Choose an image size
3. Enter your prompt describing the image you want
4. Specify how many images to generate (1-10)

Generated images will be saved in a `DALL-E` folder within the project directory.

## Example Prompts

Here are some example prompts that work well with DALL-E:

### For Landscapes:
```
A serene mountain lake at sunset with pine trees and snow-capped peaks reflected in the still water
```

### For Abstract Art:
```
Abstract digital art representing the concept of artificial intelligence, with flowing data patterns in blue and purple
```

### For Character Design:
```
A friendly robot assistant with rounded features, big expressive eyes, in a modern office setting
```

## Troubleshooting

### API Key Issues
- Ensure your OpenAI API key is valid and has not expired
- Check that you have sufficient credits in your OpenAI account
- Verify that the API key is properly set in your `.env` file

### Image Generation Failures
- Check your internet connection
- The script has a 30-second timeout for API requests - if your connection is slow, try again
- Very complex or lengthy prompts might fail - try simplifying your prompt
- Ensure you're not requesting inappropriate content (which OpenAI filters will block)

### Installation Issues
- If tkinter is not found, install it using the commands in the Setup section
- Virtual environment issues? Try removing the `.venv` directory and creating it again

## OpenAI API Usage Notes

This tool uses OpenAI's API which has:
- Rate limits on the number of requests
- Costs associated with image generation (varies by model and size)
- Content moderation filters

Please review [OpenAI's pricing](https://openai.com/pricing) and [usage policies](https://openai.com/policies/usage-policies) for more information.

## License

[MIT License](LICENSE)
