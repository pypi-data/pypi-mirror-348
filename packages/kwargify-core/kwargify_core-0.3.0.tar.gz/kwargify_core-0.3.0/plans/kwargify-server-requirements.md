# Kwargify Server: Project Requirements Document

**Version:** 1.0
**Date:** May 18, 2025

## 1. Introduction

### 1.1. Project Goal

The primary goal of the `kwargify-server` project is to develop a web application that provides a user-friendly graphical interface for all functionalities currently available in the `kwargify-core` Python library. This server will allow users to manage, run, validate, and monitor Kwargify workflows without needing to use the command-line interface.

### 1.2. Target User

This application is intended for users of `kwargify-core` who prefer a visual interface for their workflow management tasks, or for teams where a centralized web UI can streamline workflow operations.

### 1.3. Core Technologies

- **Backend:**
  - Programming Language: Python (latest stable version)
  - Framework: FastAPI
  - Core Logic: `kwargify-core` (imported as a Python package)
  - ASGI Server: Uvicorn (or similar)
  - Package Management: `uv`
- **Frontend:**
  - Programming Language: TypeScript
  - Framework/Library: React
  - Build Tool: Vite
  - UI Component Library: DaisyUI
  - CSS Framework: TailwindCSS
  - State Management: Jotai
- **Database:**
  - The `kwargify-core` library uses SQLite for its registry and logging. The `kwargify-server` backend will interact with `kwargify-core` services, which in turn manage their own database persistence. No separate database is planned for `kwargify-server` itself at this stage, unless specifically for server-side session management if authentication is added later.

### 1.4. Repository Structure (New `kwargify-server` Repository)

The project will be housed in a new Git repository with the following structure:

```
kwargify-server/
├── backend/                # FastAPI application
│   ├── app/                # Main application code
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI app instantiation
│   │   ├── routers/        # API endpoint definitions
│   │   │   ├── __init__.py
│   │   │   ├── project.py
│   │   │   ├── workflows.py
│   │   │   └── history.py
│   │   ├── services/       # Business logic interacting with kwargify-core
│   │   │   └── __init__.py
│   │   ├── models/         # Pydantic models for API requests/responses
│   │   │   └── __init__.py
│   │   └── core/           # Core configuration, dependencies
│   │       └── __init__.py
│   ├── tests/              # Backend tests
│   ├── .env.example        # Example environment variables
│   ├── pyproject.toml      # Backend dependencies (for uv)
│   └── README.md           # Backend specific README
├── frontend/               # React/Vite application
│   ├── public/             # Static assets
│   ├── src/                # Frontend source code
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Top-level page components
│   │   ├── services/       # API client services
│   │   ├── store/          # Jotai state atoms
│   │   ├── styles/         # Global styles, Tailwind config
│   │   └── types/          # TypeScript type definitions
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── README.md           # Frontend specific README
├── .gitignore              # Git ignore rules for the whole project
└── README.md               # Main project README
```

## 2. Backend API Design (FastAPI)

The backend will expose a RESTful API. All interactions with `kwargify-core` will be done through its service layer (`kwargify_core.services`).

### 2.1. General API Conventions

- Base URL: `/api/v1`
- Responses: JSON format.
- Error Handling:
  - Use standard HTTP status codes (e.g., 200 OK, 201 Created, 400 Bad Request, 404 Not Found, 500 Internal Server Error).
  - Error responses should include a `detail` field with a human-readable error message.
  - Errors from `kwargify_core.services` (e.g., `ProjectInitError`, `WorkflowRunError`) should be caught and mapped to appropriate HTTP exceptions (e.g., `HTTPException` from FastAPI).
- Data Validation: Pydantic models will be used for request and response validation.

### 2.2. API Endpoints

#### 2.2.1. Project Management (`/project`)

- **`POST /project/init`**: Initialize Kwargify Project
  - **Request Body**:
    ```json
    {
      "project_name": "string",
      "db_name": "string"
    }
    ```
  - **Response (200 OK)**:
    ```json
    {
      "message": "string" // e.g., "Project 'MyProject' initialized."
    }
    ```
  - **Calls**: `kwargify_core.services.init_project_service()`
  - **Error Responses**: 400 if input is invalid, 500 if initialization fails.

#### 2.2.2. Workflow Operations (`/workflows`)

- **`POST /workflows/run/file`**: Run Workflow from File

  - **Request Body (multipart/form-data)**:
    - `workflow_file`: Uploaded Python file (`UploadFile`)
    - `resume_id` (optional, string)
    - `resume_after_block_name` (optional, string)
  - **Response (200 OK)**:
    ```json
    {
      "run_id": "string",
      "workflow_name": "string",
      "status": "string", // e.g., "COMPLETED"
      "message": "string"
    }
    ```
  - **Calls**: `kwargify_core.services.run_workflow_file_service()`
  - **Error Responses**: 400, 404 (file not found by core), 500.

- **`POST /workflows/run/registered`**: Run Registered Workflow

  - **Request Body**:
    ```json
    {
      "name": "string",
      "version": "integer | null",
      "resume_id": "string | null",
      "resume_after_block_name": "string | null"
    }
    ```
  - **Response (200 OK)**: (Same as "Run Workflow from File")
  - **Calls**: `kwargify_core.services.run_registered_workflow_service()`
  - **Error Responses**: 400, 404 (workflow/version not found), 500.

- **`POST /workflows/validate/file`**: Validate Workflow from File

  - **Request Body (multipart/form-data)**:
    - `workflow_file`: Uploaded Python file (`UploadFile`)
  - **Response (200 OK)**:
    ```json
    {
      "is_valid": "boolean",
      "name": "string | null",
      "blocks_count": "integer | null",
      "dependency_flow": "string | null",
      "mermaid_diagram": "string | null",
      "errors": "array[string] | null"
    }
    ```
  - **Calls**: `kwargify_core.services.validate_workflow_service()`
  - **Error Responses**: 400, 500.

- **`POST /workflows/show/file`**: Show Workflow Details from File

  - **Request Body (multipart/form-data)**:
    - `workflow_file`: Uploaded Python file (`UploadFile`)
    - `diagram_only` (optional, boolean, default: false)
  - **Response (200 OK)**:
    - If `diagram_only` is true: `{"mermaid_diagram": "string"}`
    - Else:
      ```json
      {
        "name": "string",
        "total_blocks": "integer",
        "execution_order": "array[object]", // { order, name, dependencies }
        "block_details": "array[object]", // { name, config, input_map }
        "mermaid_diagram": "string"
      }
      ```
  - **Calls**: `kwargify_core.services.show_workflow_service()`
  - **Error Responses**: 400, 500.

- **`POST /workflows/register/file`**: Register Workflow from File

  - **Request Body (multipart/form-data)**:
    - `workflow_file`: Uploaded Python file (`UploadFile`)
    - `description` (optional, string)
  - **Response (200 OK / 201 Created)**: (Structure from `registry.register()`)
    ```json
    {
      // Example:
      "id": "integer",
      "workflow_id": "integer",
      "name": "string",
      "version": "integer",
      "description": "string | null",
      "source_path": "string",
      "registered_at": "string" // ISO datetime
    }
    ```
  - **Calls**: `kwargify_core.services.register_workflow_service()`
  - **Error Responses**: 400, 500.

- **`GET /workflows`**: List All Registered Workflows

  - **Response (200 OK)**: `array[object]` (Structure from `registry.list_workflows()`)
    ```json
    [
      // Example:
      {
        "id": "integer",
        "name": "string",
        "latest_version": "integer",
        "description": "string | null",
        "created_at": "string", // ISO datetime
        "updated_at": "string" // ISO datetime
      }
    ]
    ```
  - **Calls**: `kwargify_core.services.list_workflows_service()`
  - **Error Responses**: 500.

- **`GET /workflows/{workflow_name}/versions`**: List Versions of a Workflow

  - **Path Parameter**: `workflow_name` (string)
  - **Response (200 OK)**: `array[object]` (Structure from `registry.list_versions()`)
    ```json
    [
      // Example:
      {
        "id": "integer", // version_id
        "version": "integer",
        "description": "string | null",
        "source_path": "string",
        "registered_at": "string" // ISO datetime
      }
    ]
    ```
  - **Calls**: `kwargify_core.services.list_workflow_versions_service()`
  - **Error Responses**: 404 (workflow not found), 500.

- **`GET /workflows/{workflow_name}/versions/details`**: Get Specific Workflow Version Details
  - **Path Parameter**: `workflow_name` (string)
  - **Query Parameter**: `version` (optional, integer, defaults to latest)
  - **Response (200 OK)**: (Structure from `registry.get_version_details()`)
    ```json
    {
      // Example:
      "id": "integer", // version_id
      "workflow_id": "integer",
      "name": "string",
      "version": "integer",
      "description": "string | null",
      "source_path": "string",
      "registered_at": "string" // ISO datetime
    }
    ```
  - **Calls**: `kwargify_core.services.get_workflow_version_details_service()`
  - **Error Responses**: 404 (workflow/version not found), 500.

#### 2.2.3. Run History (`/history`)

- **`GET /history/runs`**: List Recent Workflow Runs

  - **Response (200 OK)**: `array[object]` (Structure from `logger.list_runs()`)
    ```json
    [
      // Example:
      {
        "run_id": "string",
        "workflow_name": "string",
        "workflow_version_id": "integer | null",
        "start_time": "string", // ISO datetime
        "end_time": "string | null", // ISO datetime
        "status": "string", // e.g., "COMPLETED", "FAILED", "RUNNING"
        "triggered_by": "string | null" // e.g., "file_run", "registered_run"
      }
    ]
    ```
  - **Calls**: `kwargify_core.services.list_run_history_service()`
  - **Error Responses**: 500.

- **`GET /history/runs/{run_id}`**: Get Detailed Run Information
  - **Path Parameter**: `run_id` (string)
  - **Response (200 OK)**: (Structure from `logger.get_run_details()`)
    ```json
    {
      "run_id": "string",
      "workflow_name": "string",
      // ... all other details provided by the service
      "blocks": "array[object]" // { block_name, status, start_time, end_time, inputs, outputs, logs }
    }
    ```
  - **Calls**: `kwargify_core.services.get_run_details_service()`
  - **Error Responses**: 404 (run not found), 500.

### 2.3. Pydantic Models

Define Pydantic models in `backend/app/models/` for all request bodies and complex response structures to ensure type safety and automatic validation.

## 3. Frontend UI/UX Design

The frontend will be a Single Page Application (SPA) built with React, TypeScript, Vite, DaisyUI, and TailwindCSS. Jotai will be used for state management.

### 3.1. Overall Layout

- **Theme:** Use DaisyUI themes (e.g., a clean, professional theme like "light", "corporate", or "cupcake" by default, potentially with a theme switcher later).
- **Navigation:** A persistent sidebar (DaisyUI `Menu` component in a `Drawer` for responsiveness).
  - Navigation Links: Dashboard (future), Project Setup, Run Workflow, Validate Workflow, Show Workflow, Register Workflow, View Workflows, Run History.
- **Main Content Area:** This area will render the content for the selected navigation item.
- **Responsiveness:** The application should be responsive and usable on various screen sizes, leveraging TailwindCSS and DaisyUI's responsive features.

### 3.2. Key Pages/Views and Functionalities

#### 3.2.1. Project Setup Page (`/setup`)

- **UI:**
  - A form with input fields for "Project Name" and "Database Name" (DaisyUI `Input` components).
  - A "Initialize Project" button (DaisyUI `Button`).
  - Display area for success/error messages (DaisyUI `Alert`).
  - (Future: Display current project name and DB name if already configured).
- **Functionality:**
  - Submits data to `POST /api/v1/project/init`.
  - Handles responses and displays feedback.

#### 3.2.2. Run Workflow Page (`/run-workflow`)

- **UI:**
  - Tabs (DaisyUI `Tabs`) for "Run from File" and "Run Registered Workflow".
  - **Run from File Tab:**
    - File input (custom styled or DaisyUI `FileInput`) for `.py` workflow file.
    - Optional text inputs for "Resume ID" and "Resume After Block Name".
  - **Run Registered Workflow Tab:**
    - Dropdown (DaisyUI `Select`) to select Workflow Name (populated from `GET /api/v1/workflows`).
    - Dropdown to select Workflow Version (populated based on selected name from `GET /api/v1/workflows/{name}/versions`).
    - Optional text inputs for "Resume ID" and "Resume After Block Name".
  - A "Run Workflow" button.
  - Display area for run results: Run ID, workflow name, status, message. Link to the "Run Details Page" using the Run ID.
- **Functionality:**
  - Submits data to `POST /api/v1/workflows/run/file` or `POST /api/v1/workflows/run/registered`.
  - Handles file uploads for the "Run from File" scenario.
  - Manages state for form inputs and API responses.

#### 3.2.3. Validate Workflow Page (`/validate-workflow`)

- **UI:**
  - File input for `.py` workflow file.
  - "Validate" button.
  - Display area for validation results:
    - Validity status (e.g., "Valid" / "Invalid").
    - Workflow Name, Blocks Count.
    - Dependency Flow (text).
    - Mermaid Diagram (rendered using a library like `mermaid` or `@mermaid-js/mermaid-cli` if server-side rendering is preferred for complex diagrams, or client-side rendering).
    - List of errors, if any.
- **Functionality:**
  - Submits file to `POST /api/v1/workflows/validate/file`.
  - Displays structured validation results.

#### 3.2.4. Show Workflow Details Page (`/show-workflow`)

- **UI:**
  - File input for `.py` workflow file.
  - Checkbox for "Diagram Only?" (DaisyUI `Checkbox`).
  - "Show Details" button.
  - Display area:
    - If "Diagram Only": Rendered Mermaid Diagram.
    - Else: Workflow Name, Total Blocks.
      - Execution Order: Table (DaisyUI `Table`) showing Order, Block Name, Dependencies.
      - Block Details: Accordion (DaisyUI `Collapse`) or cards for each block, showing Name, Config (formatted JSON/object), Input Map.
      - Rendered Mermaid Diagram.
- **Functionality:**
  - Submits file and `diagram_only` flag to `POST /api/v1/workflows/show/file`.
  - Displays comprehensive workflow details.

#### 3.2.5. Register Workflow Page (`/register-workflow`)

- **UI:**
  - File input for `.py` workflow file.
  - Text input for "Description" (optional).
  - "Register" button.
  - Display area for registration success/error messages and details of the registered version.
- **Functionality:**
  - Submits file and description to `POST /api/v1/workflows/register/file`.

#### 3.2.6. View Workflows Page (`/workflows`)

- **UI:**
  - Table displaying registered workflows: Name, Latest Version, Description, Created At, Updated At.
  - Each workflow name can be a link or have an action button to view its versions.
  - When a workflow is selected:
    - Display a sub-table or modal showing all its versions: Version #, Description, Registered At, Source Path.
    - Option to "Run" a specific version (navigates to Run Workflow page, pre-filled).
    - Option to view "Details" of a specific version (fetches and displays from `GET /api/v1/workflows/{name}/versions/details`).
- **Functionality:**
  - Fetches data from `GET /api/v1/workflows` and `GET /api/v1/workflows/{name}/versions`.
  - Manages display of workflow and version lists.

#### 3.2.7. Run History Page (`/history`)

- **UI:**
  - Table displaying workflow runs: Run ID, Workflow Name, Version ID, Start Time, End Time, Status, Triggered By.
  - Run ID should be a link to the "Run Details Page".
  - (Future: Filtering by status, date range; sorting).
- **Functionality:**
  - Fetches data from `GET /api/v1/history/runs`.

#### 3.2.8. Run Details Page (`/history/runs/{runId}`)

- **UI:**
  - Displays all details for a specific run ID.
  - Key Info: Run ID, Workflow Name, Status, Start/End Times, Parameters.
  - Blocks Section: Table or list of cards for each block in the run: Block Name, Status, Start Time, End Time, Inputs (formatted), Outputs (formatted), Logs (if available, could be expandable).
- **Functionality:**
  - Fetches data from `GET /api/v1/history/runs/{runId}` (where `{runId}` is a path parameter).
  - Presents detailed run information in a readable format.

### 3.3. State Management (Jotai)

- Identify global/shared state:
  - List of registered workflows and their versions.
  - Current project configuration (if displayed globally).
  - User preferences (e.g., theme - future).
- Define Jotai atoms for managing this state and any complex local component state.
- API data fetching can be managed within components or using Jotai atoms with async capabilities.

### 3.4. User Feedback and Interactions

- **Loading States:** Use spinners or skeleton loaders (DaisyUI `Spinner`, `Skeleton`) during API calls.
- **Notifications:** Use toasts or alerts (DaisyUI `Toast`, `Alert`) for success messages, errors, and warnings.
- **Forms:** Clear validation messages for form inputs. Disable submit buttons during submission.

### 3.5. Component Design (Frontend - `frontend/src/components/`)

Identify and create reusable React components. Examples:

- `SidebarNav.tsx`
- `PageLayout.tsx` (includes sidebar and main content area)
- `WorkflowForm.tsx` (generic form for workflow operations needing file + options)
- `WorkflowTable.tsx` (for listing registered workflows)
- `VersionTable.tsx` (for listing versions of a workflow)
- `RunHistoryTable.tsx`
- `MermaidDiagram.tsx` (component to render Mermaid strings)
- `FileInput.tsx` (custom styled file input if needed)
- `LoadingSpinner.tsx`
- `NotificationToast.tsx`

## 4. Development & Project Management Guidelines

### 4.1. Setup Steps

#### 4.1.1. Backend (FastAPI)

1.  Clone the `kwargify-server` repository.
2.  Navigate to the `backend/` directory.
3.  Create and activate a virtual environment using `uv`:
    ```bash
    uv venv
    source .venv/bin/activate # or .venv\Scripts\activate on Windows
    ```
4.  Install dependencies using `uv`:
    ```bash
    uv pip install -r requirements.txt # (or from pyproject.toml if using poetry/pdm sections)
    # Initially, pyproject.toml will be used with `uv pip install .` or `uv pip install -e .`
    # kwargify-core should be added as a dependency (local path for dev, or from PyPI if published)
    ```
5.  Create a `.env` file from `.env.example` if needed for any configurations.
6.  Run the development server: `uvicorn app.main:app --reload` (or as defined in `pyproject.toml` scripts).

#### 4.1.2. Frontend (React + Vite)

1.  Navigate to the `frontend/` directory.
2.  Install dependencies: `npm install` (or `yarn install`).
3.  Run the development server: `npm run dev` (or `yarn dev`).

### 4.2. Task Breakdown (Suggested Order)

1.  **Backend:**
    - Set up basic FastAPI application structure.
    - Implement Pydantic models for API contracts.
    - Implement `Project Setup` endpoints.
    - Implement `Workflow Listing` (workflows and versions) endpoints.
    - Implement `Run History Listing` (summary and details) endpoints.
    - Implement `Workflow Execution` (file and registered) endpoints.
    - Implement `Validation`, `Show`, and `Register` endpoints.
    - Add error handling and logging.
2.  **Frontend:**
    - Set up Vite + React + TS project with TailwindCSS and DaisyUI.
    - Set up Jotai for state management.
    - Implement basic layout (Sidebar, Main Content).
    - Implement `Project Setup` page and connect to backend.
    - Implement `View Workflows` page (listing workflows and versions).
    - Implement `Run History` page (listing runs and run details).
    - Implement `Run Workflow` page.
    - Implement `Validate`, `Show`, `Register` pages.
    - Refine UI/UX, add loading states, notifications.

### 4.3. Testing

- **Backend:**
  - Write unit tests for API endpoints using FastAPI's `TestClient`.
  - Mock interactions with `kwargify_core.services` where appropriate.
  - Aim for good test coverage of critical paths and error conditions.
- **Frontend:**
  - Write component tests using Vitest and React Testing Library.
  - Test user interactions and state changes.

### 4.4. Documentation

- **Backend:**
  - FastAPI automatically generates OpenAPI (Swagger UI/ReDoc) documentation from code and Pydantic models. Ensure docstrings are clear.
  - Update `backend/README.md` with setup and run instructions.
- **Frontend:**
  - Use JSDoc/TSDoc for components and functions.
  - (Optional) Consider Storybook for component development and showcasing if complexity grows.
  - Update `frontend/README.md` with setup and run instructions.
- **Project Root:**
  - Update the main `README.md` with an overview of the project, architecture, and how to get both frontend and backend running.

### 4.5. Version Control (Git)

- Use a branching strategy (e.g., Gitflow: `main`, `develop`, feature branches `feature/XYZ`).
- Create feature branches for each distinct piece of functionality.
- Make small, atomic commits with clear messages.
- Use Pull Requests (PRs) for merging feature branches into `develop`. PRs should be reviewed.
- Merge `develop` into `main` for releases.

### 4.6. Code Quality

- **Backend:** Use `ruff` for linting and formatting. Configure in `pyproject.toml`.
- **Frontend:** Use ESLint and Prettier for linting and formatting. Configure in `package.json` and respective config files.
- Follow consistent coding styles and naming conventions.

## 5. Non-Functional Requirements

- **Usability:** The application should be intuitive and easy to use.
- **Performance:** Frontend should be responsive. API response times should be reasonable (most operations depend on `kwargify-core` performance).
- **Maintainability:** Code should be well-structured, commented, and tested.

## 6. Future Considerations (Out of Scope for Initial Version)

- User Authentication and Authorization.
- Real-time updates for long-running workflows (e.g., using WebSockets).
- Advanced filtering and searching in tables.
- User-configurable themes.
- Dashboard page with summary statistics.
- Deployment strategy (e.g., Docker, serverless).

This document provides a comprehensive starting point. Further clarifications and iterative refinements are expected during the development process.
