import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

# File upload
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    # preprocess
    df = preprocessor.preprocess(data)

    # extract users
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if selected_user == "Overall":
        display_df = df.copy()
    else:
        display_df = df[df['user'] == selected_user].copy()

    display_df['message'] = display_df['message'].str.replace(
    '<Media omitted>',
    '📷 Media File',
    regex=False
    )

    # show all columns
    st.dataframe(display_df,use_container_width=True)

    # =========================
    #  MAIN ANALYSIS BUTTON
    # =========================
    if st.sidebar.button("Show Analysis"):

        # ===== FETCH STATS =====
        stats = helper.fetch_stats(selected_user, df)

        # ===== TOP STATS =====
        st.subheader("Top Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Messages", stats["messages"])

        with col2:
            st.metric("Words", stats["words"])

        with col3:
            st.metric("Media", stats["media"])
 
        with col4:
            st.metric("Links", stats["links"])

        # =========================
        #  MOST BUSY USERS
        # =========================
        if selected_user == "Overall":
            st.title("Most Busy Users")

            x, new_df = helper.most_busy_users(df)

            col1, col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # =========================
        #  WORDCLOUD
        # =========================
        st.title("WordCloud")

        df_wc = helper.create_wordcloud(selected_user, df)

        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis("off")
        st.pyplot(fig)

        # =========================
        #  MOST COMMON WORDS
        # =========================
        # st.title("Most Common Words")

        # common_df = helper.most_common_words(selected_user, df)

        # fig, ax = plt.subplots()
        # ax.barh(common_df[0], common_df[1])
        # plt.xticks(rotation='vertical')
        # st.pyplot(fig)

        common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots(figsize=(8,5))

        ax.barh(
            common_df['Word'],
            common_df['Count']
        )

        ax.set_xlabel("Frequency")
        ax.set_ylabel("Words")
        ax.set_title("Top 20 Most Common Words")

        plt.tight_layout()

        st.pyplot(fig)

        # =========================
        # EMOJI ANALYSIS
        # =========================
        # import plotly.express as px

        # st.title("Emoji Analysis")

        # emoji_df = helper.emoji_helper(selected_user, df)

        # col1, col2 = st.columns(2)

        # # 👉 Table
        # with col1:
        #   st.dataframe(emoji_df)

        # # 👉 Plotly Chart (BEST)
        # with col2:
        #   fig = px.bar(
        #   emoji_df.head(10),
        #   x='Emoji',
        #   y='Count',
        #   title="Top Emojis"
        #   )
        # st.plotly_chart(fig)
        
        import plotly.express as px

        st.title("Emoji Analysis")

        emoji_df = helper.emoji_helper(selected_user, df)

        # 👉 side-by-side layout
        col1, col2 = st.columns(2)


        with col1:
            st.dataframe(emoji_df, use_container_width=True)

        # RIGHT → PIE CHART

        with col2:
            fig = px.pie(
                emoji_df.head(8),
                names='Emoji',
                values='Count',
                title="Top Emojis"
            )

        # styling
        fig.update_traces(
        textinfo='percent+label',
        textfont=dict(size=14, color='black')
        )

        fig.update_layout(
        template="plotly_white",
        showlegend=True
        )

        # ✅ ONLY ONE CALL + UNIQUE KEY
        st.plotly_chart(fig, use_container_width=True, key="emoji_pie_chart")

        # =========================
        #  TIMELINE
        # =========================
# =========================
# 🔥 MONTHLY TIMELINE
# =========================
        st.title("Monthly Timeline")

        timeline = helper.monthly_timeline(selected_user, df)

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(
        timeline['time'],
        timeline['message'],
        marker='o',
        linewidth=2
        )

        # labels
        ax.set_title("Monthly Message Trend", fontsize=16)
        ax.set_xlabel("Month-Year", fontsize=12)
        ax.set_ylabel("Number of Messages", fontsize=12)

        # rotate labels
        plt.xticks(rotation=45, ha='right')

        # grid
        ax.grid(True, linestyle='--', alpha=0.6)

        plt.tight_layout()

        st.pyplot(fig)

        # =========================
        # 🔥 DAILY TIMELINE
        # =========================
        # st.title("Daily Timeline")

        # daily_timeline = helper.daily_timeline(selected_user, df)

        # fig, ax = plt.subplots()
        # ax.plot(daily_timeline['date'], daily_timeline['message'])
        # plt.xticks(rotation='vertical')
        # st.pyplot(fig)
        # =========================
        # 🔥 DAILY TIMELINE
        # =========================
        st.title("Daily Timeline")

        daily_timeline = helper.daily_timeline(selected_user, df)

        fig, ax = plt.subplots(figsize=(10, 5))

        # plot with line + markers
        ax.plot(
           daily_timeline['date'],
           daily_timeline['message'],
           marker='o',
        linewidth=2
        )

        # labels
        ax.set_title("Daily Message Trend", fontsize=16)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Number of Messages", fontsize=12)

        # rotate x-axis for readability
        plt.xticks(rotation=45)

        # grid for better visualization
        ax.grid(True, linestyle='--', alpha=0.6)

        # layout fix
        plt.tight_layout()

        # display
        st.pyplot(fig)

        # week timeline
        # =========================
# 🔥 WEEKDAY ACTIVITY
# =========================
        st.title("Weekly Activity")

        week_activity = helper.week_activity_map(selected_user, df)

        # reorder days properly
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        week_activity = week_activity.reindex(days_order)

        fig, ax = plt.subplots(figsize=(8,5))

        ax.bar(week_activity.index, week_activity.values)

        ax.set_title("Messages per Day of Week")
        ax.set_xlabel("Day")
        ax.set_ylabel("Number of Messages")

        plt.xticks(rotation=45)

        st.pyplot(fig)

        # =========================
        # 🔥 HEATMAP
        # =========================
        st.title("Activity Heatmap")

        heatmap = helper.activity_heatmap(selected_user, df)

        import seaborn as sns

        fig, ax = plt.subplots(figsize=(10,5))

        sns.heatmap(heatmap, cmap='YlGnBu')
        ax.set_xlabel("Hour Interval")
        ax.set_ylabel("Day")

        st.pyplot(fig)

        # response time analysis 

        # =========================
        # RESPONSE TIME ANALYSIS
        # =========================
        # st.title("Response Time Analysis")

        # response_df = helper.response_time_analysis(df)

        # # 📊 Bar Chart (fastest at top)
        # import plotly.express as px

        # fig = px.bar(
        # response_df.head(10),
        # x='user',
        # y='avg_response_time',
        # title="Average Response Time (minutes)",
        # labels={'avg_response_time': 'Minutes', 'user': 'User'}
        # )

        # fig.update_layout(template="plotly_white")

        # st.plotly_chart(fig, use_container_width=True)

        # # 📋 Table
        # st.subheader("Average Response Time Table")
        # st.dataframe(response_df)

        import matplotlib.pyplot as plt
        import streamlit as st
        import helper

        st.title("Response Time Analysis")

        response_df = helper.response_time_analysis(selected_user, df)

        if selected_user == 'Overall':

            if not response_df.empty:

                fig, ax = plt.subplots(figsize=(10, 5))

                ax.bar(response_df['user'], response_df['avg_response_time'])

                ax.set_title("Average Response Time (minutes)")
                ax.set_xlabel("User")
                ax.set_ylabel("Minutes")

                plt.xticks(rotation=45)

                st.pyplot(fig)

                # 🔥 Fastest responder
                fastest = response_df.iloc[0]
                st.success(f"⚡ Fastest Responder: {fastest['user']} ({fastest['avg_response_time']:.2f} min)")
        
            else:
                st.warning("No response data available")

        else:

            if not response_df.empty:

                avg_time = response_df['avg_response_time'].values[0]

                st.subheader("Response Insights")

                col1, col2 = st.columns(2)

                # ⏱️ Average time
                with col1:
                    st.metric("Avg Response Time", f"{avg_time:.2f} min")

                # 🚀 Speed category
                with col2:
                    if avg_time < 2:
                        st.success("⚡ Fast Responder")
                    elif avg_time < 5:
                        st.info("🙂 Moderate Responder")
                    else:
                        st.warning("🐢 Slow Responder")

            else:
                st.warning("No response data available for this user")

        # sentiment analysis
        # =========================
        #  SENTIMENT ANALYSIS
       # =========================
        st.title("Sentiment Analysis")

        sentiment_df = helper.sentiment_analysis(selected_user, df)

        # 📊 Pie Chart
        import plotly.express as px

        fig = px.pie(
        sentiment_df,
        names='Sentiment',
        values='Count',
        title="Sentiment Distribution",
        color='Sentiment',
        color_discrete_map={
        'Positive': 'green',
        'Neutral': 'gray',
        'Negative': 'red'
        }
        )

        fig.update_traces(
        textinfo='percent+label',
        textfont=dict(size=14, color='black')
        )

        fig.update_layout(template="plotly_white")

        st.plotly_chart(fig, use_container_width=True, key="sentiment_pie")

        # 📋 Table
        st.subheader("Sentiment Breakdown")
        st.dataframe(sentiment_df)