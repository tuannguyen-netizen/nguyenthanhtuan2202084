import streamlit as st
import yt_dlp
import time
import pandas as pd
import plotly.express as px

# Function to fetch video data from YouTube
def fetch_video_data(video_url):
    try:
        with yt_dlp.YoutubeDL({"quiet": True, "skip_download": True}) as ydl:
            info = ydl.extract_info(video_url, download=False)
        
        return {
            "Views": info.get("view_count", 0),
            "Likes": info.get("like_count", 0),
            "Comments": info.get("comment_count", 0),
            "Timestamp": pd.Timestamp.now()
        }
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

# Function to create line charts
def create_line_chart(df, column, title, color):
    if len(df) < 2:
        return None

    df["Change"] = df[column].diff()  # Calculate change compared to the previous record

    fig = px.line(df, x="Timestamp", y=column, title=title, markers=True)
    fig.update_traces(line=dict(color=color, width=2))

    # Adjust display settings
    fig.update_layout(
        xaxis=dict(showgrid=True, tickangle=45),
        yaxis=dict(showgrid=True, zeroline=True),
        hovermode="x unified"
    )

    # Add tooltip to display changes
    fig.update_traces(
        hovertemplate="<b>Time:</b> %{x}<br>"
                      "<b>Value:</b> %{y}<br>"
                      "<b>Change:</b> %{customdata}",
        customdata=df["Change"]
    )

    return fig

# Main function
def main():
    st.set_page_config(layout="wide")
    st.title("🎥 YouTube Video Statistics Tracker")

    # Sidebar configuration
    st.sidebar.header("Tracking Settings")
    update_interval = st.sidebar.slider("Update Interval (seconds)", 5, 60, 10)
    VIDEO_URL = st.sidebar.text_input("YouTube Video URL", "https://youtu.be/ESw0aKi8elE")

    # Tracking status
    if "tracking" not in st.session_state:
        st.session_state.tracking = False
        st.session_state.data = pd.DataFrame(columns=["Timestamp", "Views", "Likes", "Comments"])

    # Start/Stop button
    if st.session_state.tracking:
        if st.sidebar.button("Stop Tracking"):
            st.session_state.tracking = False
            st.success("Tracking stopped")
    else:
        if st.sidebar.button("Start Tracking"):
            st.session_state.tracking = True
            st.session_state.data = pd.DataFrame(columns=["Timestamp", "Views", "Likes", "Comments"])  # Reset data
            st.success("Started tracking video")

    # Update and display data while tracking
    if st.session_state.tracking:
        new_data = fetch_video_data(VIDEO_URL)
        if new_data:
            if not st.session_state.data.empty:
                st.session_state.data = pd.concat(
                    [st.session_state.data, pd.DataFrame([new_data])],
                    ignore_index=True
                )
            else:
                st.session_state.data = pd.DataFrame([new_data])  # Avoid concatenating with an empty DataFrame

            # Keep only the last 50 data points for better visualization
            if len(st.session_state.data) > 50:
                st.session_state.data = st.session_state.data.tail(20)

            df = st.session_state.data

            # Calculate the most recent change
            views_change = df["Views"].diff().iloc[-1] if len(df) > 1 else 0
            likes_change = df["Likes"].diff().iloc[-1] if len(df) > 1 else 0
            comments_change = df["Comments"].diff().iloc[-1] if len(df) > 1 else 0

            # Display metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Views", f"{df.iloc[-1]['Views']:,}", f"{views_change:,}")
            col2.metric("Likes", f"{df.iloc[-1]['Likes']:,}", f"{likes_change:,}")
            col3.metric("Comments", f"{df.iloc[-1]['Comments']:,}", f"{comments_change:,}")

            # Display charts in a single row
            col_chart1, col_chart2, col_chart3 = st.columns(3)

            chart_views = create_line_chart(df, "Views", "📊 Views", "blue")
            chart_likes = create_line_chart(df, "Likes", "❤️ Likes", "red")
            chart_comments = create_line_chart(df, "Comments", "💬 Comments", "green")

            if chart_views:
                col_chart1.plotly_chart(chart_views, use_container_width=True)
            if chart_likes:
                col_chart2.plotly_chart(chart_likes, use_container_width=True)
            if chart_comments:
                col_chart3.plotly_chart(chart_comments, use_container_width=True)

            # Auto-update
            time.sleep(update_interval)
            st.rerun()

if __name__ == "__main__":
    main()
