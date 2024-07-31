def calculate_price(response):
    # 가격 정보 ($/1M tokens)
    PRICING = {
        "gpt-4o-mini": {"input": 0.150, "output": 0.600},
        "gpt-4o-mini-2024-07-18": {"input": 0.150, "output": 0.600},
        "gpt-4o": {"input": 5.00, "output": 15.00},
        "gpt-4o-2024-05-13": {"input": 5.00, "output": 15.00}
    }

    model = response.model
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens

    if model not in PRICING:
        return f"Unknown model: {model}"

    input_price = (input_tokens / 1_000_000) * PRICING[model]["input"]
    output_price = (output_tokens / 1_000_000) * PRICING[model]["output"]
    total_price = input_price + output_price

    return f"입력 토큰: {input_tokens}, 출력 토큰: {output_tokens}, 총 가격: ${total_price:.6f}"

# 사용 예시
# response를 받아 함수에 넣어주면 얼만지 나옴.

# response = client.chat.completions.create(...) 

# print(calculate_price(response)) 