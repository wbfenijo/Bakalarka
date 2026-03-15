import pandas as pd
from openai_client import *
from load_data import *


PROMPT_ZS1 = """Generate a PlantUML sequence diagram based on the following user story.

User story:
{USER_STORY}

Return only valid PlantUML code for the sequence diagram."""

# sequenceDiagram_1 = client.prompt(useCase1)

# sequenceDiagram_2 = client.prompt(useCase2)

# with open(r"data/outputsAI/SD1.puml", "w") as f:
#     f.write(sequenceDiagram_1)

# with open(r"data/outputsAI/SD2.puml", "w") as f:
#     f.write(sequenceDiagram_2)


PROMPT_ZS2 = """Generate a PlantUML sequence diagram representing the interactions described in the following user story.

User story:
{USER_STORY}

The output must:
- Represent the main actors and system components
- Include the correct sequence of messages
- Follow valid PlantUML syntax

Return only the PlantUML code of the sequence diagram."""

PROMPT_ZS3 = """You are a software engineer specializing in UML modeling.

Based on the following user story, generate a sequence diagram in PlantUML that captures the interactions between actors and system components.

User story:
{USER_STORY}

Return only the PlantUML code."""

PROMPT_ZS4 = """Create a PlantUML sequence diagram for the following user story.

User story:
{USER_STORY}

Identify:
- the actors
- the system components
- the sequence of interactions between them

Then generate the corresponding PlantUML sequence diagram.

Return only the PlantUML code."""

PROMPT_ZS5 = """Generate a sequence diagram in PlantUML for the following user story.

User story:
{USER_STORY}

Rules:
- Output must contain only valid PlantUML code
- Do not include explanations or comments
- The diagram must begin with @startuml and end with @enduml"""

