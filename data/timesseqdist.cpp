// g++ -std=c++11 frequency.cpp -o frequency -I ~/include -L ~/lib -lsdsl -ldivsufsort -ldivsufsort64 -O3 -DNDEBUG

#include <set>
#include <map>
#include <string>
#include "sys/times.h"
#include <chrono>
#include <vector>
#include <array>
#include <algorithm>
#include <bitset>

#include <sdsl/int_vector.hpp>
#include <sdsl/bit_vectors.hpp>
#include <sdsl/util.hpp>
#include <sdsl/rank_support.hpp>
#include <sdsl/select_support.hpp>
#include <sdsl/suffix_arrays.hpp>


void readCompressed(const std::string path, sdsl::wm_int<sdsl::rrr_vector<15>> &x_wm,
    sdsl::rrr_vector<63> &b1_rrr, sdsl::wt_hutu<sdsl::rrr_vector<15>> &b2_wt,
    sdsl::wm_int<sdsl::rrr_vector<15>> &y_wm)
{
    // Path to sequences
    const std::string xPath = path + ".X.bin-wm_int.sdsl";
    const std::string b1Path = path + ".B1-rrr-64.sdsl";
    const std::string b2Path = path + ".B2.bin-wt_hutu.sdsl";
    const std::string yPath = path + ".Y.bin-wm_int.sdsl";

    // Read compressed files
    load_from_file(x_wm, xPath.c_str());
    load_from_file(b1_rrr, b1Path.c_str());
    load_from_file(b2_wt, b2Path.c_str());
    load_from_file(y_wm, yPath.c_str());

    return;
}

uint32_t totBpn = 0; // total bytes per part
uint32_t totCpp = 0; // total cliques per part
uint32_t totNpp = 0; // total nodes per part
uint32_t maxBpn = 0; // total bytes per part
uint32_t maxCpp = 0; // total cliques per part
uint32_t maxNpp = 0; // total nodes per part
uint32_t totBpn0 = 0; // total parts with 1 clique, bytesPerNode =0
uint32_t naccum0 = 0; // total nodes accum in partitions 1 clique, bytesPerNode =0
uint32_t maxclique0 = 0; // tamano max clique en 1 part bytesPerNode =0
uint32_t minclique0 = 100000; // tamano min clique en 1 part bytesPerNode =0
uint32_t totalparts;

void getSeq(sdsl::wm_int<sdsl::rrr_vector<15>> &x_wm,
    sdsl::rrr_vector<63>::rank_1_type &b1_rank, sdsl::rrr_vector<63>::select_1_type &b1_select,
    std::vector<uint8_t> &b2RAM, std::vector<uint32_t> &yRAM,
    std::map<uint32_t, std::set<uint32_t>> &graph)
{
    // get neighbors by each partition
    //uint64_t maxnode = 0;
    uint32_t b1size = b1_rank.size();
    uint32_t ps = b1_rank(b1size) - 1;
    totalparts = ps;
    uint64_t partitionIndex = 0;
    std::cerr<<" Total Partitions "<<ps<<"\n";
    for (uint64_t partitionNumber = 1; partitionNumber <=ps; ++partitionNumber)
    {
        const uint64_t nextPartitionIndex = b1_select(partitionNumber + 1);
	// current partition indexes are [partitionIndex, nextPartitionIndex) (the same in B1 and X)

        const uint32_t current_Y = yRAM[partitionNumber-1];
        const uint32_t howManyNodesInPartition = nextPartitionIndex - partitionIndex;
        const uint32_t bytesPerNode = (yRAM[partitionNumber] - current_Y)/howManyNodesInPartition;
	//std::cout<<"current_Y "<<current_Y<<" partitionNumber "<<partitionNumber<<" howManyNodesInPartition "<<howManyNodesInPartition<<"\n";
	//std::cout<<"bytesPerNode "<<bytesPerNode<<" partition "<<partitionIndex<<" nextPartitionIndex "<<nextPartitionIndex<<"\n";
	
   	const uint32_t psize = nextPartitionIndex - partitionIndex;
        std::vector<uint64_t> xRAM(psize, 0);
	//std::cout<<" psize "<<psize<<"\n";
        for(uint64_t i = 0; i < psize; ++i)
        {
            xRAM[i] = x_wm[i+partitionIndex];
	    //if(xRAM[i] > maxnode)
	//	maxnode = xRAM[i];
        }
	//std::cout<<"\n after X\n ";

        // If no bytes per node, all nodes are adjacent
        if(0 == bytesPerNode)
        {
	    std::cout<<"nodesPerPartition "<<psize<<" bytesPerNode "<<bytesPerNode<<" cliquesPerPartition "<<1<<"\n";
	    totBpn0++;
	    naccum0 += psize;
	    if(maxclique0 < psize)
		maxclique0 = psize;
	    if(minclique0 > psize)
		minclique0 = psize;
            for (uint64_t xI = 0; xI < psize; xI++)
            {
                    const uint64_t current_node = xRAM[xI];
            	    for (uint64_t cn = xI+1; cn < psize; ++cn)
            	    {
                        const uint64_t adjacentNode = xRAM[cn];
			if(current_node != adjacentNode){
                    		graph[current_node].insert(adjacentNode);
                    		graph[adjacentNode].insert(current_node);
			}
		    }
            }
        } else {
	    uint32_t maxcliquenode = 0;
            for(uint32_t xI1 = partitionIndex; xI1 < nextPartitionIndex; xI1++)
            {
              const uint64_t currentByteIndex = current_Y + bytesPerNode * (xI1 - partitionIndex);
              const uint64_t current_node = xRAM[xI1-partitionIndex];
              for(uint32_t xI = xI1+1; xI < nextPartitionIndex; ++xI)
              {
                const uint32_t b2xIbyteIndex = current_Y + bytesPerNode * (xI - partitionIndex);
                const uint64_t xNeighbor = xRAM[xI-partitionIndex];
		//std::cout<<" vecino "<<xNeighbor<<"\n";
	      	uint32_t cur_ones = 0;
	      	uint32_t cur_next = 0;
	    	for(uint64_t bytesChecked = 0; bytesChecked<bytesPerNode; ++bytesChecked){
              		const uint8_t maskByteOfCurrent = b2RAM[currentByteIndex + bytesChecked];
                	const uint8_t maskBytePossibleNeighbor = b2RAM[b2xIbyteIndex + bytesChecked];
			std::bitset<8> b2_cur(maskByteOfCurrent);
			cur_ones += b2_cur.count();
			std::bitset<8> b2_next(maskBytePossibleNeighbor);
			cur_next += b2_next.count();
			//std::cout<<" verifying byte current "<<currentByteIndex + bytesChecked<<" with second "<<b2xIbyteIndex + bytesChecked<<"\n";

                        if(maskByteOfCurrent & maskBytePossibleNeighbor)
                        {

                            	graph[current_node].insert(xNeighbor);
                            	graph[xNeighbor].insert(current_node);
				//break; this is commented only to count the number ofcliques
			}
		}
		if(maxcliquenode < cur_ones)
			maxcliquenode = cur_ones;
		if(maxcliquenode < cur_next)
			maxcliquenode = cur_next;
	      }
	    }
	    std::cout<<"nodesPerPartition "<<psize<<" bytesPerNode "<<bytesPerNode<<" cliquesPerPartition "<<maxcliquenode<<"\n";
	    totBpn += bytesPerNode;
	    totCpp += maxcliquenode;
	    totNpp += psize;
	    if(maxBpn < bytesPerNode){
		maxBpn = bytesPerNode;
	    }
	    if(maxCpp < maxcliquenode){
		maxCpp = maxcliquenode;
	    }
	    if(maxNpp < psize){
		maxNpp = psize;
	    }
	}
	//}
        /*
	if(bytesPerNode > 0){
		std::cout<<"nodesPerPartition "<<psize<<" bytesPerNode "<<bytesPerNode<<" cliquesPerPartition "<<maxcliquenode<<"\n";
	} else {
		std::cout<<"nodesPerPartition "<<psize<<" bytesPerNode "<<bytesPerNode<<" cliquesPerPartition "<<1<<"\n";
	}
	*/
	partitionIndex = nextPartitionIndex;
    }
    //std::cerr<<"\n maxnode "<<maxnode<<"\n";
}

void getNodeNeighbors(sdsl::wm_int<sdsl::rrr_vector<15>> &x_wm,
    sdsl::rrr_vector<63>::rank_1_type &b1_rank, sdsl::rrr_vector<63>::select_1_type &b1_select,
    std::vector<uint8_t> &b2RAM, std::vector<uint32_t> &yRAM,
    std::map<uint32_t, std::set<uint32_t>> &graph, uint64_t current_node)
{
    const uint32_t howManyX = x_wm.rank(x_wm.size(), current_node);

    //std::cout<<"howManyX "<<howManyX<<"\n";

    for (uint32_t xCount = 1; xCount <= howManyX; ++xCount)
    {
        // std::cerr << "N" << current_node << " ";

        const uint64_t xIndex = x_wm.select(xCount, current_node);
        // std::cerr << "nI" << xIndex << " ";

        uint64_t partitionNumber = b1_rank(xIndex + 1) - 1;
        // std::cerr << "pN " << partitionNumber << " ";

        const uint64_t partitionIndex = b1_select(partitionNumber + 1);
        // std::cerr <<  "pI " << partitionIndex << " ";

        const uint64_t nextPartitionIndex = b1_select(partitionNumber + 2);
        // std::cerr <<  "nPI " << nextPartitionIndex << " ";

        const uint32_t howManyNodesInPartition = nextPartitionIndex - partitionIndex;
        // std::cerr <<  "hMB " << howManyNodesInPartition << " ";

        const uint32_t current_Y = yRAM[partitionNumber];
        // std::cerr <<  "cY " << current_Y << " ";

        const uint32_t bytesPerNode = (yRAM[partitionNumber + 1] - current_Y)/howManyNodesInPartition;
        // std::cerr << "bpn " << bytesPerNode << " ";

        // If no bytes per node, all nodes are adjacent
        if(0 == bytesPerNode)
        {
            for (uint64_t xI = partitionIndex; xI < nextPartitionIndex; ++xI)
            {
                if(xIndex != xI)
                {
                    const uint64_t adjacentNode = x_wm[xI];

                    graph[current_node].insert(adjacentNode);
                    //graph[adjacentNode].insert(current_node);
                }
            }
        }
        else
        {
            const uint64_t currentByteIndex = current_Y + bytesPerNode * (xIndex - partitionIndex);
            // std::cerr << "cBi " << currentByteIndex << " ";

            std::vector<bool> neighbors(nextPartitionIndex - partitionIndex, 0);
            neighbors[xIndex - partitionIndex] = 1;

            // std::cerr << "xI ";
            uint32_t bytesChecked = 0;
            while(bytesChecked != bytesPerNode)
            {
                const uint8_t maskByteOfCurrent = b2RAM[currentByteIndex + bytesChecked];

                for(uint32_t xI = partitionIndex; xI < nextPartitionIndex; ++xI)
                {
                    if(!neighbors[xI - partitionIndex])
                    {
                        // std::cerr << xI << " ";

                        const uint32_t b2xIbyteIndex = current_Y + bytesPerNode * (xI - partitionIndex);
			// std::cerr << " " << b2xIbyteIndex

                        const uint8_t maskBytePossibleNeighbor = b2RAM[b2xIbyteIndex + bytesChecked];

                        if(maskByteOfCurrent & maskBytePossibleNeighbor)
                        {
                            neighbors[xI - partitionIndex] = 1;

                            const uint64_t xNeighbor = x_wm[xI];

                            graph[current_node].insert(xNeighbor);
                            //graph[xNeighbor].insert(current_node);
                        }
                    }
                }

                ++bytesChecked;
            }

        }

        // std::cerr << std::endl;
    }
    // std::cerr << std::endl;

    return ;
}


void reconstructGraph(sdsl::wm_int<sdsl::rrr_vector<15>> &x_wm,
    sdsl::rrr_vector<63> &b1_rrr, sdsl::wt_hutu<sdsl::rrr_vector<15>> &b2_wt,
    sdsl::wm_int<sdsl::rrr_vector<15>> &y_wm, std::map<uint32_t, std::set<uint32_t>> &graph,
    uint64_t &totalNodes, uint8_t &random, uint32_t querynode)
{
    sdsl::rrr_vector<63>::rank_1_type b1_rank(&b1_rrr);
    sdsl::rrr_vector<63>::select_1_type b1_select(&b1_rrr);

    std::vector<uint8_t> b2RAM(b2_wt.size(), 0);
    for(uint64_t i = 0; i < b2_wt.size(); ++i)
    {
        b2RAM[i] = b2_wt[i];
    }

    std::vector<uint32_t> yRAM(y_wm.size(), 0);
    for(uint64_t i = 0; i < y_wm.size(); ++i)
    {
        yRAM[i] = y_wm[i];
    }
    std::cerr << std::endl;

    if(random)
    {
        std::vector<bool> nodesDone(totalNodes, 0);
        uint64_t doneNodesCount = 0;

        srand(time(NULL));

        while(doneNodesCount < totalNodes)
        {
            uint64_t random_node = rand() % totalNodes;
            if(nodesDone[random_node])
            {
                continue;
            }

            nodesDone[random_node] = 1;

            getNodeNeighbors(x_wm, b1_rank, b1_select, b2RAM, yRAM, graph, random_node);

            ++doneNodesCount;
        }
    }
    else
    {
        getSeq(x_wm, b1_rank, b1_select, b2RAM, yRAM, graph);
    }

    return;
}


int main(int argc, char const *argv[])
{
    if(4 > argc)
    {
        std::cerr << "Modo de uso: " << argv[0] << " RUTA_BASE NODES (0:ORDERNADO/1:ALEATORIO) querynode" << std::endl;
        return -1;
    }

    const std::string path(argv[1]);
    uint64_t totalNodes = atoi(argv[2]);
    uint8_t random = atoi(argv[3]);

    //const uint8_t iterations = argv[4] ? atoi(argv[4]) : 1;
    const uint8_t iterations = argv[5] ? atoi(argv[5]) : 1;
    uint32_t querynode = atoi(argv[4]);
    //std::cout<<"querynode "<<querynode<<"\n";

    // Variables to read compressed sequences
    sdsl::wm_int<sdsl::rrr_vector<15>> x_wm;
    sdsl::rrr_vector<63> b1_rrr;
    sdsl::wt_hutu<sdsl::rrr_vector<15>> b2_wt;
    sdsl::wm_int<sdsl::rrr_vector<15>> y_wm;

    // std::map<uint32_t, std::set<uint32_t>> xOnRAM;

    // Read compressed sequences
    readCompressed(path, x_wm, b1_rrr, b2_wt, y_wm);

    std::map<uint32_t, std::set<uint32_t>> graph;

    for(uint8_t i = 1; i <= iterations; ++i)
    {
        graph.clear();

        std::chrono::high_resolution_clock::time_point start_time = std::chrono::high_resolution_clock::now();

        reconstructGraph(x_wm, b1_rrr, b2_wt, y_wm, graph, totalNodes, random, querynode);

        std::chrono::high_resolution_clock::time_point stop_time = std::chrono::high_resolution_clock::now();

        auto duration = std::chrono::duration_cast<std::chrono::milliseconds> (stop_time - start_time).count();

        std::cerr << "Time Reconstruction " << i << ": " << duration << " [ms]" << std::endl;
    }

    std::cout << graph.size() << std::endl;
    uint64_t nodeIndex = 0;
    if(querynode != 0){
      for(const auto & pair : graph)
      {
        std::cout << pair.first << ": ";
	
	std::set<uint32_t> v = pair.second;
	//std::sort(v.begin(), v.end());

    	//for(const auto & node : pair.second)
    	for(const auto & node : v)
        {
            std::cout << node << " ";
        }

        ++nodeIndex;
        std::cout << std::endl;
      }
    }

    std::cout<<"TOTALParts "<<totalparts<<"\n";
    std::cout<<"TOTALN totBpn "<<totBpn<<" maxBpn "<<maxBpn<<" totCpp "<<totCpp<<" maxCpp "<<maxCpp<<" totNpp "<<totNpp<<" maxNpp "<<maxNpp<<"\n";
    std::cout<<"AVG bpn "<<totBpn*1.0/totalparts<<" cpp "<<totCpp*1.0/totalparts<<" npp "<<totNpp*1.0/totalparts<<"\n";
    std::cout<<"TOTAL0 totBpn0(num cliques part 1) "<<totBpn0<<" maxBpn0 "<<0<<" totCpp0 "<<1<<" maxCpp "<<1<<" totNpp "<<naccum0<<" maxNodesClique "<<maxclique0<<" minNodesClique "<<minclique0<<"\n";
    std::cout<<"AVG0 total nodes in cliques en 1 part "<<naccum0*1.0/totBpn0<<"\n";



    return 0;
}
