import streamlit as st
import pandas as pd
from datetime import datetime
import base64

# Load the CSV file
data = pd.read_csv('trending_news_.csv')

# Convert created_at to datetime format, trying first with seconds, then without
data['created_at'] = pd.to_datetime(data['created_at'], format='%d-%m-%Y %H:%M:%S', errors='coerce')
data['created_at'] = data['created_at'].fillna(pd.to_datetime(data['created_at'], format='%d-%m-%Y %H:%M', errors='coerce'))

# Handle NaT values in the created_at column
data['created_at'] = data['created_at'].apply(lambda x: x.strftime('%B %d, %Y') if pd.notnull(x) else "Date not available")

# Define a mapping of subcategories to main categories
category_mapping = {
    'cricket': 'Sports',
    'OLYMPICS_2024': 'Sports',
    'sports': 'Sports',
    'Russia-Ukraine_Conflict': 'World',
    'world': 'World',
    'technology': 'Science & Technology',
    'science': 'Science & Technology',
    'politics': 'National & Politics',
    'national': 'National & Politics',
    # Keep the rest as they are
    'EXPLAINERS': 'EXPLAINERS',
    'FINANCE': 'FINANCE',
    'Feel_Good_Stories': 'Feel_Good_Stories',
    'Health___Fitness': 'Health & Fitness',
    'Lifestyle': 'Lifestyle',
    'automobile': 'Automobile',
    'business': 'Business',
    'crime': 'Crime',
    'entertainment': 'Entertainment',
    'experiment': 'Experiment',
    'facts': 'Facts',
    'hatke': 'Hatke',
    'miscellaneous': 'Miscellaneous',
    'startup': 'Startup',
    'travel': 'Travel',
}

# Function to map subcategories to main categories
def map_category(category_names):
    mapped_categories = set()
    for category in category_names.split(','):
        category = category.strip()
        # Map subcategories to their broader main category
        mapped_category = category_mapping.get(category, category)  # Default to original if no mapping
        mapped_categories.add(mapped_category)
    return ', '.join(sorted(mapped_categories))

# Apply the mapping to the category_names column
data['mapped_category_names'] = data['category_names'].apply(map_category)

# Extract unique individual categories from the mapped_category_names column
categories_list = sorted(set(category_mapping.values()))

def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def show_home_page():
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
            <img src="data:image/png;base64,{}" style="width: 100px; height: auto; margin-right: 15px;">
            <h1 style="color: #0000FF; font-size: 36px; margin: 0;">GANIT NEWSPAPER</h1>
        </div>
        """.format(get_image_base64('Ganitlogo.png')), unsafe_allow_html=True)

    st.markdown(f"<h4 style='text-align: center; color: #0000FF;'>Today's Date: {datetime.now().strftime('%B %d, %Y')}</h4>", unsafe_allow_html=True)
    
    # Blue strip with app download message (matching the logo color)
    st.markdown(
        """
        <div style="background-color: #0000FF; color: white; padding: 10px; text-align: center; margin-bottom: 20px;">
            For the best experience, download the app
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Create three columns
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        for row in data.iloc[:2].itertuples():  # First 2 news items
            st.markdown(
                f"""
                <div style="border: 2px solid #0000FF; border-radius: 10px; padding: 10px; margin-bottom: 20px;">
                    <h4 style="color: #0000FF;">{row.title}</h4>
                    <p style="font-size: 12px;">{row.content}</p>
                    <p style="font-size: 10px; color: grey;">By {row.author_name}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )

    with col2:
        selected_item = st.selectbox("Choose a category:", categories_list)
        if st.button("Submit"):
            st.session_state.selected_item = selected_item
            st.session_state.page = 'next_page'
        
        # Display the 3rd news item in the center column
        if len(data) > 2:
            st.markdown(
                f"""
                <div style="border: 2px solid #0000FF; border-radius: 10px; padding: 10px; margin-bottom: 20px;">
                    <h4 style="color: #0000FF;">{data.iloc[2].title}</h4>
                    <img src="{data.iloc[2].image_url}" style="width: 100%; height: auto; border-radius: 10px;"/>
                    <p style="font-size: 12px;">{data.iloc[2].content}</p>
                    <p style="font-size: 10px; color: grey;">By {data.iloc[2].author_name}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )

        # Display the 6th news item directly below the 3rd news item
        if len(data) > 5:
            st.markdown(
                f"""
                <div style="border: 2px solid #0000FF; border-radius: 10px; padding: 10px; margin-top: 20px;">
                    <h4 style="color: #0000FF;">{data.iloc[5].title}</h4>
                    <img src="{data.iloc[5].image_url}" style="width: 100%; height: auto; border-radius: 10px;"/>
                    <p style="font-size: 12px;">{data.iloc[5].content}</p>
                    <p style="font-size: 10px; color: grey;">By {data.iloc[5].author_name}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )

    with col3:
        for row in data.iloc[3:5].itertuples():  # Remaining news items
            st.markdown(
                f"""
                <div style="border: 2px solid #0000FF; border-radius: 10px; padding: 10px; margin-bottom: 20px;">
                    <h4 style="color: #0000FF;">{row.title}</h4>
                    <p style="font-size: 12px;">{row.content}</p>
                    <p style="font-size: 10px; color: grey;">By {row.author_name}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )

def show_next_page():
    st.title("Next Page")
    st.write(f"You selected: {st.session_state.selected_item}")

    # Filter the data based on the mapped categories
    selected_rows = data[data['mapped_category_names'].apply(
        lambda x: st.session_state.selected_item in x)
    ]

    # Display each row's content with title, image, content, and author name
    for _, row in selected_rows.iterrows():
        st.markdown(
            f"""
            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
                <img src="{row['image_url']}" style="width: 100%; height: auto; border-radius: 10px;"/>
                <h2 style="margin-top: 20px; color: #0000FF;">{row['title']}</h2>
                <p>{row['content']}</p>
                <p style="font-size: 10px; color: grey;">By {row['author_name']}</p>
                <p><a href="{row['source_url']}" target="_blank" style="color: #0066cc;">Read more</a></p>
            </div>
            """, 
            unsafe_allow_html=True
        )

    if st.button("Back to Home"):
        st.session_state.page = 'home'


# Initialize session state if it does not exist
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Render the appropriate page based on session state
if st.session_state.page == 'home':
    show_home_page()
elif st.session_state.page == 'next_page':
    show_next_page()
