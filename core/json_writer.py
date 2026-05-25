import json
import os


class JSONWriter:

    def save(self, data):

        os.makedirs("output", exist_ok=True)

        with open(
            "output/results.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

        print(
            "\n[JSON SAVED] output/results.json"
        )