# Agentic AI


## Foundations: APIs and the Client-Server Model


At a basic level an API is a programmatic interface to functions
or services, implying a Server and a Client. The Client initiates
contact (often at the behest of a User with some intention) and the Server
responds. By far the most common API implementation is as a stateless 
(jargon: 'RESTful') interface, meaning the Server retains no memory 
from one interaction to another. This places the onus of 'advancing
the conversation' on the Client (if necessary). I refer to data
sent and received by the Client on API calls as message payloads.


## The Agentic AI Construction


In the use of Agentic AI we have a construction similar to the API. Presuming a User (human) driving the conversation we can imagine an Agentic AI as three components:

- **Harness (Agent):** Orchestrating software that mediates between the User
  and the Model. Referred to as the *harness*, *agent*, *orchestrator*, or *runtime*. The analog of an API Client.
- **Connection / Authentication:** The machinery that connects the harness to one or more Models. This connection incorporates authentication: Credentials, API keys, service accounts etcetera.
- **Model:** Typically one or more language models (LLMs) that the Harness calls upon for reasoning. A Model provides a stateless service: it receives a message payload, generates and sends back a response payload, and retains no memory of the transaction.


In brief, then: **User : Harness — Connection — Model**. What is of interest are some further details of this process. First the Model receives a data payload from the harness and generates a response that often includes human-readable language. But this is not generated in the way a human composes a paragraph.


The model produces one token at a time,
each conditioned on everything that precedes it: the entire payload plus all
tokens already generated in the current response. There is no planning, drafting,
or backtracking. The output is an autoregressive chain — each token is the
model's best prediction of what should come next given everything so far. This
matters because it explains certain failure modes (rambling, losing coherence on
long outputs) and why structured output formats like JSON tool calls are
impressive: the model must maintain syntactic validity token by token without
the ability to revise earlier tokens. We call the completed token sequence the
**return payload**.


## Anatomy of the Payload

The payload that the harness sends to the model on each API call is not a single
blob of text. It has at least **6 distinct components**, assembled by the harness
into a structured message. These components form the framework of the
relationship between User, Harness/Agent, and Model:

| # | Component | Source | Purpose |
|---|-----------|--------|---------|
| 1 | **System prompt** | Harness (static or semi-static) | Identity, behavioral rules, safety guardrails, response style. Tells the model *what it is* and how to behave. |
| 2 | **Tool definitions** | Harness (static per session) | A schema describing every tool the model may invoke (read file, write file, run command, search, etc.). The model cannot act on the world without these. |
| 3 | **Steering / context rules** | Harness (from workspace config) | Project-specific instructions, conventions, and constraints injected from steering files. |
| 4 | **Conversation history** | Harness (grows each turn) | The full sequence of prior user messages, assistant responses, tool calls, and tool results accumulated during the session. This is what gives the stateless model the *illusion* of memory. |
| 5 | **Current user message** | User (via harness) | The latest request or follow-up from the user. |
| 6 | **Attached context** | Harness (on demand) | File contents, diagnostics, search results, or other material the harness injects to give the model visibility into the current state of the workspace. |

The key insight is that component 4 (conversation history) grows monotonically
throughout a session — every exchange adds to it. This is what makes the payload
progressively larger and eventually runs into the model's context window limit.
The harness manages this growth: summarizing, compacting, or dropping older
context when the window fills.

Components 1–3 are relatively stable across a session. Component 5 is fresh each
turn. Component 6 is situational — the harness decides what's relevant based on
the user's request and the tools being invoked. The entire assembly is sent as
one atomic API call; the model sees it all at once with no structural distinction
between "old" and "new" — it's all just tokens in a sequence.


## The Context Window and Session Lifetime

In a User-driven project the pattern is prompt, reply, prompt, reply — a
conversation that accumulates context as work progresses. The limiting factor
on this process is the **context window**: a system-dependent maximum volume
(measured in tokens) that defines how large a payload the model can accept and
reason over in a single call.

Because the conversation history (component 4) grows monotonically — every
exchange adds user messages, model responses, tool calls, and tool results —
the payload assembled by the harness gets larger with every turn. Eventually it
approaches or exceeds the context window. At that point the session becomes
unreliable: the model may lose coherence, drop earlier context, or refuse to
respond. The session is generally abandoned in favor of starting fresh.

The important misconception to dispel: **the model does not "wear out."** It is
stateless, just like a RESTful API. It has no memory of previous calls. It does
not grow tired or confused from a long conversation. What happens is purely
mechanical — the harness is assembling increasingly large payloads (because each
one must include the full conversation history), and eventually that payload
exceeds what the model can process in one shot. The model on turn 50 is exactly
as capable as it was on turn 1; it simply cannot see all of turns 1–49 anymore
because they no longer fit.

Sophisticated harnesses mitigate this with **compaction strategies**: summarizing
older exchanges, dropping tool-result details that are no longer relevant, or
splitting work across sub-agents with fresh context windows. But the fundamental
constraint remains — a single model call can only reason over what fits in its
context window.


## Tools, Skills, and the Session Loop

### Tools

A **tool** is a capability of the Harness/Agent — the ability to take some action
in the real world. Compare this to the Model, which is essentially building a
string (an albeit complex one, token by token). The Model cannot read a file,
cannot run a program, cannot search the internet. It can only produce text. A
tool bridges that gap.

The typical example: the ability to run a `bash` script on the Client computer.
Other tools include reading a file, writing a file, searching the codebase by
regex, or fetching a web page. The list of available tools is delivered to the
Model in component 2 from the table above (tool definitions). We say the harness
*provides* a list of tools and the model *invokes* a tool as appropriate.

This raises an interesting question: how does a Model arrive at a decision to
"just send back some text" versus "invoke a tool"? The latter does not sound like
an autoregressive chain — it sounds like a logical decision.

The answer: it *is* still autoregressive. The model has been trained (via
reinforcement learning from human feedback and specialized fine-tuning) to
recognize situations where tool use is appropriate and to emit a specific
structured format — a tool-call block — as its next tokens. From the model's
perspective, generating `{"tool": "execute_bash", "command": "ls -la"}` is no
different mechanically from generating a paragraph of English. It's all token
prediction. But the *training* has taught the model that when the user asks
"what files are here?" and a filesystem tool is available, the highest-probability
next tokens form a tool invocation rather than a guess. The model doesn't
"decide" in a deliberative sense; it has learned statistical patterns that
produce tool calls in the right contexts.

The harness then intercepts this structured output, recognizes it as a tool
invocation (not prose for the user), executes the requested action, and appends
the result to the conversation history before calling the model again.

### Skills

A **skill** is a higher-level concept: a reusable bundle of instructions that
tells the model *how* to approach a particular kind of task. Where a tool is a
single action ("run this command"), a skill is a strategy or procedure composed
of multiple steps.

Example: "When the user asks you to add a new Python dependency, do the
following: (1) add it to requirements.txt with a pinned version, (2) run
`pip install -r requirements.txt`, (3) offer to clear the pip cache." That's a
skill — it combines knowledge of project conventions with a sequence of tool
invocations and user interactions. Skills are typically delivered to the model
via steering files (component 3) or as part of the system prompt (component 1).

The distinction: tools are atomic capabilities the harness *provides*; skills
are composite behaviors the model *exhibits* because it has been instructed how
to behave in certain situations.

### The Session Loop

With tools and skills in place, a session proceeds as a back-and-forth loop
between Harness and Model:

1. **Harness assembles the payload** — all 6 components, including the
   conversation history so far — and sends it to the Model.
2. **Model generates a response.** This might be:
   - Plain text (an answer to the user), or
   - A tool invocation (a structured request to take an action).
3. **If tool invocation:** The harness executes the tool, captures the result,
   appends both the tool call and its result to the conversation history, and
   loops back to step 1 — sending a new, larger payload.
4. **If plain text:** The harness presents it to the user. The user may respond
   (adding another turn), or the task is complete.

This loop repeats as many times as necessary — sometimes dozens of tool calls
for a complex task — until some halting criterion is met. The halting criterion
is typically: the model produces a final text response addressed to the user
(rather than another tool call), indicating it considers the task resolved. The
harness may also impose limits: maximum turns, maximum token expenditure, or
timeout.

From the outside this looks like intelligence and agency. From the inside it is:
a stateless prediction engine being called repeatedly, with the harness
maintaining all state, executing all actions, and deciding when to stop.
