#!/usr/bin/env python

# Comment out Matplotlib: KadiStudio imports this file.
# Have it in: Kadistudio errors out with "(WW) QPRocess: Destroyed while
# process (...) is still running. ((null:0, (null))
import matplotlib.pyplot as plt
import xmlhelpy


@xmlhelpy.command(
    name='python -m timeit', version='1.0'
)
@xmlhelpy.option(
    'number',
    char='n',
    param_type=xmlhelpy.Integer,
    default=50000000,
    description="See python -m timeit -h.",
)
def timeit(number):
    # Do nothing here, as this is supposed to be a dummy
    # for a package that would actually be installed.
    plt.show()
    return


if __name__ == '__main__':
    timeit()
