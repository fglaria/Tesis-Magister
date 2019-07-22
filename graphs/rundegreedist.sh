echo "ca-coauthors"
cat graphs/ca-coauthors.txt | awk -F " " '{if(NR>1){printf("%d\n",NF-1);}}' > degreedist/d-ca-coauthors.txt
sort -n degreedist/d-ca-coauthors.txt > degreedist/d-ca-coauthors-s.txt

echo "marknewman-astro"
cat graphs/marknewman-astro.txt | awk -F " " '{if(NR>1){printf("%d\n",NF-1);}}' > degreedist/d-marknewman-astro.txt
sort -n degreedist/d-marknewman-astro.txt > degreedist/d-marknewman-astro-s.txt

echo "marknewman-condmat"
cat graphs/marknewman-condmat.txt | awk -F " " '{if(NR>1){printf("%d\n",NF-1);}}' > degreedist/d-marknewman-condmat.txt
sort -n degreedist/d-marknewman-condmat.txt > degreedist/d-marknewman-condmat-s.txt

echo "dblp-2010"
cat graphs/dblp-2010.txt | awk -F " " '{if(NR>1){printf("%d\n",NF-1);}}' > degreedist/d-dblp-2010.txt
sort -n degreedist/d-dblp-2010.txt > degreedist/d-dblp-2010-s.txt

echo "dblp-2011"
cat graphs/dblp-2011.txt | awk -F " " '{if(NR>1){printf("%d\n",NF-1);}}' > degreedist/d-dblp-2011.txt
sort -n degreedist/d-dblp-2011.txt > degreedist/d-dblp-2011-s.txt

echo "snap-dblp"
cat graphs/snap-dblp.txt | awk -F " " '{if(NR>1){printf("%d\n",NF-1);}}' > degreedist/d-snap-dblp.txt
sort -n degreedist/d-snap-dblp.txt > degreedist/d-snap-dblp-s.txt

echo "snap-amazon"
cat graphs/snap-amazon.txt | awk -F " " '{if(NR>1){printf("%d\n",NF-1);}}' > degreedist/d-snap-amazon.txt
sort -n degreedist/d-snap-amazon.txt > degreedist/d-snap-amazon-s.txt
