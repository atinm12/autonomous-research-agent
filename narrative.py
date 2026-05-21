def build_narrative(data_points):

    narrative = ""

    for point in data_points:

        narrative += (
            f"{point}\n\n"
        )

    return narrative