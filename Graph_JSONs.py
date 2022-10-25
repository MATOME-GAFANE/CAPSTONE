# Class supplying a list of graph JSON files for each page.
from DB_manager import DB_manager
import plotly.express as px
import plotly
import pandas as pd
import json


class Analysis:
    def __init__(self, DB_name, specializations):
        self.manager = DB_manager(DB_name, specializations)

    def researchers_per_inst_JSON(self):
        researchers_dist = self.manager.researchers_per_inst()
        x_axis = researchers_dist[0]
        y_axis = researchers_dist[1]
        df = pd.DataFrame({
            'Institution': x_axis,
            'Researchers': y_axis,
        })
        fig = px.bar(df, y='Institution', x='Researchers', barmode='group', orientation='h')
        fig.update_layout(title="Researcher distribution by institution", title_x=0.5)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON, x_axis

    def researchers_per_rating_JSON(self, table="Researchers"):
        rating_dist = self.manager.researchers_per_rating(table)
        x_axis = rating_dist[0]
        y_axis = rating_dist[1]
        df = pd.DataFrame({
            'Rating': x_axis,
            table: y_axis,
        })
        fig = px.bar(df, x='Rating', y=table, barmode='group', title="Researcher distribution by rating")
        fig.update_layout(title="Researcher distribution by rating", title_x=0.5)
        fig.update_traces(marker_color='Yellow')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON

    def researcher_rating_by_inst_JSON(self, institution):
        rating_dist = self.manager.researcher_rating_by_inst(institution)
        x_axis = rating_dist[0]
        y_axis = rating_dist[1]
        df = pd.DataFrame({
            'Rating': x_axis,
            'Researchers': y_axis,
        })
        fig = px.bar(df, x='Rating', y='Researchers', barmode='group')
        fig.update_layout(title="Institution Researcher distribution by rating", title_x=0.5)
        fig.update_traces(marker_color='Yellow')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON, y_axis

    def rating_pie_chart_JSON(self):
        rating_dist = self.manager.researchers_per_rating()
        rating_x = rating_dist[0]
        rating_y = rating_dist[1]
        df = pd.DataFrame({
            'Rating': rating_x,
            'Researchers': rating_y
        })
        fig = px.pie(df, values='Researchers', names='Rating', hole=.3)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON

    def get_ratings_list(self):
        rating_dist = self.manager.researchers_per_rating()
        return rating_dist[1]

    def researchers_per_specializations_JSON(self):
        distribution = self.manager.researchers_per_specialization()
        x_axis = distribution[0]
        y_axis = distribution[1]
        df = pd.DataFrame({
            'Specialization': x_axis,
            'Number of researchers': y_axis,
        })
        df.sort_values("Number of researchers", ascending=False, inplace=True)
        fig = px.bar(df, x='Specialization', y='Number of researchers', barmode='group')
        fig.update_layout(title="Researcher distribution by Specializations (AI only)", title_x=0.5)
        fig.update_traces(marker_color='Green')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON

    def researchers_per_topic_JSON(self, topic):
        rating, frequency = self.manager.researcher_dist_by_specialization(topic)
        df = pd.DataFrame({
            'Rating': rating,
            'Number of researchers': frequency,
        })
        fig = px.bar(df, x='Rating', y='Number of researchers', barmode='group')
        fig.update_layout(title="Researcher Rating distribution by Specialization: " + topic, title_x=0.5)
        fig.update_traces(marker_color='Purple')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON

    def primary_research_top_inst_JSON(self, primary):
        frequency = self.manager.primary_research_dist_by_top_inst(primary)
        df = pd.DataFrame({
            'Primary Research': primary,
            'Number of researchers': frequency,
        })
        df.sort_values("Number of researchers", ascending=False, inplace=True)
        fig = px.bar(df, y='Number of researchers', x='Primary Research', barmode='group', orientation='v')
        fig.update_layout(title="Researcher distribution by primary research", title_x=0.5)
        fig.update_traces(marker_color='cornflowerblue')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON

    def top_5_researchers_distribution_JSON(self):
        x_axis, y_axis = self.manager.pie_chart_top_5_vs_rest()
        df = pd.DataFrame({
            'Affiliation': x_axis,
            'Researchers': y_axis
        })
        fig = px.pie(df, values='Researchers', names='Affiliation')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON
