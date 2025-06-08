

import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import re

Page = st.sidebar.radio('Navigation',['Home','Interactive Visualizations','Interactive Filtering'])

if Page =='Home':

    st.markdown(
        "<h1 style='text-align: center; color: blue;'>Welcome to Sailaja MiniProject Demo</h1>", 
        unsafe_allow_html=True
    )

    st.image("C:/Users/muthu/OneDrive/Desktop/Python/2024 Movie Analysis.png")

#st.markdown(" " * 300 + "# Welcome to Sailaja MiniProject Demo")




elif Page=='Interactive Visualizations':
    st.title("Visualization Page")

    option = st.selectbox('Select an option',["Top 10 Movies by Rating and Voting Counts",'Genre Distribution','Average Duration by Genre','Voting Trends by Genre','Rating Distribution','Genre-Based Rating Leaders','Most Popular Genres by Voting','Duration Extremes','Ratings by Genre','Correlation Analysis'],index=0)
    
    if option=='Top 10 Movies by Rating and Voting Counts':
        DATABASE_URL = "mysql+pymysql://Harshu:root@localhost/world"
        engine = create_engine(DATABASE_URL)

        rating_query = """
        SELECT Title, Rating
        FROM imdb_movies_list 
        ORDER BY Rating DESC
        LIMIT 10
        """
        df_rating = pd.read_sql(rating_query, engine)

        voting_query = """
        SELECT Title, Voting
        FROM imdb_movies_list 
        ORDER BY Voting DESC
        LIMIT 10
        """
        df_voting = pd.read_sql(voting_query, engine)

        query = """
        SELECT Title, Rating, Voting
        FROM imdb_movies_list 
        ORDER BY Rating DESC, Voting DESC
        LIMIT 10
        """
        df_rating_voting = pd.read_sql(query, engine)

        tab1, tab2, tab3 = st.tabs(["Top 10 Movies by Rating", "Top 10 Movies by Voting", "Top 10 Movies by Rating and Voting Counts"])
        
        with tab1:
            #st.subheader("🎬 Top 10 Movies by Rating Counts")
            #st.dataframe(df_rating)

            fig_rating = px.bar(df_rating, x="Title", y="Rating", title="Top 10 Movies by Rating")
            st.plotly_chart(fig_rating)

        with tab2:
            #st.subheader("📊 Top 10 Movies by Voting Counts")
            #st.dataframe(df_voting)

            fig_voting = px.bar(df_voting, x="Title", y="Voting", title="Top 10 Movies by Voting")
            st.plotly_chart(fig_voting)

        with tab3:
            #st.subheader("📊 Top 10 Movies by Rating and Voting Counts")
            #st.dataframe(df_rating_voting)

            fig = px.bar(df_rating_voting, x="Title", y=["Rating", "Voting"], title="Top 10 Movies by Rating and Voting Counts")
            st.plotly_chart(fig)

    if option=='Genre Distribution':
        DATABASE_URL = "mysql+pymysql://Harshu:root@localhost/world"
        engine = create_engine(DATABASE_URL)

        Genre_query = """
        SELECT Genre, COUNT(*) AS Movie_count
        FROM imdb_movies_list 
        GROUP BY Genre
        """
        df_Genre = pd.read_sql(Genre_query, engine)

        #st.subheader("Genre Distribution")
        #st.dataframe(df_Genre)
        
        fig, ax = plt.subplots()
        ax.bar(df_Genre["Genre"], df_Genre["Movie_count"], color="skyblue")
        ax.set_xlabel("Genre")
        ax.set_ylabel("Movie Count")
        ax.set_title("Genre Distribution Bar Chart")
        st.pyplot(fig)

    if option=='Average Duration by Genre':
        DATABASE_URL = "mysql+pymysql://Harshu:root@localhost/world"
        engine = create_engine(DATABASE_URL)

        Duration_Genre_query = """
        SELECT Genre, AVG(Duration) AS Average_Duration
        FROM imdb_movies_list 
        GROUP BY Genre
        """
        df_Genre_Duration = pd.read_sql(Duration_Genre_query, engine)

        #st.subheader("Average Movie Duration by Genre")
        #st.dataframe(df_Genre_Duration)  

        fig, ax = plt.subplots()
        ax.barh(df_Genre_Duration["Genre"], df_Genre_Duration["Average_Duration"], color="lightcoral")
        ax.set_xlabel("Average Duration")
        ax.set_ylabel("Genre")
        ax.set_title("Average Movie Duration by Genre")
        st.pyplot(fig)
    
    if option=='Voting Trends by Genre':
        DATABASE_URL = "mysql+pymysql://Harshu:root@localhost/world"
        engine = create_engine(DATABASE_URL)

        Voting_Genre_query = """
        SELECT Genre, AVG(Voting) AS Average_Voting
        FROM imdb_movies_list 
        GROUP BY Genre
        """
        df_Voting_Genre = pd.read_sql(Voting_Genre_query, engine)

        #st.subheader("Voting Trends by Genre")
        #st.dataframe(df_Voting_Genre)  

        fig, ax = plt.subplots()
        ax.plot(df_Voting_Genre["Genre"], df_Voting_Genre["Average_Voting"], marker="o", linestyle="-", color="dodgerblue")
        ax.set_xlabel("Genre")
        ax.set_ylabel("Average Votes")
        ax.set_title("Average Voting Counts Across Genres")
        ax.grid(True)
        st.pyplot(fig)

    if option=='Rating Distribution':
        DATABASE_URL = "mysql+pymysql://Harshu:root@localhost/world"
        engine = create_engine(DATABASE_URL)

        Rating_Distribution_query = """
        SELECT Rating
        FROM imdb_movies_list 
        """
        df_Rating_Distribution = pd.read_sql(Rating_Distribution_query, engine)

        #st.subheader("Rating Distribution")
        #st.dataframe(df_Rating_Distribution)  

        fig, ax = plt.subplots()
        sns.histplot(df_Rating_Distribution["Rating"], bins=20, kde=True, color="skyblue", ax=ax)
        ax.set_xlabel("Rating")
        ax.set_ylabel("Frequency")
        ax.set_title("Movie Ratings Distribution")
        st.pyplot(fig)

    if option=='Genre-Based Rating Leaders':
        DATABASE_URL = "mysql+pymysql://Harshu:root@localhost/world"
        engine = create_engine(DATABASE_URL)

        GenreVsRating_query = """
        SELECT Genre, Title, Rating FROM imdb_movies_list 
        WHERE (Genre, Rating) IN (
        SELECT Genre, MAX(Rating) FROM imdb_movies_list GROUP BY Genre
        )
        ORDER BY Genre;
        """
        df_GenreVsRating = pd.read_sql(GenreVsRating_query, engine)

        st.subheader("Top-Rated Movie for Each Genre")
        st.table(df_GenreVsRating) 

    if option=='Most Popular Genres by Voting':
        DATABASE_URL = "mysql+pymysql://Harshu:root@localhost/world"
        engine = create_engine(DATABASE_URL)

        GenreVsVoting_query = """
        SELECT Genre, SUM(Voting) AS Total_votes
        FROM imdb_movies_list
        GROUP BY Genre
        """
        df_GenreVsVoting = pd.read_sql(GenreVsVoting_query, engine)

        #st.subheader("Most Popular Genres by Voting")
        #st.dataframe(df_GenreVsVoting)   

        fig, ax = plt.subplots()
        ax.pie(df_GenreVsVoting["Total_votes"], labels=df_GenreVsVoting["Genre"], autopct="%1.1f%%", startangle=90, colors=plt.cm.Paired.colors)
        ax.set_title("Genres by Voting in Pie Chart")
        st.pyplot(fig)

    if option=='Duration Extremes':
        DATABASE_URL = "mysql+pymysql://Harshu:root@localhost/world"
        engine = create_engine(DATABASE_URL)

        df_Shortestlongestmovie = pd.read_sql("SELECT Title, Genre, Duration FROM imdb_movies_list;", engine)

        def convert_to_minutes(Duration):
            hours = re.search(r"(\d+)h", Duration)
            minutes = re.search(r"(\d+)m", Duration)
        
            hours = int(hours.group(1)) * 60 if hours else 0
            minutes = int(minutes.group(1)) if minutes else 0
            
            return hours + minutes

        df_Shortestlongestmovie["Duration"] = df_Shortestlongestmovie["Duration"].apply(convert_to_minutes)

        df_Shortestlongestmovie["Duration"] = pd.to_numeric(df_Shortestlongestmovie["Duration"], errors="coerce")

        df_Shortestlongestmovie = df_Shortestlongestmovie.dropna(subset=["Duration"])

        df_Shortestlongestmovie = df_Shortestlongestmovie.sort_values(by="Duration", ascending=True)

        shortest_movie = df_Shortestlongestmovie.iloc[0]
        longest_movie = df_Shortestlongestmovie.iloc[-1]

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🎬 Shortest Movie")
            st.write(f"**Title:** {shortest_movie['Title']}")
            st.write(f"**Genre:** {shortest_movie['Genre']}")
            st.write(f"**Duration:** {shortest_movie['Duration']} mins")


        with col2:
            st.subheader("🎥 Longest Movie")
            st.write(f"**Title:** {longest_movie['Title']}")
            st.write(f"**Genre:** {longest_movie['Genre']}")
            st.write(f"**Duration:** {longest_movie['Duration']} mins")

    if option=='Ratings by Genre':
        DATABASE_URL = "mysql+pymysql://Harshu:root@localhost/world"
        engine = create_engine(DATABASE_URL)

        RatingsbyGenre_query = """
        SELECT Genre, AVG(Rating) AS Avg_Rating
        FROM imdb_movies_list
        GROUP BY Genre
        """
        df_RatingsbyGenre = pd.read_sql(RatingsbyGenre_query, engine)

        #st.subheader("Most Popular Genres by Voting")
        #st.dataframe(df_RatingsbyGenre)  

        df_RatingsbyGenre = df_RatingsbyGenre.pivot_table(values="Avg_Rating", index="Genre") 

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(df_RatingsbyGenre, cmap="coolwarm", annot=True, fmt=".2f", linewidths=0.5, ax=ax)
        ax.set_title("Average Ratings Across Genres")
        st.pyplot(fig)
    
    if option=='Correlation Analysis':
        DATABASE_URL = "mysql+pymysql://Harshu:root@localhost/world"
        engine = create_engine(DATABASE_URL)

        RatingVsVoting_query = """
        SELECT Rating, Voting
        FROM imdb_movies_list
        """
        df_RatingvsVoting = pd.read_sql(RatingVsVoting_query, engine)

        #st.subheader("Correlation Analysis Rating Vs Voting")
        #st.dataframe(df_RatingVsVoting)  

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(x=df_RatingvsVoting["Rating"], y=df_RatingvsVoting["Voting"], color="dodgerblue", alpha=0.6)
        ax.set_xlabel("Movie Rating")
        ax.set_ylabel("Vote Count")
        ax.set_title("Scatter Plot of Ratings vs Voting Counts")
        ax.grid(True)
        st.pyplot(fig)

elif Page=='Interactive Filtering':
    

    DATABASE_URL = "mysql+pymysql://Harshu:root@localhost/world"
    engine = create_engine(DATABASE_URL)

    Movie_query = """
    SELECT Title, Genre, Duration, Rating, Voting
    FROM imdb_movies_list
    """
    df_Moviefiltering = pd.read_sql(Movie_query, engine)

    st.title("🎬 Movie Dataset Filtering")
    st.sidebar.subheader("Apply Filters")

    def convert_to_minutes(Duration):
        hours = re.search(r"(\d+)h", Duration)
        minutes = re.search(r"(\d+)m", Duration)
    
        hours = int(hours.group(1)) * 60 if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        
        return hours + minutes

    df_Moviefiltering["Duration"] = df_Moviefiltering["Duration"].apply(convert_to_minutes)

    df_Moviefiltering["Duration"] = pd.to_numeric(df_Moviefiltering["Duration"], errors="coerce")

    df_Moviefiltering = df_Moviefiltering.dropna(subset=["Duration", "Rating", "Voting"])

    duration_range = st.sidebar.slider("Select Duration Range", min_value=3, max_value=240, value=(120, 180))
    df_Moviefiltering = df_Moviefiltering[(df_Moviefiltering["Duration"] >= duration_range[0]) & (df_Moviefiltering["Duration"] <= duration_range[1])]

    rating_threshold = st.sidebar.slider("Select Rating", min_value=0.0, max_value=10.0, value=(8.0, 9.0))
    df_Moviefiltering = df_Moviefiltering[(df_Moviefiltering["Rating"] >= rating_threshold[0]) & (df_Moviefiltering["Rating"] <= rating_threshold[1])]

    vote_threshold = st.sidebar.number_input("Select Voting", min_value=0, value=10000, step=5000)
    df_Moviefiltering = df_Moviefiltering[df_Moviefiltering["Voting"] >= vote_threshold]
    
    selected_genres = st.sidebar.multiselect("Select Genre(s)", options=df_Moviefiltering["Genre"].unique(), default=["Action"])
    df_Moviefiltering = df_Moviefiltering[df_Moviefiltering["Genre"].isin(selected_genres)]

    st.subheader("Filtered Movies")
    st.write(df_Moviefiltering)