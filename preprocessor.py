import pandas as pd
from loadData import loadDataFromS3


class Preprocessor:

    def process_count(self, df_review, df_listing):
        df1 = df_review.drop(['reviewer_id', 'reviewer_name', 'comments'], axis=1)
        df2 = df_listing[['id', 'neighbourhood_group_cleansed']]
        df3 = pd.merge(df2, df1, left_on='id', right_on='listing_id')
        df3 = df3[['date', 'listing_id', 'neighbourhood_group_cleansed']]
        df3.date = pd.to_datetime(df3.date, format="%Y-%m-%d")
        df3 = df3[df3['date'].isin(pd.date_range("2019-07-10", "2021-04-10"))]
        df3 = df3.set_index(df3.date).drop('date', axis=1)
        #df3.to_pickle("ts.pkl")
        return df3

    def process_location_count(self, df_review, df_listing):
        # process data for timestamped folium map
        df2 = df_review.groupby(['listing_id', 'date'])['id'].count().rename('review_count').reset_index()
        df2['date'] = pd.to_datetime(df2['date'])
        df2 = df2[df2['date'].isin(pd.date_range("2019-07-10", "2021-04-10"))]
        df2 = df2.groupby(['listing_id', pd.Grouper(key='date', freq='M')])['review_count'] \
            .sum().reset_index()

        merged = pd.merge(df_listing, df2, left_on='id', right_on='listing_id')
        #merged.to_pickle("timestamped_review.pkl")
        return merged
