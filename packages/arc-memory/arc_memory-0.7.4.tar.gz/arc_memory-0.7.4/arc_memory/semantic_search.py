"""Semantic search module for Arc Memory.

This module provides functions to process natural language queries against
the knowledge graph, leveraging LLMs to understand the query intent and
extract relevant information from the graph.
"""

import json
import sqlite3
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
import os

from arc_memory.llm.ollama_client import OllamaClient, ensure_ollama_available
from arc_memory.logging_conf import get_logger
from arc_memory.schema.models import Node, NodeType
from arc_memory.sql.db import get_connection
from arc_memory.trace import (
    format_trace_results,
    get_node_by_id,
    get_connected_nodes,
    trace_history_for_file_line,
)

# Import OpenAI client conditionally to avoid hard dependency
try:
    from arc_memory.llm.openai_client import OpenAIClient, ensure_openai_available
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

logger = get_logger(__name__)

# Enable or disable debug mode
DEBUG_MODE = os.environ.get("ARC_DEBUG", "").lower() in ("1", "true", "yes")

def debug_log(
    func_name: str,
    inputs: Dict[str, Any] = None,
    outputs: Dict[str, Any] = None,
    debug_dir: str = None
) -> None:
    """Log debug information for a function call.

    This function logs the inputs and outputs of a function call to a debug file.
    Useful for debugging LLM interactions and understanding the system's behavior.

    Args:
        func_name: Name of the function being debugged
        inputs: Dictionary of input values
        outputs: Dictionary of output values
        debug_dir: Directory to store debug logs (defaults to ~/.arc/debug)
    """
    if not DEBUG_MODE:
        return

    try:
        # Default debug directory
        if not debug_dir:
            arc_dir = Path.home() / ".arc"
            debug_dir = arc_dir / "debug"

        # Ensure directory exists
        os.makedirs(debug_dir, exist_ok=True)

        # Create a timestamped file name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{func_name}.json"
        filepath = Path(debug_dir) / filename

        # Prepare debug data
        debug_data = {
            "timestamp": datetime.now().isoformat(),
            "function": func_name,
            "inputs": inputs or {},
            "outputs": outputs or {}
        }

        # Write to file
        with open(filepath, "w") as f:
            json.dump(debug_data, f, indent=2, default=str)

        logger.debug(f"Debug log written to {filepath}")

    except Exception as e:
        logger.warning(f"Failed to write debug log: {e}")

# Function decorator to automatically log inputs and outputs
def debug_function(func: Callable) -> Callable:
    """Decorator to automatically log function inputs and outputs for debugging.

    Args:
        func: The function to decorate

    Returns:
        The decorated function
    """
    if not DEBUG_MODE:
        return func

    def wrapper(*args, **kwargs):
        # Prepare input data
        inputs = {
            "args": args,
            "kwargs": kwargs
        }

        # Call the function
        result = func(*args, **kwargs)

        # Log the inputs and outputs
        debug_log(
            func_name=func.__name__,
            inputs=inputs,
            outputs={"result": result}
        )

        return result

    return wrapper

# System prompts for different phases of semantic processing
QUERY_UNDERSTANDING_PROMPT = """You are a specialized AI assistant for the Arc Memory knowledge graph system.
Your task is to parse and understand natural language queries about a codebase and its development history.

Focus solely on understanding the query intent, do not generate answers yet.

The knowledge graph contains the following types of nodes:
- commit: Git commits with code changes
- pr: Pull requests that merge changes
- issue: GitHub issues or Linear tickets describing problems or features
- adr: Architecture Decision Records documenting technical decisions
- file: Source code files in the repository

When analyzing a user's question, identify:
1. The primary entity types the user is asking about (commits, PRs, issues, ADRs, files)
2. Any temporal constraints (e.g., "last month", "before version 2.0")
3. Any specific attributes to filter on (e.g., author, status, title keywords)
4. The type of relationship or information the user wants to know

For temporal constraints:
- When the user mentions relative time periods like "last month", "last week", etc., convert them to specific date strings in YYYY-MM-DD format.
- For "last month", use a date 30 days ago from today.
- For "last week", use a date 7 days ago from today.
- For "last year", use a date 365 days ago from today.
- For "last X days", calculate the appropriate date.
- Always use ISO format dates (YYYY-MM-DD).

Format your response as valid JSON with the following structure:
{
  "understanding": "Brief explanation of what the user is asking in your own words",
  "entity_types": ["commit", "pr", "issue", "file", "adr"],
  "temporal_constraints": {
    "before": "YYYY-MM-DD",
    "after": "YYYY-MM-DD",
    "version": "x.y.z"
  },
  "attributes": {
    "commit": {"author": "name"},
    "pr": {"status": "merged"},
    "issue": {"labels": ["bug", "feature"]},
    "title_keywords": ["authentication", "login"]
  },
  "relationship_focus": "MENTIONS"
}

IMPORTANT: Do NOT include any comments in the JSON. The JSON must be valid and parseable by standard JSON parsers.
Only include fields that are relevant to the query. If information is not specified or implied in the user's question, do not include it in the JSON response.
"""

KNOWLEDGE_GRAPH_SEARCH_PROMPT = """You are a specialized AI assistant for the Arc Memory knowledge graph system.
Your task is to guide the search process through a knowledge graph of code repository information.

Important: Most development teams do not formally document all decisions in ADRs. Instead, valuable reasoning and context is typically distributed across commit messages, PR descriptions, issue discussions, and code comments.

When processing queries, prioritize these search strategies:
1. Include a diverse mix of entity types (not just ADRs)
2. For "why" questions, focus heavily on commits, PRs, and issues as they often contain decision reasoning
3. For questions about code changes or features, prioritize commits and PRs
4. For questions about problems or requirements, prioritize issues
5. Only focus primarily on ADRs if the user specifically mentions architecture decisions

The nodes in the graph are connected by these relationships:
- MODIFIES: Connects commits to the files they modify
- MERGES: Connects PRs to the commits they merge
- MENTIONS: Connects PRs or issues to other entities they reference
- DECIDES: Connects ADRs to the issues they resolve

Format your response as search parameters in valid JSON:
{
  "primary_node_types": ["commit", "pr"],
  "secondary_node_types": ["issue", "adr"],
  "time_range": {
    "start": "YYYY-MM-DD",  // Use specific ISO format dates
    "end": "YYYY-MM-DD"     // Convert any relative dates to absolute dates
  },
  "search_strategy": "recent_first",
  "max_nodes_per_type": 3,
  "keywords": ["database", "schema"],
  "relationship_priorities": ["MODIFIES", "MENTIONS"]
}

IMPORTANT: Do NOT include any comments in the JSON. The JSON must be valid and parseable by standard JSON parsers.
"""

RESPONSE_GENERATION_PROMPT = """You are an expert AI assistant for Arc Memory, a knowledge graph for code repositories.
Given a user's question and a set of relevant graph nodes, create a comprehensive, accurate answer.

Important guidelines:
1. Decision reasoning is often distributed across many node types:
   - Commits often contain explanations of why a change was made
   - PR descriptions frequently explain the rationale behind changes
   - Issue discussions capture problem contexts and solution reasoning
   - ADRs formalize decisions but may be rare or missing entirely
   - Code comments and patterns can reveal design intentions

2. When answering "why" questions:
   - Synthesize reasoning from ALL available node types, not just ADRs
   - Extract implicit reasoning from commit messages and PR descriptions
   - Look for patterns across multiple nodes to infer motivations
   - Acknowledge when reasoning must be inferred versus being explicitly stated

Your response should include:
1. A brief summary (1-2 sentences)
2. A detailed answer that synthesizes information from the provided nodes
3. Clear reasoning that connects the evidence to your answer, noting when you're making inferences
4. A confidence score (1-10) indicating how well the available information answers the question

Format your response as valid JSON with the following structure:
{
  "summary": "One-line summary of the answer",
  "answer": "Detailed response to the question",
  "reasoning": "Explanation of how you arrived at this answer",
  "confidence": 7
}

IMPORTANT: Do NOT include any comments in the JSON. The JSON must be valid and parseable by standard JSON parsers.
Base your response ONLY on the provided context and be honest about limitations in the available information.
"""

QUERY_SYSTEM_PROMPT = """You are a specialized AI assistant for the Arc Memory knowledge graph system.
Your task is to parse and understand natural language queries about a codebase and its development history.

The knowledge graph contains the following types of nodes:
- commit: Git commits with code changes (these often contain valuable context about decision reasoning)
- pr: Pull requests that merge changes (PR descriptions frequently explain the rationale behind changes)
- issue: GitHub issues or Linear tickets describing problems or features (contain problem statements and solutions)
- adr: Architecture Decision Records documenting technical decisions (formal, but often rare or missing)
- file: Source code files in the repository (code itself may reveal intentions through comments and structure)

Important: Most development teams do not formally document all decisions in ADRs. Instead, valuable reasoning and context is typically distributed across commit messages, PR descriptions, issue discussions, and code comments. When processing "why" questions, prioritize looking at ALL relevant entity types, not just ADRs.

These nodes are connected by the following relationships:
- MODIFIES: Connects commits to the files they modify
- MERGES: Connects PRs to the commits they merge
- MENTIONS: Connects PRs or issues to other entities they reference
- DECIDES: Connects ADRs to the issues they resolve

When analyzing a user's question, always:
1. Include a diverse mix of entity types (not just ADRs)
2. For "why" questions, focus heavily on commits, PRs, and issues as they often contain decision reasoning
3. For questions about code changes or features, prioritize commits and PRs
4. For questions about problems or requirements, prioritize issues
5. Only focus primarily on ADRs if the user specifically mentions architecture decisions

Given a user's question, identify:
1. The primary entity types the user is asking about (commits, PRs, issues, ADRs, files)
2. Any temporal constraints (e.g., "last month", "before version 2.0")
3. Any specific attributes to filter on (e.g., author, status, title keywords)
4. The type of relationship or information the user wants to know

For temporal constraints:
- When the user mentions relative time periods like "last month", "last week", etc., convert them to specific date strings in YYYY-MM-DD format.
- For "last month", use a date 30 days ago from today.
- For "last week", use a date 7 days ago from today.
- For "last year", use a date 365 days ago from today.
- For "last X days", calculate the appropriate date.
- Always use ISO format dates (YYYY-MM-DD).

Format your response as valid JSON with the following structure:
{
  "understanding": "Brief explanation of what the user is asking in your own words",
  "entity_types": ["commit", "pr", "issue", "file", "adr"],
  "temporal_constraints": {
    "before": "YYYY-MM-DD",
    "after": "YYYY-MM-DD",
    "version": "x.y.z"
  },
  "attributes": {
    "commit": {"author": "name"},
    "pr": {"status": "merged"},
    "issue": {"labels": ["bug", "feature"]},
    "title_keywords": ["authentication", "login"]
  },
  "relationship_focus": "MENTIONS"
}

IMPORTANT: Do NOT include any comments in the JSON. The JSON must be valid and parseable by standard JSON parsers.
Only include fields that are relevant to the query. If information is not specified or implied in the user's question, do not include it in the JSON response.
"""

@debug_function
def process_query(
    db_path: Path,
    query: str,
    max_results: int = 5,
    max_hops: int = 3,
    timeout: int = 60,
    repo_ids: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Process a natural language query against the knowledge graph.

    This function implements a multi-stage approach:
    1. Query Understanding: Uses an LLM to understand the query intent
    2. Knowledge Graph Search: Converts the intent into appropriate graph queries
    3. Response Generation: Synthesizes the information into a natural language response

    Args:
        db_path: Path to the knowledge graph database
        query: Natural language query text
        max_results: Maximum number of results to return
        max_hops: Maximum number of hops in the graph traversal
        timeout: Maximum time in seconds to wait for Ollama response
        repo_ids: Optional list of repository IDs to filter by

    Returns:
        A dictionary containing the query results with these keys:
        - understanding: How the system understood the query
        - summary: One-line summary of the answer
        - answer: Detailed answer text
        - results: List of relevant nodes with metadata
        - confidence: Confidence score (1-10)
    """
    try:
        # Check for OpenAI availability first (preferred)
        openai_available = False
        if OPENAI_AVAILABLE:
            openai_available = ensure_openai_available()

        # Fall back to Ollama if OpenAI is not available
        if not openai_available and not ensure_ollama_available(timeout=timeout):
            return {
                "error": "No LLM provider available",
                "understanding": "Natural language queries require either OpenAI API access or Ollama to be installed and running. "
                                "To use OpenAI, set the OPENAI_API_KEY environment variable. "
                                "To use Ollama, install it from https://ollama.ai/download and start it with 'ollama serve'. "
                                "Then run 'ollama pull qwen3:4b' to download the default model (only ~4GB in size)."
            }

        # Connect to the database
        conn = get_connection(db_path)

        logger.info(f"Processing query: {query}")
        logger.info(f"Using max_results={max_results}, max_hops={max_hops}")

        # Stage 1: Process the query using LLM to understand intent
        logger.info("Stage 1: Understanding query intent")
        query_intent = _process_query_intent(query)

        if not query_intent:
            logger.error("Failed to process query intent")
            return {
                "error": "Failed to process query intent",
                "understanding": "I couldn't understand your question. Please try rephrasing it."
            }

        logger.info(f"Query understanding: {query_intent.get('understanding', 'No understanding available')}")

        # Stage 2: Search for relevant nodes based on the query intent
        logger.info("Stage 2: Searching knowledge graph")
        relevant_nodes = _search_knowledge_graph(
            conn,
            query_intent,
            max_results=max_results,
            max_hops=max_hops,
            repo_ids=repo_ids
        )

        if not relevant_nodes:
            logger.warning("No relevant nodes found")
            return {
                "understanding": query_intent.get("understanding", "Query understood, but no results found"),
                "summary": "No relevant information found",
                "results": []
            }

        logger.info(f"Found {len(relevant_nodes)} relevant nodes")

        # Stage 3: Generate a response using the LLM with the relevant nodes
        logger.info("Stage 3: Generating response")
        response = _generate_response(query, query_intent, relevant_nodes)

        # Close the database connection
        conn.close()

        # Return the complete response
        logger.info(f"Query processing complete. Confidence: {response.get('confidence', 'N/A')}")
        return response

    except Exception as e:
        logger.exception(f"Error processing query: {e}")
        return {
            "error": str(e),
            "understanding": "An error occurred while processing your query"
        }


@debug_function
def _process_query_intent(query: str) -> Optional[Dict[str, Any]]:
    """Process the query intent using an LLM.

    Args:
        query: The natural language query

    Returns:
        A dictionary with the parsed query intent, or None if processing failed
    """
    try:
        # Check if OpenAI is available (preferred)
        openai_client = None
        ollama_client = None

        if OPENAI_AVAILABLE and ensure_openai_available():
            logger.debug("Using OpenAI for query intent processing")
            openai_client = OpenAIClient()
        else:
            logger.debug("Using Ollama for query intent processing")
            ollama_client = OllamaClient()

        # Stage 1: Generate response with thinking for understanding the query
        logger.debug("Stage 1: Understanding query intent")

        if openai_client:
            # Use model from environment variable or default
            model = os.environ.get("OPENAI_MODEL", "gpt-4.1")
            llm_response = openai_client.generate_with_thinking(
                model=model,
                prompt=f"Parse this natural language query about a code repository: \"{query}\"",
                system=QUERY_UNDERSTANDING_PROMPT,
                options={"temperature": 0.1}  # Lower temperature for more precise parsing
            )
        else:
            # Fall back to Ollama
            llm_response = ollama_client.generate_with_thinking(
                model="qwen3:4b",
                prompt=f"Parse this natural language query about a code repository: \"{query}\"",
                system=QUERY_UNDERSTANDING_PROMPT
            )

        # Log the raw LLM response for debugging
        if DEBUG_MODE:
            debug_log(
                func_name="_process_query_intent_raw_llm",
                inputs={"query": query, "system_prompt": QUERY_UNDERSTANDING_PROMPT},
                outputs={"llm_response": llm_response}
            )

        # Extract JSON from the response
        query_intent = _extract_json_from_llm_response(llm_response)

        if not query_intent:
            logger.warning("Failed to extract query intent JSON")
            return None

        # Stage 2: Generate search parameters based on the query intent
        logger.debug("Stage 2: Generating search parameters")
        search_params_prompt = f"""
Based on this query intent:
{json.dumps(query_intent, indent=2)}

Generate appropriate search parameters for finding relevant nodes in the knowledge graph.
"""

        if openai_client:
            # Use model from environment variable or default
            model = os.environ.get("OPENAI_MODEL", "gpt-4.1")
            search_params_response = openai_client.generate_with_thinking(
                model=model,
                prompt=search_params_prompt,
                system=KNOWLEDGE_GRAPH_SEARCH_PROMPT,
                options={"temperature": 0.1}
            )
        else:
            # Fall back to Ollama
            search_params_response = ollama_client.generate_with_thinking(
                model="qwen3:4b",
                prompt=search_params_prompt,
                system=KNOWLEDGE_GRAPH_SEARCH_PROMPT
            )

        # Log the raw LLM response for debugging
        if DEBUG_MODE:
            debug_log(
                func_name="_process_search_params_raw_llm",
                inputs={"query_intent": query_intent, "system_prompt": KNOWLEDGE_GRAPH_SEARCH_PROMPT},
                outputs={"llm_response": search_params_response}
            )

        # Extract search parameters JSON
        search_params = _extract_json_from_llm_response(search_params_response)

        if not search_params:
            logger.warning("Failed to extract search parameters, falling back to query intent only")
            return query_intent

        # Merge the query intent with search parameters for a more complete search context
        enhanced_intent = {**query_intent}

        # Add search-specific parameters
        if "primary_node_types" in search_params:
            # If entity_types already exists, prioritize primary types but keep the others
            if "entity_types" in enhanced_intent:
                # Ensure primary types come first
                primary_types = search_params.get("primary_node_types", [])
                secondary_types = search_params.get("secondary_node_types", [])
                existing_types = enhanced_intent["entity_types"]

                # Create a new ordered list with primary types first
                ordered_types = []
                # Add primary types
                for type_name in primary_types:
                    if type_name not in ordered_types:
                        ordered_types.append(type_name)

                # Add existing types not in primary
                for type_name in existing_types:
                    if type_name not in ordered_types:
                        ordered_types.append(type_name)

                # Add secondary types not already included
                for type_name in secondary_types:
                    if type_name not in ordered_types:
                        ordered_types.append(type_name)

                enhanced_intent["entity_types"] = ordered_types
            else:
                # Just use all types from search params
                all_types = search_params.get("primary_node_types", []) + search_params.get("secondary_node_types", [])
                enhanced_intent["entity_types"] = all_types

        # Add search strategy metadata
        enhanced_intent["search_metadata"] = {
            "strategy": search_params.get("search_strategy", "relevance_first"),
            "max_nodes_per_type": search_params.get("max_nodes_per_type", 5),
            "relationship_priorities": search_params.get("relationship_priorities", [])
        }

        # Add keywords if present and not already in query intent
        if "keywords" in search_params and "title_keywords" not in enhanced_intent.get("attributes", {}):
            if "attributes" not in enhanced_intent:
                enhanced_intent["attributes"] = {}
            enhanced_intent["attributes"]["title_keywords"] = search_params["keywords"]

        logger.debug(f"Enhanced query intent: {enhanced_intent}")
        return enhanced_intent

    except Exception as e:
        logger.exception(f"Error in query intent processing: {e}")
        return None


def _resolve_relative_temporal_constraints(temporal_constraints: Dict[str, Any]) -> Dict[str, Any]:
    """Convert relative temporal constraints to absolute dates.

    This function handles relative time expressions like "last month", "last week",
    "last year", etc. and converts them to absolute dates.

    Args:
        temporal_constraints: Dictionary with temporal constraints

    Returns:
        Dictionary with resolved temporal constraints
    """
    if not temporal_constraints:
        return {}

    resolved_constraints = temporal_constraints.copy()
    now = datetime.now()

    # Process "after" constraint
    after_value = resolved_constraints.get("after")
    if after_value and isinstance(after_value, str):
        # Check for relative time expressions
        if re.search(r'last\s+(\d+)\s+days?', after_value, re.IGNORECASE):
            # "last X days"
            days = int(re.search(r'last\s+(\d+)\s+days?', after_value, re.IGNORECASE).group(1))
            resolved_date = (now - timedelta(days=days)).strftime("%Y-%m-%d")
            resolved_constraints["after"] = resolved_date
            logger.debug(f"Resolved relative 'after' constraint '{after_value}' to '{resolved_date}'")
        elif re.search(r'last\s+week', after_value, re.IGNORECASE):
            # "last week"
            resolved_date = (now - timedelta(days=7)).strftime("%Y-%m-%d")
            resolved_constraints["after"] = resolved_date
            logger.debug(f"Resolved relative 'after' constraint '{after_value}' to '{resolved_date}'")
        elif re.search(r'last\s+month', after_value, re.IGNORECASE):
            # "last month"
            # Go back approximately 30 days
            resolved_date = (now - timedelta(days=30)).strftime("%Y-%m-%d")
            resolved_constraints["after"] = resolved_date
            logger.debug(f"Resolved relative 'after' constraint '{after_value}' to '{resolved_date}'")
        elif re.search(r'last\s+year', after_value, re.IGNORECASE):
            # "last year"
            # Go back approximately 365 days
            resolved_date = (now - timedelta(days=365)).strftime("%Y-%m-%d")
            resolved_constraints["after"] = resolved_date
            logger.debug(f"Resolved relative 'after' constraint '{after_value}' to '{resolved_date}'")

    # Process "before" constraint
    before_value = resolved_constraints.get("before")
    if before_value and isinstance(before_value, str):
        # Check for relative time expressions
        if re.search(r'last\s+(\d+)\s+days?', before_value, re.IGNORECASE):
            # "last X days"
            days = int(re.search(r'last\s+(\d+)\s+days?', before_value, re.IGNORECASE).group(1))
            resolved_date = (now - timedelta(days=days)).strftime("%Y-%m-%d")
            resolved_constraints["before"] = resolved_date
            logger.debug(f"Resolved relative 'before' constraint '{before_value}' to '{resolved_date}'")
        elif re.search(r'last\s+week', before_value, re.IGNORECASE):
            # "last week"
            resolved_date = (now - timedelta(days=7)).strftime("%Y-%m-%d")
            resolved_constraints["before"] = resolved_date
            logger.debug(f"Resolved relative 'before' constraint '{before_value}' to '{resolved_date}'")
        elif re.search(r'last\s+month', before_value, re.IGNORECASE):
            # "last month"
            resolved_date = (now - timedelta(days=30)).strftime("%Y-%m-%d")
            resolved_constraints["before"] = resolved_date
            logger.debug(f"Resolved relative 'before' constraint '{before_value}' to '{resolved_date}'")
        elif re.search(r'last\s+year', before_value, re.IGNORECASE):
            # "last year"
            resolved_date = (now - timedelta(days=365)).strftime("%Y-%m-%d")
            resolved_constraints["before"] = resolved_date
            logger.debug(f"Resolved relative 'before' constraint '{before_value}' to '{resolved_date}'")

    return resolved_constraints


def _extract_json_from_llm_response(response: str) -> Optional[Dict[str, Any]]:
    """Extract JSON from LLM response text.

    Args:
        response: The raw LLM response text

    Returns:
        Parsed JSON object or None if extraction failed
    """
    try:
        # First, handle thinking sections
        if "<think>" in response and "</think>" in response:
            # Remove everything between <think> and </think>
            start_think = response.find("<think>")
            end_think = response.find("</think>") + len("</think>")
            response = response[:start_think] + response[end_think:]
            # Clean up any extra whitespace
            response = response.strip()

        # Check for JSON block format with code fences
        if "```json" in response:
            # Extract content between ```json and ```
            start = response.find("```json") + 7
            end = response.find("```", start)
            if end != -1:  # Ensure closing fence exists
                json_str = response[start:end].strip()
            else:
                # Handle missing closing fence
                json_str = response[start:].strip()  # Or appropriate fallback
        elif "```" in response:
            # Extract content between ``` and ```
            start = response.find("```") + 3
            end = response.find("```", start)
            json_str = response[start:end].strip()
        else:
            # Try to find JSON-like structure with outer braces
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = response[start:end].strip()
            else:
                # No JSON-like structure found
                logger.warning(f"No JSON structure found in: {response}")
                return None

        # Clean the JSON string by removing comments before parsing
        import re
        # Remove single-line comments (// comment)
        json_str = re.sub(r'//.*?$', '', json_str, flags=re.MULTILINE)
        # Remove multi-line comments (/* comment */)
        json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)
        # Clean up any trailing commas (common issue with LLM-generated JSON)
        json_str = re.sub(r',\s*}', '}', json_str)
        json_str = re.sub(r',\s*]', ']', json_str)

        # Parse the JSON
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.warning(f"Initial JSON parsing failed: {e}. Attempting to fix...")

            # Try a more lenient approach by manually fixing common issues
            # Replace single quotes with double quotes
            json_str = json_str.replace("'", "\"")

            # Fix unquoted keys
            json_str = re.sub(r'(\s*?)(\w+)(\s*?):', r'\1"\2"\3:', json_str)

            # Remove any trailing commas in objects and arrays
            json_str = re.sub(r',\s*}', '}', json_str)
            json_str = re.sub(r',\s*]', ']', json_str)

            # Fix missing commas between objects in arrays
            json_str = re.sub(r'(\})\s*(\{)', r'\1,\2', json_str)

            # Fix missing commas between array elements
            json_str = re.sub(r'(\])\s*(\[)', r'\1,\2', json_str)

            # Fix missing commas after values in objects
            json_str = re.sub(r'("[^"]*?")\s*("[^"]*?"\s*:)', r'\1,\2', json_str)
            json_str = re.sub(r'(true|false|null|\d+)\s*("[^"]*?"\s*:)', r'\1,\2', json_str)

            # Try again with the cleaned string
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e2:
                logger.warning(f"JSON parsing still failed after fixes: {e2}. Trying more aggressive fixes...")

                # If still failing, try more aggressive fixes
                try:
                    # Handle the specific error patterns from the logs
                    if "Expecting ',' delimiter" in str(e2):
                        error_parts = str(e2).split(":")
                        if len(error_parts) >= 3:
                            # Extract line and column information
                            line_col_info = error_parts[2].strip()
                            line_col_match = re.search(r'line (\d+) column (\d+)', line_col_info)
                            if line_col_match:
                                line = int(line_col_match.group(1))
                                column = int(line_col_match.group(2))

                                # Split the text into lines
                                lines = json_str.split('\n')
                                if 0 < line <= len(lines):
                                    # Insert a comma at the problematic position
                                    problem_line = lines[line-1]
                                    if 0 < column <= len(problem_line):
                                        # Special handling for column 22 (common in the error logs)
                                        if column == 22:
                                            # This is likely after a "confidence" value
                                            if '"confidence": 0' in problem_line:
                                                fixed_line = problem_line.replace('"confidence": 0', '"confidence": 0,')
                                                lines[line-1] = fixed_line
                                                logger.debug(f"Fixed missing comma after confidence value at line {line}")
                                            elif '"confidence": ' in problem_line:
                                                # More general case for any confidence value
                                                fixed_line = re.sub(r'("confidence": \d+(?:\.\d+)?)\s+', r'\1, ', problem_line)
                                                lines[line-1] = fixed_line
                                                logger.debug(f"Fixed missing comma after confidence value at line {line}")
                                            else:
                                                # General case for column 22 - insert a comma
                                                fixed_line = problem_line[:column-1] + ',' + problem_line[column-1:]
                                                lines[line-1] = fixed_line
                                                logger.debug(f"Inserted comma at line {line}, column {column}")
                                        # Special handling for column 209 (seen in adr:adr-006-blast-radius-prediction.md)
                                        elif column >= 200 and column <= 210:
                                            # For column ~209, insert a comma at the position
                                            fixed_line = problem_line[:column-1] + ',' + problem_line[column-1:]
                                            lines[line-1] = fixed_line
                                            logger.debug(f"Inserted comma at line {line}, column {column} (special case for ~209)")
                                        else:
                                            # General case - insert a comma at the problematic position
                                            fixed_line = problem_line[:column-1] + ',' + problem_line[column-1:]
                                            lines[line-1] = fixed_line
                                            logger.debug(f"Inserted comma at line {line}, column {column}")

                                    json_str = '\n'.join(lines)

                    # Try to parse with the more aggressively fixed text
                    return json.loads(json_str)
                except Exception as fix_error:
                    logger.debug(f"Error during aggressive fixes: {fix_error}")
                    # Continue to regex fallback

                # If that still fails, continue with regex fallback
                raise  # Re-raise the original exception to trigger the fallback

    except json.JSONDecodeError as e:
        logger.warning(f"JSON parse error: {e}, response: {response}")

        # Fallback: Try regex to find JSON-like structure
        import re
        try:
            # More robust regex pattern to find the outermost JSON object
            pattern = r'(\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\}))*\}))*\})'
            match = re.search(pattern, response, re.DOTALL)
            if match:
                json_str = match.group(0)
                # Clean the JSON string again
                json_str = re.sub(r'//.*?$', '', json_str, flags=re.MULTILINE)
                json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)
                json_str = re.sub(r',\s*}', '}', json_str)
                json_str = re.sub(r',\s*]', ']', json_str)

                # Try to parse the cleaned JSON
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    # If still failing, try more aggressive fixes
                    # Fix missing commas after values in objects
                    json_str = re.sub(r'("[^"]*?")\s*("[^"]*?"\s*:)', r'\1,\2', json_str)
                    json_str = re.sub(r'(true|false|null|\d+)\s*("[^"]*?"\s*:)', r'\1,\2', json_str)

                    # Try again
                    try:
                        return json.loads(json_str)
                    except json.JSONDecodeError:
                        # Continue to next fallback
                        pass
        except Exception as regex_err:
            logger.warning(f"Regex fallback also failed to parse JSON: {regex_err}")

        # Last resort: Try to manually fix the specific issue we're seeing with o4-mini
        try:
            # The specific error we're seeing is with comments in the JSON
            # Try to manually remove any line with // in it
            lines = response.split('\n')
            cleaned_lines = [line for line in lines if '//' not in line]
            cleaned_json = '\n'.join(cleaned_lines)

            # Try to extract and parse again
            start = cleaned_json.find("{")
            end = cleaned_json.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = cleaned_json[start:end].strip()

                # Apply all our fixes one more time
                json_str = re.sub(r',\s*}', '}', json_str)
                json_str = re.sub(r',\s*]', ']', json_str)
                json_str = re.sub(r'("[^"]*?")\s*("[^"]*?"\s*:)', r'\1,\2', json_str)
                json_str = re.sub(r'(true|false|null|\d+)\s*("[^"]*?"\s*:)', r'\1,\2', json_str)

                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    # If still failing, return a minimal valid structure instead of None
                    logger.warning("All JSON parsing attempts failed. Returning minimal structure.")
                    return {"understanding": "Query understood, but JSON parsing failed"}
        except Exception as manual_err:
            logger.warning(f"Manual cleanup failed: {manual_err}")

        # Return a minimal valid structure instead of None
        logger.warning("All JSON parsing attempts failed. Returning minimal structure.")
        return {"understanding": "Query understood, but JSON parsing failed"}
    except Exception as e:
        logger.exception(f"Error extracting JSON: {e}")
        # Return a minimal valid structure instead of None
        return {"understanding": "Query understood, but JSON parsing failed"}


def _search_knowledge_graph(
    conn: sqlite3.Connection,
    query_intent: Dict[str, Any],
    max_results: int = 5,
    max_hops: int = 3,
    repo_ids: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """Search the knowledge graph for nodes relevant to the query intent.

    Args:
        conn: Database connection
        query_intent: The parsed query intent
        max_results: Maximum number of results to return
        max_hops: Maximum number of hops in the graph traversal
        repo_ids: Optional list of repository IDs to filter by

    Returns:
        List of relevant nodes with metadata
    """
    try:
        # Extract search parameters from enhanced query intent
        search_metadata = query_intent.get("search_metadata", {})
        search_strategy = search_metadata.get("strategy", "relevance_first")
        max_nodes_per_type = search_metadata.get("max_nodes_per_type", max_results // 2)
        relationship_priorities = search_metadata.get("relationship_priorities", [])

        # Extract entity types
        entity_types = query_intent.get("entity_types", [])
        if not entity_types:
            # Default to all types if none specified
            entity_types = ["commit", "pr", "issue", "adr", "file"]

        # Convert string entity types to NodeType enum
        node_types = []
        for entity_type in entity_types:
            try:
                node_type = NodeType(entity_type)
                node_types.append(node_type)
            except ValueError:
                logger.warning(f"Unknown entity type: {entity_type}")

        if not node_types:
            logger.warning("No valid node types found")
            return []

        # Extract attributes for filtering
        attributes = query_intent.get("attributes", {})
        title_keywords = attributes.get("title_keywords", [])

        # Extract temporal constraints
        temporal_constraints = query_intent.get("temporal_constraints", {})

        # Start with an empty list of seed nodes
        seed_nodes = []

        # First, search based on entity types and title keywords
        for node_type in node_types[:2]:  # Start with the first two types (highest priority)
            type_nodes = _find_nodes_by_type_and_keywords(
                conn,
                node_type,
                title_keywords,
                temporal_constraints,
                limit=max_nodes_per_type,
                repo_ids=repo_ids
            )
            seed_nodes.extend(type_nodes)

            # If we have enough seed nodes, stop searching
            if len(seed_nodes) >= max_nodes_per_type * 2:
                break

        # If we don't have enough seed nodes, try the remaining types
        if len(seed_nodes) < max_nodes_per_type and len(node_types) > 2:
            for node_type in node_types[2:]:
                type_nodes = _find_nodes_by_type_and_keywords(
                    conn,
                    node_type,
                    title_keywords,
                    temporal_constraints,
                    limit=max_nodes_per_type,
                    repo_ids=repo_ids
                )
                seed_nodes.extend(type_nodes)

                # If we have enough seed nodes, stop searching
                if len(seed_nodes) >= max_nodes_per_type * 2:
                    break

        # If no seed nodes found, try a fallback approach
        if not seed_nodes:
            logger.warning("No seed nodes found with initial search, trying fallback approach")

            # Fallback 1: Try without temporal constraints
            if temporal_constraints:
                logger.info("Fallback 1: Trying without temporal constraints")
                for node_type in node_types[:2]:  # Start with the first two types
                    # Use empty temporal constraints
                    type_nodes = _find_nodes_by_type_and_keywords(
                        conn,
                        node_type,
                        title_keywords,
                        {},  # Empty temporal constraints
                        limit=max_nodes_per_type,
                        repo_ids=repo_ids
                    )
                    seed_nodes.extend(type_nodes)

                    if len(seed_nodes) >= max_nodes_per_type:
                        break

            # Fallback 2: Try with just the node types, no keywords or constraints
            if not seed_nodes:
                logger.info("Fallback 2: Trying with just node types, no keywords or constraints")
                for node_type in node_types:
                    # Direct query by type only
                    cursor = conn.cursor()
                    query = "SELECT * FROM nodes WHERE type = ? ORDER BY timestamp DESC LIMIT ?"
                    params = [node_type.value, max_nodes_per_type]

                    # Add repository filter if specified
                    if repo_ids:
                        placeholders = ", ".join(["?"] * len(repo_ids))
                        query = f"SELECT * FROM nodes WHERE type = ? AND repo_id IN ({placeholders}) ORDER BY timestamp DESC LIMIT ?"
                        params = [node_type.value] + repo_ids + [max_nodes_per_type]

                    try:
                        cursor.execute(query, params)

                        for row in cursor.fetchall():
                            # Create Node objects
                            node_data = {
                                'id': row["id"],
                                'type': NodeType(row["type"]) if row["type"] else None,
                                'title': row["title"],
                                'body': row["body"]
                            }

                            # Add optional fields
                            if "url" in row and row["url"]:
                                node_data['url'] = row["url"]

                            if "repo_id" in row and row["repo_id"]:
                                node_data['repo_id'] = row["repo_id"]

                            if "merged" in row and row["merged"] is not None:
                                node_data['merged'] = bool(row["merged"])

                            # Create the node
                            node = Node(**node_data)

                            # Add timestamp if available
                            if "timestamp" in row and row["timestamp"]:
                                try:
                                    node.ts = datetime.fromisoformat(row["timestamp"])
                                except (ValueError, TypeError):
                                    pass

                            seed_nodes.append(node)
                    except sqlite3.Error as e:
                        logger.warning(f"Error executing query for node type {node_type.value}: {e}")
                        continue

                    if len(seed_nodes) >= max_nodes_per_type * 2:
                        break

            # Fallback 3: Get any nodes, regardless of type
            if not seed_nodes:
                logger.info("Fallback 3: Getting any nodes regardless of type")
                try:
                    cursor = conn.cursor()
                    query = "SELECT * FROM nodes ORDER BY timestamp DESC LIMIT ?"
                    params = [max_nodes_per_type * 3]

                    # Add repository filter if specified
                    if repo_ids:
                        placeholders = ", ".join(["?"] * len(repo_ids))
                        query = f"SELECT * FROM nodes WHERE repo_id IN ({placeholders}) ORDER BY timestamp DESC LIMIT ?"
                        params = repo_ids + [max_nodes_per_type * 3]

                    cursor.execute(query, params)

                    for row in cursor.fetchall():
                        try:
                            # Create Node objects
                            node_data = {
                                'id': row["id"],
                                'type': NodeType(row["type"]) if row["type"] else NodeType.FILE,  # Default to FILE if type is missing
                                'title': row["title"] or "Untitled",  # Default title if missing
                                'body': row["body"]
                            }

                            # Add optional fields
                            if "url" in row and row["url"]:
                                node_data['url'] = row["url"]

                            if "repo_id" in row and row["repo_id"]:
                                node_data['repo_id'] = row["repo_id"]

                            # Create the node
                            node = Node(**node_data)

                            # Add timestamp if available
                            if "timestamp" in row and row["timestamp"]:
                                try:
                                    node.ts = datetime.fromisoformat(row["timestamp"])
                                except (ValueError, TypeError):
                                    pass

                            seed_nodes.append(node)
                        except Exception as node_error:
                            logger.warning(f"Error creating node from row: {node_error}")
                            continue
                except sqlite3.Error as e:
                    logger.warning(f"Error executing fallback query: {e}")

            # If still no seed nodes, return a minimal result set
            if not seed_nodes:
                logger.warning("No seed nodes found after all fallback approaches")
                # Return a minimal result with an explanation instead of an empty list
                return [{
                    "id": "no_results",
                    "type": "info",
                    "title": "No Results Found",
                    "body": "No relevant information was found in the knowledge graph for this query. "
                            "This could be because the information doesn't exist in the graph, or "
                            "because the query terms don't match the available content."
                }]

            logger.info(f"Found {len(seed_nodes)} seed nodes using fallback approach")

        # Score and rank the seed nodes
        scored_nodes = _score_nodes(seed_nodes, query_intent)

        # Select top nodes after scoring
        top_seed_nodes = scored_nodes[:max(3, max_nodes_per_type)]

        # Expand the search from seed nodes based on search strategy
        if search_strategy == "broad_first":
            # Broad search prioritizes finding a diverse set of related nodes
            max_hops = max(2, max_hops)  # Ensure at least 2 hops
            expanded_nodes = _expand_search(conn, top_seed_nodes, max_hops, max_results, repo_ids)
        elif search_strategy == "recent_first":
            # Recent search prioritizes newer nodes
            expanded_nodes = _expand_search(conn, top_seed_nodes, max_hops, max_results, repo_ids)
            # Sort by timestamp (newest first)
            expanded_nodes = sorted(expanded_nodes, key=lambda n: n.ts if n.ts else datetime.min, reverse=True)
        else:  # Default to relevance_first
            # Relevance search uses the scoring function
            expanded_nodes = _expand_search(conn, top_seed_nodes, max_hops, max_results * 2, repo_ids)
            expanded_nodes = _score_nodes(expanded_nodes, query_intent)

        # Format the nodes for response
        relevant_nodes = []
        for node in expanded_nodes[:max_results]:
            # Start with basic fields that should always be present
            formatted_node = {
                "id": node.id,
                "type": node.type.value if node.type else "unknown",
            }

            # Add other fields only if they exist and aren't None
            if hasattr(node, "title") and node.title is not None:
                formatted_node["title"] = node.title

            if hasattr(node, "body") and node.body is not None:
                formatted_node["body"] = node.body

            if hasattr(node, "url") and node.url is not None:
                formatted_node["url"] = node.url

            if hasattr(node, "ts") and node.ts is not None:
                formatted_node["timestamp"] = node.ts.isoformat()

            # Add type-specific fields
            if node.type == NodeType.COMMIT:
                # Short hash (first 8 characters) for commits
                if len(node.id) >= 8:
                    formatted_node["hash"] = node.id[:8]

            elif node.type == NodeType.PR:
                if hasattr(node, "merged"):
                    formatted_node["status"] = "merged" if node.merged else "open"

            elif node.type == NodeType.ISSUE:
                # Extract status and labels from extra data if available
                if hasattr(node, "extra") and node.extra and isinstance(node.extra, dict):
                    if "status" in node.extra:
                        formatted_node["status"] = node.extra["status"]
                    if "labels" in node.extra:
                        formatted_node["labels"] = node.extra["labels"]

            relevant_nodes.append(formatted_node)

        return relevant_nodes

    except Exception as e:
        logger.exception(f"Error searching knowledge graph: {e}")
        return []

# Helper function to find nodes by type and keywords
def _find_nodes_by_type_and_keywords(
    conn: sqlite3.Connection,
    node_type: NodeType,
    keywords: List[str],
    temporal_constraints: Dict[str, Any],
    limit: int = 5,
    repo_ids: Optional[List[str]] = None
) -> List[Node]:
    """Find nodes by type and keywords.

    Args:
        conn: Database connection
        node_type: Type of node to search for
        keywords: List of keywords to search for
        temporal_constraints: Temporal constraints for filtering
        limit: Maximum number of nodes to return
        repo_ids: Optional list of repository IDs to filter by

    Returns:
        List of matching nodes
    """
    try:
        cursor = conn.cursor()

        # Base query
        query = "SELECT * FROM nodes WHERE type = ?"
        params = [node_type.value]

        # Add repository filter if specified
        if repo_ids:
            placeholders = ", ".join(["?"] * len(repo_ids))
            query += f" AND (repo_id IN ({placeholders}))"
            params.extend(repo_ids)

        # Add keyword filters if any
        if keywords:
            keyword_conditions = []
            for keyword in keywords:
                # Search in title and body
                keyword_conditions.append("(title LIKE ? OR body LIKE ?)")
                params.extend([f"%{keyword}%", f"%{keyword}%"])

            if keyword_conditions:
                query += " AND (" + " OR ".join(keyword_conditions) + ")"

        # Resolve any relative temporal constraints to absolute dates
        resolved_constraints = _resolve_relative_temporal_constraints(temporal_constraints)

        # Log the resolution of temporal constraints
        if resolved_constraints != temporal_constraints:
            logger.debug(f"Resolved temporal constraints: {temporal_constraints} -> {resolved_constraints}")

        # Add temporal constraints if any
        if "before" in resolved_constraints:
            query += " AND timestamp <= ?"
            params.append(resolved_constraints["before"])

        if "after" in resolved_constraints:
            query += " AND timestamp >= ?"
            params.append(resolved_constraints["after"])

        # Order by timestamp descending (newest first) if available
        query += " ORDER BY timestamp DESC NULLS LAST"

        # Add limit
        query += " LIMIT ?"
        params.append(limit)

        # Execute query
        cursor.execute(query, params)

        # Convert to Node objects
        nodes = []
        for row in cursor.fetchall():
            # Initialize with required fields
            node_data = {
                'id': row["id"],
                'type': NodeType(row["type"]) if row["type"] else None,
                'title': row["title"],
                'body': row["body"]
            }

            # Add optional fields if they exist
            if "url" in row:
                node_data['url'] = row["url"]

            if "merged" in row:
                node_data['merged'] = bool(row["merged"]) if row["merged"] is not None else None

            # Create the node
            node = Node(**node_data)

            # Add timestamp if available
            if "timestamp" in row and row["timestamp"]:
                try:
                    node.ts = datetime.fromisoformat(row["timestamp"])
                except (ValueError, TypeError):
                    pass

            # Add extra data if available
            if "extra" in row and row["extra"]:
                try:
                    node.extra = json.loads(row["extra"])
                except (json.JSONDecodeError, TypeError):
                    pass

            nodes.append(node)

        return nodes

    except Exception as e:
        logger.exception(f"Error finding nodes by type and keywords: {e}")
        return []

def _expand_search(
    conn: sqlite3.Connection,
    seed_nodes: List[Node],
    max_hops: int,
    max_results: int,
    repo_ids: Optional[List[str]] = None
) -> List[Node]:
    """Expand the search from seed nodes using graph relationships.

    Args:
        conn: Database connection
        seed_nodes: Initial set of nodes to expand from
        max_hops: Maximum number of hops in the graph traversal
        max_results: Maximum number of results to return
        repo_ids: Optional list of repository IDs to filter by

    Returns:
        List of additional nodes found through graph traversal
    """
    try:
        # Keep track of visited nodes to avoid duplicates
        visited_ids = set(node.id for node in seed_nodes)
        expanded_nodes = list(seed_nodes)  # Start with the seed nodes

        # Queue for BFS traversal
        from collections import deque
        queue = deque([(node.id, 1) for node in seed_nodes])  # (node_id, hop_count)

        # Perform BFS traversal
        while queue and len(expanded_nodes) < max_results:
            node_id, hop_count = queue.popleft()

            # Skip if max hops reached
            if hop_count > max_hops:
                continue

            # Get connected nodes
            connected_ids = get_connected_nodes(conn, node_id)

            # Process each connected node
            for connected_id in connected_ids:
                if connected_id not in visited_ids:
                    visited_ids.add(connected_id)

                    # Get the node from the database
                    node = get_node_by_id(conn, connected_id)
                    if node:
                        # Filter by repository ID if specified
                        if repo_ids and hasattr(node, 'repo_id') and node.repo_id is not None:
                            if node.repo_id not in repo_ids:
                                continue

                        expanded_nodes.append(node)

                        # Add to queue for further expansion
                        if hop_count < max_hops:
                            queue.append((connected_id, hop_count + 1))

                    # Check if we have enough nodes
                    if len(expanded_nodes) >= max_results:
                        break

        return expanded_nodes

    except Exception as e:
        logger.exception(f"Error expanding search: {e}")
        return []


def _score_nodes(nodes: List[Node], query_intent: Dict[str, Any]) -> List[Node]:
    """Score and rank nodes by relevance to the query.

    Args:
        nodes: List of nodes to score
        query_intent: The parsed query intent

    Returns:
        List of nodes sorted by relevance score (most relevant first)
    """
    try:
        scored_nodes = []

        # Extract scoring criteria from query intent
        entity_types = query_intent.get("entity_types", [])
        title_keywords = query_intent.get("attributes", {}).get("title_keywords", [])
        temporal_constraints = query_intent.get("temporal_constraints", {})

        for node in nodes:
            score = 0

            # Score based on entity type
            if entity_types and node.type and node.type.value in entity_types:
                score += 5

            # Score based on title keywords
            if title_keywords and node.title:
                for keyword in title_keywords:
                    if keyword.lower() in node.title.lower():
                        score += 3

            # Score based on temporal constraints
            if temporal_constraints and node.ts:
                # Handle "after" constraint
                if "after" in temporal_constraints:
                    after_date = datetime.fromisoformat(temporal_constraints["after"])
                    if node.ts > after_date:
                        score += 2

                # Handle "before" constraint
                if "before" in temporal_constraints:
                    before_date = datetime.fromisoformat(temporal_constraints["before"])
                    if node.ts < before_date:
                        score += 2

                # Handle version constraint (for commits and PRs)
                if "version" in temporal_constraints and node.type in [NodeType.COMMIT, NodeType.PR]:
                    # Check if version is mentioned in title or body
                    version = temporal_constraints["version"]
                    if (node.title and version in node.title) or (node.body and version in node.body):
                        score += 4

            # Add to scored nodes list
            scored_nodes.append((node, score))

        # Sort by score (descending) and return just the nodes
        scored_nodes.sort(key=lambda x: x[1], reverse=True)
        return [node for node, _ in scored_nodes]

    except Exception as e:
        logger.exception(f"Error scoring nodes: {e}")
        return nodes  # Return unsorted nodes on error

@debug_function
def _generate_response(
    query: str,
    query_intent: Dict[str, Any],
    relevant_nodes: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Generate a natural language response to the query.

    Args:
        query: The original natural language query
        query_intent: The parsed query intent
        relevant_nodes: List of relevant nodes with metadata

    Returns:
        A dictionary with the response including summary, answer, and results
    """
    try:
        # Check if OpenAI is available (preferred)
        openai_client = None
        ollama_client = None

        if OPENAI_AVAILABLE and ensure_openai_available():
            logger.debug("Using OpenAI for response generation")
            openai_client = OpenAIClient()
        else:
            logger.debug("Using Ollama for response generation")
            ollama_client = OllamaClient()

        # Prepare context from relevant nodes
        context_str = json.dumps(relevant_nodes, indent=2)

        # Define the system prompt for response generation - now using the dedicated prompt
        system_prompt = RESPONSE_GENERATION_PROMPT

        # Generate the response with the LLM
        llm_prompt = f"""User's question: {query}

Query understanding: {query_intent.get('understanding', 'Not available')}

Relevant information from the knowledge graph:
{context_str}

Based on this information, please answer the user's question."""

        # Generate response with thinking for better reasoning
        if openai_client:
            # Use model from environment variable or default
            model = os.environ.get("OPENAI_MODEL", "gpt-4.1")
            llm_response = openai_client.generate_with_thinking(
                model=model,
                prompt=llm_prompt,
                system=system_prompt,
                options={"temperature": 0.2}  # Slightly higher temperature for more natural responses
            )
        else:
            # Fall back to Ollama
            llm_response = ollama_client.generate_with_thinking(
                model="qwen3:4b",
                prompt=llm_prompt,
                system=system_prompt
            )

        # Log the raw LLM response for debugging
        if DEBUG_MODE:
            debug_log(
                func_name="_generate_response_raw_llm",
                inputs={
                    "query": query,
                    "query_intent": query_intent,
                    "relevant_nodes_count": len(relevant_nodes),
                    "system_prompt": system_prompt
                },
                outputs={"llm_response": llm_response}
            )

        # Extract JSON from the response
        response_json = _extract_json_from_llm_response(llm_response)

        if not response_json:
            # Fallback for parsing errors
            return {
                "understanding": query_intent.get("understanding", "Query understood, but response processing failed"),
                "summary": "Unable to generate a structured response",
                "answer": "I encountered an error while processing the information from the knowledge graph.",
                "results": relevant_nodes,
                "confidence": 1
            }

        # Combine the response with the original query understanding and relevant nodes
        final_response = {
            "understanding": query_intent.get("understanding", "Not available"),
            "summary": response_json.get("summary", "No summary available"),
            "answer": response_json.get("answer", "No detailed answer available"),
            "results": relevant_nodes,
            "confidence": response_json.get("confidence", 5)
        }

        # Add reasoning to each result if available
        if "reasoning" in response_json:
            # Add overall reasoning to the response
            final_response["reasoning"] = response_json["reasoning"]

        return final_response

    except Exception as e:
        logger.exception(f"Error generating response: {e}")
        return {
            "understanding": query_intent.get("understanding", "Query understood, but response generation failed"),
            "summary": "Error generating response",
            "answer": f"An error occurred while generating the response: {e}",
            "results": relevant_nodes,
            "confidence": 1
        }
