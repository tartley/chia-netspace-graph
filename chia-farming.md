# Drive endurance

Documentation for H:Plotting(1TB ssd) allegedly shows 600TBW endurance:
https://documents.westerndigital.com/content/dam/doc-library/en_us/assets/public/western-digital/product/internal-drives/wd-blue-nvme-ssd/product-brief-wd-blue-sn550-nvme-ssd.pdf
At (I think) 1.1TB writes per plot gives lifetime of ~550 plots.

# Plotting times

D:Data (1TB hdd): 20.2 hours
plots per day = 24/20.2 = 1.19 p/d

H:Plotting(1TB ssd): 12.6 hours = 1.9 p/d

2x:
H:Plotting(1TB ssd): 11.6
H:Plotting(1TB ssd): 11.6
24/11.6 + 24/11.6 = 4.13 p/d

3x:
1x on H:Plotting: 52174.234 seconds = 14.5 hours
1x on H:Plotting: 51379.967 seconds = 14.3 hours
1x on D:Data: 65451.866 seconds = 18.2 hours
24/14.5 + 24/14.3 + 24/18.2 = 1.66 + 1.68 + 1.32 = 4.67 p/d

# Netspace growth

Mar 20: 120PiB
Apr 04: 206PiB
15 days = 2.143 weeks (chia explorer requires per week)

final = initial . (rate ^ period)
rate = (final / initial) ^ (1 / period)
rate = (206 / 123) ^ (1 / 2.143)
     = 1.29
     = 29% growth per week

Or, weekly:

date      netspace  delta  %change
03/20/21  121
03/27/21  145       24     +20%
04/03/21  191       46     +32%
04/10/21  268       77     +40%

# Expected earnings

Initial plots: 1.68TiB
Plotting speed: 413GiB/day
Max size: 16TiB

10XCH after 3 months, never reaching 11.

Increasing farming space barely improves that
(eg. doubling to 32TiB approaches, but does not reach, 14 XCH)

Key is to also speed up plotting, and do it ASAP, before netspace gets too big.

eg. Doubling plotting speed AND doubling storage gives a final yield of 20XCH.

