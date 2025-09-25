# Hunter.io API Integration Service

## Overview

This API service provides seamless integration with Hunter.io, enabling companies to leverage advanced email verification, discovery, and enrichment capabilities programmatically.

## Features

### Lead Management API

Our Hunter.io API Integration provides a robust set of endpoints for managing leads with full CRUD (Create, Read, Update, Delete) functionality.

#### 1. Create Lead
- **Endpoint:** `POST /leads`
- **Description:** Create a new lead in the Hunter.io system
- **Key Features:**
  - Supports comprehensive lead information
  - Validates lead data before submission
  - Returns created lead details
- **Example Payload:**
  ```json
  {
    "email": "alexis@reddit.com",
    "first_name": "Alexis",
    "last_name": "Ohanian",
    "position": "Cofounder",
    "company": "Reddit"
  }
  ```

#### 2. Retrieve Lead
- **Endpoint:** `GET /leads/{id}`
- **Description:** Fetch detailed information for a specific lead
- **Key Features:**
  - Retrieve lead details by unique ID
  - Validates lead ID (must be positive integer)
  - Returns comprehensive lead information

#### 3. Update Lead
- **Endpoint:** `PUT /leads/{id}`
- **Description:** Modify existing lead information
- **Key Features:**
  - Update specific fields of a lead
  - Supports partial updates
  - Validates lead ID
- **Example Use Cases:**
  - Update contact information
  - Change job position
  - Modify company details

#### 4. Delete Lead
- **Endpoint:** `DELETE /leads/{id}`
- **Description:** Remove a lead from the system
- **Key Features:**
  - Permanently delete a lead
  - Validates lead ID before deletion
  - Provides confirmation of deletion


## Support

Contact: calfonsoba@constructor.university
