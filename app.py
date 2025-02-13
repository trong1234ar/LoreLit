# Author: trongntdseb@gmail.com
# Uniform naming convention for LoreLit 
# MMP: Meaning_Modifier__Place
# Meaning: Actual meaning or function of the variable
# Modifier: The variation of variable
# Place: Where the variable is used

## Fix:
# light/dark theme
# timer
# still not randomly 3 task (task a, b, c for every champ)
# word limit error:)

import streamlit as st
from config import *
from model import *
import time
import random

st.set_page_config(page_icon=f'{APP_LOGO}', 
                   page_title=f'{APP_NAME}', 
                   layout='wide',
                   initial_sidebar_state='auto',
                   menu_items={
                        'Get Help': 'https://github.com/trong1234ar/LoreLit',
                        'Report a bug': "mailto:trongntdseb@gmail.com",
                        'About': "# This is a header. This is an *extremely* cool app!"
                    })
# ------------------------------------------------------------------------------ #

local_css('style.css')
ss = st.session_state
# ------------------------------------------------------------------------------ #
st.markdown(header_css, unsafe_allow_html=True)
st.markdown(subheader_css, unsafe_allow_html=True)
st.markdown(paragraph_css, unsafe_allow_html=True)

st.markdown(f"<div class='header'>{APP_NAME}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='subheader'>{APP_SLOGAN}</div>", unsafe_allow_html=True)
# ------------------------------------------------------------------------------ #
para_main__col, answer_main__col = st.columns(2)
with para_main__col:
    if 'champ_list_full__dict' not in ss:
        ss.champ_list_full__dict = get_champ_name()
    champ_selected = st.selectbox(label='Caution: Do not choose the same champion twice in a row. Wait for 20s-40s to choose another one.', 
                                  options=ss.champ_list_full__dict.keys(), 
                                  index=None, 
                                  placeholder="Choose a champion")
    if 'champ_selected' not in ss:
        ss.champ_selected = None
    #     ss.prev_selected = None
    # ss.prev_selected = champ
# ------------------------------------------------------------------------------ #
    img__col, timer_font__slider  = st.columns([3,5], gap='small')
    if champ_selected:
        st.markdown(f"<div class=subheader_noncenter>{champ_selected}</div>", unsafe_allow_html=True)

        with img__col:
            st.image(ss.champ_list_full__dict[champ_selected], use_container_width=True)
        with timer_font__slider:
            font_size__temp = st.slider(label='Font size', min_value=1, max_value=40, value=20)
            create_stopwatch()



# ------------------------------------------------------------------------------ 
        if 'paragraph_text_list' not in ss:
            ss.paragraph_text_list = None
        if ss.champ_selected != champ_selected:
            with st.spinner('Collecting lore, please wait... (up to 15 seconds)'):
                ss.paragraph_text_list = get_champ_lore(champ_selected)   


        lore_feed = ''
        for lore in ss.paragraph_text_list:
            st.markdown(
                f"""
                <div class="paragraph" style="font-size: {font_size__temp}px; word-wrap: break-word; white-space: normal;">
                {lore}
                </div>
                """,
                unsafe_allow_html=True
            )
            st.write('')
            lore_feed += f"{lore}\n"
# ------------------------------------------------------------------------------
if champ_selected:
    with answer_main__col:
        st.write('')
        with st.form(key='answer_form'):
# static------------------------------------------------------------------------------ #
            if ss.champ_selected != champ_selected:
                with st.spinner('Generating questions, please wait... (up to 20 seconds)'):
                    prompt = ChatPromptTemplate.from_template(template=template_string)
                    task_list = random.sample(range(1, 9), 3)
                    messages = prompt.format_messages(text=lore_feed, task_list=task_list)
                    if 'response' not in ss:
                        ss.response = None
                    ss.response = llm.invoke(messages)
# dynamic------------------------------------------------------------------------------ 
            question_ui, answer_key = get_qna(ss.response)
            st.markdown(
            f"""
            <div class="paragraph" style="font-size: {font_size__temp}px; word-wrap: break-word; white-space: normal;">
                {question_ui}
            </div>
            """,
            unsafe_allow_html=True)
# dynamic------------------------------------------------------------------------------ #
            ans_input__upbox1 = st.columns(7)
            ans_input__upbox2 = st.columns(6)
            my_answer = {}
            for i in range(len(ans_input__upbox1)):
                with ans_input__upbox1[i]:
                    my_answer[i+1] = ''
                    my_answer[i+1] = st.text_input(label='', placeholder=f'Q{i+1}')
            for i in range(len(ans_input__upbox2)):
                with ans_input__upbox2[i]:
                    ii = i + len(ans_input__upbox1)
                    my_answer[ii+1] = ''
                    my_answer[ii+1] = st.text_input(label='', placeholder=f'Q{ii+1}')
            submit_button = st.form_submit_button(label='Submit')
# dynamic------------------------------------------------------------------------------
        if ss.champ_selected != champ_selected:
            ss.score = None
            ss.recheck_df = None
        if submit_button: 
            with st.spinner('Checking answers, please wait...'):
                score = 0
                for q, a in my_answer.items():
                    if a.upper() == answer_key[q].upper():
                        score += 1
                time.sleep(3) 
            if score == len(answer_key): st.balloons()
            ss.score = score
            ss.user_answer = my_answer
            ss.recheck_df = pd.DataFrame({
                "#Q": answer_key.keys(),
                "Key": answer_key.values(),
                "Your Answer": ss.user_answer.values()
            }).set_index('#Q')
        if ss.score is not None:
            st.markdown(f"""
                        <div class="subheader_noncenter">
                        Your score: {ss.score}/{len(answer_key)}
                        </div>""", 
                unsafe_allow_html=True)
            st.table(ss.recheck_df)
        
# st.markdown(question_ui)
# Make sure any changes of user does not influence the llm or scraping process
ss.champ_selected = champ_selected

