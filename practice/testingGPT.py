from openai import OpenAI

# 🔑 Paste your API key directly here
client = OpenAI(api_key="put in the folder. find it in documents")  # <<< Replace this with your actual key

def main():
    print("🤖 ChatGPT CLI - type 'exit' to quit\n")

    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Bye!")
            break

        messages.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            reply = response.choices[0].message.content
            messages.append({"role": "assistant", "content": reply})
            print(f"GPT: {reply}\n")

        except Exception as e:
            print("❌ Error:", e)

if __name__ == "__main__":
    main()
