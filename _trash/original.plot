set style line 1 \
    linecolor rgb '#0060ad' \
    linetype 1 linewidth 2 \
    pointtype 7 pointsize 1.5
set style line 2 \
    linecolor rgb 'red' \
    linetype 1 linewidth 2 \
    pointtype 7 pointsize 1.5

set xdata time
set timefmt "%m/%d/%y"
set format x "%m/%d"

set ylabel "Delta / week (PiB)" textcolor rgb '#0060ad'

set ytics nomirror
set y2tics
set y2range [0:100]
set y2label "% change / week" textcolor rgb "red"

set key off

plot 'netspace.dat' using 1:3 title "Delta/week (PiB)" with linespoints linestyle 1, \
    '' using 1:(100*$4) title "% change/week" with linespoints linestyle 2


