# system packages 
import os
from functools import cache
from typing import Optional, Dict

# internal packages

# external packages 
import pandas as pd
import matplotlib.pyplot as plt

class Visualizer: 
    """A class for visualizing SQL data.
    """
    # TODO: I believe pretty much all of these should just be static methods

    def __init__(self) -> None:
        pass

    def plot_token_length_by_group(
        self, 
        df: pd.DataFrame,
        group_by: str,
        measure_by: str,
        ascending: bool = False,    
        title: Optional[str] = "Average Token Length by Database",
        xlabel: Optional[str] = "Database ID",
        ylabel: Optional[str] = "Average Token Length",   
        cutoff_length=512,
        display_cutoff=True, 
    ): 
        grouped_df = df.groupby(group_by).apply(
            lambda x: x[measure_by].apply(lambda y: len(y.input_ids)).mean()
        )
        sorted_df = grouped_df.sort_values(ascending=ascending)
        
        plt.figure(figsize=(16, 10))
        plt.bar(sorted_df.index, sorted_df.values)
        plt.xticks(rotation=90, fontsize=6) 
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()

        if display_cutoff:
            plt.axhline(y=cutoff_length, color='r', linestyle='--', label='Cutoff Length')
        plt.show()

    def plot_stacked_bar_chart(
            self, 
            df: pd.DataFrame, 
            group_col: str, 
            value_col: str,
            color_dict: Dict[str, str],
            title="",
        ):
        grouped_data = df.groupby(group_col)[value_col].value_counts().unstack(fill_value=0)

        total_counts = grouped_data.sum(axis=1)
        sorted_grouped_data = grouped_data.reindex(total_counts.sort_values(ascending=False).index)

        plt.figure(figsize=(16, 10))
        bottom = [0] * len(sorted_grouped_data)
        for col in sorted_grouped_data.columns:
            color = color_dict.get(col, 'grey')
            plt.bar(sorted_grouped_data.index, sorted_grouped_data[col], bottom=bottom, color=color, label=col)
            bottom = [sum(x) for x in zip(bottom, sorted_grouped_data[col])]

        plt.xlabel(group_col)
        plt.ylabel(f'Count of {value_col}')
        plt.xticks(rotation=90, fontsize=6)
        #plt.title(f'{value_col} Count by {group_col}')
        plt.title(title)
        plt.legend(title=value_col)
        plt.tight_layout()
        plt.show()

    def plot_category_scores(
            self, 
            df: pd.DataFrame,
            categories: Optional[list] = ['easy', 'medium', 'hard', 'extra', 'all'],
        ): 
        ex_scores = [df[f'{cat}_execution_accuracy'].values[0] for cat in categories]
        em_scores = [df[f'{cat}_exact_matching_accuracy'].values[0] for cat in categories]

        x = range(len(categories))
        width = 0.4

        ex_bars = plt.bar([a - width/2 for a in x], ex_scores, width=width, label='EX', color='blue')
        em_bars = plt.bar([a + width/2 for a in x], em_scores, width=width, label='EM', color='orange')

        plt.xlabel('Category')
        plt.ylabel('Score')
        plt.title('Execution and Exact Match Accuracy by Group')
        plt.xticks(x, categories)
        plt.legend()

        for bar in ex_bars + em_bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.01, round(yval, 2), ha='center', va='bottom')
        plt.show()

    # TODO: refactor this to be more dynamic
    def plot_separate_run_type_scores(
            self, 
            df: pd.DataFrame,
            categories: Optional[list] = ['easy', 'medium', 'hard', 'extra', 'all'],
            title_ex: Optional[str] = 'Execution Accuracy by Group for All Run Types',
            title_em: Optional[str] = 'Exact Match Accuracy by Group for All Run Types',
            color_dict: Optional[Dict[str, str]] = None,
        ):
        if color_dict is None:
                    color_dict = {}

        run_types = df['run_type'].unique()
        # colors = ['blue', 'orange', 'green', 'red', 'purple']  # TODO: make this dynamic and/or a dictionary so we have consistent colors
        width = 0.8 / len(run_types)  

        # Plot Execution Accuracy (EX)
        plt.figure(figsize=(12, 6))
        for i, category in enumerate(categories):
            for j, run_type in enumerate(run_types):
                run_df = df[df['run_type'] == run_type]
                ex_score = run_df[f'{category}_execution_accuracy'].values[0]

                bar_x = i - 0.4 + j * width
                color = color_dict.get(run_type, 'grey')
                plt.bar(bar_x, ex_score, width=width, color=color, label=f'{run_type}' if i == 0 else '')
                plt.text(bar_x, ex_score + 0.01, f'{ex_score:.2f}', ha='center', va='bottom')

        plt.xlabel('Category')
        plt.ylabel('Execution Accuracy (EX)')
        plt.title(title_ex)
        plt.xticks(range(len(categories)), categories)
        plt.legend(title='Run Type', loc='center left', bbox_to_anchor=(1, 0.5))
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, zorder=1)
        plt.show()

        # Plot Exact Match Accuracy (EM)
        plt.figure(figsize=(12, 6))
        for i, category in enumerate(categories):
            for j, run_type in enumerate(run_types):
                run_df = df[df['run_type'] == run_type]
                em_score = run_df[f'{category}_exact_matching_accuracy'].values[0]

                bar_x = i - 0.4 + j * width
                color = color_dict.get(run_type, 'grey')
                plt.bar(bar_x, em_score, width=width, color=color, label=f'{run_type}' if i == 0 else '')
                plt.text(bar_x, em_score + 0.01, f'{em_score:.2f}', ha='center', va='bottom')

        plt.xlabel('Category')
        plt.ylabel('Exact Match Accuracy (EM)')
        plt.title(title_em)
        plt.xticks(range(len(categories)), categories)
        plt.legend(title='Run Type', loc='center left', bbox_to_anchor=(1, 0.5))
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, zorder=1)
        plt.show()