#PBS -N pet-seg
#PBS -l walltime=1:30:00
#PBS -l nodes=1:ppn=20:gpus=1
#PBS -j oe
#PBS -A PAS1759

# uncomment if using qsub
cd $PBS_O_WORKDIR
echo $PBS_O_WORKDIR

module reset
source $HOME/osc_classes/PHYSICS6820/mypython/bin/activate
which python
module load cuda/10.1.168

time python3 ct-scan-seg.py
