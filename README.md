# Nano Banana MCP Server

A Model Context Protocol (MCP) server for AI-powered image generation using Google's Gemini 2.5 Flash Image Preview model. This server enables text-to-image and image-to-image generation through the MCP interface.

## Features

- **Text-to-Image Generation**: Generate images from text prompts
- **Image-to-Image Generation**: Create variations or modifications of existing images
- **Base64 Support**: Handle image data in base64 format for MCP compatibility
- **Google AI Studio Integration**: Uses Google's latest Gemini 2.5 Flash Image Preview model
- **Error Handling**: Comprehensive error handling and logging
- **Environment Variable Support**: Secure API key management

## Prerequisites

- Python 3.7+
- Google AI Studio API key
- Internet connection for API calls

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Google AI Studio API key:
   ```bash
   export GOOGLE_AI_STUDIO_API_KEY="your_api_key_here"
   ```

## Configuration

### MCP Configuration

Add the following to your MCP configuration file:

```json
{
  "mcpServers": {
    "nano-banana": {
      "command": "python3",
      "args": ["nano_banana_server.py"],
      "env": {
        "GOOGLE_AI_STUDIO_API_KEY": "${GOOGLE_AI_STUDIO_API_KEY}"
      }
    }
  }
}
```

### Environment Variables

- `GOOGLE_AI_STUDIO_API_KEY`: Your Google AI Studio API key (required)

## Usage

### MCP Tool Function

The server provides a single MCP tool function:

#### `generate_image_with_nano_banana`

Generate images using Google's Gemini 2.5 Flash Image Preview model.

**Parameters:**
- `prompt` (string, required): Text description of the image to generate
- `input_image_b64` (string, optional): Base64 encoded input image for variations
- `input_image_mime_type` (string, optional): MIME type of input image (e.g., 'image/png', 'image/jpeg')

**Returns:**
- `success` (boolean): Whether the generation was successful
- `generated_image_b64` (string): Base64 encoded generated image (if successful)
- `generated_image_size` (integer): Size of generated image in bytes
- `model_used` (string): Name of the model used ("gemini-2.5-flash-image-preview")
- `error` (string): Error message (if failed)

### Example Usage

#### Text-to-Image Generation
```python
result = await generate_image_with_nano_banana(
    prompt="A beautiful handcrafted ceramic bowl with intricate patterns"
)
```

#### Image-to-Image Generation
```python
result = await generate_image_with_nano_banana(
    prompt="Transform this into a watercolor painting",
    input_image_b64="iVBORw0KGgoAAAANSUhEUgAA...",  # Base64 encoded image
    input_image_mime_type="image/png"
)
```

### Testing

Run the test function to verify the server is working:

```bash
python nano_banana_server.py
```

This will generate a test image and display the results.

## API Reference

### Classes

#### `ImageGenerationRequest`
Data class for image generation requests.

**Attributes:**
- `prompt` (str): Text prompt for image generation
- `input_image_data` (Optional[bytes]): Raw image data
- `input_image_mime_type` (Optional[str]): MIME type of input image

#### `ImageGenerationResponse`
Data class for image generation responses.

**Attributes:**
- `success` (bool): Whether generation was successful
- `generated_image_data` (Optional[bytes]): Generated image data
- `error_message` (Optional[str]): Error message if failed
- `model_used` (str): Model name used for generation

#### `NanoBananaMCPServer`
Main server class for handling image generation.

**Methods:**
- `__init__(api_key: Optional[str] = None)`: Initialize server with API key
- `generate_image(request: ImageGenerationRequest) -> ImageGenerationResponse`: Generate image from request
- `generate_image_from_base64(prompt: str, input_image_b64: Optional[str] = None, input_image_mime_type: Optional[str] = None) -> Dict[str, Any]`: Generate image with base64 input
