#! /bin/bash
  
../quick-cliques/bin/qc --input-file=../quick-cliques/data/snap/snap-amazon0601 --algorithm=tomita > cliques/snapamazon.tomita.cliques 2> cliques/snapamazon.tomita.log
../quick-cliques/bin/qc --input-file=../quick-cliques/data/snap/snap-amazon0601 --algorithm=adjlist > cliques/snapamazon.adjlist.cliques 2> cliques/snapamazon.adjlist.log
../quick-cliques/bin/qc --input-file=../quick-cliques/data/snap/snap-amazon0601 --algorithm=degeneracy > cliques/snapamazon.degeneracy.cliques 2> cliques/snapamazon.degeneracy.log
../quick-cliques/bin/qc --input-file=../quick-cliques/data/snap/snap-amazon0601 --algorithm=hybrid > cliques/snapamazon.hybrid.cliques 2> cliques/snapamazon.hybrid.log

../quick-cliques/bin/qc --input-file=../quick-cliques/data/marknewman/marknewman-astro --algorithm=tomita > cliques/marknewmanastro.tomita.cliques 2> cliques/marknewmanastro.tomita.log
../quick-cliques/bin/qc --input-file=../quick-cliques/data/marknewman/marknewman-astro --algorithm=adjlist > cliques/marknewmanastro.adjlist.cliques 2> cliques/marknewmanastro.adjlist.log
../quick-cliques/bin/qc --input-file=../quick-cliques/data/marknewman/marknewman-astro --algorithm=degeneracy > cliques/marknewmanastro.degeneracy.cliques 2> cliques/marknewmanastro.degeneracy.log
../quick-cliques/bin/qc --input-file=../quick-cliques/data/marknewman/marknewman-astro --algorithm=hybrid > cliques/marknewmanastro.hybrid.cliques 2> cliques/marknewmanastro.hybrid.log

../quick-cliques/bin/qc --input-file=../quick-cliques/data/marknewman/marknewman-condmat --algorithm=tomita > cliques/marknewmancondmat.tomita.cliques 2> cliques/marknewmancondmat.tomita.log
../quick-cliques/bin/qc --input-file=../quick-cliques/data/marknewman/marknewman-condmat --algorithm=adjlist > cliques/marknewmancondmat.adjlist.cliques 2> cliques/marknewmancondmat.adjlist.log
../quick-cliques/bin/qc --input-file=../quick-cliques/data/marknewman/marknewman-condmat --algorithm=degeneracy > cliques/marknewmancondmat.degeneracy.cliques 2> cliques/marknewmancondmat.degeneracy.log
../quick-cliques/bin/qc --input-file=../quick-cliques/data/marknewman/marknewman-condmat --algorithm=hybrid > cliques/marknewmancondmat.hybrid.cliques 2> cliques/marknewmancondmat.hybrid.log
