import logging

from langgraph.graph import StateGraph, START


from arklex.env.workers.worker import BaseWorker, register_worker
from arklex.utils.graph_state import MessageState
from arklex.env.tools.utils import ToolGenerator
from arklex.env.tools.RAG.search import SearchEngine


logger = logging.getLogger(__name__)


@register_worker
class SearchWorker(BaseWorker):

    description = "Answer the user's questions based on real-time online search results"

    def __init__(self):
        super().__init__()
        self.action_graph = self._create_action_graph()

    def _create_action_graph(self):
        workflow = StateGraph(MessageState)
        # Add nodes for each worker
        search_engine = SearchEngine()
        workflow.add_node("search_engine", search_engine.search)
        workflow.add_node("tool_generator", ToolGenerator.context_generate)
        # Add edges
        workflow.add_edge(START, "search_engine")
        workflow.add_edge("search_engine", "tool_generator")
        return workflow

    def _execute(self, msg_state: MessageState, **kwargs):
        graph = self.action_graph.compile()
        result = graph.invoke(msg_state)
        return result
