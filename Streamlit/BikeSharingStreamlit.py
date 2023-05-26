### Streamlit app for visualizing the results of the model

# Importing the needed libraries and packages

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import shap
import streamlit as st

st.set_option("deprecation.showPyplotGlobalUse", False)


logo_path = "Desktop\GitHubProjects\BikeSharing\Streamlit\Data\logo.png"
#Display image on sidebar
st.sidebar.image(logo_path, use_column_width=True)


intro = st.sidebar.button("Introduction")
insights = st.sidebar.button("Insights")
ml = st.sidebar.button("Machine Learning")
forecast = st.sidebar.button("Forecast")

shap_data = pd.read_csv("Desktop\GitHubProjects\BikeSharing\Streamlit\Data\shap.csv")
full_data = pd.read_csv("Desktop\GitHubProjects\BikeSharing\Streamlit\Data\df.csv", index_col=0)

full_data["datetime"] = pd.to_datetime(full_data["datetime"])

full_data["year"] = full_data["datetime"].dt.year
full_data["month"] = full_data["datetime"].dt.month
full_data["day"] = full_data["datetime"].dt.day


st.sidebar.markdown("# Data Filters")

filtered_data = full_data

year_options = ["All"] + list(full_data.year.unique())
year_range = st.sidebar.selectbox("Select a year range:", year_options)

holiday_options = ["All"] + list(full_data.holiday.unique())
holiday_option = st.sidebar.selectbox("Holiday:", holiday_options)

season_options = ["All"] + list(full_data.season.unique())
season_option = st.sidebar.selectbox("Season:", season_options)

if year_range != "All":
    filtered_data = filtered_data.loc[(filtered_data.year == year_range)]

if holiday_option != "All":
    filtered_data = filtered_data.loc[(filtered_data.holiday == holiday_option)]

if season_option != "All":
    filtered_data = filtered_data.loc[(filtered_data.season == season_option)]


if intro:
    st.title("Bike Sharing in Washington DC")

    ## INTRODUCTION ##

    st.markdown("📍 Todays date: 31/12/2012")

    st.markdown(
        """
    The following StreamLit app has been created to visualize and provide insights into our main objectives for the Bike Sharing Demand project.
    
    The main goals are:
    - To derive meaningful insights with regard to how citizens use the bike-sharing service in Washington DC and propose potential product improvements. 
    - To build a predictive model that can predict the total number of bike users on an hourly basis in an effort to optimize bike provisioning and reduce costs. 

    """
    )

    ## CONTENTS ##
    st.header(" 💥 Our Approach")
    st.markdown(
        """
    -	Data Engineering 
	   - Ingesting
	   - Preprocessing
	   - Aggregating
	   - Enriching
       - Insights 
-	Machine Learning 
	   - Column Transformer 
	   - Model Selection 
	   - Hyperparameter tuning 
       - Model Evaluation
       - Model Explanation
	   - Forecasting Unseen Data
-	Forecast for tomorrow 
    """
    )

    ## DATA ENGINEERING ##
    st.header("🔍 Data Engineering")

    st.markdown(
        """
    While this was an iterative process, we enhanced our approach to achieving your objectives by enriching the data with new more accurate features. 
    We did this by using the following database: https://www.visualcrossing.com/weather/weather-data-services.
    
    This resource offers meteorological data about any given location in the world at any given time. Given todays date is 2012 / 12 / 31 😉. 
    This data repository also provided our team with the most accurate weather predictions ever for the first quarter of 2013… crazy!
    
    This way we can more accurately assess our model's prediction on unseen data bringing you closer to your forecasting objectives. 

    """
    )

    st.markdown("#### 📥 Ingesting")

    st.markdown(
        """##### Datasets

    The initial dataset named: "bike-sharing_hourly.csv", contained 17 features and 17379 rows representing hours of the days between 2011-1-1 and 2012-12-31. 
    Columns mainly regarded values representing the date whether or not (???). 
    The meteorological datasets contain data on weather in Washington DC on two temporal granularities:
    -	By hour of the day: "washington DC hourly.csv" (from 2011-1-1 to 2012-12-31), "TestWeatherHourly.csv" (from 2013-01-01 to 2013-03-31).
    -	By day: "washington DC Daily.csv" (from 2011-1-1 to 2012-12-31), "TestWeatherDaily.csv" (from 2013-01-01 to 2013-03-31).
    The data by the day was needed for enrichment of the weather related features in the initial data. 
    The data by the hour was necessary to extract information about exact sunrise and sundown moments for all the dates in the dataset. 
"""
    )

    st.markdown(
        """

    ##### Initial data
    A pandas Profiling Report was executed to better understand the raw data ingested. We quickly came to find out that there were 165 instants missing from the dataset.
    Given that 2012 was a leap year and 2011 was not, our dataset has 731 individual dates, so with an hourly granularity the data should have: 731 days * 24 hours = 17544 rows. 
    In the processing we therefore imputed these values but before doing so we realized that it would be useful to find weather data from a repository, and so we did. 
    ##### Meteorological Data
    A Profiling Report was also executed on the meteorological data.
    This revealed that the min and the max of columns such as temp, atemp, windspeed, humidity from the initial dataset had the exact same maximums (before min max scaling) as the values from the meteorological data in the profiling report.
    This way we confirmed that the data reconciles between the initial dataset and the extra meteorological dataset, and is indeed consistent, accurate and adequate for enriching the initial dataset. 
    The data also provided more accurate information to replace the column weathersit from the initial dataset. 
    Finally, this data includes information that will be used as "unseen" data for the the model, specifically the Q1 2013 data (after today's date). 

    """
    )

    st.markdown("#### 🧹 Preprocessing")

    st.markdown(
        """
    ##### Initial data
    - Creation of a datetime column which was used to later merge the datasets. Making the initial dataset the base table. 
    - Creation of the missing rows for the dataset. 
    - Filling missing values of imputed rows with different conditions and methods, please refer to the notebook for more details since all columns had to be imputed.

    ##### Meteorological Data
    - Creation of a datetime column.
    - From the hourly weather data, we dropped columns which were not needed for enriching the initial dataset (do we want to say how we decided what was not needed???).
    - From the daily weather data, we extracted the exact moments of sunrise and sunset. 

    This process was repeated for the upcoming weather data from 2013-1-1 to 2013-3-31.
    """
    )

    st.markdown("#### 🗜️ Aggregating")

    st.markdown(
        """
    The two main aggregations that we performed before model training were: 
    - Aggregating the data by the hour, merging the initial dataset with the hourly weather data.
    - Aggregating the the sunrise and sundown moments by the day, merging the dataframe tha resulted from the previous step with sunrise and sundown data.

    At this point we had the dataframe checked for correctness and had added more accurate weather related featues. We sorted the data frame by the datetime column. 
    The size of the dataframe was 17544 rows and 30 columns.
    """
    )

    st.markdown("#### 🌟 Enriching")
    st.markdown(
        """
    At this point we added numerous features to the dataset including; 
    - hours of sunlight 
    - minutes till sunrise
    - minutes till sunset
    - share of casual users
    - share of registered users

    We found that the most relevant features were the ones that were related to the sunlight in each day. However, soon afterwards we ended up dropping both "share of users" columns, as they introduced not needed multicollinearity into our model, reducing its overall predictive power. 
    The following dataframe resulted from the ETL process. 
    """
    )

    st.markdown("#### 📐 Macrotable")

    st.dataframe(full_data.head(10))

    ### SET UP THE SIDEBAR ###


elif insights:
    st.title("💡 Insights")
    full_data = pd.read_csv(r"Desktop\GitHubProjects\BikeSharing\Streamlit\Data\unified.csv")  # This dataset includes our forecast aswell as the actual values
    shap_data = pd.read_csv(r"Desktop\GitHubProjects\BikeSharing\Streamlit\Data\shap.csv")
    initial_data = pd.read_csv(r"Desktop\GitHubProjects\BikeSharing\Streamlit\Data\bike-sharing_hourly.csv")
    # full_data = pd.read_csv('pythonII_group7/.csv')

    fig = px.scatter(
        filtered_data,
        x="temp",
        y="cnt",
        trendline="ols",
        trendline_color_override="red",
    )
    fig.update_layout(title="Scatter Plot of Total Users by Temperatures 🌡️")
    fig

    st.markdown(
        "This graph tells us that the count of users is at its highest during warm temperatures (15-25), which makes sense."
    )
    fig = px.scatter(
        filtered_data,
        x="hr",
        y="cnt",
        trendline="lowess",
        trendline_color_override="red",
    )
    fig.update_layout(title="Scatter Plot of Total Users by Hours of the day ⏰")
    fig
    st.markdown(
        "The graph above shows an overall higher user load at 8am, 5pm and 6pm. This seems justified, as we would expect people to bike to/from work around these timelines."
    )

    # Plot a line chart by day
    filtered_data["datetime"] = pd.to_datetime(filtered_data["datetime"])
    daily_data = (
        filtered_data.iloc[0:17546,].groupby(pd.Grouper(key="datetime", freq="D")).sum()
    )
    fig = px.line(
        daily_data, x=daily_data.index, y="cnt", title="Total Users over Time (Daily) ⏳"
    )
    fig

    st.markdown(
        "The amount of users tend to increase in warm times of the year and decreases in cold times."
    )


elif ml:
    st.title("🤖 Machine Learning")

    st.header("🔀 Column Transformer")
    st.markdown(
        """
    Different columns in the dataset required different preprocessing steps before being fed into the model. 
    For this the two main transfomers were used in the column transformer: One-Hot-Encoder and Standard Scaler.
    The One-Hot-Encoder was applied to the categorical columns and the Standard Scaler to the numerical columns.
    """
    )
    st.markdown("###### Categorical Columns")
    categorical_columns = [
        "yr",
        "mnth",
        "hr",
        "holiday",
        "weekday",
        "workingday",
        "season",
        "icon",
    ]
    categorical_columns

    st.markdown("###### Numerical Columns")
    numerical_columns = [
        "temp",
        "feelslike",
        "humidity",
        "precip",
        "snowdepth",
        "windspeed",
        "cloudcover",
        "uvindex",
        "sunlight_hours",
        "mtillsunrise",
        "mtillsunset",
    ]
    numerical_columns
    st.markdown("###### Splits")
    st.markdown(
        """
    The final Preprocessed data has shape 17544, 74. 
    We then dropped the datetime column and the "cnt" column was assigned as the target variable.
    We separated unseen data for 2013 which we will later use to make forecasts. We had to pass unseen data through the same column transformer given that
    we gave the year 2013 the year value 2. It was therefore essential that even the train set was transformed to include a one-hot-encoded 
    column for the year 2013. This way the model will better understand the data it is being fed.
    We separated the data between 2012-1-1 and 2012-12-31 into a train and test set, with the test set being the most recent 30% of the data. 
               
    """
    )
    st.header(" 🎯 Model Selection")
    st.markdown("###### Evaluation Metrics ")
    # Finish. which evaluation metrics did we use?
    st.markdown(
        """
    To evaluate the model we used the R^2 score. It shows the proportion of variance in the dependent variable that can be explained by the independent variable. 
    In other words, it shows the goodness of fit of our model to the data.
    """
    )
    # #which models did we train and what were there scrores?
    st.markdown(
        """
    The models we trained included models for numerical predictions, given the regression nature of the problem.
    We trained a linear regression model, a random forest regressor, a decision tree alogrithm and XG Boost regressor and assessed their performance using the R^2 score.

        - Linear Regression Score: 0.6872
        - Decision Tree Score: 0.8906
        - Random Forest Score: 0.9351
        - XGBoost Score: 0.9391
    """
    )
    # Cross validation
    st.markdown(
        """
    We then chose the best model based on the R^2 score and performed cross validation on the model, using 5 folds and tuning the hyperparameters.
    The cross-validation settings were as follows:

    - Linear Regression: fit_intercept: [True, False]
    - Decision Tree: max_depth': [3, 5, 7, None], min_samples_leaf': [1, 5, 10], min_samples_split': [2, 5, 10]
    - Random Forest: n_estimators': [20 - we didn't pass a list as such approach takes rather a long time. Instead, we kept increasing the number until the score maxed out], max_depth: [1, 2, 3], min_samples_leaf: [1, 2, 3, 4], min_samples_split: [2, 5, 10]
    - XG Boost: learning_rate: list(np.linspace(0.01, 0.99,5)), max_depth: list(range(1,4)), n_estimators: list(range(85,140,2)), colsample_bytree: [0.5, 0.7, 1.0], subsample: [0.5, 0.7, 1.0],
    gamma: [0.1,0.3,0.8,1,3,5,8], reg_alpha: list(np.linspace(0.01, 0.99,10)), reg_lambda: list(np.linspace(0.01, 0.99,10)) 

    """
    )

    st.markdown("#### 🕵️‍♂️ Hyperparameter Tuning")
    st.markdown("###### Grid Search CV")
    # how did we tune the hyperparameters? what were the best parameters?
    st.markdown(
        """
    By using the cross validated R^2 score we tuned the hyperparameters of the model.
    We did this by using Grid Search CV and passing dictionaries with lists of values for the hyperparameters we wanted to tune.
    This was again an iterative process, we looked at the bins in which our model was getting better and then zoomed-in to those bins to find the best hyperparameters.
    The best hyperparameters for the winning model, XG Boost, were as follows:

        - learning_rate = 0.255,
        - max_depth = 3,
        - n_estimators = 1000,
        - colsample_bytree = 0.5,
        - subsample = 0.7,
        - gamma = 0.1,
        - reg_alpha = 0.446,
        - reg_lambda = 0.554
    """
    )

    st.header("📈 Model Evaluation")
    # Final model evaluation across different metrics
    #

    st.markdown("#### 💬 Model Explanation")
    st.markdown(
        """
    In an effort to explain the models predictions we used the SHAP library and SHAP values to explain the model predictions.
    Shapley Additive exPlanations (SHAP) is a game theoretic approach to explain the output of any machine learning model. 
    In this case the players are each individual matrix value and the game being played is the prediction of the total amount of users per hour. 
    The SHAP values are the marginal contribution of each feature to the prediction. 
    They show more about the magnitude in which a value impacts the prediction and at the same time showing the direction in which the model is affected when the value changes through its feature range. 
    Let's look more closely at the SHAP values for the different features in our model. 
    """
    )

    st.markdown("###### ⚖️ SHAP values absolute mean ")
    mean_data = shap_data.abs().mean().sort_values(ascending=False)
    mean_data.drop("Unnamed: 0", inplace=True)
    mean_df = pd.DataFrame(mean_data, columns=["mean"])
    fig = px.bar(mean_df, x=mean_df.index, y="mean")
    fig

    st.markdown(
        """
    The above values show the absolute importance of columns in the model. Please take note that this says nothing about in which direction the variable affects the model.
    The most important columns that affect the model the most in any direction are:

        - Minutes until sunrise
        - Temperature
        - Specific hours of the day have different importance. The hour being 18:00 is the most important hour of the day for our model predictions. 
        - When the season is 4 (Autumn) the model is affected the most. 

    This led us to look more closely at different features of the data and how they affect the model.
    We checked how the model is impacted by the weekday, day type, season, and various weather-related data by using violin plots extracted from the SHAP Library.
    """
    )

    st.markdown("###### 🕒 SHAP Values for hours of the day ")
    st.pyplot(
        shap.summary_plot(
            shap_values=shap_data.iloc[:, 15:39].values,
            features=shap_data.iloc[:, 15:39],
            plot_type="violin",
        )
    )
    st.markdown(
        """
    From the above violin plot we can see that the hours between 17:00 and 19:00 and the hours between 07:00 and 08:00 are the most important hours of the day. 
    When those hours are 1 our model is affected the most when compared to other hours of the day. Specifically in those hours the model is affected positively meaning it is predicted values are higher.
    Hours in the middle of the night and during lunchtime are the least important hours of the day for our predictions and in fact have a negative effect on the model, meaning that the model predicts lower values when those hours are 1.

    This makes sense with normal traffic routes and patterns. People are more likely to use the bike sharing service during rush hours and during lunch time.
    """
    )

    st.markdown("###### 🗓️ SHAP Values for days of the week ")
    st.pyplot(
        shap.summary_plot(
            shap_values=shap_data.iloc[:, 41:50].values,
            features=shap_data.iloc[:, 41:50],
            plot_type="violin",
        )
    )
    st.markdown(
        """
    It is evident from the violin plot above that the bikes are mainly used on workdays. When workday is 0 our prediction actually decreases.
    This is probably due to the fact that people are more likely to use bikes for commuting to work and back home than for leisure activities. 
    Days in the weekend where the weekday is 6 or 0 most affect our model negatively of all the days, while non-weekend days (1-5) have a positive effect on our prediction. 
    with Friday impacting positive prediction the most of all the columns representing days of the week. 
    """
    )

    st.markdown("###### 🍂❄️ SHAP Values for seasons of the year 🌸")
    st.pyplot(
        shap.summary_plot(
            shap_values=shap_data.iloc[:, 51:56].values,
            features=shap_data.iloc[:, 51:56],
            plot_type="violin",
        )
    )
    # For each insert the inshgtful comment about the plot
    st.markdown(
        """
    We see here that during winter people bike the least and our predictions are negatively affected by season being one (winter). 
    The most important season for our model is the autumn season with the highest positive effect on our predictions. The summer season had the least impact on our predictions.
    We considered that during the summer months different features become more important and not the season per se. We can overall say that the winter months have relatively smaller business than the summer months.
    """
    )

    st.markdown("###### 🌤️ SHAP Values for weather icons ")
    st.pyplot(
        shap.summary_plot(
            shap_values=shap_data.iloc[:, 56:64].values,
            features=shap_data.iloc[:, 56:64],
            plot_type="violin",
        )
    )
    # For each insert the inshgtful comment about the plot
    st.markdown(
        """
    Next, we looked at the weather icons - one of the categorical variables in the weather datasets that we considered useful for our analysis.
    We checked how weather icons affect our model and your customers' habits. For instance, when the weather icon is 'rain', it is has a negative prediction impact on our model.

    """
    )

    st.markdown("###### 🌦️ SHAP Values for weather data ")
    st.pyplot(
        shap.summary_plot(
            shap_values=shap_data.iloc[:, 64:74].values,
            features=shap_data.iloc[:, 64:74],
            plot_type="violin",
        )
    )
    # For each insert the inshgtful comment about the plot
    st.markdown(
        """
    Here we saw that temperature has quite a significant feature value, and the impact on the predictions can go in opposite ways. 
    Precipitation and windspeed have a high feature value, but compared to temperature, the have mostly a negative impact on the prediction.    
    """
    )


elif forecast:
    year_range = st.sidebar.selectbox("Select a year range:", full_data.year.unique())

    filtered_data = full_data.loc[(full_data.year == year_range)]
    # # Display the filtered data

    st.title(" 🔮 Forecast")

    st.markdown(
        """
    In the final part, we re-trained our winner model on the complete dataset. The complete dataset consisted of the following parts: 
    - The original 2011-2012 bike data, provided by the client,
    - Weather data we found online for 2011-2012,
    - Weather predictions for the first three months of 2013 (Q1 2013). 
    
    We re-trained the XG Boost model on the complete 2011-2012 data and made predictions on the bike count in Q1 2013. Our final dataframe therefore consists of historical information for 2011-2012 and forecast for Q1 2013 that we hope will add value to client's decision-making.
    
    """
    )

    full_data = pd.read_csv("Desktop\GitHubProjects\BikeSharing\Streamlit\Data\df.csv", index_col=0)

    full_data["datetime"] = pd.to_datetime(full_data["datetime"])

    full_data["year"] = full_data["datetime"].dt.year
    full_data["month"] = full_data["datetime"].dt.month
    full_data["day"] = full_data["datetime"].dt.day

    reduced_data = full_data[["datetime", "year", "mnth", "day", "hr", "cnt"]]

    grouped_data = (
        reduced_data.groupby(reduced_data["datetime"].dt.date)["cnt"]
        .sum()
        .reset_index()
    )

    df_blue = grouped_data[grouped_data["datetime"] < pd.to_datetime("2013-01-01")]
    df_red = grouped_data[grouped_data["datetime"] >= pd.to_datetime("2013-01-01")]

    fig = px.line(
        grouped_data, x="datetime", y="cnt", title="Rental bike count (daily)"
    )

    # fig = px.line(df_blue, x=reduced_data.index, reduced_data.values, title='Rental bike count')
    fig.update_traces(line=dict(color="blue"))

    # add red line
    fig.add_scatter(
        x=df_red["datetime"],
        y=df_red["cnt"],
        mode="lines",
        name="Predicted",
        line=dict(color="red")
    )

    # update layout
    fig.update_layout(xaxis_title="Date", yaxis_title="Count")
    fig

    st.markdown(
        "From the graph we can see that our Q1 2013 prediction follows the shape of the actual data pertaining to Q1 2011 and Q1 2012."
    )

else:
    st.title("Bike Sharing in Washington DC")

    st.markdown(
        '<p style="font-family:arial; font-size:24px; color:#23395d;"><b> 👋 ️🚴‍♀️ Welcome to ourlLanding page streamlit projec!</b></p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """

    As we approach the end of 2012, we're super excited to dive into the fascinating world of bike sharing and uncover insights into how citizens of our nation's capital utilize this service. 💡 With the aim of improving the overall bike sharing experience, we're using advanced data analysis techniques to identify potential areas for product improvement. 📈

    But that's not all! Our app also includes a state-of-the-art predictive model 🤖 that accurately forecasts the total number of bike users on an hourly basis. By leveraging the power of machine learning, we hope to help public transport department optimize their bike provisioning and reduce operational costs. 💰

    Whether you're a bike sharing enthusiast 🚲, a data science aficionado 🤓, or simply someone who wants to learn more about how we can use technology to make our cities more efficient and sustainable ♻️, you've come to the right place. Let's explore the world of bike sharing together! 🌎
                    """
    )

    st.markdown(
        "Feel free to navigate to other sections of the page in the left menu!",
        unsafe_allow_html=True,
    )

    st.subheader("Created by:")
    st.markdown(
        "Niels van Meijel, Roman Zotkin, Mariana Osório, Daniel Sebastian, Alberto Fuentes, Fabio Venturini, Muriel Vergara",
        unsafe_allow_html=True,
    )
