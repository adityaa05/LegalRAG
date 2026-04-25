#!/usr/bin/env python3
"""Test Gemini API directly to find working model."""

import google.generativeai as genai

api_key = "AIzaSyDd-lZhiaMojYL8_QMlt6s0PeAoClJipAA"
genai.configure(api_key=api_key)

print("Testing Gemini API...")
print("=" * 60)

# List available models
print("\n1. Listing available models:")
try:
    models = genai.list_models()
    available_models = []
    for m in models:
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)
            print(f"   ✓ {m.name}")
    
    if not available_models:
        print("   No models found with generateContent support")
        print("   Your API key might not have access to Gemini models")
        print("\n   Try getting a new API key from: https://makersuite.google.com/app/apikey")
        exit(1)
    
    # Try the first available model
    model_name = available_models[0]
    print(f"\n2. Testing model: {model_name}")
    
    model = genai.GenerativeModel(model_name)
    response = model.generate_content("Say 'Hello, I am working!'")
    
    print(f"\n3. Success! Model response:")
    print(f"   {response.text}")
    print(f"\n✓ Use this model name: {model_name}")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nYour API key might be:")
    print("  1. Invalid or expired")
    print("  2. Not enabled for Gemini API")
    print("  3. Rate limited")
    print("\nGet a new key from: https://makersuite.google.com/app/apikey")
