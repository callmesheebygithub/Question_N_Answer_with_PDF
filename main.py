# # streamlit_app.py

# import os
# import streamlit as st
# import final_app

# class StreamlitApp:
#     def __init__(self):
#         self.file_name = None
#         self.file_path = None
#         self.query = None

#     def main(self):
#         st.title("PDF File Uploader")
#         st.write("Upload a PDF file and save it to the specified directory.")

#         uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

#         if uploaded_file is not None:
#             SAVE_DIR = "docs"  # Adjust this path as needed
            
#             # Ensure the directory exists
#             os.makedirs(SAVE_DIR, exist_ok=True)
            
#             # Extract the filename from the uploaded file
#             self.file_name = uploaded_file.name
            
#             # Full path to save the file
#             self.file_path = os.path.join(SAVE_DIR, self.file_name)
            
#             # Save the uploaded file to the specified directory
#             with open(self.file_path, "wb") as f:
#                 f.write(uploaded_file.getbuffer())
            
#             # Get the query from the text input
#             self.query = st.text_input("Enter Your Query Here")

#             if self.query:  # Check if query is provided
#                 # Process the directory containing the saved file using FileReader
#                 object = final_app.FileReader(SAVE_DIR, self.query)
#                 answer = object.ollama_model()
#                 st.write(answer)
#             else:
#                 st.warning("Please enter a query.")

#         else:
#             st.warning("Please upload a PDF file.")

# if __name__ == "__main__":
#     app = StreamlitApp()
#     app.main()
import os
import streamlit as st
import final_app

class StreamlitApp:
    def __init__(self):
        self.file_name = None
        self.file_path = None
        self.query = None
        self.reader = None

    def main(self):
        st.title("PDF File Uploader")
        st.write("Upload a PDF file and save it to the specified directory.")

        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

        if uploaded_file is not None:
            SAVE_DIR = "docs"  # Adjust this path as needed
            os.makedirs(SAVE_DIR, exist_ok=True)
            self.file_name = uploaded_file.name
            self.file_path = os.path.join(SAVE_DIR, self.file_name)

            with open(self.file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            self.reader = final_app.FileReader(SAVE_DIR, "")
            st.success(f"File saved successfully at {self.file_path}")
            st.write("Processing completed. You can now enter your query.")

        self.query = st.text_input("Enter Your Query Here")

        if self.query and self.reader:
            self.reader.query = self.query
            answer = self.reader.ollama_model()
            st.write(answer)
        elif self.query and not self.reader:
            st.warning("Please upload a PDF file first.")

if __name__ == "__main__":
    app = StreamlitApp()
    app.main()
