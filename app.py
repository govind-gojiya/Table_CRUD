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
        name = st.text_input("Intern's Name", value="", placeholder="Govind", key="internName")
        mentor = st.text_input("Mentor Name", value="", placeholder="Hima Soni", key="internMentor")

    with right_column:
        technology = st.selectbox("Assigned Technology", techstack, key="internTechnology")
        stiphend = round(st.number_input("Stiphend", placeholder=0.00, key="internStiphend"), 2)

    st.form_submit_button("Add Details", on_click=addIntern, type="primary", use_container_width=True)
    
st.divider()

# get all intern trainees details to show
def getTrainees(trainee = ""):
    searchQuery = f"""SELECT NAME, TECHNOLOGY, MENTOR, STIPHEND FROM TRAINEES {trainee}"""
    try:
        cursor.execute(searchQuery)
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

def updateTrainee():
    if st.session_state.isUpdating:
        updateTraineeSQL = "UPDATE TRAINEES SET TECHNOLOGY = %s AND MENTOR = %s AND  STIPHEND = %s WHERE NAME = %s"
        updateDetails = (st.session_state.updateInternTechnology, st.session_state.updateInternMentor, st.session_state.updateInternStiphend, st.session_statex.updateTrainee)
        try:
            cursor.execute(updateTraineeSQL, updateDetails)
            db.commit()
            st.toast(f'Hooray! Updated details having id as {cursor.lastrowid}', icon='🎉')
            time.sleep(0.3)
        except:
            db.rollback()
    else:
        st.toast("Not callable like this.")

def traineeDetails():
        st.session_state.isUpdating = False
        whereCluseForOne = f"WHERE NAME = \"{st.session_state.updateTrainee}\""
        getTraineeDetails = getTrainees(whereCluseForOne)
        print(getTraineeDetails)
        st.session_state.updateTech = getTraineeDetails.iloc[1:,1:2]
        st.session_state.updateMentor = getTraineeDetails.iloc[1:,2:3]
        st.session_state.updateStiphend = getTraineeDetails.iloc[1:,3:4]

# interface for update trainee
with st.container(border=True):
    st.session_state.isUpdating = True
    st.session_state.updateMentor = ""
    st.title("Update Trainee Details")
    allIntern = getTrainees()
    st.selectbox("Select Trainee to update details:", allIntern.iloc[0:,0:1], index=None, on_change=traineeDetails, key="updateTrainee")
    mentorCol, technoCol, stiphendCol = st.columns(3)
    updateMentor = mentorCol.text_input("Mentor Name", value=st.session_state.updateMentor, placeholder="Hima Soni", key="updateInternMentor", disabled=st.session_state.isUpdating)
    updateTechno = technoCol.selectbox("Assigned Technology", techstack, key="updateInternTechnology", disabled=st.session_state.isUpdating)
    updateStiphend = stiphendCol.number_input("Stiphend", placeholder=0.00, key="updateInternStiphend", disabled=st.session_state.isUpdating)
    updateStiphend = round(updateStiphend, 2)
    st.button("Update Details", on_click=updateTrainee, type="primary", use_container_width=True, disabled=st.session_state.isUpdating)


