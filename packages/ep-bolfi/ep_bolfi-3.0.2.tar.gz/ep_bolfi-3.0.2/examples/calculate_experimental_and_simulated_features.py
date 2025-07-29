import csv
import json
from multiprocessing import Pool
import numpy as np
from os import linesep
from runpy import run_module

from parameters.estimation.gitt import (
    calculate_experimental_and_simulated_features
)


def parallel_computation(i, estimation_result):
    data = run_module(
        'parameters.estimation.gitt_basf',
        init_globals={
            # set to False for full synthetic data
            'optimize_simulation_speed': False,
            'soc_dependent_estimation': True,
            'white_noise': False,
            'parameter_noise': False,
            'pulse_number': i,
            'overpotential': False,
            'three_electrode': 'negative'
        }
    )

    evaluation, sensitivity, experimental_feature, output_dataset = (
        calculate_experimental_and_simulated_features(
            [data['simulator']],
            [data['experimental_dataset']],
            [data['parameters']],
            [estimation_result],
            data['free_parameters_names'],
            data['transform_parameters'],
            bounds_in_standard_deviations=1
        )
    )
    return (
        evaluation,
        sensitivity,
        experimental_feature,
        output_dataset
    )


if __name__ == "__main__":
    with open(
        './GITT estimation results/'
        'estimation_results_with_pybamm_24_5_names.json',
        'r'
    ) as f:
        estimation_results = json.load(f)

    with Pool() as p:
        results = p.starmap(
            parallel_computation, list(enumerate(estimation_results))
        )

    feature_names = list(results[0][0].keys())
    parameter_names = list(results[0][1].keys())
    evaluations = {
        f_name: [0.0 for i in range(len(estimation_results))]
        for f_name in feature_names
    }
    sensitivities = {
        p_name: {
            f_name: [[0.0, 0.0] for i in range(len(estimation_results))]
            for f_name in feature_names
        }
        for p_name in parameter_names
    }
    experimental_features = {
        f_name: [0.0 for i in range(len(estimation_results))]
        for f_name in feature_names
    }
    output_datasets = []
    for i, (eva, sen, exp, out) in enumerate(results):
        for f_name in feature_names:
            evaluations[f_name][i] = eva[f_name][0]
            for p_name in parameter_names:
                sensitivities[p_name][f_name][i] = sen[p_name][f_name][0]
            experimental_features[f_name][i] = exp[f_name][0]
        output_datasets.append(out[0])

    """
    print("evaluations:")
    print(evaluations)
    print("sensitivities:")
    print(sensitivities)
    with open(
        "./GITT estimation results/simulated_features_at_each_pulse.json", "w"
    ) as f:
        json.dump(evaluations, f)
    with open(
        "./GITT estimation results/boundaries_of_simulated_features.json", "w"
    ) as f:
        json.dump(sensitivities, f)

    print("experimental_features:")
    print(experimental_features)
    with open(
        "./GITT estimation results/experimental_features_at_each_pulse.json",
        "w"
    ) as f:
        json.dump(experimental_features, f)
    """

    for i in range(len(output_datasets)):
        times, voltages, currents = output_datasets[i]
        j = len(times)
        k = [len(times[ell]) for ell in range(j)]
        times = np.array(np.concatenate(times))
        currents = np.array(np.concatenate(currents))
        voltages = np.array(np.concatenate(voltages))
        segments = np.zeros_like(times, dtype=np.int64)
        counter = 0
        for ell in range(j):
            length = k[ell]
            segments[counter:counter + length] = ell + 2 * i
            counter += length
        data = [
            [t, c, v, s]
            for t, c, v, s in zip(times, currents, voltages, segments)
        ]
        with open(
            "./GITT synthetic data/cell voltage/negative_3ele_cell/"
            "pulses/pulse_"
            + str(i)
            + ".csv",
            'w',
            newline=''
        ) as f:
            f.write("Time[s],Current[A],Voltage[V],Segment" + linesep)
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)
