#!/usr/bin/env python3
"""Check available Gemini models for your API key."""

import google.generativeai as genai

api_key = "AIzaSyDd-lZhiaMojYL8_QMlt6s0PeAoClJipAA"
genai.configure(api_key=api_key)

print("Available Gemini models:")
print("=" * 60)

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✓ {model.name}")
        print(f"  Display name: {model.display_name}")
        print(f"  Description: {model.description[:80]}...")
        print()
