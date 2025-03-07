                                    # YouTube Video Statistics Tracker

A. Introduction
This is a real-time YouTube video tracking tool. It displays key video metrics on an interactive dashboard:
        - **Views**
        - **Likes**
        - **Comments**

B. Features
        - Fetch real-time data from YouTube.
        - Display line charts for each metric.
        - Show the latest changes in views, likes, and comments.
        - Allow users to enter a desired YouTube video URL.
        - Enable users to start/stop tracking flexibly.
        - Adjust update intervals (from 5 to 60 seconds).
        - Retain only the 50 most recent data points for optimal visualization.

C. System Requirements
- Operating System: Windows, Linux, macOS
- Python 3.8+

D. Installation
Ensure you have Python installed, then install the required libraries:

```bash
pip install -r requirements.txt
```

E. Usage
        1. Open a terminal or command prompt.
        2. Run the application with:
        ```bash
        streamlit run app.py
        ```
        3. Enter the YouTube video URL in the sidebar.
        4. Click "Start Tracking" to begin monitoring video statistics.
        5. Adjust the update interval as needed.
        6. Click "Stop Tracking" to end the tracking session.

F. Data Visualization
    - The dashboard displays three line charts (Views, Likes, Comments).
    - Data updates at the specified interval (default: 10 seconds).
    - The most recent changes for each metric are displayed next to the values.

## Authors
**Phan Van Tai**  
**Nguyen Thanh Tuan**