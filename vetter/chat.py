"""A chat bot that interacts with GPT."""

import logging
from os import environ
from sys import stderr

import openai
import streamlit as st
from streamlit import session_state as sess
from streamlit_chat import message
from tenacity import retry, stop_after_attempt, wait_exponential

from vetter.history import History

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


def handle_error(state):
    """Handle errors that happen durring queries."""
    breakpoint()
    if "history" in sess:
        sess.history.errors.append(state.outcome.result())
    return state.outcome.result()


@retry(wait=wait_exponential(min=20, max=60), stop=stop_after_attempt(6),
       retry_error_callback=handle_error)
def query():
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
    logging.info(
        f"============> [query()] "
        f"processed: {sess.history.processed}, "
        f"count: {sess.history.count}, "
        f"last: {sess.history.last}, "
        f"should?: {sess.history.should_query}"
    )

    if not sess.history.should_query:
        return

    logging.info("============> [query()] Trying...")

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=sess.history.messages
    )
    result = response["choices"][0]

    if result["finish_reason"] == "max_tokens":
        sess.history.errors.append("Max tokens reached.")
        logging.error("Max tokens reached.")
        st.error("Max tokens reached.")
        return

    sess.history.add("assistant", result["message"]["content"])
    sess.history.processed = sess.history.count
    logging.info(f"~~~~~~~~~> SUCCESS processed: {sess.processed}")


def loop():
    """The page loop which is rerun on user-interaction with any widget."""
    # initialize processed value in session to track the messages that have
    # already been submitted to GPT and received a response
    logging.info(f"LOOP session keys: {list(sess.keys())}")
    if "history" not in sess:
        sess["history"] = History()

    if not sess.history.processed:
        query()

    st.set_page_config(
        page_title="Candidate Vetter",
        page_icon=":robot:"
    )

    st.header("Candidate Vetter")

    logging.info(
        f"processed: {sess.history.processed}, "
        f"count: {sess.history.count}, "
        f"messages: {len(sess.history.messages)}, "
        f"last: {sess.history.last}"
    )

    # get input from user
    text = st.text_input("", key="input")

    # add to history and process response
    if text:
        sess.history.add("user", text)
        query()

    # print the message history
    for i, msg in enumerate(sess.history.messages):
        if msg["role"] == "system":
            continue

        message(
            msg["content"],
            is_user=(msg["role"] == "user"),
            key=f"{msg['role']}_{i}"
        )


if __name__ == "__main__":
    loop()
