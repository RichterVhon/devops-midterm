# [Project Title: Automated Image Processing Pipeline]

> **Requirement Proof:** Python 3 | OpenCV | GitHub Actions | PyTest | Docker

## 📝 Project Overview

This project is an automated batch image processing system. It is designed to monitor an input directory, detect image files, apply complex transformations using **OpenCV**, and save the results to a structured output directory.

## 🚦 Status & Traceability Matrix (System Requirements)

> **Documenter Source:** *Project Board "Done" Column + Merged Pull Requests.*

| ID | System Requirement | Status | Verification (Link) |
| --- | --- | --- | --- |
| **REQ-01** | Auto-detect images in input directory | ✅ DONE | [Link to PR #] |
| **REQ-02** | Apply 2+ OpenCV techniques | ✅ DONE | [Link to PR #] |
| **REQ-03** | Save to output directory | ✅ DONE | [Link to PR #] |
| **REQ-04** | GitHub Actions Pipeline (Run on Push) | ✅ DONE | [Link to PR #] |

---

## ✨ Key Features

* **Automated Detection**: Script scans for supported image formats (JPG, PNG) in `/input`.
* **OpenCV Suite**: High-performance transformations including Grayscale and Edge Detection.
* **Validation Layer**: Integrated **PyTest** suite for logic verification.
* **Infrastructure as Code**: **Docker** support for platform-independent execution.
* insert more if may madagdag

---

## 🚀 Getting Started

### 👤 For Users (Quick Run)

1. **Install Docker Desktop.**
2. **Run via Command Terminal:**
```bash
docker run -v "%cd%":/app/data [image-name]

```


*This maps your current directory to the container to see results locally.*

### 💻 For Developers (Setup Environment)

1. **Clone the Repository:** `git clone [url]`
2. **Install Dependencies:** `pip install opencv-python pytest`
3. **Run Local Tests:** Execute `pytest` to verify the logic before pushing.

---

## 🛠 Technical Architecture & Logic

> **Documenter Source:** *Lead Developer's code comments and OpenCV documentation.*

### ⚙️ DevOps Workflow (CI/CD)

The project utilizes **Continuous Integration (CI)** through **GitHub Actions**.

* **Trigger**: The pipeline automatically fires on every GitHub **Push**.
* **Process**: The pipeline builds the environment, installs dependencies, and runs the **PyTest** suite.
* **Gatekeeping**: If tests fail, the merge is blocked to protect the `main` branch.

### 🧩 Image Processing Logic

The core engine utilizes **OpenCV (cv2)** following this logic:

1. **Ingestion**: Scans the input directory for valid file signatures.
2. **Transformation**:
* **Grayscale**: Converts BGR to single-channel luminosity.
* **Edge Detection**: Uses the **Sobel Operator** to calculate intensity gradients, identifying object boundaries.


3. **Export**: Saves the processed array to the `/output` folder with timestamped filenames.

---

## 📸 Visual Gallery & File Proof

> **Documenter Source:** *Tester's PR screenshots.*

### End-Product Results

* **Grayscale Transformation**: `![Grayscale_Final_REQ-02](path/to/image)`
* **Edge Detection**: `![Edge_Final_REQ-02](path/to/image)`

### File System Proof

* **Directory Verification**: `![Folder_Structure_REQ-03](path/to/screenshot)`
*(Note: Include screenshots proving the automatic creation of files inside the `/output` folder).*

---

## 📈 Process Evolution (Workflow & Documentation)

We implemented advanced **Industry Workflows** to ensure project quality:

* **Continuous Documentation Strategy**: The Documenter manually syncs this **Traceability Matrix** with the Project Board after every merge to eliminate "documentation debt."
* **Gatekeeper Protocol**: Enforced a "No Direct Push" policy; all code requires **Tester** validation and **DevOps** automated approval.
* **CI Efficiency**: Integrated **GitHub Actions** to automate environment setup and testing on every push.

---

## 🧪 Quality Assurance (Automated Testing)

> **Documenter Source:** *PyTest terminal logs and Actions history.*

The system ensures reliability through **PyTest**. Automated tests verify:

* **Detection**: Correct identification of image files in the input folder.
* **Integrity**: Dimensional consistency between original and processed images.
* **I/O Success**: Verified permission to write processed files to the output directory.

---

## 📜 Version History (Changelog)

* **[Date]**: Implemented REQ-04 (GitHub Actions & PyTest integration).
* **[Date]**: Integrated OpenCV processing techniques.
* **[Date]**: Initial environment and Docker setup.

---

## 👥 The Team

* **Lead Developer**: Algorithm & OpenCV logic.
* **Tester**: Manual validation & PR Gatekeeping.
* **DevOps**: Pipeline, Docker, & GitHub Actions.
* **Documenter**: Traceability, README, & Visual Gallery.
