# Privacy Policy Analyzer

The **Privacy Policy Analyzer** is a lightweight command‑line application that helps non‑technical users quickly identify potential data‑privacy issues in the privacy policies of mobile or web apps.  
It scans the text of a privacy policy, looks for sentences that mention sensitive topics—such as data sharing, tracking, advertising, selling personal information, retention, and security practices—and highlights those sentences for review. The goal is to help users understand how an app may handle their personal data before downloading or using the app.

## Features

* **Ease of use:** Provide a policy by copying and pasting the text or by passing a `.txt` file as an argument.
* **Heuristic detection:** Uses simple keyword matching to flag sentences that suggest data sharing with third parties, sale of personal information, targeted advertising, tracking technologies (cookies, beacons, etc.), location data, data retention, or security practices.  
  (For more advanced automated scraping and analysis, see research projects such as **PoliPy**, a Python library developed by the Berkeley Lab for Usable and Experimental Security to scrape, parse and analyze privacy policies.)
* **Open source:** Licensed under the MIT License. Feel free to fork, adapt or extend it.
* **Actionable recommendations:** After analyzing a policy, the tool suggests steps you can take on your device or within the app to mitigate privacy risks—such as limiting ad tracking, adjusting permissions, or enabling stronger security features.

## Installation

You only need Python 3.7 or newer. The script has no external dependencies beyond the Python standard library. Clone or download this repository, then run the script:

```
python privacy_policy_analyzer.py --help
```

## Usage

### Analyze a policy file

If you have a text file containing a privacy policy (for example, exported from a website or copied from an app store page), run:

```
python privacy_policy_analyzer.py -f path/to/policy.txt
```

The application will parse the file, examine each sentence, and print any sentences that contain potential privacy concerns along with the relevant categories.

It then summarizes which categories were found and provides practical recommendations to help you adjust your settings or usage to better protect your data.

### Paste text interactively

If you don’t have a file, omit the `-f` flag. You will be prompted to paste the policy text. Finish by entering a blank line (press **Enter** twice):

```
python privacy_policy_analyzer.py
```

## How it works

The analyzer defines several categories of potentially sensitive practices and associates each category with a list of keywords.  
When the user provides the privacy policy text, the script splits it into sentences and checks each sentence for the presence of any keywords.  
If a sentence contains one or more keywords, it is reported along with the categories it matched.

You can adjust the categories and keywords by editing the `categories` dictionary in `privacy_policy_analyzer.py`.

You can also customize the privacy recommendations in the `get_recommendations` function within `privacy_policy_analyzer.py`. Each category maps to a list of suggested actions, and the tool will aggregate and deduplicate them based on the concerns detected.

## Limitations

* This tool uses a simple keyword‑based approach. It may produce false positives (flagging benign sentences) and false negatives (missing nuanced or implicit data practices).
* It does not automatically fetch privacy policies from app store pages. To obtain the policy text, copy and paste it yourself.  
  Researchers working at the BLUES lab developed **PoliPy**, which provides a command‑line interface and API to scrape, parse, and analyze privacy policies. That project is more complex and requires Selenium and a browser driver.
* It does not provide legal advice. Always read the full privacy policy and consult a professional if you have specific concerns.

## License

This project is licensed under the MIT License. See the [`LICENSE`](LICENSE) file for details.
  
