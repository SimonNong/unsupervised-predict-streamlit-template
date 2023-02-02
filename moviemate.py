"""

    Streamlit webserver-based Recommender Engine.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.

    NB: !! Do not remove/modify the code delimited by dashes !!

    This application is intended to be partly marked in an automated manner.
    Altering delimited code may result in a mark of 0.
    ---------------------------------------------------------------------

    Description: This file is used to launch a minimal streamlit web
	application. You are expected to extend certain aspects of this script
    and its dependencies as part of your predict project.

	For further help with the Streamlit framework, see:

	https://docs.streamlit.io/en/latest/

"""
# Streamlit dependencies
import streamlit as st
import joblib,os
import csv
from PIL import Image, ImageDraw


# Data handling dependencies
import pandas as pd
import numpy as np

# Custom Libraries
from utils.data_loader import load_movie_titles
from recommenders.collaborative_based import collab_model
from recommenders.content_based import content_model

# Data Loading
title_list = load_movie_titles('resources/data/movies.csv')

# App declaration
def main():

    # DO NOT REMOVE the 'Recommender System' option below, however,
    # you are welcome to add more options to enrich your app.
    page_options = ["General Information", "Recommender System", "Solution Overview", "Register", "INTELLICON Al Movies Search", "About Us", "Feedback"]

    # -------------------------------------------------------------------
    # ----------- !! THIS CODE MUST NOT BE ALTERED !! -------------------
    # -------------------------------------------------------------------
    page_selection = st.sidebar.selectbox("Choose Option", page_options)
    if page_selection == "Recommender System":
        # Header contents
        st.write('# Movie Recommender Engine')
        st.write('### EXPLORE Data Science Academy Unsupervised Predict')
        st.image('resources/imgs/Image_header.png',use_column_width=True)
        # Recommender System algorithm selection
        sys = st.radio("Select an algorithm",
                       ('Content Based Filtering',
                        'Collaborative Based Filtering'))

        # User-based preferences
        st.write('### Enter Your Three Favorite Movies')
        movie_1 = st.selectbox('Fisrt Option',title_list[14930:15200])
        movie_2 = st.selectbox('Second Option',title_list[25055:25255])
        movie_3 = st.selectbox('Third Option',title_list[21100:21200])
        fav_movies = [movie_1,movie_2,movie_3]

        # Perform top-10 movie recommendation generation
        if sys == 'Content Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = content_model(movie_list=fav_movies,
                                                            top_n=10)
                    st.title("We think you'll like:")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")


        if sys == 'Collaborative Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = collab_model(movie_list=fav_movies,
                                                           top_n=10)
                    st.title("We think you'll like:")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")


    # -------------------------------------------------------------------

    # ------------- SAFE FOR ALTERING/EXTENSION -------------------
    if page_selection == "General Information":
        st.title("General Information")
        st.write("INTELLICON Al is a cutting-edge artificial intelligence and machine learning company that provides personalized solutions for various industries. With INTELLICON Al businesses and individuals can benefit from the power of artificial intelligence and machine learning technology to enhance their operations and improve their overall user experience")
        image = Image.open('movie_reco.jpg')
        st.image(image, caption='YOUR BEST TOOL FOR RECOMMENDATIONS!')

        st.title("How to use the app")
        st.write("Select 'INTELLICON Al Search and Filter Movies' on the left panel under the drop down arrow. Then choose movie of choice by using atleast one filter options displayed on the screen. Then a movie of your choice will be displayed on the screen")
        using_app = open('using_the_app.mp4', 'rb')
        video_bytes = using_app.read()
        st.video(video_bytes)

    if page_selection == "Solution Overview":
        st.title("Solution Overview")
        st.write("The recommender system works by taking huge movie datasets, viewer ratings and then uses the collective ratings to break down individual movies into a long list of attributes or identifiable qualities such as comedy or romance. Then the recommender system decodes individual tastes, and matching those taste will recommend relevant movies")

    # You may want to add more sections here for aspects such as an EDA,
    # or to provide your business pitch.
    if page_selection == "Register":    
    
        st.title("Create User Profile")
        name = st.text_input("Enter your name:")
        age = st.number_input("Enter your age:")
        gender = st.selectbox("Select your gender:", ["Male", "Female", "Other"])
        favorite_genres = st.multiselect("Select your favorite genres:", ["Action", "Comedy", "Drama", "Horror", "Romance"])
        favorite_actors = st.text_input("Enter your favorite actors (separated by commas):")
        favorite_directors = st.text_input("Enter your favorite directors (separated by commas):")
        if st.button("Submit"):
        # Save the user's profile information to a database or file
            st.success("User profile created!")
    
    if page_selection == "INTELLICON Al Movies Search": 
        image = Image.open('movie_poster.jpg')
        st.image(image, caption='Get popcorns ready! its movie time!')  
        st.title("Search and Filter Movies")
    # Load movies data
        movies_data = pd.read_csv('resources/data/movies.csv')
    # Search by title
        title = st.text_input("Search by title:")
        if title:
            movies_data = movies_data[movies_data["title"].str.contains(title, case=False)]
    # Filter by genre
        genres = ["All"] + list(movies_data["genre"].unique())
        genre = st.selectbox("Filter by genre:", genres)
        if genre != "All":
            movies_data = movies_data[movies_data["genre"] == genre]
    # Filter by year
        min_year = st.number_input("Filter by minimum release year:")
        max_year = st.number_input("Filter by maximum release year:")
        if min_year:
            movies_data = movies_data[movies_data["year"] >= min_year]
        if max_year:
            movies_data = movies_data[movies_data["year"] <= max_year]
    # Display results
        if movies_data.shape[0] > 0:
            st.dataframe(movies_data)
            st.balloons()
        else:
            st.warning("No movies found.")
        st.title("Search and filter movies")
    if page_selection == "Feedback":
        st.title("Rate and Provide Feedback")
        movie_title = st.text_input("Enter the title of the movie you would like to rate:")
        rating = st.radio("Rate the movie:", options=[1, 2, 3, 4, 5], format_func=lambda x: "⭐ "*x)
        feedback = st.text_area("Provide feedback on the movie:")
        if st.button("Submit"):
            # Save the user's rating and feedback to a database or file
            st.success("Rating and feedback submitted!")
            

    if page_selection == "About Us":
        st.title("About us")
        st.write("INTELLICON Al company is made up of professional bodies under the Umbrella of 'Data' who aim to revolutionize businesses with accurate and easy-to-use platforms powered by cutting-edge Al and machine learning techmology. INTELLICON Al also aims, to become a leading movie data-driven company, constantly innovating and evolving to provide the best possible artificial intelligence experience for our customers")
        team_members = [
            {
                "name": "Alaine Tobias",
                "position": "Machine Learning Engineer",
                "bio": "Alaine Tobias is a machine learning engineer at IntellicoAI, where she has been working for the past 5 years. She specializes in developing and implementing advanced algorithms to solve complex business problems. Alaine holds a degree in Computer Science, and has experience in various areas of machine learning, including natural language processing, computer vision, and deep learning. She is passionate about using her skills to help companies leverage the power of AI to improve their operations and gain a competitive edge in their industry.",
                "image": "resources/imgs/alaine.jpg"
            },
            {
                "name": "Umar Kabir",
                "position": "Data Scientist",
                "bio": "Umar Kabir is a data scientist at IntellicoAI, where he specializes in data analysis, modeling, and machine learning. He holds a degree in Computer Science and a graduate degree in Data Science. With over 5 years of experience in the field, Umar has worked on a wide range of projects, from natural language processing to predictive modeling. He is skilled in using various data science tools and technologies, such as Python, R, and SQL. Umar is passionate about using data to uncover insights and drive business decisions. He is also a strong communicator, able to clearly explain complex data-driven insights to stakeholders at all levels of an organization.",
                "image": "resources/imgs/umar.jpg"
            },
            {
                "name": "Sello Simon Nong",
                "position": "Data Engineer",
                "bio": "Sello Simon Nong is a data engineer at IntellicoAI, where he is responsible for designing, building, and maintaining the company's data infrastructure. With over 5 years of experience in the field, he has a deep understanding of data management, data warehousing, and data pipelines. Sello holds a degree in Computer Science, and is skilled in using various programming languages such as Python, Java and SQL. He has experience working with big data technologies such as Apache Hadoop, Apache Spark and Apache Kafka. Sello is passionate about creating efficient and scalable data systems to support the company's data science and machine learning efforts. He is dedicated to ensuring that the data is accurate, timely, and accessible to all stakeholders.",
                "image": "resources/imgs/sello.jpg"
            },
            {
                "name": "Hafsa Shariff Abass",
                "position": "Data Analyst",
                "bio": "Hafsa Shariff Abass is a data analyst at IntellicoAI, where she is responsible for analyzing and interpreting large sets of data to provide insights that drive business decisions. She holds a degree in statistics and has over 3 years of experience in the field. Hafsa has experience working with various data analysis tools and technologies such as Python, R and SQL. She is skilled in data visualization, statistical modeling, and data mining. She is also proficient in using machine learning techniques to uncover patterns and trends in data. Hafsa is passionate about turning data into actionable insights and is dedicated to helping her clients make better data-driven decisions.",
                "image": "resources/imgs/hafsa.jpg"
            },
            {
                "name": "Iman Fasasi",
                "position": "Business Analyst",
                "bio": "Iman Fasasi is a business analyst at IntellicoAI, where she is responsible for identifying and analyzing business opportunities, trends, and challenges. She holds a degree in Business Administration and has over 5 years of experience in the field. Iman has experience working with various data analysis tools and technologies such as Excel and SQL. She is skilled in creating financial models, conducting market research, and developing business cases. She is also an expert in using data analysis and visualization techniques to identify patterns, trends and opportunities that can help the company to optimize operations and improve performance. Iman is passionate about using data and analytics to inform business strategy, and is dedicated to helping her clients make better data-driven decisions.",
                "image": "resources/imgs/iman.jpg"
            }
        ]

        for member in team_members:
            st.subheader(member["name"])
            st.write(member["position"])
            # Open and show the image
            image = Image.open(member["image"])
            
            # Create a circular mask
            mask = Image.new("L", image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rectangle((10, 10) + image.size, fill=255)
            # Apply the mask to the image
            image.putalpha(mask)
            st.image(image, use_column_width=True, caption=member["bio"])

if __name__ == '__main__':
    main()
