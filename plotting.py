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


def metapopulation_plot_comparison(dataset_1, dataset_2, title, legend_1, legend_2, output_file, what_measure, number_of_pulses = 5, length_of_pulses = 1, settling_period = 99,  dataset_3 = None, legend_3 = None):
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
    elif what_measure == 'beta':
        dataset_1_global = pd.read_csv(f"{dataset_1}_beta_diversity.csv", index_col=0)
        dataset_2_global = pd.read_csv(f"{dataset_2}_beta_diversity.csv", index_col=0)
    else:
        raise ValueError("You need to decide what measure you will plot: 'set_counts', 'shannon', 'simpson' or 'gini'?")
    
    color1 = "xkcd:medium blue"
    color2 = "xkcd:violet"
    color3 = "xkcd:dark orange"

    line1, = plt.plot(dataset_1_global.mean(axis=1), color = color1, label=f"{legend_1}")
    line2, = plt.plot(dataset_2_global.mean(axis=1), color = color2, label=f"{legend_2}")
    
    plt.fill_between(dataset_1_global.index, dataset_1_global.mean(axis=1) - dataset_1_global.std(axis=1), dataset_1_global.mean(axis=1) + dataset_1_global.std(axis=1), color=color1, alpha=0.2)
    plt.fill_between(dataset_2_global.index, dataset_2_global.mean(axis=1) - dataset_2_global.std(axis=1), dataset_2_global.mean(axis=1) + dataset_2_global.std(axis=1), color=color2, alpha=0.2)
    
    plt.axvline(500, color="black", linestyle='--', ymax=1)

    if dataset_3 is not None:
        if what_measure == 'set_counts':
            dataset_3_global = pd.read_csv(f"{dataset_3}_metapop_set_counts.csv", index_col=0)
        elif what_measure == 'shannon':
            dataset_3_global == pd.read_csv(f"{dataset_3}_metapop_shannon.csv", index_col=0)
        elif what_measure == 'simpson':
            dataset_3_global = pd.read_csv(f"{dataset_3}_metapop_simpson.csv", index_col=0)
        elif what_measure == 'gini':
            dataset_3_global = pd.read_csv(f"{dataset_3}_metapop_gini.csv", index_col=0)
        elif what_measure == 'beta':
            dataset_3_global = pd.read_csv(f"{dataset_3}_beta_diversity.csv", index_col=0)
        else:
            print("You need to decide what measure you will plot: 'set_counts', 'shannon', 'simpson' or 'gini'?")

        line3, = plt.plot(dataset_3_global.mean(axis=1), color = color3, label=f"{legend_3}")
        plt.fill_between(dataset_3_global.index, dataset_3_global.mean(axis=1) - dataset_3_global.std(axis=1), dataset_3_global.mean(axis=1) + dataset_3_global.std(axis=1), color=color3, alpha=0.2)

    if dataset_3 is not None:
        plt.legend(loc=3, handles=[line1, line2, line3])
    else:
        plt.legend([f"{legend_1}", f"{legend_2}"])

    plt.axvline(500, color="black", linestyle='--', ymax=1)
    for i in range(1, number_of_pulses + 1):
        plt.axvline(500 + i*(length_of_pulses + settling_period), color="dimgrey", linestyle='--', ymax=1)
    
    match what_measure:
        case 'set_counts':
            plt.ylabel("Number of sets of features")
        case 'shannon':
            plt.ylabel("Shannon diversity")
        case 'simpson':
            plt.ylabel("Simpson diversity")
        case 'gini':
            plt.ylabel(r"Gini-Simpson diversity")
        case 'beta':
            plt.ylabel(r"Whittaker $\beta$-diversity")
    plt.xlabel("Steps (x100)")
    plt.grid(linestyle=':', linewidth=0.5)
    plt.title(title)

    plt.savefig(output_file)


def subpopulation_plot_comparison(dataset_1, dataset_2, title, legend_1, legend_2, output_file, what_measure, number_of_pulses = 5, length_of_pulses = 1, settling_period = 99,  dataset_3 = None, legend_3 = None):
    if what_measure == 'set_counts':
        dataset_1_global = pd.read_csv(f"{dataset_1}_subpop_set_counts.csv", index_col=0)
        dataset_2_global = pd.read_csv(f"{dataset_2}_subpop_set_counts.csv", index_col=0)
    elif what_measure == 'shannon':
        dataset_1_global == pd.read_csv(f"{dataset_1}_subpop_shannon.csv", index_col=0)
        dataset_2_global = pd.read_csv(f"{dataset_2}_subpop_shannon.csv", index_col=0)
    elif what_measure == 'simpson':
        dataset_1_global = pd.read_csv(f"{dataset_1}_subpop_simpson.csv", index_col=0)
        dataset_2_global = pd.read_csv(f"{dataset_2}_subpop_simpson.csv", index_col=0)
    elif what_measure == 'gini':
        dataset_1_global = pd.read_csv(f"{dataset_1}_subpop_gini.csv", index_col=0)
        dataset_2_global = pd.read_csv(f"{dataset_2}_subpop_gini.csv", index_col=0)
    else:
        raise ValueError("You need to decide what measure you will plot: 'set_counts', 'shannon', 'simpson' or 'gini'?")
    
    color1 = "xkcd:medium blue"
    color2 = "xkcd:violet"
    color3 = "xkcd:dark orange"

    line1, = plt.plot(dataset_1_global.mean(axis=1), color = color1, label=f"{legend_1}")
    line2, = plt.plot(dataset_2_global.mean(axis=1), color = color2, label=f"{legend_2}")
    
    plt.fill_between(dataset_1_global.index, dataset_1_global.mean(axis=1) - dataset_1_global.std(axis=1), dataset_1_global.mean(axis=1) + dataset_1_global.std(axis=1), color=color1, alpha=0.2)
    plt.fill_between(dataset_2_global.index, dataset_2_global.mean(axis=1) - dataset_2_global.std(axis=1), dataset_2_global.mean(axis=1) + dataset_2_global.std(axis=1), color=color2, alpha=0.2)
    
    plt.axvline(500, color="black", linestyle='--', ymax=1)

    if dataset_3 is not None:
        if what_measure == 'set_counts':
            dataset_3_global = pd.read_csv(f"{dataset_3}_subpop_set_counts.csv", index_col=0)
        elif what_measure == 'shannon':
            dataset_3_global == pd.read_csv(f"{dataset_3}_subpop_shannon.csv", index_col=0)
        elif what_measure == 'simpson':
            dataset_3_global = pd.read_csv(f"{dataset_3}_subpop_simpson.csv", index_col=0)
        elif what_measure == 'gini':
            dataset_3_global = pd.read_csv(f"{dataset_3}_subpop_gini.csv", index_col=0)
        else:
            print("You need to decide what measure you will plot: 'set_counts', 'shannon', 'simpson' or 'gini'?")

        line3, = plt.plot(dataset_3_global.mean(axis=1), color = color3, label=f"{legend_3}")
        plt.fill_between(dataset_3_global.index, dataset_3_global.mean(axis=1) - dataset_3_global.std(axis=1), dataset_3_global.mean(axis=1) + dataset_3_global.std(axis=1), color=color3, alpha=0.2)

    if dataset_3 is not None:
        plt.legend(loc=3, handles=[line1, line2, line3])
    else:
        plt.legend([f"{legend_1}", f"{legend_2}"])

    plt.axvline(500, color="black", linestyle='--', ymax=1)
    for i in range(1, number_of_pulses + 1):
        plt.axvline(500 + i*(length_of_pulses + settling_period), color="dimgrey", linestyle='--', ymax=1)
    
    match what_measure:
        case 'set_counts':
            plt.ylabel("Number of sets of features")
        case 'shannon':
            plt.ylabel("Shannon diversity")
        case 'simpson':
            plt.ylabel("Simpson diversity")
        case 'gini':
            plt.ylabel("Gini-Simpson diversity")
    # plt.ylim([0, 100])
    plt.xlabel("Steps (x100)")
    plt.grid(linestyle=':', linewidth=0.5)
    plt.title(title)

    plt.savefig(output_file)


def plot_comparison_gini_pulses(dataset_1, dataset_2, title, legend_1, legend_2, number_of_pulses, length_of_pulses, settling_period, output_file, dataset_3=None, legend_3=None):
    dataset_1_local = pd.read_csv(f"{dataset_1}_subpop_gini.csv", index_col=0)
    dataset_2_local = pd.read_csv(f"{dataset_2}_subpop_gini.csv", index_col=0)

    line1, = plt.plot(dataset_1_local.mean(axis=1), color = 'xkcd:sky blue', label=f"{legend_1} subpop avg")
    line2, = plt.plot(dataset_2_local.mean(axis=1), color = 'tan', label=f"{legend_2} subpop avg")
    plt.fill_between(dataset_1_local.index, dataset_1_local.mean(axis=1) - dataset_1_local.std(axis=1), dataset_1_local.mean(axis=1) + dataset_1_local.std(axis=1), color='xkcd:sky blue', alpha=0.3)
    plt.fill_between(dataset_2_local.index, dataset_2_local.mean(axis=1) - dataset_2_local.std(axis=1), dataset_2_local.mean(axis=1) + dataset_2_local.std(axis=1), color='tan', alpha=0.3)
    
    if dataset_3 is not None:
        dataset_3_local = pd.read_csv(f"{dataset_3}_subpop_gini.csv", index_col=0)
        line3, = plt.plot(dataset_3_local.mean(axis=1), color = 'mediumpurple', label=f"{legend_3} subpop avg")
        plt.fill_between(dataset_3_local.index, dataset_3_local.mean(axis=1) - dataset_3_local.std(axis=1), dataset_3_local.mean(axis=1) + dataset_3_local.std(axis=1), color='mediumpurple', alpha=0.3)
        #plt.legend([f"{legend_1} subpop avg", f"{legend_2} subpop avg", f"{legend_3} subpop avg"])
        plt.legend(loc=3, handles=[line1, line2, line3])
    
    else:    
        plt.legend([f"{legend_1} subpop avg", f"{legend_2} subpop avg"])


    plt.axvline(500, color="black", linestyle='--', ymax=1)
    for i in range(1, number_of_pulses + 1):
        plt.axvline(500 + i*(length_of_pulses + settling_period), color="dimgrey", linestyle='--', ymax=1)


    plt.ylabel("Gini-Simpson diversity index")
    plt.xlabel("Generations (x100)")
    plt.grid(linestyle=':', linewidth=0.5)
    plt.title(title)

    plt.savefig(output_file)


def plot_subpopulation_mean(dataset, subpop_id, output_file, number_of_pulses = 5, length_of_pulses = 1, settling_period = 99):
    # deme = pd.Series(dataset[dataset["Replicate"] == 0][f"{subpop_id}"])
    for replicate in dataset["Replicate"].unique():
        if replicate == 0:
            deme = pd.Series(dataset[dataset["Replicate"] == replicate][f"{subpop_id}"])

        deme = pd.concat([deme, pd.Series(dataset[dataset["Replicate"] == replicate][f"{subpop_id}"])], axis=1)

    fig = plt.plot(deme.mean(axis=1), color="tab:orange")
    std_plus = deme.mean(axis=1) + deme.std(axis=1)
    std_minus = deme.mean(axis=1) - deme.std(axis=1)
    # std_plus cannot be larger than 100 in the beginning (but values can as it can be below 0 and this is a symetric +/-!)
    std_plus[std_plus > 100] = 100
    std_minus[std_minus < 0] = 0
    plt.fill_between(deme.index, std_minus, std_plus, alpha = 0.3, color="tab:orange")
    plt.ylabel("Individuals with extra trait")
    plt.xlabel("Generations (x100)")
    plt.ylim([0, 100])
    plt.grid(linestyle=':', linewidth=0.5)
    plt.title(f"Extra trait in subpopulation {subpop_id}")
    
    plt.axvline(500, color="black", linestyle='--', ymax=1)
    for i in range(1, number_of_pulses + 1):
        plt.axvline(500 + i*(length_of_pulses + settling_period), color="dimgrey", linestyle='--', ymax=1)

    plt.savefig(output_file)
    
    return fig, deme