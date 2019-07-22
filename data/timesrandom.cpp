// g++ -std=c++11 frequency.cpp -o frequency -I ~/include -L ~/lib -lsdsl -ldivsufsort -ldivsufsort64 -O3 -DNDEBUG

#include <set>
#include <map>
#include <string>
#include "sys/times.h"
#include <chrono>
#include <vector>
#include <array>
#include <stdio.h>
#include <stdlib.h>

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


//void getNodeNeighbors(sdsl::wm_int<sdsl::rrr_vector<15>> &x_wm,
//    sdsl::rrr_vector<63>::rank_1_type &b1_rank, sdsl::rrr_vector<63>::select_1_type &b1_select,
//    sdsl::wt_hutu<sdsl::rrr_vector<15>> &b2_wt, sdsl::wm_int<sdsl::rrr_vector<15>> &yRAM,
//    std::map<uint32_t, std::set<uint32_t>> &graph, uint64_t &current_node)
void getNodeNeighbors(sdsl::wm_int<sdsl::rrr_vector<15>> &x_wm,
    sdsl::rrr_vector<63>::rank_1_type &b1_rank, sdsl::rrr_vector<63>::select_1_type &b1_select,
    sdsl::wt_hutu<sdsl::rrr_vector<15>> &b2_wt, sdsl::wm_int<sdsl::rrr_vector<15>> &yRAM,
    std::set<uint32_t> &neighs, uint32_t &current_node)
{
    const uint32_t howManyX = x_wm.rank(x_wm.size(), current_node);

    for (uint32_t xCount = 1; xCount <= howManyX; ++xCount)
    {
        // std::cerr << current_node << " " << howManyX << "; ";

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
        const uint32_t nextp_Y = yRAM[partitionNumber+1];
        // std::cerr <<  "cY " << current_Y << " ";

        //const uint32_t bytesPerNode = (yRAM[partitionNumber + 1] - current_Y)/howManyNodesInPartition;
        const uint32_t bytesPerNode = (nextp_Y - current_Y)/howManyNodesInPartition;
        // std::cerr << "bpn " << bytesPerNode << " ";

        // If no bytes per node, all nodes are adjacent
        if(0 == bytesPerNode)
        {
            for (uint64_t xI = partitionIndex; xI < nextPartitionIndex; ++xI)
            {
                if(xIndex != xI)
                {
                    //const uint32_t adjacentNode = x_wm[xI];
                    //graph[current_node].insert(adjacentNode);
		    neighs.insert(x_wm[xI]);
                }
            }
        }
        else
        {
		uint32_t numb2 = nextp_Y-current_Y;
	        std::vector<uint8_t> b2RAM(numb2, 0);
		for(uint64_t ii = 0 ; ii < numb2; ++ii)
    		{
        		b2RAM[ii] = b2_wt[ii+current_Y];
    		}


            const uint64_t currentByteIndex = current_Y + bytesPerNode * (xIndex - partitionIndex);
            //const uint64_t currentByteIndex = bytesPerNode * (xIndex - partitionIndex);
            // std::cerr << "cBi " << currentByteIndex << " ";

            std::vector<bool> neighbors(nextPartitionIndex - partitionIndex, 0);
            neighbors[xIndex - partitionIndex] = 1;

            // std::cerr << "xI ";
            uint32_t bytesChecked = 0;
            while(bytesChecked != bytesPerNode)
            {
                //const uint8_t maskByteOfCurrent = b2RAM[currentByteIndex + bytesChecked];
                const uint8_t maskByteOfCurrent = b2RAM[currentByteIndex + bytesChecked-current_Y];

                for(uint32_t xI = partitionIndex; xI < nextPartitionIndex; ++xI)
                {
                    if(!neighbors[xI - partitionIndex])
                    {
                        // std::cerr << xI << " ";

                        const uint32_t b2xIbyteIndex = current_Y + bytesPerNode * (xI - partitionIndex);
                        //const uint32_t b2xIbyteIndex = bytesPerNode * (xI - partitionIndex);
			// std::cerr << " " << b2xIbyteIndex

                        //const uint8_t maskBytePossibleNeighbor = b2RAM[b2xIbyteIndex + bytesChecked];
                        const uint8_t maskBytePossibleNeighbor = b2RAM[b2xIbyteIndex + bytesChecked-current_Y];

                        if(maskByteOfCurrent & maskBytePossibleNeighbor)
                        {
                            neighbors[xI - partitionIndex] = 1;

                            //const uint32_t xNeighbor = x_wm[xI];
                            //graph[current_node].insert(xNeighbor);
			    neighs.insert(x_wm[xI]);
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


int main(int argc, char const *argv[])
{
    if(3 > argc)
    {
        std::cerr << "Modo de uso: " << argv[0] << " RUTA_BASE QueryFile.bin iterations" << std::endl;
        return -1;
    }

    const std::string path(argv[1]);
    
    const uint8_t iterations = argv[3] ? atoi(argv[3]) : 1;

    // Variables to read compressed sequences
    sdsl::wm_int<sdsl::rrr_vector<15>> x_wm;
    sdsl::rrr_vector<63> b1_rrr;
    sdsl::wt_hutu<sdsl::rrr_vector<15>> b2_wt;
    sdsl::wm_int<sdsl::rrr_vector<15>> y_wm;

    // std::map<uint32_t, std::set<uint32_t>> xOnRAM;

    // Read compressed sequences
    readCompressed(path, x_wm, b1_rrr, b2_wt, y_wm);
    sdsl::rrr_vector<63>::rank_1_type b1_rank(&b1_rrr);
    sdsl::rrr_vector<63>::select_1_type b1_select(&b1_rrr);

    std::map<uint32_t, std::set<uint32_t>> graph;
    //char * list_file = argv[2];
    FILE * list_fp = fopen(argv[2],"r");
    uint queries;
    fread(&queries, sizeof(uint), 1, list_fp);
    ulong recovered = 0;
    double t = 0;
    uint32_t *qry = (uint32_t *) malloc(sizeof(uint32_t)*queries);
    fread(qry,sizeof(uint),queries,list_fp);
    std::cerr<<"Processing "<<queries<<" queries\n";

    for(uint8_t k = 1; k <= iterations; ++k)
    {
        //graph.clear();

        //std::chrono::high_resolution_clock::time_point start_time = std::chrono::high_resolution_clock::now();

        //reconstructGraph(x_wm, b1_rrr, b2_wt, y_wm, graph, totalNodes, random);

        std::chrono::high_resolution_clock::time_point start_time = std::chrono::high_resolution_clock::now();
  	for(uint32_t i=0;i<queries;i++) {
    		//uint *l  = compactTreeAdjacencyList(trep, qry[i]);
    		//recovered += l[0];
		std::set<uint32_t> neighs;
                getNodeNeighbors(x_wm, b1_rank, b1_select, b2_wt, y_wm, neighs, qry[i]);
    		recovered += neighs.size();
  	}
        std::chrono::high_resolution_clock::time_point stop_time = std::chrono::high_resolution_clock::now();

        auto duration = std::chrono::duration_cast<std::chrono::milliseconds> (stop_time - start_time).count();

        std::cerr <<"total time iter "<<k<<" : " << duration << " [ms]" << " \n";
        std::cerr <<"total queries "<<queries << " \n";
        std::cerr <<"recovered edges "<<recovered<<" time per link "<<1.0*duration/recovered<< std::endl;
        std::cerr <<"time per query "<<1.0*duration/queries << " \n";
    }

    std::cout << graph.size() << std::endl;
    uint64_t nodeIndex = 0;
    for(const auto & pair : graph)
    {
        std::cout << pair.first << ": ";
/*
    	while(pair.first != nodeIndex)
        {
            std::cout << std::endl;
    	    ++nodeIndex;
    	}
*/

    	for(const auto & node : pair.second)
        {
            std::cout << node << " ";
        }

        ++nodeIndex;
        std::cout << std::endl;
    }



    return 0;
}
