# import streamlit as st
# import os
# import tempfile
# from code_review.crew import run_code_review, CodeReview

# # Configure the page
# st.set_page_config(
#     page_title="AI Code Review Assistant",
#     page_icon="🔍",
#     layout="wide"
# )

# st.markdown("""
# <div style='text-align: center; background-color: #f0f2f6; padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem'>
#     <h1 style='color: #1E3A8A'>AI Code Review Assistant</h1>
#     <p style='font-size: 1.1rem'>Analyze, improve, and optimize your code with AI-powered insights</p>
# </div>""", unsafe_allow_html=True)

# st.markdown("### How Our AI Code Review Works")
# st.markdown("<hr>", unsafe_allow_html=True)

# # Main container for settings and code input
# main_container = st.container()



# def display_code_result(review_result):
#     """
#     Enhanced method to display code review results using Streamlit components
#     """
#     # Extract key components from review result
#     final_output = review_result.get("combined_output", str(review_result))
#     request_type = review_result.get("request_type", "general")
    
#     # Parsing helpers
#     def extract_section(output, section_name):
#         """Extract specific sections from the output"""
#         try:
#             if section_name in output:
#                 return output.split(f"{section_name}:")[1].split("\n\n")[0].strip()
#         except:
#             pass
#         return ""

#     # Extract sections
#     language = extract_section(final_output, "Language") or "Not detected"
#     explanation = extract_section(final_output, "Explanation") or final_output
#     structure = extract_section(final_output, "Structure Analysis") or ""
#     response = extract_section(final_output, "Response") or ""

#     # Color and icon mapping for different request types
#     type_styles = {
#         "debug": {
#             "color": "red",
#             "icon": "🐛",
#             "title": "Debugging Results"
#         },
#         "refactor": {
#             "color": "green",
#             "icon": "🔧",
#             "title": "Code Optimization"
#         },
#         "explain": {
#             "color": "blue",
#             "icon": "📘",
#             "title": "Code Explanation"
#         },
#         "specific_error": {
#             "color": "orange",
#             "icon": "⚠️",
#             "title": "Error Analysis"
#         },
#         "general": {
#             "color": "purple",
#             "icon": "📊",
#             "title": "Code Review"
#         }
#     }

#     # Get style for the current request type
#     style = type_styles.get(request_type, type_styles["general"])

#     # Main result display
#     st.markdown(f"## {style['icon']} {style['title']}")
    
#     # Language Detection Card
#     st.info(f"Detected Language: {language}")

#     # Explanation Card
#     st.markdown(f"""
#     ### 📝 Key Insights
#     {explanation}
#     """)

#     # Conditional sections
#     if structure:
#         st.markdown(f"""
#         ### 🔍 Structure Analysis
#         {structure}
#         """)

#     if response:
#         st.markdown(f"""
#         ### 💡 Recommendations
#         {response}
#         """)

#     # Code Display (if applicable)
#     def display_code_card(title, code, language="python"):
#         """Helper to display code in a clean card"""
#         with st.expander(title):
#             st.code(code, language=language)

#     # Optionally display code if there are code snippets in the result
#     if "```" in final_output:
#         code_snippets = [snippet.strip() for snippet in final_output.split("```") if snippet.strip()]
#         for i, code_snippet in enumerate(code_snippets, 1):
#             # Try to detect language
#             detected_language = "python"  # Default
#             for lang in ["python", "javascript", "java", "cpp", "rust", "go"]:
#                 if lang in code_snippet.lower():
#                     detected_language = lang
#                     break
            
#             display_code_card(f"Code Snippet {i}", code_snippet, detected_language)

#     # Download Report Button
#     report_content = f"""# {style['title']}

# ## Analysis Details
# {final_output}
#     """
#     st.download_button(
#         label="📥 Download Full Report",
#         data=report_content,
#         file_name=f"code_review_report_{request_type}.md",
#         mime="text/markdown",
#         use_container_width=True
#     )


# # Initialize session state flags if not already set
# if "input_mode" not in st.session_state:
#     st.session_state.input_mode = None
# def handle_large_file_upload(uploaded_file, max_file_size_mb=10):
#     """
#     Safely handle large file uploads with size and content validation.
    
#     Args:
#         uploaded_file (UploadedFile): Streamlit uploaded file object
#         max_file_size_mb (int): Maximum allowed file size in megabytes
    
#     Returns:
#         tuple: (file_content, error_message)
#     """
#     # Check if file is uploaded
#     if uploaded_file is None:
#         return None, "No file uploaded."
    
#     # Check file size
#     file_size_bytes = uploaded_file.size
#     file_size_mb = file_size_bytes / (1024 * 1024)
    
#     if file_size_mb > max_file_size_mb:
#         return None, f"File too large. Maximum file size is {max_file_size_mb} MB."
    
#     try:
#         # Read file content
#         file_content = uploaded_file.getvalue().decode("utf-8")
        
#         # Additional content validation
#         if not file_content.strip():
#             return None, "The uploaded file is empty."
        
#         # Line count for large file detection
#         line_count = len(file_content.split('\n'))
        
#         return file_content, None
    
#     except UnicodeDecodeError:
#         return None, "Unable to decode file. Please ensure it's a text file."
#     except Exception as e:
#         return None, f"Error processing file: {str(e)}"

# def sample_large_file(file_content, max_lines=500):
#     """
#     Sample a large file to make analysis more manageable.
    
#     Args:
#         file_content (str): Full file content
#         max_lines (int): Maximum number of lines to retain
    
#     Returns:
#         str: Sampled file content
#     """
#     lines = file_content.split('\n')
    
#     if len(lines) <= max_lines:
#         return file_content
    
#     # Take first 100 lines
#     start_sample = '\n'.join(lines[:100])
    
#     # Take last 100 lines
#     end_sample = '\n'.join(lines[-100:])
    
#     # Take middle section
#     middle_start = len(lines) // 2 - 50
#     middle_sample = '\n'.join(lines[middle_start:middle_start+100])
    
#     # Combine samples with markers
#     sampled_content = f"""{start_sample}

# # [LARGE FILE: Middle section omitted for brevity]

# {middle_sample}

# # [LARGE FILE: End section follows]

# {end_sample}"""
    
#     return sampled_content
# with main_container:
#     # Settings (without programming language selection)
#     col1, col2= st.columns(2)
    
#     # with col1:
#     #     st.markdown("#### Review Configuration")
#     #     review_depth = st.select_slider(
#     #         "Review Depth",
#     #         options=["Basic", "Standard", "Comprehensive"],
#     #         value="Standard",
#     #         help="Controls how detailed the code review will be"
#     #     )
    
#     with col1:
#         st.markdown("#### Focus Areas")
#         focus_areas = st.multiselect(
#             "Select focus areas",
#             options=["Syntax", "Security", "Performance", "Readability", "Maintainability"],
#             default=["Syntax", "Performance", "Readability"],
#             help="Select areas to focus on during the review"
#         )
    
#     with col2:
#         st.markdown("#### Additional Options")
#         language_specific = st.checkbox(
#             "Enable language-specific rules",
#             value=True,
#             help="Apply language-specific best practices (the LLM will detect the language from your code)"
#         )
#         include_examples = st.checkbox(
#             "Include examples in feedback",
#             value=True,
#             help="Show example solutions for identified issues"
#         )
#         debug_mode = st.checkbox(
#             "Debug mode",
#             value=False,
#             help="Show additional debug information and detailed analysis logs"
#         )
    
#     st.markdown("<hr>", unsafe_allow_html=True)
    
#     # Code input section with two input methods
#     st.markdown("## Code Input")
#     input_tab1, input_tab2 = st.tabs(["📝 Enter Code", "📁 Upload File"])
    
#     code_input = ""
#     with input_tab1:
#         if st.session_state.input_mode == "file":
#             st.info("You have already uploaded a file. Switching to text input will clear the uploaded file.")
#             if st.button("Switch to Text Input"):
#                 st.session_state.input_mode = "text"
#                 st.session_state.uploaded_file = None
#                 st.rerun()

#         elif st.session_state.input_mode in [None, "text"]:
#             pasted_code = st.text_area(
#                 "Paste your code here:",
#                 height=250,
#                 help="Enter the code you want to analyze"
#             )

#             if pasted_code.strip():
#                 st.session_state.input_mode = "text"
#                 code_input = pasted_code

#     # === 📁 File Upload Tab ===
#     with input_tab2:
#         if st.session_state.input_mode == "text":
#             st.info("You have already entered text input. Switching to file upload will clear the text input.")
#             if st.button("Switch to File Upload"):
#                 st.session_state.input_mode = "file"
#                 st.session_state.pasted_code = ""
#                 st.rerun()

#         elif st.session_state.input_mode in [None, "file"]:
#             uploaded_file = st.file_uploader(
#                 "Upload a code file",
#                 type=["py", "js", "java", "cpp", "cs", "go", "rb", "php", "html", "css", "txt"],
#                 help="Only one input method is allowed. Uploading a file disables the text input."
#             )

#             if uploaded_file:
#                 st.session_state.input_mode = "file"
#                 uploaded_content, upload_error = handle_large_file_upload(uploaded_file, max_file_size_mb=10)

#                 if upload_error:
#                     st.error(upload_error)
#                 else:
#                     if len(uploaded_content.split('\n')) > 500:
#                         st.warning("Large file detected. File will be sampled.")
#                         uploaded_content = sample_large_file(uploaded_content)

#                     st.code(uploaded_content[:1000] + ("..." if len(uploaded_content) > 1000 else ""), language="python", line_numbers=True)
#                     code_input = uploaded_content
#     # Additional query input for specific code questions/instructions
#     user_query = st.text_input(
#         "Have a specific question or instruction about your code? Ask here:",
#         placeholder="E.g., 'Debug this code', 'Explain this function', 'Refactor for better performance', or 'Fix error on line 42'",
#         help="Enter any specific request about your code. You can ask for debugging help, code explanation, refactoring suggestions, or to fix specific errors."
#     )
    
#     # Collect settings
#     settings = {
#         "focus_areas": focus_areas,
#         "language_specific": language_specific,
#         "include_examples": include_examples,
#         "debug_mode": debug_mode,
#     }
    
#     # Model selection section
#     st.markdown("## Model Selection")
#     st.markdown("Select which language model you want to use for the analysis:")
    
#     model_col1, model_col2 = st.columns(2)
    
#     with model_col1:
#         llm_provider = st.selectbox(
#             "Language Model Provider",
#             options=["azure", "mistral"],
#             format_func=lambda x: {
#                 "azure": "Azure OpenAI (GPT-4o)",
#                 "mistral": "Mistral AI (Large)"
#             }.get(x, x),
#             help="Choose the AI model to analyze your code"
#         )
        
#         # Add model info based on selection
#         if llm_provider == "azure":
#             st.info("GPT-4o: Advanced code understanding with strong multi-language support")
#         elif llm_provider == "mistral":
#             st.info("Mistral Large: Efficient code analysis with strong reasoning capabilities")
    
    
#     # Add model selection to settings
#     settings["llm_provider"] = llm_provider
    
#     # Center the review button
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col1:
#         review_button = st.button(
#             "📊 Review Code", 
#             type="primary", 
#             disabled=not code_input,
#             use_container_width=True
#         )
    
#     if review_button and code_input:
#         with st.spinner(f"AI agents are reviewing your code using {llm_provider.capitalize()}..."):
#             try:
#                 # Simulate progress phases
#                 progress_container = st.container()
#                 with progress_container:
#                     progress_bar = st.progress(0)
#                     phases = [
#                         {"name": "Language Detection", "icon": "🔍", "description": "Identifying programming language..."},
#                         {"name": "Code Analysis", "icon": "🧮", "description": "Analyzing code structure and patterns..."},
#                         {"name": "Processing User Query", "icon": "💭", "description": "Addressing specific user requirements..."},
#                         {"name": "Generating Final Output", "icon": "✨", "description": "Compiling comprehensive review..."}
#                     ]
                    
#                     # Customize phases based on user query type
#                     if user_query and "debug" in user_query.lower():
#                         phases[2]["description"] = "Debugging code and identifying issues..."
#                         phases[3]["description"] = "Generating debugging recommendations..."
#                     elif user_query and any(word in user_query.lower() for word in ["refactor", "improve", "optimize"]):
#                         phases[2]["description"] = "Identifying optimization opportunities..."
#                         phases[3]["description"] = "Generating refactored code suggestions..."
#                     elif user_query and any(word in user_query.lower() for word in ["explain", "understand", "what does"]):
#                         phases[2]["description"] = "Analyzing code functionality..."
#                         phases[3]["description"] = "Generating detailed explanation..."
#                     elif user_query and any(word in user_query.lower() for word in ["error", "fix", "issue"]):
#                         phases[2]["description"] = "Diagnosing specific errors..."
#                         phases[3]["description"] = "Generating targeted solutions..."
                    
#                     for i, phase in enumerate(phases):
#                         progress_percent = (i + 0.5) * (100/len(phases))
#                         progress_bar.progress(int(progress_percent))
#                         st.markdown(f"**{phase['icon']} Phase {i+1}: {phase['name']}** - {phase['description']}")
#                     progress_bar.progress(100)
                
#                 # Run code review with user query
#                 review_result = run_code_review(code_input, settings, user_query)
                
#                 # Display file size information if it's a large file
#                 if "file_info" in review_result:
#                     st.markdown("""
#                     <div style='background-color: #fff3cd; padding: 0.75rem; border-radius: 0.5rem; border-left: 5px solid #ffc107; margin: 1rem 0'>
#                         <h4 style='color: #856404'>Large File Detected</h4>
#                         <p>{}</p>
#                         <p>Analysis will focus on high-level architecture and main components rather than detailed line-by-line review.</p>
#                     </div>
#                     """.format(review_result["file_info"]), unsafe_allow_html=True)
                
#                 # Display model information
#                 if "model_info" in review_result:
#                     model_color = {
#                         "azure": "#0078D4",
#                         "mistral": "#6B46C1"
#                     }.get(settings.get("llm_provider", "azure"), "#4CAF50")
                    
#                     st.markdown(f"""
#                     <div style='background-color: #f8f9fa; padding: 0.75rem; border-radius: 0.5rem; border-left: 5px solid {model_color}; margin: 1rem 0'>
#                         <h4 style='color: {model_color}'>Model Information</h4>
#                         <p>{review_result["model_info"]}</p>
#                         <p>Each model has different strengths and may provide varying insights.</p>
#                     </div>
#                     """, unsafe_allow_html=True)
                
#                 # Display appropriate heading based on request type
#                 if "request_type" in review_result:
#                     request_type = review_result["request_type"]
#                     if request_type == "debug":
#                         review_heading = "Debugging Results"
#                         review_description = "The AI agents have analyzed your code for errors and bugs. Below are the findings and recommended fixes."
#                     elif request_type == "refactor":
#                         review_heading = "Code Optimization Results"
#                         review_description = "The AI agents have identified optimization opportunities. Below are the recommended code improvements."
#                     elif request_type == "explain":
#                         review_heading = "Code Explanation"
#                         review_description = "The AI agents have analyzed your code structure and functionality. Below is a detailed explanation."
#                     elif request_type == "specific_error":
#                         review_heading = "Error Analysis Results"
#                         review_description = "The AI agents have analyzed the specific issues in your code. Below are the targeted solutions."
#                     else:
#                         review_heading = "Review Complete"
#                         review_description = "The AI agents have completed their analysis. Below is the consolidated final output."
#                 else:
#                     review_heading = "Review Complete"
#                     review_description = "The AI agents have completed their analysis. Below is the consolidated final output."
                
#                 st.markdown(f"""
#                 <div style='background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; border-left: 5px solid #4CAF50; margin: 1rem 0'>
#                     <h2 style='color: #2E7D32'>{review_heading}</h2>
#                     <p>{review_description}</p>
#                 </div>
#                 """, unsafe_allow_html=True)
                
#                 # Display only the final consolidated output
#                 final_output = review_result.get("combined_output", str(review_result))
#                 if "user_query" in review_result:
#                     st.markdown("### Your Question/Instruction:")
#                     st.info(review_result["user_query"])
#                     st.markdown("### Analysis:")
                    
#                 # Format the output in a more structured way
#                 try:
#                     # Get language
#                     if "Language:" in final_output:
#                         language = final_output.split("Language:")[1].split("\n")[0].strip()
#                     else:
#                         language = "Not detected"
                    
#                     # Get explanation
#                     if "Explanation:" in final_output and "Structure Analysis:" in final_output:
#                         explanation = final_output.split("Explanation:")[1].split("Structure Analysis:")[0].strip()
#                     elif "Explanation:" in final_output and "Response:" in final_output:
#                         explanation = final_output.split("Explanation:")[1].split("Response:")[0].strip()
#                     elif "Explanation:" in final_output:
#                         explanation = final_output.split("Explanation:")[1].strip()
#                     else:
#                         explanation = final_output.strip()
                    
#                     # Get structure analysis
#                     if "Structure Analysis:" in final_output and "Response:" in final_output:
#                         structure = final_output.split("Structure Analysis:")[1].split("Response:")[0].strip()
#                     elif "Structure Analysis:" in final_output:
#                         structure = final_output.split("Structure Analysis:")[1].strip()
#                     else:
#                         structure = ""
                    
#                     # Get response
#                     if "Response:" in final_output:
#                         response = final_output.split("Response:")[1].strip()
#                     else:
#                         response = ""
                    
#                     # Handle different request types with appropriate UI elements
#                     request_type = review_result.get("request_type", "general")
                    
#                     # Customize UI based on request type
#                     if request_type == "debug":
#                         st.markdown("""
#                         <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; margin: 1rem 0; border-left: 5px solid #dc3545'>
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #dc3545'>Identified Issues:</h4>
#                                 <p>{explanation}</p>
#                             </div>
#                             {structure_section}
#                             {response_section}
#                         </div>
#                         """.format(
#                             explanation=explanation,
#                             structure_section=f"""
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #dc3545'>Debugging Recommendations:</h4>
#                                 <p>{structure}</p>
#                             </div>
#                             """ if structure else "",
#                             response_section=f"""
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #dc3545'>Suggested Fixes:</h4>
#                                 <p>{response}</p>
#                             </div>
#                             """ if response else ""
#                         ), unsafe_allow_html=True)
#                     elif request_type == "refactor":
#                         st.markdown("""
#                         <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; margin: 1rem 0; border-left: 5px solid #28a745'>
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #28a745'>Current Implementation:</h4>
#                                 <p>{explanation}</p>
#                             </div>
#                             {structure_section}
#                             {response_section}
#                         </div>
#                         """.format(
#                             explanation=explanation,
#                             structure_section=f"""
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #28a745'>Optimization Opportunities:</h4>
#                                 <p>{structure}</p>
#                             </div>
#                             """ if structure else "",
#                             response_section=f"""
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #28a745'>Refactored Code Suggestions:</h4>
#                                 <p>{response}</p>
#                             </div>
#                             """ if response else ""
#                         ), unsafe_allow_html=True)
#                     elif request_type == "explain":
#                         st.markdown("""
#                         <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; margin: 1rem 0; border-left: 5px solid #17a2b8'>
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #17a2b8'>Code Explanation:</h4>
#                                 <p>{explanation}</p>
#                             </div>
#                             {structure_section}
#                             {response_section}
#                         </div>
#                         """.format(
#                             explanation=explanation,
#                             structure_section=f"""
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #17a2b8'>Code Structure:</h4>
#                                 <p>{structure}</p>
#                             </div>
#                             """ if structure else "",
#                             response_section=f"""
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #17a2b8'>Additional Notes:</h4>
#                                 <p>{response}</p>
#                             </div>
#                             """ if response else ""
#                         ), unsafe_allow_html=True)
#                     elif request_type == "specific_error":
#                         st.markdown("""
#                         <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; margin: 1rem 0; border-left: 5px solid #ffc107'>
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #ffc107'>Error Analysis:</h4>
#                                 <p>{explanation}</p>
#                             </div>
#                             {structure_section}
#                             {response_section}
#                         </div>
#                         """.format(
#                             explanation=explanation,
#                             structure_section=f"""
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #ffc107'>Context:</h4>
#                                 <p>{structure}</p>
#                             </div>
#                             """ if structure else "",
#                             response_section=f"""
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #ffc107'>Solution:</h4>
#                                 <p>{response}</p>
#                             </div>
#                             """ if response else ""
#                         ), unsafe_allow_html=True)
#                     else:
#                         st.markdown("""
#                         <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; margin: 1rem 0'>
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #1E3A8A'>Code Explanation:</h4>
#                                 <p>{explanation}</p>
#                             </div>
#                             {structure_section}
#                             {response_section}
#                         </div>
#                         """.format(
#                             explanation=explanation,
#                             structure_section=f"""
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #1E3A8A'>Structure Analysis:</h4>
#                                 <p>{structure}</p>
#                             </div>
#                             """ if structure else "",
#                             response_section=f"""
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #1E3A8A'>Response to Your Query:</h4>
#                                 <p>{response}</p>
#                             </div>
#                             """ if response else ""
#                         ), unsafe_allow_html=True)
                    
#                 except Exception as e:
#                     st.error(f"Error parsing output: {str(e)}")
#                     st.write("Raw output:")
#                     st.write(final_output)
                
#                 # Provide a download button for the final report
#                 report_title = "Code Review Report"
#                 if request_type == "debug":
#                     report_title = "Code Debugging Report"
#                 elif request_type == "refactor":
#                     report_title = "Code Optimization Report"
#                 elif request_type == "explain":
#                     report_title = "Code Explanation Report"
#                 elif request_type == "specific_error":
#                     report_title = "Error Analysis Report"
                
#                 report_content = f"""# {report_title}

# ## Your Question/Instruction
# {review_result.get("user_query", "")}

# ## Analysis
# {final_output}
#                 """
#                 st.download_button(
#                     label="📥 Download Report",
#                     data=report_content,
#                     file_name=f"{report_title.lower().replace(' ', '_')}.md",
#                     mime="text/markdown",
#                     use_container_width=True
#                 )
                
#                 # Show debug information if enabled
#                 if settings.get("debug_mode", False):
#                     with st.expander("Debug Information"):
#                         debug_tab1, debug_tab2, debug_tab3 = st.tabs(["Analysis Output", "Process Details", "Model Information"])
                        
#                         with debug_tab1:
#                             st.subheader("Raw LLM Response")
#                             st.code(final_output, language="text")
#                             st.subheader("Parsed Results")
#                             st.json(review_result)
#                             st.subheader("Request Type")
#                             st.write(f"Detected request type: {request_type}")
                        
#                         with debug_tab2:
#                             st.subheader("Settings")
#                             st.json(settings)
#                             st.subheader("Agent Process")
#                             st.write("The code was analyzed by three AI agents:")
#                             st.write("1. **Code Analysis Expert** - Identified code issues and patterns")
#                             st.write("2. **Code Review Specialist** - Provided feedback on findings")
#                             st.write("3. **Code Optimization Specialist** - Suggested improvements")
                        
#                         with debug_tab3:
#                             st.subheader("Model Information")
#                             st.write(f"**Selected Model**: {settings.get('llm_provider', 'azure').capitalize()}")
                            
#                             if settings.get("llm_provider") == "azure":
#                                 st.write("**Model**: GPT-4o")
#                                 st.write("**Provider**: Azure OpenAI")
#                                 st.write("**Strengths**: Advanced reasoning, strong understanding of complex code patterns, excellent multi-language support")
#                                 st.write("**Best for**: Complex code analysis, detailed explanations, architectural insights")
#                             elif settings.get("llm_provider") == "mistral":
#                                 st.write("**Model**: Mistral Large")
#                                 st.write("**Provider**: Mistral AI")
#                                 st.write("**Strengths**: Fast analysis, efficient reasoning, good balance of speed and accuracy")
#                                 st.write("**Best for**: Quick code reviews, straightforward debugging suggestions, performance optimizations")
                            
#                             st.write("**API Key Status**: ✅ Configured")
                
#                 if st.button("🔄 New Review", use_container_width=True):
#                     st.session_state.clear()
#                     st.rerun()
            
#             except Exception as e:
#                 st.error(f"An error occurred during code review: {str(e)}")
#                 st.code(f"Error details:\n{str(e)}", language="python")
                
#                 if settings.get("debug_mode", False):
#                     with st.expander("Debug Information (Error)"):
#                         st.subheader("Exception Details")
#                         st.exception(e)
#                         st.subheader("Settings")
#                         st.json(settings)
#                         st.subheader("Input Code Length")
#                         st.write(f"Code input length: {len(code_input)} characters, {len(code_input.split('//n'))} lines")



# import streamlit as st
# import os
# import tempfile
# from code_review.crew import run_code_review, CodeReview

# # Configure the page
# st.set_page_config(
#     page_title="AI Code Review Assistant",
#     page_icon="🔍",
#     layout="wide"
# )

# st.markdown("""
# <div style='text-align: center; background-color: #f0f2f6; padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem'>
#     <h1 style='color: #1E3A8A'>AI Code Review Assistant</h1>
#     <p style='font-size: 1.1rem'>Analyze, improve, and optimize your code with AI-powered insights</p>
# </div>""", unsafe_allow_html=True)

# st.markdown("### How Our AI Code Review Works")
# st.markdown("<hr>", unsafe_allow_html=True)

# # Main container for settings and code input
# main_container = st.container()

# # Initialize session state flags if not already set
# if "input_mode" not in st.session_state:
#     st.session_state.input_mode = None
# def handle_large_file_upload(uploaded_file, max_file_size_mb=10):
#     """
#     Safely handle large file uploads with size and content validation.
    
#     Args:
#         uploaded_file (UploadedFile): Streamlit uploaded file object
#         max_file_size_mb (int): Maximum allowed file size in megabytes
    
#     Returns:
#         tuple: (file_content, error_message)
#     """
#     # Check if file is uploaded
#     if uploaded_file is None:
#         return None, "No file uploaded."
    
#     # Check file size
#     file_size_bytes = uploaded_file.size
#     file_size_mb = file_size_bytes / (1024 * 1024)
    
#     if file_size_mb > max_file_size_mb:
#         return None, f"File too large. Maximum file size is {max_file_size_mb} MB."
    
#     try:
#         # Read file content
#         file_content = uploaded_file.getvalue().decode("utf-8")
        
#         # Additional content validation
#         if not file_content.strip():
#             return None, "The uploaded file is empty."
        
#         # Line count for large file detection
#         line_count = len(file_content.split('\n'))
        
#         return file_content, None
    
#     except UnicodeDecodeError:
#         return None, "Unable to decode file. Please ensure it's a text file."
#     except Exception as e:
#         return None, f"Error processing file: {str(e)}"

# def sample_large_file(file_content, max_lines=500):
#     """
#     Sample a large file to make analysis more manageable.
    
#     Args:
#         file_content (str): Full file content
#         max_lines (int): Maximum number of lines to retain
    
#     Returns:
#         str: Sampled file content
#     """
#     lines = file_content.split('\n')
    
#     if len(lines) <= max_lines:
#         return file_content
    
#     # Take first 100 lines
#     start_sample = '\n'.join(lines[:100])
    
#     # Take last 100 lines
#     end_sample = '\n'.join(lines[-100:])
    
#     # Take middle section
#     middle_start = len(lines) // 2 - 50
#     middle_sample = '\n'.join(lines[middle_start:middle_start+100])
    
#     # Combine samples with markers
#     sampled_content = f"""{start_sample}

# # [LARGE FILE: Middle section omitted for brevity]

# {middle_sample}

# # [LARGE FILE: End section follows]

# {end_sample}"""
    
#     return sampled_content
# with main_container:
#     # Settings (without programming language selection)
#     col1, col2= st.columns(2)
    
#     # with col1:
#     #     st.markdown("#### Review Configuration")
#     #     review_depth = st.select_slider(
#     #         "Review Depth",
#     #         options=["Basic", "Standard", "Comprehensive"],
#     #         value="Standard",
#     #         help="Controls how detailed the code review will be"
#     #     )
    
#     with col1:
#         st.markdown("#### Focus Areas")
#         focus_areas = st.multiselect(
#             "Select focus areas",
#             options=["Syntax", "Security", "Performance", "Readability", "Maintainability"],
#             default=["Syntax", "Performance", "Readability"],
#             help="Select areas to focus on during the review"
#         )
    
#     with col2:
#         st.markdown("#### Additional Options")
#         language_specific = st.checkbox(
#             "Enable language-specific rules",
#             value=True,
#             help="Apply language-specific best practices (the LLM will detect the language from your code)"
#         )
#         include_examples = st.checkbox(
#             "Include examples in feedback",
#             value=True,
#             help="Show example solutions for identified issues"
#         )
#         debug_mode = st.checkbox(
#             "Debug mode",
#             value=False,
#             help="Show additional debug information and detailed analysis logs"
#         )
    
#     st.markdown("<hr>", unsafe_allow_html=True)
    
#     # Code input section with two input methods
#     st.markdown("## Code Input")
#     input_tab1, input_tab2 = st.tabs(["📝 Enter Code", "📁 Upload File"])
    
#     code_input = ""
#     with input_tab1:
#         if st.session_state.input_mode == "file":
#             st.info("You have already uploaded a file. Switching to text input will clear the uploaded file.")
#             if st.button("Switch to Text Input"):
#                 st.session_state.input_mode = "text"
#                 st.session_state.uploaded_file = None
#                 st.rerun()

#         elif st.session_state.input_mode in [None, "text"]:
#             pasted_code = st.text_area(
#                 "Paste your code here:",
#                 height=250,
#                 help="Enter the code you want to analyze"
#             )

#             if pasted_code.strip():
#                 st.session_state.input_mode = "text"
#                 code_input = pasted_code

#     # === 📁 File Upload Tab ===
#     with input_tab2:
#         if st.session_state.input_mode == "text":
#             st.info("You have already entered text input. Switching to file upload will clear the text input.")
#             if st.button("Switch to File Upload"):
#                 st.session_state.input_mode = "file"
#                 st.session_state.pasted_code = ""
#                 st.rerun()

#         elif st.session_state.input_mode in [None, "file"]:
#             uploaded_file = st.file_uploader(
#                 "Upload a code file",
#                 type=["py", "js", "java", "cpp", "cs", "go", "rb", "php", "html", "css", "txt"],
#                 help="Only one input method is allowed. Uploading a file disables the text input."
#             )

#             if uploaded_file:
#                 st.session_state.input_mode = "file"
#                 uploaded_content, upload_error = handle_large_file_upload(uploaded_file, max_file_size_mb=10)

#                 if upload_error:
#                     st.error(upload_error)
#                 else:
#                     if len(uploaded_content.split('\n')) > 500:
#                         st.warning("Large file detected. File will be sampled.")
#                         uploaded_content = sample_large_file(uploaded_content)

#                     st.code(uploaded_content[:1000] + ("..." if len(uploaded_content) > 1000 else ""), language="python", line_numbers=True)
#                     code_input = uploaded_content
#     # Additional query input for specific code questions/instructions
#     user_query = st.text_input(
#         "Have a specific question or instruction about your code? Ask here:",
#         placeholder="E.g., 'Debug this code', 'Explain this function', 'Refactor for better performance', or 'Fix error on line 42'",
#         help="Enter any specific request about your code. You can ask for debugging help, code explanation, refactoring suggestions, or to fix specific errors."
#     )
    
#     # Collect settings
#     settings = {
#         "focus_areas": focus_areas,
#         "language_specific": language_specific,
#         "include_examples": include_examples,
#         "debug_mode": debug_mode,
#     }
    
#     # Model selection section
#     st.markdown("## Model Selection")
#     st.markdown("Select which language model you want to use for the analysis:")
    
#     model_col1, model_col2 = st.columns(2)
    
#     with model_col1:
#         llm_provider = st.selectbox(
#             "Language Model Provider",
#             options=["azure", "mistral"],
#             format_func=lambda x: {
#                 "azure": "Azure OpenAI (GPT-4o)",
#                 "mistral": "Mistral AI (Large)"
#             }.get(x, x),
#             help="Choose the AI model to analyze your code"
#         )
        
#         # Add model info based on selection
#         if llm_provider == "azure":
#             st.info("GPT-4o: Advanced code understanding with strong multi-language support")
#         elif llm_provider == "mistral":
#             st.info("Mistral Large: Efficient code analysis with strong reasoning capabilities")
    
    
#     # Add model selection to settings
#     settings["llm_provider"] = llm_provider
    
#     # Center the review button
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col1:
#         review_button = st.button(
#             "📊 Review Code", 
#             type="primary", 
#             disabled=not code_input,
#             use_container_width=True
#         )

# import streamlit as st
# import os
# import tempfile
# from code_review.crew import run_code_review, CodeReview

# # Configure the page
# st.set_page_config(
#     page_title="AI Code Review Assistant",
#     page_icon="🔍",
#     layout="wide"
# )

# st.markdown("""
# <div style='text-align: center; background-color: #f0f2f6; padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem'>
#     <h1 style='color: #1E3A8A'>AI Code Review Assistant</h1>
#     <p style='font-size: 1.1rem'>Analyze, improve, and optimize your code with AI-powered insights</p>
# </div>""", unsafe_allow_html=True)

# st.markdown("### How Our AI Code Review Works")
# st.markdown("<hr>", unsafe_allow_html=True)

# # Main container for settings and code input
# main_container = st.container()

# # Initialize session state flags if not already set
# if "input_mode" not in st.session_state:
#     st.session_state.input_mode = None

# def handle_large_file_upload(uploaded_file, max_file_size_mb=10):
#     """
#     Safely handle large file uploads with size and content validation.
    
#     Args:
#         uploaded_file (UploadedFile): Streamlit uploaded file object
#         max_file_size_mb (int): Maximum allowed file size in megabytes
    
#     Returns:
#         tuple: (file_content, error_message)
#     """
#     # Check if file is uploaded
#     if uploaded_file is None:
#         return None, "No file uploaded."
    
#     # Check file size
#     file_size_bytes = uploaded_file.size
#     file_size_mb = file_size_bytes / (1024 * 1024)
    
#     if file_size_mb > max_file_size_mb:
#         return None, f"File too large. Maximum file size is {max_file_size_mb} MB."
    
#     try:
#         # Read file content
#         file_content = uploaded_file.getvalue().decode("utf-8")
        
#         # Additional content validation
#         if not file_content.strip():
#             return None, "The uploaded file is empty."
        
#         # Line count for large file detection
#         line_count = len(file_content.split('\n'))
        
#         return file_content, None
    
#     except UnicodeDecodeError:
#         return None, "Unable to decode file. Please ensure it's a text file."
#     except Exception as e:
#         return None, f"Error processing file: {str(e)}"

# def sample_large_file(file_content, max_lines=500):
#     """
#     Sample a large file to make analysis more manageable.
    
#     Args:
#         file_content (str): Full file content
#         max_lines (int): Maximum number of lines to retain
    
#     Returns:
#         str: Sampled file content
#     """
#     lines = file_content.split('\n')
    
#     if len(lines) <= max_lines:
#         return file_content
    
#     # Take first 100 lines
#     start_sample = '\n'.join(lines[:100])
    
#     # Take last 100 lines
#     end_sample = '\n'.join(lines[-100:])
    
#     # Take middle section
#     middle_start = len(lines) // 2 - 50
#     middle_sample = '\n'.join(lines[middle_start:middle_start+100])
    
#     # Combine samples with markers
#     sampled_content = f"""{start_sample}

# # [LARGE FILE: Middle section omitted for brevity]

# {middle_sample}

# # [LARGE FILE: End section follows]

# {end_sample}"""
    
#     return sampled_content

# with main_container:
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.markdown("#### Focus Areas")
#         focus_areas = st.multiselect(
#             "Select focus areas",
#             options=["Syntax", "Security", "Performance", "Readability", "Maintainability"],
#             default=["Syntax", "Performance", "Readability"],
#             help="Select areas to focus on during the review"
#         )
    
#     with col2:
#         st.markdown("#### Additional Options")
#         language_specific = st.checkbox(
#             "Enable language-specific rules",
#             value=True,
#             help="Apply language-specific best practices (the LLM will detect the language from your code)"
#         )
#         include_examples = st.checkbox(
#             "Include examples in feedback",
#             value=True,
#             help="Show example solutions for identified issues"
#         )    
#     st.markdown("<hr>", unsafe_allow_html=True)
    
#     # Code input section with two input methods
#     st.markdown("## Code Input")
#     input_tab1, input_tab2 = st.tabs(["📝 Enter Code", "📁 Upload File"])
    
#     code_input = ""
#     with input_tab1:
#         if st.session_state.input_mode == "file":
#             st.info("You have already uploaded a file. Switching to text input will clear the uploaded file.")
#             if st.button("Switch to Text Input"):
#                 st.session_state.input_mode = "text"
#                 st.session_state.uploaded_file = None
#                 st.rerun()

#         elif st.session_state.input_mode in [None, "text"]:
#             pasted_code = st.text_area(
#                 "Paste your code here:",
#                 height=250,
#                 help="Enter the code you want to analyze"
#             )

#             if pasted_code.strip():
#                 st.session_state.input_mode = "text"
#                 code_input = pasted_code

#     # === 📁 File Upload Tab ===
#     with input_tab2:
#         if st.session_state.input_mode == "text":
#             st.info("You have already entered text input. Switching to file upload will clear the text input.")
#             if st.button("Switch to File Upload"):
#                 st.session_state.input_mode = "file"
#                 st.session_state.pasted_code = ""
#                 st.rerun()

#         elif st.session_state.input_mode in [None, "file"]:
#             uploaded_file = st.file_uploader(
#                 "Upload a code file",
#                 type=["py", "js", "java", "cpp", "cs", "go", "rb", "php", "html", "css", "txt"],
#                 help="Only one input method is allowed. Uploading a file disables the text input."
#             )

#             if uploaded_file:
#                 st.session_state.input_mode = "file"
#                 uploaded_content, upload_error = handle_large_file_upload(uploaded_file, max_file_size_mb=10)

#                 if upload_error:
#                     st.error(upload_error)
#                 else:
#                     if len(uploaded_content.split('\n')) > 500:
#                         st.warning("Large file detected. File will be sampled.")
#                         uploaded_content = sample_large_file(uploaded_content)

#                     st.code(uploaded_content[:1000] + ("..." if len(uploaded_content) > 1000 else ""), language="python", line_numbers=True)
#                     code_input = uploaded_content
    
#     # Additional query input for specific code questions/instructions
#     user_query = st.text_input(
#         "Have a specific question or instruction about your code? Ask here:",
#         placeholder="E.g., 'Debug this code', 'Explain this function', 'Refactor for better performance', or 'Fix error on line 42'",
#         help="Enter any specific request about your code. You can ask for debugging help, code explanation, refactoring suggestions, or to fix specific errors."
#     )
    
#     # Collect settings
#     settings = {
#         "focus_areas": focus_areas,
#         "language_specific": language_specific,
#         "include_examples": include_examples,
#     }
    
#     # Model selection section
#     st.markdown("## Model Selection")
#     st.markdown("Select which language model you want to use for the analysis:")
    
#     model_col1, model_col2 = st.columns(2)
    
#     with model_col1:
#         llm_provider = st.selectbox(
#             "Language Model Provider",
#             options=["azure", "mistral"],
#             format_func=lambda x: {
#                 "azure": "Azure OpenAI (GPT-4o)",
#                 "mistral": "Mistral AI (Large)"
#             }.get(x, x),
#             help="Choose the AI model to analyze your code"
#         )
        
#         # Add model info based on selection
#         if llm_provider == "azure":
#             st.info("GPT-4o: Advanced code understanding with strong multi-language support")
#         elif llm_provider == "mistral":
#             st.info("Mistral Large: Efficient code analysis with strong reasoning capabilities")
    
    
#     # Add model selection to settings
#     settings["llm_provider"] = llm_provider
    
#     # Center the review button
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col1:
#         review_button = st.button(
#             "📊 Review Code", 
#             type="primary", 
#             disabled=not code_input,
#             use_container_width=True
#         )
    
#     # The rest of the code remains the same as in the original document...
#     # (I've truncated it for brevity, but you would keep the entire implementation)
    
#     if review_button and code_input:
#         with st.spinner(f"AI agents are reviewing your code using {llm_provider.capitalize()}..."):
#             try:
#                 # Simulate progress phases
#                 progress_container = st.container()
#                 with progress_container:
#                     progress_bar = st.progress(0)
#                     phases = [
#                         {"name": "Language Detection", "icon": "🔍", "description": "Identifying programming language..."},
#                         {"name": "Code Analysis", "icon": "🧮", "description": "Analyzing code structure and patterns..."},
#                         {"name": "Processing User Query", "icon": "💭", "description": "Addressing specific user requirements..."},
#                         {"name": "Generating Final Output", "icon": "✨", "description": "Compiling comprehensive review..."}
#                     ]
                    
#                     # Customize phases based on user query type
#                     if user_query and "debug" in user_query.lower():
#                         phases[2]["description"] = "Debugging code and identifying issues..."
#                         phases[3]["description"] = "Generating debugging recommendations..."
#                     elif user_query and any(word in user_query.lower() for word in ["refactor", "improve", "optimize"]):
#                         phases[2]["description"] = "Identifying optimization opportunities..."
#                         phases[3]["description"] = "Generating refactored code suggestions..."
#                     elif user_query and any(word in user_query.lower() for word in ["explain", "understand", "what does"]):
#                         phases[2]["description"] = "Analyzing code functionality..."
#                         phases[3]["description"] = "Generating detailed explanation..."
#                     elif user_query and any(word in user_query.lower() for word in ["error", "fix", "issue"]):
#                         phases[2]["description"] = "Diagnosing specific errors..."
#                         phases[3]["description"] = "Generating targeted solutions..."
                    
#                     for i, phase in enumerate(phases):
#                         progress_percent = (i + 0.5) * (100/len(phases))
#                         progress_bar.progress(int(progress_percent))
#                         st.markdown(f"**{phase['icon']} Phase {i+1}: {phase['name']}** - {phase['description']}")
#                     progress_bar.progress(100)
                
#                 # Run code review with user query
#                 review_result = run_code_review(code_input, settings, user_query)
                
#                 # Display file size information if it's a large file
#                 if "file_info" in review_result:
#                     st.markdown("""
#                     <div style='background-color: #fff3cd; padding: 0.75rem; border-radius: 0.5rem; border-left: 5px solid #ffc107; margin: 1rem 0'>
#                         <h4 style='color: #856404'>Large File Detected</h4>
#                         <p>{}</p>
#                         <p>Analysis will focus on high-level architecture and main components rather than detailed line-by-line review.</p>
#                     </div>
#                     """.format(review_result["file_info"]), unsafe_allow_html=True)
                
#                 # Display model information
#                 if "model_info" in review_result:
#                     model_color = {
#                         "azure": "#0078D4",
#                         "mistral": "#6B46C1"
#                     }.get(settings.get("llm_provider", "azure"), "#4CAF50")
                    
#                     st.markdown(f"""
#                     <div style='background-color: #f8f9fa; padding: 0.75rem; border-radius: 0.5rem; border-left: 5px solid {model_color}; margin: 1rem 0'>
#                         <h4 style='color: {model_color}'>Model Information</h4>
#                         <p>{review_result["model_info"]}</p>
#                         <p>Each model has different strengths and may provide varying insights.</p>
#                     </div>
#                     """, unsafe_allow_html=True)
                
#                 # Display appropriate heading based on request type
#                 if "request_type" in review_result:
#                     request_type = review_result["request_type"]
#                     if request_type == "debug":
#                         review_heading = "Debugging Results"
#                         review_description = "The AI agents have analyzed your code for errors and bugs. Below are the findings and recommended fixes."
#                     elif request_type == "refactor":
#                         review_heading = "Code Optimization Results"
#                         review_description = "The AI agents have identified optimization opportunities. Below are the recommended code improvements."
#                     elif request_type == "explain":
#                         review_heading = "Code Explanation"
#                         review_description = "The AI agents have analyzed your code structure and functionality. Below is a detailed explanation."
#                     elif request_type == "specific_error":
#                         review_heading = "Error Analysis Results"
#                         review_description = "The AI agents have analyzed the specific issues in your code. Below are the targeted solutions."
#                     else:
#                         review_heading = "Review Complete"
#                         review_description = "The AI agents have completed their analysis. Below is the consolidated final output."
#                 else:
#                     review_heading = "Review Complete"
#                     review_description = "The AI agents have completed their analysis. Below is the consolidated final output."
                
#                 st.markdown(f"""
#                 <div style='background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; border-left: 5px solid #4CAF50; margin: 1rem 0'>
#                     <h2 style='color: #2E7D32'>{review_heading}</h2>
#                     <p>{review_description}</p>
#                 </div>""", unsafe_allow_html=True)
                
#                 # Display only the final consolidated output
#                 final_output = review_result.get("combined_output", str(review_result))
#                 if "user_query" in review_result:
#                     st.markdown("### Your Question/Instruction:")
#                     st.info(review_result["user_query"])
#                     st.markdown("### Analysis:")
                    
#                 # Format the output in a more structured way
#                 try:
#                     # Get language
#                     if "Language:" in final_output:
#                         language = final_output.split("Language:")[1].split("\n")[0].strip()
#                     else:
#                         language = "Not detected"
                    
#                     # Get explanation
#                     if "Explanation:" in final_output and "Structure Analysis:" in final_output:
#                         explanation = final_output.split("Explanation:")[1].split("Structure Analysis:")[0].strip()
#                     elif "Explanation:" in final_output and "Response:" in final_output:
#                         explanation = final_output.split("Explanation:")[1].split("Response:")[0].strip()
#                     elif "Explanation:" in final_output:
#                         explanation = final_output.split("Explanation:")[1].strip()
#                     else:
#                         explanation = final_output.strip()
                    
#                     # Get structure analysis
#                     if "Structure Analysis:" in final_output and "Response:" in final_output:
#                         structure = final_output.split("Structure Analysis:")[1].split("Response:")[0].strip()
#                     elif "Structure Analysis:" in final_output:
#                         structure = final_output.split("Structure Analysis:")[1].strip()
#                     else:
#                         structure = ""
                    
#                     # Get response
#                     if "Response:" in final_output:
#                         response = final_output.split("Response:")[1].strip()
#                     else:
#                         response = ""
                    
#                     # Handle different request types with appropriate UI elements
#                     request_type = review_result.get("request_type", "general")
                    
#                     # Customize UI based on request type
#                     if request_type == "debug":
#                         st.markdown("""
#                         <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; margin: 1rem 0; border-left: 5px solid #dc3545'>
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #dc3545'>Identified Issues:</h4>
#                                 <p>{explanation}</p>
#                             </div>
#                             {structure_section}
#                             {response_section}
#                         </div>
#                         """.format(
#                             explanation=explanation,
#                             structure_section=f"""
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #dc3545'>Debugging Recommendations:</h4>
#                                 <p>{structure}</p>
#                             </div>
#                             """ if structure else "",
#                             response_section=f"""
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #dc3545'>Suggested Fixes:</h4>
#                                 <p>{response}</p>
#                             </div>
#                             """ if response else ""
#                         ), unsafe_allow_html=True)
#                     elif request_type == "refactor":
#                         st.markdown("""
#                         <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; margin: 1rem 0; border-left: 5px solid #28a745'>
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #28a745'>Current Implementation:</h4>
#                                 <p>{explanation}</p>
#                             </div>
#                             {structure_section}
#                             {response_section}
#                         </div>
#                         """.format(
#                             explanation=explanation,
#                             structure_section=f"""
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #28a745'>Optimization Opportunities:</h4>
#                                 <p>{structure}</p>
#                             </div>
#                             """ if structure else "",
#                             response_section=f"""
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #28a745'>Refactored Code Suggestions:</h4>
#                                 <p>{response}</p>
#                             </div>
#                             """ if response else ""
#                         ), unsafe_allow_html=True)
#                     elif request_type == "explain":
#                         st.markdown("""
#                         <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; margin: 1rem 0; border-left: 5px solid #17a2b8'>
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #17a2b8'>Code Explanation:</h4>
#                                 <p>{explanation}</p>
#                             </div>
#                             {structure_section}
#                             {response_section}
#                         </div>
#                         """.format(
#                             explanation=explanation,
#                             structure_section=f"""
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #17a2b8'>Code Structure:</h4>
#                                 <p>{structure}</p>
#                             </div>
#                             """ if structure else "",
#                             response_section=f"""
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #17a2b8'>Additional Notes:</h4>
#                                 <p>{response}</p>
#                             </div>
#                             """ if response else ""
#                         ), unsafe_allow_html=True)
#                     elif request_type == "specific_error":
#                         st.markdown("""
#                         <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; margin: 1rem 0; border-left: 5px solid #ffc107'>
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #ffc107'>Error Analysis:</h4>
#                                 <p>{explanation}</p>
#                             </div>
#                             {structure_section}
#                             {response_section}
#                         </div>
#                         """.format(
#                             explanation=explanation,
#                             structure_section=f"""
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #ffc107'>Context:</h4>
#                                 <p>{structure}</p>
#                             </div>
#                             """ if structure else "",
#                             response_section=f"""
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #ffc107'>Solution:</h4>
#                                 <p>{response}</p>
#                             </div>
#                             """ if response else ""
#                         ), unsafe_allow_html=True)
#                     else:
#                         st.markdown("""
#                         <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; margin: 1rem 0'>
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #1E3A8A'>Code Explanation:</h4>
#                                 <p>{explanation}</p>
#                             </div>
#                             {structure_section}
#                             {response_section}
#                         </div>
#                         """.format(
#                             explanation=explanation,
#                             structure_section=f"""
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #1E3A8A'>Structure Analysis:</h4>
#                                 <p>{structure}</p>
#                             </div>
#                             """ if structure else "",
#                             response_section=f"""
#                             <div style='margin-bottom: 1rem'>
#                                 <h4 style='color: #1E3A8A'>Response to Your Query:</h4>
#                                 <p>{response}</p>
#                             </div>
#                             """ if response else ""
#                         ), unsafe_allow_html=True)
                    
#                 except Exception as e:
#                     st.error(f"Error parsing output: {str(e)}")
#                     st.write("Raw output:")
#                     st.write(final_output)
                
#                 # Provide a download button for the final report
#                 report_title = "Code Review Report"
#                 if request_type == "debug":
#                     report_title = "Code Debugging Report"
#                 elif request_type == "refactor":
#                     report_title = "Code Optimization Report"
#                 elif request_type == "explain":
#                     report_title = "Code Explanation Report"
#                 elif request_type == "specific_error":
#                     report_title = "Error Analysis Report"
                
#                 report_content = f"""# {report_title}

# ## Your Question/Instruction
# {review_result.get("user_query", "")}

# ## Analysis
# {final_output}
#                 """
#                 st.download_button(
#                     label="📥 Download Report",
#                     data=report_content,
#                     file_name=f"{report_title.lower().replace(' ', '_')}.md",
#                     mime="text/markdown",
#                     use_container_width=True
#                 )
                
# import streamlit as st
# import os
# from code_review.crew import run_code_review, CodeReview

# st.set_page_config(
#     page_title="AI Code Review Assistant",
#     page_icon="🔍",
#     layout="wide"
# )

# # --- Header Section ---
# st.markdown("""
# <style>
#     .header {
#         background-color: #1E3A8A;
#         color: white;
#         padding: 2rem;
#         text-align: center;
#         border-radius: 0.5rem;
#     }
#     .section-title {
#         font-size: 1.3rem;
#         color: #1E3A8A;
#         margin-top: 2rem;
#     }
#     .box {
#         background-color: #f8f9fa;
#         padding: 1rem;
#         border-radius: 0.5rem;
#         border-left: 4px solid #0d6efd;
#         margin-bottom: 1.5rem;
#     }
# </style>
# <div class='header'>
#     <h1>🔍 AI Code Review Assistant</h1>
#     <p>Get intelligent, role-specific analysis for any code snippet — debug, refactor, explain, or review with clarity.</p>
# </div>
# """, unsafe_allow_html=True)

# # --- How It Works ---
# st.markdown("""
# <div class='box'>
#     <h4>✨ How It Works</h4>
#     <ol>
#         <li><strong>Paste or upload</strong> your code in the input section.</li>
#         <li><strong>Optionally type a question</strong> (e.g., "Fix this bug" or "Explain this code").</li>
#         <li>Click <strong>"🚀 Review Code"</strong> and let the AI agents process your input.</li>
#         <li>Receive <strong>clear, actionable feedback</strong> — structured by debug, refactor, explanation, or analysis.</li>
#     </ol>
# </div>
# """, unsafe_allow_html=True)

# # --- Main Layout ---
# st.markdown("<div class='section-title'>📥 Input Your Code</div>", unsafe_allow_html=True)

# col1, col2 = st.columns(2)
# with col1:
#     code_input = st.text_area("Paste your code here", height=250)
# with col2:
#     uploaded_file = st.file_uploader("Or upload a file", type=["py", "js", "java", "cpp", "cs", "go", "rb", "php", "html", "css", "txt"])
#     if uploaded_file:
#         code_input = uploaded_file.getvalue().decode("utf-8")

# st.markdown("<div class='section-title'>💬 Have a Specific Question?</div>", unsafe_allow_html=True)
# user_query = st.text_input("Example: 'Refactor this code', 'Fix bug in line 42', 'Explain this function'")

# # --- Review Trigger ---
# settings = {
#     "focus_areas": ["Syntax", "Performance"],  # simplified
#     "language_specific": True,
#     "include_examples": True,
#     "llm_provider": "azure"  # default for simplicity
# }

# if st.button("🚀 Review Code"):
#     if not code_input.strip():
#         st.warning("Please enter or upload code first.")
#     else:
#         with st.spinner("Analyzing your code with AI agents..."):
#             result = run_code_review(code_input, settings, user_query)

#         # --- Display Results ---
#         st.markdown("<div class='section-title'>📊 Review Summary</div>", unsafe_allow_html=True)

#         if "file_info" in result:
#             st.markdown(f"""
#             <div class='box'>
#                 <strong>Large File Notice:</strong> {result['file_info']}<br>
#                 Summary shown based on sample sections.
#             </div>
#             """, unsafe_allow_html=True)

#         if "model_info" in result:
#             st.success(f"LLM Used: {result['model_info']}")

#         if "user_query" in result:
#             st.markdown(f"<div class='box'><strong>User Query:</strong> {result['user_query']}</div>", unsafe_allow_html=True)

#         final_output = result.get("combined_output", "[No output received]")
#         st.markdown("<div class='section-title'>🧠 AI Code Review Output</div>", unsafe_allow_html=True)
#         st.code(final_output, language="markdown")

#         st.download_button("📥 Download Report", final_output, file_name="code_review_report.md", mime="text/markdown")



# import streamlit as st
# import os
# from code_review.crew import run_code_review, CodeReview

# # Custom CSS for a modern, professional look
# st.set_page_config(
#     page_title="CodeSage AI Review",
#     page_icon="🧠",
#     layout="wide"
# )

# # Advanced Styling
# st.markdown("""
# <style>
#     /* Global Styles */
#     body {
#         background-color: #f4f6f9;
#         font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
#     }

#     /* Header Styling */
#     .header {
#         background: linear-gradient(135deg, #4A6CF7 0%, #3658E0 100%);
#         color: white;
#         padding: 2.5rem;
#         border-radius: 12px;
#         box-shadow: 0 12px 24px rgba(70, 108, 247, 0.2);
#         text-align: center;
#         margin-bottom: 1.5rem;
#     }

#     .header h1 {
#         font-size: 2.5rem;
#         font-weight: 800;
#         margin-bottom: 1rem;
#         letter-spacing: -1px;
#     }

#     .header p {
#         font-size: 1.1rem;
#         opacity: 0.9;
#         max-width: 800px;
#         margin: 0 auto;
#     }

#     /* Section Styles */
#     .section-title {
#         color: #4A6CF7;
#         font-weight: 700;
#         margin-top: 2rem;
#         margin-bottom: 1rem;
#         border-bottom: 2px solid #4A6CF7;
#         padding-bottom: 0.5rem;
#     }

#     /* Card Styles */
#     .card {
#         background: white;
#         border-radius: 12px;
#         padding: 1.5rem;
#         box-shadow: 0 8px 16px rgba(0, 0, 0, 0.06);
#         margin-bottom: 1.5rem;
#         transition: all 0.3s ease;
#     }

#     .card:hover {
#         transform: translateY(-5px);
#         box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
#     }

#     /* Input Styles */
#     .stTextArea, .stTextInput {
#         background-color: white;
#         border-radius: 8px;
#         border: 1px solid #E0E4E8;
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
#     }

#     /* Button Styles */
#     .stButton > button {
#         background-color: #4A6CF7;
#         color: white;
#         border: none;
#         border-radius: 8px;
#         padding: 12px 24px;
#         font-weight: 600;
#         transition: all 0.3s ease;
#     }

#     .stButton > button:hover {
#         background-color: #3658E0;
#         transform: scale(1.02);
#     }

#     /* Spinner Styles */
#     .stSpinner > div {
#         border-color: #4A6CF7 transparent #4A6CF7 transparent;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Header Section
# st.markdown("""
# <div class='header'>
#     <h1>🧠 CodeSage AI Review</h1>
#     <p>Advanced AI-powered code analysis that provides intelligent insights, debugs complex issues, and helps you write cleaner, more efficient code.</p>
# </div>
# """, unsafe_allow_html=True)

# # Main Content Layout
# st.markdown("<div class='section-title'>🚀 Code Analysis</div>", unsafe_allow_html=True)

# # Use full width for better layout
# st.markdown("""
# <div class='card'>
#     <div class='row'>
#         <div class='col-md-6'>
#             <h4>📝 Code Input</h4>
#             <p>Paste your code or upload a file for comprehensive AI review.</p>
#         </div>
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # Code Input Section
# code_input = st.text_area(
#     "Paste your code here", 
#     height=300, 
#     help="Supports multiple programming languages"
# )

# # File Upload
# uploaded_file = st.file_uploader(
#     "Or upload a file", 
#     type=["py", "js", "java", "cpp", "cs", "go", "rb", "php", "html", "css", "txt"],
#     help="Max file size: 10MB"
# )

# if uploaded_file:
#     code_input = uploaded_file.getvalue().decode("utf-8")

# # Query Input
# st.markdown("<div class='section-title'>🤔 Specific Instruction</div>", unsafe_allow_html=True)
# user_query = st.text_input(
#     "Optional: Provide specific review instructions", 
#     placeholder="E.g., 'Refactor for performance', 'Check security vulnerabilities'"
# )

# # Review Button
# review_button = st.button("🔬 Perform Code Review", use_container_width=True)

# # Review Results
# if review_button:
#     if not code_input.strip():
#         st.warning("Please enter or upload code first.")
#     else:
#         with st.spinner("🧠 AI agents analyzing your code..."):
#             settings = {
#                 "focus_areas": ["Syntax", "Performance", "Best Practices"],
#                 "language_specific": True,
#                 "include_examples": True,
#                 "llm_provider": "azure"
#             }
            
#             result = run_code_review(code_input, settings, user_query)

#             # Results Card
#             st.markdown("<div class='section-title'>📊 Review Results</div>", unsafe_allow_html=True)
            
#             st.markdown("""
#             <div class='card'>
#                 <h4>🔍 Comprehensive Analysis</h4>
#             """, unsafe_allow_html=True)
            
#             if "file_info" in result:
#                 st.info(f"File Details: {result['file_info']}")
            
#             if "model_info" in result:
#                 st.success(f"Analysis Model: {result['model_info']}")
            
#             final_output = result.get("combined_output", "[No detailed output received]")
#             st.code(final_output, language="markdown")
            
#             st.download_button(
#                 "💾 Download Full Report", 
#                 final_output, 
#                 file_name="code_review_report.md", 
#                 mime="text/markdown",
#                 use_container_width=True
#             )

# import streamlit as st
# import os
# from code_review.crew import run_code_review, CodeReview

# # Custom CSS for a modern, professional look
# st.set_page_config(
#     page_title="CodeSage AI Review",
#     page_icon="🧠",
#     layout="wide"
# )

# # Advanced Styling
# st.markdown("""
# <style>
#     body {
#         background-color: #f4f6f9;
#         font-family: 'Inter', sans-serif;
#     }
#     .header {
#         background: linear-gradient(135deg, #4A6CF7 0%, #3658E0 100%);
#         color: white;
#         padding: 2.5rem;
#         border-radius: 12px;
#         box-shadow: 0 12px 24px rgba(70, 108, 247, 0.2);
#         text-align: center;
#         margin-bottom: 1.5rem;
#     }
#     .header h1 {
#         font-size: 2.5rem;
#         font-weight: 800;
#         margin-bottom: 1rem;
#         letter-spacing: -1px;
#     }
#     .header p {
#         font-size: 1.1rem;
#         opacity: 0.9;
#         max-width: 800px;
#         margin: 0 auto;
#     }
#     .section-title {
#         color: #4A6CF7;
#         font-weight: 700;
#         margin-top: 2rem;
#         margin-bottom: 1rem;
#         border-bottom: 2px solid #4A6CF7;
#         padding-bottom: 0.5rem;
#     }
#     .card {
#         background: white;
#         border-radius: 12px;
#         padding: 1.5rem;
#         box-shadow: 0 8px 16px rgba(0, 0, 0, 0.06);
#         margin-bottom: 1.5rem;
#         transition: all 0.3s ease;
#     }
#     .card:hover {
#         transform: translateY(-5px);
#         box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
#     }
#     .stButton > button {
#         background-color: #4A6CF7;
#         color: white;
#         border: none;
#         border-radius: 8px;
#         padding: 12px 24px;
#         font-weight: 600;
#         transition: all 0.3s ease;
#     }
#     .stButton > button:hover {
#         background-color: #3658E0;
#         transform: scale(1.02);
#     }
# </style>
# """, unsafe_allow_html=True)

# # Header
# st.markdown("""
# <div class='header'>
#     <h1>🧠 CodeSage AI Review</h1>
#     <p>Advanced AI-powered code analysis that provides intelligent insights, debugs complex issues, and helps you write cleaner, more efficient code.</p>
# </div>
# """, unsafe_allow_html=True)

# # Code Input
# st.markdown("<div class='section-title'>🚀 Code Analysis</div>", unsafe_allow_html=True)
# code_input = st.text_area("Paste your code here", height=300, help="Supports multiple programming languages")

# uploaded_file = st.file_uploader("Or upload a file", type=["py", "js", "java", "cpp", "cs", "go", "rb", "php", "html", "css", "txt"])
# if uploaded_file:
#     code_input = uploaded_file.getvalue().decode("utf-8")

# # User Query
# st.markdown("<div class='section-title'>🤔 Specific Instruction</div>", unsafe_allow_html=True)
# user_query = st.text_input("Optional: Provide specific review instructions", placeholder="E.g., 'Refactor for performance', 'Check security vulnerabilities'")

# # LLM Selection
# st.markdown("<div class='section-title'>🧠 Model Preference</div>", unsafe_allow_html=True)
# llm_provider = st.radio("Choose LLM Provider:", options=["azure", "mistral"], index=0, horizontal=True, format_func=lambda x: {
#     "azure": "Azure GPT-4o",
#     "mistral": "Mistral Large"
# }[x])

# # Review Button
# review_button = st.button("🔬 Perform Code Review", use_container_width=True)

# # Review Results
# if review_button:
#     if not code_input.strip():
#         st.warning("Please enter or upload code first.")
#     else:
#         with st.spinner("🧠 AI agents analyzing your code..."):
#             settings = {
#                 "focus_areas": ["Syntax", "Performance", "Best Practices"],
#                 "language_specific": True,
#                 "include_examples": True,
#                 "llm_provider": llm_provider
#             }
#             result = run_code_review(code_input, settings, user_query)

#         # Display Result
#         st.markdown("<div class='section-title'>📊 Review Results</div>", unsafe_allow_html=True)
#         st.markdown("<div class='card'>", unsafe_allow_html=True)

#         if "file_info" in result:
#             st.info(f"File Info: {result['file_info']}")
#         if "model_info" in result:
#             st.success(f"Model Used: {result['model_info']}")
#         if "user_query" in result:
#             st.markdown(f"**User Query:** {result['user_query']}")

#         st.markdown("---")
#         final_output = result.get("combined_output", "[No output received]")
#         st.code(final_output, language="markdown")

#         st.download_button("💾 Download Report", final_output, file_name="code_review_report.md", mime="text/markdown", use_container_width=True)

#         st.markdown("</div>", unsafe_allow_html=True)



import streamlit as st
import os
from code_review.crew import run_code_review, CodeReview

# Page Setup
st.set_page_config(
    page_title="AI powered Code Review Assistant",
    page_icon="🧠",
    layout="wide"
)
logo_path = "https://trigent.com/wp-content/uploads/Trigent_Axlr8_Labs.png"
st.markdown(
    f"""
    <div style="text-align:center;">
        <img src="{logo_path}" alt="Trigent Logo" style="max-width:100%;">
    </div>
    """,
    unsafe_allow_html=True
)
# Styling
st.markdown("""
<style>
    body {
        background-color: #f4f6f9;
        font-family: 'Inter', sans-serif;
    }
    .header {
        background: linear-gradient(135deg, #4A6CF7 0%, #3658E0 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 12px 24px rgba(70, 108, 247, 0.2);
        text-align: center;
        margin-bottom: 1rem;  
        }
    .header h1 {
        font-size: 2.1rem; 
        font-weight: 800;
        margin-bottom: 0.75rem;
        letter-spacing: -1px;
    }
    .header p {
        font-size: 1rem; 
        opacity: 0.9;
        max-width: 800px;
        margin: 0 auto;
    }
    .section-title {
        color: #4A6CF7;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #4A6CF7;
        padding-bottom: 0.5rem;
    }
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.06);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
    }
    .stButton > button {
        background-color: #4A6CF7;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #3658E0;
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class='header'>
    <h1>🧠 AI Powered Code Review Assistant</h1>
    <p>Advanced AI-powered code analysis that provides intelligent insights, debugs complex issues, and helps you write cleaner, more efficient code.</p>
</div>
""", unsafe_allow_html=True)
st.markdown("<div class='section-title'>🔍 How It Works</div>", unsafe_allow_html=True)

st.markdown("""
<style>
.how-it-works-row {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 1.5rem;
}
.how-it-works-step {
    flex: 1;
    background: linear-gradient(135deg, #4A6CF7 0%, #3658E0 100%);
    color: white;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 12px 24px rgba(70, 108, 247, 0.2);
    transition: transform 0.3s ease;
}
.how-it-works-step:hover {
    transform: translateY(-5px);
}
.how-it-works-step h3 {
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}
.how-it-works-step p {
    opacity: 0.9;
}
.advanced-features {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.06);
    margin-top: 1.5rem;
}
.advanced-features h3 {
    color: #4A6CF7;
    border-bottom: 2px solid #4A6CF7;
    padding-bottom: 10px;
    margin-bottom: 15px;
}
.advanced-features ul {
    list-style-type: none;
    padding: 0;
}
.advanced-features ul li {
    margin-bottom: 10px;
    padding-left: 30px;
    position: relative;
}
.advanced-features ul li:before {
    content: '✓';
    color: #4A6CF7;
    position: absolute;
    left: 0;
    top: 0;
}
</style>

<div class='how-it-works-row'>
    <div class='how-it-works-step'>
        <h3>📝 1. Input Code</h3>
        <p>Paste your code directly into the text area or upload a file. We support multiple programming languages including Python, JavaScript, Java, C++, and more.</p>
    </div>
    <div class='how-it-works-step'>
        <h3>🤖 2. AI Analysis</h3>
        <p>Our advanced AI agents perform a comprehensive code review, analyzing syntax, performance, best practices, and any specific instructions you provide.</p>
    </div>
    <div class='how-it-works-step'>
        <h3>📊 3. Detailed Report</h3>
        <p>Receive an intelligent, actionable report with insights, potential improvements, and code refactoring suggestions tailored to your specific code.</p>
    </div>
</div>

<div class='advanced-features'>
    <h3>🧠 Advanced Features</h3>
    <ul>
        <li><strong>Multi-Model Support:</strong> Choose between Azure GPT-4o and Mistral Large for your code review</li>
        <li><strong>Custom Instructions:</strong> Provide specific review focus areas like performance optimization or security checks</li>
        <li><strong>Comprehensive Analysis:</strong> Covers syntax, performance, best practices, and language-specific insights</li>
        <li><strong>Easy Download:</strong> Download the full review report as a markdown file</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Code Input
st.markdown("<div class='section-title'>🚀 Code Analysis</div>", unsafe_allow_html=True)
# code_input = st.text_area("Paste your code here", height=300, help="Supports multiple programming languages")

# uploaded_file = st.file_uploader("Or upload a file", type=["py", "js", "java", "cpp", "cs", "go", "rb", "php", "html", "css", "txt"])
# if uploaded_file:
#     code_input = uploaded_file.getvalue().decode("utf-8")


# Add a radio button to choose input method
input_method = st.radio("Choose Input Method:", ["Text Input", "File Upload"])

if input_method == "Text Input":
    # Text area for code input
    code_input = st.text_area("Paste your code here", height=300, help="Supports multiple programming languages")
    
    # Clear any previously uploaded file
    uploaded_file = None
    st.session_state.uploaded_file = None

elif input_method == "File Upload":
    # File uploader
    uploaded_file = st.file_uploader("Upload a file", type=["py", "js", "java", "cpp", "cs", "go", "rb", "php", "html", "css", "txt"])
    
    # Clear the text input if a file is uploaded
    if uploaded_file:
        code_input = uploaded_file.getvalue().decode("utf-8")
        # Disable text area
        st.text_area("Code from uploaded file", value=code_input, height=300, disabled=True)
    else:
        code_input = ""

# Ensure code_input is not None
code_input = code_input if code_input else ""


# User Query
st.markdown("<div class='section-title'>🤔 Specific Instruction</div>", unsafe_allow_html=True)
user_query = st.text_input("Optional: Provide specific review instructions", placeholder="E.g., 'Refactor for performance', 'Check security vulnerabilities'")

# LLM Selection
st.markdown("<div class='section-title'>🧠 Model Preference</div>", unsafe_allow_html=True)
llm_provider = st.radio("Choose LLM Provider:", options=["azure", "mistral"], index=0, horizontal=True, format_func=lambda x: {
    "azure": "Azure GPT-4o",
    "mistral": "Mistral Large"
}[x])

# Review Button
review_button = st.button("🔬 Perform Code Review", use_container_width=True)

# Review Results
if review_button:
    if not code_input.strip():
        st.warning("Please enter or upload code first.")
    else:
        with st.spinner("🧠 AI agents analyzing your code..."):
            settings = {
                "focus_areas": ["Syntax", "Performance", "Best Practices"],
                "language_specific": True,
                "include_examples": True,
                "llm_provider": llm_provider
            }
            result = run_code_review(code_input, settings, user_query)

        st.markdown("<div class='section-title'>📊 Review Results</div>", unsafe_allow_html=True)
        with st.container():
            if "file_info" in result:
                st.info(f"📁 File Info: {result['file_info']}")
            if "model_info" in result:
                st.success(f"🧠 Model Used: {result['model_info']}")
            if "user_query" in result:
                st.markdown(f"**🎯 User Query:** {result['user_query']}")

            st.markdown("---")

            final_output = result.get("combined_output", "[No output received]")

            # Render output like ChatGPT, code blocks shown properly
            inside_code_block = False
            code_block = []
            for line in final_output.split("\n"):
                if line.strip().startswith("```"):
                    if inside_code_block:
                        st.code("\n".join(code_block))
                        code_block = []
                        inside_code_block = False
                    else:
                        inside_code_block = True
                elif inside_code_block:
                    code_block.append(line)
                else:
                    st.write(line)

            st.download_button("💾 Download Report", final_output, file_name="code_review_report.md", mime="text/markdown", use_container_width=True)


footer_html = """
   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
   <div style="text-align: center;">
       <p>
           Copyright © 2024 | <a href="https://trigent.com/ai/" target="_blank" aria-label="Trigent Website">Trigent Software Inc.</a> All rights reserved. |
           <a href="https://www.linkedin.com/company/trigent-software/" target="_blank" aria-label="Trigent LinkedIn"><i class="fab fa-linkedin"></i></a> |
           <a href="https://www.twitter.com/trigentsoftware/" target="_blank" aria-label="Trigent Twitter"><i class="fab fa-twitter"></i></a> |
           <a href="https://www.youtube.com/channel/UCNhAbLhnkeVvV6MBFUZ8hOw" target="_blank" aria-label="Trigent Youtube"><i class="fab fa-youtube"></i></a>
       </p>
   </div>
   """

footer_css = """
   <style>
   .footer {
       position: fixed;
       z-index: 1000;
       left: 0;
       bottom: 0;
       width: 100%;
       background-color: white;
       color: black;
       text-align: center;
   }
   [data-testid="stSidebarNavItems"] {
       max-height: 100%!important;
   }
   [data-testid="collapsedControl"] {
       display: none;
   }
   </style>
   """

footer = f"{footer_css}<div class='footer'>{footer_html}</div>"

st.markdown(footer, unsafe_allow_html=True)