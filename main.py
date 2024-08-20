## import packages
import streamlit as st # for web app
from langchain.prompts import PromptTemplate # for language chain mode
from langchain_openai import OpenAI # for language chain mode

## template for language chain mode
template = """
    Below is a draft text that may be poorly worded.
    Your goal is to:
    - Properly redact the draft text
    - Convert the draft text to a specified tone
    - Convert the draft text to a specified dialect

    Here are some examples different Tones:
    - Formal: Greetings! OpenAI has announced that Sam Altman is rejoining the company as its Chief Executive Officer. After a period of five days of conversations, discussions, and deliberations, the decision to bring back Altman, who had been previously dismissed, has been made. We are delighted to welcome Sam back to OpenAI.
    - Informal: Hey everyone, it's been a wild week! We've got some exciting news to share - Sam Altman is back at OpenAI, taking up the role of chief executive. After a bunch of intense talks, debates, and convincing, Altman is making his triumphant return to the AI startup he co-founded.  

    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, \
        cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, \
        car park, trousers, windscreen

    Example Sentences from each dialect:
    - American: Greetings! OpenAI has announced that Sam Altman is rejoining the company as its Chief Executive Officer. After a period of five days of conversations, discussions, and deliberations, the decision to bring back Altman, who had been previously dismissed, has been made. We are delighted to welcome Sam back to OpenAI.
    - British: On Wednesday, OpenAI, the esteemed artificial intelligence start-up, announced that Sam Altman would be returning as its Chief Executive Officer. This decisive move follows five days of deliberation, discourse and persuasion, after Altman's abrupt departure from the company which he had co-established.

    Please start the redaction with a warm introduction. Add the introduction \
        if you need to.
    
    Below is the draft text, tone, and dialect:
    DRAFT: {draft}
    TONE: {tone}
    DIALECT: {dialect}

    YOUR {dialect} RESPONSE:
"""

#PromptTemplate variables definition
prompt = PromptTemplate(
    input_variables=["tone", "dialect", "draft"],
    template=template,
)


## LLM and key loading function 
def load_LLM(openai_api_key):
    """Load the language model

    Args:
        openai_api_key (_type_): openai api key
        temperature (float, optional): determing the level of randomness. Defaults to 0.7.

    Returns:
        _type_: llm model
    """
    # load the language model
    llm  = OpenAI(openai_api_key=openai_api_key,temperature=0.7)
    return llm 

## page title and header 
st.set_page_config(page_title="Re-write your text", page_icon="🔗", layout="wide")
st.header("Re-write your text")

# intro 
col1, col2 = st.columns(2)

with col1:
    st.markdown('Re-write the text in the specified tone and dialect')

with col2:
    st.markdown('''
        ## How to Use
        - Select the tone and dialect
        - Enter the draft text in the text box
        - Click the button to generate the re-written text
    ''')

## api key input
st.markdown("### Enter your OpenAI API Key")

def get_openai_api_key():
    input_text  = st.text_input("Enter your OpenAI API Key", type="password",placeholder="Enter your OpenAI API Key", key="openai_api_key", help="Enter your OpenAI API Key here")
    return input_text

openai_api_key = get_openai_api_key()


## get imput text 
st.markdown("### Enter the Draft Text")

def get_draft_text():
    input_text  = st.text_area(label="Text", label_visibility='collapsed', placeholder="Your Text...", key="draft_input")

    return input_text

draft_input = get_draft_text()

if len(draft_input) > 700:
    st.write("The text is too long. Please enter a shorter text. max=700 words")
    st.stop()


## promt template tuning options 
col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox("Select the Tone", ["Formal", "Informal"])
with col2:
    option_dialect = st.selectbox("Select the Dialect", ["American", "British"])


## output
st.markdown("### Redacted Text")

if draft_input:
    if not openai_api_key:
        st.warning("Please enter your OpenAI API Key \
                   Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key) ",icon="⚠️")
        st.stop()

    try:   
        llm = load_LLM(openai_api_key)
    except Exception as e:
        st.warning(f"Error loading the language model: {e}")
        st.stop()

    promt_with_draft = prompt.format(
        tone=option_tone,
        dialect=option_dialect,
        draft=draft_input
    )

    try:
        response = llm(promt_with_draft)
    except Exception as e:
        st.warning(f"Error generating the response: {e}")
        st.stop()

    st.write(response)

