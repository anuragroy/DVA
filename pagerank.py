import time
import mmap
from struct import unpack


"""
Code for the PageRank algorithm (power iteration)

Here, the binary index_file contains the mapping of each node's ID to its degree.
The node IDs range from 0 to max_node_id.
Hence, the index_file contains (max_node_id + 1) pairs of values,
each of which is of 'long long' C type in little endian byte order.
The index_file is memory-mapped into the index_map object.

The binary edge_file contains the edges in the (source ID, target ID) format.
Hence, the edge_file contains edge_count pairs of values,
each of which is of 'int' C type in little endian byte order.
The edge_file is memory-mapped into the edge_map object.

This code will:
(1) initialize the memory-mapped objects (index_map and edge_map),
(2) unpack the source and target IDs from the edge_map, and
(3) upack the source ID and source degree from the index_map.

Note: This code assumes that the node IDs start from 0 and are contiguous up to max_node_id.

"""
def pagerank(index_file, edge_file, max_node_id, edge_count, damping_factor=0.85, iterations=10):
    index_map = mmap.mmap(
        index_file.fileno(),
        length=(max_node_id + 1)*16,   
        access=mmap.ACCESS_READ)

    edge_map = mmap.mmap(
        edge_file.fileno(),
        length=edge_count*8,   
        access=mmap.ACCESS_READ)

    scores = [1.0 / (max_node_id + 1)] * (max_node_id + 1)

    start_time = time.time()

    for it in range(iterations):
        new_scores = [0.0] * (max_node_id + 1)

        for i in xrange(edge_count):
            source, target = unpack(
                '<ii',   
                edge_map[i * 8: i * 8 + 8])   

            source_degree = unpack(
                '<qq',   
                index_map[source * 16: source * 16+ 16])[1]   
            new_scores[target] += damping_factor * scores[source] / source_degree

        min_pr = (1 - damping_factor) / (max_node_id + 1)
        new_scores = [min_pr + item for item in new_scores]
        scores = new_scores

        print "Completed {0}/{1} iterations. {2} seconds elapsed." \
            .format(it + 1, iterations, time.time() - start_time)

    print

    return scores