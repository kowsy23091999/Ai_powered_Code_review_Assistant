import os
import litellm
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enable LiteLLM logging
litellm.set_verbose = True

# Function to get LLM based on provider
def get_llm(provider="azure"):
    """
    Get LLM instance based on provider.
    Supported providers: 'azure', 'mistral'
    """
    if provider == "azure":
        return LLM(
            api_key=os.getenv("AZURE_API_KEY"),
            base_url=os.getenv("AZURE_API_BASE"),
            api_version=os.getenv("AZURE_API_VERSION"),
            model="azure/gpt-4o"
        )
    elif provider == "mistral":
        return LLM(
            api_key=os.getenv("MISTRAL_API_KEY"),
            base_url=os.getenv("MISTRAL_API_BASE"),
            model="mistral-large-latest"
        )
    else:
        # Default to Azure
        return LLM(
            api_key=os.getenv("AZURE_API_KEY"),
            base_url=os.getenv("AZURE_API_BASE"),
            api_version=os.getenv("AZURE_API_VERSION"),
            model="azure/gpt-4o"
        )

@CrewBase
class CodeReview:
    """Code Review CrewAI setup using YAML configuration."""

    # YAML file paths
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    def __init__(self, llm_provider="azure"):
        self.llm = get_llm(llm_provider)
        self.llm_provider = llm_provider

    @agent
    def researcher(self) -> Agent:
        """Code Analysis Expert"""
        return Agent(
            config=self.agents_config["researcher"],
            verbose=True,
            llm=self.llm,
            tools=[],  # Can be expanded if needed
            context="""You are a code analysis expert. Your output MUST follow this EXACT format:

                        Language: [programming language detected]

                        Explanation: [Clear, concise explanation of what the code does, focusing on its main purpose and functionality. Do not repeat the code.]

                        Structure Analysis: [Brief overview of the code's structure, main components, and organization. For large files, focus on identifying key modules, classes, or functions.]

                        Response: [Direct response to the user's specific query or instruction, if provided. Focus on answering their question without repeating information from the explanation.]

                        For large code files:
                        1. Focus on high-level architecture rather than line-by-line analysis
                        2. Identify the main components and their relationships
                        3. Highlight the most important patterns and design decisions
                        4. Summarize potential issues by category rather than exhaustively listing every small issue

                        If the user specifically asks for line-by-line explanation, ignore the above recommendation and provide detailed explanation of each significant line or block.

                        For debugging requests:
                        1. Identify potential errors and bugs in the code
                        2. Suggest specific debugging approaches
                        3. Recommend appropriate logging or debugging tools for the identified language
                        4. Provide example debug statements at critical points in the code flow

                        IMPORTANT: You MUST include all four sections (Language, Explanation, Structure Analysis, and Response) in your output, using exactly these section titles followed by a colon. If you don't have a response to a specific query, still include the "Response:" section with a note that there was no specific query.

                        Keep explanations clear and concise. Never repeat the code in your response unless specifically asked to show modifications."""
            )

    @agent
    def reporting_analyst(self) -> Agent:
        """Code Review Specialist"""
        return Agent(
            config=self.agents_config["reporting_analyst"],
            verbose=True,
            llm=self.llm,
            context="""You write detailed code review reports. Use the language information
                       from the researcher to provide language-specific feedback. If a user
                       query is provided, make sure to address it in your feedback.
                       
                       When addressing errors in the code:
                       1. Cite the specific line number where each error occurs
                       2. Explain why it's an error and potential consequences
                       3. Provide corrected code snippets
                       
                       For line-by-line explanation requests:
                       1. Break down the code into logical sections
                       2. Explain each significant line or block in detail
                       3. Highlight the purpose and functionality of key variables and functions
                       
                       For debugging requests:
                       1. Suggest a systematic debugging approach
                       2. Recommend specific debugging tools or methods for the identified language
                       3. Provide sample debug code or logging statements at critical points
                       
                       Always tailor your feedback to the specific user query."""
        )

    @agent
    def optimization_expert(self) -> Agent:
        """Code Optimization Specialist"""
        return Agent(
            config=self.agents_config["optimization_expert"],
            verbose=True,
            llm=self.llm,
            context="""You optimize code while preserving its functionality. Use the language
                       information to apply language-specific optimizations. If a user query
                       contains specific optimization requests, prioritize those in your
                       refactoring.
                       
                       For refactoring requests:
                       1. Identify code smells and technical debt
                       2. Apply appropriate design patterns and best practices
                       3. Improve naming conventions, code organization, and structure
                       4. Present before/after comparisons for significant changes
                       
                       For performance optimization:
                       1. Identify inefficient algorithms or operations
                       2. Suggest specific optimizations with rationale
                       3. Estimate potential performance improvements
                       4. Provide benchmark suggestions when appropriate
                       
                       For debugging suggestions:
                       1. Restructure code to be more testable and debuggable
                       2. Add appropriate error handling and validation
                       3. Suggest logging and monitoring improvements
                       
                       When the user asks for specific types of optimizations, focus exclusively on those areas."""
        )

    @task
    def analyze_code_task(self) -> Task:
        """Analyze the given code snippet"""
        return Task(
            config=self.tasks_config["analyze_code_task"],
        )

    @task
    def provide_feedback_task(self) -> Task:
        """Provide feedback on identified issues"""
        return Task(
            config=self.tasks_config["provide_feedback_task"],
            output_file="feedback_report.md"
        )

    @task
    def optimize_code_task(self) -> Task:
        """Refactor and optimize the given code"""
        return Task(
            config=self.tasks_config["optimize_code_task"],
            output_file="optimized_code.md"
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Code Review Crew"""
        return Crew(
            agents=self.agents,  
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )

def generate_targeted_answer_only(code_snippet: str, user_query: str, llm_provider: str = "azure") -> str:
    """
    Generate a targeted answer for a specific user query about the code.
    
    Args:
        code_snippet (str): The code to analyze
        user_query (str): Specific query about the code
        llm_provider (str, optional): LLM provider to use. Defaults to "azure".
    
    Returns:
        str: Targeted response to the user's query
    """
    model_map = {
        "azure": {
            "model": "azure/gpt-4o",
            "api_key": os.getenv("AZURE_API_KEY"),
            "base_url": os.getenv("AZURE_API_BASE"),
            "api_version": os.getenv("AZURE_API_VERSION")
        },
        "mistral": {
            "model": "mistral-large-latest",
            "api_key": os.getenv("MISTRAL_API_KEY"),
            "base_url": os.getenv("MISTRAL_API_BASE")
        }
    }

    selected_config = model_map.get(llm_provider)
    if not selected_config:
        raise ValueError(f"Unsupported provider: {llm_provider}")

    # Enhanced system prompt to focus on the user's specific query
    response = litellm.completion(
        model=selected_config["model"],
        api_key=selected_config["api_key"],
        api_base=selected_config.get("base_url"),
        api_version=selected_config.get("api_version"),
        messages=[
            {
                "role": "system", 
                "content": """You are an expert AI code reviewer focused on providing precise, actionable insights.
                
                Key Guidelines:
                - Analyze the code thoroughly
                - Directly address the user's specific query
                - Provide clear, concise explanations
                - Include code examples if helpful
                - Be specific and pragmatic"""
            },
            {
                "role": "user", 
                "content": f"""Carefully analyze the following code and address the specific query:

                            Code Snippet:
                            ```
                            {code_snippet}
                            ```

                            User Query:
                            {user_query}

                            Please provide a focused, direct response that:
                            1. Directly answers the specific question
                            2. Explains the reasoning behind the answer
                            3. Provides actionable insights or recommendations
                            4. Uses code examples if clarification is needed"""
                                        }
                                    ]
                                )

    return response["choices"][0]["message"]["content"]

def run_code_review(code_snippet, settings, user_query=None):
    """
    Run a comprehensive code review with optional user-specific query handling.
    
    Args:
        code_snippet (str): The code to review
        settings (dict): Review settings and configurations
        user_query (str, optional): Specific user query about the code
    
    Returns:
        dict: Comprehensive review results
    """
    # Prioritize user query if provided
    if user_query and user_query.strip():
        # Generate targeted answer for specific query
        targeted_response = generate_targeted_answer_only(
            code_snippet, 
            user_query, 
            settings.get("llm_provider", "azure")
        )
        
        return {
            "combined_output": targeted_response,
            "user_query": user_query,
            "request_type": "targeted_query",
            "model_info": f"Analysis using {settings.get('llm_provider', 'azure').capitalize()} model"
        }
    
    # Default code review process if no specific query
    llm_provider = settings.get("llm_provider", "azure")
    
    # Create a crew instance with the selected provider
    crew_instance = CodeReview(llm_provider=llm_provider)
    
    # Detect code size and set appropriate flags
    code_lines = code_snippet.split('\n')
    is_large_file = len(code_lines) > 100
    is_very_large_file = len(code_lines) > 500
    
    # Handle large files by sampling
    if is_very_large_file:
        middle = max(100, len(code_lines) // 2 - 50)
        code_snippet = '\n'.join(
            code_lines[:100] + 
            ['\n# ... [Middle section of code omitted for brevity] ...\n'] + 
            code_lines[middle:middle+100] +
            ['\n# ... [Later section of code omitted for brevity] ...\n'] +
            code_lines[-100:]
        )
    
    # Set up tasks
    analyze_task = crew_instance.analyze_code_task()
    analyze_task.description = f"Perform a comprehensive code analysis. Code size: {len(code_lines)} lines."
    
    feedback_task = crew_instance.provide_feedback_task()
    feedback_task.description = "Provide detailed code review feedback and suggestions."
    
    optimize_task = crew_instance.optimize_code_task()
    optimize_task.description = "Identify and propose code optimizations."
    
    # Run the crew
    crew = crew_instance.crew()
    result = crew.kickoff(inputs={"code_snippet": code_snippet})
    
    # Prepare output
    output = {
        "combined_output": str(result),
        "request_type": "default_review",
        "model_info": f"Analysis using {llm_provider.capitalize()} model"
    }
    
    # Add file size information
    if is_large_file:
        output["file_info"] = f"Large file: {len(code_lines)} lines"
    
    return output


# def generate_targeted_answer_only(code_snippet: str, user_query: str, llm_provider: str = "azure") -> str:
#     # Map model names and get credentials
#     model_map = {
#         "azure": {
#             "model": "azure/gpt-4o",
#             "api_key": os.getenv("AZURE_API_KEY"),
#             "base_url": os.getenv("AZURE_API_BASE"),
#             "api_version": os.getenv("AZURE_API_VERSION")
#         },
#         "mistral": {
#             "model": "mistral-large-latest",
#             "api_key": os.getenv("MISTRAL_API_KEY"),
#             "base_url": os.getenv("MISTRAL_API_BASE")
#         }
#     }

#     selected_config = model_map.get(llm_provider)
#     if not selected_config:
#         raise ValueError(f"Unsupported provider: {llm_provider}")

#     # Set up LiteLLM request
#     response = litellm.completion(
#         model=selected_config["model"],
#         api_key=selected_config["api_key"],
#         api_base=selected_config.get("base_url"),
#         api_version=selected_config.get("api_version"),
#         messages=[
#             {"role": "system", "content": "You are a helpful and focused code reviewer."},
#             {"role": "user", "content": f"""
#                     You are an expert AI code reviewer. A developer has asked a question about their code.

#                     --- USER QUESTION ---
#                     {user_query}

#                     --- CODE SNIPPET ---
#                     {code_snippet}

#                     Your task:
#                     1. Analyze the code **carefully** before answering — do not say "Yes" or "No" without evaluating.
#                     2. If the user asks if something is good, secure, or valid:
#                     - ✅ Explain whether it is, **why or why not**, and under what conditions.
#                     - ✅ Provide better alternatives if available.
#                     - ✅ Include small working code examples if helpful.
#                     3. If installation or dependency is needed, mention it.
#                     4. Keep the output simple and focused — avoid bloated summaries.

#                     Use Markdown formatting where helpful (code blocks, bullet points, etc).
#                     """}


#                 ]
#             )

#     return response["choices"][0]["message"]["content"]


# def run_code_review(code_snippet, settings, user_query=None):
#     """Run the code review process on the provided code snippet with custom settings.
#        Optionally process a user query about the code. The LLM will detect the
#        programming language from the provided code snippet.
       
#        If a user query is provided, the query is passed to all agents to ensure
#        the entire review process takes it into account.
#     """
#     # Get the selected LLM provider from settings
#     llm_provider = settings.get("llm_provider", "azure")
    
#     # Create a crew instance with the selected provider
#     crew_instance = CodeReview(llm_provider=llm_provider)
    
#     # Check code size and set appropriate flags for large files
#     code_lines = len(code_snippet.split('\n'))
#     is_large_file = code_lines > 100
#     is_very_large_file = code_lines > 500
    
#     # For extremely large files, we'll only analyze a portion
#     if is_very_large_file:
#         # Take first 100 lines, middle 100 lines, and last 100 lines
#         code_lines_list = code_snippet.split('\n')
#         middle_start = max(100, len(code_lines_list) // 2 - 50)
#         sample_code = '\n'.join(
#             code_lines_list[:100] + 
#             ['\n# ... [Middle section of code omitted for brevity] ...\n'] + 
#             code_lines_list[middle_start:middle_start+100] +
#             ['\n# ... [Later section of code omitted for brevity] ...\n'] +
#             code_lines_list[-100:]
#         )
        
#         # Add a note about the sampling
#         code_snippet = sample_code
#         is_sampled = True
#     else:
#         is_sampled = False
    
#     # Process user query to identify specific request types
#     request_type = "general"
#     query_keywords = {
#         "debug": ["debug", "error", "fix", "not working", "crash", "exception", "traceback"],
#         "refactor": ["refactor", "optimize", "improvement", "clean", "better", "redesign", "restructure"],
#         "explain": ["explain", "understand", "what does", "how does", "line by line", "detailed explanation"],
#         "specific_error": ["error in line", "issue with", "problem at", "fix this specific", "why is this not"]
#     }
    
#     # Determine the type of request from the user query
#     if user_query:
#         user_query_lower = user_query.lower()
#         for req_type, keywords in query_keywords.items():
#             if any(keyword in user_query_lower for keyword in keywords):
#                 request_type = req_type
#                 break
    
#     # Set up special instructions based on request type and settings
#     special_instructions = ""
    
#     if request_type == "debug" or settings.get("debug_mode", False):
#         special_instructions += """
#         DEBUGGING FOCUS: This is a debugging request. Please:
#         1. Identify all potential errors and bugs in the code
#         2. Suggest specific debugging approaches and tools
#         3. Add logging statements at key points
#         4. Provide a step-by-step debugging plan
#         5. If possible, provide fixed code examples
#         """
    
#     elif request_type == "refactor":
#         special_instructions += """
#         REFACTORING FOCUS: This is a code refactoring request. Please:
#         1. Identify all code smells and technical debt
#         2. Apply appropriate design patterns and best practices
#         3. Improve naming conventions and code organization
#         4. Show direct before/after comparisons for major changes
#         5. Preserve all original functionality while improving structure
#         """
    
#     elif request_type == "explain":
#         special_instructions += """
#         EXPLANATION FOCUS: This is a request for detailed explanation. Please:
#         1. Provide line-by-line explanation of the code's functionality
#         2. Explain the purpose of each function, class, and significant variable
#         3. Describe the overall architecture and design approach
#         4. Use simple language and avoid jargon where possible
#         5. Include examples of expected inputs/outputs where helpful
#         """
    
#     elif request_type == "specific_error":
#         special_instructions += """
#         SPECIFIC ERROR FOCUS: This is a request to address a specific error. Please:
#         1. Identify the exact error or issue mentioned in the query
#         2. Analyze that specific part of the code in detail
#         3. Provide a targeted solution for the specified problem
#         4. Explain why the error occurs and how your solution fixes it
#         5. Suggest additional tests to verify the fix works properly
#         """
#     yes_no_words = ["is", "can", "should", "do you think", "could", "would", "will", "does"]
#     if request_type == "general" and user_query and any(w in user_query.lower() for w in yes_no_words):

#         return {
#             "combined_output": "Response: " + generate_targeted_answer_only(user_query, code_snippet, llm_provider),
#             "user_query": user_query,
#             "request_type": "targeted"
#         }

#     # Apply focus areas from settings
#     if "focus_areas" in settings and settings["focus_areas"]:
#         focus_str = ", ".join(settings["focus_areas"])
#         special_instructions += f"\nPrioritize focus on these areas: {focus_str}\n"
    
#     # Handle review depth setting
#     if "review_depth" in settings:
#         if settings["review_depth"] == "Comprehensive":
#             special_instructions += "\nProvide a comprehensive, detailed analysis of all aspects of the code.\n"
#         elif settings["review_depth"] == "Basic":
#             special_instructions += "\nProvide a basic, high-level overview focusing only on major issues.\n"
    
#     # Detect programming language (this will be done by the LLM)
#     # We'll include instructions for the LLM to detect the language
#     language_detection_prompt = "First, identify the programming language of this code snippet."
    
#     if is_large_file:
#         language_detection_prompt += " This is a large code file, so focus on high-level architecture and main components rather than detailed line-by-line analysis."
    
#     if is_very_large_file:
#         language_detection_prompt += " Note: This is a sample of a very large file. The complete file contains " + str(code_lines) + " lines of code."
    
#     # Set up tasks using the code snippet and include language detection prompt
#     analyze_task = crew_instance.analyze_code_task()
#     analyze_task.description = language_detection_prompt + "\n\n" + analyze_task.description.replace("{code_snippet}", code_snippet) + special_instructions
    
#     feedback_task = crew_instance.provide_feedback_task()
#     feedback_task.description = feedback_task.description.replace("{code_snippet}", code_snippet) + special_instructions
    
#     optimize_task = crew_instance.optimize_code_task()
#     optimize_task.description = optimize_task.description.replace("{code_snippet}", code_snippet) + special_instructions
    
#     # If the user provided a query, update all task descriptions
#     if user_query and user_query.strip():
#         user_query_instruction = f"\n\nAdditional instruction from user: {user_query}"
        
#         # Add user query to all three tasks to ensure comprehensive handling
#         analyze_task.description += user_query_instruction
#         feedback_task.description += user_query_instruction
#         optimize_task.description += user_query_instruction
    
#     # Create and run the crew
#     crew = crew_instance.crew()
#     result = crew.kickoff()
    
#     # Parse result from various possible output formats
#     if hasattr(result, 'raw_output'):
#         raw_result = result.raw_output
#     elif isinstance(result, dict):
#         raw_result = result
#     elif isinstance(result, str):
#         raw_result = {"combined_output": result}
#     else:
#         raw_result = {"combined_output": str(result)}
    
#     # Ensure the user query is included in the final output
#     if user_query:
#         raw_result["user_query"] = f"User Query: {user_query}"
#         raw_result["request_type"] = request_type  # Include detected request type
    
#     # Add file size info
#     if is_large_file:
#         raw_result["file_info"] = f"Large file detected: {code_lines} lines of code"
    
#     if is_very_large_file:
#         raw_result["file_info"] = f"Very large file detected: {code_lines} lines of code. Analysis performed on a representative sample."
    
#     # Add model info
#     raw_result["model_info"] = f"Analysis performed using {llm_provider.capitalize()} model"
    
#     return raw_result
