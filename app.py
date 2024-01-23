import streamlit as st
import mysql.connector as sql
import time
import pandas as pd

db=cursor=None

# Connecting database
try: 
    db = sql.connect(
        host="localhost",
        user="data_profiler",
        password="data_profiler_trainees_2929",
        database="INTERN"
    )
    cursor = db.cursor()

except Exception as e:
    print("Error in fetching. trainees details !!!", " \nError: ", e)

# Technology stack list to use where ever need
techstack = ["AI/ML", ".Net and Angular", "DevOps", "React JS", "Node JS", "Python Developer", "GO Lang"]

# adding new trainee details to database
def addIntern(**intern):
    addQuery = "INSERT INTO TRAINEES (NAME, TECHNOLOGY, MENTOR, STIPHEND) VALUES (%s, %s, %s, %s)"
    newIntern = (st.session_state.internName, st.session_state.internMentor, st.session_state.internTechnology, st.session_state.internStiphend)

    try:
        cursor.execute(addQuery, newIntern)
        db.commit()
        st.toast(f'Hooray! Added details having id as {cursor.lastrowid}', icon='🎉')
        time.sleep(0.3)
    except:
        db.rollback()

# interface(form) for adding new trainee details
with st.form("Add Trainees:", clear_on_submit=True):
    st.title('Add User :')
    left_column, right_column = st.columns(2)


    with left_column:
        name = st.text_input("Intern's Name", value=f'{st.session_state.isUpdating}', placeholder="Govind", key="internName")
        mentor = st.text_input("Mentor Name", value="", placeholder="Hima Soni", key="internMentor")

    with right_column:
        technology = st.selectbox("Assigned Technology", techstack, key="internTechnology")
        stiphend = round(st.number_input("Stiphend", placeholder=0.00, key="internStiphend"), 2)

    st.form_submit_button("Add Details", on_click=addIntern, type="primary", use_container_width=True)
    
st.divider()

# get all intern trainees details to show
def getTrainees(trainee = ""):
    searchAllQuery = f"SELECT NAME, TECHNOLOGY, MENTOR, STIPHEND FROM TRAINEES {trainee}"
    try:
        cursor.execute(searchAllQuery)
        field_names = [i[0] for i in cursor.description]
        allInternFromDB = cursor.fetchall()
        allIntern = pd.DataFrame(allInternFromDB, columns=field_names)
        return allIntern
    except Exception as e:
        print("Error in fetching. trainees details !!!", " \nError: ", e)

# call to show trainees data
with st.container(border=True):
    st.title("All Trainees")
    st.table(getTrainees())

st.divider()

# interface for update trainee
with st.container(border=True):
    def traineeDetails():
        st.table(getAllTrainees(f'WHERE NAME = "{st.session_state.updateTrainee}"'))

    st.title("Update Trainee Details")
    allIntern = getTrainees()
    st.write(allIntern)
    boxOfName = st.selectbox("Select Trainee to update details:", allIntern.iloc[0:,0:1], index=None, on_change=traineeDetails, key="updateTrainee")



