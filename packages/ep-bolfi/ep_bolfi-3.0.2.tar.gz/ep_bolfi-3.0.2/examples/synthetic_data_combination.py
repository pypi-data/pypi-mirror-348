import csv
from os import linesep

for folder in ("full_cell", "negative_3ele_cell", "positive_3ele_cell"):
    for noise_label in (
        "pulses",
        "pulses_with_realistic_noise",
        "pulses_with_exaggerated_noise"
    ):
        for i in range(85):
            data = [[], [], [], [], []]
            with open(
                "./GITT synthetic data/cell voltage/"
                + folder
                + "/"
                + noise_label
                + "/pulse_"
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
            with open(
                "./GITT synthetic data/overpotential/"
                + folder
                + "/"
                + noise_label
                + "/pulse_"
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
                    data[4].append(row[2])
            header = (
                "Time[s],Current[A],Voltage[V],Segment,Overpotential[V]"
                + linesep
            )
            data = [[t, c, v, int(s), o] for t, c, v, s, o in zip(*data)]
            with open(
                "./GITT synthetic data/combined/"
                + folder
                + "/"
                + noise_label
                + "/pulse_"
                + str(i)
                + ".csv",
                'w',
                newline=''
            ) as f:
                f.write(header)
                writer = csv.writer(f, delimiter=',')
                writer.writerows(data)
