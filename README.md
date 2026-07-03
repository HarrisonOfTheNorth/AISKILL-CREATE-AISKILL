# CREATE-AISKILL.aiskill

This is the skill that creates skills. Every AI Skill Package that exists — or will exist — can trace its origin to this one. Each one lives as a single file with a `.aiskill` extension — a ZIP archive at its core, small enough to share in a message, complete enough to stand alone. Before diving into what it does, it's worth taking a moment to understand the world it belongs to, because that context is what makes this particular package so significant.

---

## The AI Skill Universe

Most people are already familiar with the idea of giving an AI agent a set of instructions — a prompt that tells it what to do and how to behave. When someone refines a prompt they find themselves using repeatedly — saves it to a text file or a notebook so they can reach for it again whenever that same task comes up — that saved, reusable piece of text is called an **AI skill**. It is just text. Nothing more. But it is text that has been thought through, kept, and given a purpose.

An **AI Skill Package** is something different.

Where a simple AI skill is just text — a prompt saved to a file and pasted in whenever that task is needed — an AI Skill Package is a structured, versioned, unit-tested artifact that has been built, verified, and packaged in advance. It contains not just instructions, but scripts, templates, tests, and a manifest that identifies exactly what it is and what version it is. It has been checked, and it checks itself.

The key insight is this: **the AI becomes the executor, not the author.**

When an agent receives an AI Skill Package, the thinking has already been done. The procedure has already been written, tested, and verified by whoever built the package. The agent's job is simply to open it, read the entry point, follow the steps, and ask the user for anything it still needs. The output is deterministic — the same inputs produce the same result, every time, regardless of which agent runs it or when.

This is what separates an AI Skill Package from a prompt: reliability, repeatability, and trust.

---

## How People Use AI Skill Packages

You don't need to be a developer to use an AI Skill Package. You don't need to know what a manifest is, or what a unit test does, or how a ZIP archive is structured.

What you need is an idea — and a way to express it.

You open your AI agent (Claude Code, or any compatible runtime), and you say something like:

> _"Use the skill at /path/to/skill-name.aiskill to do this for me."_

You can type that, or you can press record and say it out loud. The agent reads the package, figures out what it needs to know, and asks you questions until it has enough to proceed. If your initial prompt already answered those questions, it gets straight to work.

No commands. No configuration files. No prior knowledge required.

---

## This Skill in Particular

CREATE-AISKILL is the origin point. It is the one AI Skill Package that was not itself created by an AI Skill Package — and from which every other AI Skill Package can be made.

When you run CREATE-AISKILL, the agent asks you about the skill you want to build: what it should do, who it's for, what kind of output it produces. You answer in plain language. The agent does the rest — creating the complete package structure, setting up version control, and leaving you with everything in place to start describing your skill's procedure.

The result is your own AI Skill Package: structured, versioned, and ready to run. Something you can keep for personal use, share with a team, or publish publicly so that others can download, inspect, and trust it.

If you have an idea for something an AI agent should be able to do repeatedly and reliably — this is where that idea becomes a package.

---

> ### AI Independence Day — 4 July 2026
>
> CREATE-AISKILL was first published on 4 July 2026, the date we mark as **AI Independence Day** — the day a normative open standard first formalised, for the history of AI, the separation of computation from generation.
>
> Until this point, when you asked an AI agent to perform a complex task, it authored the solution in the moment: reasoning its way through, generating steps it had never verified, producing output that could differ each time. An AI Skill Package changes that contract entirely. The procedure has been written in advance. It has been tested. It has been packaged and signed. When the agent runs it, it is not authoring anything — it is executing work that already exists, against inputs you provide, toward an outcome that has already been verified to be achievable.
>
> The computation is independent of the generation. The agent is the executor, not the author.
>
> CREATE-AISKILL is the package that made every other package possible. It is the origin of that independence. Released on the 4th of July, not by coincidence.

---

## Prerequisites

If you are new to AI Skill Packages, you can ignore this section entirely. The AI agent will identify anything it needs and ask your permission before installing it. The list below is for developers who prefer to know what's on the engine before they turn the key.

- Python 3.8+
- git
- gh CLI (optional — only needed to publish a GitHub release)

---

## Quick Start

Give your AI agent this prompt — nothing more is needed to begin:

> _Run the Skill Package at /path/to/CREATE-AISKILL-1.0.0.aiskill_

That is the complete minimal prompt. The agent opens the package, reads its entry point, and starts a conversation with you to gather what it needs. It will typically ask:

- What do you want to call your skill?
- What should it do — describe it in your own words
- Who is it for, and what will they give it as input?
- Do you want to connect it to a GitHub repository so others can find and trust it? (You can say no — a local-only skill works just as well)
- Your name and contact email, so the package can be properly attributed

You can answer in any order and in any amount of detail. If your opening prompt already covered some of these, the agent skips straight past them. If you'd rather talk than type, press record and describe your idea out loud — the agent will work with whatever it receives.

**A fuller prompt — for illustration:**

> _Run the Skill Package at /path/to/CREATE-AISKILL-1.0.0.aiskill — I want to create a skill that helps a home cook plan a week of dinners based on what's in season and any dietary restrictions in the household._

With a prompt like that, the agent already knows the name, the purpose, and the audience. It may only need to ask one or two follow-up questions before it gets to work.

---

## Under the Bonnet

Think of buying a car. You want to sit in it, feel comfortable, and go touring. How much you need to know about the engine is entirely up to you — most drivers never lift the bonnet, and they never need to. This section is the bonnet. Read on if you're curious; skip ahead to the specification link if you're not.

When CREATE-AISKILL finishes, it has produced a directory containing everything a skill package needs:

- A **manifest** — the identity card: name, version, unique ID, author, licence
- A **SKILL.md** — the entry point the AI agent reads first; this is where the procedure lives
- **Scripts** — executable files (Python, or whatever language fits the task) that do the actual work
- **Templates** — reusable file skeletons the scripts can stamp out
- **Tests** — unit tests that verify the scripts behave correctly before the package is shipped
- **Checksums** — a record of every file's fingerprint, so anyone can verify the package hasn't been tampered with
- **A schema** — a formal definition of what inputs the skill accepts
- **A changelog and README** — so humans know what it does and what has changed

Once all of those are in place, turning that folder into an AI Skill Package takes exactly two steps: zip it up, and rename the file extension from `.zip` to `.aiskill`. That is all the format is — a ZIP with a name that says what it contains.

When an agent receives an `.aiskill` file, it reverses that process: unpacks the archive into a temporary working area, opens `SKILL.md`, and follows the instructions inside like a flowchart. Each branch either continues the task or returns to the user with a question. Eventually every branch leads to the same place — the completed output the skill was built to produce.

---

## On Public Distribution

For personal or internal use, a local-only skill works just as well — no GitHub account, no repository, no configuration. The skill lives on your machine and runs when you point an agent at it.

If you intend to share your skill publicly, a public repository is strongly recommended — not for convenience, but for trust. When users can read the source, they can verify the package does what it says and nothing it shouldn't. The open `.aiskill` format exists precisely so that inspection is always possible.

---

## Specification

The full Open AI Skill Package specification is at [openaiskillpackage.com](https://openaiskillpackage.com/).

---

## License

MIT

**Author:** Anthony Harrison — widgets@penrithbeacon.com
