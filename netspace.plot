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

# Reddit doesn't like svg images
# set term svg enhanced
# set output "netspace.svg"

set term pngcairo enhanced size 800,600
set output "netspace.png"

set xdata time
set x2data time
set timefmt "%s"
set xrange [1616155200:]
set x2range [1616155200:]

set grid xtics ytics linestyle 10

set key off

set multiplot layout 2,1

set lmargin 10
set rmargin 10
set bmargin 0.5
set tmargin 1.5

set format x ""
set format x2 "%m/%d"
set x2tics 1616155200,604800
set xtics 1616155200,604800
set ylabel "Size (PiB)"
set yrange [0:*]

plot 'netspace.tsv' using 1:2 with points linestyle 1, \
                 '' using 1:3 with lines linestyle 2, \

unset x2tics
set tmargin 0.5
set ytics nomirror
set ylabel "Growth (PiB/week)" textcolor rgb "#0060ad"
set yrange [0:700]
set bmargin 1.5
set format x "%m/%d"
set y2label "Growth (%/week)" textcolor rgb "#ad3030"
set y2tics
set key top left box

set link y2 via y/5 inverse y*5

plot 'netspace.tsv' using 1:4 title "Growth PiB/week" with lines linestyle 2, \
                 '' using 1:5 title "Growth %/week" with lines linestyle 3 axis x1y2

unset multiplot

