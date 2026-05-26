import anthropic, os

client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
response = client.messages.create(
    model='claude-sonnet-4-6',
    max_tokens=100,
    tools=[{'type': 'web_search_20250305', 'name': 'web_search', 'max_uses': 1}],
    messages=[{'role': 'user', 'content': 'Search for one piece of semiconductor news today and summarize it in one sentence.'}]
)
for i, block in enumerate(response.content):
    print(f'Block {i}: type={block.type}, length={len(block.text) if hasattr(block, "text") else "N/A"}')
print('Stop reason:', response.stop_reason)