def generate_location_points(all_points):
    # two_year_review = pd.read_pickle("ts.pkl")
    # all_points = pd.read_pickle("timestamped_review.pkl")
    # loc_points = all_points[all_points.neighbourhood_group_cleansed == location]
    loc_points = all_points.drop(['neighbourhood_group_cleansed', 'listing_id'], axis=1)
    loc_points = loc_points.groupby('date').agg(lambda x: list(x))

    to_draw = []
    for i in range(loc_points.shape[0]):
        single_draw = []
        for j in list(zip(loc_points.iloc[i].latitude, loc_points.iloc[i].longitude, loc_points.iloc[i].review_count)):
            single_draw.append(list(j))
        to_draw.append(single_draw)

    time_index = []
    for t in loc_points.index:
        time_index.append(t.strftime("%Y-%m-%d"))

    return to_draw, time_index
