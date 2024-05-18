import googleapiclient.discovery
import time
import pandas as pd


class API:
    def __init__(self, api_key: str, limit: int = 500) -> None:
        """Init key and limit

        Args:
            api_key (str): Key to Google Api
            limit (int, optional): Maximum number of comments. Defaults to 500.
        """
        
        self.api_key = api_key
        self.limit = limit

        self._create_api()


    def _create_api(self) -> None:
        """
        Function create handle to GoogleApi
        """
        
        self.api = googleapiclient.discovery.build(
            "youtube", 
            "v3", 
            developerKey=self.api_key
        )


    def _format_data(self, responses: dict) -> pd.DataFrame:
        """Function formating data returned from api in json format to pandas DataFrame

        Args:
            responses (dict): Dict with data from api responses

        Returns:
            pd.DataFrame: data in pandas DataFrame format
        """

        results = {}
        df_data = pd.DataFrame({"text": [], "likes": [], "replies": []})

        for response in responses["items"]:
            results["text"] = response["snippet"]["topLevelComment"]["snippet"]["textDisplay"].replace("\n", " ").replace(r"/\s\s+/g", " ")
            results["likes"] = response["snippet"]["topLevelComment"]["snippet"]["likeCount"]
            results["replies"] = response["snippet"]["totalReplyCount"]

            # Taking comments with more than 5 words and less than 514 chars
            if 5 <= len(results["text"].split()) and len(results["text"]) <= 514:
                df_data = pd.concat([df_data, pd.DataFrame([results])], axis=0)

        return df_data


    def get_comments(self, short_link: str) -> pd.DataFrame:
        """Function gets data from a video specified by a short link 
           Short link is the part of url after 'watch'

        Args:
            short_link (str): the part of url after 'watch'

        Returns:
            pd.DataFrame: data in pandas DataFrame format
        """

        df_data = pd.DataFrame({"text": [], "likes": [], "replies": []})
        request = self.api.commentThreads().list(
            part="snippet",
            maxResults=100,
            order="relevance",
            textFormat="plainText",
            videoId=short_link
        )
        response = request.execute()
        df_data = pd.concat([df_data, self._format_data(response)], axis=0)

        # while loop until all the data is collected
        while len(df_data) < self.limit:
            try:
                response["nextPageToken"]
            except Exception:
                break

            time.sleep(0.25)
            request = self.api.commentThreads().list(
                part="snippet",
                maxResults=100,
                order="relevance",
                textFormat="plainText",
                videoId=short_link,
                pageToken=response["nextPageToken"]
            )
            response = request.execute()
            df_data = pd.concat([df_data, self._format_data(response)], axis=0)

        return df_data 