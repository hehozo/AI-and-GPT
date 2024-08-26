from openai import OpenAI

client = OpenAI()

messages = [
    {
        "role": "system",
        "content": "You are a young home chef who loves to cook and invent new recipes. You love to add a twist to classic dishes and blend different cuisines together. You value originality and unexpected ingredients over traditional recipes. You also are willing to cook very complex dishes, because you are a bit of a show off and like to impress your friends.",
    }
]
messages.append(
    {
        "role": "system",
        "content": "Your client is going to provide either the name of a dish, the name of an ingredient, or a full recipe. If they provide input that is not a recognizable dish name, ingredient, or a recipe, you should reply that you can't help with that. Do not answer a recipe if you do not understand the name of the dish. If you know the dish, you must answer directly with a detailed recipe for it. If you don't know the dish, you should answer that you don't know the dish and end the conversation. If they provide an ingredient, you should answer with recipe suggestions to use that ingredient. If they provide a recipe, you should suggest improvements to make the recipe more interesting.",
    }
)


# given dish name, generate recipe
dish = input("Type the name of the dish you want a recipe for:\n")
messages.append(
    {
        "role": "user",
        "content": f"Suggest me a detailed recipe and the preparation steps for making {dish}.",
    }
)

# given ingredient, generate dish ideas
ingredient = input("Type the name of the ingredient you want ideas for:\n")
messages.append(
    {
        "role": "user",
        "content": f"Suggest 3 dish ideas that use {ingredient}. One or more should use {ingredient} as a main ingredient, and at least one should use {ingredient} as a twist to a classic dish.",
    }
)

# given a recipe, generate feedback
recipe = input("Provide the recipe you'd like feedback on:\n")
messages.append(
    {
        "role": "user",
        "content": f"Provide a suggestion to make the given recipe more interesting: {recipe}",
    }
)

model = "gpt-4o-mini"

stream = client.chat.completions.create(
    model=model,
    messages=messages,
    stream=True,
)

collected_messages = []
for chunk in stream:
    chunk_message = chunk.choices[0].delta.content or ""
    print(chunk_message, end="")
    collected_messages.append(chunk_message)

messages.append({"role": "system", "content": "".join(collected_messages)})

while True:
    print("\n")
    user_input = input()
    messages.append({"role": "user", "content": user_input})
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    collected_messages = []
    for chunk in stream:
        chunk_message = chunk.choices[0].delta.content or ""
        print(chunk_message, end="")
        collected_messages.append(chunk_message)

    messages.append({"role": "system", "content": "".join(collected_messages)})
