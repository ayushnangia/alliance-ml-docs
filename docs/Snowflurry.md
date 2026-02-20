# Snowflurry

Other languages:

- English
- [français](Snowflurry.md)

[Snowflurry](https://github.com/SnowflurrySDK/Snowflurry.jl/) is an open-source quantum computing library developed in [Julia](Julia.md) by [Anyon Systems](https://anyonsys.com/) that allows you to build, simulate, and run quantum circuits. A related library called [SnowflurryPlots](https://github.com/SnowflurrySDK/SnowflurryPlots.jl/) allows you to visualize the simulation results in a bar chart. Useful to explore quantum computing, its features are described in the [documentation](https://snowflurrysdk.github.io/Snowflurry.jl/dev/index.html) and the [installation guide is available on the GitHub page](https://github.com/SnowflurrySDK/Snowflurry.jl). Like the [PennyLane](PennyLane.md) library, Snowflurry can be used to run quantum circuits on the [MonarQ](MonarQ.md) quantum computer.

## Installation

The quantum computer simulator with [Snowflurry](https://github.com/SnowflurrySDK/Snowflurry.jl) is available on all of our clusters. The [Julia](https://julialang.org/) programming language must be loaded before accessing Snowflurry.

```
[name@server ~]$ module load julia

```

The Julia programming interface is then called and the Snowflurry quantum library is loaded (in about 5-10 minutes) with the commands

```
[name@server ~]$ julia
julia> import Pkg
julia> Pkg.add(url="https://github.com/SnowflurrySDK/Snowflurry.jl", rev="main")
julia> Pkg.add(url="https://github.com/SnowflurrySDK/SnowflurryPlots.jl", rev="main")
julia> using Snowflurry

```

Quantum logic gates and commands are described in the [Snowflurry documentation](https://snowflurrysdk.github.io/Snowflurry.jl/dev/).

## Use case: Bell states

Bell states are maximally entangled two-qubit states. They are simple examples of two quantum phenomena: superposition and entanglement. The [Snowflurry](https://github.com/SnowflurrySDK/Snowflurry.jl/) library allows you to construct the first Bell state as follows:

```
[name@server ~]$ julia
julia> using Snowflurry
julia> circuit=QuantumCircuit(qubit_count=2);
julia> push!(circuit,hadamard(1));
julia> push!(circuit,control_x(1,2));
julia> print(circuit)

Quantum Circuit Object:
   qubit_count: 2 
q[1]:──H────*──
            ¦ 
q[2]:───────X──

```

In the above code section, the Hadamard gate creates an equal superposition of |0⟩ and |1⟩ on the first qubit while the CNOT gate (controlled X gate) creates an entanglement between the two qubits. We find an equal superposition of states |00⟩ and |11⟩, which is the first Bell state. The `simulate` function allows us to simulate the exact state of the system.

```
 julia> state = simulate(circuit)
 julia> print(state)   
 4-element Ket{ComplexF64}:
 0.7071067811865475 + 0.0im
 0.0 + 0.0im
 0.0 + 0.0im
 0.7071067811865475 + 0.0im

```

The `readout` operation lets you specify which qubits will be measured. The `plot_histogram` function from the SnowflurryPlots library allows you to visualize the results.

```
[name@server ~]$ julia
julia> using SnowflurryPlots
julia> push!(circuit, readout(1,1), readout(2,2))
julia> plot_histogram(circuit,1000)

```

[![Résultats de 1000 simulations de l'état de Bell.](/mediawiki/images/thumb/8/8b/Bell_Graph.png/300px-Bell_Graph.png)](FileBell_Graphpng.md)