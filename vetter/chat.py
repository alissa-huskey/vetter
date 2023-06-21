"""A chat bot that interacts with GPT."""

from os import environ
from sys import stderr

import openai
from openai.openai_object import OpenAIObject
import streamlit as st
from streamlit import session_state as session
from streamlit_chat import message
from tenacity import (RetryError, retry, stop_after_attempt,
                      wait_random_exponential)

MODEL = "gpt-3.5-turbo"

try:
    openai.api_key = environ['OPENAI_API_KEY']
except KeyError:
    stderr.write("""
        You haven't set up your API key yet.

        If you don't have an API key yet, visit:

        https://platform.openai.com/signup

        1. Make an account or sign in
        2. Click "View API Keys" from the top right menu.
        3. Click "Create new secret key"

        Then, open the Secrets Tool and add OPENAI_API_KEY as a secret.
    """)
    exit(1)


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def query(history) -> OpenAIObject:
    """Send a query to GPT, retry and backoff exponentially, and return the
    first item in the "choice" list.

    Args:
        history (list): list of messages, each containing a dictionary with the
          keys role and content.

    Returns:
        Dictionary-like object that looks something like:
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Orange who?"
                },
                "finish_reason": "stop"
            }
    """
    response = openai.ChatCompletion.create(model=MODEL, messages=history)
    return response["choices"][0]


def user_input() -> str:
    """Place a text box widget on the page and return the user submitted
    content."""
    return st.text_area("", key="input")


def loop():
    """The page loop which is rerun on user-interaction with any widget."""
    # initialize processed value in session to track the messages that have
    # already been submitted to GPT and received a response
    if "processed" not in session:
        session["processed"] = 0

    # initialize message history
    if "messages" not in session:
        session["messages"] = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Knock knock."},
            {"role": "assistant", "content": "Who's there?"},
            {"role": "user", "content": "Orange."},
        ]

    st.set_page_config(
        page_title="Candidate Vetter",
        page_icon=":robot:"
    )
    st.header("Candidate Vetter")

    # only attempt to query GPT if there are messages that have not been
    # processed
    if session.processed < len(session["messages"]):
        try:
            # query GPT
            result = query(session.messages)

        # give up retries
        except RetryError:
            st.error("Rate limit reached.")
            st.stop()
            return

        else:
            # handle max token errors
            if result["finish_reason"] == "max_tokens":
                st.error("Max tokens reached.")
                st.stop()
                return

            # a successful result is appended to the session messages and
            # counted as processed
            session.messages.append(
                {"role": "assistant", "content": result["message"]["content"]}
            )
            session.processed = len(session["messages"]) + 1

    # get input from user
    text = user_input()

    if text:
        # append to message (but do NOT mark as processed)
        session.messages.append({"role": "user", "content": text})

    # print the message history
    for i, msg in enumerate(session.messages):
        if msg["role"] == "system":
            continue

        message(
            msg["content"],
            is_user=(msg["role"] == "user"),
            key=f"{msg['role']}_{i}"
        )


if __name__ == "__main__":
    loop()
