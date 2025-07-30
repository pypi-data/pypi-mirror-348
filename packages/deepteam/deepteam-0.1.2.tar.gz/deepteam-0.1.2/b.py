#!/usr/bin/env python3
"""
Test script to verify that supported vulnerability types can generate attacks using the OpenAI model.
This performs a local attack simulation test for vulnerability types in the template.
"""

import os
import time
import argparse
import sys
from typing import List, Dict, Any, Optional, Tuple

from deepeval.models import GPTModel
from deepteam.attacks.attack_simulator.attack_simulator import AttackSimulator
from deepteam.attacks.attack_simulator.template import AttackSimulatorTemplate
from deepteam.vulnerabilities import (
    Bias,
    Misinformation,
    Toxicity,
    PIILeakage,
    PromptLeakage,
    UnauthorizedAccess,
    Competition,
    IllegalActivity,
    ExcessiveAgency,
    GraphicContent,
    IntellectualProperty,
    PersonalSafety,
    Robustness,
)

from deepteam.vulnerabilities.types import (
    BiasType,
    CompetitionType,
    ExcessiveAgencyType,
    GraphicContentType,
    IllegalActivityType,
    IntellectualPropertyType,
    MisinformationType,
    PersonalSafetyType,
    PIILeakageType,
    PromptLeakageType,
    RobustnessType,
    ToxicityType,
    UnauthorizedAccessType,
    VulnerabilityType,
)

from deepteam.vulnerabilities.bias import BiasTemplate
from deepteam.vulnerabilities.competition import CompetitionTemplate
from deepteam.vulnerabilities.excessive_agency import ExcessiveAgencyTemplate
from deepteam.vulnerabilities.graphic_content import GraphicContentTemplate
from deepteam.vulnerabilities.illegal_activity import IllegalActivityTemplate
from deepteam.vulnerabilities.intellectual_property import (
    IntellectualPropertyTemplate,
)
from deepteam.vulnerabilities.misinformation import MisinformationTemplate
from deepteam.vulnerabilities.personal_safety import PersonalSafetyTemplate
from deepteam.vulnerabilities.pii_leakage import PIILeakageTemplate
from deepteam.vulnerabilities.prompt_leakage import PromptLeakageTemplate
from deepteam.vulnerabilities.robustness import RobustnessTemplate
from deepteam.vulnerabilities.toxicity import ToxicityTemplate
from deepteam.vulnerabilities.unauthorized_access import (
    UnauthorizedAccessTemplate,
)

# Configuration
MAX_GOLDENS = 3
DEFAULT_PURPOSE = "chatbot assistant"

# Maps vulnerability type names to their enum values
VULNERABILITY_TYPE_MAPPING = {
    "bias": {
        "gender": BiasType.GENDER,
        "religion": BiasType.RELIGION,
        "race": BiasType.RACE,
        "politics": BiasType.POLITICS,
    },
    "competition": {
        "competitor_mention": CompetitionType.COMPETITOR_MENTION,
        "market_manipulation": CompetitionType.MARKET_MANIPULATION,
        "discreditation": CompetitionType.DISCREDITATION,
        "confidential_strategies": CompetitionType.CONFIDENTIAL_STRATEGIES,
    },
    "excessive_agency": {
        "functionality": ExcessiveAgencyType.FUNCTIONALITY,
        "permissions": ExcessiveAgencyType.PERMISSIONS,
        "autonomy": ExcessiveAgencyType.AUTONOMY,
    },
    "graphic_content": {
        "sexual_content": GraphicContentType.SEXUAL_CONTENT,
        "graphic_content": GraphicContentType.GRAPHIC_CONTENT,
        "pornographic_content": GraphicContentType.PORNOGRAPHIC_CONTENT,
    },
    "illegal_activity": {
        "weapons": IllegalActivityType.WEAPONS,
        "illegal_drugs": IllegalActivityType.ILLEGAL_DRUGS,
        "violent_crime": IllegalActivityType.VIOLENT_CRIME,
        "non_violent_crime": IllegalActivityType.NON_VIOLENT_CRIME,
        "sex_crime": IllegalActivityType.SEX_CRIME,
        "cybercrime": IllegalActivityType.CYBERCRIME,
        "child_exploitation": IllegalActivityType.CHILD_EXPLOITATION,
    },
    "intellectual_property": {
        "imitation": IntellectualPropertyType.IMITATION,
        "copyright_violations": IntellectualPropertyType.COPYRIGHT_VIOLATIONS,
        "trademark_infringement": IntellectualPropertyType.TRADEMARK_INFRINGEMENT,
        "patent_disclosure": IntellectualPropertyType.PATENT_DISCLOSURE,
    },
    "misinformation": {
        "factual_errors": MisinformationType.FACTUAL_ERRORS,
        "unsupported_claims": MisinformationType.UNSUPPORTED_CLAIMS,
        "expertise_misrepresentation": MisinformationType.EXPERTIZE_MISREPRESENTATION,
    },
    "personal_safety": {
        "bullying": PersonalSafetyType.BULLYING,
        "self_harm": PersonalSafetyType.SELF_HARM,
        "unsafe_practices": PersonalSafetyType.UNSAFE_PRACTICES,
        "dangerous_challenges": PersonalSafetyType.DANGEROUS_CHALLENGES,
        "stalking": PersonalSafetyType.STALKING,
    },
    "pii_leakage": {
        "direct": PIILeakageType.DIRECT,
        "database_access": PIILeakageType.DATABASE_ACCESS,
        "social_manipulation": PIILeakageType.SOCIAL_MANIPULATION,
        "session_leak": PIILeakageType.SESSION_LEAK,
    },
    "prompt_leakage": {
        "secrets_and_credentials": PromptLeakageType.SECRETS_AND_CREDENTIALS,
        "instructions": PromptLeakageType.INSTRUCTIONS,
        "guard_exposure": PromptLeakageType.GUARD_EXPOSURE,
        "permissions_and_roles": PromptLeakageType.PERMISSIONS_AND_ROLES,
    },
    "robustness": {
        "input_overreliance": RobustnessType.INPUT_OVERRELIANCE,
        "hijacking": RobustnessType.HIJACKING,
    },
    "toxicity": {
        "insults": ToxicityType.INSULTS,
        "profanity": ToxicityType.PROFANITY,
        "threats": ToxicityType.THREATS,
        "mockery": ToxicityType.MOCKERY,
    },
    "unauthorized_access": {
        "bfla": UnauthorizedAccessType.BFLA,
        "bola": UnauthorizedAccessType.BOLA,
        "rbac": UnauthorizedAccessType.RBAC,
        "debug_access": UnauthorizedAccessType.DEBUG_ACCESS,
        "shell_injection": UnauthorizedAccessType.SHELL_INJECTION,
        "sql_injection": UnauthorizedAccessType.SQL_INJECTION,
        "ssrf": UnauthorizedAccessType.SSRF,
    },
}


def get_all_vulnerability_types() -> str:
    """Return a formatted string listing all available vulnerability types and subtypes."""
    result = "Available vulnerability types and subtypes:\n\n"
    for vul_type, subtypes in VULNERABILITY_TYPE_MAPPING.items():
        result += f"{vul_type}:\n"
        for subtype in subtypes:
            result += f"  - {subtype}\n"
        result += "\n"
    return result


def get_vulnerability_from_args(
    vul_type: str, subtype: str
) -> Optional[VulnerabilityType]:
    """Convert command line arguments to a vulnerability type enum."""
    if vul_type not in VULNERABILITY_TYPE_MAPPING:
        print(f"Error: '{vul_type}' is not a valid vulnerability type.")
        return None

    if subtype not in VULNERABILITY_TYPE_MAPPING[vul_type]:
        print(f"Error: '{subtype}' is not a valid subtype for {vul_type}.")
        print(f"Available subtypes for {vul_type}:")
        for available_subtype in VULNERABILITY_TYPE_MAPPING[vul_type]:
            print(f"  - {available_subtype}")
        return None

    return VULNERABILITY_TYPE_MAPPING[vul_type][subtype]


def separator():
    """Print a separator line for better readability."""
    print("\n" + "=" * 80 + "\n")


def test_local_baseline_attacks(purpose: str):
    """Test local baseline attack generation using OpenAI for key vulnerability types"""
    print(
        f"Testing local baseline attack generation with OpenAI for purpose: {purpose}\n"
    )

    # Check if OpenAI API key is set
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        api_key = input("Please enter your OpenAI API key: ")
        os.environ["OPENAI_API_KEY"] = api_key

    # Create a simulator with an OpenAI model
    openai_model = GPTModel(model_name="gpt-3.5-turbo")
    simulator = AttackSimulator(
        purpose=purpose, max_concurrent=3, simulator_model=openai_model
    )

    # Create all vulnerabilities to test, grouped by category for easier debugging
    vulnerabilities = []

    # Group 1: Basic vulnerabilities already verified to work
    basic_vulnerabilities = [
        Bias(types=["religion"]),
        Misinformation(types=["factual errors"]),
        Toxicity(types=["profanity"]),
        PIILeakage(types=["direct disclosure"]),
    ]
    vulnerabilities.extend(basic_vulnerabilities)

    # Group 2: PromptLeakage vulnerabilities
    prompt_leakage_vulnerabilities = [
        PromptLeakage(types=["secrets and credentials"]),
        PromptLeakage(types=["instructions"]),
        PromptLeakage(types=["guard exposure"]),
        PromptLeakage(types=["permissions and roles"]),
    ]
    vulnerabilities.extend(prompt_leakage_vulnerabilities)

    # Group 3: UnauthorizedAccess vulnerabilities
    unauthorized_access_vulnerabilities = [
        UnauthorizedAccess(types=["debug access"]),
        UnauthorizedAccess(
            types=["bola"]
        ),  # Correct string for "broken object level authorization"
        UnauthorizedAccess(
            types=["bfla"]
        ),  # Correct string for "broken function level authorization"
        UnauthorizedAccess(
            types=["rbac"]
        ),  # Correct string for "role-based access control"
        UnauthorizedAccess(types=["shell injection"]),
        UnauthorizedAccess(types=["sql injection"]),
    ]
    vulnerabilities.extend(unauthorized_access_vulnerabilities)

    # Group 4: Competition vulnerabilities
    competition_vulnerabilities = [
        Competition(types=["competitor mention"]),
        Competition(types=["market manipulation"]),
        Competition(types=["discreditation"]),
        Competition(types=["confidential strategies"]),
    ]
    vulnerabilities.extend(competition_vulnerabilities)

    # Group 5: RobustnessType vulnerabilities
    robustness_vulnerabilities = [
        Robustness(types=["input overreliance"]),
        Robustness(types=["hijacking"]),
    ]
    vulnerabilities.extend(robustness_vulnerabilities)

    # Group 6: ExcessiveAgency vulnerabilities
    excessive_agency_vulnerabilities = [
        ExcessiveAgency(types=["functionality"]),
        ExcessiveAgency(types=["permissions"]),
        ExcessiveAgency(types=["autonomy"]),
    ]
    vulnerabilities.extend(excessive_agency_vulnerabilities)

    # Group 7: GraphicContent vulnerabilities
    graphic_content_vulnerabilities = [
        GraphicContent(types=["sexual content"]),
        GraphicContent(types=["graphic content"]),
        GraphicContent(types=["pornographic content"]),
    ]
    vulnerabilities.extend(graphic_content_vulnerabilities)

    # Group 8: IllegalActivity vulnerabilities - only test a few selected types
    illegal_activity_vulnerabilities = [
        IllegalActivity(types=["weapons"]),
        IllegalActivity(types=["illegal drugs"]),
        IllegalActivity(types=["violent crimes"]),
        IllegalActivity(types=["cybercrime"]),
    ]
    vulnerabilities.extend(illegal_activity_vulnerabilities)

    # Group 9: IntellectualProperty vulnerabilities
    intellectual_property_vulnerabilities = [
        IntellectualProperty(types=["copyright violations"]),
        IntellectualProperty(types=["trademark infringement"]),
        IntellectualProperty(types=["patent disclosure"]),
        IntellectualProperty(types=["imitation"]),
    ]
    vulnerabilities.extend(intellectual_property_vulnerabilities)

    # Group 10: PersonalSafety vulnerabilities
    personal_safety_vulnerabilities = [
        PersonalSafety(types=["bullying"]),
        PersonalSafety(types=["self-harm"]),
        PersonalSafety(types=["dangerous challenges"]),
        PersonalSafety(types=["stalking"]),
    ]
    vulnerabilities.extend(personal_safety_vulnerabilities)

    print(f"Testing {len(vulnerabilities)} vulnerability types")

    # Track results
    successful = []
    failed = []

    # Generate baseline attacks locally
    print("Generating baseline attacks locally for each vulnerability type...")

    for i, vulnerability in enumerate(vulnerabilities):
        print(f"\n[{i+1}/{len(vulnerabilities)}] Testing: {vulnerability}")
        try:
            attacks = simulator.simulate_baseline_attacks(
                attacks_per_vulnerability_type=1,
                vulnerability=vulnerability,
                ignore_errors=False,  # We want to catch errors
            )

            if attacks:
                successful.append((vulnerability, attacks[0]))
                print(f"✅ SUCCESS: Generated attack")
                print(f"Input: {attacks[0].input}")
            else:
                failed.append((vulnerability, "No attacks generated"))
                print(f"❌ FAILED: No attacks generated")
        except Exception as e:
            failed.append((vulnerability, str(e)))
            print(f"❌ ERROR: {str(e)}")

        # Add a small delay to avoid rate limiting
        time.sleep(1)

    # Print summary
    print("\n\n=== SUMMARY ===")
    print(f"Total vulnerability types tested: {len(vulnerabilities)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")

    if failed:
        print("\n=== FAILED VULNERABILITY TYPES ===")
        for vulnerability, error in failed:
            print(f"- {vulnerability}: {error}")

    print("\nDone!")


def test_specific_vulnerability(
    vul_type: VulnerabilityType, max_goldens: int, purpose: str
):
    """Test a specific vulnerability type."""
    separator()
    print(f"Testing vulnerability type: {vul_type}")
    print(f"Purpose: {purpose}")
    print(f"Max goldens: {max_goldens}")
    separator()

    # Get the appropriate template class for this vulnerability type
    for (
        type_class,
        template_class,
    ) in AttackSimulatorTemplate.TEMPLATE_MAP.items():
        if isinstance(vul_type, type_class):
            prompt_template = template_class.generate_baseline_attacks(
                vul_type, max_goldens, purpose
            )
            print(prompt_template)
            return

    print(f"Error: No template found for vulnerability type {vul_type}")


def simulate_local_attacks(vul_type: str, subtype: str, purpose: str):
    """Simulate local attacks for a given vulnerability type and subtype."""
    vulnerability = get_vulnerability_from_args(vul_type, subtype)
    if not vulnerability:
        print("Invalid vulnerability type or subtype.")
        return

    # Initialize the attack simulator
    simulator = AttackSimulator(purpose=purpose, max_concurrent=3)

    # Simulate local attacks
    try:
        attacks = simulator.simulate_local_attack(
            purpose, vulnerability, MAX_GOLDENS
        )
        print(f"Simulated attacks for {vul_type} ({subtype}):")
        for attack in attacks:
            print(attack)
    except Exception as e:
        print(f"Error during simulation: {str(e)}")


def main():
    parser = argparse.ArgumentParser(
        description="Simulate local attacks for a given vulnerability type and subtype."
    )
    parser.add_argument("vul_type", type=str, help="The vulnerability type.")
    parser.add_argument("subtype", type=str, help="The vulnerability subtype.")
    parser.add_argument(
        "purpose", type=str, help="The purpose for generating the prompts."
    )
    args = parser.parse_args()

    simulate_local_attacks(args.vul_type, args.subtype, args.purpose)


if __name__ == "__main__":
    main()
