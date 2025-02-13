APP_NAME = 'LoreLit'
APP_LOGO = '🐍'
APP_SLOGAN = 'A play-based learning English app'
# FONT_FAMILY = "calibri"
FONT_HEADER_SIZE = 60
FONT_SUBHEADER_SIZE = 20


header_css = f"""
    <style>
        .header {{
            font-size: {FONT_HEADER_SIZE}px;
            font-weight: bold;
            text-align: center;
            margin-top: -100px;  /* Moves the header up */
            padding-top: 0px;   /* Removes extra padding */
        }}
    </style>
"""
subheader_css = f"""
    <style>
        .subheader {{
            font-size: {FONT_SUBHEADER_SIZE}px;
            font-weight: bold;
            text-align: center
        }}
        .subheader_noncenter {{
            font-size: {FONT_SUBHEADER_SIZE * 2}px;
            font-weight: bold;
        }}
    </style>
"""

paragraph_css = f"""
    <style>
        .paragraph {{
        }}
    </style>
"""

import streamlit as st
def local_css(file_name):#func to read css file -> create flake
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
def get_champ_name():
    champ_info__df = pd.read_csv('Champs.csv')
    champ_info__dict = champ_info__df.set_index('champ')['image'].to_dict()
    return champ_info__dict

import re, time
def get_champ_lore(name):
    lore_list = []
    while not lore_list:
        # Normalize champ name for searching
        champ_name = ''.join(re.findall(r'\b[a-zA-Z]+\b', name)).lower()
        url = f"https://universe.leagueoflegends.com/en_US/story/champion/{champ_name}/"
        # Scraping data
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        driver.quit()
        # Extracting data into a list
        lores = soup.find('div', id='CatchElement').contents
        lore_list = []
        for line in lores:
            temp_line = ''
            try:
                for l in line.contents:
                    try:
                        if not l.contents:
                            continue
                        else:
                            temp_line += l.contents[0]
                    except:
                        temp_line += l
                lore_list.append(temp_line)
            except:
                lore_list.append(line)
            
        lore_list
    return lore_list

def get_qna(response):
    text = response.content
    # Step 1: Use regex to separate the question section from the answer key
    match = re.search(r"(ANSWER KEY:\n)([\s\S]*)", text)
    if match:
        question_parts = text[:match.start(1)].strip()
        answer_part = match.group(2).strip()
    else:
        question_parts = text
        answer_part = ""

    # Step 2: Convert the answer part into a dictionary
    answer_dict = {}
    for line in answer_part.split("\n"):
        match = re.match(r"(\d+)\.\s(.+)", line)
        if match:
            key = int(match.group(1))
            value = match.group(2).strip()
            answer_dict[key] = value

    return question_parts, answer_dict

def create_stopwatch():
    from streamlit_theme import st_theme
    theme = st_theme()
    time.sleep(1)
    stopwatch_html = f"""
        <style>
            .timer-container {{
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: {FONT_SUBHEADER_SIZE}px;
                gap: 10px;
                font-family: {theme['font']};
            }}

            .timer-text {{
                font-size: {FONT_SUBHEADER_SIZE * 2.5}px;
                font-weight: bold;
                width: 150px;
                text-align: center;
                color: {theme['textColor']}
            }}

            .timer-buttons {{
                gap: 10px;

            }}

            button {{
                font-size: 18px;
                width: 75px; /* Buttons are half the size of the time text */
                height: 40px; /* Explicit height to ensure proper centering */
                
                /* Center text inside button */
                align-items: center;
                justify-content: center;
                
                cursor: pointer;
                border: 2px solid #333;
                border-radius: 5px;
                background-color: #f4f4f4;
                text-align: center;
            }}



            button:hover {{
                background-color: #ddd;
            }}
        </style>

        <div class="timer-container">
            <div id="time" class="timer-text">00:00</div>
            <div class="timer-buttons">
                <button onclick="startStopwatch()">Start</button>
                <button onclick="stopStopwatch()">Stop</button>
                <button onclick="resetStopwatch()">Reset</button>
            </div>
        </div>

        <script>
            var timer;
            var isRunning = false;
            var elapsedTime = 0;

            function updateTimeDisplay() {{
                var minutes = Math.floor(elapsedTime / 60);
                var remainingSeconds = elapsedTime % 60;

                minutes = minutes < 10 ? "0" + minutes : minutes;
                remainingSeconds = remainingSeconds < 10 ? "0" + remainingSeconds : remainingSeconds;

                document.getElementById("time").textContent = minutes + ":" + remainingSeconds;
            }}

            function startStopwatch() {{
                if (!isRunning) {{
                    isRunning = true;
                    timer = setInterval(function() {{
                        elapsedTime++;
                        updateTimeDisplay();
                    }}, 1000);
                }}
            }}

            function stopStopwatch() {{
                clearInterval(timer);
                isRunning = false;
            }}

            function resetStopwatch() {{
                clearInterval(timer);
                isRunning = false;
                elapsedTime = 0;
                updateTimeDisplay();
            }}
        </script>
    """

    st.components.v1.html(stopwatch_html, height=100)


template_string = """
You are an IELTS judge. Your task is to generate IELTS Reading tasks based on a given paragraph.  
Follow IELTS Reading Task Types Criteria and ensure your output strictly follows the instructions.  

---

### Instructions  

1. Create 13 questions across 3 different tasks, RANDOMLY selecting from the 11 IELTS task types below.  
   - Each task must have at least 3 and at most 7 questions.  
   - NO repetition of task types (use random.sample(range(1, 12), 3) for task selection).
   - Number all questions sequentially (e.g., Task 1: 1-5, Task 2: 6-9).  

2. Generate accurate questions by paraphrasing sentences from the paragraph.  
   - Ensure the questions appear in the same order as information in the text (if applicable).  

3. Word Limit Rules (MUST be followed):  
   - If a task requires a word limit (e.g., Sentence Completion, Short Answer),  
     determine the longest answer and set the word limit accordingly.  
   - Example:  
     - Answers: "A PLANE", "A NICE JACKET", "BEAUTY"  
     - Max words = 3, so word limit = "NO MORE THAN THREE WORDS AND/OR A NUMBER"  
   - DO NOT exceed the word limit in any answer.  

4. Answer Formatting Rules:  
   - All answers must be in UPPERCASE.  
   - For fill-in-the-gap tasks, answers MUST be found in the paragraph.  
   - Singular and plural forms are treated as different answers.  

5. Proper IELTS Task Instructions:  
   - Each task must include detailed task-specific instructions as found in IELTS reading exams.  
   - Example: "Write NO MORE THAN TWO WORDS AND/OR A NUMBER"  

6. Ensure Proper Formatting:  
   - The output must NOT use bold, italics, or underlined text.
   - Task instruction should be formatted correctly (must have new line for each instruction)
   - For multiple choice, the choice should be indented by 4 spaces
   - For each task, each instruction, each question or each choice, they should lie in a new line. 
    (Use double \\n to create a new line)

7. ANSWER SECTION MUST BE AT THE END OF OUTPUT:  
   - Use this format:  
     ```
     ANSWER KEY:\n\n
     1. A  \n\n
     2. B  \n\n
     3. FALSE  \n\n
     4. NOT GIVEN  \n\n
     5. THE RIVER NILE  \n\n
     ...
     ```
---

Task Types:\n
Type 1 – Multiple choice\n
What's involved?\n
This type of question may be a question with four possible answers or the first half of a sentence with four possible sentence endings. You have to choose one correct answer (A, B, C or D), then write the correct answer on the answer sheet.
Sometimes you are given a longer list of possible answers and you have to choose more than one answer. You should read the question carefully to check how many answers you need to choose.
The questions are in the same order as the information in the text: that is, the answer to the first question will be before the answer to the second question, and so on.
\nWhat skills are tested?\n
This type of question tests many different reading skills including: detailed understanding of specific points or general understanding of the main points of the text.
\nExpected format:\n
Task 1: Multiple Choice
    Choose the correct letter, A, B, C, or D.

    1. What was the primary reason for the decline of the Silk Road?
    A. The rise of maritime trade routes.
    B. The destruction caused by Mongol invasions.
    C. The lack of interest in silk products.
    D. The spread of infectious diseases.
    
    2. Which technological advancement significantly influenced the Silk Road trade?
    A. The invention of the printing press.
    B. The development of the compass.
    C. The construction of transcontinental railways.
    D. The establishment of postal services.
    
Type 2 – Identifying information (True/False/Not given)\n
What's involved?\n
In this type of question, you are given a number of statements and are asked: ‘Do the following statements agree with the information in the text?’ You have to write ‘True’, ‘False’ or ‘Not given’ in the boxes on your answer sheet. It is important to understand the difference between ‘False’ and ‘Not given’. ‘False’ means that the statement contradicts the information in the text. ‘Not given’ means that the statement neither agrees with nor contradicts the information in the text. You must be careful not to use any information you already know about the topic of the text when choosing your answer.
\nWhat skills are tested?\n
This type of question tests your ability to recognise specific information given in the text.
\nYou must provide the answer format for users to follow the instructions.
\nExpected Format:\n
Task 2: Identifying Information
    Do the following statements agree with the information in the text?
    Write 'TRUE', 'FALSE' or 'NOT GIVEN'.

    1. The Silk Road was exclusively used for trading silk products.
    2. Marco Polo documented his travels along the Silk Road.
    3. The Silk Road remained the primary trade route until the 20th century.


Type 3 – Identifying writer’s views/claims (Yes/No/Not given)\n
What's involved?\n
In this type of question, you are given a number of statements and asked: ‘Do the following statements agree with the views of the writer?’ or ‘Do the following statements agree with the claims of the writer?’ You have to write ‘Yes’, ‘No’ or ‘Not given’ in the boxes on your answer sheet. It is important to understand the difference between ‘no’ and ‘not given’. ‘No’ means that the statement contradicts the writer’s view or claim. ‘Not given’ means that the statement neither agrees with nor contradicts the writer’s view or claim. You must be careful not to use any information you already know about the topic of the text when choosing your answer.
\nWhat skills are tested?\n
This type of question tests your ability to recognise opinions or ideas.
\nYou must provide the answer format for users to follow the instructions.
\nExpected Format:\n
Task 3: Identifying Writer’s Views/Claims
    Do the following statements agree with the views of the writer?
    Write 'YES', 'NO' or 'NOT GIVEN'.

    1. The writer believes the Silk Road played a crucial role in cultural exchanges.
    2. The writer suggests that silk was the most valuable commodity traded on the route.
    3. The writer argues that modern globalization has eliminated the need for long-distance trade routes.

Type 4 – Matching headings\n
What's involved?\n
In this type of question, there is a list of headings (one heading lies in one line) which are identified by Roman numerals (i, ii, iii, etc.). A heading summarises the main idea of a paragraph or section of the text. You must match the heading to the correct paragraph or section. The paragraphs (or sections) are identified by number (1, 2, 3, etc.). You will need to write the correct Roman numerals in the boxes on your answer sheet. There will always be more headings than paragraphs or sections, so some headings will not be used. It is also possible that some paragraphs or sections may not be included in the task. One or more paragraphs or sections may already be matched with a heading as an example on the question paper. No heading may be used more than once.
\nWhat skills are tested?\n
This type of question tests your ability to identify the general topic of a paragraph (or section) and to recognise the difference between the main idea and a supporting idea.
\nExpected format:\n
Task 4: Matching Headings
    Choose the correct heading for each paragraph.

    List of Headings:
    i. The Expansion of the Silk Road
    ii. Cultural Exchanges along the Route
    iii. The Role of Merchants and Traders
    iv. Challenges and Dangers of the Journey
    v. The Decline of the Silk Road
    
    1. Paragraph 1
    2. Paragraph 3
    3. Paragraph 5

Type 5 – Matching features\n
What's involved?\n
In this type of question, you have to match a set of statements or pieces of information to a list of options. The options are a group of features from the text, and letters (A, B, C, etc.) are used to identify them. Write the correct letter on the answer sheet. You may, for example, have to match descriptions of inventions to the people who invented them. It is possible that some options will not be used, and that others may be used more than once. When it is possible to use any option more than once, the instructions will say: ‘You may use any option more than once’.
\nWhat skills are tested?\n
This type of question tests your ability to recognise relationships and connections between facts in the text and your ability to recognise opinions and theories. You need to be able to skim and scan the text to find the information quickly so that you can then read that part more carefully for detail.
\nYou must provide the answer format for users to follow the instructions.
\nExpected Format:\n
Task 5: Matching Features
    Match each development with the correct civilization.

    A. China
    B. Persia
    C. India
    D. Rome
    
    1. The invention of paper.
    2. The development of the decimal system.
    3. The introduction of silk production to Europe.

Type 6 – Matching sentence endings\n
What's involved?\n
In this type of question, you are given the first half of a sentence based on information in the text and you have to choose the best way to complete the sentence by choosing from a list of possible endings. The endings are identified by letters (A, B, C, etc.). There will be more sentence endings than beginnings, so you will not use all of them. You must write the letter you choose on the answer sheet. The sentence beginnings are in the same order as the information in the text.
\nWhat skills are tested?\n
This type of question tests your ability to understand the main ideas in the text.
\nExpected format:\n
Task 6: Matching Sentence Endings
    Complete each sentence with the correct ending, A-E.

    A. ...which led to a decline in land-based trade.
    B. ...and contributed to the spread of ideas across continents.
    C. ...resulting in an increase in merchant wealth.
    D. ...making the Silk Road a crucial economic link.
    E. ...which was later adopted by European merchants.
    
    1. The rise of maritime trade routes...
    2. The cultural exchanges along the Silk Road...
    3. The demand for luxury goods in Europe...

Type 7 – Sentence completion\n
What's involved?\n
In this type of question, you have to fill in a gap in each sentence by choosing words from the text. You must write the words you choose on the answer sheet.
You should read the instructions very carefully as the number of words or numbers you may use to fill the gaps can change. A word limit is given, for example, ‘NO MORE THAN TWO WORDS AND/OR A NUMBER’. You will lose the mark for writing more than the word limit. Contracted words such as ‘they’re’ will not be tested. Hyphenated words such as ‘check-in’ count as single words.
The questions are in the same order as the information in the text.
\nWhat skills are tested?\n
This type of question tests your ability to find detail/specific information in a text.
\nYou must provide the answer format for users to follow the instructions.
\nExpected Format:\n
Task 7: Sentence Completion
    Complete the sentences below using NO MORE THAN TWO WORDS.

    1. The Silk Road connected Asia, the Middle East, and ______.
    2. One of the most valuable exports from China was ______.
    3. Merchants along the Silk Road used ______ as a medium of exchange.

Type 8 – Summary/note/table/flow-chart completion\n
What's involved?\n
In this type of question, you are given a summary of a part of the text, and have to complete it using words taken from the text. Note that the summary is not normally of the whole text. The summary may be in the form of:
a continuous text (called ‘a summary’ in the instructions)
several notes (called ‘notes’ in the instructions)
a table with some parts of it left empty or partially empty (called ‘a table’ in the instructions)
a series of boxes or steps linked by arrows to show the order of events, with some of the boxes or steps empty or partially empty (called ‘a flow chart’ in the instructions).
The answers may not come in the same order as in the text. However, they will usually come from one part of the text rather than the whole text.
There are two variations of this task type. In the first variation, you need to select words from the text which fit into gaps on the question paper. You must write the words you choose on the answer sheet.You should read the instructions very carefully as the number of words or numbers you may use to fill the gaps can change. A word limit is given, for example, ‘NO MORE THAN TWO WORDS AND/OR A NUMBER’. You will lose the mark for writing more than the word limit. Contracted words such as ‘they’re’ will not be tested. Hyphenated words such as ‘check-in’ count as single words.
In the second variation, you have to choose from a list of words to fill the gaps. The words are identified by letters (A, B, C, etc.).
You must write the letter you choose on the answer sheet.
\nWhat skills are tested?\n
This type of question tests your ability to understand details and/or the main ideas of a part of the text. When completing this type of question, you will need to think about the type of word(s) that will fit into a gap (for example, whether a noun is needed, or a verb, etc.).
\nExpected Format:\n
Task 8: Summary Completion
Complete the summary using words from the passage.

The development of early aviation was driven by both scientific curiosity and practical necessity. The Wright brothers, inspired by ________, conducted extensive experiments with gliders before achieving powered flight. Their breakthrough came with the invention of a ________, which allowed better control of the aircraft. Over time, advancements in ________ led to the creation of safer and more efficient airplanes, revolutionizing both travel and commerce.

task list selected: ```{task_list}```
paragraph: ```{text}```
"""