# MassLaw

MassLaw is a full-stack project aimed at putting state-of-the-art machine learning and artificial intelligence technology in the hands of ordinary legal professionals.

This repository is the main mono-repo of the project, consisting of the entirety of MassLaw's production code.

## Product

MassLaw's product is a platform aimed to be used by people who deal with content-heavy legal cases. Interfaced with an easy-to-use and understandable web-front, that implements secure login and account management it provides easy access to high-end technology for people whose careers are in the legal industry.

### Case Content

MassLaw allows users to create and manage their cases and the content they consist of in a straightforward and intuitive way.

The content of MassLaw's cases can be any type of file your case has within it. Textual files (PDF, TXT, any type of office file...), Images, Videos, Audio Files, etc...

MassLaw supports intuitive features that allow users to easily partition their case content and organize it into a directory file hierarchy (recursive folder tree).

### Collaboration

In addition to letting users easily manage their cases, MassLaw allows the collaboration of multiple users in a permission-based manner. Allowing the owner of any case to add other users with any of the following permissions:

• Owner - every case has and only has a single owner. The owner is inherently the person who originally created the case, they have full access to the case's management features and content. The "Owner" access level is the highest and most senior access level of any case

• Manager - the manager access level can only be given to users either by the owner of the case or by any of the other managers. They have access to changing the case information, to change the access levels of other colaborators in the case (except the owner's) and the have no access restrictions to the case's content.

• Editor - editors have read and write access to the case. They can upload content to the non-restricted portions of the case's storage and edit their properties in addition to full read-access and commenting on files already in the case in those same non-restricted parts of the case. Editors have no management access to the case. They cannot edit the case's settings (including managing the case collaborators)

• Reader - readers have the lowest level of access to the case. They can only read files and post comments on them

### Content Processing

MassLaw's most powerful features are the case-content-processing abilities it provides. As soon as any type of file is added to any case, it immediately initiates a processing pipeline through which it works its way in MassLaw's backend. 

This processing pipeline, "squeezes" any insight or piece of relevant information from the files that make their way through it. Using state-of-the-art technologies, MassLaw extends its user's talent by giving them straight-forward and infered insights about the contents of their case.

The following is a list of features currently implemented using the case-processing abilities of MassLaw:

• Text Extraction - allowing users to gain direct access to textual content in files that don't have it by default (such as images and scanned documents, as well as hybrid documents that have both typed text and scanned text)

• Full Text Search - MassLaw loads both existing and extracted text content in its files to a full-text-search index which lets the case collaborators search for appearances of any text they like throughout the entirety of the content to which they have access.

• Text Processing - MassLaw processes the text contained in any of the case's files identifying entities mentioned in it, their relevance in the case and the connections between them, providing deep insights out-of-the-box.

• Relations Graph - MassLaw uses the extracted insights to construct an intuitive and readable graph representation of the entities inside the case and their relations (example: "**Emily** saw a car with the license plate **I35-759** at **06-12-24 at 3 AM** near the **Town Hall**, which is **one hour** before the **crime**")

• Event Timeline - MassLaw constructs a timeline of events that occurred in a case, which it interferes from the text contained within the processed case's content.

• LLM Conversations - MassLaw utilizes OpenAI's API to allow users to perform conversations with a GPT model about the case. The model is briefly exposed to the textual highlights from the case which are indexed **by meaning** in real time based on the user's prompt, allowing the model to gain insights and provide qualitative responses about actual information within the case. The conversations and their content are securely managed within MassLaw's backend services.

The following is a list of technologies used to provide MassLaw with its capabilities:

• OCR - Allowing Text Extraction - Using **Tesseract**

• NLP - Allowing Text Processing - Using **SpaCy**

• Full Text Search Index - Allowing Full-Text-Search in real time - Using **Amazon's OpenSearch Service**

• Text Embeddings Vector-Based Indexing And Querying - Allowing Index and Query Text By Meaning - Using OpenAI's embeddings API to generate embedding vectors used to index text within **Amazon's OpenSearch Service** allowing fast queries in real time.

• Graph Database Storage - Allowing The Storage Of Entities And Relations in a Graph Queriable Way - Using **Amazon's Neptune** and **Gremlin Query**

• Pipeline Orchestration And Management - Allowing easy building, orchestrating, and manipulating of the case-processing-pipeline - Using **Amazon's Step-Functions Service** and **Amazon's Lambda Service**

• Job Execution And Resources Orchestration - Allowing easy resource management, load balancing, queuing and fault tolerating of processing jobs of any kind - Using **Amazon's Batch Service**

• Information Management and Implementation - Allowing the files to properly undergo the information extracting processes within the pipeline - Using the developed in-house MLCP Engine - "MassLaw's Content Processing Engine"

### Working With Files

After uploaded and processed, the files can be displayed on-demand on the web front in a displayer dedicated to displaying the file's information structured in a way specific to MassLaw developed in-house.

The file display view provides intuitive ways to mark text within the files in addition to commenting on it. Comments can be viewed by all collaborators in the case (who have access to viewing the specific file commented), it is a central feature boosting the collaboration capabilities of the product.

Files also have their own sub-displays of features implemented for the entire case, designed to show the same information, specifically for the file being viewed (such as full-text-search, relations graph, timeline, etc...)


