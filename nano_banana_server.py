import asyncio
import base64
import json
import os
import sys
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from google.genai import Client, types
except ImportError:
    print("Error: google-genai package not found. Install with: pip install google-genai")
    sys.exit(1)

@dataclass
class ImageGenerationRequest:
    """Request for image generation."""
    prompt: str
    input_image_data: Optional[bytes] = None
    input_image_mime_type: Optional[str] = None

@dataclass
class ImageGenerationResponse:
    """Response from image generation."""
    success: bool
    generated_image_data: Optional[bytes] = None
    error_message: Optional[str] = None
    model_used: str = "gemini-2.5-flash-image-preview"

class NanoBananaMCPServer:
    """MCP Server for Nano Banana image generation."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the MCP server.
        
        Args:
            api_key: Google AI Studio API key. If None, reads from GOOGLE_AI_STUDIO_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("GOOGLE_AI_STUDIO_API_KEY")
        if not self.api_key:
            raise ValueError("Google AI Studio API key is required. Set GOOGLE_AI_STUDIO_API_KEY environment variable.")
        
        self.model_name = "gemini-2.5-flash-image-preview"
        self.client = None
        
    async def _get_client(self) -> Client:
        """Get or create the AI Studio client."""
        if self.client is None:
            self.client = Client(api_key=self.api_key)
            print("✅ Nano Banana MCP Server: Created AI Studio client")
        
        return self.client
    
    async def generate_image(self, request: ImageGenerationRequest) -> ImageGenerationResponse:
        """Generate an image using Nano Banana.
        
        Args:
            request: Image generation request with prompt and optional input image
            
        Returns:
            ImageGenerationResponse with generated image data or error
        """
        try:
            print(f"🎨 Nano Banana MCP: Generating image with prompt: {request.prompt[:100]}...")
            
            client = await self._get_client()
            
            # Prepare content for the model
            contents = [request.prompt]
            
            # Add input image if provided
            if request.input_image_data:
                print(f"📷 Nano Banana MCP: Using input image ({len(request.input_image_data)} bytes)")
                image_part = types.Part.from_bytes(
                    data=request.input_image_data,
                    mime_type=request.input_image_mime_type or "image/png"
                )
                contents.append(image_part)
            
            # Generate content
            response = client.models.generate_content(
                model=self.model_name,
                contents=contents,
            )
            
            print(f"✅ Nano Banana MCP: Received response with {len(response.candidates)} candidates")
            
            # Extract generated image
            generated_image_data = None
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data is not None:
                    if hasattr(part.inline_data, 'data') and part.inline_data.data:
                        generated_image_data = part.inline_data.data
                        print(f"✅ Nano Banana MCP: Extracted generated image ({len(generated_image_data)} bytes)")
                        break
            
            if generated_image_data:
                return ImageGenerationResponse(
                    success=True,
                    generated_image_data=generated_image_data,
                    model_used=self.model_name
                )
            else:
                return ImageGenerationResponse(
                    success=False,
                    error_message="No image data found in model response"
                )
                
        except Exception as e:
            print(f"Nano Banana MCP: Error generating image: {str(e)}")
            return ImageGenerationResponse(
                success=False,
                error_message=f"Image generation failed: {str(e)}"
            )
    
    async def generate_image_from_base64(self, prompt: str, input_image_b64: Optional[str] = None, 
                                       input_image_mime_type: Optional[str] = None) -> Dict[str, Any]:
        """Generate image with base64 input (MCP tool interface).
        
        Args:
            prompt: Text prompt for image generation
            input_image_b64: Optional base64 encoded input image
            input_image_mime_type: MIME type of input image
            
        Returns:
            Dictionary with success status and base64 encoded generated image
        """
        # Decode base64 input image if provided
        input_image_data = None
        if input_image_b64:
            try:
                input_image_data = base64.b64decode(input_image_b64)
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to decode base64 input image: {str(e)}"
                }
        
        # Create request
        request = ImageGenerationRequest(
            prompt=prompt,
            input_image_data=input_image_data,
            input_image_mime_type=input_image_mime_type
        )
        
        # Generate image
        response = await self.generate_image(request)
        
        # Prepare result
        result = {
            "success": response.success,
            "model_used": response.model_used
        }
        
        if response.success and response.generated_image_data:
            result["generated_image_b64"] = base64.b64encode(response.generated_image_data).decode('utf-8')
            result["generated_image_size"] = len(response.generated_image_data)
        else:
            result["error"] = response.error_message
        
        return result

# MCP Tool Functions
async def generate_image_with_nano_banana(
    prompt: str,
    input_image_b64: Optional[str] = None,
    input_image_mime_type: Optional[str] = None
) -> Dict[str, Any]:
    """MCP tool function for generating images with Nano Banana.
    
    Args:
        prompt: Text prompt describing what image to generate
        input_image_b64: Optional base64 encoded input image for variations
        input_image_mime_type: MIME type of input image (e.g., 'image/png', 'image/jpeg')
        
    Returns:
        Dictionary with:
        - success: bool indicating if generation was successful
        - generated_image_b64: base64 encoded generated image (if successful)
        - generated_image_size: size of generated image in bytes
        - model_used: name of the model used
        - error: error message (if failed)
    """
    server = NanoBananaMCPServer()
    return await server.generate_image_from_base64(prompt, input_image_b64, input_image_mime_type)

# Test function
async def test_nano_banana_server():
    """Test the Nano Banana MCP server."""
    print("🧪 Testing Nano Banana MCP Server...")
    
    # Test without input image (text-to-image)
    result = await generate_image_with_nano_banana(
        prompt="A beautiful handcrafted ceramic bowl with intricate patterns"
    )
    
    print(f"Text-to-image result: {result['success']}")
    if result['success']:
        print(f"Generated image size: {result['generated_image_size']} bytes")
    else:
        print(f"Error: {result['error']}")
    
    return result

if __name__ == "__main__":
    # Run test if executed directly
    asyncio.run(test_nano_banana_server())
