import matplotlib.pyplot as plt
import pandas as pd

def plot_comparison_set_counts(dataset_1, dataset_2, title, legend_1, legend_2, output_file):
    dataset_1_local = pd.read_csv(f"{dataset_1}_subpop_set_counts.csv", index_col=0)
    dataset_2_local = pd.read_csv(f"{dataset_2}_subpop_set_counts.csv", index_col=0)
    dataset_1_global = pd.read_csv(f"{dataset_1}_metapop_set_counts.csv", index_col=0)
    dataset_2_global = pd.read_csv(f"{dataset_2}_metapop_set_counts.csv", index_col=0)

    plt.plot(dataset_1_local.mean(axis=1), color = 'xkcd:sky blue')
    plt.plot(dataset_1_global.mean(axis=1), color = 'xkcd:blue')
    plt.plot(dataset_2_local.mean(axis=1), color = 'tan')
    plt.plot(dataset_2_global.mean(axis=1), color = 'xkcd:puce')

    plt.fill_between(dataset_1_local.index, dataset_1_local.mean(axis=1) - dataset_1_local.std(axis=1), dataset_1_local.mean(axis=1) + dataset_1_local.std(axis=1), color='xkcd:sky blue', alpha=0.3)
    plt.fill_between(dataset_2_local.index, dataset_2_local.mean(axis=1) - dataset_2_local.std(axis=1), dataset_2_local.mean(axis=1) + dataset_2_local.std(axis=1), color='tan', alpha=0.3)
    plt.fill_between(dataset_1_global.index, dataset_1_global.mean(axis=1) - dataset_1_global.std(axis=1), dataset_1_global.mean(axis=1) + dataset_1_global.std(axis=1), color='xkcd:blue', alpha=0.3)
    plt.fill_between(dataset_2_global.index, dataset_2_global.mean(axis=1) - dataset_2_global.std(axis=1), dataset_2_global.mean(axis=1) + dataset_2_global.std(axis=1), color='xkcd:puce', alpha=0.3)

    plt.axvline(500, color="black", linestyle='--', ymax=1)

    plt.legend([f"{legend_1} subpop avg", f"{legend_1} whole metapop", f"{legend_2} subpop avg", f"{legend_2} whole metapop"])
    plt.ylabel("Number of feature sets")
    plt.xlabel("Generations (x100)")
    plt.grid(linestyle=':', linewidth=0.5)
    plt.title(title)

    plt.savefig(output_file)


def plot_comparison_gini(dataset_1, dataset_2, title, legend_1, legend_2, output_file):
    dataset_1_local = pd.read_csv(f"{dataset_1}_subpop_gini.csv", index_col=0)
    dataset_2_local = pd.read_csv(f"{dataset_2}_subpop_gini.csv", index_col=0)
    dataset_1_global = pd.read_csv(f"{dataset_1}_metapop_gini.csv", index_col=0)
    dataset_2_global = pd.read_csv(f"{dataset_2}_metapop_gini.csv", index_col=0)

    plt.plot(dataset_1_local.mean(axis=1), color = 'xkcd:sky blue')
    plt.plot(dataset_1_global.mean(axis=1), color = 'xkcd:blue')
    plt.plot(dataset_2_local.mean(axis=1), color = 'tan')
    plt.plot(dataset_2_global.mean(axis=1), color = 'xkcd:puce')

    plt.fill_between(dataset_1_local.index, dataset_1_local.mean(axis=1) - dataset_1_local.std(axis=1), dataset_1_local.mean(axis=1) + dataset_1_local.std(axis=1), color='xkcd:sky blue', alpha=0.3)
    plt.fill_between(dataset_2_local.index, dataset_2_local.mean(axis=1) - dataset_2_local.std(axis=1), dataset_2_local.mean(axis=1) + dataset_2_local.std(axis=1), color='tan', alpha=0.3)
    plt.fill_between(dataset_1_global.index, dataset_1_global.mean(axis=1) - dataset_1_global.std(axis=1), dataset_1_global.mean(axis=1) + dataset_1_global.std(axis=1), color='xkcd:blue', alpha=0.3)
    plt.fill_between(dataset_2_global.index, dataset_2_global.mean(axis=1) - dataset_2_global.std(axis=1), dataset_2_global.mean(axis=1) + dataset_2_global.std(axis=1), color='xkcd:puce', alpha=0.3)

    plt.axvline(500, color="black", linestyle='--', ymax=1)

    plt.legend([f"{legend_1} subpop avg", f"{legend_1} whole metapop", f"{legend_2} subpop avg", f"{legend_2} whole metapop"])
    plt.ylabel("Number of feature sets")
    plt.xlabel("Generations (x100)")
    plt.grid(linestyle=':', linewidth=0.5)
    plt.title(title)

    plt.savefig(output_file)


def metapopulation_plot_comparison(dataset_1, dataset_2, title, legend_1, legend_2, output_file, what_measure, dataset_3 = None, legend_3 = None):
    if what_measure == 'set_counts':
        dataset_1_global = pd.read_csv(f"{dataset_1}_metapop_set_counts.csv", index_col=0)
        dataset_2_global = pd.read_csv(f"{dataset_2}_metapop_set_counts.csv", index_col=0)
    elif what_measure == 'shannon':
        dataset_1_global == pd.read_csv(f"{dataset_1}_metapop_shannon.csv", index_col=0)
        dataset_2_global = pd.read_csv(f"{dataset_2}_metapop_shannon.csv", index_col=0)
    elif what_measure == 'simpson':
        dataset_1_global = pd.read_csv(f"{dataset_1}_metapop_simpson.csv", index_col=0)
        dataset_2_global = pd.read_csv(f"{dataset_2}_metapop_simpson.csv", index_col=0)
    elif what_measure == 'gini':
        dataset_1_global = pd.read_csv(f"{dataset_1}_metapop_gini.csv", index_col=0)
        dataset_2_global = pd.read_csv(f"{dataset_2}_metapop_gini.csv", index_col=0)
    else:
        print("You need to decide what measure you will plot: 'set_counts', 'shannon', 'simpson' or 'gini'?")
    
    plt.plot(dataset_1_global.mean(axis=1), color = 'xkcd:blue')
    plt.plot(dataset_2_global.mean(axis=1), color = 'xkcd:puce')
    
    plt.fill_between(dataset_1_global.index, dataset_1_global.mean(axis=1) - dataset_1_global.std(axis=1), dataset_1_global.mean(axis=1) + dataset_1_global.std(axis=1), color='xkcd:blue', alpha=0.3)
    plt.fill_between(dataset_2_global.index, dataset_2_global.mean(axis=1) - dataset_2_global.std(axis=1), dataset_2_global.mean(axis=1) + dataset_2_global.std(axis=1), color='xkcd:puce', alpha=0.3)
    
    plt.axvline(500, color="black", linestyle='--', ymax=1)

    if dataset_3 is not None:
        # TODO FIX HERE
        dataset_3_global = pd.read_csv(f"{dataset_3}_metapop_set_counts.csv", index_col=0)
        plt.plot(dataset_3_global.mean(axis=1), color = 'xkcd:light purple')
        plt.fill_between(dataset_3_global.index, dataset_3_global.mean(axis=1) - dataset_3_global.std(axis=1), dataset_3_global.mean(axis=1) + dataset_3_global.std(axis=1), color='xkcd:light purple', alpha=0.3)


    if dataset_3 is not None:
        plt.legend([f"{legend_1}", f"{legend_2}", f"{legend_3}"])
    else:
        plt.legend([f"{legend_1}", f"{legend_2}"])

    plt.ylabel("Number of feature sets")
    plt.xlabel("Generations (x100)")
    plt.grid(linestyle=':', linewidth=0.5)
    plt.title(title)

    plt.savefig(output_file)