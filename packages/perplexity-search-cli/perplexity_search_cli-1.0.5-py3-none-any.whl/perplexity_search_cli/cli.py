#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import os
import sys
import argparse
import requests
import json
import datetime

def main():
    parser = argparse.ArgumentParser(description='Perplexity API CLI')
    parser.add_argument('-p', '--prompt', help='Prompt to send to Perplexity API')
    parser.add_argument('-k', '--api-key', help='Perplexity API key (or set PPLX_API_KEY env var)')
    parser.add_argument('-o', '--output', help='Path to save full JSON response')
    parser.add_argument('--params', help='Additional API parameters as JSON string')
    args = parser.parse_args()

    api_key = args.api_key or os.getenv('PPLX_API_KEY', None)
    if not api_key:
        print("Error: API key is required but not found.", file=sys.stderr)
        print("Please either:", file=sys.stderr)
        print("1. Set the PPLX_API_KEY environment variable", file=sys.stderr)
        print("2. Or provide the API key via --api-key argument", file=sys.stderr)
        print("You can get an API key from https://perplexity.ai", file=sys.stderr)
        sys.exit(1)

    prompt = args.prompt
    if not prompt:
        # Read from stdin if no prompt argument
        if sys.stdin.isatty():
            print("\n=== PERPLEXITY CLI ===", file=sys.stderr)
            print("Please enter your query (press Ctrl+D when done):", file=sys.stderr)
        prompt = sys.stdin.read().strip()
        if sys.stdin.isatty():
            print("\n=== Processing your query... ===\n", file=sys.stderr)
        if not prompt:
            print("Error: No prompt provided", file=sys.stderr)
            sys.exit(1)

    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    # Base payload
    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": "Be precise and concise."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    # Merge additional parameters if provided
    if args.params:
        try:
            additional_params = json.loads(args.params)
            payload.update(additional_params)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON parameters: {e}", file=sys.stderr)
            sys.exit(1)

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        # Save full JSON response if output path specified
        if args.output:
            try:
                with open(args.output, 'w') as f:
                    json.dump(result, f, indent=2)
            except Exception as e:
                print(f"Error saving output file: {e}", file=sys.stderr)
                sys.exit(1)
                
        print(result.get('choices', [{}])[0].get('message', {}).get('content', ''))
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
