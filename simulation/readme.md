conda deactivate

cd /work/hdd/bbqg/wzhong/container

'''
apptainer run --writable-tmpfs \
--no-home \
--bind /taiga/illinois/eng/cee/meidani/Vincent:/taiga/illinois/eng/cee/meidani/Vincent \
--bind /u/wzhong/PhD/Github/NO4mre/simulation/:/simulation \
dolfinx_mre.sif
'''

cd /simulation

source /usr/local/bin/dolfinx-complex-mode



