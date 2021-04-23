set style line 1 \
    linecolor rgb '#aacaff' \
    pointtype 7 pointsize 0.5
set style line 2 \
    linecolor rgb '#0060ad' \
    linetype 1 linewidth 2 \
    pointtype 7 pointsize 1.5

set xdata time
set timefmt "%s"
set format x "%m/%d"

set multiplot layout 3,1

set lmargin 10

set ylabel "Chia Netspace (PiB)"
set yrange [0:]

set key off

plot 'netspace.tsv' using 1:2 with points linestyle 1, \
                 '' using 1:3 with lines linestyle 2

set size 1,0.67
set origin 0,0

set ylabel "Growth (PiB/week)" textcolor rgb "#0060ad"
set yrange [-100:]

plot 'netspace.tsv' using 1:4 with lines linestyle 2

unset multiplot

