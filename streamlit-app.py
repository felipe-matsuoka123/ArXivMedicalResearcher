import streamlit as st
import json
from agents import crew
from dotenv import load_dotenv
import os

# Define Streamlit app
def main():
    # Load environment variables
    load_dotenv()
    open_api_key = os.getenv("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = open_api_key

    st.title("ArXiv Research Tool")
    st.write("An interactive tool to explore research papers related to engineering, computer science, and healthcare from ArXiv.")

    # Input Section
    st.header("Search for Research Papers")
    user_query = st.text_area("Enter your research query (e.g., 'Mitigating AI bias in medical imaging'):")

    if st.button("Search Papers"):
        # Define inputs for the crew
        print(user_query)
        inputs = {"wish": user_query}

        # Initialize and execute the crew
        # Run the crew process
        with st.spinner("Fetching and processing research papers..."):
            #try:
            results = crew.kickoff(inputs=inputs)
            print(results)
            
            st.success("Search Complete! Here are the selected papers:")
            file_path = r'C:\Users\felip\OneDrive\Área de Trabalho\agentic arxiv\selected_papers.json'
            with open(file_path, 'r') as file:
                content = file.read()
                cleaned_output = content.strip('```')  # Removes the triple backticks
                cleaned_output = cleaned_output.replace("json\n", "", 1)  # Removes the "json" line
                parsed_result = json.loads(cleaned_output)

            

            # Display each paper
            for paper in parsed_result['papers']:
                st.subheader(paper["title"])
                authors = ", ".join(paper["authors"])
                st.write(f"**Authors:** {authors}")
                st.write(f"**Published:** {paper['published']}")
                st.write(f"**Abstract:** {paper['abstract']}")
                st.markdown(f"[PDF Link]({paper['PDF']})")
                st.write(f"**Why Selected:** {paper['explanation']}")
                st.write("---")
            #except Exception as e:
            #    st.error(f"An error occurred: {e}")

    # Footer
    st.write("Built with ❤️ using Streamlit and ArXiv API.")

# Run the app
if __name__ == "__main__":
    main()
    
