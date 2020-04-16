# Copyright 2020 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

## ------- import packages -------
from dwave.system import DWaveSampler, EmbeddingComposite
import dwave.inspector as inspector

# TODO:  Add code here to define your QUBO dictionary
def get_qubo(S):
    """Returns a dictionary representing a QUBO.

    Args:
        S(list of integers): represents the numbers being partitioned
    """

    Q = {}
    c = sum(S)

    # Add QUBO construction here
    for i in range(len(S) - 1):

        # Add the linear terms
        Q[i, i] = -4*c*S[i] + 4*S[i]**2

        # Add the quadratic terms
        for j in range(i+1, len(S)):
            Q[i, j] = 8*S[i]*S[i+1]
        
        
    return Q

# TODO:  Choose QPU parameters in the following function
def run_on_qpu(Q, sampler):
    """Runs the QUBO problem Q on the sampler provided.

    Args:
        Q(dict): a representation of a QUBO
        sampler(dimod.Sampler): a sampler that uses the QPU
    """

    chainstrength = 15000 # update
    numruns = 1000 # update

    sample_set = sampler.sample_qubo(Q, chain_strength=chainstrength, num_reads=numruns)
    inspector.show(sample_set)

    return sample_set


## ------- Main program -------
if __name__ == "__main__":

    ## ------- Set up our list of numbers -------
    S = [25, 7, 13, 31, 42, 17, 21, 10]

    # TODO: Enter your token here
    # token = 'Your-Token-Here'

    ## ------- Set up our QUBO dictionary -------

    Q = get_qubo(S)

    ## ------- Run our QUBO on the QPU -------

    sampler = EmbeddingComposite(DWaveSampler(solver={'qpu': True}))

    sample_set = run_on_qpu(Q, sampler)

    ## ------- Return results to user -------
    for sample in sample_set:
        S1 = [S[i] for i in sample if sample[i] == 1]
        S0 = [S[i] for i in sample if sample[i] == 0]
        print("S0 Sum: ", sum(S0), "\tS1 Sum: ", sum(S1), "\t", S0) 
