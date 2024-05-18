from __future__ import annotations # without list[pd.Series[Any]] get error
from typing import Any
from dataclasses import dataclass
import matplotlib.pyplot as plt
import pandas as pd
import emoji
from collections import Counter
import string
import re


plt.style.use('seaborn-v0_8-pastel')

@dataclass
class MakeStats():
    
    def types_sentiments_number_by(self, df: pd.DataFrame) -> tuple[pd.Series[int], pd.Series[int]]:
        """Function count number of likes and sentiments

        Args:
            df (pd.DataFrame): data frame with data from yt video

        Returns:
            tuple[pd.Series[int], pd.Series[int]]: list of df of likes and sentiments
        """
        
        likes = df["type"].value_counts()
        likes.index = [str(val).capitalize() for val in likes.index] # type: ignore
        
        sentiments = df["sentiment"].value_counts()
        sentiments.index = [str(val).capitalize() for val in sentiments.index] # type: ignore
        
        return likes, sentiments
    
    
    def length_of_text_by(self, df: pd.DataFrame) -> tuple[pd.Series[Any], pd.Series[Any], pd.Series[Any]]:
        """Function to sum text size by type and sentiments

        Args:
            df (pd.DataFrame): data frame with data from yt video

        Returns:
            tuple[pd.Series[Any], pd.Series[Any], pd.Series[Any]]: values from groupby operation
        """
        
        df_copy = df.copy()
        
        df_copy["text_size"] = df_copy["text"].str.len()
        
        types_sum = df_copy.groupby("type")["text_size"].sum()
        types_sum.index = [str(val).capitalize() for val in types_sum.index] # type: ignore
        
        sentiments_sum = df_copy.groupby("sentiment")["text_size"].sum()
        sentiments_sum.index = [str(val).capitalize() for val in sentiments_sum.index] # type: ignore
        
        return types_sum, sentiments_sum,  df_copy["text_size"]
    
    
    def letter_count(self, df: pd.DataFrame) -> pd.Series[int]:
        """Function count letters in all comments and return top 10

        Args:
            df (pd.DataFrame): data frame with data from yt video

        Returns:
            pd.Series[int]: counted letters from comments
        """
                
        join_comments = " ".join(df["text"].to_list()).lower()
        join_comments = re.sub(r"\s+", "", join_comments)
        
        symbols_counted = pd.Series(list(join_comments)) \
                                                .value_counts() \
                                                .sort_values(ascending=False)[:10]
        
        return symbols_counted
    
    
    def number_of_emojis(self, df: pd.DataFrame) -> tuple[int, int, pd.Series[int]]:
        """Function count number of each emojii, sum and unique

        Args:
            df (pd.DataFrame): data frame with data from yt video
            
        Returns:
            tuple[int, int, pd.Series[int]]: list of diferent number of emojis stats
        """

        join_comments = " ".join(df["text"].to_list())
        
        # Get number of all emojis and unique
        all_emojis = emoji.emoji_count(join_comments)
        unique_emojis = emoji.emoji_count(join_comments, unique=True)
        
        # Counted emojis
        emojis_list = []
        for symbol in emoji.emoji_list(join_comments):
            emojis_list.append(symbol["emoji"])
        
        return all_emojis, unique_emojis, pd.Series(emojis_list).value_counts()


    def emojis_in_text(self, df: pd.DataFrame) -> pd.DataFrame:
        """Function to check if emoji and number of emoji in text

        Args:
            df (pd.DataFrame): data frame with data from yt video

        Returns:
            pd.DataFrame: new df with aditional two columns
        """
        
        df_copy = df.copy()
        
        df_copy["emoji_number"] = df_copy["text"].map(lambda x: emoji.emoji_count(x))
        df_copy["is_emoji"] = df_copy["text"].map(lambda x: 1 if emoji.emoji_count(x) > 0 else 0)   
        
        return df_copy
    
    
    def number_of_characters(self, df: pd.DataFrame) -> tuple[int, int, pd.Series[int]]:
        """Function count number of each special character, sum and unique

        Args:
            df (pd.DataFrame): data frame with data from yt video

        Returns:
            tuple[int, int, pd.Series[int]]: return unique, sum and pd.Series data
        """

        join_comments = " ".join(df["text"].to_list())
               
        char_count = {char : count
                                        for char, count in Counter(join_comments).items() 
                                            if char in string.punctuation}
        s_char_count = pd.Series(char_count)
        
        return sum(s_char_count), len(s_char_count.index), s_char_count
    
    
    def sum_of_replies_by(self, df: pd.DataFrame) -> tuple[pd.Series[Any], pd.Series[Any]]:
        """Function get sum from groupby replies by type and sentiment

        Args:
            df (pd.DataFrame): data frame with data from yt video

        Returns:
            tuple[pd.Series[Any], pd.Series[Any]]: values from groupby operation
        """
        
        type_replies_sum = df.groupby("type")["replies"].sum()
        type_replies_sum.index = [str(val).capitalize() for val in type_replies_sum.index] # type: ignore
        
        sentiment_replies_sum = df.groupby("sentiment")["replies"].sum()
        sentiment_replies_sum.index = [str(val).capitalize() for val in sentiment_replies_sum.index] # type: ignore
    
        return type_replies_sum, sentiment_replies_sum
      
       
    def top_3(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Funtion for getting top 3 of comment by likes, replies and number of emojis

        Args:
            df (pd.DataFrame): df with emojis, returned by other function

        Returns:
            tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: tuple of results
        """
        
        df_copy = df.copy()
        df_copy.columns = [str(val).capitalize() for val in df_copy.columns] # type: ignore
        
        comment_by_likes = df_copy.sort_values(by="Likes", ascending=False).drop("Index", axis=1)[:3]
        comment_by_replies = df_copy.sort_values(by="Replies", ascending=False).drop("Index", axis=1)[:3]
        comment_by_emojis = df_copy.sort_values(by="Emoji_number", ascending=False).drop("Index", axis=1)[:3]
        
        return comment_by_likes, comment_by_replies, comment_by_emojis
        
    
    def plot_bars(self, df: pd.Series | pd.DataFrame,
                    xlabel: str, ylabel: str, 
                    title: str, direction: str = "v") -> plt.Figure: # type: ignore
        """Function to plot bar

        Args:
            df (pd.Series | pd.DataFrame): data to plot
            xlabel (str): name of xlabel
            ylabel (str): name of ylabel
            title (str): title of chart
            direction (str, optional): chart type vertical or horizontal - v or h. Defaults to "v".

        Returns:
            plt.Figure: figure of chart
        """

        fig, ax = plt.subplots()
        fig.tight_layout()
        
        if direction == "v":
            df.plot.bar(ax=ax)
            
        elif direction == "h":
            df.plot.barh(ax=ax)

        ax.grid(True, alpha=0.25)
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel, labelpad=10)
        
        return fig
    