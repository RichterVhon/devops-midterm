
# 🖼 Image Processing Project: Workflow & Team Standards

This document outlines the mandatory procedure for all code changes. To ensure project stability, **direct pushes to `main` are blocked.** All members must follow this "Gatekeeper" workflow.

---

## 🏗 The Global Issue Lifecycle (Todo ⮕ Done)

Every task must follow this progression on the Project Board. **Do not skip columns.**

* **Todo**: Issues are either assigned to you or created by you (see creating an issue section below).
* **In Progress**: Move your card here when you start coding on a Branch.
* **Review (PR Opened)**: Move your card here once you open a Pull Request (PR).
* **Testing/QA**: The Tester moves the card here to validate the filters/logic locally.
* **Done**: The PR is merged, the pipeline is green, and the Issue is closed.

---

## 🌿 Branch Naming Standards

Before coding, create a branch using this specific format: `type/short-description-issue#`

| Type | Description | Example |
| --- | --- | --- |
| `feat/` | New filters or processing logic | `feat/grayscale-7` |
| `fix/` | Bug fixes | `fix/memory-leak-12` |
| `docs/` | Documentation only | `docs/workflow-update-3` |

> **Example Command:** `git checkout -b feat/sobel-edge-15`

---


## 💬 Commit Message Standards

Keep history clean using the format: `[Action]: [Description]`

> **Example**: `git commit -m "Filter: Add brightness adjustment logic"`

*Note: The `Closes #X` tag must be placed in the **Pull Request description**, not the commit message, to ensure board automation.*

--

## 🚩 Creating a New Issue


1. The Navigation Path
Navigate to our Repository page on GitHub.

Click the Issues tab (located between "Code" and "Pull requests").

Click the green New Issue button.

2. Filling the Metadata (The "Pro" Step)
Before you hit "Submit," look at the right-hand sidebar. This is where the magic happens for your Roadmap:

Assignees: Click "assign yourself" or select the teammate responsible.

Labels: Choose the appropriate category (e.g., feature, documentation, bug).

Projects: Select your Project Board. This puts the issue on your Kanban Board.

Milestone: Select the Active Milestone (e.g., Milestone 1: Setup). This is what puts the issue on your Visual Roadmap.



---

## 👥 Role-Specific Procedures

### 💻 Lead Developer (Feature Creator)

1. **Sync**: `git checkout main` && `git pull origin main`.
2. **Branch**: Create a branch using the naming standard.
3. **Code**: Implement your image processing logic.
4. **Push**: `git push origin [your-branch-name]`.
5. **Pull Request (PR)**: Open a PR to `main`.
* **Mandatory**: In the PR description, write `Closes #X` (where X is the issue number).
* **Link**: In the PR sidebar, select our Project Board under **Projects**.
* **Reviewer**: Assign the **Tester** as the reviewer.


6. **Handoff**: Drag the Issue and PR cards to **Review**.

### 🧪 Tester (The Gatekeeper)

*You are the final authority for the `main` branch.*

1. **Handoff**: Drag the cards from **Review** to **Testing/QA**.
2. **Local Test**: Fetch the branch and run it locally:
```bash
git fetch origin && git checkout [dev-branch-name]
python processor.py

```


3. **Proof**: Attach a screenshot of the processed image from the `/output` folder to the PR comments.
4. **Verification**: Confirm the GitHub Actions Pipeline (DevOps) is **Green**.
5. **Merge**: Click **Merge Pull Request**. This will automatically move the task to **Done**.

---

## 📝 Documenter Instruction

Maintain the project's public "Dashboard" via the `README.md`. Ensure technical work is translated into a professional record.

* **Feature Traceability Matrix**: Update the README table immediately after any PR is merged.
* *Source*: Feature ID/Title from Issue, Status from Board, and Link from PR URL.


* **Key Feature Documentation**: Maintain a high-level list of current software capabilities.
* *Source*: "Labels" on the Project Board and Feature Descriptions in merged Issues.


* **Visual Archive Management**: Retrieve "Proof of Work" screenshots from Tester's PR comments. Save in `/docs/assets/` and embed in the README Visual Gallery.
* **Version History (Changelog)**: Maintain a chronological list of merges.
* *Source*: `main` branch commit history or the Closed PR list.


---

## 💡 The "Definition of Done" (DoD)

An Issue is only considered **Done** when:

1. **Passed Pipeline**: The GitHub Actions build is **Green**.
2. **Peer Verified**: The Tester has approved and merged the Pull Request.
3. **Proof of Work**: A Success Screenshot is attached to the PR comments.
