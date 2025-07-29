import csv
from numpy import array
from numpy.random import default_rng

seed = 0
white_noise_generator = default_rng(seed)

for component in ("cell voltage",):
    for folder in ("full_cell", "negative_3ele_cell", "positive_3ele_cell"):
        for noise_level, label in zip(
            (0.1e-3, 0.5e-3),
            ("pulses_with_realistic_noise", "pulses_with_exaggerated_noise")
        ):
            for i in range(85):
                data = [[], [], [], []]
                with open(
                    "./GITT synthetic data/"
                    + component
                    + "/"
                    + folder
                    + "/pulses/pulse_"
                    + str(i)
                    + ".csv",
                    'r',
                    newline=''
                ) as f:
                    header = f.readline()
                    reader = csv.reader(
                        f, delimiter=',', quoting=csv.QUOTE_NONNUMERIC
                    )
                    for row in reader:
                        for j, entry in enumerate(row):
                            data[j].append(entry)
                data[2] = array(data[2]) + (
                    noise_level
                    * white_noise_generator.standard_normal(len(data[2]))
                )
                data = [[t, c, v, int(s)] for t, c, v, s in zip(*data)]
                with open(
                    "./GITT synthetic data/"
                    + component
                    + "/"
                    + folder
                    + "/"
                    + label
                    + "/pulse_"
                    + str(i)
                    + ".csv",
                    'w',
                    newline=''
                ) as f:
                    f.write(header)
                    writer = csv.writer(f, delimiter=',')
                    writer.writerows(data)
