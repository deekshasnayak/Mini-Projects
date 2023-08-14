# Import necessary libraries
import os
import streamlit as st
import openai
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper

# Set your OpenAI API key
os.environ['OPENAI_API_KEY'] = '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'

# Set the Streamlit app title and header
st.set_page_config(page_title="Synopsis Generator", page_icon="📚🎥")

# Add styling to the title
st.title('Book/Movie Synopsis Generator')

# Create a text input for the user's prompt
prompt = st.text_input('Enter a Book/Movie/Show title for synopsis generation')

# Prompt templates, memory, LLMs setup, etc.
title_template = PromptTemplate(
    input_variables=['title'],
    template='Generate a synopsis for the book/movie/show: {title}'
)

# Memory
title_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')

# LLMs setup
llm = OpenAI(temperature=0.7)
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='synopsis', memory=title_memory)

# Wikipedia API setup
wiki = WikipediaAPIWrapper()

# Apply styling to the text output
if prompt:
    synopsis = title_chain.run(title=prompt)
    wiki_research = wiki.run(prompt)

    # Display the generated synopsis using Markdown
    st.markdown(f'## Synopsis for **{prompt}**')
    st.write(synopsis)

    # Show Wikipedia research
    with st.expander('Wikipedia Research'):
        st.info(wiki_research)

        # Extract information
        author = None
        actors = None
        directors = None
        lines = wiki_research.split('\n')
        for line in lines:
            if line.startswith("Author:"):
                author = line[len("Author: "):].strip()
            elif line.startswith("Actors:"):
                actors = line[len("Actors: "):].strip()
            elif line.startswith("Directors:"):
                directors = line[len("Directors: "):].strip()

        # Suggest other books/movies by the same author/actor/director
        if author:
            st.markdown(f'### Other Books by {author}')
            # Replace with actual suggested books by the same author
            suggested_books_by_author = ["Book A", "Book B", "Book C"]
            for book in suggested_books_by_author:
                st.write(f"- {book}")

        if actors:
            st.markdown('### Other Movies by the Same Actors')
            # Replace with actual suggested movies by the same actors
            suggested_movies_by_actors = ["Movie X", "Movie Y", "Movie Z"]
            for movie in suggested_movies_by_actors:
                st.write(f"- {movie}")

        if directors:
            st.markdown('### Other Movies by the Same Director')
            # Replace with actual suggested movies by the same director
            suggested_movies_by_director = ["Movie P", "Movie Q", "Movie R"]
            for movie in suggested_movies_by_director:
                st.write(f"- {movie}")
