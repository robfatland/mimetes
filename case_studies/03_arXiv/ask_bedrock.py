"""
ask_bedrock.py — Send a science reasoning question to AWS Bedrock (Claude Sonnet).

Usage:
    python ask_bedrock.py

Output:
    Prints response and token usage to console.
    Writes response to bedrock_response.md
"""

import boto3
import json
from pathlib import Path

REGION = "us-west-2"
MODEL_ID = "us.anthropic.claude-sonnet-4-6"
OUTPUT_PATH = Path(__file__).parent / "bedrock_response.md"

COST_PER_1K_INPUT = 0.003
COST_PER_1K_OUTPUT = 0.015

PROMPT = """You are a glaciologist. I have the following observational context for 
the Bagley Ice Valley in south-central Alaska:

- Surface slope: approximately 1 degree (constant along the profile)
- Ice thickness: ranges from 650 to 1200 meters along an 18 km longitudinal profile
- Valley width: approximately 4 km
- The ice is temperate (at the pressure melting point, 0°C)

Using Glen's flow law (A = 2.4e-24 Pa^-3 s^-1, n=3) with a Nye shape factor 
for the valley walls, calculated deformation-only surface speed ranges from 
approximately 15 to 100 meters per year.

Observed surface speeds from ITS_LIVE satellite data range from 140 to 220 
meters per year along the same profile.

This implies basal sliding speeds varying from roughly 40 to 150 meters per year.

My questions:
1. Are there estimates in the glaciology literature for basal sliding speed 
   relevant to these values — both in magnitude and spatial variability — for 
   temperate valley glaciers of this scale?
2. What physical mechanisms would explain this range of sliding speeds?
3. Are there specific papers or datasets I should look at to compare these 
   inferred sliding rates?

Please cite specific studies where possible."""


def call_bedrock(prompt: str) -> dict:
    from botocore.config import Config

    config = Config(read_timeout=300)  # 5 minutes
    client = boto3.client("bedrock-runtime", region_name=REGION, config=config)

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2048,
        "messages": [{"role": "user", "content": prompt}]
    })

    response = client.invoke_model(
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=body
    )

    result = json.loads(response["body"].read())
    return {
        "text": result["content"][0]["text"],
        "input_tokens": result["usage"]["input_tokens"],
        "output_tokens": result["usage"]["output_tokens"],
    }


if __name__ == "__main__":
    print(f"Calling Bedrock ({MODEL_ID}) in {REGION}...")
    print("(This may take 15-30 seconds)\n")

    result = call_bedrock(PROMPT)

    print("=" * 60)
    print(result["text"])
    print("=" * 60)

    cost = (result["input_tokens"] / 1000 * COST_PER_1K_INPUT +
            result["output_tokens"] / 1000 * COST_PER_1K_OUTPUT)
    print(f"\nTokens: {result['input_tokens']:,} in / {result['output_tokens']:,} out")
    print(f"Cost: ${cost:.2f}")

    # Save
    OUTPUT_PATH.write_text(
        f"# Bedrock Response: Basal Sliding in the Bagley Ice Valley\n\n"
        f"> Model: {MODEL_ID} | Tokens: {result['input_tokens']:,} in, "
        f"{result['output_tokens']:,} out | Cost: ${cost:.2f}\n\n---\n\n"
        f"{result['text']}\n",
        encoding="utf-8"
    )
    print(f"Saved to: {OUTPUT_PATH.name}")
