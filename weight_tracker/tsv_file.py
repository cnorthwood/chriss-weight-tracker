def write_tsv(filename, data):
    with open(filename, "w") as output_tsv:
        for d in data:
            fields = [
                d["date"],
                d["weight"],
                d["bmi"],
                "",
                d["moving_average_weight"],
                d["moving_average_bmi"],
                "",
                d["weekly_weight_delta"],
                d["weekly_bmi_delta"],
                "",
                d["monthly_weight_delta"],
                d["monthly_bmi_delta"],
            ]
            output_tsv.write("\t".join(fields) + "\n")
