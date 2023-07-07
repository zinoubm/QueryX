def ask(context, question, manager):
    prompt = f"""
    Use the context to write a detailed answer to the following question

    context: {context}

    question: {question}

    answer:
    """

    return manager.get_chat_completion(prompt)


def summarize(input, manager):
    prompt = f"""
    Summarize the following passage in detail

    passage: {input}

    summary:
    """

    return manager.get_chat_completion(prompt)
