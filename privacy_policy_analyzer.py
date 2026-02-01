#!/usr/bin/env python3
"""
privacy_policy_analyzer.py

Simple command‑line tool to flag potentially sensitive data practices in a privacy policy.

This script splits the input policy text into sentences and checks each sentence for
keywords associated with various categories of data practices. When a sentence
contains one or more keywords, the sentence and its matched categories are
displayed to the user.

Usage:
  python privacy_policy_analyzer.py -f path/to/policy.txt
  python privacy_policy_analyzer.py

If no file is provided, the user will be prompted to paste the policy text
directly. Finish input by entering a blank line.

The categories and keywords are defined in the `categories` dictionary. Feel free
to edit or extend them to improve detection.
"""

import argparse
import re
import sys
from typing import Dict, List, Tuple



def split_sentences(text: str) -> List[str]:
    """Split text into sentences using a simple regex.

    This function looks for sentence boundaries defined by punctuation marks
    (period, exclamation mark, question mark) followed by whitespace and a
    capital letter. It also handles newlines. The approach is heuristic and
    may not be perfect, but it avoids external dependencies.

    Parameters
    ----------
    text : str
        The full privacy policy text.

    Returns
    -------
    List[str]
        A list of sentences.
    """
    # Normalize whitespace
    cleaned = re.sub(r"\s+", " ", text.strip())
    # Split on punctuation followed by a space and a capital letter or end of string
    # Keep the delimiter by using a positive lookahead
    sentence_endings = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")
    sentences = sentence_endings.split(cleaned)
    return [s.strip() for s in sentences if s.strip()]


def analyze_policy(text: str, categories: Dict[str, List[str]]) -> List[Tuple[str, List[str]]]:
    """Analyze the policy text and return sentences that match any category keywords.

    Parameters
    ----------
    text : str
        The full privacy policy text.
    categories : Dict[str, List[str]]
        A mapping from category name to a list of keywords.

    Returns
    -------
    List[Tuple[str, List[str]]]
        A list of (sentence, matched_categories) tuples.
    """
    results: List[Tuple[str, List[str]]] = []
    sentences = split_sentences(text)
    for sentence in sentences:
        lowered = sentence.lower()
        matched = [cat for cat, keywords in categories.items() if any(kw in lowered for kw in keywords)]
        if matched:
            results.append((sentence, matched))
    return results


def get_recommendations(matched_categories: List[str]) -> List[str]:
    """Return a list of privacy and security recommendations based on matched categories.

    Parameters
    ----------
    matched_categories : List[str]
        A list of unique category names flagged in the policy.

    Returns
    -------
    List[str]
        A list of human‑readable recommendations.
    """
    recs: List[str] = []
    # Mapping from category to suggested actions. These recommendations are generic
    # and should be tailored to the specific app and device settings when possible.
    category_recommendations: Dict[str, List[str]] = {
        "Data Sharing": [
            "Review the app's settings for data sharing or personalization. Opt out of sharing personal data with third‑party partners whenever possible.",
            "Disable permissions for unnecessary sensors or data (e.g., contacts, photos) if they are not needed for the app's core functionality."
        ],
        "Data Selling": [
            "Check whether the app offers an option to opt out of the sale of personal information. If so, enable it.",
            "Consider contacting the app developer or using a different service if the policy allows selling your data."
        ],
        "Advertising": [
            "In your device settings, limit ad tracking or disable personalized ads (e.g., 'Limit Ad Tracking' on iOS or 'Opt out of Ads Personalization' on Android).",
            "Within the app, look for advertising preferences and opt out of targeted advertising."
        ],
        "Analytics & Tracking": [
            "Disable analytics or usage tracking in the app's settings if available.",
            "Clear cookies and app data periodically to minimize tracking."
        ],
        "Personal Information": [
            "Provide only the minimum personal information required for the app to function.",
            "Regularly review and update your privacy settings to restrict access to sensitive data."
        ],
        "Location": [
            "Set location permissions to 'While Using the App' or 'Never' unless the app truly needs continuous location access.",
            "Disable precise location access if approximate location suffices for the app's functionality."
        ],
        "Retention": [
            "If the policy indicates long data retention, consider periodically deleting your account or data within the app.",
            "Request account deletion or data export when you stop using the service."
        ],
        "Security": [
            "Enable any available security features such as two‑factor authentication (2FA) or passcodes within the app.",
            "Keep your device and apps updated to ensure you have the latest security patches."
        ],
    }
    for category in matched_categories:
        recs.extend(category_recommendations.get(category, []))
    # Deduplicate recommendations while preserving order
    seen: set = set()
    deduped: List[str] = []
    for rec in recs:
        if rec not in seen:
            seen.add(rec)
            deduped.append(rec)
    return deduped


def load_text_from_file(path: str) -> str:
    """Read the contents of a text file.

    Parameters
    ----------
    path : str
        Path to the text file.

    Returns
    -------
    str
        The contents of the file.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def prompt_for_text() -> str:
    """Prompt the user to paste policy text.

    Continues reading from stdin until an empty line is encountered.

    Returns
    -------
    str
        The concatenated text.
    """
    print("Paste the privacy policy text. Enter a blank line to finish:\n")
    lines = []
    for line in sys.stdin:
        # stop on blank line
        if line.strip() == "":
            break
        lines.append(line.rstrip("\n"))
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Privacy Policy Analyzer")
    parser.add_argument("-f", "--file", dest="file_path", help="Path to privacy policy text file", required=False)
    args = parser.parse_args()

    # Define categories and associated keywords. Keywords should be lowercase.
    categories: Dict[str, List[str]] = {
        "Data Sharing": [
            "share", "third party", "third-party", "partner", "vendor", "affiliate", "disclose", "provide"
        ],
        "Data Selling": [
            "sell", "sale", "monetize", "commercialize"
        ],
        "Advertising": [
            "advertising", "advertisement", "advertiser", "marketing", "promotional"
        ],
        "Analytics & Tracking": [
            "analytics", "tracking", "cookie", "beacon", "pixel", "sdk"
        ],
        "Personal Information": [
            "personal information", "personal data", "pii", "personally identifiable", "sensitive information"
        ],
        "Location": [
            "location", "geolocation", "gps"
        ],
        "Retention": [
            "retain", "retention", "store", "storage", "keep", "period", "duration"
        ],
        "Security": [
            "security", "protect", "encryption", "breach"
        ],
    }

    if args.file_path:
        try:
            text = load_text_from_file(args.file_path)
        except OSError as e:
            print(f"Error reading file: {e}")
            return
    else:
        text = prompt_for_text()
        if not text.strip():
            print("No text provided. Exiting.")
            return

    results = analyze_policy(text, categories)
    if not results:
        print("\nNo potentially sensitive practices were detected based on the current heuristics.")
    else:
        print("\nPotential data privacy concerns detected:\n")
        for i, (sentence, matched) in enumerate(results, start=1):
            cats = ", ".join(matched)
            print(f"{i}. {sentence}\n   Categories: {cats}\n")

        # Extract unique categories from matches
        unique_categories = []
        for _, matched in results:
            for cat in matched:
                if cat not in unique_categories:
                    unique_categories.append(cat)
        recommendations = get_recommendations(unique_categories)
        if recommendations:
            print("Recommended actions to protect your data:\n")
            for idx, rec in enumerate(recommendations, start=1):
                print(f"- {rec}")


if __name__ == "__main__":
    main()
