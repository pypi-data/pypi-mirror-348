# ------------------------------------------------------------------------
# This module contains the ClassifierHandler class.
# The ClassifierHandler class is a class that contains the methods used to
# classify tblastx hits as full-length duplications.
# ------------------------------------------------------------------------
import portion as P


class ClassifierHandler(object):
    def __init__(
            self,
            search_engine: object
    ):
        self.data_container = search_engine.data_container
        self.environment = search_engine.environment
        self.search_engine = search_engine
        self.database_interface = search_engine.database_interface

    def get_mrna_cds_annotations(
            self,
            transcript_dictionary: dict,
    ):
        return [
            annotation['coordinate']
            for annotation in transcript_dictionary['structure']
            if annotation['type'] == self.environment.cds_annot_feature
        ]

    @staticmethod
    def get_coding_events_in_mrna(
            mrna_cds_coordinates_list: list,
            events_coordinates_list: list

    ):
        return [
            event_coord
            for event_coord in events_coordinates_list
            if (event_coord in mrna_cds_coordinates_list or
                any(cds_coord.contains(event_coord) for cds_coord in mrna_cds_coordinates_list))
        ]

    @staticmethod
    def get_missing_coordinates(
            coding_events_coordinates_list: list,
            coding_events_in_mrna_list: list,
    ):
        missing_coordinates = tuple(
            coding_event
            for coding_event in coding_events_coordinates_list
            if coding_event not in coding_events_in_mrna_list
        )
        if len(missing_coordinates) == 1:
            return missing_coordinates[0]
        return missing_coordinates if missing_coordinates else ''

    def get_coding_events_transcript_counts(
            self,
            gene_id: str,
            coding_events_coordinates_list: list,
    ) -> list:
        transcript_counts_list = []
        n_events = len(coding_events_coordinates_list)
        mrnas_dictionary = self.data_container.gene_hierarchy_dictionary[gene_id]['mRNAs']
        for mrna_transcript, trans_dict in mrnas_dictionary.items():
            mrna_cds_coords_list = self.get_mrna_cds_annotations(
                transcript_dictionary=trans_dict
            )
            coding_events_in_mrna_list = self.get_coding_events_in_mrna(
                mrna_cds_coordinates_list=mrna_cds_coords_list,
                events_coordinates_list=coding_events_coordinates_list
            )
            n_coding_events_in_transcript = len(coding_events_in_mrna_list)
            # All
            if n_coding_events_in_transcript == n_events:
                transcript_counts_list.append(
                    (n_events, 0, 0, 0, '')
                )
            # Neither
            elif n_coding_events_in_transcript == 0:
                transcript_counts_list.append(
                    (0, 0, 0, n_events, '')
                )
            # Rest
            else:
                missing_coordinates = self.get_missing_coordinates(
                    coding_events_coordinates_list=coding_events_coordinates_list,
                    coding_events_in_mrna_list=coding_events_in_mrna_list
                )
                n_missing_events = len(missing_coordinates)
                k = n_events - n_missing_events
                transcript_counts_list.append(
                    (0, k, n_missing_events, 0, missing_coordinates if missing_coordinates else '')
                )
        return transcript_counts_list

    def interdependence_classification(
            self,
            gene_id: str,
            id_: int,
            transcript_counts_list: list,
            n_coding_events: int,
            coding_events_coordinates: list
    ) -> tuple:
        n_mrnas = len(transcript_counts_list)
        classification_sums = self._calculate_classification_sums(transcript_counts_list)

        temp = (
            gene_id,
            id_,
            n_mrnas,
            n_coding_events,
            classification_sums['all'],
            classification_sums['present'],
            classification_sums['abscent'],
            classification_sums['neither']
        )

        category, exclusive_events = self._determine_category(
            n_mrnas, n_coding_events, classification_sums, transcript_counts_list, coding_events_coordinates
        )
        exclusive_events_str = ''
        if exclusive_events:
            temp_list_events = [tuple(event) if len(event) > 1 else list(event).pop() for event in exclusive_events]
            exclusive_events_str = '_'.join(map(str, temp_list_events))

        return *temp, category, exclusive_events_str

    @staticmethod
    def _calculate_classification_sums(
            transcript_counts_list: list
    ):
        """Calculate sums for each classification category."""
        return {
            category: sum(mrna_count[i] for mrna_count in transcript_counts_list)
            for i, category in enumerate(['all', 'present', 'abscent', 'neither'])
        }

    @staticmethod
    def _find_related_items(item, list_items):
        def check_condition(itemi, itemj):
            return bool(set(itemi).intersection(set(itemj))) if itemi != itemj else {}

        temp_list = [other_item for other_item in list_items if check_condition(item, other_item)]
        return temp_list

    def _determine_category(
            self,
            n_mrnas: int,
            n_coding_events: int,
            classification_sums: dict,
            transcript_counts_list: list,
            coding_events_coordinates: list
    ):
        """Determine the category and exclusive events based on classification sums and intersection."""
        category = ''
        exclusive_events = None
        N = n_mrnas * n_coding_events
        exclusive_candidates = {
            frozenset(set(coding_events_coordinates) - set(missing_events))
            for *_, missing_events in transcript_counts_list
            # we exclude the case where all events are missing
            if set(coding_events_coordinates) - set(missing_events) != set(coding_events_coordinates)
        }
        intersection = [item for item in exclusive_candidates if self._find_related_items(item, exclusive_candidates)]
        if classification_sums['all'] == N:
            category = 'OBLIGATE'
        elif classification_sums['neither'] == N:
            category = 'NEITHER'
        elif classification_sums['neither'] == 0 and 0 < classification_sums['all'] < N:
            category = 'FLEXIBLE'
        elif classification_sums['neither'] > 0:
            if classification_sums['all'] == N - classification_sums['neither']:
                category = 'OPTIONAL_OBLIGATE'
            elif 0 < classification_sums['all'] < N - classification_sums['neither']:
                category = 'OPTIONAL_FLEXIBLE'
            else:
                if not intersection:
                    category = 'OPTIONAL_EXCLUSIVE'
                    exclusive_events = exclusive_candidates
                elif intersection:
                    category = 'OPTIONAL_FLEXIBLE'
        elif not intersection:
            category = 'EXCLUSIVE'
            exclusive_events = exclusive_candidates
        else:
            category = '-'

        return category, exclusive_events

    def classify_expansion_interdependence(
            self,
            expansions_dictionary: dict
    ):
        expansions_classification_tuples = []
        for gene_id, gene_dict in expansions_dictionary.items():
            for expansion_id, expansion_coding_events_coordinates in gene_dict.items():
                n_events = len(expansion_coding_events_coordinates)
                transcript_counts_list = self.get_coding_events_transcript_counts(
                    gene_id=gene_id,
                    coding_events_coordinates_list=expansion_coding_events_coordinates
                    )
                classified_expansion = self.interdependence_classification(
                    gene_id=gene_id,
                    id_=expansion_id,
                    transcript_counts_list=transcript_counts_list,
                    n_coding_events=n_events,
                    coding_events_coordinates=expansion_coding_events_coordinates
                )
                expansions_classification_tuples.append(classified_expansion)
        return expansions_classification_tuples

    def classify_coding_match_interdependence(
            self,
            gene_id: str,
            match_id: int,
            query_coordinates: P.Interval,
            target_coordinates: P.Interval,
    ) -> tuple:
        match_coding_events_coordinates = [query_coordinates, target_coordinates]
        transcript_counts_list = self.get_coding_events_transcript_counts(
            gene_id=gene_id,
            coding_events_coordinates_list=match_coding_events_coordinates
        )
        classified_match = self.interdependence_classification(
            gene_id=gene_id,
            id_=match_id,
            transcript_counts_list=transcript_counts_list,
            n_coding_events=len(match_coding_events_coordinates),
            coding_events_coordinates=match_coding_events_coordinates
        )
        return classified_match
