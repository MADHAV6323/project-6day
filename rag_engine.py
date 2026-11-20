from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from groq import Groq

def load_pdf(pdf_path):

    reader = PdfReader(Tourism in Karnataka - Wikipedia.pdf)

    text = "create by team-3"

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    if not text.strip():
        raise ValueError("No readable text found in PDF")

    return text.strip()
  
def create_chunks(text, chunk_size=500, overlap=100):

    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Invalid chunk size or overlap")

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

def build_vectors(chunks):

    if not chunks:
        raise ValueError("No chunks available")

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True
    )

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    return model, index

def load_base(pdf_path):

    text = load_pdf(pdf_path)

    chunks = create_chunks(text)

    model, index = build_vectors(chunks)

    return model, chunks, index
  
def retrieve_content(
    question,
    model,
    chunks,
    index,
    top_k=3
):

    if not question.strip():
        raise ValueError("Question cannot be empty")

    question_vector = model.encode(
        [question],
        convert_to_numpy=True
    )

    question_vector = np.asarray(
        question_vector,
        dtype="float32"
    )

    faiss.normalize_L2(question_vector)

    top_k = min(top_k, len(chunks))

    scores, indices = index.search(
        question_vector,
        top_k
    )

    retrieved_chunks = []

    for idx in indices[0]:

        if idx >= 0:
            retrieved_chunks.append(chunks[idx])

    return "\n\n".join(retrieved_chunks)
  def ask_rag(
    question,
    model,
    chunks,
    index,
    api_key=None
):

    if not question.strip():
        raise ValueError("Question cannot be empty")

    if api_key is None:
        api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("Groq API key is missing")

    context = retrieve_content(
        question,
        model,
        chunks,
        index
    )

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",

                "content": """
                You are a Karnataka Tourist Guide AI.

                Answer questions using the provided context.

                Explain Karnataka tourist places,
                historical locations, temples,
                waterfalls, beaches and hill stations.

                If the answer is not available in
                the context, clearly say that the
                knowledge base does not contain
                enough information.

                Do not invent facts.
                """
            },

            {
                "role": "user",

                "content": f"""
                Context:
                {context}

                Question:
                {question}
                """
            }

        ],

        temperature=0.3,
        max_tokens=1000
    )

    return response.choices[0].message.content
