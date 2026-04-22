# Enterprise Support Resolution Copilot

## Goal
Build a support agent for a SaaS company that answers questions from:
- product docs
- release notes
- help-center articles
- historical tickets

The project will use:
- Azure AI Search
- LangGraph
- LangSmith
- FastAPI
- Microsoft Foundry Agent Service

---

## Learning style
We are building this step by step for learning and mastery.

Rules:
- one step at a time
- understand why each step matters
- do not rush into the full build
- focus on strong foundations first
- only move to the next step after the current step is complete

---

## What I completed

### Step 1: Environment setup
Completed:
- Installed Python
- Installed VS Code
- Installed Git
- Installed Azure Developer CLI (`azd`)
- Created the project folder
- Created and activated the virtual environment

Why it mattered:
- This created the base environment needed to build and run the project
- It prepared the system for Azure, Python, and later deployment work

Notes:
- `azd version` worked outside VS Code first
- Issue was related to terminal/session refresh, not project code

---

### Step 2: Project skeleton and local API
Completed:
- Installed core Python packages:
  - `fastapi`
  - `uvicorn`
  - `python-dotenv`
  - `pydantic`
  - `azure-search-documents`
  - `langgraph`
  - `langchain-core`
  - `langsmith`
- Created project structure
- Created:
  - `.env`
  - `.env.example`
  - `.gitignore`
  - `requirements.txt`
- Created:
  - `app/config.py`
  - `app/api.py`
  - `app/__init__.py`
- Started the FastAPI app successfully
- Verified the root endpoint worked:
  - `http://127.0.0.1:8000/`

Why it mattered:
- This turned the project into a real runnable Python app
- It established config management and a clean structure
- It gave us the first working service that future features will plug into

What I learned:
- `requirements.txt` lists packages but does not install them by itself
- `uvicorn` must run from the correct active environment
- Python imports depend on the current working directory
- I must run the app from the actual project folder:
  - `enterprise-support-copilot`

Notes:
- `favicon.ico 404` is normal for now
- Root route is working correctly

---

### Step 3: Config cleanup and health endpoint
Completed:
- Strengthened environment-based configuration
- Updated `app/config.py` to centralize settings
- Added integration status checks for:
  - Azure AI Search
  - LangSmith
  - Microsoft Foundry Agent Service
- Added `/health` endpoint in FastAPI
- Verified the health endpoint returned app status and integration flags

Why it mattered:
- This made the app easier to manage and debug
- It created a clean place for environment-driven settings
- It gave a reliable health check before connecting external services

What I learned:
- Configuration should be centralized early
- Health endpoints are useful before adding real business logic
- Integration flags help verify setup without guessing

---

### Step 4: Azure AI Search setup and first connection
Completed:
- Created Azure subscription resources needed for search
- Created an Azure AI Search service
- Found and copied the Azure AI Search endpoint
- Retrieved the Azure AI Search admin key
- Created an Azure Storage account
- Created a blob container:
  - `support-docs`
- Created and uploaded a test file:
  - `test-doc.txt`
- Used the Azure portal import flow to create an index from blob storage
- Verified the created index in Azure:
  - `search-1775664160172`
- Added Azure values into `.env`
- Created `app/search.py`
- Added a debug route:
  - `/debug/search`
- Successfully tested the Azure AI Search connection
- Verified document count returned:
  - `1`

Why it mattered:
- This was the first real cloud connection in the project
- It proved the local app could talk to a live Azure Search index
- It confirmed the index existed and contained data

What I learned:
- Azure setup must exist before code can connect to it
- Endpoint, index name, and API key must match exactly
- Small connection tests are better than mixing setup with retrieval logic
- Environment variable naming must be consistent across `.env` and Python code

Notes:
- There was a config mismatch between `AZURE_SEARCH_KEY` and `AZURE_SEARCH_API_KEY`
- Fixing the env variable name resolved the missing configuration issue

---

### Step 5: First real search query
Completed:
- Added `run_search()` in `app/search.py`
- Added a query debug route:
  - `/debug/search-query`
- Ran the first real search query against Azure AI Search
- Tested query mismatch:
  - `login` returned no results
- Tested matching query:
  - `log in` returned 1 result
- Verified returned fields included:
  - `id`
  - `title`
  - `content`
  - `@search.score`

Why it mattered:
- This was the first real retrieval step for the copilot
- It proved the system could query indexed support content
- It showed how search behavior depends on wording

What I learned:
- `login` and `log in` are not always treated the same way
- Search depends on the indexed text and analyzer behavior
- Query wording matters even before adding semantic or LLM layers

---

### Step 6: Clean retrieval results
Completed:
- Cleaned the search response format in `run_search()`
- Reduced returned fields to:
  - `id`
  - `title`
  - `content`
  - `score`
- Added `top` support to control number of returned results
- Updated `/debug/search-query` to accept:
  - `q`
  - `top`
- Added `top` into the returned JSON
- Added `make_snippet()` helper
- Returned both:
  - `snippet`
  - `content`

Why it mattered:
- Raw Azure search objects were too noisy for app use
- Clean retrieval output makes future answer generation easier
- Separating snippet from full content prepares the app for both UI and LLM use cases

What I learned:
- Retrieval responses should be structured for the next layer, not just dumped raw
- `top` is important for controlling how much context comes back
- Snippets are useful for previews, while full content is useful for later answer generation

---

### Step 7: Built the first `/ask` endpoint
Completed:
- Added `AskRequest` request model
- Added `POST /ask` endpoint
- Made `/ask` accept JSON input:
  - `question`
  - `top`
- Reused retrieval logic to search based on the question
- Returned a cleaner app-facing response shape:
  - `question`
  - `top`
  - `context_count`
  - `context`
- Added handling for no retrieved context
- Added safe fallback response when nothing matched

Why it mattered:
- This created the first question-based retrieval API
- It bridged user input and retrieval behavior
- It established the first real support-copilot request flow

What I learned:
- App-facing endpoints should not expose raw tool responses unnecessarily
- No-context handling matters early to prevent bad answer generation later
- Response shape consistency helps future frontend and orchestration layers

---

### Step 8: Added deterministic answer building
Completed:
- Added a draft answer builder
- Returned structured `response` data from `/ask`
- Improved answer format to include:
  - `answer`
  - `answer_type`
  - `sources`
  - `primary_source`
- Improved wording of the draft answer to sound more support-friendly
- Added extraction of likely causes from the retrieved snippet
- Added suggested `next_steps`
- Added fallback next steps when no specific causes were found
- Added a simple confidence classifier:
  - `high`
  - `medium`
  - `low`
- Unified the no-context response shape so it also returns structured `response`

Why it mattered:
- This created the first full retrieval-to-response pipeline
- It showed how the system can turn retrieved context into usable support guidance
- It established the structure that a future LLM layer can follow

What I learned:
- A system can become meaningfully smarter even before using an LLM
- Extracting structured guidance from context is better than only echoing snippets
- Confidence and next-step suggestions make the API more practical

Notes:
- At one point `app/answering.py` had duplicate code after a `return`
- That extra dead code was removed and the file was cleaned up

---

### Step 9: Refactored into cleaner modules
Completed:
- Moved answer-building logic into:
  - `app/answering.py`
- Moved request models into:
  - `app/models.py`
- Created a service layer:
  - `app/services.py`
- Moved `/ask` orchestration into:
  - `handle_ask()`
- Added helper builders for:
  - success response
  - no-context response

Why it mattered:
- This separated responsibilities across the codebase
- It made the project easier to understand and extend
- It prepared the architecture for LangGraph later

What I learned:
- `api.py` should stay focused on routes
- Retrieval, answering, models, and orchestration should live in separate files
- Refactoring early makes future workflow changes easier

---

### Step 10: Stronger input validation
Completed:
- Added stricter validation in `app/models.py`
- Used Pydantic `Field` to validate:
  - `question`
  - `top`
- Restricted `top` to:
  - minimum `1`
  - maximum `10`
- Added a validator to trim whitespace from `question`
- Rejected empty or whitespace-only questions at the model layer
- Added service-layer protection for empty questions too
- Verified invalid inputs return proper FastAPI validation errors

Why it mattered:
- This made the API safer and cleaner
- It prevented invalid requests from reaching retrieval logic
- It created a more production-style validation approach

What I learned:
- Input validation should happen as early as possible
- FastAPI and Pydantic can block bad requests before business logic runs
- Even if validation exists in models, service-level safety checks are still useful

---

### Step 11: Basic LangSmith tracing setup
Completed:
- Added LangSmith environment variables into `.env`:
  - `LANGSMITH_TRACING=true`
  - `LANGSMITH_API_KEY=...`
  - `LANGSMITH_PROJECT=enterprise-support-copilot`
- Confirmed `.env` loading was already in place
- Added top-level tracing to `handle_ask()`
- Ran the FastAPI app and tested `/ask`
- Verified the trace appeared in LangSmith

Why it mattered:
- This was the first observability step for the support workflow
- It proved the application could send traced runs to LangSmith
- It gave a debugging view of the support question flow

What I learned:
- LangSmith should be connected before adding deeper workflow logic
- Tracing must be verified with a real request, not just configuration
- The first goal is visibility, not complexity

---

### Step 12: Added nested child traces
Completed:
- Added `@traceable(name="run_search")` to `run_search()` in `app/search.py`
- Verified `run_search` appeared as a child run under the top-level trace
- Added `@traceable(name="build_draft_answer")` to `build_draft_answer()` in `app/answering.py`
- Verified both child traces appeared in LangSmith

Why it mattered:
- This broke the support flow into observable internal steps
- It made it possible to see whether retrieval or answer building was responsible for weak behavior
- It prepared the app for more advanced debugging later

What I learned:
- Nested tracing works naturally when traced functions call other traced functions
- A top-level trace alone is useful, but child traces make debugging much more practical
- Observability should mirror the architecture

---

### Step 13: Improved trace readability
Completed:
- Inspected `run_search` input and output in LangSmith
- Inspected `build_draft_answer` input and output in LangSmith
- Verified the top-level trace output was already readable enough for debugging
- Renamed the top-level trace from:
  - `handle_ask`
  to:
  - `support_question_flow`

Why it mattered:
- Clear trace names make LangSmith easier to use as the project grows
- Better naming helps distinguish code-level functions from workflow-level operations
- This made the top-level run easier to understand at a glance

What I learned:
- Naming matters in observability, not just in code
- Sometimes the biggest improvement is not more metadata, but better labels
- Inspecting existing trace output first avoids unnecessary decoration

---

### Step 14: Added top-level tags and metadata
Completed:
- Added a static tag to the top-level trace:
  - `support-api`
- Added static metadata to the top-level trace:
  - `component: services`

Why it mattered:
- This made top-level traces easier to organize and filter in LangSmith
- It established a consistent tagging pattern before adding request-specific metadata

What I learned:
- Start with small, static metadata first
- Tags and metadata are useful when they reflect architecture and workflow role
- It is better to add simple structure early than random labels later

---

### Step 15: Added child-trace tags and metadata
Completed:
- Added tags and metadata to `run_search()`:
  - tag: `support-search`
  - metadata: `component: search`
- Added tags and metadata to `build_draft_answer()`:
  - tag: `support-answering`
  - metadata: `component: answering`

Why it mattered:
- This made child traces easier to inspect independently
- It aligned the trace labeling with the module boundaries in the codebase

What I learned:
- Child traces benefit from the same structure as top-level traces
- Consistent metadata across components makes later debugging easier
- Observability should reflect system responsibility boundaries

---

### Step 16: Added dynamic metadata for `top`
Completed:
- Passed request-specific metadata to `handle_ask()` from the `/ask` route using:
  - `langsmith_extra={"metadata": {"top": request.top}}`
- Verified `top` appeared in the top-level LangSmith trace

Why it mattered:
- This was the first request-level dynamic metadata field
- It made traces more useful for comparing behavior across retrieval settings

What I learned:
- Static metadata belongs in decorators
- Request-specific metadata belongs at invocation time
- Small per-request fields are often the most useful later

---

### Step 17: Added dynamic metadata for `question_length`
Completed:
- Added:
  - `question_length: len(request.question)`
  into `langsmith_extra` in `app/api.py`
- Verified it appeared in the LangSmith trace

Why it mattered:
- This added another useful signal for comparing short vs long queries
- It made traces more informative without exposing unnecessary noise

What I learned:
- Safe, simple metadata can reveal patterns later
- Query length can be a useful retrieval and UX signal
- Dynamic metadata should stay lightweight and intentional

---

### Step 18: Added `context_count` into top-level trace metadata
Completed:
- Imported `get_current_run_tree` in `app/services.py`
- Updated top-level trace metadata inside `handle_ask()` after retrieval returned
- Added:
  - `context_count = len(context)`
- Verified it appeared in LangSmith

Why it mattered:
- This created an immediate retrieval-quality signal in the trace
- It helped distinguish “bad retrieval” from “bad answer generation”

What I learned:
- Some metadata is only known after part of the workflow runs
- Updating the current run inside the traced function is the right pattern for such values
- Retrieval count is one of the most useful debugging fields

---

### Step 19: Added `answer_type` into top-level trace metadata
Completed:
- Updated `handle_ask()` so both return paths set:
  - `answer_type = no_context`
  - or `answer_type = retrieval_based_draft`
- Verified both success and no-context branches were correctly reflected in LangSmith metadata

Why it mattered:
- This made it easy to filter traces by outcome type
- It improved observability of system behavior, not just system inputs

What I learned:
- Outcome metadata is just as important as input metadata
- Trace metadata should reflect both the request and the result
- Branch-specific metadata helps quickly debug system behavior

---

### Step 20: Created the first manual eval question set
Completed:
- Created:
  - `eval/manual_questions.json`
- Added 5 starter questions:
  - 4 supported-style questions
  - 1 clearly unsupported question
- Created:
  - `eval/load_manual_questions.py`
- Verified the JSON could be loaded correctly

Why it mattered:
- This was the first reusable eval dataset for the project
- It moved testing beyond manual typing into a small repeatable structure

What I learned:
- A tiny dataset is enough to start evaluation work
- Reusable questions are better than ad hoc manual testing
- File-path handling matters when building local tools

Notes:
- Updated file loading to use:
  - `Path(__file__).parent / "manual_questions.json"`
  so it works regardless of the terminal working directory

---

### Step 21: Built the first local eval runner
Completed:
- Created:
  - `eval/run_manual_eval.py`
- Loaded the 5 manual questions
- Sent each question to the local `/ask` endpoint
- Printed the result for each question

Why it mattered:
- This created the first batch-style evaluation runner
- It proved the app could be tested automatically across multiple cases

What I learned:
- Even a simple loop over `/ask` is valuable
- Batch testing is much better than clicking each question manually
- The eval runner is the bridge between the app and structured evaluation

---

### Step 22: Saved eval results to JSON
Completed:
- Updated `eval/run_manual_eval.py` to collect results in a list
- Saved results to:
  - `eval/manual_eval_results.json`

Why it mattered:
- This made eval runs persistent and inspectable
- It allowed later comparisons across code changes

What I learned:
- Printed output is useful for quick testing, but saved output is necessary for real evaluation
- Structured JSON output is a strong foundation for later scoring

---

### Step 23: Verified saved eval output structure
Completed:
- Inspected the first result object
- Verified it included:
  - `id`
  - `question`
  - `status_code`
  - `ok`
  - `context_count`
  - `answer_type`
  - `primary_source`
  - `confidence`
  - `answer`
- Inspected the last unsupported-question object and confirmed it looked correct

Why it mattered:
- This confirmed the eval output structure was trustworthy before adding scoring logic
- It ensured the unsupported case was being captured correctly

What I learned:
- Verify structure before building metrics on top of it
- Unsupported examples are just as important as supported ones

---

### Step 24: Added expected labels to manual questions
Completed:
- Updated `eval/manual_questions.json` so each question includes:
  - `expected_has_context`
- Updated the eval runner to carry that expected field into saved results

Why it mattered:
- This created the first ground-truth label for evaluation
- It made it possible to compare expected behavior against actual behavior

What I learned:
- Evaluation requires expected labels, even if they are very simple at first
- The easiest useful label was “should this question retrieve support context or not”

---

### Step 25: Added first retrieval pass/fail check
Completed:
- Added:
  - `passed_context_check`
- Rule used:
  - expected context → pass if `context_count > 0`
  - expected no context → pass if `context_count == 0`
- Verified all 5 starter questions passed this check

Why it mattered:
- This created the first actual evaluation metric
- It turned the dataset from “saved outputs” into “measurable outputs”

What I learned:
- Even a simple pass/fail rule is valuable
- Retrieval behavior can be evaluated before using an LLM judge

---

### Step 26: Printed summary score in terminal
Completed:
- Added terminal summary fields:
  - total questions
  - passed
  - failed
  - pass rate

Why it mattered:
- This gave an immediate score after each eval run
- It made the runner more useful without opening the JSON file every time

What I learned:
- Quick summaries improve iteration speed
- Eval runners should provide both detail and overview

---

### Step 27: Saved summary and results together
Completed:
- Changed the saved eval output from a raw list to a structured object with:
  - `summary`
  - `results`
- Verified both top-level keys appeared in the JSON output

Why it mattered:
- This made the results file more self-contained and easier to compare later
- It organized per-run metrics and per-question details together

What I learned:
- Evaluation output should have both run-level and item-level structure
- Good file shape makes future automation easier

---

### Step 28: Added no-context response behavior check
Completed:
- Added:
  - `passed_no_context_answer_check`
- Rule used:
  - for unsupported questions, `answer_type` must be `no_context`
  - for supported questions, this check remains `True`
- Verified the unsupported question passed this check

Why it mattered:
- This checked not only retrieval behavior, but also response behavior
- It ensured unsupported questions were handled correctly by the app

What I learned:
- Retrieval is not the only thing to evaluate
- Behavior on unsupported inputs matters just as much

---

### Step 29: Added overall pass/fail per question
Completed:
- Added:
  - `passed_overall`
- Rule used:
  - overall pass only if:
    - `passed_context_check == True`
    - and `passed_no_context_answer_check == True`
- Verified all 5 starter questions passed overall

Why it mattered:
- This created a single final pass/fail field per result
- It simplified overall evaluation logic

What I learned:
- It helps to combine smaller checks into one final score
- A clean “overall pass” is easier to summarize and compare

---

### Step 30: Made summary use overall pass logic
Completed:
- Updated summary scoring to count:
  - `passed_overall`
  instead of:
  - `passed_context_check`
- Verified the summary still showed all questions passing

Why it mattered:
- This aligned the scoreboard with the real evaluation logic
- It prevented the summary from being misleading

What I learned:
- Summary metrics should reflect the true final check, not an intermediate one

---

### Step 31: Saved `top` into each eval result
Completed:
- Added:
  - `top`
  into each saved result object
- Verified it appeared in the results JSON

Why it mattered:
- This made each saved result self-describing
- It prepared the runner for later comparison across different retrieval settings

What I learned:
- A good result file should not depend on memory for run settings
- Configuration values should be saved alongside outputs

---

### Step 32: Made `TOP_K` configurable in the eval runner
Completed:
- Replaced hardcoded `top=3` in payloads with:
  - `TOP_K = 3`
- Verified results still recorded `top: 3`

Why it mattered:
- This created a single control point for retrieval depth during evaluation
- It made the runner easier to reuse for future experiments

What I learned:
- Small configuration refactors reduce future friction
- Repeated values should become named constants early

---

### Step 33: Saved `top_k` in eval summary
Completed:
- Added:
  - `top_k`
  into the `summary` block
- Verified it appeared in the results JSON

Why it mattered:
- This made the run-level summary reflect the run configuration
- It improved comparability across eval runs

What I learned:
- Configuration should be visible at both item and run level when it matters

---

### Step 34: Printed `Top K` in terminal summary
Completed:
- Added:
  - `Top K: {TOP_K}`
  into the terminal summary
- Verified it printed correctly

Why it mattered:
- This aligned terminal output with JSON output
- It made quick eval runs easier to interpret

What I learned:
- The terminal summary and the saved JSON should tell the same story

---

### Step 35: Added run timestamp
Completed:
- Added:
  - `RUN_TIMESTAMP = datetime.now(UTC).isoformat()`
- Saved:
  - `run_timestamp`
  into the eval summary
- Printed the timestamp in terminal summary too

Why it mattered:
- This gave each eval run a clear time marker
- It made run history more trustworthy than relying on file modified times

What I learned:
- Time is part of experiment context
- Timestamps are essential once history files are involved

---

### Step 36: Kept terminal summary aligned with JSON summary
Completed:
- Verified run timestamp was printed in the terminal summary as well
- Confirmed terminal and JSON outputs stayed aligned

Why it mattered:
- It kept quick terminal inspection and saved output consistent
- It reduced confusion when comparing results

What I learned:
- Consistency between quick output and saved output matters

---

### Step 37: Saved timestamped history files
Completed:
- Changed results saving from a fixed filename to a timestamped history filename:
  - `manual_eval_results_<timestamp>.json`
- Replaced `:` with `-` in the timestamp so filenames work on Windows
- Verified new history files were created correctly

Why it mattered:
- This preserved eval history instead of overwriting the same file
- It made later comparison across runs possible

What I learned:
- Eval history is valuable even in small projects
- Filenames need platform-safe timestamps

---

### Step 38: Added a stable latest-results file
Completed:
- Kept timestamped history output
- Also wrote the same payload to:
  - `manual_eval_results_latest.json`
- Verified both files were created

Why it mattered:
- Timestamped files preserve history
- A stable latest file provides a fixed path for quick inspection

What I learned:
- It is useful to have both history and a stable “current” artifact

---

### Step 39: Printed saved output paths
Completed:
- Added terminal print lines for:
  - history file path
  - latest file path
- Verified both paths printed correctly

Why it mattered:
- This removed the need to guess where files were saved
- It improved usability of the eval runner

What I learned:
- Small UX improvements matter even in developer tools

---

### Step 40: Added basic request safety guards
Completed:
- Added:
  - `timeout=10`
  to `requests.post(...)`
- Added:
  - `response.raise_for_status()`
- Verified normal runs still worked

Why it mattered:
- This prevented the eval runner from hanging forever
- It made HTTP failures fail clearly instead of silently

What I learned:
- Eval runners should fail clearly and safely
- Timeouts are basic but important protection

---

### Step 41: Added per-question request error handling
Completed:
- Wrapped each request in a `try/except`
- If a request failed, created a fallback result with:
  - `answer_type = eval_request_error`
  - `status_code = 0`
  - low-confidence failure message
- Verified one request failure would not stop the whole batch

Why it mattered:
- This made the runner resilient
- It ensured one broken request did not destroy the entire eval run

What I learned:
- Batch evaluation tools should continue through partial failures
- Errors should become data, not crashes

---

### Step 42: Made request errors fail checks explicitly
Completed:
- Added:
  - `is_request_error`
- Updated:
  - `passed_context_check`
  - `passed_no_context_answer_check`
  - `passed_overall`
  so request errors always evaluate to `False`
- Verified normal runs still worked

Why it mattered:
- This prevented request failures from being mistaken for valid no-context results
- It closed an important evaluation loophole

What I learned:
- Failure cases must be explicitly handled in scoring logic
- Silent false positives are worse than visible errors

---

---

### Step 44: Expanded retrieval testing beyond the initial login-only theme
Completed:
- Expanded `eval/manual_questions.json` from the original small set to a broader set of realistic SaaS support questions
- Added more support-style paraphrases and short user phrasing
- Verified the eval runner could handle the larger set without request errors
- Confirmed the system was ready for retrieval-quality expansion, not just LangSmith tracing

Why it mattered:
- This moved the project from a narrow proof of concept to broader retrieval testing
- It created a better stress test for search behavior and support relevance
- It exposed where the next real retrieval weaknesses were

What I learned:
- Passing a small eval set does not mean retrieval is strong enough
- More realistic and varied questions are necessary before moving to bigger orchestration work
- Retrieval should be pressure-tested before adding more system complexity

---

### Step 45: Improved support content instead of relying on score tweaking
Completed:
- Decided not to rely on arbitrary search score tuning just to improve pass rate
- Recognized that weak retrieval performance was partly caused by tiny and narrow support content
- Improved indexed support content rather than trying to “game” thresholds
- Confirmed that content quality and indexing quality were major parts of retrieval performance

Why it mattered:
- This kept the project focused on better system quality rather than cosmetic metric chasing
- It made the retrieval improvements more realistic and explainable
- It established a better mindset for later scaling

What I learned:
- Better content is often a stronger fix than threshold fiddling
- Retrieval quality depends heavily on document coverage
- Evaluation should improve the system, not just the score

---

### Step 46: Verified indexing issues before changing retrieval logic
Completed:
- Uploaded new support files to Azure Blob Storage
- Discovered that some new files were uploaded but not yet indexed
- Verified indexing status using the existing debug endpoint
- Reran the Azure Search indexer so the uploaded support documents became searchable

Why it mattered:
- This prevented debugging the wrong layer
- It confirmed that some earlier failures were caused by missing indexed content, not retrieval logic itself
- It reinforced the correct workflow: upload → index → query → evaluate

What I learned:
- Blob upload alone is not enough; the index must actually refresh
- Missing indexed content can make search look worse than it really is
- Always verify the search index before changing retrieval logic

---

### Step 47: Added realistic support documents for multiple SaaS support themes
Completed:
- Added support content for:
  - billing and subscription
  - user invitations and permissions
  - notifications and email delivery
  - performance and slow loading
- Added a clean login/account-access support file:
  - `login-account-access-support.txt`
- Moved toward a more intentional knowledge-base structure instead of relying on `test-doc.txt`
- Uploaded and indexed the new support files in Azure Search

Why it mattered:
- This expanded the knowledge base from one narrow issue family into multiple realistic SaaS support themes
- It improved retrieval coverage across common day-to-day support cases
- It created a much stronger foundation for future answer generation and evaluation

What I learned:
- Realistic support coverage needs multiple themes, not one test file
- Clear document naming and structure matter once the knowledge base grows
- Broader content makes retrieval improvements more meaningful

---

### Step 48: Tested and removed dependence on query normalization
Completed:
- Added a temporary normalization experiment for `login` → `log in`
- Used it to confirm that wording mismatch was one real retrieval issue
- Later reran retrieval tests without normalization after improving support content and indexing
- Confirmed the system could perform well without relying on normalization as a permanent solution

Why it mattered:
- This helped separate temporary patching from real long-term design
- It confirmed that better indexed support content reduced the need for brittle normalization rules
- It kept the project focused on scalable retrieval improvements

What I learned:
- Query normalization can help in specific cases, but it is not the ultimate solution
- Better content and better retrieval structure matter more than ad hoc string replacements
- Temporary experiments are useful, but they should not automatically become architecture

---

### Step 49: Added a service-layer relevance gate to block false positives
Completed:
- Added a relevance gate inside `app/services.py`
- Stopped blindly trusting every retrieved result
- Changed the system so raw search could still return candidates, but the service layer decides whether the context is trustworthy enough to use
- Verified that clearly out-of-scope questions could be turned into `no_context` at the app level

Why it mattered:
- This gave the app a cleaner boundary between “search found something” and “the app should trust it”
- It prevented irrelevant results from automatically becoming user-facing answers
- It made retrieval decision logic more explicit and explainable

What I learned:
- Search results and trustworthy context are not always the same thing
- Service-layer relevance checks are often clearer than hiding everything inside search code
- A small guardrail can improve user-facing behavior significantly

---

### Step 50: Evolved the relevance gate from score-only to theme-based matching
Completed:
- Tried simple score-based trust logic and found it was too crude
- Observed that score alone could still allow obviously irrelevant matches
- Replaced the simplistic gate with a theme-based relevance gate in `app/services.py`
- Grouped support concepts into themes such as:
  - auth/account
  - billing
  - invitations/permissions
  - notifications/email
  - performance/loading
- Allowed context only when the question and retrieved result aligned on the same support theme

Why it mattered:
- This created a much more explainable retrieval control mechanism
- It blocked nonsense queries without rejecting valid support intent as often as the score-only approach
- It scaled better as support themes expanded

What I learned:
- Search score alone is not a reliable proxy for relevance
- Exact keyword overlap is often too rigid
- Theme-based relevance matching is a more practical middle ground for this project stage

---

### Step 51: Refined theme keywords to reduce false positives
Completed:
- Discovered that overly generic performance keywords such as:
  - `app`
  - `page`
  were causing false positives
- Tightened the performance theme keywords to remove overly broad terms
- Re-ran eval after the keyword refinement
- Verified that the remaining out-of-scope false positives were eliminated

Why it mattered:
- This improved precision without weakening valid support retrieval too much
- It showed that theme design matters just as much as theme existence
- It helped the relevance gate become more practical and realistic

What I learned:
- Some keywords are too generic to be useful in a relevance gate
- Theme design requires careful word choice, not just more words
- Small keyword refinements can have a large effect on false positives

---

### Step 52: Expanded the eval set to 30 and then 40 realistic questions
Completed:
- Added new billing and invitations/permissions questions
- Increased the eval set to 30 questions and reached 30/30 passing
- Added notifications/email and performance/loading questions
- Increased the eval set to 40 questions
- Iteratively fixed theme-gate coverage for the new support themes
- Reached 40/40 passing with 0 request errors

Why it mattered:
- This significantly improved confidence in the current retrieval baseline
- It tested retrieval quality across multiple realistic SaaS support categories
- It proved that the current support knowledge base and relevance gate work together effectively on a broader question set

What I learned:
- Expanding the eval set reveals the next real weaknesses faster than guessing
- New support themes often require gate updates, not necessarily retrieval rewrites
- A broader eval set is one of the best ways to harden the system step by step

---

### Step 53: Cleaned the knowledge-base structure around the login theme
Completed:
- Created:
  - `login-account-access-support.txt`
- Uploaded and indexed it successfully
- Verified search results included the new login/account-access file
- Confirmed the system still passed the full eval after replacing the improvised login support content with a cleaner file structure

Why it mattered:
- This made the knowledge base more intentional and easier to maintain
- It reduced reliance on `test-doc.txt` as the effective login support document
- It improved the project’s content structure without sacrificing performance

What I learned:
- Clean content structure matters once the knowledge base grows
- Replacing placeholder documents with real support-theme documents improves maintainability
- Cleanup work is worth doing once the baseline is stable

---

### Step 54: Added realistic FAQ-style support documents for broader corpus learning
Completed:
- Added FAQ-style support documents for:
  - billing
  - login and account access
  - invitations and permissions
  - notifications and email delivery
  - performance and slow loading
- Uploaded the new FAQ documents to Azure Blob Storage
- Reran the Azure Search indexer after each upload batch
- Verified the new FAQ documents appeared in search results

Why it mattered:
- This made the knowledge base more realistic by mixing support article style and FAQ style documents
- It showed how document shape affects retrieval ranking
- It moved the project closer to real support knowledge-base behavior instead of a neatly hand-shaped corpus

What I learned:
- Corpus balance matters, not just retrieval code
- If one theme has FAQ coverage and others do not, ranking can become distorted
- More realistic documents expose weaknesses that clean test docs can hide

---

### Step 55: Learned that mixed document styles can break retrieval and answer quality
Completed:
- Reran the full local eval after adding FAQ-style documents
- Observed the pass rate drop significantly after the new corpus was indexed
- Inspected failed question IDs and traced failures to:
  - FAQ-style documents outranking the wrong themes
  - answer-quality checks failing because FAQ docs did not contain numbered troubleshooting steps
- Used this as a debugging and learning step instead of treating it as a regression panic

Why it mattered:
- This showed how retrieval behavior changes when the corpus becomes more realistic
- It revealed that answer-building logic had been overly dependent on numbered-step support docs
- It turned the ingestion phase into a real retrieval stress test

What I learned:
- A stronger corpus can lower eval scores before the system adapts
- Retrieval failures and answer-quality failures need to be separated carefully
- Search ranking, corpus shape, and answer extraction all influence final performance

---

### Step 56: Improved answer extraction to handle FAQ-style documents
Completed:
- Updated `extract_recommended_steps(...)` in `app/answering.py`
- Kept support for numbered troubleshooting steps
- Added a second pass to extract useful sentences from FAQ-style `A:` lines
- Verified the answer builder could now produce actionable next steps from FAQ content too

Why it mattered:
- This made the answer layer work across mixed document styles
- It reduced dependence on one specific content format
- It improved answer quality for FAQ-driven retrieval cases

What I learned:
- Answer extraction logic must evolve with document formats
- FAQ answers can still provide good actionable steps if parsed carefully
- Retrieval quality and answer usefulness should be improved together

---

### Step 57: Added failed question printing to the eval runner
Completed:
- Updated `eval/run_manual_eval.py` to print:
  - failed question IDs
  - failed question text
- Added `failed_ids` into the saved summary JSON
- Improved terminal usability so failures no longer needed to be inspected manually from the results file

Why it mattered:
- This made debugging much faster during larger-ingestion experiments
- It removed repeated manual file inspection work
- It improved the eval runner as a learning tool

What I learned:
- Developer tools should surface the most useful debugging signals directly
- Small quality-of-life improvements save a lot of time during iterative testing
- Failed IDs are especially useful once the eval set grows

---

### Step 58: Fixed retrieval contamination by balancing FAQ coverage across themes
Completed:
- Updated `billing-faq.txt` to reduce generic wording and make it more billing-specific
- Added:
  - `login-faq.txt`
  - `invitations-permissions-faq.txt`
- Uploaded the new FAQ documents and reran indexing
- Verified problematic queries started ranking the correct theme more naturally

Why it mattered:
- This reduced cross-theme retrieval contamination
- It showed that corpus balancing can fix ranking issues without immediately changing retrieval code
- It made the corpus more symmetrical across major support themes

What I learned:
- FAQ coverage should be balanced across themes
- Generic FAQ wording can become too competitive in search
- Content cleanup is often a better first fix than forcing retrieval logic changes

---

### Step 59: Strengthened service logic by filtering each retrieved result individually
Completed:
- Identified a failure case where the top raw result was wrong but lower-ranked results were correct
- Updated the service flow to filter retrieved results item-by-item using relevance checks
- Stopped rejecting the full result set based only on the first raw result
- Verified supported queries could still succeed even when raw ranking was noisy

Why it mattered:
- This made the system more robust against messy real-world search results
- It improved retrieval behavior for mixed and ambiguous corpora
- It preserved correct lower-ranked results instead of throwing away the whole response opportunity

What I learned:
- One bad top result should not always kill the whole response
- Relevance filtering is stronger when applied per result instead of only to the first match
- Messier corpora require more resilient context selection logic

---

### Step 60: Restored a clean 40/40 eval run on a more realistic mixed corpus
Completed:
- Reran the full local eval after corpus balancing and per-result relevance filtering
- Reached:
  - `40 / 40 passed`
  - `0 request errors`
- Confirmed the system still passed after:
  - multiple support themes
  - support article style docs
  - FAQ-style docs
  - more realistic retrieval ambiguity

Why it mattered:
- This proved the system could recover and stay strong under a more realistic corpus
- It validated the combined improvements across retrieval, answer quality, and corpus structure
- It created a stronger baseline than the earlier cleaner-only support corpus

What I learned:
- Passing on a realistic corpus is more meaningful than passing on a clean toy corpus
- Content balancing and relevance filtering work well together
- Strong eval recovery after a corpus expansion is a real milestone

---

### Step 61: Started LangGraph by wrapping the existing support flow in a minimal graph
Completed:
- Created:
  - `app/graph.py`
- Built a minimal LangGraph wrapper using:
  - graph state
  - one node
  - `START`
  - `END`
- Wrapped the existing `handle_ask(...)` flow inside the graph
- Verified the graph compiled and invoked successfully

Why it mattered:
- This introduced the LangGraph mental model without forcing a large rewrite
- It taught how to represent the existing workflow as graph state and nodes
- It established the first LangGraph-backed execution path in the project

What I learned:
- The best first LangGraph step is to wrap a working function, not rebuild the whole system
- Graph state, nodes, edges, and compile/invoke are the core beginner concepts
- LangGraph can be introduced incrementally

---

### Step 62: Split the graph into multiple nodes and connected the real API route to LangGraph
Completed:
- Replaced the one-node graph with a multi-node graph
- Split the flow into:
  - search
  - filtering
  - response-building
- Updated `/ask` in `app/api.py` to call `support_graph.invoke(...)`
- Verified the real FastAPI route worked through LangGraph

Why it mattered:
- This moved LangGraph from a side test into the real application path
- It taught how to model the workflow as separate graph steps
- It created a more explicit orchestration structure

What I learned:
- LangGraph becomes useful when node responsibilities are separated
- Connecting the graph to the real API is the first real integration milestone
- It is safer to preserve existing behavior while changing orchestration

---

### Step 63: Added graph branching and preserved relevance filtering inside the graph
Completed:
- Added conditional routing after retrieval/filtering
- Created separate branches for:
  - answer path
  - no-context path
- Detected that the graph initially trusted raw search results too much
- Fixed the graph so it preserved the same per-result relevance filtering used by the service flow
- Verified:
  - supported questions went to `retrieval_based_draft`
  - unsupported questions went to `no_context`

Why it mattered:
- This taught that graph nodes must preserve important protections from the earlier service flow
- It introduced conditional graph routing as a real orchestration mechanism
- It made the graph behavior more faithful to the application’s intended logic

What I learned:
- Raw retrieval and usable context are not the same thing
- Conditional routing is one of the most important LangGraph concepts
- When logic moves into a graph, safeguards must move with it

---

### Step 64: Added debug state, ambiguity signals, and ambiguity-aware graph branching
Completed:
- Added explicit graph-state fields for:
  - `raw_result_count`
  - `filtered_result_count`
  - `is_ambiguous`
- Updated `app/test_graph.py` to print raw and filtered counts and top titles
- Verified supported questions could have:
  - noisy raw results
  - filtered relevant results
  - ambiguity marked in state
- Added an ambiguity-aware branch so the graph could respond differently when multiple relevant results survived filtering

Why it mattered:
- This made the graph easier to debug and understand
- It taught how graph state can carry derived quality/debug signals
- It introduced routing based on retrieval quality, not just empty vs non-empty context

What I learned:
- State can hold both business data and debugging signals
- Ambiguity is a useful first-class workflow concept
- Conditional routing can depend on retrieval quality signals, not just existence of context

---

### Step 65: Separated ambiguity handling into a post-processing node and added final response assembly
Completed:
- Refactored the graph so ambiguity handling became its own node:
  - `annotate_ambiguous_answer`
- Added:
  - `prepare_final_response`
  as a dedicated final formatting node
- Changed branch nodes to produce intermediate response payload data instead of fully formatted API responses
- Verified the final API response shape still worked correctly
- Verified LangSmith traces showed the graph-backed flow and branching behavior

Why it mattered:
- This created a cleaner LangGraph design
- It taught the difference between:
  - generating intermediate response data
  - formatting final output
- It made the graph more modular and easier to reason about

What I learned:
- A good graph separates decision logic, post-processing, and final formatting
- Post-processing nodes are useful for controlled response adjustments
- Final response assembly is cleaner when handled in one dedicated node

---


### Step 66: Added realistic FAQ-style support documents for broader corpus learning
Completed:
- Added FAQ-style support documents for:
  - billing
  - login and account access
  - invitations and permissions
  - notifications and email delivery
  - performance and slow loading
- Uploaded the new FAQ documents to Azure Blob Storage
- Reran the Azure Search indexer after uploads
- Verified the new FAQ documents appeared in search results

Why it mattered:
- This made the knowledge base more realistic by mixing support article style and FAQ style documents
- It showed how document shape affects retrieval ranking
- It moved the project closer to real support knowledge-base behavior instead of a neatly hand-shaped corpus

What I learned:
- Corpus balance matters, not just retrieval code
- If one theme has FAQ coverage and others do not, ranking can become distorted
- More realistic documents expose weaknesses that clean test docs can hide

---

### Step 67: Learned that mixed document styles can break retrieval and answer quality
Completed:
- Reran the full local eval after adding FAQ-style documents
- Observed the pass rate drop significantly after the new corpus was indexed
- Inspected failed question IDs and traced failures to:
  - FAQ-style documents outranking the wrong themes
  - answer-quality checks failing because FAQ docs did not contain numbered troubleshooting steps

Why it mattered:
- This showed how retrieval behavior changes when the corpus becomes more realistic
- It revealed that answer-building logic had been overly dependent on numbered-step support docs
- It turned the ingestion phase into a real retrieval stress test

What I learned:
- A stronger corpus can lower eval scores before the system adapts
- Retrieval failures and answer-quality failures need to be separated carefully
- Search ranking, corpus shape, and answer extraction all influence final performance

---

### Step 68: Improved answer extraction to handle FAQ-style documents
Completed:
- Updated `extract_recommended_steps(...)` in `app/answering.py`
- Kept support for numbered troubleshooting steps
- Added a second pass to extract useful sentences from FAQ-style `A:` lines
- Verified the answer builder could now produce actionable next steps from FAQ content too

Why it mattered:
- This made the answer layer work across mixed document styles
- It reduced dependence on one specific content format
- It improved answer quality for FAQ-driven retrieval cases

What I learned:
- Answer extraction logic must evolve with document formats
- FAQ answers can still provide good actionable steps if parsed carefully
- Retrieval quality and answer usefulness should be improved together

---

### Step 69: Added failed question printing to the eval runner
Completed:
- Updated `eval/run_manual_eval.py` to print:
  - failed question IDs
  - failed question text
- Added `failed_ids` into the saved summary JSON
- Improved terminal usability so failures no longer needed to be inspected manually from the results file

Why it mattered:
- This made debugging much faster during larger-ingestion experiments
- It removed repeated manual file inspection work
- It improved the eval runner as a learning tool

What I learned:
- Developer tools should surface the most useful debugging signals directly
- Small quality-of-life improvements save a lot of time during iterative testing
- Failed IDs are especially useful once the eval set grows

---

### Step 70: Fixed retrieval contamination by balancing FAQ coverage across themes
Completed:
- Updated `billing-faq.txt` to reduce generic wording and make it more billing-specific
- Added:
  - `login-faq.txt`
  - `invitations-permissions-faq.txt`
- Uploaded the new FAQ documents and reran indexing
- Verified problematic queries started ranking the correct theme more naturally

Why it mattered:
- This reduced cross-theme retrieval contamination
- It showed that corpus balancing can fix ranking issues without immediately changing retrieval code
- It made the corpus more symmetrical across major support themes

What I learned:
- FAQ coverage should be balanced across themes
- Generic FAQ wording can become too competitive in search
- Content cleanup is often a better first fix than forcing retrieval logic changes

---

### Step 71: Strengthened service logic by filtering each retrieved result individually
Completed:
- Identified a failure case where the top raw result was wrong but lower-ranked results were correct
- Updated the service flow to filter retrieved results item-by-item using relevance checks
- Stopped rejecting the full result set based only on the first raw result
- Verified supported queries could still succeed even when raw ranking was noisy

Why it mattered:
- This made the system more robust against messy real-world search results
- It improved retrieval behavior for mixed and ambiguous corpora
- It preserved correct lower-ranked results instead of throwing away the whole response opportunity

What I learned:
- One bad top result should not always kill the whole response
- Relevance filtering is stronger when applied per result instead of only to the first match
- Messier corpora require more resilient context selection logic

---

### Step 72: Restored a clean 40/40 eval run on a more realistic mixed corpus
Completed:
- Reran the full local eval after corpus balancing and per-result relevance filtering
- Reached:
  - `40 / 40 passed`
  - `0 request errors`
- Confirmed the system still passed after:
  - multiple support themes
  - support article style docs
  - FAQ-style docs
  - more realistic retrieval ambiguity

Why it mattered:
- This proved the system could recover and stay strong under a more realistic corpus
- It validated the combined improvements across retrieval, answer quality, and corpus structure
- It created a stronger baseline than the earlier cleaner-only support corpus

What I learned:
- Passing on a realistic corpus is more meaningful than passing on a clean toy corpus
- Content balancing and relevance filtering work well together
- Strong eval recovery after a corpus expansion is a real milestone

---

### Step 73: Started LangGraph by wrapping the existing support flow in a minimal graph
Completed:
- Created:
  - `app/graph.py`
- Built a minimal LangGraph wrapper using:
  - graph state
  - one node
  - `START`
  - `END`
- Wrapped the existing `handle_ask(...)` flow inside the graph
- Verified the graph compiled and invoked successfully

Why it mattered:
- This introduced the LangGraph mental model without forcing a large rewrite
- It taught how to represent the existing workflow as graph state and nodes
- It established the first LangGraph-backed execution path in the project

What I learned:
- The best first LangGraph step is to wrap a working function, not rebuild the whole system
- Graph state, nodes, edges, and compile/invoke are the core beginner concepts
- LangGraph can be introduced incrementally

---

### Step 74: Split the graph into multiple nodes and connected the real API route to LangGraph
Completed:
- Replaced the one-node graph with a multi-node graph
- Split the flow into:
  - search
  - filtering
  - response-building
- Updated `/ask` in `app/api.py` to call `support_graph.invoke(...)`
- Verified the real FastAPI route worked through LangGraph

Why it mattered:
- This moved LangGraph from a side test into the real application path
- It taught how to model the workflow as separate graph steps
- It created a more explicit orchestration structure

What I learned:
- LangGraph becomes useful when node responsibilities are separated
- Connecting the graph to the real API is the first real integration milestone
- It is safer to preserve existing behavior while changing orchestration

---

### Step 75: Added graph branching and preserved relevance filtering inside the graph
Completed:
- Added conditional routing after retrieval/filtering
- Created separate branches for:
  - answer path
  - no-context path
- Detected that the graph initially trusted raw search results too much
- Fixed the graph so it preserved the same per-result relevance filtering used by the service flow
- Verified:
  - supported questions went to `retrieval_based_draft`
  - unsupported questions went to `no_context`

Why it mattered:
- This taught that graph nodes must preserve important protections from the earlier service flow
- It introduced conditional graph routing as a real orchestration mechanism
- It made the graph behavior more faithful to the application’s intended logic

What I learned:
- Raw retrieval and usable context are not the same thing
- Conditional routing is one of the most important LangGraph concepts
- When logic moves into a graph, safeguards must move with it

---

### Step 76: Added debug state, ambiguity signals, and ambiguity-aware graph branching
Completed:
- Added explicit graph-state fields for:
  - `raw_result_count`
  - `filtered_result_count`
  - `is_ambiguous`
- Updated `app/test_graph.py` to print raw and filtered counts and top titles
- Verified supported questions could have:
  - noisy raw results
  - filtered relevant results
  - ambiguity marked in state
- Added an ambiguity-aware branch so the graph could respond differently when multiple relevant results survived filtering

Why it mattered:
- This made the graph easier to debug and understand
- It taught how graph state can carry derived quality/debug signals
- It introduced routing based on retrieval quality, not just empty vs non-empty context

What I learned:
- State can hold both business data and debugging signals
- Ambiguity is a useful first-class workflow concept
- Conditional routing can depend on retrieval quality signals, not just existence of context

---

### Step 77: Added final response assembly and separated ambiguity post-processing
Completed:
- Refactored the graph so ambiguity handling became its own node:
  - `annotate_ambiguous_answer`
- Added:
  - `prepare_final_response`
  as a dedicated final formatting node
- Changed branch nodes to produce intermediate response payload data instead of fully formatted API responses
- Verified the final API response shape still worked correctly
- Verified LangSmith traces showed the graph-backed flow and branching behavior

Why it mattered:
- This created a cleaner LangGraph design
- It taught the difference between:
  - generating intermediate response data
  - formatting final output
- It made the graph more modular and easier to reason about

What I learned:
- A good graph separates decision logic, post-processing, and final formatting
- Post-processing nodes are useful for controlled response adjustments
- Final response assembly is cleaner when handled in one dedicated node

---

### Step 78: Created the Azure AI Foundry resource and connected from Python
Completed:
- Created an Azure AI Foundry resource in the portal
- Created and configured:
  - `AZURE_AI_PROJECT_ENDPOINT`
  in `.env`
- Installed the required auth and project SDK packages in the correct virtual environment:
  - `azure-identity`
  - `azure-ai-projects>=2.0.0`
- Created:
  - `foundry/test_foundry_connection.py`
- Verified `AIProjectClient` could connect successfully to the Foundry project endpoint

Why it mattered:
- This was the real start of Foundry integration
- It proved the project could authenticate and connect to the Foundry project from Python
- It established the foundation required for model deployment, agent creation, and later integration work

What I learned:
- Foundry integration depends on the correct project endpoint and Azure auth
- Package installs must happen in the same active virtual environment used by the scripts
- Connection testing should come before any agent creation logic

---

### Step 79: Deployed a model in Foundry and created the first agent version
Completed:
- Deployed:
  - `gpt-4o-mini-2`
  using Global Standard deployment
- Added:
  - `AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini-2`
  to `.env`
- Created:
  - `foundry/create_agent.py`
- Adjusted the code to match the current Foundry SDK:
  - used `create_version(...)`
  - used `PromptAgentDefinition`
- Successfully created:
  - `support-copilot-agent:1`

Why it mattered:
- Agents require a deployed model before they can be created
- This moved Foundry from project connection into real agent-service use
- It proved that the current SDK-based agent creation flow worked

What I learned:
- The newer Foundry SDK uses `create_version(...)` instead of the older `create_agent(...)`
- Agent creation now requires a definition object
- SDK method names can change, so direct testing is important

---

### Step 80: Generated the first Foundry agent responses and learned the difference between generic and system-specific behavior
Completed:
- Created:
  - `foundry/test_agent_response.py`
- Successfully created conversations and generated responses through the Foundry agent
- Tested support-style prompts such as:
  - `How do I log in?`
  - `Why was I charged twice?`
- Improved output printing so only the assistant reply text was shown

Why it mattered:
- This proved the Foundry agent could answer successfully
- It also showed an important limitation:
  - the Foundry agent was responding like a general instructed model
  - it was not yet using the real Azure Search + LangGraph support flow

What I learned:
- An agent can work technically while still being generic behaviorally
- Model instructions alone do not equal integration with the real product logic
- Testing with actual support questions reveals whether the agent is really aligned to the system

---

### Step 81: Built a Foundry-side bridge into the real support-copilot API
Completed:
- Created:
  - `foundry/test_local_support_api.py`
  - `foundry/test_foundry_bridge.py`
  - `foundry/support_bridge.py`
  - `foundry/test_foundry_agent_via_bridge.py`
  - `foundry/run_support_agent.py`
- Verified that calling the local FastAPI `/ask` endpoint returned the real support-copilot answers
- Refactored the bridge into a reusable helper:
  - `ask_support_api(...)`
- Verified multiple support questions could be answered through the bridge using the real system output

Why it mattered:
- This established the correct mental model for Foundry integration:
  - Foundry should sit in front of the real support system
  - it should not replace the actual support logic with generic model behavior
- It created a practical reusable path for Foundry-side code to call the real support API

What I learned:
- The bridge is the key integration pattern for this project stage
- The real product-specific value comes from Azure Search + LangGraph + answer shaping
- Foundry is most useful when connected to the real support workflow, not used in isolation

---

### Step 82: Confirmed the practical Foundry integration foundation is complete
Completed:
- Verified the reusable Foundry-side wrapper:
  - `run_support_agent(...)`
  returned:
  - answer
  - next steps
  - confidence
  - primary source
- Confirmed the bridge approach worked for multiple support questions
- Reached a stable learning milestone where:
  - Foundry connection worked
  - agent creation worked
  - agent response generation worked
  - bridge-to-real-system flow worked

Why it mattered:
- This completed the practical Foundry integration foundation for the learning project
- It connected the Foundry phase back to the actual support-copilot architecture
- It provided a strong base for later production hardening or deeper Foundry/tool integration

What I learned:
- Foundry integration is strongest when it complements the existing support system
- A clean wrapper around the bridge is useful for reuse across tests and future integration paths
- The combination of FastAPI, Azure Search, LangGraph, LangSmith, and Foundry now forms a coherent learning architecture

---

## Updated project structure

```text
enterprise-support-copilot/
  app/
    __init__.py
    api.py
    answering.py
    config.py
    graph.py
    models.py
    search.py
    services.py
    test_graph.py
  data/
    login-account-access-support.txt
    billing-support.txt
    invitations-permissions-support.txt
    notifications-email-delivery-support.txt
    performance-slow-loading-support.txt
    billing-faq.txt
    login-faq.txt
    invitations-permissions-faq.txt
    notifications-email-faq.txt
    performance-faq.txt
  docs/
    ingestion_plan.md
  eval/
    __init__.py
    manual_questions.json
    load_manual_questions.py
    run_manual_eval.py
    create_langsmith_dataset.py
    prepare_langsmith_dataset.py
    run_langsmith_eval.py
    langsmith_target.py
    langsmith_evaluators.py
    manual_eval_results_latest.json
    manual_eval_results_<timestamp>.json
  foundry/
    __init__.py
    create_agent.py
    run_support_agent.py
    support_bridge.py
    test_agent_response.py
    test_foundry_agent_via_bridge.py
    test_foundry_bridge.py
    test_foundry_connection.py
    test_local_support_api.py
  ingestion/
  .env
  .env.example
  .gitignore
  requirements.txt