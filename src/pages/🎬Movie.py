import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.grid import grid
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import shapiro, kurtosis, skew
from api import API
from model import Sentimets
from make_stats import MakeStats
from googleapiclient.errors import HttpError
import emoji


st.set_page_config(
    page_title = "YT-Sentiments",
    page_icon = "🎬",
    layout="wide"
)

# Objecy of stats on df
stats = MakeStats()

# Side bar for API key loading
with st.sidebar:
    key_input = st.text_input("YT-API", placeholder="Key...")       
    st.write("")
    
# Title of page
st.subheader("YT-Sentiments Stats 🎬", divider="blue")

if key_input == "":
    st.error("No Key Insert")
        
else:   
    url_input = st.text_input("URL", placeholder="URL for YT video...")
    url_btn = st.button("Search")
    
    if url_btn:
        api = API(key_input, 500)
        
        try:
            short_url = url_input.split("=")[1].split("&")[0]
            comments = api.get_comments(short_url)  
        
        except HttpError as e:
            st.error(f"Error {emoji.emojize(':right_arrow:')} check URL or API key") 
            st.stop()
            
        except Exception as e:
            st.error(f"Error {emoji.emojize(':right_arrow:')} check URL or API key")
            st.stop()
            
            
        with st.spinner("Generating..."):          
            model = Sentimets()
            result_type, result_sentiment = model.predict(list(comments["text"]))

            comments["type"] = result_type
            comments["sentiment"] = result_sentiment
            comments = comments.sort_values(by="likes", ascending=False).reset_index()
            
            # ----------------- #
             
            add_vertical_space(3)    
            st.subheader("Types and sentiments of comments 🎭", divider="blue")    
                
            # Types and sentiments counted
            by_types, by_sentiments = stats.types_sentiments_number_by(comments)     
            
            by_types_sentiments_grid = grid(2, 2, vertical_align="center")
            
            by_types_sentiments_grid.pyplot(
                    stats.plot_bars(by_types.sort_values(ascending=True),
                                    "Number of types", "Type", 
                                    "Number of each type", "h")
                )
                
            by_types_sentiments_grid.pyplot(
                    stats.plot_bars(by_sentiments.sort_values(ascending=True),
                                    "Number of sentiments", "Sentiment", 
                                    "Number of each sentiment", "h")
                )
            
            # ----------------- #
            
            add_vertical_space(3)    
            st.subheader("Sum of text length by types and sentiments 📃", divider="blue")
            
            # Get sum of text length by types and sentiments and pd.Series with len of each comment
            types_sum, sentiments_sum, s_text_size = stats.length_of_text_by(comments)
            types_sentiments_sum_grid = grid(2, 2, 2, vertical_align="bottom")
        
            
            types_sentiments_sum_grid.pyplot(
                    stats.plot_bars(types_sum.sort_values(ascending=True),
                                    "Sum of text size", "Type", 
                                    "Sum of text size by type", "h")
                )
            
            types_sentiments_sum_grid.pyplot(
                    stats.plot_bars(sentiments_sum.sort_values(ascending=True),
                                    "Sum of text size", "Sentiment", 
                                    "Sum of text size by sentiment", "h")
                )
                
            add_vertical_space(1)
                
            types_sentiments_sum_grid.data_editor(pd.DataFrame(types_sum.sort_values(ascending=False)).T, 
                                                    use_container_width=True, 
                                                    hide_index=True, disabled=True)
                                          
            types_sentiments_sum_grid.data_editor(pd.DataFrame(sentiments_sum.sort_values(ascending=False)).T, 
                                                    use_container_width=True, 
                                                    hide_index=True, disabled=True)
            
            add_vertical_space(2)
                                    
            fig_text, ax_text = plt.subplots(figsize=(12,5))
            
            ax_text.hist(s_text_size, bins=20, label="Value")
            ax_text.axvline(s_text_size.mean(),   color="red",  linestyle="--", label="Mean")
            ax_text.axvline(s_text_size.median(), color="cyan", linestyle="--", label="Median")
            ax_text.set_title("Histogram of text size")
            ax_text.grid(True, alpha=.25)
            ax_text.legend(loc="upper right")
            
            fig_text.tight_layout()
            st.pyplot(fig_text)       
            
            add_vertical_space(1)
            
            _, column_stast, _ = st.columns(3)

            with column_stast:
                st.data_editor(pd.DataFrame({"Shapiro"  : [shapiro(s_text_size).pvalue],
                                             "Kurtosis" : [kurtosis(s_text_size)],
                                             "Skewness" : [skew(s_text_size)]}), 
                                use_container_width=True, 
                                hide_index=True, disabled=True)
            
            # ----------------- #
            
            add_vertical_space(3)
            st.subheader("Statistics of emojis 🥳", divider="blue")
            
            # Diferent stats of emojis like all, unique and counted
            all_emojis, unique_emojis, number_emojis = stats.number_of_emojis(comments)
            
            st.data_editor(pd.DataFrame(number_emojis).T, 
                           use_container_width=True, 
                           hide_index=True, disabled=True)
            
            _, emojis_mid, _ = st.columns(3)
                        
            with emojis_mid:
                st.data_editor(pd.DataFrame({"All" :    [all_emojis],
                                             "Unique" : [unique_emojis]}), 
                               use_container_width=True, 
                               hide_index=True, disabled=True)
            
            # ----------------- #
              
            add_vertical_space(3)
            st.subheader("Statistics of special characters #️⃣", divider="blue")
            
            # Diferent stats of chars like all, unique and counted
            all_chars, unique_chars, number_chars = stats.number_of_characters(comments)
            
            st.data_editor(pd.DataFrame(number_chars).T, 
                           use_container_width=True, 
                           hide_index=True, disabled=True)
            
            _, chars_mid, _ = st.columns(3)
                        
            with chars_mid:
                st.data_editor(pd.DataFrame({"All" :    [all_chars],
                                             "Unique" : [unique_chars]}), 
                               use_container_width=True, 
                               hide_index=True, disabled=True)
            
            # ----------------- #
            
            add_vertical_space(3)
            st.subheader("Sum of replies by... ➕", divider="blue")
            
            # Get sum of replies by type and sentiment
            type_replies_sum, sentiment_replies_sum = stats.sum_of_replies_by(comments)
            
            replies_sum_grid = grid(2, 2, vertical_align="bottom")
            
            replies_sum_grid.pyplot(
                    stats.plot_bars(type_replies_sum.sort_values(ascending=True),
                                    "Number of replies", "Type", 
                                    "Number of replies for each type", "h")
                )
                
            replies_sum_grid.pyplot(
                    stats.plot_bars(sentiment_replies_sum.sort_values(ascending=True),
                                    "Number of replies", "Sentiment", 
                                    "Number of replies for each sentiment", "h")
                )
            
            add_vertical_space(1)
                
            replies_sum_grid.data_editor(pd.DataFrame(type_replies_sum.sort_values(ascending=False)).T, 
                                            use_container_width=True, 
                                            hide_index=True, disabled=True)
                                          
            replies_sum_grid.data_editor(pd.DataFrame(sentiment_replies_sum.sort_values(ascending=False)).T, 
                                            use_container_width=True, 
                                            hide_index=True, disabled=True)

            # ----------------- #
            
            add_vertical_space(3)
            st.subheader("Top 3 comments by... 💬", divider="blue")
            
            df_emojis = stats.emojis_in_text(comments)
            comment_by_likes, comment_by_replies, comment_by_emojis = stats.top_3(df_emojis)
            
            st.data_editor(comment_by_likes,
                            use_container_width=True, 
                            hide_index=True, disabled=True)
                                   
            add_vertical_space(1)
                                          
            st.data_editor(comment_by_replies, 
                            use_container_width=True, 
                            hide_index=True, disabled=True)
            
            add_vertical_space(1)
                                                      
            st.data_editor(comment_by_emojis, 
                            use_container_width=True, 
                            hide_index=True, disabled=True)