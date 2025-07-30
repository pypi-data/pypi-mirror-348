import unittest
from eacy import collate
import numpy as np


def test_collate():
        import pickle
        params_to_compare = pickle.load(open("eacy_params.pk", "rb"))
        telescope_name = "EAC1"
        instrument_name = "CI"
        detector_name = "IMAGER"
        output_format = "pickle"
        #print(collate(telescope_name, instrument_name, detector_name, output_format, save=False))
        #print(params_to_compare)
        #print(np.diff(collate(telescope_name, instrument_name, detector_name, output_format, save=False), params_to_compare))

        # Find keys that are different
        dict1 = collate(telescope_name, instrument_name, detector_name, output_format, save=False)
        dict2 = params_to_compare
        keys_in_dict1_not_in_dict2 = dict1.keys() - dict2.keys()
        keys_in_dict2_not_in_dict1 = dict2.keys() - dict1.keys()

        # Find differing values for common keys
        differing_values = {}
        for k in dict1.keys() & dict2.keys():
            v1, v2 = dict1[k], dict2[k]
            if isinstance(v1, np.ndarray) and isinstance(v2, np.ndarray):
                if not np.array_equal(v1, v2):  # Use np.array_equal for array comparison
                    differing_values[k] = (v1, v2)
            elif v1 != v2:  # Regular comparison for non-array values
                differing_values[k] = (v1, v2)

        # Combine results
        difference = {
            "keys_in_dict1_not_in_dict2": keys_in_dict1_not_in_dict2,
            "keys_in_dict2_not_in_dict1": keys_in_dict2_not_in_dict1,
            "differing_values": differing_values,
        }

        print(difference)
        are_equal = True
        for k in dict1.keys() | dict2.keys():  # Union of keys
            if k not in dict1 or k not in dict2:
                are_equal = False
                break
            v1, v2 = dict1[k], dict2[k]
            if isinstance(v1, np.ndarray) and isinstance(v2, np.ndarray):
                if not np.array_equal(v1, v2):  # Use np.array_equal for array comparison
                    are_equal = False
                    break
            elif v1 != v2:  # Regular comparison for non-array values
                are_equal = False
                break
        print("Are dict1 and dict2 equal?", are_equal)

if __name__ == "__main__":
    test_collate()