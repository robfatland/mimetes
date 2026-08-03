# Cloud AI API Services and Available Models

A summary of the major cloud providers, their AI API services, and the
foundation models accessible through each.


| Cloud Provider | AI API Service | Models Available |
|---------------|---------------|-----------------|
| **AWS** | Amazon Bedrock | Anthropic Claude, Meta Llama, Mistral AI, Cohere, AI21 Labs Jamba, Amazon Titan, Stability AI (image) |
| **Azure** | Microsoft Foundry (formerly Azure OpenAI + AI Studio) | OpenAI GPT-4/GPT-5, Anthropic Claude, Meta Llama, Mistral AI, DeepSeek, xAI Grok, Cohere, NVIDIA |
| **Google Cloud** | Vertex AI / Gemini Enterprise Agent Platform | Google Gemini, Anthropic Claude, Meta Llama, Mistral AI, AI21 Labs |


## Notes

- **Anthropic Claude** is available on all three platforms — it is not exclusive
  to any single provider.
- **OpenAI models** (GPT-4, GPT-5) are exclusive to Azure via Microsoft's
  partnership. They are not available on AWS Bedrock or Google Vertex AI.
- **Google Gemini** is exclusive to Google Cloud (Vertex AI).
- **Meta Llama** and **Mistral AI** models are available on all three.
- Each provider also offers proprietary models: AWS has Amazon Titan, Azure has
  its OpenAI partnership, Google has Gemini.
- Pricing, context windows, and available model variants differ by provider even
  for the same model family. Check provider documentation for specifics.
- This landscape changes frequently as new models launch and providers add access.
