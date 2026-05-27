def generate_report(title, findings):

    report = f"# {title}\n\n"

    report += "## Research Findings\n\n"

    for item in findings:

        report += f"- {item}\n"

    return report