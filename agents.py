from crewai import Agent, Task, Crew
import arxiv
from pydantic import BaseModel
from crewai_tools import BaseTool
from typing import List

class ArxivSearchTool(BaseTool):
    name: str = "ArXiv Search Tool"
    description: str = (
        "Searches for research papers on the ArXiv platform based on a query. "
        "Returns a list of paper titles, abstracts, authors, and publication dates."
    )

    def _run(self, query: str, max_results: int = 5) -> str:
        try:
            search = arxiv.Search(
                query=query,
                max_results=30,
                sort_by=arxiv.SortCriterion.SubmittedDate
            )


            unique_titles = set()
            results = []

            for result in search.results():
                title = result.title.strip()
                if title not in unique_titles:
                    unique_titles.add(title)  
                    paper_info = (
                        f"Title: {result.title}\n"
                        f"Authors: {', '.join(author.name for author in result.authors)}\n"
                        f"Published: {result.published}\n"
                        f"Abstract: {result.summary[:700]}...\n"  
                        f"PDF: {result.pdf_url}\n"
                        + ("-" * 100)
                    )
                    results.append(paper_info)

            #print(f"DEBUG: Found {len(results)} results from ArXiv.")


            return "\n\n".join(results)
        except Exception as e:
            return f"An error occurred while searching on ArXiv: {e}"
    
class PaperDetail(BaseModel):
    title: str
    abstract: str
    authors: List[str] 
    published: str  
    PDF: str
    explanation: str  
class PaperInfo(BaseModel):
    papers: List[PaperDetail] 

query_generator = Agent(
    role="AI Research Query Engineer",
    goal=(
        "Given a user's prompt ({wish}), transform it into a focused and specialized ArXiv search query that directly addresses the user's input. "
        "The query should prioritize technical and methodological aspects aligned with the prompt, while maintaining potential adaptability to healthcare contexts. "
        "Avoid overly generic or irrelevant terms and focus on specificity and relevance to the user's request."
    ),
    backstory=(
        "You possess expertise in AI, machine learning, computer science (CS), and interdisciplinary research. "
        "You are skilled at creating highly targeted search queries that reflect the nuances of a user's prompt. "
        "While you aim to surface papers with potential applicability to healthcare, your primary focus is ensuring technical alignment with the user's input.\n\n"
        "You understand advanced technical terms and concepts like attention mechanisms, reinforcement learning, multimodal models, and convolutional neural networks. "
        "Your goal is to construct a query that effectively narrows down results on ArXiv to meet the user's needs."
    ),
    allow_delegation=False,
    verbose=False
)


arxiv_searcher = Agent(
    role="Senior Research Librarian (ArXiv Specialist)",
    goal=(
        "Retrieve the most relevant and impactful search results from the ArXiv platform "
        "to fulfill the research request as the primary objective."
        "You have to create the best query to search on Arxiv based on the used wish."
    ),
    backstory=(
        "You are a Senior Research Librarian specializing in academic research. Your expertise lies "
        "in navigating and extracting insights from platforms like ArXiv. "
        "Your primary goal is to ensure that the results are accurate, relevant, and comprehensive. You must deliver results with utmost clarity and precision, and make no assumptions. "
        "If additional context is needed, ask thoughtful follow-up questions to ensure your responses exceed expectations."
    ),
    allow_delegation=False,
    verbose=False,
    tools=[ArxivSearchTool()]
)

moderator = Agent(
    role="Research Paper Moderator",
    goal=(
        "Evaluate and select up to ten articles from the ArXiv search results that demonstrate strong potential for "
        "application in medical or clinical settings, maintaining a high standard of quality and relevance."
        "for each paper you have to provide an explanation of why this paper is relevant to the users prompt ({wish})."
    ),
    backstory=(
        "You are a Research Paper Moderator with a robust medical background and expertise in academic research "
        "evaluation. You excel at identifying studies that have clear applicability in healthcare—especially regarding "
        "clinical diagnostics, treatment strategies, medical imaging, and patient outcomes.\n\n"
        "Your primary task is to carefully review the articles retrieved from ArXiv, focusing on their relevance to "
        "the query's and {wish} goals, methodological soundness, and overall potential to advance medical knowledge or practice. "
        "You provide clear justifications for your decisions to ensure that others understand why each selected paper "
        "is important.\n\n"
        "Always prioritize clinical applicability, evidence-based methods, and potential impact on patient care. "
        "Avoid including articles that are outdated, vague about real-world use, or only tangentially related to "
        "medical research. Select no more than ten articles to maintain a concise yet impactful set of results."
    ),
    allow_delegation=False,
    verbose=False
)

json_writer_agent = Agent(
    role="JSON Writer",
    goal=(
        "Take a list of research papers and output a well-structured JSON file following the specified format. "
        "Ensure the JSON structure is correct, consistent, and valid."
    ),
    backstory=(
        "You specialize in formatting and structuring data into JSON files. Your primary task is to take data provided "
        "by other agents and convert it into a JSON file with a predefined structure."
    ),
    allow_delegation=False,
    verbose=False
)

generate_advanced_arxiv_query = Task(
    name="Generate Advanced ArXiv Query",
    description=(
        "Transform the user's prompt into a highly specialized ArXiv search query.\n\n"
        "1. Analyze the user's prompt ({wish}) to identify key technical terms and concepts.\n"
        "2. Construct a query that is directly aligned with the user's input, ensuring specificity and relevance.\n"
        "3. Avoid introducing unrelated terms or broad assumptions (e.g., unnecessary mentions of healthcare, unless explicitly part of the user's prompt).\n\n"
        "The final query should:\n"
        "- Be concise and targeted.\n"
        "- Use Boolean operators (AND, OR) to refine the search.\n"
        "- Include only terms relevant to the user's input."
    ),
    expected_output=(
        "A focused ArXiv search query string that directly reflects the user's input."
    ),
    agent=query_generator,
    verbose=True
)


retrieve_research_papers = Task(
    name="Retrieve Research Papers",
    description=(
        "It was requested a detailed list of relevant papers on a specific topic:\n"
        "{wish}\n\n"
        "Your goal is to:\n"
        "1) Take the refined query generated by the AI Research Query Engineer agent.\n"
        "2) Use the ArXiv tool with the refined query to search for relevant papers.\n"
        "3) Return the list of retrieved papers (title, abstract, authorship information, publication date) "
        "to the Research Paper Moderator for further filtering and selection.\n\n"
        "Make sure to include in your output:\n"
        "- The exact query used for searching ArXiv.\n"
        "- A list of all research papers that match this query.\n"
    ),
    expected_output=(
        "A JSON-like structure containing:\n"
        "1) 'used_query': the exact query string sent to ArXiv.\n"
        "2) 'papers': single list of objects, each with 'title', 'abstract', 'authors', 'published', 'PDF' fields "
        "that are most relevant to the user's query."
    ),
    agent=arxiv_searcher, 
)



select_and_explain_papers = Task(
    name="Select and Explain Papers",
    description=(
        "Review a list of research papers selected by the Senior Research Librarian (ArXiv Specialist) and "
        "select the most relevant ones based on their alignment with the user's objective ({wish}).\n\n"
        "For each selected paper, save the following details:\n"
        "- 'title': The title of the paper.\n"
        "- 'abstract': A brief summary of the paper.\n"
        "- 'authors': A list of the authors' names.\n"
        "- 'published': The publication date in 'YYYY-MM-DD' format.\n"
        "- 'PDF': A link to the PDF of the paper.\n"
        "- 'explanation': A specific explanation of why the paper was selected, focusing on its relevance to the user's objective ({wish}).\n\n"
        "The paper does not have to be directly related to healthcare, but it has to have some applicability to healthcare."
        "In the explantion, write an insight about how the paper can be applied to healthcare even though it's main purpose was other."
        "Try to aggregate the technical aspect of the paper with the healthcare aspect."
        "Output a list of dictionaries where each dictionary contains the above fields.\n\n"
        "Do not write generic explanations; be specific, make references to the user's prompt ({wish}) and to the current paper."
    ),
    expected_output=(
        "A list of dictionaries where each dictionary contains:\n"
        "- 'title': The paper's title.\n"
        "- 'abstract': A summary of the paper.\n"
        "- 'authors': A list of authors.\n"
        "- 'published': The publication date.\n"
        "- 'PDF': A link to the paper's PDF.\n"
        "- 'explanation': A specific explanation of why the paper was selected.\n\n"
    ),
    agent=moderator
)


write_json_task = Task(
    name="Write JSON File",
    description=(
        "Take a list of research papers and structure them into a JSON file. Each paper must be represented as a "
        "dictionary with the following fields:\n"
        "  - 'title': The title of the paper.\n"
        "  - 'abstract': A brief summary of the paper.\n"
        "  - 'authors': A list of author names.\n"
        "  - 'published': The publication date in 'YYYY-MM-DD' format.\n"
        "  - 'PDF': The URL to the PDF version of the paper.\n"
        "  - 'explanation': A brief explanation of why the paper was selected.\n\n"
    ),
    expected_output=(
        "A JSON object with a single key, 'papers', containing a list of dictionaries. Each dictionary must have the "
        "specified fields and follow the defined structure. If no papers are provided, return an empty list for 'papers'."
        "Return the JSON object in this format:\n"
        "a list of dictionaries with the following fields:\n"
        "  - 'title': The title of the paper.\n"
        "  - 'abstract': A brief summary of the paper.\n"
        "  - 'authors': A list of author names.\n"
        "  - 'published': The publication date in 'YYYY-MM-DD' format.\n"
        "  - 'PDF': The URL to the PDF version of the paper.\n"
        "  - 'explanation': A brief explanation of why the paper was selected.\n\n"
        
    ),
    agent=json_writer_agent,
    output_json=PaperInfo,
    output_file="selected_papers.json"
)

crew = Crew(
    agents=[query_generator, arxiv_searcher, moderator, json_writer_agent], 
    tasks=[generate_advanced_arxiv_query,retrieve_research_papers,select_and_explain_papers, write_json_task],  
    verbose=True
)
