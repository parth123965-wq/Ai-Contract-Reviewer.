from ai_engine.services.chunk_service import ChunkService
from ai_engine.services.embedding_service import EmbeddingService
from ai_engine.services.text_extractor import TextExtractor
from ai_engine.services.vector_store_service import VectorStoreService
from ai_engine.graph.state import ContractState

class ContractNodes:
    
    def __init__(self):
        self.text_extractor = TextExtractor()
        self.chunk_service = ChunkService()
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService()
        
    def extract_text_node(self,state: ContractState) -> ContractState:
        state['extracted_text'] = self.text_extractor.extract_text(file_path=state['file_path'])
        return state
    
    def chunk_text_node(self,state: ContractState) -> ContractState:
        state['chunks'] = self.chunk_service.chunk_text(state['extracted_text'])
        return state
    
    def embedding_node(self,state: ContractState) -> ContractState:
        state['embeddings'] = self.embedding_service.create_embeddings(chunks=state['chunks'])
        state['query_embedding'] = state['embeddings'][0]
        return state
    
    def store_vector_node(self,state: ContractState) -> ContractState:
        self.vector_store.store_embeddings(
            contract_id=state['contract_id'],
            user_id=state['user_id'],
            chunks=state['chunks'],
            embeddings=state['embeddings'],
            version=state['analysis_version']
        )
        return state
    
    def retrieve_context_node(self,state: ContractState) -> ContractState:
        state['retrieved_chunks'] = self.vector_store.search(
            contract_id=state['contract_id'],
            user_id=state['user_id'],
            query_embedding=state['query_embedding'],
        )
        return state
    
    def prompt_node(self,state: ContractState) -> ContractState:
        pass
    
    def llm_node(self,state: ContractState) -> ContractState:
        pass
    
    def parser_node(self,state: ContractState) -> ContractState:
        pass
    
    def save_analysis_node(self,state: ContractState) -> ContractState:
        pass