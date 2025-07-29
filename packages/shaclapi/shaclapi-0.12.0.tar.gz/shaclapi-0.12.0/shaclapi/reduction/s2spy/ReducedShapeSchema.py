import logging
import os
import re
from pathlib import Path

from SHACL2SPARQLpy.ShapeNetwork import ShapeNetwork
from SHACL2SPARQLpy.sparql.SPARQLEndpoint import SPARQLEndpoint
from SHACL2SPARQLpy.utils import fileManagement
from TravSHACL.TravSHACL import parse_heuristics
from TravSHACL.core.GraphTraversal import GraphTraversal

from shaclapi.reduction.s2spy.ReducedShapeParser import ReducedShapeParser
from shaclapi.reduction.s2spy.RuleBasedValidationResultStreaming import RuleBasedValidationResultStreaming

logger = logging.getLogger(__name__)


class ReducedShapeSchema(ShapeNetwork):
    def __init__(self, schema_dir, schema_format, endpoint_url, graph_traversal, heuristics, use_selective_queries, max_split_size, output_dir, order_by_in_queries, save_outputs, work_in_parallel, query, config, result_transmitter):
        self.shaclAPIConfig = config
        self.shapeParser = ReducedShapeParser(query, graph_traversal, config)
        self.shapes, self.node_order, self.target_shape_list = self.shapeParser.parseShapesFromDir(
            schema_dir, schema_format, use_selective_queries, max_split_size, order_by_in_queries)
        self.schema_dir = schema_dir
        self.shapesDict = {shape.getId(): shape for shape in self.shapes}
        self.endpoint = SPARQLEndpoint(endpoint_url)
        self.graphTraversal = graph_traversal
        self.dependencies, self.reverse_dependencies = self.compute_edges()
        self.outputDirName = output_dir
        self.result_transmitter = result_transmitter

    @staticmethod
    def from_config(config, query_object, result_transmitter):
        return ReducedShapeSchema(config.schema_directory, config.schema_format, config.external_endpoint, \
            GraphTraversal[config.traversal_strategy], parse_heuristics(config.heuristic), config.use_selective_queries, \
                config.max_split_size, os.path.join(config.output_directory, config.backend, re.sub(r'[^\w\-_.]', '_', config.test_identifier), ''), config.order_by_in_queries, config.save_outputs, config.work_in_parallel, \
                    query_object, config, result_transmitter)

    def validate(self, start_with_target_shape=True):
        """Executes the validation of the shape network."""
        start = None
        if self.shaclAPIConfig.start_shape_for_validation:
            logger.info('Starting with Shape set in Configuration')
            start = [self.shaclAPIConfig.start_shape_for_validation]
        elif self.node_order is not None:
            logger.info('Using Node Order provided by the shaclapi')
            node_order = self.node_order
        elif start_with_target_shape:
            logger.info('Starting with Target Shape')
            start = self.target_shape_list
        else:
            logger.warning('Starting with Shape determined by S2Spy')
            from SHACL2SPARQLpy.utils.globals import PARSING_ORDER
            node_order = PARSING_ORDER

        if start is not None:
            logger.debug('Starting Point is:' + start[0])
            node_order = self.graphTraversal.traverse_graph(
                self.dependencies, self.reverse_dependencies, start[0])
        
        for s in self.shapes:
            s.computeConstraintQueries()

        os.makedirs(self.outputDirName, exist_ok=True)
        for file in ['validation.log', 'targets_valid.log', 'targets_violated.log', 'stats.txt', 'traces.csv']:
            Path(self.outputDirName, file).touch()

        RuleBasedValidationResultStreaming(
            self.endpoint,
            node_order,
            self.shapesDict,
            fileManagement.openFile(self.outputDirName, 'validation.log'),
            fileManagement.openFile(self.outputDirName, 'targets_valid.log'),
            fileManagement.openFile(self.outputDirName, 'targets_violated.log'),
            fileManagement.openFile(self.outputDirName, 'stats.txt'),
            fileManagement.openFile(self.outputDirName, 'traces.csv'),
            self.result_transmitter
        ).exec()
        return {}
    
    def compute_edges(self):
        """Computes the edges in the network."""
        dependencies = {s.getId(): [] for s in self.shapes}
        reverse_dependencies = {s.getId(): [] for s in self.shapes}
        for s in self.shapes:
            refs = s.getShapeRefs()
            if refs:
                name = s.getId()
                dependencies[name] = refs
                for ref in refs:
                    reverse_dependencies[ref].append(name)
        return dependencies, reverse_dependencies
