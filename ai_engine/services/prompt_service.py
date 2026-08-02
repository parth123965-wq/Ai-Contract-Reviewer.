

class PromptService:
    
    def build_prompt(self,request: list[str]) -> str:
        formatted_chunks = "\n\n".join(
            f"[Chunk {i+1}]:\n{chunk}"
            for i, chunk in enumerate(request)
        )
        prompt = f"""You are a helpful assistant. Answer the user's question using only the context provided below.

            --- CONTEXT START ---
            {formatted_chunks}
            --- CONTEXT END ---

            Please provide a clear and accurate response based strictly on the context above."""
        return prompt
    