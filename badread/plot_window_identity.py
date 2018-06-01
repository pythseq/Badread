"""
Copyright 2018 Ryan Wick (rrwick@gmail.com)
https://github.com/rrwick/Badread/

This file is part of Badread. Badread is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version. Badread is distributed
in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details. You should have received a copy of the GNU General Public License along with Badread.
If not, see <http://www.gnu.org/licenses/>.
"""

import matplotlib
import matplotlib.pyplot as plt
from .alignment import load_alignments, align_sequences
from .misc import load_fasta, load_fastq, reverse_complement


def plot_window_identity(args):
    reads = load_fastq(args.reads)
    refs = load_fasta(args.reference)
    alignments = load_alignments(args.alignment)

    for a in alignments:
        print(a)
        read_seq, read_qual = (x[a.read_start:a.read_end] for x in reads[a.read_name])
        ref_seq = refs[a.ref_name][a.ref_start:a.ref_end]
        if a.strand == '-':
            ref_seq = reverse_complement(ref_seq)
        _, _, errors_per_read_pos = align_sequences(read_seq, ref_seq, a)
        positions, identities = get_window_identity(errors_per_read_pos, args.window, a.read_start)
        plot_one_alignment(positions, identities, args.window, a, len(reads[a.read_name][0]))


def get_window_identity(errors_per_read_pos, window_size, read_start):
    positions, identities = [], []
    window_sum = sum(errors_per_read_pos[:window_size])
    for i in range(len(errors_per_read_pos) - window_size):
        window_start = i
        window_end = i + window_size
        window_centre = i + (window_size // 2)

        identities.append(100.0 * (1.0 - window_sum / window_size))
        positions.append(read_start + window_centre)

        window_sum -= errors_per_read_pos[window_start]
        window_sum += errors_per_read_pos[window_end]
    return positions, identities


class MyAxes(matplotlib.axes.Axes):
    name = "MyAxes"

    def drag_pan(self, button, key, x, y):
        matplotlib.axes.Axes.drag_pan(self, button, 'x', x, y)  # pretend key=='x'


matplotlib.projections.register_projection(MyAxes)


def plot_one_alignment(positions, identities, window_size, alignment, read_length):
    fig = plt.figure(figsize=(12, 4))
    fig.add_subplot(111, projection='MyAxes')
    plt.plot(positions, identities, '-')
    plt.ylabel('% identity ({} bp windows)'.format(window_size))
    plt.title('{} ({} bp, {:.1f}% identity)'.format(alignment.read_name, read_length,
                                                    alignment.percent_identity))
    plt.gca().set_xlim([0,10000])
    plt.gca().set_ylim([50,100])
    fig.canvas.manager.toolbar.pan()
    plt.show()
