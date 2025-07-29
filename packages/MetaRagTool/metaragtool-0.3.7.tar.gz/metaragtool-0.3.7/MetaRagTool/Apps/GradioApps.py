﻿from MetaRagTool.RAG.Chunkers import ChunkingMethod
import gradio as gr
from MetaRagTool.Utils.MRUtils import read_pdf, init_hf, listToString
import MetaRagTool.Utils.DataLoader as DataLoader
from MetaRagTool.RAG.MetaRAG import MetaRAG
import MetaRagTool.Constants as Constants
from MetaRagTool.LLM.GoogleGemini import Gemini




colors = [
    "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEEAD",
    "#D4A5A5", "#9B59B6", "#3498DB", "#E74C3C", "#2ECC71"
]
chunking_methods = [ChunkingMethod.SENTENCE_MERGER, ChunkingMethod.SENTENCE_MERGER_CROSS_PARAGRAPH,
                    ChunkingMethod.PARAGRAPH, ChunkingMethod.RECURSIVE, ChunkingMethod.SENTENCE]

rag:MetaRAG = None
encoder_model = None
reranker_model=None
contexts=None
qa=None

def load_models_and_data(encoder_name,reranker_name=None):
    from MetaRagTool.Encoders.SentenceTransformerEncoder import SentenceTransformerEncoder
    from MetaRagTool.Encoders.Reranker import CrossEncoderReranker
    global encoder_model,reranker_model, contexts,qa


    encoder_model = SentenceTransformerEncoder(encoder_name)
    if reranker_name is not None and len(reranker_name) > 0:
        reranker_model = CrossEncoderReranker(reranker_name)
    else:
        reranker_model = None

    contexts, qa = DataLoader.loadWikiFaQa(sample_size=10)

def tokenize_and_colorize(encoder_name, reranker_name,pdf_files, text, chunking_method, chunk_size, max_sentence_len,ignore_pfd_line_breaks,gemini_api_key):
    global rag
    load_models_and_data(encoder_name, reranker_name)

    corpus_texts = []

    if pdf_files is not None:
        for pdf_file in pdf_files:
            corpus_texts.append(read_pdf(pdf_file.name,ignore_line_breaks=ignore_pfd_line_breaks))
    if text:
        corpus_texts.append(text)
    if not corpus_texts:
        corpus_texts.append(contexts[1])
        # return "No input provided", []


    chunking_method = ChunkingMethod[chunking_method]

    api_key_to_use = gemini_api_key if gemini_api_key else Constants.API_KEY_GEMINI
    llm = Gemini(api_key=api_key_to_use)


    rag = MetaRAG(encoder_model=encoder_model, llm=llm, splitting_method=chunking_method,
                  chunk_size=chunk_size, max_sentence_len=max_sentence_len,reranker_model=reranker_model)

    rag.add_corpus(corpus_texts)
    tokens = rag.ChunksList

    color_index = 0
    colored_tokens = []
    for token in tokens:
        color = colors[color_index]
        color_index = (color_index + 1) % len(colors)

        # colored_token = f'<span style="color: {color}; font-size: 1.2em; margin: 0 2px;">{token}</span>'
        # colored_tokens.append(colored_token)
        colored_tokens.append((f"{token}", color))

    # result = ' '.join(colored_tokens)
    # result = f'<div dir="rtl" style="padding: 10px; background-color: #27272A; border-radius: 5px;">{result}</div>'
    # return rag.chunking_report(), result
    return rag.chunker.chunking_report(), colored_tokens





def retrieve_chunks(query, k,add_neighbor_chunks_smart,replace_retrieved_chunks_with_parent_paragraph, rerank):
    global rag

    # Check if rag instance exists
    if rag is None:
        return [("Please run the chunker first to initialize the RAG system.", "red")]

    try:
        rag.add_neighbor_chunks_smart = add_neighbor_chunks_smart
        rag.replace_retrieved_chunks_with_parent_paragraph=replace_retrieved_chunks_with_parent_paragraph
        rag.rerank = rerank
        # Retrieve the top k chunks
        results = rag.retrieve(query, top_k=k)

        # Format the results for HighlightedText component
        colored_chunks = []
        for i, chunk in enumerate(results):
            # Use cycling colors for different chunks
            color = colors[i % len(colors)]
            colored_chunks.append((f"{chunk}\n", color))

        return colored_chunks

    except Exception as e:
        # Return error message if something goes wrong
        return [(f"Error during retrieval: {str(e)}", "red")]


def full_rag_ask(query, k, add_neighbor_chunks_smart, replace_retrieved_chunks_with_parent_paragraph, rerank):
    global rag

    # Check if rag instance exists
    if rag is None:
        return "Please run the chunker first to initialize the RAG system."

    try:
        rag.add_neighbor_chunks_smart = add_neighbor_chunks_smart
        rag.replace_retrieved_chunks_with_parent_paragraph = replace_retrieved_chunks_with_parent_paragraph
        rag.rerank = rerank

        # Use rag.ask instead of rag.retrieve
        result = rag.ask(query, top_k=k)
        messages_history = listToString(rag.llm.messages_history,separator="\n\n")

        # Return raw text result
        return result,messages_history

    except Exception as e:
        # Return error message if something goes wrong
        return f"Error during RAG processing: {str(e)}"


def full_tool_rag_ask(query, add_neighbor_chunks_smart, replace_retrieved_chunks_with_parent_paragraph, rerank):
    global rag

    # Check if rag instance exists
    if rag is None:
        return "Please run the chunker first to initialize the RAG system."

    try:
        rag.add_neighbor_chunks_smart = add_neighbor_chunks_smart
        rag.replace_retrieved_chunks_with_parent_paragraph = replace_retrieved_chunks_with_parent_paragraph
        rag.rerank = rerank

        # Use rag.ask instead of rag.retrieve
        result = rag.ask(query,useTool=True)

        messages_history = listToString(rag.llm.messages_history,separator="\n\n")


        # Return raw text result
        return result,messages_history

    except Exception as e:
        # Return error message if something goes wrong
        return f"Error during RAG processing: {str(e)}"



def load_app(encoder_model_name='sentence-transformers/LaBSE', reranker_model_name='cross-encoder/mmarco-mMiniLMv2-L12-H384-v1'):
    Constants.lang = 'fa'

    if Constants.HFToken is None:
        import os
        Constants.HFToken=os.getenv('HFToken')
        Constants.API_KEY_GEMINI=os.getenv('GEMINIToken')
        Constants.API_KEY_OPENROUTER=os.getenv('OPENROUTERToken')

    init_hf()


    css = """
    #tokenized-output {
        direction: rtl;
        text-align: right;
    }
    """

    chunker = gr.Interface(
        fn=tokenize_and_colorize,
        inputs=[
            gr.Textbox(
                label="Encoder Model Name",
                placeholder="Enter encoder model name (e.g., sentence-transformers/all-MiniLM-L6-v2)",
                value=encoder_model_name
            ),
            gr.Textbox(
                label="Reranker Model Name (Optional)",
                placeholder="Enter reranker model name (e.g., cross-encoder/ms-marco-MiniLM-L-6-v2)",
                value=reranker_model_name

            ),
            gr.File(
                label="Upload PDF", file_count="multiple"
            ),
            gr.Textbox(
                label="Or Enter your text",
                placeholder="Type some large amount of text here...",
                lines=3
            ),
            gr.Dropdown(
                label="Select Chunking Method",
                choices=[method.name for method in chunking_methods],
                value=chunking_methods[0].name
            ),
            gr.Slider(
                label="Select Chunk Size",
                minimum=1,
                maximum=300,
                step=1,
                value=90
            ),
            gr.Slider(
                label="Select Max Sentence Size",
                minimum=-1,
                maximum=500,
                step=1,
                value=-1
            ),
            gr.Checkbox(
                label="ignore_pfd_line_breaks",
                value=True
            ),
            gr.Textbox( # Added Gemini API Key input
                label="Gemini API Key (Optional)",
                placeholder="Enter your Gemini API Key here...",
                type="password" # Use password type for security
            )

        ],
        outputs=[
            gr.Plot(label="Chunking Report"),
            gr.HighlightedText(
                label="Tokenized Output",
                show_inline_category=False,
                elem_id="tokenized-output"

            )
            # gr.HTML(label="Tokenized Output")
        ],
        title="Persian RAG",
        description="Enter some text and see it tokenized with different colors for each chunk!",
        theme="default",
        css=css
    )



    retriever = gr.Interface(
        fn=retrieve_chunks,
        inputs=[
            gr.Textbox(
                label="Enter your query",
                placeholder="Type some text here...",
                lines=3
            ),
            gr.Slider(
                label="Select K",
                minimum=1,
                maximum=100,
                step=1,
                value=10
            ),
            gr.Checkbox(
                label="Include Neighbors",
                value=False
            ),
            gr.Checkbox(
                label="Replace With Parent Paragraph",
                value=False
            ),
            gr.Checkbox(
                label="Rerank",
                value=False
            ),

        ],
        outputs=[
            gr.HighlightedText(
                label="retrieved chunks",
                show_inline_category=False,
                elem_id="tokenized-output"
            )
            # gr.HTML(label="Tokenized Output")
        ],
        title="Retriever with Colored Output",
        theme="default",
        css=css
    )

    full_rag = gr.Interface(
        fn=full_rag_ask,
        inputs=[
            gr.Textbox(
                label="Enter your query",
                placeholder="Type some text here...",
                lines=3
            ),
            gr.Slider(
                label="Select K",
                minimum=1,
                maximum=100,
                step=1,
                value=10
            ),
            gr.Checkbox(
                label="Include Neighbors",
                value=False
            ),
            gr.Checkbox(
                label="Replace With Parent Paragraph",
                value=False
            ),
            gr.Checkbox(
                label="Rerank",
                value=False
            ),
        ],
        outputs=[
            gr.Textbox(
                label="RAG Output",
                lines=20
            ),
            gr.Textbox(
                label="LLM Messages History",
                lines=20
            )
        ],
        title="Full RAG with Raw Output",
        theme="default",
        css=css
    )

    full_tool_rag = gr.Interface(
        fn=full_tool_rag_ask,
        inputs=[
            gr.Textbox(
                label="Enter your query",
                placeholder="Type some text here...",
                lines=3
            ),
            gr.Checkbox(
                label="Include Neighbors",
                value=False
            ),
            gr.Checkbox(
                label="Replace With Parent Paragraph",
                value=False
            ),
            gr.Checkbox(
                label="Rerank",
                value=False
            ),
        ],
        outputs=[
            gr.Textbox(
                label="RAG Output",
                lines=20
            ),
            gr.Textbox(
                label="LLM Messages History",
                lines=20
            )
        ],
        title="Full Tool RAG with Raw Output",
        theme="default",
        css=css
    )

    iface = gr.TabbedInterface([chunker, retriever,full_rag,full_tool_rag], ["Chunker", "Retriever", "Full RAG","Full Tool RAG"])

    iface.launch(show_error=True)






