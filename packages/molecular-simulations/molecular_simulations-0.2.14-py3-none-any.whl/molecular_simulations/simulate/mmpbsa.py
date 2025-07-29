from MMPBSA_mods import main
from pathlib import Path
import shutil
import subprocess
from typing import Union

PathLike = Union[Path, str]

class MMGBSA:
    def __init__(self,
                 top: PathLike,
                 dcd: PathLike,
                 use_mpi: bool=False):
        self.top = top
        self.traj = dcd
        self.use_mpi = use_mpi

    def generate_mdcrd(self) -> None:
        cpptraj_in = [
            f'parm {self.top}', 
            f'parm {self.top} [top1]',
            f'trajin {self.traj} {self.ff} last {self.lf}',
            f'trajout {self.traj.with_suffix(".mdcrd")} [top1]'
        ]
        
        name = self.write_script('\n'.join(cpptraj_in))
        subprocess.call(f'cpptraj -f {name}', shell=True)

        self.traj = self.traj.with_suffix('.mdcrd')
        shutil.remove(name)

    def generate_solvent_input(self) -> None:
        solv = [
            '&general',
            'startframe=1',
            'endframe=6000',
            'interval=1',
            'verbose=2',
            'keep_files=2',
            '/',
            '&gb',
            'igb=2',
            'saltcon=0.15',
            '/'
        ]

        return self.write_script('\n'.join(solv))

    def mmpbsa(self):
        if self.use_mpi:
            from mpi4py import MPI
        else:
            from MMPBSA_mods.fake_mpi import MPI
        
        main.setup_run()
        app = main.MMPBSA_App(MPI)

        app.read_input_file()
        app.process_input()
        app.check_for_bad_input()
        app.loadcheck_prmtops()
        app.file_setup()

        app.run_mmpbsa()

        app.parse_output_files()
        app.write_final_outputs()
        app.finalize()
        
    @staticmethod
    def write_script(code: str) -> PathLike:
        name = 'script.txt'
        with open(name, 'w') as f:
            f.write(code)

        return name

class MMPBSA(MMGBSA):
    def __init__(self):
        pass

    def generate_solvent_input(self):
        pass
