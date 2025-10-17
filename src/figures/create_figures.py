import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.patches import Rectangle


def update_figures():
    """
    This method reads the current player results and calls
    the methods to update both the tricks and wins figures,
    located in the figures folder
    """
    df = pd.read_csv("src/scoring/player_wins.csv", dtype={"p1": str, "p2": str})
    update_tricks_figure(df)
    update_cards_figure(df)

def update_tricks_figure(df):
    """
    This method calculates win percentages for each combination based on tricks.
    It then creates a heat map based on those numbers and saves it to the Figures folder.
    """
    df = df
    # Compute
    df["total_tricks"] = df["p1_wins_tricks"] + df["p2_wins_tricks"] + df["draws_tricks"] # total tricks per matchup
    df["p1_win_rate_tricks"] = df["p1_wins_tricks"] / df["total_tricks"] # P1 win rate for tricks
    df["draws_rate_tricks"] = df["draws_tricks"] / df["total_tricks"] # P1 win rate for tricks

    # Create a label for each cell: "WinRate% (Draws)"
    df["label"] = (df["p1_win_rate_tricks"] * 100).round(0).astype(int).astype(str) + \
                "(" + (df["draws_rate_tricks"]*100).round(0).astype(int).astype(str) + ")"

    # Turn 001 labels into BBR
    df["p1"] = df["p1"].str.replace("0", "B").str.replace("1", "R")
    df["p2"] = df["p2"].str.replace("0", "B").str.replace("1", "R")

    # Pivot tables for heatmap values and annotations
    heatmap_values = df.pivot(index="p2", columns="p1", values="p1_win_rate_tricks")
    heatmap_labels = df.pivot(index="p2", columns="p1", values="label")

    # Plot the heatmap
    plt.figure(figsize=(6, 5))
    ax = sns.heatmap(
        heatmap_values,
        cmap="coolwarm",
        annot=heatmap_labels,
        fmt="",
        annot_kws={"size": 8},
        cbar=False  # or True if you want the colorbar
    )

    plt.title(f"My Chance of Win(Draw)\nBy Tricks\nN = {(df['total_tricks'][0]):,}", fontsize=12, pad=12)
    plt.xlabel("My Choice")
    plt.ylabel("Opponent Choice")
    plt.yticks(rotation=0)  # make y-axis labels horizontal

    # Add a black rectangle around the highest value in each row
    for y_index, row_label in enumerate(heatmap_values.index):
        row = heatmap_values.loc[row_label]
        max_col_label = row.idxmax()  # column with max value
        x_index = heatmap_values.columns.get_loc(max_col_label)  # column index

        # Draw rectangle at (x_index, y_index)
        rect = Rectangle((x_index, y_index), 1, 1, fill=False, edgecolor='black', linewidth=2)
        ax.add_patch(rect)

    plt.tight_layout()
    plt.savefig("Figures/tricks_heatmap.png", dpi=200, bbox_inches="tight") # save heatmap as png

def update_cards_figure(df):
    """
    This method calculates win percentages for each combination based on cards.
    It then creates a heat map based on those numbers and saves it to the Figures folder.
    """
    
    df = df
    df["total_cards"] = df["p1_wins_cards"] + df["p2_wins_cards"] + df["draws_cards"] # total tricks per matchup
    df["p1_win_rate_cards"] = df["p1_wins_cards"] / df["total_cards"] # P1 win rate for tricks
    df["draws_rate_cards"] = df["draws_cards"] / df["total_cards"] # P1 win rate for tricks

    # Create a label for each cell: "WinRate% (Draws)"
    df["label"] = (df["p1_win_rate_cards"] * 100).round(0).astype(int).astype(str) + \
                "(" + (df["draws_rate_cards"]*100).round(0).astype(int).astype(str) + ")"

    # Turn 001 labels into BBR
    df["p1"] = df["p1"].str.replace("0", "B").str.replace("1", "R")
    df["p2"] = df["p2"].str.replace("0", "B").str.replace("1", "R")

    # Pivot tables for heatmap values and annotations
    heatmap_values = df.pivot(index="p2", columns="p1", values="p1_win_rate_cards")
    heatmap_labels = df.pivot(index="p2", columns="p1", values="label")

    # Plot the heatmap
    plt.figure(figsize=(6, 5))
    ax = sns.heatmap(
        heatmap_values,
        cmap="coolwarm",
        annot=heatmap_labels,
        fmt="",
        annot_kws={"size": 8},
        cbar=False  # or True if you want the colorbar
    )

    plt.title(f"My Chance of Win(Draw)\nBy Cards\nN = {(df['total_tricks'][0]):,}", fontsize=12, pad=12)
    plt.xlabel("My Choice")
    plt.ylabel("Opponent Choice")
    plt.yticks(rotation=0)  # make y-axis labels horizontal

    # Add a black rectangle around the highest value in each row
    for y_index, row_label in enumerate(heatmap_values.index):
        row = heatmap_values.loc[row_label]
        max_col_label = row.idxmax()  # column with max value
        x_index = heatmap_values.columns.get_loc(max_col_label)  # column index

        # Draw rectangle at (x_index, y_index)
        rect = Rectangle((x_index, y_index), 1, 1, fill=False, edgecolor='black', linewidth=2)
        ax.add_patch(rect)

    plt.tight_layout()
    plt.savefig("Figures/cards_heatmap.png", dpi=200, bbox_inches="tight") # save heatmap as png

