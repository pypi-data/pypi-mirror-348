from qiskit import QuantumCircuit
import matplotlib.pyplot as plt
from qiskit_ibm_runtime.fake_provider import FakeLimaV2, FakeBrisbane, FakeSherbrooke, FakeAthensV2
from qiskit.quantum_info import Statevector
from .models import Autoencoder
from .utils import full_counts
# Do for visualization
from .plot_utils import overall_plot

class Overall_test():
    def __init__(self):
        self.AE =  Autoencoder()
        self.backends = {"FakeLima": FakeLimaV2(),
                        "FakeAthens": FakeAthensV2(),
                        "FakeBrisbane": FakeBrisbane(),
                        "FakeSherbrooke": FakeSherbrooke()}
        self.jobs = {}

    def add_job(self, circ: QuantumCircuit, job_id: str, backend_id=""):
        if not isinstance(circ, QuantumCircuit):
            raise TypeError("You have to give a Quantum circuit object instead.")
        if not isinstance(job_id, str):
            raise TypeError("The jod id should be a string.")
        if not isinstance(backend_id, str):
            raise TypeError("The backend id should be a string.")
        if backend_id not in list(self.backends.keys()):
            raise KeyError(f"The backend id is not in the storage. The available backends are {list(self.backends.keys())}")
        if backend_id == None:
            backend_id = "FakeLima"
            backend = self.backends["FakeLima"]
        else:
            backend = self.backends[backend_id]
        circ.remove_final_measurements()
        theorem = Statevector(data=circ).probabilities()
        circ.measure_all()
        noise_result = full_counts(backend.run(circ, shots=10000).result().get_counts())/10000
        miti_result = self.AE.mitigation(noise_result)
        self.jobs[f"{job_id}"] = {"circuit": circ, "backend":backend_id, "Statevector":theorem, "noisy_input":noise_result, "Autoencoder": miti_result}

    def visualization(self, job_id: str):
        if job_id not in self.jobs.keys():
            raise KeyError("The job id is not in the storage. Please check again.")
        plotter = overall_plot(self.jobs[job_id])
        plotter.plot_result()
    
    def MAE_visualization(self, job_id: str, data):
        if job_id not in self.jobs.keys():
            raise KeyError("The job id is not in the storage. Please check again.")  
        plotter = overall_plot(self.jobs[job_id])
        plotter.plot_MAE(data)
        
        
        
        
        
        