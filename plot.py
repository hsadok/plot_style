#!/usr/bin/env python3.9

import math

from itertools import cycle
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

import numpy as np

from pubplot import Document
from pubplot.document_classes import acm_sigconf

inches_per_pt = 1.0 / 72.27
golden_ratio = (1.0 + math.sqrt(5.0)) / 2.0
doc = Document(acm_sigconf)
width = doc.columnwidth
height = width / golden_ratio
width = width * inches_per_pt
height = height * inches_per_pt * 0.8
figsize = [width, height]

width_third = doc.textwidth / 3
height_third = width_third / golden_ratio
width_third = width_third * inches_per_pt
height_third = height_third * inches_per_pt
figsize_third = [width_third, height_third]

width_full = doc.textwidth
height_full = width_full / golden_ratio / 3
width_full = width_full * inches_per_pt
height_full = height_full * inches_per_pt
figsize_full = [width_full, height_full]

tight_layout_pad = 0.21
linewidth = 2
elinewidth = 0.5
capsize = 1
capthick = 0.5

# This is "colorBlindness::PairedColor12Steps" from R.
# Check others here: https://r-charts.com/color-palettes/#discrete
palette = [
    '#19B2FF',
    '#2ca02c',  # "#32FF00",  # I hate this green, so I changed it... It may
                # not be as color-blind friendly as it was originally but since
                # we also use patterns, it should be fine.
    '#FF7F00',
    '#654CFF',
    '#E51932',
    '#FFBF7F',
    '#FFFF99',
    '#B2FF8C',
    '#A5EDFF',
    '#CCBFFF'
]

hatch_list = ['////////', '-----', '+++++++', '|||||||']

linestyle = [
    (0, (1, 0)),
    (0, (4, 1)),
    (0, (2, 0.5)),
    (0, (1, 0.5)),
    (0, (0.5, 0.5)),
    (0, (4, 0.5, 0.5, 0.5)),
    (0, (3, 1, 1, 1)),
    (0, (8, 1)),
    (0, (3, 1, 1, 1, 1, 1)),
    (0, (3, 1, 1, 1, 1, 1, 1, 1)),
]

prop_cycle = mpl.cycler(color=palette) + mpl.cycler(linestyle=linestyle)

style = {
    # Line styles.
    'axes.prop_cycle': prop_cycle,

    # Grid.
    'grid.linewidth': 0.2,
    'grid.alpha': 0.4,
    'axes.grid': True,
    'axes.axisbelow': True,

    'axes.linewidth': 0.2,

    # Ticks.
    'xtick.major.width': 0.2,
    'ytick.major.width': 0.2,
    'xtick.minor.width': 0.2,
    'ytick.minor.width': 0.2,

    # Font.
    # You can use any of the predefined LaTeX font sizes here as well as
    # "caption", to match the caption size.
    'font.family': 'serif',
    'font.size': doc.footnotesize,
    'axes.labelsize': doc.small,
    'legend.fontsize': doc.footnotesize,
    'xtick.labelsize': doc.footnotesize,
    'ytick.labelsize': doc.footnotesize,

    'patch.linewidth': 0.2,

    'figure.dpi': 1000,

    'text.usetex': True
}


# Apply style globally.
for k, v in style.items():
    mpl.rcParams[k] = v


def bar_subplot(ax, xlabel: str, ylabel: str, xtick_labels: list,
                data: list[dict], width_scale: float = 0.7) -> None:
    x = np.arange(len(xtick_labels))  # The xtick_labels locations.
    nb_catgs = len(data)
    bar_width = width_scale/nb_catgs  # The width of the bars.
    offset = bar_width * (1 - nb_catgs) / 2

    for d, color, hatch in zip(data, cycle(palette), cycle(hatch_list)):
        ax.bar(x + offset, d['values'], bar_width, yerr=d['errors'],
               label=d['label'], fill=False, hatch=hatch, edgecolor=color,
               error_kw=dict(elinewidth=elinewidth, capsize=capsize,
                             capthick=capthick))
        offset += bar_width

    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    ax.set_xticks(x)
    ax.set_xticklabels(xtick_labels)

    ax.tick_params(axis='both', length=0)
    ax.grid(visible=False, axis='x')


def bar_plot(xlabel: str, ylabel: str, xtick_labels: list, data, fig_name,
             dest_dir,
             set_figsize=None, legend_kwargs=None, hide_legend=False,
             width_scale=0.7) -> None:
    fig, ax = plt.subplots()

    bar_subplot(ax, xlabel, ylabel, xtick_labels, data, width_scale)

    if set_figsize is None:
        set_figsize = figsize

    if not hide_legend:
        if legend_kwargs is None:
            ax.legend()
        else:
            ax.legend(**legend_kwargs)

    fig.set_size_inches(*set_figsize)
    fig.tight_layout(pad=0.1)

    plt.savefig(dest_dir / f'{fig_name}.pdf')
    plt.savefig(dest_dir / f'{fig_name}.png')


def example_bar_plot() -> None:
    # In this example we will plot the result of a made-up survey with people
    # from different age groups. The survey targets a very important
    # issue: What percentage of people in each age group likes basil or
    # cilantro?

    # Note that these labels can use LaTeX notation, we are using `\\%`` to
    # create a `%` and `--` to create an en-dash.
    xlabel = 'Age group'
    ylabel = 'Fraction of people (\\%)'
    xtick_labels = ['0--12', '13--17', '18--29', '30--49', '50+']

    # `bar_plot` takes data in a specific format. Every "series" is an element
    # in the list
    data = [
        {
            'label': 'Cilantro',
            'values': [12, 32, 48, 41, 85],  # These are the actual value
                                             # displayed in the bar plot (often
                                             # the median or average).
                                             # Values correspond to the
                                             # `xtick_labels` we defined above.
                                             # So 32% of people between 13 and
                                             # 18 like cilantro.
            'errors': [1, 2, 1, 10, 20]  # These are used for error bars
                                         # (often the standard deviation).
        },
        {
            'label': 'Basil',
            'values': [84, 72, 99, 87, 60],
            'errors': [5, 6, 2, 10, 18]
        }
    ]

    # Where to save the figure, it will produce both a pdf and a png. Use pdf
    # for the paper, png is useful for some presentation software that does not
    # accept pdf (e.g., Google slides).
    dest_dir = Path.cwd()  # Same as Path('./')
    fig_name = 'example_bar_plot'

    # Optional: The default figure size takes an entire column, the following
    # is the same as the default, but it could be changed for instance to
    # occupy a third of the page (`figsize_third`).
    set_figsize = figsize

    # Optional: Use legend_kwargs to control the legend placement and
    # configuration. If not specified, it the legend is placed automatically.
    # The following example places the legend on top of the plot, which is
    # useful when you want to avoid to overlap with the data.
    # Check this link for other examples:
    # https://matplotlib.org/3.5.0/api/_as_gen/matplotlib.pyplot.legend.html
    legend_kwargs = {
        'loc': 'lower right', 'ncol': 2, 'bbox_to_anchor': (0, 1, 1, 1)
    }

    bar_plot(xlabel, ylabel, xtick_labels, data, fig_name,
             dest_dir, set_figsize=set_figsize, legend_kwargs=legend_kwargs,
             hide_legend=False)


def example_line_plot():
    # Line plot simply uses the matplotlib functions. So there is not much to
    # describe here.

    dest_dir = Path.cwd()  # Same as Path('./')
    fig_name = 'example_line_plot'

    x1 = [1, 2, 3, 4, 5]
    y1 = [20, 30, 40, 50, 60]
    err1 = [2, 3, 2, 1, 3]

    x2 = [1, 2, 3, 4, 5]
    y2 = [20, 50, 10, 20, 30]
    err2 = [2, 3, 2, 1, 3]

    fig, ax = plt.subplots()

    # This makes sure the figure fits the column.
    fig.set_size_inches(*figsize)

    ax.errorbar(x1, y1, yerr=err1, elinewidth=linewidth, label='Data 1')
    ax.errorbar(x2, y2, yerr=err2, elinewidth=linewidth, label='Data 2')

    plt.legend(fontsize=doc.footnotesize)

    ax.set_xlabel('x label')
    ax.set_ylabel('y label')

    ax.tick_params('y', length=0)
    ax.tick_params('x', length=0)

    fig.tight_layout(pad=tight_layout_pad)

    plt.savefig(dest_dir / f'{fig_name}.pdf')
    plt.savefig(dest_dir / f'{fig_name}.png')


def main() -> None:
    example_bar_plot()
    example_line_plot()


if __name__ == '__main__':
    main()
