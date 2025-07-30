# ------------------------------------------------------------------------
# This module contains the CounterHandler class, which is used to handle
# the counter object in the BlastEngine class.
# ------------------------------------------------------------------------
import matplotlib
import networkx as nx
from collections import defaultdict
import portion as P
import matplotlib.pyplot as plt
from pathlib import Path
from Bio.Seq import Seq
matplotlib.use('Agg')


class ReconcilerHandler(object):
    def __init__(
            self,
            blast_engine: object,
            cds_overlapping_threshold: float,
    ):
        self.environment = blast_engine.environment
        self.data_container = blast_engine.data_container
        self.database_interface = blast_engine.database_interface
        self.blast_engine = blast_engine
        self.cds_overlapping_threshold = cds_overlapping_threshold

    @staticmethod
    def compute_average(
            a_list: list
    ) -> float:
        return sum(a_list) / len(a_list)

    def get_candidate_cds_reference(
            self,
            cds_coordinates_list: list[P.Interval],
            overlapping_coordinates_list: list[tuple[P.Interval, float]]
    ) -> P.Interval:
        """
        get_candidate_cds_reference is a function that given a list
        of overlapping target coordinates, returns the best candidate CDS reference

        Example:
         >>> cds_list = [P.open(0, 100), P.open(200, 300)]
         >>> overlapping_list = [(P.open(5, 100), 0.9), (P.open(10, 100), 0.9)]
         >>> get_candidate_cds_reference(cds_list, overlapping_list)
         >>> P.open(0, 100)

        :param cds_coordinates_list: list of CDS coordinates across all transcripts,
         sorted by the lower bound. The intervals can overlap.
        :param overlapping_coordinates_list: list of overlapping target coordinates

        """
        # We want to find the CDS that overlaps with the overlapping targets by
        # the highest percentage. We will compute the average of the two-way overlapping
        # percentage between the CDS and the overlapping targets and take the
        # CDS with the highest average.
        cand_reference_list = [
            cds_coordinate for cds_coordinate in cds_coordinates_list
            if all(
                [self.data_container.min_perc_overlap(
                    intv_i=cds_coordinate,
                    intv_j=target_coordinate
                ) > self.cds_overlapping_threshold
                 for target_coordinate, _ in overlapping_coordinates_list]
            )
        ]
        if cand_reference_list:
            # Since we are considering all CDSs across all transcripts,
            # we might end up with more than one CDS candidate.
            candidate_reference, _ = max(cand_reference_list, key=lambda x: x[0].upper - x[0].lower)
            return candidate_reference
        return P.open(0, 0)

    def process_full_overlap(
            self,
            source_set: set,
            target_set: set,
            overlapping_coords: dict,
            processed_target: set
    ):
        for coordinate in source_set:
            for other_coord, oeval in target_set:
                overlap_perc = self.data_container.min_perc_overlap(coordinate, other_coord)
                if overlap_perc >= self.cds_overlapping_threshold:
                    overlapping_coords[coordinate].append((other_coord, oeval))
                    processed_target.add((other_coord, oeval))
        return overlapping_coords, processed_target

    def get_coding_reference_dictionary(
            self,
            cds_coordinates_set: set,
            coding_coordinates_set: set,
            auxiliary_cds_set: set
    ):
        overlapping_coords = defaultdict(list)
        processed_target = set()
        overlapping_coords, processed_target = self.process_full_overlap(
            source_set=cds_coordinates_set,
            target_set=coding_coordinates_set,
            overlapping_coords=overlapping_coords,
            processed_target=processed_target
        )
        orphan_coord = set(coord for coord in coding_coordinates_set if coord not in processed_target)
        if orphan_coord:
            overlapping_coords, processed_target = self.process_full_overlap(
                source_set=auxiliary_cds_set,
                target_set=orphan_coord,
                overlapping_coords=overlapping_coords,
                processed_target=processed_target
            )
        return dict(sorted(overlapping_coords.items(), key=lambda k: len(k[1]), reverse=True))

    def process_insertion_overlaps(
            self,
            source_set: set,
            target_set: set,
            overlapping_coords: dict,
            processed_target: set

    ):
        for coordinate in source_set:
            for other_coord, oeval in target_set:
                if coordinate.contains(other_coord):
                    overlapping_coords[coordinate].append((other_coord, oeval))
                    processed_target.add((other_coord, oeval))
                elif self.blast_engine.get_overlap_percentage(
                        intv_i=coordinate,
                        intv_j=other_coord
                ) >= self.cds_overlapping_threshold:
                    reference = P.open(
                        max(other_coord.lower, coordinate.lower),
                        min(other_coord.upper, coordinate.upper)
                    )
                    overlapping_coords[coordinate].append((other_coord, reference, oeval))
                    processed_target.add((other_coord, oeval))
        return overlapping_coords, processed_target

    def get_insertion_reference_dictionary(
            self,
            cds_candidates_set: set,
            auxiliary_cds_set: set,
            coding_coordinates_set: set
    ):
        overlapping_coords = defaultdict(list)
        insertion_reference_dict = {}
        processed_target = set()
        overlapping_coords, processed_target = self.process_insertion_overlaps(
            source_set=cds_candidates_set,
            target_set=coding_coordinates_set,
            overlapping_coords=overlapping_coords,
            processed_target=processed_target
        )
        orphan_coord = set(coord for coord in coding_coordinates_set if coord not in processed_target)
        if orphan_coord:
            overlapping_coords, processed_target = self.process_insertion_overlaps(
                source_set=auxiliary_cds_set,
                target_set=orphan_coord,
                overlapping_coords=overlapping_coords,
                processed_target=processed_target
            )
        overlapping_coords = dict(sorted(overlapping_coords.items(), key=lambda k: len(k[1]), reverse=True))
        for cds_coordinate, list_of_overlapping_coords in overlapping_coords.items():
            reference = min(list_of_overlapping_coords, key=lambda x: x[-1])
            if len(reference) == 3:
                _, reference, _ = reference
            else:
                reference, _ = reference
            for target_coordinate in list_of_overlapping_coords:
                if len(target_coordinate) == 3:
                    target_coordinate, _, oeval = target_coordinate
                    target_coordinate = (target_coordinate, oeval)
                if target_coordinate not in insertion_reference_dict:
                    insertion_reference_dict[target_coordinate] = reference
        return insertion_reference_dict

    @staticmethod
    def fetch_non_coding_coordinates(
            target_coordinates_list: list,
            cds_coordinates_set: set,

    ):
        return [
            (target_coordinate, evalue)
            for target_coordinate, evalue in target_coordinates_list
            if all(not target_coordinate.overlaps(cds_coordinate)
                   for cds_coordinate in cds_coordinates_set)
        ]

    def get_matches_reference_mode_dictionary(
            self,
            clusters_list: list[list[tuple]],
            cds_candidates_set: set,
            gene_cds_set: set,
    ):
        auxiliary_candidates_cds_set = gene_cds_set - cds_candidates_set
        reference_dictionary = dict()
        for coordinates_cluster in clusters_list:
            non_coding_coordinates = self.fetch_non_coding_coordinates(
                target_coordinates_list=coordinates_cluster,
                cds_coordinates_set=set(cds_candidates_set).union(set(auxiliary_candidates_cds_set))
            )
            coding_coordinates = set(
                target
                for target in coordinates_cluster
                if target not in non_coding_coordinates
            )
            # INACTIVE
            if non_coding_coordinates:
                reference = min(non_coding_coordinates, key=lambda x: x[1])[0]
                ref_type = 'INACTIVE_UNANNOTATED'
                for non_coding_event, evalue, in non_coding_coordinates:
                    if non_coding_event not in reference_dictionary:
                        reference_dictionary[non_coding_event] = {
                            'reference': reference,
                            'mode': ref_type
                        }
            # FULL
            if coding_coordinates:
                candidate_cds_reference = self.get_coding_reference_dictionary(
                    cds_coordinates_set=cds_candidates_set,
                    auxiliary_cds_set=auxiliary_candidates_cds_set,
                    coding_coordinates_set=coding_coordinates
                )
                if candidate_cds_reference:
                    ref_type = 'FULL'
                    for cds_coord, overlapping_coords in candidate_cds_reference.items():
                        for target_coord, _ in overlapping_coords:
                            if target_coord not in reference_dictionary:
                                reference_dictionary[target_coord] = {
                                    'reference': cds_coord,
                                    'mode': ref_type
                                }
                # INSERTION
                insertion_candidate_coding_coordinates = set(
                    (target_coord, eval_)
                    for (target_coord, eval_) in coding_coordinates
                    if target_coord not in reference_dictionary
                )
                if insertion_candidate_coding_coordinates:
                    insertion_reference_dictionary = self.get_insertion_reference_dictionary(
                        cds_candidates_set=cds_candidates_set,
                        auxiliary_cds_set=auxiliary_candidates_cds_set,
                        coding_coordinates_set=insertion_candidate_coding_coordinates
                    )
                    if insertion_reference_dictionary:
                        ref_type = 'INSERTION_EXCISION'
                        for target_coordinate, reference in insertion_reference_dictionary.items():
                            tar_coordinate, _ = target_coordinate
                            reference_coordinate = reference
                            if tar_coordinate not in reference_dictionary:
                                reference_dictionary[tar_coordinate] = {
                                    'reference': reference_coordinate,
                                    'mode': ref_type
                                }
                truncation_candidate_coordinates = set(
                    (target, eval_)
                    for target, eval_ in coding_coordinates
                    if target not in reference_dictionary
                )
                if truncation_candidate_coordinates:
                    reference = min(truncation_candidate_coordinates, key=lambda x: x[1])[0]
                    ref_type = 'TRUNCATION_ACQUISITION'
                    for target, eval_ in truncation_candidate_coordinates:
                        if target not in reference_dictionary:
                            reference_dictionary[target] = {
                                'reference': reference,
                                'mode': ref_type
                            }
        return reference_dictionary

    @staticmethod
    def create_events_multigraph(
            targets_reference_coordinates_dictionary: dict,
            query_coordinates_set: set,
            tblastx_records_set: set,
    ) -> nx.MultiGraph:
        gene_graph = nx.MultiGraph()
        target_coordinates_set = set([
            (reference['reference'], reference['mode'])
            for reference in targets_reference_coordinates_dictionary.values()
        ])

        set_of_nodes = set([
            ((node_coordinate.lower, node_coordinate.upper), coordinate_type)
            for node_coordinate, coordinate_type in [
                *[(coordinate, 'FULL') for coordinate in query_coordinates_set],
                *target_coordinates_set
            ]
        ])
        gene_graph.add_nodes_from(
            [node_coordinate for node_coordinate, _ in set_of_nodes]
        )
        for node in set_of_nodes:
            node_coordinate, coordinate_type = node
            gene_graph.nodes[node_coordinate]['type'] = coordinate_type

        for event in tblastx_records_set:
            (fragment_id, _, cds_start, cds_end, target_start, target_end, evalue) = event
            target_coordinate = P.open(target_start, target_end)  # exact target coordinates
            # we take the "reference target coordinates"
            reference_coordinate = targets_reference_coordinates_dictionary[target_coordinate]['reference']
            mode = targets_reference_coordinates_dictionary[target_coordinate]['mode']
            gene_graph.add_edge(
                u_for_edge=(cds_start, cds_end),
                v_for_edge=(reference_coordinate.lower, reference_coordinate.upper),
                fragment_id=fragment_id,
                target=(target_start, target_end),
                corrected_target=(reference_coordinate.lower, reference_coordinate.upper),
                query=(cds_start, cds_end),
                evalue=evalue,
                mode=mode,
                color='black',
                width=2
            )
        return gene_graph

    @staticmethod
    def draw_event_multigraph(
            gene_graph: nx.MultiGraph,
            figure_path: Path,
    ):
        color_map = {
            'INSERTION_EXCISION': 'blue',
            'FULL': 'green',
            'INACTIVE_UNANNOTATED': 'red',
            'TRUNCATION_ACQUISITION': 'orange'
        }

        plt.figure(figsize=(16, 8))
        node_colors = [
            color_map[node[1]['type']]
            for node in gene_graph.nodes(data=True)
        ]
        components = list(nx.connected_components(gene_graph))
        node_labels = {
            node: f'({node[0]},{node[1]})'
            for node in gene_graph.nodes
        }
        # Create a separate circular layout for each component
        layout_scale = 2
        component_positions = []
        for component in components:
            layout = nx.circular_layout(
                gene_graph.subgraph(component),
                scale=layout_scale
            )
            component_positions.append(layout)
        position_shift = max(layout_scale * 5.5, 15)
        component_position = {}
        for event_idx, layout in enumerate(component_positions):
            for node, position in layout.items():
                shifted_position = (position[0] + event_idx * position_shift, position[1])
                component_position[node] = shifted_position

        if max([len(component) for component in components]) == 2:
            label_positions = component_position
        else:
            label_positions = {
                node: (position[0], position[1] + 0.1)
                for node, position in component_position.items()
            }

        # Draw the graph with edge attributes
        nx.draw_networkx_nodes(
            G=gene_graph,
            node_color=node_colors,
            pos=component_position,
            node_size=350,
        )
        nx.draw_networkx_labels(
            gene_graph,
            label_positions,
            labels=node_labels,
            font_size=8,
            bbox=dict(
                boxstyle="round,pad=0.3",
                edgecolor="white",
                facecolor="white"
            )
        )
        # Draw edges with different styles and colors
        for edge in gene_graph.edges(data=True):
            source, target, attributes = edge
            edge_style = attributes.get('style', 'solid')
            edge_color = attributes.get('color', 'black')
            edge_width = attributes.get('width', 1)
            nx.draw_networkx_edges(
                gene_graph,
                component_position,
                edgelist=[(source, target)],
                edge_color=edge_color,
                style=edge_style,
                width=edge_width
            )
        plt.savefig(figure_path)
        plt.close()

    @staticmethod
    def build_mode_dictionary(
            targets_reference_coordinates_dictionary: dict
    ) -> dict:
        return {
            reference_coordinate['reference']: reference_coordinate['mode']
            for reference_coordinate in targets_reference_coordinates_dictionary.values()
        }

    @staticmethod
    def build_event_coordinates_dictionary(
            component: set[tuple],
            mode_dict: dict,
            gene_graph: nx.MultiGraph
    ) -> dict:
        event_coord_dict = {}
        for start, end in component:
            node_coord = P.open(int(start), int(end))
            mode = mode_dict.get(node_coord, "FULL")  # queries are not included in the mode dictionary
            degree = gene_graph.degree((start, end))
            event_coord_dict[node_coord] = [mode, degree, None]  # cluster_id is None initially
        return event_coord_dict

    def assign_cluster_ids_to_event_coordinates(
            self,
            event_coordinates_dictionary: dict
    ) -> None:
        # Convert event coordinates to a set of tuples for clustering
        node_coordinates_set = set(
            (node_coordinate, 0)
            for node_coordinate in event_coordinates_dictionary.keys()
        )
        # get clusters of overlapping nodes
        node_coordinates_clusters = [
            [node_coordinate for node_coordinate, _ in cluster]
            for cluster in self.data_container.get_overlapping_clusters(
                target_coordinates_set=node_coordinates_set,
                threshold=0  # we want to get all overlaps regardless of the percentage
            )
            if len(cluster) > 1
        ]
        cluster_id = 0
        # Assign cluster id to each cluster within the component
        for cluster in node_coordinates_clusters:
            for node_coordinate in cluster:
                event_coordinates_dictionary[node_coordinate][2] = cluster_id
            cluster_id += 1

    @staticmethod
    def map_edges_to_records(
            graph: nx.MultiGraph,
            expansion_id_counter: int,
            component: set[tuple]
    ) -> list[tuple]:
        comp_event_list = []
        subgraph = graph.subgraph(component)
        # in here we are mapping the event id to each fragment id (event)
        # where each fragment represents a BLAST hit between the query and the target
        # hence, in the graph each fragment is represented by an edge
        for edge in subgraph.edges(data=True):
            # edge is a tuple (node1, node2, attributes)
            comp_event_list.append(
                (expansion_id_counter, edge[-1]['fragment_id'])
            )
        return comp_event_list

    @staticmethod
    def build_events_list(
            gene_id: str,
            event_coordinates_dictionary: dict,
            expansion_id_counter: int,
            gene_start: int,
    ) -> list[tuple]:
        return [
            (gene_id,
             mode,
             node_coordinate.lower + gene_start,
             node_coordinate.upper + gene_start,
             degree,
             cluster_id,
             expansion_id_counter
             )
            for node_coordinate, (mode, degree, cluster_id) in event_coordinates_dictionary.items()
        ]

    @staticmethod
    def gene_non_reciprocal_fragments(
            gene_graph: nx.MultiGraph,
            events_list: list[tuple],
            gene_start: int
    ):
        event_reduced_fragments_list = list()
        skip_pair = list()
        for event in events_list:
            _, _, node_start, node_end, *_, event_id = event
            for adjacent_node, adjacent_edges in gene_graph[(node_start - gene_start, node_end - gene_start)].items():
                pair = {(node_start - gene_start, node_end - gene_start), adjacent_node}
                if pair not in skip_pair:
                    event_reduced_fragments_list.append((adjacent_edges[0]['mode'], adjacent_edges[0]['fragment_id']))
                    skip_pair.append(pair)
        return event_reduced_fragments_list

    def get_reconciled_graph_and_expansion_events_tuples(
            self,
            targets_reference_coordinates_dictionary: dict,
            gene_id: str,
            gene_graph: nx.MultiGraph
    ) -> tuple[list[tuple], list]:
        gene_start = self.data_container.gene_hierarchy_dictionary[gene_id]['coordinate'].lower

        mode_dictionary = self.build_mode_dictionary(
            targets_reference_coordinates_dictionary=targets_reference_coordinates_dictionary
        )
        # each disconnected component will represent a duplication event within a gene
        # and the number of nodes in the component is the number of duplicated exons
        # i.e., each event is described by a number of duplicated exons
        disconnected_components = list(nx.connected_components(gene_graph))
        expansion_events_list = []
        expansion_non_reciprocal_fragments = []
        expansion_id_counter = 0
        for component in disconnected_components:
            # First: Assign event id to each component
            event_coordinates_dictionary = self.build_event_coordinates_dictionary(
                component=component,
                mode_dict=mode_dictionary,
                gene_graph=gene_graph,
            )
            # Second : Assign cluster ids within events
            self.assign_cluster_ids_to_event_coordinates(
                event_coordinates_dictionary=event_coordinates_dictionary
            )
            events_list = self.build_events_list(
                    gene_id=gene_id,
                    event_coordinates_dictionary=event_coordinates_dictionary,
                    expansion_id_counter=expansion_id_counter,
                    gene_start=gene_start
                )
            expansion_events_list.extend(events_list)
            expansion_non_reciprocal_fragments.extend(
                self.gene_non_reciprocal_fragments(
                    gene_graph=gene_graph,
                    events_list=events_list,
                    gene_start=gene_start
                )
            )
            expansion_id_counter += 1
        return expansion_events_list, expansion_non_reciprocal_fragments

    @staticmethod
    def get_gene_events_dictionary(
            tblastx_full_matches_list: list[tuple],
    ):
        full_matches_dictionary = defaultdict(set)
        # group full matches by gene id
        for match in tblastx_full_matches_list:
            gene_id = match[1]
            full_matches_dictionary[gene_id].add(match)
        return full_matches_dictionary

    @staticmethod
    def get_hits_query_and_target_coordinates(
            tblastx_records_set: set,
    ):
        query_coordinates = set()
        min_e_values = {}
        for record in tblastx_records_set:
            fragment_id, gene_id, cds_start, cds_end, target_start, target_end, evalue = record
            target_coordinate = P.open(target_start, target_end)
            query_coordinates.add(P.open(cds_start, cds_end))
            if target_coordinate not in min_e_values or evalue < min_e_values[target_coordinate]:
                min_e_values[target_coordinate] = evalue
        target_coordinates_set = set([
            (target_coordinate, min_evalue)
            for target_coordinate, min_evalue in min_e_values.items()
        ])
        return query_coordinates, target_coordinates_set

    @staticmethod
    def center_and_sort_cds_coordinates(
            cds_coordinates: list,
            gene_start: int
    ) -> list[P.Interval]:
        return sorted(
                list(set([P.open(i.lower - gene_start, i.upper - gene_start) for i in cds_coordinates])),
                key=lambda x: (x.lower, x.upper)
        )

    def get_corrected_frames_and_identity(
            self,
            gene_id: str,
            cds_coordinate: P.Interval,
            corrected_coordinate: P.Interval,
            cds_candidates_dictionary: dict
    ):
        target_sequence_frames_translations = []
        gene_start = self.data_container.gene_hierarchy_dictionary[gene_id]['coordinate'].lower
        chrom = self.data_container.gene_hierarchy_dictionary[gene_id]['chrom']
        strand = self.data_container.gene_hierarchy_dictionary[gene_id]['strand']
        aligned_cds_coord = P.open(cds_coordinate.lower + gene_start, cds_coordinate.upper + gene_start)
        query_frame = int(cds_candidates_dictionary['cds_frame_dict'][aligned_cds_coord])
        query = Seq(self.data_container.genome_dictionary[chrom][aligned_cds_coord.lower:aligned_cds_coord.upper])
        if strand == '-':
            query = query.reverse_complement()
        adjusted_end = self.adjust_coordinates_to_frame(
            end=len(query),
            frame=query_frame
        )
        query = query[query_frame:adjusted_end]
        trans_query = query.translate()
        for frame in [0, 1, 2]:
            target_coord = P.open(corrected_coordinate.lower + gene_start,
                                  corrected_coordinate.upper + gene_start)
            target = Seq(self.data_container.genome_dictionary[chrom][target_coord.lower:target_coord.upper])
            if strand == '-':
                target = target.reverse_complement()
            adjusted_end = self.adjust_coordinates_to_frame(
                end=len(target),
                frame=frame
            )
            target = target[frame:adjusted_end]
            trans_target = target.translate()
            n_stop_codons = str(trans_target).count('*')
            alignment = self.blast_engine.perform_msa(
                query=trans_query,
                target=trans_target
            )
            prot_identity = self.blast_engine.compute_identity(
                sequence_i=alignment[0],
                sequence_j=alignment[1]
            )
            target_sequence_frames_translations.append(
                (prot_identity, frame, target, trans_target, n_stop_codons)
            )
        # we want the frame that gives us the highest identity alignment
        (corrected_prot_perc_id,
         corrected_frame,
         target,
         trans_target,
         n_stop_codons
         ) = max(target_sequence_frames_translations, key=lambda x: x[0])
        alignment = self.blast_engine.perform_msa(
            query=query,
            target=target
        )
        dna_identity = self.blast_engine.compute_identity(
            sequence_i=alignment[0],
            sequence_j=alignment[1]
        )
        return dna_identity, corrected_prot_perc_id, corrected_frame, query_frame, str(trans_query), str(trans_target)

    @staticmethod
    def adjust_coordinates_to_frame(
            end: int,
            frame: int
    ):
        length = end - frame
        if length % 3 != 0:
            adjusted_end = end - (length % 3)
        else:
            adjusted_end = end
        return adjusted_end

    def get_matches_corrected_coordinates_and_identity(
            self,
            gene_id: str,
            tblastx_records_set: set[tuple],
            targets_reference_coordinates_dictionary: dict,
            cds_candidates_dictionary: dict
    ) -> list[tuple]:
        corrected_coordinates_list = []
        for record in tblastx_records_set:
            fragment_id, _, cds_start, cds_end, target_start, target_end, _ = record
            target_coordinate = P.open(target_start, target_end)
            corrected_coordinate = targets_reference_coordinates_dictionary[target_coordinate]['reference']
            if target_coordinate != corrected_coordinate:
                (corrected_dna_ident,
                 corrected_prot_ident,
                 corrected_target_frame,
                 corrected_query_frame,
                 query_amino_seq,
                 corrected_target_seq
                 ) = (0, 0, 0, 0, '', '')

                # (corrected_dna_ident,
                #  corrected_prot_ident,
                #  corrected_target_frame,
                #  corrected_query_frame,
                #  query_amino_seq,
                #  corrected_target_seq
                #  ) = self.get_corrected_frames_and_identity(
                #     gene_id=gene_id,
                #     cds_coordinate=P.open(cds_start, cds_end),
                #     corrected_coordinate=corrected_coordinate,
                #     cds_candidates_dictionary=cds_candidates_dictionary
                # )
                corrected_coordinates_list.append((
                    corrected_coordinate.lower,
                    corrected_coordinate.upper,
                    corrected_dna_ident,
                    corrected_prot_ident,
                    query_amino_seq,
                    corrected_target_seq,
                    corrected_target_frame,
                    corrected_query_frame,
                    fragment_id))
        return corrected_coordinates_list

    def fetch_gene_cdss_set(
            self,
            gene_id: str
    ):
        return set(
            i['coordinate']
            for mran, struct in self.data_container.gene_hierarchy_dictionary[gene_id]['mRNAs'].items()
            for i in struct['structure'] if i['type'] == 'CDS'
            if i['coordinate'].upper - i['coordinate'].lower >= self.blast_engine.min_exon_length
        )

    def align_target_coordinates(
            self,
            gene_id: str,
            tblastx_records_set: set[tuple],
            cds_candidates_dictionary: dict
    ) -> tuple[set[P.Interval], dict]:
        gene_start = self.data_container.gene_hierarchy_dictionary[gene_id]['coordinate'].lower
        # center cds coordinates to gene start
        cds_candidates_coordinates = self.center_and_sort_cds_coordinates(
            cds_coordinates=cds_candidates_dictionary['candidates_cds_coordinates'],
            gene_start=gene_start
        )
        query_coordinates, target_coordinates = self.get_hits_query_and_target_coordinates(
            tblastx_records_set=tblastx_records_set
        )
        overlapping_targets = self.data_container.get_overlapping_clusters(
            target_coordinates_set=target_coordinates,
            threshold=self.cds_overlapping_threshold
        )
        gene_cds_set = self.fetch_gene_cdss_set(
            gene_id=gene_id
        )
        targets_reference_coordinates_dictionary = self.get_matches_reference_mode_dictionary(
            clusters_list=overlapping_targets,
            cds_candidates_set=set(cds_candidates_coordinates),
            gene_cds_set=gene_cds_set
        )
        return query_coordinates, targets_reference_coordinates_dictionary
