# Office Assistant Policy Query Feature

## Overview

The Office Assistant now includes the ability to answer questions about company policies using ChromaDB for semantic search and retrieval.

## Features

- **Semantic Policy Search**: Uses ChromaDB with sentence transformers to find relevant policies based on natural language queries
- **Policy Categories**: Supports queries across all policy categories including:
  - Leave policies (vacation, sick leave)
  - Work arrangements (remote work, flexible hours)
  - Compensation (overtime, expenses)
  - Workplace conduct (dress code, security)
  - Travel policies
  - Performance management

## How It Works

1. **Policy Loading**: Policies from `example_policies.json` are automatically loaded into ChromaDB on startup
2. **Embedding Generation**: Each policy is embedded using the `all-MiniLM-L6-v2` sentence transformer
3. **Semantic Search**: User queries are embedded and matched against policy embeddings using cosine similarity
4. **Relevance Scoring**: Results are ranked by relevance and returned with metadata

## Usage Examples

### Policy Questions
- "How many vacation days do I get per year?"
- "What is the work from home policy?"
- "What are the overtime rules?"
- "What is the dress code?"
- "How do I request sick leave?"
- "What are the travel expense limits?"

### Request Processing
- "I need to take a day off on 2024-12-25 for Christmas"
- "Can I work from home tomorrow?"
- "I need to book a meeting room for next Tuesday at 2 PM"

## Technical Implementation

### Dependencies
- `chromadb`: Vector database for policy storage and retrieval
- `sentence-transformers`: For generating embeddings
- `openai`: For LLM integration

### Key Functions
- `initialize_chroma_db()`: Sets up ChromaDB client and embedding model
- `load_policies_to_chroma()`: Loads policies from JSON into ChromaDB
- `query_policies(question, n_results=3)`: Performs semantic search
- `query_policy(question)`: Formats and returns policy information

### Database Structure
- **Collection**: "policies"
- **Documents**: Policy text content
- **Metadata**: Category, version, effective date, department
- **Embeddings**: Generated using sentence-transformers

## Testing

Run the demo script to test policy queries:
```bash
python demo_policy_queries.py
```

Or test individual functionality:
```bash
python simple_test.py
```

## Configuration

Ensure your `.env` file contains:
```
MODEL=your_model_name
OPENAI_BASE_URL=your_openai_base_url
OPENAI_API_KEY=your_api_key
MAX_TOKENS=200
```

## Error Handling

The system gracefully handles:
- ChromaDB connection issues
- Missing policy files
- Embedding generation errors
- API failures

If policy queries fail, the assistant will inform the user and continue with other functionality.
