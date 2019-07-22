// g++ -std=c++11 frequency.cpp -o frequency -I ~/include -L ~/lib -lsdsl -ldivsufsort -ldivsufsort64 -O3 -DNDEBUG

#include <set>
#include <map>
#include <string>
#include "sys/times.h"
#include <chrono>
#include <vector>
#include <array>
#include <algorithm>
#include <immintrin.h>  // AVX intrinsics

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


void getNodeNeighbors(sdsl::wm_int<sdsl::rrr_vector<15>> &x_wm,
    sdsl::rrr_vector<63>::rank_1_type &b1_rank, sdsl::rrr_vector<63>::select_1_type &b1_select,
    //std::vector<uint8_t> &b2RAM, std::vector<uint32_t> &yRAM,
    sdsl::wt_hutu<sdsl::rrr_vector<15>> &b2_wt, sdsl::wm_int<sdsl::rrr_vector<15>> &yRAM,
    std::map<uint32_t, std::set<uint32_t>> &graph, uint64_t current_node)
{
    const uint32_t howManyX = x_wm.rank(x_wm.size(), current_node);

    //std::cout<<"current_node"<<current_node<<" howManyX "<<howManyX<<"\n";

    #pragma omp parallel for
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

        //const uint32_t bytesPerNode = (yRAM[partitionNumber + 1] - current_Y)/howManyNodesInPartition;
        // std::cerr << "bpn " << bytesPerNode << " ";
        //const uint32_t current_Y = yRAM[partitionNumber];
        const uint32_t nextp_Y = yRAM[partitionNumber+1];
        // std::cerr <<  "cY " << current_Y << " ";

        //const uint32_t bytesPerNode = (yRAM[partitionNumber + 1] - current_Y)/howManyNodesInPartition;
        const uint32_t bytesPerNode = (nextp_Y - current_Y)/howManyNodesInPartition;

        // If no bytes per node, all nodes are adjacent
        if(0 == bytesPerNode)
        {
            for (uint64_t xI = partitionIndex; xI < nextPartitionIndex; ++xI)
            {
                if(xIndex != xI)
                {
                    const uint64_t adjacentNode = x_wm[xI];
                    //graph[current_node].insert(adjacentNode);
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

            //const uint64_t currentByteIndex = current_Y + bytesPerNode * (xIndex - partitionIndex);
            const uint64_t currentByteIndex = bytesPerNode * (xIndex - partitionIndex);
            for(uint32_t xI = partitionIndex; xI < nextPartitionIndex; ++xI){
	      //if(xI == xIndex)continue;
                 //const uint32_t b2xIbyteIndex = current_Y + bytesPerNode * (xI - partitionIndex);
                 const uint32_t b2xIbyteIndex = bytesPerNode * (xI - partitionIndex);
                 int32_t xNeighbor = -1;
                 for(uint32_t bytesChecked = 0; bytesChecked<bytesPerNode; ++bytesChecked){
                      const uint8_t maskByteOfCurrent = b2RAM[currentByteIndex + bytesChecked];
                      const uint8_t maskBytePossibleNeighbor = b2RAM[b2xIbyteIndex + bytesChecked];

                      if(maskByteOfCurrent & maskBytePossibleNeighbor)
                      {
                 	 xNeighbor = x_wm[xI];
			 //if(current_node != xNeighbor)
                         //   graph[current_node].insert(xNeighbor);
                         break;
                      }
                 }
	    }
	    
        } // del if bypesPerNode > 0

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

/*
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

    std::vector<uint32_t> xRAM(x_wm.size(), 0);
    for(uint64_t i = 0; i < x_wm.size(); ++i)
    {
        xRAM[i] = x_wm[i];
    }
*/

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

            //getNodeNeighbors(x_wm, b1_rank, b1_select, b2RAM, yRAM, graph, random_node);

            ++doneNodesCount;
        }
    }
    else
    {
        for (uint64_t ordered_node = 0; ordered_node < totalNodes; ++ordered_node)
        {
            //getNodeNeighbors(xRAM, x_wm, b1_rank, b1_select, b2RAM, yRAM, graph, ordered_node);
            getNodeNeighbors(x_wm, b1_rank, b1_select, b2_wt, y_wm, graph, ordered_node);
        }
	/*
	for(uint32_t ir=0;ir<querynode; ir++){
		uint32_t q = rand()%totalNodes;	
        	getNodeNeighbors(x_wm, b1_rank, b1_select, b2RAM, yRAM, graph, q);
	}
	*/
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
    std::cout<<"totalNodes "<<totalNodes<<" querynode "<<querynode<<" iters "<<iterations<<"\n";

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

    return 0;
}
