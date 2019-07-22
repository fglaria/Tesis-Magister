// g++ -std=c++11 testingSDSL.cpp -o testingSDSL -I ~/include -L ~/lib -lsdsl -ldivsufsort -ldivsufsort64 -O3 -DNDEBUG -fopenmp

#include <set>
#include <map>
#include <unordered_map>
#include <string>
#include "sys/times.h"
#include <chrono>
#include <vector>
#include <array>
#include <algorithm>
#include <omp.h>

#include <sdsl/int_vector.hpp>
#include <sdsl/bit_vectors.hpp>
#include <sdsl/util.hpp>
#include <sdsl/rank_support.hpp>
#include <sdsl/select_support.hpp>
#include <sdsl/suffix_arrays.hpp>

void readCompressed(const std::string path,
    sdsl::wm_int<sdsl::rrr_vector<15>> &x_wm,
    sdsl::wt_int<sdsl::rrr_vector<15>> &x_wt,
    sdsl::rrr_vector<63> &b1_rrr,
    sdsl::sd_vector<> &b1_sdb,
    sdsl::wt_hutu<sdsl::rrr_vector<15>> &b2_hutu,
    sdsl::wt_huff<sdsl::rrr_vector<15>> &b2_huff,
    sdsl::wt_blcd<sdsl::rrr_vector<15>> &b2_blcd,
    sdsl::wm_int<sdsl::rrr_vector<15>> &y_wm,
    sdsl::wt_int<sdsl::rrr_vector<15>> &y_wt
    )
{
    // Read compressed files
    load_from_file(x_wm, path + ".X.bin-wm_int.sdsl");
    load_from_file(x_wt, path + ".X.bin-wt_int.sdsl");
    load_from_file(b1_rrr, path + ".B1-rrr-64.sdsl");
    load_from_file(b1_sdb, path + ".B1-sdb.sdsl");
    load_from_file(b2_hutu, path + ".B2.bin-wt_hutu.sdsl");
    load_from_file(b2_huff, path + ".B2.bin-wt_huff.sdsl");
    load_from_file(b2_blcd, path + ".B2.bin-wt_blcd.sdsl");
    load_from_file(y_wm, path + ".Y.bin-wm_int.sdsl");
    load_from_file(y_wt, path + ".Y.bin-wt_int.sdsl");

    return;
}

template<class X, class Br, class Bs, class BB, class Y>
void getSeq(X &x_wm, Br &b1_rank, Bs &b1_select, BB &b2_wt, Y &yRAM,
    std::map<uint32_t, std::set<uint32_t>> &graph, uint32_t nthreads)
{
    // get neighbors by each partition
    uint32_t b1size = b1_rank.size();
    uint32_t ps = b1_rank(b1size) - 1;
    //uint64_t partitionIndex = 0;
    // std::cerr<<" Total Partitions "<<ps<<"\n";
    //int nthreads = 4;
    omp_set_num_threads(nthreads);
    int tid;
    std::vector< std::unordered_map<uint32_t, std::set<uint32_t> > > pg;

    std::unordered_map< uint32_t, std::set<uint32_t> > gx[nthreads];

    for(uint32_t i=0; i<nthreads; i++)
    {
        pg.push_back(gx[i]);
    }

    //#pragma omp parallel for private(tid,nthreads) shared(pg) schedule(static,10000)
    #pragma omp parallel for private(tid,nthreads) shared(pg) schedule(guided)
    for (uint64_t partitionNumber = 1; partitionNumber <=ps; ++partitionNumber)
    {
        uint64_t partitionIndex = b1_select(partitionNumber);
        tid = omp_get_thread_num();
        //std::cout<<" tid "<<tid<<"\n";

        //std::unordered_map<uint32_t, std::set<uint32_t> > privg = pg[tid];
        //std::unordered_map<uint32_t, std::set<uint32_t> > privg;
        const uint64_t nextPartitionIndex = b1_select(partitionNumber + 1);
        // current partition indexes are [partitionIndex, nextPartitionIndex) (the same in B1 and X)

        const uint32_t current_Y = yRAM[partitionNumber-1];
        const uint32_t howManyNodesInPartition = nextPartitionIndex - partitionIndex;
        //const uint32_t bytesPerNode = (yRAM[partitionNumber] - current_Y)/howManyNodesInPartition;

        //const uint32_t current_Y = yRAM[partitionNumber];
        //const uint32_t nextp_Y = yRAM[partitionNumber+1];
        const uint32_t nextp_Y = yRAM[partitionNumber];

        const uint32_t bytesPerNode = (nextp_Y - current_Y)/howManyNodesInPartition;

        const uint32_t psize = nextPartitionIndex - partitionIndex;
        std::vector<uint64_t> xRAM(psize, 0);
        //std::cout<<" psize "<<psize<<"\n";
        for(uint64_t i = 0; i < psize; ++i)
        {
            xRAM[i] = x_wm[i+partitionIndex];
        }
        //std::cout<<"\n after X\n ";

        // If no bytes per node, all nodes are adjacent
        if(0 == bytesPerNode)
        {
            for (uint64_t xI = 0; xI < psize; xI++)
            {
                const uint64_t current_node = xRAM[xI];
                for (uint64_t cn = xI+1; cn < psize; ++cn)
                {
                    const uint64_t adjacentNode = xRAM[cn];
                    if(current_node != adjacentNode)
                    {
                        //privg[current_node].insert(adjacentNode);
                        //privg[adjacentNode].insert(current_node);
                        (pg[tid])[current_node].insert(adjacentNode);
                        (pg[tid])[adjacentNode].insert(current_node);
                    }
                }
            }
        } else {

            uint32_t numb2 = nextp_Y-current_Y;
            std::vector<uint8_t> b2RAM(numb2, 0);
            for(uint64_t ii = 0 ; ii < numb2; ++ii)
            {
                b2RAM[ii] = b2_wt[ii+current_Y];
            }

            for(uint32_t xI1 = partitionIndex; xI1 < nextPartitionIndex; xI1++)
            {
                //const uint64_t currentByteIndex = current_Y + bytesPerNode * (xI1 - partitionIndex);
                const uint64_t currentByteIndex = bytesPerNode * (xI1 - partitionIndex);
                const uint64_t current_node = xRAM[xI1-partitionIndex];
                //std::cout<<" current_node "<<current_node<<" at "<<xI1-partitionIndex<<"\n";
                //std::cout<<" currentByteIndex "<<currentByteIndex<<"\n";
                //for(uint32_t xI = partitionIndex+xI1+1; xI < nextPartitionIndex; ++xI)
                for(uint32_t xI = xI1+1; xI < nextPartitionIndex; ++xI)
                {
                    //const uint32_t b2xIbyteIndex = current_Y + bytesPerNode * (xI - partitionIndex);
                    const uint32_t b2xIbyteIndex = bytesPerNode * (xI - partitionIndex);
                    const uint64_t xNeighbor = xRAM[xI-partitionIndex];
                    for(uint64_t bytesChecked = 0; bytesChecked<bytesPerNode; ++bytesChecked)
                    {
                        const uint8_t maskByteOfCurrent = b2RAM[currentByteIndex + bytesChecked];
                        const uint8_t maskBytePossibleNeighbor = b2RAM[b2xIbyteIndex + bytesChecked];
                        //std::cout<<" verifying byte current "<<currentByteIndex + bytesChecked<<" with second "<<b2xIbyteIndex + bytesChecked<<"\n";

                        if(maskByteOfCurrent & maskBytePossibleNeighbor)
                        {
                            //privg[current_node].insert(xNeighbor);
                            //privg[xNeighbor].insert(current_node);
                            (pg[tid])[current_node].insert(xNeighbor);
                            (pg[tid])[xNeighbor].insert(current_node);
                            break;
                        }
                    }
                }
            }
        }
        //pg[tid] = privg;
        //partitionIndex = nextPartitionIndex;
        //std::cout<<" tid "<<tid<<" partitionNumber "<<partitionNumber<<"\n";
    }

    std::unordered_map<uint32_t, std::set<uint32_t> >::iterator mm;
    for(uint32_t i=0; i<nthreads; i++)
    {
        std::unordered_map<uint32_t, std::set<uint32_t> > gg = pg[i];
        for(mm=gg.begin(); mm!=gg.end(); mm++){
            std::set<uint32_t> ss = mm->second;
            graph[mm->first].insert(ss.begin(), ss.end());
        }
    }
}

template<class X, class B, class BB, class Y>
void reconstructGraph(X &x_wm, B &b1_rrr, BB &b2_wt, Y &y_wm,
    std::map<uint32_t, std::set<uint32_t>> &graph, uint64_t &totalNodes, uint8_t &random, uint32_t nthreads)
{
    class B::rank_1_type b1_rank(&b1_rrr);
    class B::select_1_type b1_select(&b1_rrr);

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
    //std::cout<<" before getSeq\n";
        //getSeq(x_wm, b1_rank, b1_select, b2RAM, yRAM, graph);
        getSeq
            <X, class B::rank_1_type, class B::select_1_type, BB, Y>
            (x_wm, b1_rank, b1_select, b2_wt, y_wm, graph, nthreads);
    }

    return;
}


int main(int argc, char const *argv[])
{
    if(4 > argc)
    {
        std::cerr << "Modo de uso: " << argv[0] << " RUTA_BASE NODES (0:ORDERNADO/1:ALEATORIO) nthreads" << std::endl;
        return -1;
    }

    const std::string path(argv[1]);
    uint64_t totalNodes = atoi(argv[2]);
    uint8_t random = atoi(argv[3]);

    uint32_t nthreads = argv[4] ? atoi(argv[4]) : 1;

    // Variables to read compressed sequences
    sdsl::wm_int<sdsl::rrr_vector<15>> x_wm;
    sdsl::wt_int<sdsl::rrr_vector<15>> x_wt;

    sdsl::rrr_vector<63> b1_rrr;
    sdsl::sd_vector<> b1_sdb;

    sdsl::wt_hutu<sdsl::rrr_vector<15>> b2_hutu;
    sdsl::wt_huff<sdsl::rrr_vector<15>> b2_huff;
    sdsl::wt_blcd<sdsl::rrr_vector<15>> b2_blcd;

    sdsl::wm_int<sdsl::rrr_vector<15>> y_wm;
    sdsl::wt_int<sdsl::rrr_vector<15>> y_wt;

    readCompressed(path, x_wm, x_wt, b1_rrr, b1_sdb, b2_hutu, b2_huff, b2_blcd, y_wm, y_wt);

    std::map<uint32_t, std::set<uint32_t>> graph;

    graph.clear();

    std::chrono::high_resolution_clock::time_point start_time, stop_time;



    start_time = std::chrono::high_resolution_clock::now();

    reconstructGraph
        <sdsl::wm_int<sdsl::rrr_vector<15>>, sdsl::rrr_vector<63>, sdsl::wt_hutu<sdsl::rrr_vector<15>>, sdsl::wm_int<sdsl::rrr_vector<15>>>
        (x_wm, b1_rrr, b2_hutu, y_wm, graph, totalNodes, random, nthreads);

    stop_time = std::chrono::high_resolution_clock::now();

    auto duration = std::chrono::duration_cast<std::chrono::milliseconds> (stop_time - start_time).count();

    std::cerr << "x_wm b_rrr bb_hutu y_wm: " << duration << " [ms]; V: " << graph.size() << std::endl;


    graph.clear();
    start_time = std::chrono::high_resolution_clock::now();

    reconstructGraph
        <sdsl::wt_int<sdsl::rrr_vector<15>>, sdsl::rrr_vector<63>, sdsl::wt_hutu<sdsl::rrr_vector<15>>, sdsl::wt_int<sdsl::rrr_vector<15>>>
        (x_wt, b1_rrr, b2_hutu, y_wt, graph, totalNodes, random, nthreads);

    stop_time = std::chrono::high_resolution_clock::now();
    duration = std::chrono::duration_cast<std::chrono::milliseconds> (stop_time - start_time).count();

    std::cerr << "x_wt b_rrr bb_hutu y_wt: " << duration << " [ms]; V: " << graph.size() << std::endl;


    graph.clear();
    start_time = std::chrono::high_resolution_clock::now();

    reconstructGraph
        <sdsl::wm_int<sdsl::rrr_vector<15>>, sdsl::rrr_vector<63>, sdsl::wt_huff<sdsl::rrr_vector<15>>, sdsl::wm_int<sdsl::rrr_vector<15>>>
        (x_wm, b1_rrr, b2_huff, y_wm, graph, totalNodes, random, nthreads);

    stop_time = std::chrono::high_resolution_clock::now();
    duration = std::chrono::duration_cast<std::chrono::milliseconds> (stop_time - start_time).count();

    std::cerr << "x_wm b_rrr bb_huff y_wm: " << duration << " [ms]; V: " << graph.size() << std::endl;


    graph.clear();
    start_time = std::chrono::high_resolution_clock::now();

    reconstructGraph
        <sdsl::wt_int<sdsl::rrr_vector<15>>, sdsl::rrr_vector<63>, sdsl::wt_huff<sdsl::rrr_vector<15>>, sdsl::wt_int<sdsl::rrr_vector<15>>>
        (x_wt, b1_rrr, b2_huff, y_wt, graph, totalNodes, random, nthreads);

    stop_time = std::chrono::high_resolution_clock::now();
    duration = std::chrono::duration_cast<std::chrono::milliseconds> (stop_time - start_time).count();

    std::cerr << "x_wt b_rrr bb_huff y_wt: " << duration << " [ms]; V: " << graph.size() << std::endl;


    graph.clear();
    start_time = std::chrono::high_resolution_clock::now();

    reconstructGraph
        <sdsl::wm_int<sdsl::rrr_vector<15>>, sdsl::rrr_vector<63>, sdsl::wt_blcd<sdsl::rrr_vector<15>>, sdsl::wm_int<sdsl::rrr_vector<15>>>
        (x_wm, b1_rrr, b2_blcd, y_wm, graph, totalNodes, random, nthreads);

    stop_time = std::chrono::high_resolution_clock::now();
    duration = std::chrono::duration_cast<std::chrono::milliseconds> (stop_time - start_time).count();

    std::cerr << "x_wm b_rrr bb_blcd y_wm: " << duration << " [ms]; V: " << graph.size() << std::endl;


    graph.clear();
    start_time = std::chrono::high_resolution_clock::now();

    reconstructGraph
        <sdsl::wt_int<sdsl::rrr_vector<15>>, sdsl::rrr_vector<63>, sdsl::wt_blcd<sdsl::rrr_vector<15>>, sdsl::wt_int<sdsl::rrr_vector<15>>>
        (x_wt, b1_rrr, b2_blcd, y_wt, graph, totalNodes, random, nthreads);

    stop_time = std::chrono::high_resolution_clock::now();
    duration = std::chrono::duration_cast<std::chrono::milliseconds> (stop_time - start_time).count();

    std::cerr << "x_wt b_rrr bb_blcd y_wt: " << duration << " [ms]; V: " << graph.size() << std::endl;



    // SDB
    start_time = std::chrono::high_resolution_clock::now();

    reconstructGraph
        <sdsl::wm_int<sdsl::rrr_vector<15>>, sdsl::sd_vector<>, sdsl::wt_hutu<sdsl::rrr_vector<15>>, sdsl::wm_int<sdsl::rrr_vector<15>>>
        (x_wm, b1_sdb, b2_hutu, y_wm, graph, totalNodes, random, nthreads);

    stop_time = std::chrono::high_resolution_clock::now();

    duration = std::chrono::duration_cast<std::chrono::milliseconds> (stop_time - start_time).count();

    std::cerr << "x_wm b_sdb bb_hutu y_wm: " << duration << " [ms]; V: " << graph.size() << std::endl;


    graph.clear();
    start_time = std::chrono::high_resolution_clock::now();

    reconstructGraph
        <sdsl::wt_int<sdsl::rrr_vector<15>>, sdsl::sd_vector<>, sdsl::wt_hutu<sdsl::rrr_vector<15>>, sdsl::wt_int<sdsl::rrr_vector<15>>>
        (x_wt, b1_sdb, b2_hutu, y_wt, graph, totalNodes, random, nthreads);

    stop_time = std::chrono::high_resolution_clock::now();
    duration = std::chrono::duration_cast<std::chrono::milliseconds> (stop_time - start_time).count();

    std::cerr << "x_wt b_sdb bb_hutu y_wt: " << duration << " [ms]; V: " << graph.size() << std::endl;


    graph.clear();
    start_time = std::chrono::high_resolution_clock::now();

    reconstructGraph
        <sdsl::wm_int<sdsl::rrr_vector<15>>, sdsl::sd_vector<>, sdsl::wt_huff<sdsl::rrr_vector<15>>, sdsl::wm_int<sdsl::rrr_vector<15>>>
        (x_wm, b1_sdb, b2_huff, y_wm, graph, totalNodes, random, nthreads);

    stop_time = std::chrono::high_resolution_clock::now();
    duration = std::chrono::duration_cast<std::chrono::milliseconds> (stop_time - start_time).count();

    std::cerr << "x_wm b_sdb bb_huff y_wm: " << duration << " [ms]; V: " << graph.size() << std::endl;


    graph.clear();
    start_time = std::chrono::high_resolution_clock::now();

    reconstructGraph
        <sdsl::wt_int<sdsl::rrr_vector<15>>, sdsl::sd_vector<>, sdsl::wt_huff<sdsl::rrr_vector<15>>, sdsl::wt_int<sdsl::rrr_vector<15>>>
        (x_wt, b1_sdb, b2_huff, y_wt, graph, totalNodes, random, nthreads);

    stop_time = std::chrono::high_resolution_clock::now();
    duration = std::chrono::duration_cast<std::chrono::milliseconds> (stop_time - start_time).count();

    std::cerr << "x_wt b_sdb bb_huff y_wt: " << duration << " [ms]; V: " << graph.size() << std::endl;


    graph.clear();
    start_time = std::chrono::high_resolution_clock::now();

    reconstructGraph
        <sdsl::wm_int<sdsl::rrr_vector<15>>, sdsl::sd_vector<>, sdsl::wt_blcd<sdsl::rrr_vector<15>>, sdsl::wm_int<sdsl::rrr_vector<15>>>
        (x_wm, b1_sdb, b2_blcd, y_wm, graph, totalNodes, random, nthreads);

    stop_time = std::chrono::high_resolution_clock::now();
    duration = std::chrono::duration_cast<std::chrono::milliseconds> (stop_time - start_time).count();

    std::cerr << "x_wm b_sdb bb_blcd y_wm: " << duration << " [ms]; V: " << graph.size() << std::endl;


    graph.clear();
    start_time = std::chrono::high_resolution_clock::now();

    reconstructGraph
        <sdsl::wt_int<sdsl::rrr_vector<15>>, sdsl::sd_vector<>, sdsl::wt_blcd<sdsl::rrr_vector<15>>, sdsl::wt_int<sdsl::rrr_vector<15>>>
        (x_wt, b1_sdb, b2_blcd, y_wt, graph, totalNodes, random, nthreads);

    stop_time = std::chrono::high_resolution_clock::now();
    duration = std::chrono::duration_cast<std::chrono::milliseconds> (stop_time - start_time).count();

    std::cerr << "x_wt b_sdb bb_blcd y_wt: " << duration << " [ms]; V: " << graph.size() << std::endl;




    // std::cout << graph.size() << std::endl;
    // uint64_t nodeIndex = 0;
    // for(const auto & pair : graph)
    // {
    //     std::cout << pair.first << ": ";

    //     std::set<uint32_t> v = pair.second;
    //     //std::sort(v.begin(), v.end());

    //  //for(const auto & node : pair.second)
    //  for(const auto & node : v)
    //     {
    //         std::cout << node << " ";
    //     }

    //     ++nodeIndex;
    //     std::cout << std::endl;
    // }



    return 0;
}
