set style line 10 \
    linecolor rgb "grey"
set style line 1 \
    linecolor rgb '#aacaff' \
    pointtype 7 pointsize 0.5
set style line 2 \
    linecolor rgb '#0060ad' \
    linetype 1 linewidth 2
set style line 3 \
    linecolor rgb '#ad3030' \
    linetype 1 linewidth 2

set xdata time
set timefmt "%s"
set xrange [:1619278720]

set grid xtics ytics linestyle 10

set key off

set multiplot layout 3,1

set lmargin 10
set rmargin 10
set bmargin 0.5
set tmargin 0.5

set format x ""
set ylabel "Size (PiB)"
set yrange [0:]

plot 'netspace.tsv' using 1:2 with points linestyle 1, \
                 '' using 1:3 with lines linestyle 2

set ytics nomirror
set ylabel "Growth (PiB/week)" textcolor rgb "#0060ad"
set yrange [-100:]

plot 'netspace.tsv' using 1:4 with lines linestyle 2

set bmargin 1.5
set format x "%m/%d"
set ylabel "Growth (%/week)" textcolor rgb "#ad3030"

plot 'netspace.tsv' using 1:5 with lines linestyle 3

unset multiplot

