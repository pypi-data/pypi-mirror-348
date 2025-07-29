#!/usr/bin/env python3
"""
Test suite for OpenAI Node
"""

import logging
import asyncio
import os
import time
from typing import Dict, Any, List

# Import the OpenAI Node
from openai_node import OpenAINode, OpenAIOperation, OpenAIModelType

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def run_tests():
    """Run test suite for OpenAI node."""
    print("=== OpenAI Node Test Suite ===")
    
    # Get API key from environment or user input
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        api_key = input("Enter OpenAI API key: ")
        if not api_key:
            print("API key is required for testing")
            return
    
    # Create an instance of the OpenAI Node
    node = OpenAINode()
    
    # Test cases - only run if API key provided
    test_cases = [
        {
            "name": "Chat Completion - GPT-4o",
            "params": {
                "operation": OpenAIOperation.CHAT_COMPLETION,
                "api_key": api_key,
                "model": "gpt-4o",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Hello, tell me briefly about OpenAI's different model types."}
                ],
                "temperature": 0.7,
                "max_tokens": 150
            },
            "expected_status": "success"
        },
        {
            "name": "Chat Completion - Reasoning Model o3-mini",
            "params": {
                "operation": OpenAIOperation.CHAT_COMPLETION,
                "api_key": api_key,
                "model": "o3-mini",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "What is the square root of 169 and why?"}
                ],
                "max_completion_tokens": 250,  # Only include max_completion_tokens
                "reasoning_effort": "medium"   # And reasoning_effort parameter
            },
            "expected_status": "success"
        },
        {
            "name": "Embedding - text-embedding-3-small",
            "params": {
                "operation": OpenAIOperation.EMBEDDING,
                "api_key": api_key,
                "model": "text-embedding-3-small",
                "input": "The quick brown fox jumps over the lazy dog."
            },
            "expected_status": "success"
        },
        {
            "name": "Moderation - text-moderation-latest",
            "params": {
                "operation": OpenAIOperation.MODERATION,
                "api_key": api_key,
                "model": "text-moderation-latest",
                "moderation_input": "I want to harm someone."
            },
            "expected_status": "success"
        },
        {
            "name": "Models List",
            "params": {
                "operation": OpenAIOperation.MODELS_LIST,
                "api_key": api_key
            },
            "expected_status": "success"
        }
    ]
    
    # Run all test cases with a delay between tests
    total_tests = len(test_cases)
    passed_tests = 0
    
    for test_case in test_cases:
        print(f"\nRunning test: {test_case['name']}")
        
        try:
            # Prepare node data
            node_data = {
                "params": test_case["params"]
            }
            
            # Execute the node
            result = await node.execute(node_data)
            
            # Check if the result status matches expected status
            if result["status"] == test_case["expected_status"]:
                print(f"✅ PASS: {test_case['name']} - Status: {result['status']}")
                if result["result"]:
                    if isinstance(result["result"], dict):
                        print(f"Response preview: {str(result['result'])[:150]}...")
                    else:
                        print(f"Response preview: {str(result['result'])[:150]}...")
                passed_tests += 1
            else:
                print(f"❌ FAIL: {test_case['name']} - Expected status {test_case['expected_status']}, got {result['status']}")
                print(f"Error: {result.get('error')}")
                
            # Add a delay between tests to avoid rate limiting
            await asyncio.sleep(2.0)
            
        except Exception as e:
            print(f"❌ FAIL: {test_case['name']} - Exception: {str(e)}")
    
    # Print summary
    print(f"\n=== Test Summary ===")
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success rate: {passed_tests / total_tests * 100:.1f}%")
    
    # Also test the operation parameters helper function
    print("\n=== Testing Operation Parameters Helper ===")
    chat_params = node.get_operation_parameters(OpenAIOperation.CHAT_COMPLETION)
    embedding_params = node.get_operation_parameters(OpenAIOperation.EMBEDDING)
    print(f"Chat completion has {len(chat_params)} relevant parameters")
    print(f"Embedding has {len(embedding_params)} relevant parameters")
    
    # Manual tests (optional based on user input)
    run_manual_tests = input("\nRun optional manual tests? (y/n): ").lower() == 'y'
    
    if run_manual_tests:
        # Image generation test
        run_image_test = input("\nRun image generation test? (y/n): ").lower() == 'y'
        if run_image_test:
            print("\n=== Manual Test: Image Generation (DALL-E) ===")
            image_prompt = input("Enter an image generation prompt: ")
            if not image_prompt:
                image_prompt = "A photorealistic image of a futuristic city with flying cars and tall skyscrapers, digital art style."
            
            image_result = await node.execute({
                "params": {
                    "operation": OpenAIOperation.IMAGE_GENERATION,
                    "api_key": api_key,
                    "model": "dall-e-3",
                    "prompt": image_prompt,
                    "size": "1024x1024",
                    "quality": "standard",
                    "style": "vivid",
                    "image_n": 1
                }
            })
            
            if image_result["status"] == "success":
                print("✅ Image generation successful")
                if "data" in image_result["result"] and len(image_result["result"]["data"]) > 0:
                    print(f"Image URL: {image_result['result']['data'][0]['url']}")
                else:
                    print("No image data returned")
            else:
                print(f"❌ Image generation failed: {image_result.get('error')}")
        
        # Text-to-speech test
        run_tts_test = input("\nRun text-to-speech test? (y/n): ").lower() == 'y'
        if run_tts_test:
            print("\n=== Manual Test: Text-to-Speech ===")
            tts_text = input("Enter text to convert to speech: ")
            if not tts_text:
                tts_text = "Hello, this is a test of the OpenAI text to speech API. How does this sound to you?"
            
            tts_result = await node.execute({
                "params": {
                    "operation": OpenAIOperation.TEXT_TO_SPEECH,
                    "api_key": api_key,
                    "model": "tts-1",
                    "tts_text": tts_text,
                    "tts_voice": "alloy",
                    "tts_speed": 1.0,
                    "tts_response_format": "mp3"
                }
            })
            
            if tts_result["status"] == "success":
                print("✅ Text-to-speech conversion successful")
                print("Audio data size: ", len(tts_result["result"]["audio_data"]) if "audio_data" in tts_result["result"] else "N/A")
                
                # Save the audio file if requested
                save_audio = input("Save audio to file? (y/n): ").lower() == 'y'
                if save_audio and "audio_data" in tts_result["result"]:
                    file_name = "tts_output.mp3"
                    with open(file_name, "wb") as f:
                        f.write(tts_result["result"]["audio_data"])
                    print(f"Audio saved to {file_name}")
            else:
                print(f"❌ Text-to-speech conversion failed: {tts_result.get('error')}")
        
        # Audio transcription test
        run_audio_test = input("\nRun audio transcription test? (y/n): ").lower() == 'y'
        if run_audio_test:
            print("\n=== Manual Test: Audio Transcription ===")
            audio_file = input("Enter path to audio file (mp3, mp4, mpeg, mpga, m4a, wav, or webm): ")
            if not audio_file:
                print("No audio file provided, skipping test")
            elif not os.path.exists(audio_file):
                print(f"File not found: {audio_file}")
            else:
                audio_result = await node.execute({
                    "params": {
                        "operation": OpenAIOperation.AUDIO_TRANSCRIPTION,
                        "api_key": api_key,
                        "model": "whisper-1",
                        "audio_file": audio_file,
                        "audio_response_format": "json"
                    }
                })
                
                if audio_result["status"] == "success":
                    print("✅ Audio transcription successful")
                    print(f"Transcription: {audio_result['result'].get('text', '')[:200]}...")
                else:
                    print(f"❌ Audio transcription failed: {audio_result.get('error')}")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    # Run the async tests
    asyncio.run(run_tests())